"""
주식 관련 API 라우터

이 모듈은 주식 종목 목록 조회 및 개별 종목의 가격 데이터 조회를 위한 API 엔드포인트를 제공합니다.
주요 기능:
- 종목 목록 조회 (/stocks/list)
- 개별 종목 가격 데이터 조회 (/stocks/{code}/price)

**예제:**

.. code-block:: python

    >>> import requests
    >>> # 종목 목록 조회
    >>> response = requests.get("http://localhost:8000/api/stocks/list")
    >>> data = response.json()
    >>> print(f"총 {data['count']}개 종목이 조회되었습니다")
    총 900개 종목이 조회되었습니다

    >>> # 삼성전자 주가 데이터 조회
    >>> params = {"start_date": "20240101", "end_date": "20240131"}
    >>> response = requests.get(
    ...     "http://localhost:8000/api/stocks/005930/price", 
    ...     params=params
    ... )
    >>> data = response.json()
    >>> print(f"{data['name']} 주가 데이터: {len(data['prices'])}일치")
    삼성전자 주가 데이터: 21일치
"""
from fastapi import APIRouter, HTTPException, Query

from app.models.stock import StockListResponse, StockPriceResponse
from app.services.krx_service import KRXService

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get(
    "/list",
    response_model=StockListResponse,
    summary="종목 리스트 조회",
    description="KOSPI 시장의 상장 종목 리스트를 조회합니다"
)
async def get_stock_list():
    """
    KOSPI 상장 종목 리스트 조회

    현재 KOSPI 시장에 상장된 모든 종목의 코드와 이름을 반환합니다.

    :return: 종목 리스트 응답 객체
    :rtype: StockListResponse
    :raises HTTPException: 종목 리스트 조회 실패 시 발생 (500 에러)

    **예제:**

    .. code-block:: python

        >>> import requests
        >>> # API 엔드포인트 호출
        >>> response = requests.get("http://localhost:8000/api/stocks/list")
        >>> data = response.json()
        >>> # 응답 데이터 확인
        >>> print(f"총 {data['count']}개 종목이 조회되었습니다")
        총 900개 종목이 조회되었습니다
        >>> # 첫 3개 종목 출력
        >>> for stock in data['stocks'][:3]:
        ...     print(f"종목코드: {stock['code']}, 종목명: {stock['name']}")
        종목코드: 005930, 종목명: 삼성전자
        종목코드: 000660, 종목명: SK하이닉스
        종목코드: 051910, 종목명: LG화학
    """
    try:
        result = KRXService.get_stock_list()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"종목 리스트 조회 실패: {str(e)}"
        )


@router.get(
    "/{code}/price",
    response_model=StockPriceResponse,
    summary="개별 종목 주가 조회",
    description="특정 종목의 일봉 주가 데이터를 조회합니다"
)
async def get_stock_price(
    code: str,
    start_date: str = Query(
        ...,
        description="시작일 (YYYYMMDD 형식)",
        regex=r"^\d{8}$",
        example="20240101"
    ),
    end_date: str = Query(
        ...,
        description="종료일 (YYYYMMDD 형식)", 
        regex=r"^\d{8}$",
        example="20241231"
    )
):
    """
    개별 종목의 주가 데이터 조회

    지정된 기간 동안의 특정 종목의 일별 주가 데이터(OHLCV)를 조회합니다.

    :param code: 종목코드 (예: 005930)
    :type code: str
    :param start_date: 시작일 (YYYYMMDD 형식)
    :type start_date: str
    :param end_date: 종료일 (YYYYMMDD 형식)
    :type end_date: str
    :return: 주가 데이터 응답 객체
    :rtype: StockPriceResponse
    :raises HTTPException: 다음 경우에 발생
        - 400: 잘못된 날짜 형식
        - 404: 존재하지 않는 종목코드
        - 500: 서버 내부 오류

    **예제:**

    .. code-block:: python

        >>> import requests
        >>> # 삼성전자(005930) 2024년 1월 주가 데이터 조회
        >>> params = {"start_date": "20240101", "end_date": "20240131"}
        >>> response = requests.get(
        ...     "http://localhost:8000/api/stocks/005930/price",
        ...     params=params
        ... )
        >>> data = response.json()
        >>> print(f"{data['name']} 주가 데이터: {len(data['prices'])}일치")
        삼성전자 주가 데이터: 21일치
        >>> # 첫 거래일의 시가/종가 출력
        >>> first_day = data['prices'][0]
        >>> print(f"날짜: {first_day['date']}, 시가: {first_day['open']}원, 종가: {first_day['close']}원")
        날짜: 2024-01-02, 시가: 77000원, 종가: 76800원
    """
    try:
        # 날짜 형식 검증
        if not KRXService.validate_date_format(start_date):
            raise HTTPException(
                status_code=400,
                detail="잘못된 시작일 형식입니다 (YYYYMMDD 형식으로 입력해주세요)"
            )

        if not KRXService.validate_date_format(end_date):
            raise HTTPException(
                status_code=400,
                detail="잘못된 종료일 형식입니다 (YYYYMMDD 형식으로 입력해주세요)"
            )

        # 종목코드 검증
        if not KRXService.validate_stock_code(code):
            raise HTTPException(
                status_code=404,
                detail=f"종목코드 '{code}'를 찾을 수 없습니다"
            )

        result = KRXService.get_stock_price(
            code=code,
            start_date=start_date,
            end_date=end_date
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"주가 데이터 조회 실패: {str(e)}"
        )
