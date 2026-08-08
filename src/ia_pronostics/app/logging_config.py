import logging


def configure_logging(level: str = "info") -> None:
    logging.basicConfig(level=level.upper(), force=True)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
