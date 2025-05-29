"""
KRX 데이터 서비스
pykrx 라이브러리를 래핑하여 한국거래소(KRX)의 데이터를 가져오는 서비스

이 모듈은 주식 및 지수 데이터를 조회하는 기능을 제공합니다.
주요 기능:
- 종목 목록 조회
- 개별 종목 가격 데이터 조회
- KOSPI 지수 데이터 조회
- 날짜 및 종목코드 유효성 검증

**예제:**

.. code-block:: python

    >>> from app.services.krx_service import KRXService
    >>> # 종목 목록 조회
    >>> stock_list = KRXService.get_stock_list()
    >>> print(f"총 {stock_list.count}개 종목이 조회되었습니다")
    총 900개 종목이 조회되었습니다

    >>> # 삼성전자 주가 데이터 조회
    >>> prices = KRXService.get_stock_price("005930", "20230101", "20230131")
    >>> print(f"{prices.name} 주가 데이터: {len(prices.prices)}일치")
    삼성전자 주가 데이터: 21일치
"""
from datetime import datetime
from pykrx import stock
from ..models.index import IndexPrice, IndexResponse
from ..models.stock import (StockInfo, StockPrice,
                              StockPriceResponse, StockListResponse)


class KRXService:
    """
    KRX 데이터 서비스 클래스

    한국거래소(KRX)의 데이터를 조회하는 정적 메서드들을 제공하는 클래스입니다.
    모든 메서드는 static method로 구현되어 있어 인스턴스 생성 없이 바로 사용할 수 있습니다.

    **예제:**

    .. code-block:: python

        >>> from app.services.krx_service import KRXService
        >>> # 종목 목록 조회
        >>> stocks = KRXService.get_stock_list()
        >>> print(f"첫 번째 종목: {stocks.stocks[0].name}")
        첫 번째 종목: 삼성전자

        >>> # 종목코드 유효성 검증
        >>> is_valid = KRXService.validate_stock_code("005930")
        >>> print(f"유효한 종목코드: {is_valid}")
        유효한 종목코드: True
    """

    @staticmethod
    def get_stock_list() -> StockListResponse:
        """
        거래소별 상장 종목 리스트 조회

        현재 KOSPI 시장에 상장된 모든 종목의 리스트를 조회합니다.

        :return: 종목 리스트 응답
        :rtype: StockListResponse
        :raises Exception: 종목 리스트 조회 실패 시 발생

        **예제:**

        .. code-block:: python

            >>> from app.services.krx_service import KRXService
            >>> # 종목 리스트 조회
            >>> response = KRXService.get_stock_list()
            >>> print(f"총 {response.count}개 종목이 조회되었습니다")
            총 900개 종목이 조회되었습니다
            >>> # 첫 5개 종목 출력
            >>> for s in response.stocks[:5]:
            ...     print(f"종목코드: {s.code}, 종목명: {s.name}")
            종목코드: 005930, 종목명: 삼성전자
            종목코드: 000660, 종목명: SK하이닉스
            종목코드: 051910, 종목명: LG화학
            종목코드: 035420, 종목명: NAVER
            종목코드: 005380, 종목명: 현대차
        """
        try:
            # 오늘 날짜로 종목 리스트 조회
            today = datetime.now().strftime("%Y%m%d")
            tickers = stock.get_market_ticker_list(today, market="KOSPI")

            stocks = []
            for ticker in tickers:
                try:
                    name = stock.get_market_ticker_name(ticker)
                    stocks.append(StockInfo(
                        code=ticker,
                        name=name,
                    ))
                except Exception as e:
                    # 개별 종목 조회 실패시 스킵
                    print(f"종목 {ticker} 조회 실패: {e}")
                    continue

            return StockListResponse(
                count=len(stocks),
                stocks=stocks
            )

        except Exception as e:
            raise Exception(f"종목 리스트 조회 실패: {str(e)}")

    @staticmethod
    def get_stock_price(
            code: str,
            start_date: str,
            end_date: str
    ) -> StockPriceResponse:
        """
        개별 종목의 주가 데이터 조회

        지정된 기간 동안의 특정 종목의 일별 주가 데이터(OHLCV)를 조회합니다.

        :param code: 종목코드 (예: '005930')
        :type code: str
        :param start_date: 시작일 (YYYYMMDD 형식)
        :type start_date: str
        :param end_date: 종료일 (YYYYMMDD 형식)
        :type end_date: str
        :return: 주가 데이터 응답
        :rtype: StockPriceResponse
        :raises Exception: 종목코드가 유효하지 않거나 데이터 조회 실패 시 발생

        **예제:**

        .. code-block:: python

            >>> from app.services.krx_service import KRXService
            >>> # 삼성전자 2023년 1월 주가 데이터 조회
            >>> response = KRXService.get_stock_price("005930", "20230101", "20230131")
            >>> print(f"{response.name} 주가 데이터: {len(response.prices)}일치")
            삼성전자 주가 데이터: 21일치
            >>> # 첫 거래일의 시가/종가 출력
            >>> first_day = response.prices[0]
            >>> print(f"날짜: {first_day.date}, 시가: {first_day.open_}, 종가: {first_day.close}")
            날짜: 2023-01-02, 시가: 58000, 종가: 58200
        """
        try:
            # 종목명 조회
            name = stock.get_market_ticker_name(code)
            if not name:
                raise Exception(f"종목코드 {code}를 찾을 수 없습니다")

            # 주가 데이터 조회
            df = stock.get_market_ohlcv_by_date(start_date, end_date, code)

            if df.empty:
                raise Exception(f"해당 기간의 주가 데이터가 없습니다")

            # DataFrame을 StockPrice 리스트로 변환
            prices = []
            for date_idx, row in df.iterrows():
                prices.append(StockPrice(
                    date=date_idx.date(),  # noqa  # pyright: ignore
                    open_=int(row['시가']),
                    high=int(row['고가']),
                    low=int(row['저가']),
                    close=int(row['종가']),
                    volume=int(row['거래량'])
                ))

            return StockPriceResponse(
                code=code,
                name=name,
                prices=prices
            )

        except Exception as e:
            raise Exception(f"주가 데이터 조회 실패: {str(e)}")

    @staticmethod
    def get_kospi_index(
            start_date: str,
            end_date: str
    ) -> IndexResponse:
        """
        KOSPI 지수 데이터 조회

        지정된 기간 동안의 KOSPI 지수 일별 데이터를 조회합니다.

        :param start_date: 시작일 (YYYYMMDD 형식)
        :type start_date: str
        :param end_date: 종료일 (YYYYMMDD 형식)
        :type end_date: str
        :return: KOSPI 지수 데이터
        :rtype: IndexResponse
        :raises Exception: 데이터 조회 실패 시 발생

        **예제:**

        .. code-block:: python

            >>> from app.services.krx_service import KRXService
            >>> # 2023년 1월 KOSPI 지수 데이터 조회
            >>> response = KRXService.get_kospi_index("20230101", "20230131")
            >>> print(f"KOSPI 지수 데이터: {len(response.prices)}일치")
            KOSPI 지수 데이터: 21일치
            >>> # 기간 내 최고/최저 지수 찾기
            >>> max_value = max(map(lambda x: x.close, response.prices))
            >>> min_value = min(map(lambda x: x.close, response.prices))
            >>> print(f"기간 내 최고: {max_value}, 최저: {min_value}")
            기간 내 최고: 2510.80, 최저: 2350.97
        """
        try:
            # KOSPI 지수 데이터 조회 (지수코드 1001)
            df = stock.get_index_ohlcv_by_date(start_date, end_date, "1001")

            if df.empty:
                raise Exception(f"해당 기간의 KOSPI 지수 데이터가 없습니다")

            # DataFrame을 IndexPrice 리스트로 변환
            prices = []
            for date_idx, row in df.iterrows():
                prices.append(IndexPrice(
                    date=date_idx.date(),  # noqa  # pyright: ignore
                    close=float(row['종가']),
                    volume=int(row['거래량']) if '거래량' in row else None
                ))

            return IndexResponse(
                index_name="KOSPI",
                index_code="1001",
                prices=prices
            )

        except Exception as e:
            raise Exception(f"KOSPI 지수 조회 실패: {str(e)}")

    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """
        날짜 형식 검증 (YYYYMMDD)

        입력된 날짜 문자열이 YYYYMMDD 형식에 맞는지 검증합니다.

        :param date_str: 검증할 날짜 문자열
        :type date_str: str
        :return: 유효한 형식인지 여부
        :rtype: bool

        **예제:**

        .. code-block:: python

            >>> from app.services.krx_service import KRXService
            >>> # 유효한 날짜 형식 검증
            >>> print(KRXService.validate_date_format("20230101"))
            True
            >>> # 잘못된 날짜 형식 검증
            >>> print(KRXService.validate_date_format("2023-01-01"))
            False
            >>> print(KRXService.validate_date_format("20231301"))  # 13월은 없음
            False
        """
        try:
            datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_stock_code(code: str) -> bool:
        """
        종목코드 유효성 검증

        입력된 종목코드가 실제 존재하는 유효한 종목코드인지 검증합니다.

        :param code: 검증할 종목코드
        :type code: str
        :return: 유효한 종목코드인지 여부
        :rtype: bool

        **예제:**

        .. code-block:: python

            >>> from app.services.krx_service import KRXService
            >>> # 유효한 종목코드 검증 (삼성전자)
            >>> print(KRXService.validate_stock_code("005930"))
            True
            >>> # 존재하지 않는 종목코드 검증
            >>> print(KRXService.validate_stock_code("999999"))
            False
            >>> # 잘못된 형식의 종목코드 검증
            >>> print(KRXService.validate_stock_code("5930"))
            False
        """
        try:
            name = stock.get_market_ticker_name(code)
            return bool(name)
        except:  # noqa
            return False
