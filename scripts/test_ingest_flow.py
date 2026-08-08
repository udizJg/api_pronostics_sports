from datetime import UTC, datetime

from ia_pronostics.adapters.odds.parser import parse_event_to_snapshots
from ia_pronostics.core.checksum import payload_checksum
from ia_pronostics.core.types import RawPayload

# The Odds API devuelve una LISTA de eventos
api_response = [
    {
        "id": "evt_abc123",
        "sport_key": "soccer_epl",
        "commence_time": "2026-08-10T15:00:00Z",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "bookmakers": [
            {
                "key": "pinnacle",
                "last_update": "2026-08-10T14:55:00Z",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Arsenal", "price": 1.95},
                            {"name": "Chelsea", "price": 2.10},
                            {"name": "Draw", "price": 3.40},
                        ],
                    }
                ],
            }
        ],
    }
]
fetched_at = datetime.now(UTC)
# 1. Guardar crudo (como iría a raw_payloads en DB)
raw = RawPayload(
    provider="the_odds_api",
    endpoint="/v4/sports/soccer_epl/odds",
    payload={"events": api_response},
    fetched_at_utc=fetched_at,
    checksum=payload_checksum({"events": api_response}),
)
# 2. Parsear cada evento
all_snapshots = []
for event in api_response:
    all_snapshots.extend(parse_event_to_snapshots(event, ingested_at=fetched_at))
print(f"RawPayload checksum: {raw.checksum[:16]}...")
print(f"Eventos: {len(api_response)}")
print(f"Snapshots: {len(all_snapshots)}")
for s in all_snapshots:
    print(f"  {s.bookmaker} | {s.market.market_type} | {s.market.side} | {s.price}")
