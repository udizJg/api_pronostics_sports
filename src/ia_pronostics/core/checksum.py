import hashlib
import json


def payload_checksum(payload: dict) -> str:
    """Hash estable del JSON para idempotencia (SPEC §11.4)."""
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
