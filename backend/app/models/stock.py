from __future__ import annotations
import datetime
from pydantic import BaseModel, Field


class StockInfo(BaseModel):
    """
    종목 기본 정보

    주식 종목의 코드와 이름 등 기본적인 정보를 포함하는 모델입니다.

    :param code: 종목코드 (예: 005930)
    :type code: str
    :param name: 종목명 (예: 삼성전자)
    :type name: str

    **예제:**

    .. code-block:: python

        >>> from app.models.stock import StockInfo
        >>> stock = StockInfo(code="005930", name="삼성전자")
        >>> print(stock.model_dump())
        {'code': '005930', 'name': '삼성전자'}
        >>> print(f"종목명: {stock.name}, 종목코드: {stock.code}")
        종목명: 삼성전자, 종목코드: 005930
    """
    code: str = Field(..., description="종목코드 (예: 005930)")
    name: str = Field(..., description="종목명 (예: 삼성전자)")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "005930",
                "name": "삼성전자"
            }
        }


class StockPrice(BaseModel):
    """
    주식 일봉 가격 데이터

    특정 거래일의 주식 가격 정보(시가, 고가, 저가, 종가, 거래량)를 포함하는 모델입니다.

    :param date: 거래일
    :type date: date
    :param open_: 시가
    :type open_: int
    :param high: 고가
    :type high: int
    :param low: 저가
    :type low: int
    :param close: 종가
    :type close: int
    :param volume: 거래량
    :type volume: int

    **예제:**

    .. code-block:: python

        >>> from app.models.stock import StockPrice
        >>> import datetime
        >>> price = StockPrice(
        ...     date=datetime.date(2024, 1, 2),
        ...     open_=77000,
        ...     high=77500,
        ...     low=76000,
        ...     close=76800,
        ...     volume=15000000
        ... )
        >>> print(price.model_dump())
        {'date': '2024-01-02', 'open': 77000, 'high': 77500, 'low': 76000, 'close': 76800, 'volume': 15000000}
        >>> print(f"거래일: {price.date}, 종가: {price.close}원")
        거래일: 2024-01-02, 종가: 76800원
    """
    date: datetime.date = Field(..., description="거래일")
    open_: int = Field(..., description="시가")
    high: int = Field(..., description="고가")
    low: int = Field(..., description="저가")
    close: int = Field(..., description="종가")
    volume: int = Field(..., description="거래량")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-02",
                "open": 77000,
                "high": 77500,
                "low": 76000,
                "close": 76800,
                "volume": 15000000
            }
        }


class StockPriceResponse(BaseModel):
    """
    주식 가격 데이터 응답

    주식 가격 데이터 조회 요청에 대한 응답 모델입니다. 
    종목 코드, 이름 및 가격 데이터 리스트를 포함합니다.

    :param code: 종목코드
    :type code: str
    :param name: 종목명
    :type name: str
    :param prices: 가격 데이터 리스트
    :type prices: list[StockPrice]

    **예제:**

    .. code-block:: python

        >>> from app.models.stock import StockPriceResponse, StockPrice
        >>> import datetime
        >>> price_data = StockPrice(
        ...     date=datetime.date(2024, 1, 2),
        ...     open_=77000,
        ...     high=77500,
        ...     low=76000,
        ...     close=76800,
        ...     volume=15000000
        ... )
        >>> response = StockPriceResponse(
        ...     code="005930",
        ...     name="삼성전자",
        ...     prices=[price_data]
        ... )
        >>> print(f"종목: {response.name}, 데이터 개수: {len(response.prices)}")
        종목: 삼성전자, 데이터 개수: 1
        >>> print(f"최근 종가: {response.prices[0].close}원")
        최근 종가: 76800원
    """
    code: str = Field(..., description="종목코드")
    name: str = Field(..., description="종목명")
    prices: list[StockPrice] = Field(..., description="가격 데이터 리스트")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "005930",
                "name": "삼성전자",
                "prices": [
                    {
                        "date": "2024-01-02",
                        "open": 77000,
                        "high": 77500,
                        "low": 76000,
                        "close": 76800,
                        "volume": 15000000
                    }
                ]
            }
        }


class StockListResponse(BaseModel):
    """
    종목 리스트 응답

    주식 종목 목록 조회 요청에 대한 응답 모델입니다. 전체 종목 수와 종목 정보 리스트를 포함합니다.

    :param count: 종목 수
    :type count: int
    :param stocks: 종목 리스트
    :type stocks: list[StockInfo]

    **예제:**

    .. code-block:: python

        >>> from app.models.stock import StockListResponse, StockInfo
        >>> stocks = [
        ...     StockInfo(code="005930", name="삼성전자"),
        ...     StockInfo(code="000660", name="SK하이닉스"),
        ...     StockInfo(code="035420", name="NAVER")
        ... ]
        >>> response = StockListResponse(count=len(stocks), stocks=stocks)
        >>> print(f"총 종목 수: {response.count}")
        총 종목 수: 3
        >>> for stock in response.stocks:
        ...     print(f"종목코드: {stock.code}, 종목명: {stock.name}")
        종목코드: 005930, 종목명: 삼성전자
        종목코드: 000660, 종목명: SK하이닉스
        종목코드: 035420, 종목명: NAVER
    """
    count: int = Field(..., description="종목 수")
    stocks: list[StockInfo] = Field(..., description="종목 리스트")

    class Config:
        json_schema_extra = {
            "example": {
                "count": 2,
                "stocks": [
                    {
                        "code": "005930",
                        "name": "삼성전자"
                    },
                    {
                        "code": "000660",
                        "name": "SK하이닉스"
                    }
                ]
            }
        }
