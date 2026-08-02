"""Shared types for the web_search builtin."""

import os
from typing import Annotated, Protocol

from pydantic import BaseModel, Field, StringConstraints, field_validator


class WebSearchSource(BaseModel):
    title: str
    url: str


class WebSearchArgs(BaseModel):
    query: str = Field(min_length=1, description="Search query to run on the web.")

    @field_validator("query")
    @classmethod
    def _normalize_query(cls, value: str) -> str:
        query = value.strip()
        if not query:
            raise ValueError("Search query cannot be empty.")
        return query


class WebSearchContext(BaseModel):
    api_key_env_var: (
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None
    ) = Field(
        description="Environment variable containing the provider API key.",
    )
    provider: str = Field(
        description="Model provider to use for web search.",
    )
    model: str = Field(
        description="Model to use for web search.",
    )
    timeout_seconds: int = Field(
        gt=0,
        description="HTTP timeout in seconds.",
    )
    server_url: str = Field(
        description="Provider endpoint URL.",
    )
    http_headers: dict[str, str] = Field(
        default_factory=dict,
        description="Additional HTTP headers to send to the provider.",
    )

    @property
    def resolved_api_key(self) -> str | None:
        if self.http_headers:
            return None
        if self.api_key_env_var is None:
            raise ValueError("web_search requires either api_key_env_var or http_headers.")

        api_key = os.getenv(self.api_key_env_var, "").strip()
        if not api_key:
            raise ValueError(f"{self.api_key_env_var} environment variable not set.")
        return api_key

    @field_validator("provider", "model", "server_url")
    @classmethod
    def _normalize_required_string(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Value cannot be empty.")
        return normalized


class WebSearchResult(BaseModel):
    answer: str
    sources: list[WebSearchSource] = Field(default_factory=list)


class WebSearchGateway(Protocol):
    async def search(
        self,
        *,
        args: WebSearchArgs,
        context: WebSearchContext,
    ) -> WebSearchResult: ...
