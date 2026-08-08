from datetime import UTC, datetime

from ia_pronostics.adapters.odds.parser import parse_event_to_snapshots

sample_event = {
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
                },
                {
                    "key": "totals",
                    "outcomes": [
                        {"name": "Over", "price": 1.88, "point": 2.5},
                        {"name": "Under", "price": 1.92, "point": 2.5},
                    ],
                },
            ],
        }
    ],
}
snapshots = parse_event_to_snapshots(sample_event, ingested_at=datetime.now(UTC))
print(f"{len(snapshots)} snapshots")
for s in snapshots:
    print(s.bookmaker, s.market.market_type, s.market.side, s.price)
