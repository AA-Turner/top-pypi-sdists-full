from typing import Literal

from pydantic import BaseModel, Field


class GitIngestArgs(BaseModel):
    source: str = Field(min_length=1)
    mode: Literal["summary", "tree", "digest"] = "digest"
    include: list[str] | None = None
    exclude: list[str] | None = None
    max_file_size: int = Field(default=1_048_576, ge=1_024, le=10_485_760)
    branch: str | None = None
    include_submodules: bool = False
    token: str | None = None
    max_chars: int = Field(default=50_000, ge=500, le=500_000)


class LlmsTxtFetchArgs(BaseModel):
    url: str = Field(min_length=1)
    full: bool = False
    max_chars: int = Field(default=50_000, ge=500, le=500_000)


class PackageInfoArgs(BaseModel):
    name: str = Field(min_length=1)
    ecosystem: Literal["pypi", "npm"] = "pypi"
    include_readme: bool = True
    max_chars: int = Field(default=20_000, ge=500, le=200_000)
