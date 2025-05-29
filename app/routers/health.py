"""
헬스체크 관련 API 라우터

이 모듈은 API 서버의 상태를 확인하기 위한 헬스체크 엔드포인트를 제공합니다.
주요 기능:
- API 서버 헬스체크 (/health)

**예제:**

.. code-block:: python

    >>> import requests
    >>> # 헬스체크 API 호출
    >>> response = requests.get("http://localhost:8000/health")
    >>> data = response.json()
    >>> print(f"서버 상태: {data['status']}")
    서버 상태: healthy
    >>> print(f"API 버전: {data['version']}")
    API 버전: 1.0.0
    >>> print(f"응답 시간: {data['timestamp']}")
    응답 시간: 2024-05-01T18:30:45.123456
"""
from datetime import datetime
from fastapi import APIRouter

from app.models.common import HealthCheckResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="헬스체크",
    description="API 서버의 상태를 확인합니다"
)
async def health_check():
    """
    API 서버 헬스체크

    서버가 정상적으로 동작하는지 확인하기 위한 헬스체크 엔드포인트입니다.
    서버 상태, 현재 시간, API 버전 정보를 반환합니다.

    :return: 헬스체크 응답 객체
    :rtype: HealthCheckResponse

    **예제:**

    .. code-block:: python

        >>> import requests
        >>> # 헬스체크 API 호출
        >>> response = requests.get("http://localhost:8000/health")
        >>> data = response.json()
        >>> # 응답 데이터 확인
        >>> if data['status'] == 'healthy':
        ...     print("서버가 정상적으로 동작 중입니다.")
        ... else:
        ...     print("서버에 문제가 있습니다!")
        서버가 정상적으로 동작 중입니다.
        >>> # 응답 시간 확인
        >>> from datetime import datetime
        >>> response_time = datetime.fromisoformat(data['timestamp'])
        >>> print(f"서버 응답 시간: {response_time.strftime('%Y-%m-%d %H:%M:%S')}")
        서버 응답 시간: 2024-05-01 18:30:45
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )
