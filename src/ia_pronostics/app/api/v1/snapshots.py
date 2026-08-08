from fastapi import APIRouter

from ia_pronostics.core.types import OddsSnapshot

router = APIRouter(prefix="/v1", tags=["snapshots"])


@router.post("/snapshots", response_model=OddsSnapshot, status_code=201)
async def create_snapshot(snapshot: OddsSnapshot) -> OddsSnapshot:
    # Por ahora solo valida y devuelve; luego irá al pipeline
    return snapshot
