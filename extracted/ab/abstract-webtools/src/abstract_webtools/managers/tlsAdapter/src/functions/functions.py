from ..imports import *

def normalize_ciphers(ciphers: Optional[Union[str, Sequence[str]]]) -> Optional[str]:
    if ciphers is None:
        return None
    if isinstance(ciphers, str):
        parts = [p.strip() for p in ciphers.split(",") if p.strip()]
        return ",".join(parts) if parts else ""
    return ",".join(s.strip() for s in ciphers if s and s.strip())
