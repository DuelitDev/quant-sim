from typing import Any
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    에러 응답 모델

    API 요청 처리 중 발생한 오류에 대한 응답을 정의합니다.

    :param error: 에러 타입
    :type error: str
    :param message: 에러 메시지
    :type message: str
    :param detail: 상세 정보
    :type detail: str | None

    **예제:**

    .. code-block:: python

        >>> from app.models.common import ErrorResponse
        >>> error = ErrorResponse(
        ...     error="STOCK_NOT_FOUND",
        ...     message="해당 종목을 찾을 수 없습니다",
        ...     detail="종목코드: 999999"
        ... )
        >>> print(error.model_dump()))
        {
            'error': 'STOCK_NOT_FOUND', 
            'message': '해당 종목을 찾을 수 없습니다', 
            'detail': '종목코드: 999999'
        }
    """
    error: str = Field(..., description="에러 타입")
    message: str = Field(..., description="에러 메시지")
    detail: str | None = Field(None, description="상세 정보")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "STOCK_NOT_FOUND",
                "message": "해당 종목을 찾을 수 없습니다",
                "detail": "종목코드: 999999"
            }
        }


class SuccessResponse(BaseModel):
    """
    성공 응답 모델

    API 요청이 성공적으로 처리되었을 때 반환되는 응답을 정의합니다.

    :param success: 성공 여부
    :type success: bool
    :param message: 성공 메시지
    :type message: str
    :param data: 응답 데이터
    :type data: Any | None

    **예제:**

    .. code-block:: python

        >>> from app.models.common import SuccessResponse
        >>> response = SuccessResponse(
        ...     message="데이터를 성공적으로 조회했습니다",
        ...     data={"user_id": 123, "username": "test_user"}
        ... )
        >>> print(response.model_dump())
        {
            'success': True, 
            'message': '데이터를 성공적으로 조회했습니다', 
            'data': {}
        }
    """
    success: bool = Field(True, description="성공 여부")
    message: str = Field(..., description="성공 메시지")
    data: Any | None = Field(None, description="응답 데이터")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "데이터를 성공적으로 조회했습니다",
                "data": {}
            }
        }


class HealthCheckResponse(BaseModel):
    """
    헬스체크 응답

    API 서버의 상태를 확인하기 위한 헬스체크 응답을 정의합니다.

    :param status: 서버 상태
    :type status: str
    :param timestamp: 응답 시간
    :type timestamp: str
    :param version: API 버전
    :type version: str

    **예제:**

    .. code-block:: python

        >>> from app.models.common import HealthCheckResponse
        >>> from datetime import datetime
        >>> health_check = HealthCheckResponse(
        ...     status="healthy",
        ...     timestamp=datetime.now().isoformat(),
        ...     version="1.0.0"
        ... )
        >>> print(health_check.model_dump())
        {
            'status': 'healthy', 
            'timestamp': '2024-01-02T10:00:00', 
            'version': '1.0.0'
        }
    """
    status: str = Field(..., description="서버 상태")
    timestamp: str = Field(..., description="응답 시간")
    version: str = Field(..., description="API 버전")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-02T10:00:00",
                "version": "1.0.0"
            }
        }
