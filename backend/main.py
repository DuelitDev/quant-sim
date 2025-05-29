"""
Quant Backend API
FastAPI 기반 주식 데이터 제공 API

이 모듈은 주식 및 시장 데이터를 제공하는 FastAPI 애플리케이션의 진입점입니다.
주요 기능:
- 종목 목록 및 주가 데이터 조회 API
- KOSPI 지수 데이터 조회 API
- 시장 상태 정보 조회 API
- 서버 헬스체크 API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stocks_router, market_router, health_router


app = FastAPI(
    title="Quant Backend API",
    description="주식 데이터 제공을 위한 FastAPI 백엔드",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(stocks_router, prefix="/api")
app.include_router(market_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
