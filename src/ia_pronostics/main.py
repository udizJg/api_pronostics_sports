from fastapi import FastAPI

from ia_pronostics.app.api.v1.health import router as health_router
from ia_pronostics.app.api.v1.snapshots import router as snapshots_router
from ia_pronostics.app.logging_config import configure_logging
from ia_pronostics.app.settings import settings

configure_logging(settings.log_level)

app = FastAPI(
    title="ia_pronostics", version="0.1.0", debug=settings.env == "development"
)
app.include_router(health_router)
app.include_router(snapshots_router)
