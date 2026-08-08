from decimal import Decimal

from ia_pronostics.core.pricing.convert import decimal_odds_to_implied_prob


def proportional_devig(odds: list[Decimal]) -> list[float]:
    if len(odds) < 2:
        raise ValueError("need at least 2 outcomes")
    implied = [decimal_odds_to_implied_prob(o) for o in odds]
    total = sum(implied)
    if total <= 0:
        raise ValueError("invalid implied probability total")
    return [p / total for p in implied]
