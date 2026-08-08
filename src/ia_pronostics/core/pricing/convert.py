from decimal import Decimal


def decimal_odds_to_implied_prob(odds: Decimal) -> float:
    if odds < Decimal("1.01"):
        raise ValueError("odds must be >= 1.01")
    return float(Decimal(1) / odds)
