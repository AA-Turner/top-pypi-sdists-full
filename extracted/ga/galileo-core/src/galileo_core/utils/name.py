from datetime import datetime

SCORER_NAME_REGEX = r"^[\w -]+$"


def ts_name(prefix: str) -> str:
    ts = datetime.now()
    ts_string = ts.strftime("%b_%d_%H_%M_%S")
    return f"{prefix}-{ts_string}"
