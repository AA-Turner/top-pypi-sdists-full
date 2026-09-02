from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, RootModel

from matrx_ai.tools.declared import ToolArgs

# Keep in sync with implementations/_web_read_caps.py (DEFAULT_CHARS / MAX_CHARS).
_DEFAULT_CHARS = 8_000
_MAX_CHARS = 40_000


class WebSearchArgs(BaseModel):
    queries: list[str] = Field(min_length=1, max_length=5)
    freshness: str | None = None
    max_results_per_query: int = Field(default=5, ge=1, le=20)


class WebReadArgs(BaseModel):
    urls: list[str] = Field(min_length=1, max_length=10)
    instructions: str = ""
    summarize: bool = False
    offset: int = Field(default=0, ge=0)
    chars: int = Field(default=_DEFAULT_CHARS, ge=1, le=_MAX_CHARS)
    max_content_length: int = Field(default=_DEFAULT_CHARS, ge=1, le=_MAX_CHARS)


RESEARCH_DEPTH_CONFIG: dict[str, dict[str, int]] = {
    "shallow": {"urls_per_query": 3, "good_scrape_threshold": 1000, "target_good_per_query": 2},
    "medium": {"urls_per_query": 5, "good_scrape_threshold": 1000, "target_good_per_query": 3},
    "deep": {"urls_per_query": 8, "good_scrape_threshold": 1000, "target_good_per_query": 5},
    "very_deep": {"urls_per_query": 12, "good_scrape_threshold": 1000, "target_good_per_query": 7},
}


class WebResearchArgs(BaseModel):
    queries: list[str] = Field(min_length=1, max_length=5)
    instructions: str
    freshness: str | None = None
    research_depth: Literal["shallow", "medium", "deep", "very_deep"] = "medium"
    country: str = "us"


# ── Per-action wire contract for the `web` dispatcher ───────────────────────
# These are the models the executor validates the incoming `web` call against
# (one per `action`), assembled into the discriminated-union RootModel `WebArgs`
# registered with @tool. They subclass ToolArgs so extra keys are rejected
# inside the selected variant. Field set per variant == tool_def.parameters
# "$variants". The plain models above stay as inner worker-arg models.
# No Field(description=...) here — descriptions live only in the DB (Rule 4).


class WebSearchWire(ToolArgs):
    action: Literal["search"]
    queries: list[str] = Field(min_length=1, max_length=5)
    freshness: str | None = None
    max_results_per_query: int = Field(default=5, ge=1, le=20)


class WebReadWire(ToolArgs):
    action: Literal["read"]
    url: str
    summarize: bool = False
    instructions: str | None = None
    offset: int = Field(default=0, ge=0)
    chars: int = Field(default=_DEFAULT_CHARS, ge=1, le=_MAX_CHARS)
    max_content_length: int = Field(default=_DEFAULT_CHARS, ge=1, le=_MAX_CHARS)


class WebBatchReadWire(ToolArgs):
    action: Literal["batch_read"]
    urls: list[str] = Field(min_length=1, max_length=10)
    offset: int = Field(default=0, ge=0)
    chars: int = Field(default=_DEFAULT_CHARS, ge=1, le=_MAX_CHARS)
    max_content_length: int = Field(default=_DEFAULT_CHARS, ge=1, le=_MAX_CHARS)


class WebArgs(
    RootModel[
        Annotated[
            Union[WebSearchWire, WebReadWire, WebBatchReadWire],
            Field(discriminator="action"),
        ]
    ]
):
    pass
