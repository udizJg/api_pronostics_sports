from datetime import UTC, datetime
from decimal import Decimal

from ia_pronostics.core.types import (
    MarketKey,
    MarketSide,
    MarketType,
    OddsSnapshot,
)

MARKET_TYPE_MAP = {
    "h2h": MarketType.H2H,
    "spreads": MarketType.SPREADS,
    "totals": MarketType.TOTALS,
}


def _resolve_h2h_side(outcome_name: str, home_team: str, away_team: str) -> MarketSide:
    if outcome_name == home_team:
        return MarketSide.HOME
    if outcome_name == away_team:
        return MarketSide.AWAY
    return MarketSide.DRAW


def _resolve_totals_side(outcome_name: str) -> MarketSide:
    name = outcome_name.lower()
    if name == "over":
        return MarketSide.OVER
    return MarketSide.UNDER


def parse_event_to_snapshots(
    event: dict, ingested_at: datetime | None = None
) -> list[OddsSnapshot]:
    """Convierte un evento de The Odds API en snapshots aplanadas."""
    ingested = ingested_at or datetime.now(UTC)
    home = event["home_team"]
    away = event["away_team"]
    snapshots: list[OddsSnapshot] = []
    for bookmaker in event.get("bookmakers", []):
        source_ts = datetime.fromisoformat(bookmaker["last_update"])
        for market in bookmaker.get("markets", []):
            market_type = MARKET_TYPE_MAP.get(market["key"])
            if market_type is None:
                continue
            for outcome in market.get("outcomes", []):
                if market_type == MarketType.H2H:
                    side = _resolve_h2h_side(outcome["name"], home, away)
                    line = None
                elif market_type == MarketType.TOTALS:
                    side = _resolve_totals_side(outcome["name"])
                    line = (
                        Decimal(str(outcome["point"]))
                        if outcome.get("point") is not None
                        else None
                    )
                else:
                    side = (
                        MarketSide.HOME if outcome["name"] == home else MarketSide.AWAY
                    )
                    line = (
                        Decimal(str(outcome["point"]))
                        if outcome.get("point") is not None
                        else None
                    )
                snapshots.append(
                    OddsSnapshot(
                        event_ref=event["id"],
                        bookmaker=bookmaker["key"],
                        market=MarketKey(
                            market_type=market_type,
                            line=line,
                            side=side,
                        ),
                        price=Decimal(str(outcome["price"])),
                        source_ts_utc=source_ts,
                        ingested_at_utc=ingested,
                    )
                )
    return snapshots
