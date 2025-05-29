from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field


class IndexPrice(BaseModel):
    """
    지수 가격 데이터

    특정 거래일의 지수 가격 정보를 포함하는 모델입니다.

    :param date: 거래일
    :type date: date
    :param close: 지수값
    :type close: float
    :param volume: 거래량
    :type volume: int | None

    **예제:**

    .. code-block:: python

        >>> from app.models.index import IndexPrice
        >>> import datetime
        >>> kospi_price = IndexPrice(
        ...     date=datetime.date(2024, 1, 2),
        ...     close=2655.28,
        ...     volume=1000000000
        ... )
        >>> print(kospi_price.model_dump())
        {
            'date': '2024-01-02', 
            'close': 2655.28, 
            'volume': 1000000000
        }
        >>> print(f"KOSPI 지수({kospi_price.date}): {kospi_price.close}")
        KOSPI 지수(2024-01-02): 2655.28
    """
    date: date = Field(..., description="거래일")
    close: float = Field(..., description="지수값")
    volume: int | None = Field(None, description="거래량")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-02",
                "close": 2655.28,
                "volume": 1000000000
            }
        }


class IndexResponse(BaseModel):
    """
    지수 데이터 응답

    지수 데이터 조회 요청에 대한 응답 모델입니다. 지수명, 코드 및 가격 데이터를 포함합니다.

    :param index_name: 지수명 (KOSPI, KOSDAQ)
    :type index_name: str
    :param index_code: 지수 코드
    :type index_code: str
    :param prices: 지수 가격 데이터
    :type prices: list[IndexPrice]

    **예제:**

    .. code-block:: python

        >>> from app.models.index import IndexResponse, IndexPrice
        >>> from datetime import date
        >>> # 지수 가격 데이터 생성
        >>> price_data = [
        ...     IndexPrice(date=date(2024, 1, 2), 
        ...                close=2655.28, 
        ...                volume=1000000000),
        ...     IndexPrice(date=date(2024, 1, 3), 
        ...                close=2661.95, 
        ...                volume=950000000)
        ... ]
        >>> # 응답 객체 생성
        >>> response = IndexResponse(
        ...     index_name="KOSPI",
        ...     index_code="1001",
        ...     prices=price_data
        ... )
        >>> print(f"지수명: {response.index_name}, " 
        ...       f"데이터 개수: {len(response.prices)}")
        지수명: KOSPI, 데이터 개수: 2
        >>> # 최근 지수값 출력
        >>> latest = response.prices[-1]
        >>> print(f"최근 지수값({latest.date}): {latest.close}")
        최근 지수값(2024-01-03): 2661.95
    """
    index_name: str = Field(..., description="지수명 (KOSPI, KOSDAQ)")
    index_code: str = Field(..., description="지수 코드")
    prices: list[IndexPrice] = Field(..., description="지수 가격 데이터")

    class Config:
        json_schema_extra = {
            "example": {
                "index_name": "KOSPI",
                "index_code": "1001",
                "prices": [
                    {
                        "date": "2024-01-02",
                        "close": 2655.28,
                        "volume": 1000000000
                    }
                ]
            }
        }


class IndexInfo(BaseModel):
    """
    지수 기본 정보를 담는 데이터 모델

    지수의 코드, 이름, 시장 구분 등 기본적인 정보를 포함하는 모델입니다.
    한국거래소 및 해외 주요 지수 정보를 표준화된 형태로 관리할 수 있습니다.

    :param code: 지수 고유 식별 코드 (예: "1001", "SPX")
    :type code: str
    :param name: 지수의 공식 명칭
    :type name: str

    .. note::
       지수 코드는 데이터 제공업체별로 다를 수 있으므로 일관성 있게 관리해야 합니다.

    **기본 사용 예제:**

    .. code-block:: python

        >>> from app.models.index import IndexInfo
        >>> # 국내 주요 지수 정보 생성
        >>> kospi = IndexInfo(code="1001", name="KOSPI")
        >>> kosdaq = IndexInfo(code="2001", name="KOSDAQ")
        >>> print(f"지수: {kospi.name}, 코드: {kospi.code}")
        지수: KOSPI, 코드: 1001

    **여러 지수 일괄 처리 예제:**

    .. code-block:: python

        >>> # 여러 지수 정보를 리스트로 관리
        >>> indices = [
        ...     IndexInfo(code="1001", name="KOSPI"),
        ...     IndexInfo(code="2001", name="KOSDAQ"),
        ...     IndexInfo(code="SPX", name="S&P 500"),
        ...     IndexInfo(code="DJI", name="Dow Jones Industrial Average")
        ... ]
        >>> # 지수 정보 출력
        >>> for idx in indices:
        ...     print(f"지수: {idx.name} ({idx.code})")
        지수: KOSPI (1001)
        지수: KOSDAQ (2001)
        지수: S&P 500 (SPX)
        지수: Dow Jones Industrial Average (DJI)

    **딕셔너리 변환 예제:**

    .. code-block:: python

        >>> # Pydantic 모델을 딕셔너리로 변환
        >>> kospi_dict = kospi.model_dump()
        >>> print(kospi_dict)
        {'code': '1001', 'name': 'KOSPI'}
        >>> # JSON 문자열로 변환
        >>> import json
        >>> kospi_json = kospi.model_dump_json()
        >>> print(kospi_json)
        '{"code":"1001","name":"KOSPI"}'
    """
    code: str = Field(..., description="지수 고유 식별 코드")
    name: str = Field(..., description="지수의 공식 명칭")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "1001",
                "name": "KOSPI",
            }
        }
