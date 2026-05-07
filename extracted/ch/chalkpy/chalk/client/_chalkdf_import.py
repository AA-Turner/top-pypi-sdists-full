from __future__ import annotations

import importlib
from typing import Optional, Protocol, runtime_checkable


@runtime_checkable
class ChalkDfDataFrame(Protocol):
    """Protocol describing the chalkdf.DataFrame interface."""

    @classmethod
    def from_arrow(cls, data: object) -> ChalkDfDataFrame: ...

    def write_parquet(self, output_uri_prefix: str, **kwargs: object) -> object: ...

    def write(self, target_path: str, **kwargs: object) -> object: ...

    def run(self, **kwargs: object) -> object: ...


CHALKDF_IMPORT_MESSAGE = (
    "chalkdf is required for this functionality. Install the dependency with `pip install chalkdf`."
)

_chalkdf_dataframe_cls: Optional[type] = None


def get_chalkdf_dataframe_cls() -> type:
    global _chalkdf_dataframe_cls
    if _chalkdf_dataframe_cls is None:
        try:
            mod = importlib.import_module("chalkdf.dataframe")
        except ImportError as exc:
            raise ImportError(CHALKDF_IMPORT_MESSAGE) from exc
        _chalkdf_dataframe_cls = mod.DataFrame
    assert _chalkdf_dataframe_cls is not None
    return _chalkdf_dataframe_cls
