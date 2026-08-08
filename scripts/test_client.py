import asyncio

from ia_pronostics.adapters.odds.client import fetch_odds
from ia_pronostics.app.logging_config import configure_logging
from ia_pronostics.app.settings import settings

configure_logging(settings.log_level)


async def main() -> None:
    raw, snapshots = await fetch_odds("soccer_epl")
    print(f"checksum: {raw.checksum[:16]}...")
    print(f"eventos: {len(raw.payload['events'])}")
    print(f"snapshots: {len(snapshots)}")
    if snapshots:
        s = snapshots[0]
        print(f"ejemplo: {s.bookmaker} {s.market.side} @ {s.price}")


asyncio.run(main())
