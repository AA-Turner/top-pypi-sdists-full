from typing import Literal

from pydantic import BaseModel, Field


class RagSearchArgs(BaseModel):
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
