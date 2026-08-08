from decimal import Decimal

import pytest

from ia_pronostics.core.pricing.devig import proportional_devig


def test_proportional_devig_two_equal_odds():
    fair = proportional_devig([Decimal("2.0"), Decimal("2.0")])
    assert fair == pytest.approx([0.5, 0.5])


def test_proportional_devig_with_margin():
    fair = proportional_devig([Decimal("1.95"), Decimal("1.95")])
    assert sum(fair) == pytest.approx(1.0)
    assert fair[0] == pytest.approx(fair[1])


def test_proportional_devig_rejects_single_outcome():
    with pytest.raises(ValueError, match="at least 2"):
        proportional_devig([Decimal("1.50")])
