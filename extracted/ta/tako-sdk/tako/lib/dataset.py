"""``TakoDatasetView`` — a convenience view over a Retrieval Agent dataset slot.

The wire encoding of a filled dataset slot is positional row arrays plus a typed
``columns`` header (the SQL-API convention), which is compact but awkward to
consume directly. This view exposes the two shapes callers actually want:

* ``.records`` — ``list[dict]`` (one dict per row), no third-party dependency.
* ``.to_dataframe()`` — a typed pandas ``DataFrame`` (pandas is an optional extra;
  install ``tako-sdk[pandas]``). Column dtypes are coerced from the ``columns``
  header — "the header never lies".

Construct from either the raw slot dict (what sits at
``result.structured_output[field]``) or a generated :class:`TakoDataset`::

    view = TakoDatasetView(run.result.structured_output["cohort"])
    view.records            # [{"company": "Nvidia", "revenue": 130497000000.0}, ...]
    view.to_dataframe()     # typed pandas DataFrame
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

from tako.models.tako_dataset import TakoDataset


class TakoDatasetView:
    """Records / DataFrame view over one Retrieval Agent dataset slot."""

    def __init__(self, dataset: Union[TakoDataset, Mapping[str, Any]]) -> None:
        data: Dict[str, Any]
        if isinstance(dataset, TakoDataset):
            data = dataset.to_dict()
        elif isinstance(dataset, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]  # defensive
            data = dict(dataset)
        else:
            raise TypeError(
                f"TakoDatasetView expects a TakoDataset or a slot dict, got {type(dataset).__name__}"
            )
        self._columns: List[Dict[str, Any]] = list(data.get("columns") or [])
        self._rows: List[List[Any]] = list(data.get("rows") or [])
        self.total_rows: Optional[int] = data.get("total_rows")
        self.truncated: Optional[bool] = data.get("truncated")
        self.ref: Optional[str] = data.get("ref")
        self.sources: List[Any] = list(data.get("sources") or [])
        self.provenance: Optional[str] = data.get("provenance")

    @property
    def columns(self) -> List[Tuple[str, str]]:
        """The typed header as ``(name, type)`` tuples, in declaration order."""
        # Header keys are guaranteed by the API contract; a malformed header
        # (missing name/type) is unrecoverable, so fail loud rather than
        # silently emitting empty-named columns. (`to_dataframe`'s coercion
        # loop uses .get() only to tolerate a missing, optional `type`.)
        return [(c["name"], c["type"]) for c in self._columns]

    @property
    def column_names(self) -> List[str]:
        return [c["name"] for c in self._columns]

    @property
    def rows(self) -> List[List[Any]]:
        """The raw positional row arrays, in ``columns`` order."""
        return self._rows

    def _normalized_rows(self) -> List[List[Any]]:
        """Rows padded with ``None`` / truncated to the column width.

        The API returns rectangular rows; this only reshapes a ragged slot so
        every view (``records``, ``to_dataframe``) stays consistent instead of
        diverging on messy input.
        """
        width = len(self._columns)
        return [
            row if len(row) == width else list(row[:width]) + [None] * (width - len(row))
            for row in self._rows
        ]

    @property
    def records(self) -> List[Dict[str, Any]]:
        """One dict per row, keyed by column name. No third-party dependency."""
        names = self.column_names
        return [dict(zip(names, row, strict=False)) for row in self._normalized_rows()]

    def to_dataframe(self) -> Any:
        """A pandas ``DataFrame`` with dtypes coerced from the ``columns`` header.

        Requires the optional ``pandas`` extra (``pip install tako-sdk[pandas]``);
        returns a ``pandas.DataFrame`` (typed ``Any`` since pandas is not a hard
        dependency). Coercion is best-effort per column: a column that will not
        cleanly convert is left as-is rather than raising, so a messy slot still
        yields a frame.
        """
        try:
            import pandas as _pandas  # type: ignore[import-not-found,import-untyped]  # pyright: ignore[reportMissingImports]
        except ImportError as exc:  # pragma: no cover - exercised via monkeypatch in tests
            raise ImportError(
                "pandas is required for TakoDatasetView.to_dataframe(); install tako-sdk[pandas]"
            ) from exc

        pd: Any = _pandas  # keep pandas out of the type surface (optional dep)
        names = self.column_names
        # `_normalized_rows` reshapes any ragged row so a messy slot still
        # yields a frame — identically to `.records`.
        frame = pd.DataFrame(self._normalized_rows(), columns=names)
        for column in self._columns:
            name, col_type = column.get("name"), column.get("type")
            if name not in frame:
                continue
            try:
                if col_type in ("date", "datetime"):
                    frame[name] = pd.to_datetime(frame[name], errors="coerce")
                elif col_type == "number":
                    frame[name] = pd.to_numeric(frame[name], errors="coerce")
                elif col_type == "boolean":
                    frame[name] = frame[name].astype("boolean")
                # "string" (and anything unrecognized) stays uncoerced: object
                # under pandas < 3, the new str/string dtype under pandas 3
            except (ValueError, TypeError):
                pass  # leave the column untouched on an unexpected value
        return frame
