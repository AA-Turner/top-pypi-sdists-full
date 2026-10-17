from typing import Annotated, Any, Literal

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
            WebSearchWire | WebReadWire | WebBatchReadWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass


class AdvancedReadArgs(ToolArgs):
    """``advanced_read``: read pages our own reader could not open, through the fast paid readers (fast only)."""

    urls: list[str] = Field(
        min_length=1,
        description="The pages that failed to read (a web read lists them as failed, with what covers them).",
    )
    # No ``allow``: the agent tool is fast-only. Slow structured data is a person's click on the page
    # button, never a model-chosen argument (owner rule, coverage review 2026-10-16).


class SiteDataArgs(ToolArgs):
    """``site_data``: structured records for a covered site (covered-site datasets)."""

    url: str | None = None
    site: str | None = None
    query: str | None = None
    location: str | None = None
    inputs: list[dict[str, Any]] | None = None
    #: Default request stays small; the CEILING is the host limit (checked in the tool), not ``le``.
    max_records: int = Field(default=20, ge=1)
    save_to_table: bool = Field(
        default=False,
        description="When true the records are also saved into a real table the person owns (created in their "
                    "active organization, or added to table_id), and the result carries the table reference.",
    )
    table_name: str | None = Field(default=None, description="Name for the new table (save_to_table only).")
    table_id: str | None = Field(default=None, description="Add to this existing table instead (save_to_table only).")
