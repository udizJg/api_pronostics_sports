from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class RawPayload(BaseModel):
    """JSON crudo del proveedor. Se persiste siempre antes de parsear."""

    provider: str = Field(min_length=1)
    endpoint: str = Field(min_length=1)
    payload: dict
    fetched_at_utc: datetime
    checksum: str = Field(min_length=1)


class MarketType(StrEnum):
    H2H = "h2h"
    SPREADS = "spreads"
    TOTALS = "totals"


class Period(StrEnum):
    FULL_TIME = "full_time"
    FIRST_HALF = "first_half"


class MarketSide(StrEnum):
    HOME = "home"
    AWAY = "away"
    DRAW = "draw"
    OVER = "over"
    UNDER = "under"


class MarketKey(BaseModel):
    market_type: MarketType
    line: Decimal | None = None
    side: MarketSide
    period: Period = Period.FULL_TIME
    settlement_rule_id: str = "default"


class OddsSnapshot(BaseModel):
    event_ref: str = Field(min_length=1)
    bookmaker: str = Field(min_length=1)
    market: MarketKey
    price: Decimal
    is_live: bool = False
    is_suspended: bool = False
    source_ts_utc: datetime
    ingested_at_utc: datetime
    max_stake: Decimal | None = None
    changed_at_utc: datetime | None = None
    odds_provider: str | None = None

    @field_validator("price")
    @classmethod
    def price_must_be_valid_odds(cls, value: Decimal) -> Decimal:
        if value < Decimal("1.01"):
            raise ValueError("price must be >= 1.01")
        return value
