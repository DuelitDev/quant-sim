"""
시장 지수 관련 API 라우터

이 모듈은 KOSPI 지수 데이터 조회 및 시장 상태 정보 조회를 위한 API 엔드포인트를 제공합니다.
주요 기능:
- KOSPI 지수 데이터 조회 (/market/kospi)
- 시장 상태 정보 조회 (/market/status)

**예제:**

.. code-block:: python

    >>> import requests
    >>> # KOSPI 지수 데이터 조회
    >>> params = {"start_date": "20240101", "end_date": "20240131"}
    >>> response = requests.get(
    ...     "http://localhost:8000/api/market/kospi", 
    ...     params=params
    ... )
    >>> data = response.json()
    >>> print(f"KOSPI 지수 데이터: {len(data['prices'])}일치")
    KOSPI 지수 데이터: 21일치

    >>> # 시장 상태 조회
    >>> response = requests.get("http://localhost:8000/api/market/status")
    >>> data = response.json()
    >>> print(f"현재 시장 상태: {data['status']}, 시간: {data['current_time']}")
    현재 시장 상태: CLOSED, 시간: 2024-05-01 18:30:45
"""
from fastapi import APIRouter, HTTPException, Query

from app.models.index import IndexResponse
from app.services.krx_service import KRXService

router = APIRouter(prefix="/market", tags=["market"])


@router.get(
    "/kospi",
    response_model=IndexResponse,
    summary="KOSPI 지수 조회",
    description="KOSPI 지수 데이터를 조회합니다"
)
async def get_kospi_index(
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
    KOSPI 지수 데이터 조회

    지정된 기간 동안의 KOSPI 지수 일별 데이터를 조회합니다.

    :param start_date: 시작일 (YYYYMMDD 형식)
    :type start_date: str
    :param end_date: 종료일 (YYYYMMDD 형식)
    :type end_date: str
    :return: KOSPI 지수 데이터 응답 객체
    :rtype: IndexResponse
    :raises HTTPException: 다음 경우에 발생
        - 400: 잘못된 날짜 형식
        - 500: 서버 내부 오류

    **예제:**

    .. code-block:: python

        >>> import requests
        >>> # 2024년 1월 KOSPI 지수 데이터 조회
        >>> params = {"start_date": "20240101", "end_date": "20240131"}
        >>> response = requests.get(
        ...     "http://localhost:8000/api/market/kospi",
        ...     params=params
        ... )
        >>> data = response.json()
        >>> print(f"KOSPI 지수 데이터: {len(data['prices'])}일치")
        KOSPI 지수 데이터: 21일치
        >>> # 기간 내 최고/최저 지수 찾기
        >>> max_value = max(price['close'] for price in data['prices'])
        >>> min_value = min(price['close'] for price in data['prices'])
        >>> print(f"기간 내 최고: {max_value}, 최저: {min_value}")
        기간 내 최고: 2655.28, 최저: 2580.54
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

        result = KRXService.get_kospi_index(
            start_date=start_date,
            end_date=end_date
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"KOSPI 지수 조회 실패: {str(e)}"
        )


@router.get(
    "/status",
    summary="시장 상태 조회",
    description="현재 시장 상태 정보를 조회합니다"
)
async def get_market_status():
    """
    시장 상태 정보 조회

    현재 시장의 개장/폐장 상태 및 관련 시간 정보를 반환합니다.
    한국 시간(KST)을 기준으로 평일 09:00~15:30 사이인 경우 'OPEN', 그 외에는 'CLOSED'로 표시합니다.

    :return: 시장 상태 정보 (상태, 현재 시간, 개장 시간, 폐장 시간, 시간대)
    :rtype: dict
    :raises HTTPException: 시장 상태 조회 실패 시 발생 (500 에러)

    **예제:**

    .. code-block:: python

        >>> import requests
        >>> # 시장 상태 조회
        >>> response = requests.get("http://localhost:8000/api/market/status")
        >>> data = response.json()
        >>> print(f"현재 시장 상태: {data['status']}")
        현재 시장 상태: CLOSED
        >>> print(f"현재 시간: {data['current_time']}, 시간대: {data['timezone']}")
        현재 시간: 2024-05-01 18:30:45, 시간대: Asia/Seoul
        >>> print(f"시장 운영 시간: {data['market_open']}~{data['market_close']}")
        시장 운영 시간: 09:00~15:30
    """
    try:
        from datetime import datetime
        import pytz

        # 한국 시간으로 현재 시간 조회
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)

        # 간단한 시장 시간 체크
        market_open = now.replace(hour=9, minute=0, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)

        is_market_time = market_open <= now <= market_close
        is_weekday = now.weekday() < 5  # 0=월요일, 4=금요일

        market_status = "OPEN" if (is_market_time and is_weekday) else "CLOSED"

        return {
            "status": market_status,
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "market_open": "09:00",
            "market_close": "15:30",
            "timezone": "Asia/Seoul"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"시장 상태 조회 실패: {str(e)}"
        )
