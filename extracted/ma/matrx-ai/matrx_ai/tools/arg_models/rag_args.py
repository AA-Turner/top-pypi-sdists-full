from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeWithinArg(BaseModel):
    """A container to search within (Knowledge Hub §2 ``within``)."""

    model_config = ConfigDict(extra="forbid")

    type: str = Field(min_length=1, description="project, scope, tag, library, data_store, research_topic, or source")
    id: str | None = None
    label: str | None = None


class KnowledgeDateArg(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    field: Literal["created", "updated", "captured"] = "updated"
    from_: str | None = Field(default=None, alias="from")
    to: str | None = None
    relative: str | None = None


class RagSearchArgs(BaseModel):
    """``knowledge_search`` — the Knowledge Hub query (§2) PLUS every field the tool took
    before it became a caller of the one search service. Old fields map internally:
    ``query`` is the query text, ``data_store_id`` → within a data store, ``source_ids`` →
    within those Sources, ``rerank`` / ``use_mmr`` / ``multi_query`` / ``use_hyde`` → the
    passage lane's switches."""

    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    rerank: bool = True
    use_mmr: bool = True
    multi_query: int = Field(default=1, ge=1, le=5)
    use_hyde: bool = False
    source_kinds: list[
        Literal[
            "cld_file",
            "note",
            "code_file",
            "library_doc",
            "transcript",
            "scraped",
            "repository",
            "task",
            "project",
            "web_page",
            "scrape_parsed_page",
            "inline",
        ]
    ] | None = None
    data_store_id: str | None = None
    scope_ids: list[str] | None = Field(default=None)
    # Hard-scope retrieval to specific source rows by their source_id (e.g. cld_file
    # file_ids for a thread's attached files). None = unfiltered (today's behavior).
    # Additive: combines (AND) with every other filter and with the user/org ACL — a
    # source the caller can't see is still never returned. This is how an agent searches
    # exactly the files attached to its thread.
    source_ids: list[str] | None = Field(default=None)
    # ── the Knowledge Hub query (§2) ─────────────────────────────────────────────────
    types: list[str] | None = None
    within: list[KnowledgeWithinArg] | None = None
    entities: list[str] | None = None
    captured_by: Literal["me", "anyone"] | list[str] | None = None
    origin: list[str] | None = None
    date: KnowledgeDateArg | None = None
    state: list[Literal["inbox", "kept", "archived"]] | None = None
    # The ORGANIZATION FILTER (policies/access-ladder.md): organization ids to
    # search, null = every organization the caller belongs to. Never derived from the active
    # organization, which only attributes the call.
    organizations: list[str] | None = Field(
        default=None,
        description="Organization ids to search. Omit (null) to search every organization you belong to.",
    )
    sort: Literal["relevance", "recent", "title"] = "relevance"
    cursors: dict[str, str] | None = None
