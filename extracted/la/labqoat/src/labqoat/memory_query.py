"""Explicit retrieval modes, evidence budgets and scopes for research memory."""

from dataclasses import asdict, dataclass
from typing import Literal


@dataclass(frozen=True, kw_only=True)
class MemoryQuery:
    """A reusable search request whose filters must be retained across continuations."""

    query: str = ""
    mode: Literal["hybrid", "lexical", "semantic"] = "hybrid"
    depth: int = 2
    max_bytes: int | None = None
    limit: int | None = None
    after: str | None = None
    kind: str | None = None
    run_id: str | None = None
    node: str | None = None
    include_all: bool = False

    def to_params(self) -> dict[str, str | int]:
        """Encode the public HTTP query without empty selectors."""
        params = {name: value for name, value in asdict(self).items() if value is not None}
        del params["include_all"]
        params["all"] = str(self.include_all).lower()
        return params
