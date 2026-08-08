from datetime import UTC, datetime

from ia_pronostics.core.checksum import payload_checksum
from ia_pronostics.core.types import RawPayload

api_response = {
    "id": "evt_abc123",
    "sport_key": "soccer_epl",
    "commence_time": "2026-08-10T15:00:00Z",
    "home_team": "Arsenal",
    "away_team": "Chelsea",
    "bookmakers": [],
}

raw = RawPayload(
    provider="the_odds_api",
    endpoint="/v4/sports/soccer_epl/odds",
    payload=api_response,
    fetched_at_utc=datetime.now(UTC),
    checksum=payload_checksum(api_response),
)

print(raw.provider)
print(raw.checksum[:16] + "...")
print(len(raw.payload), "keys en payload")
