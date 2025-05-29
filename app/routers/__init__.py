"""
Routers Package
FastAPI 라우터들을 관리하는 패키지

이 패키지는 API 엔드포인트를 정의하는 FastAPI 라우터들을 포함합니다.
각 라우터는 특정 기능 영역에 대한 API 엔드포인트를 그룹화합니다.

:param stocks_router: 주식 관련 API 라우터
:type stocks_router: APIRouter
:param market_router: 시장 지수 관련 API 라우터
:type market_router: APIRouter
:param health_router: 헬스체크 관련 API 라우터
:type health_router: APIRouter

**예제:**

.. code-block:: python

    >>> from fastapi import FastAPI
    >>> from app.routers import stocks_router, market_router, health_router
    >>> 
    >>> app = FastAPI(title="Quant API")
    >>> 
    >>> # 라우터 등록
    >>> app.include_router(health_router)
    >>> app.include_router(stocks_router, prefix="/api")
    >>> app.include_router(market_router, prefix="/api")
    >>> 
    >>> # 등록된 라우터의 엔드포인트 확인
    >>> for route in app.routes:
    ...     print(f"엔드포인트: {route.path}")
    엔드포인트: /health
    엔드포인트: /api/stocks/list
    엔드포인트: /api/stocks/{code}/price
    엔드포인트: /api/market/kospi
    엔드포인트: /api/market/status
"""

from .stocks import router as stocks_router
from .market import router as market_router
from .health import router as health_router

__all__ = [
    "stocks_router",
    "market_router", 
    "health_router"
]
