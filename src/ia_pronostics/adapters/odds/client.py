import logging
from datetime import UTC, datetime

import httpx

from ia_pronostics.adapters.odds.parser import parse_event_to_snapshots
from ia_pronostics.app.settings import settings
from ia_pronostics.core.checksum import payload_checksum
from ia_pronostics.core.types import OddsSnapshot, RawPayload

logger = logging.getLogger(__name__)


class OddsApiConfigError(ValueError):
    """Falta configuración para llamar a The Odds API."""


def _silence_http_client_logs() -> None:
    # httpx/httpcore loguean la URL con apiKey; forzar WARNING tras basicConfig
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def _require_api_key() -> str:
    if not settings.odds_api_key:
        raise OddsApiConfigError("ODDS_API_KEY no configurada en .env")
    return settings.odds_api_key


def _log_api_quota(response: httpx.Response) -> None:
    remaining = response.headers.get("x-requests-remaining")
    if remaining is None:
        return
    logger.info(
        "The Odds API quota: remaining=%s used=%s last_call_cost=%s",
        remaining,
        response.headers.get("x-requests-used"),
        response.headers.get("x-requests-last"),
    )


async def fetch_odds(
    sport: str,
    regions: str = "eu,uk",
    markets: str = "h2h",
    bookmakers: str = "pinnacle",
) -> tuple[RawPayload, list[OddsSnapshot]]:
    _silence_http_client_logs()
    endpoint = f"/v4/sports/{sport}/odds"
    params = {
        "apiKey": _require_api_key(),
        "regions": regions,
        "markets": markets,
        "bookmakers": bookmakers,
        "oddsFormat": "decimal",
    }
    async with httpx.AsyncClient(
        base_url=settings.odds_api_base_url, timeout=30.0
    ) as client:
        response = await client.get(endpoint, params=params)
        response.raise_for_status()
        _log_api_quota(response)
        events = response.json()

    fetched_at = datetime.now(UTC)
    raw = RawPayload(
        provider="the_odds_api",
        endpoint=endpoint,
        payload={"events": events},
        fetched_at_utc=fetched_at,
        checksum=payload_checksum({"events": events}),
    )
    snapshots: list[OddsSnapshot] = []
    for event in events:
        snapshots.extend(parse_event_to_snapshots(event, ingested_at=fetched_at))
    return raw, snapshots
