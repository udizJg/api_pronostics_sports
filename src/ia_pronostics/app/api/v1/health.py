from fastapi import APIRouter

from ia_pronostics.app.api.schemas.health import HealthResponse

router = APIRouter(prefix="/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
