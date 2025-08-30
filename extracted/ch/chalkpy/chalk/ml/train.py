from typing import Any


# Implementation override happens in engine
def mock(*args: Any, **kwargs: Any) -> Any:
    pass


log_checkpoint = mock
load_dataset = mock
