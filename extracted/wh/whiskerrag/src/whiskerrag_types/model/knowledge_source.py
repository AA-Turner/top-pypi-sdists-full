from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, field_validator


class KnowledgeSourceEnum(str, Enum):
    """
    Specifies the source of knowledge, which influences the behavior of the resource loader
    """

    GITHUB_REPO = "github_repo"
    GITHUB_FILE = "github_file"
    USER_INPUT_TEXT = "user_input_text"
    CLOUD_STORAGE_TEXT = "cloud_storage_text"
    CLOUD_STORAGE_IMAGE = "cloud_storage_image"
    YUQUE = "yuque"


class GithubRepoSourceConfig(BaseModel):
    repo_name: str = Field(..., description="github repo url")
    url: str = Field(
        default="https://github.com",
        description="remote origin of the repo, must start with http:// or https://",
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls: Any, v: str) -> str:
        if not (
            isinstance(v, str) and (v.startswith("http://") or v.startswith("https://"))
        ):
            raise ValueError("url must start with http:// or https://")
        return v

    branch: Optional[str] = Field(None, description="branch name of the repo")
    commit_id: Optional[str] = Field(None, description="commit id of the repo")
    auth_info: Optional[str] = Field(None, description="authentication information")


class GithubFileSourceConfig(GithubRepoSourceConfig):
    path: str = Field(..., description="path of the file in the repo")


class S3SourceConfig(BaseModel):
    bucket: str = Field(..., description="s3 bucket name")
    key: str = Field(..., description="s3 key")
    version_id: Optional[str] = Field(None, description="s3 version id")
    region: Optional[str] = Field(None, description="s3 region")
    access_key: Optional[str] = Field(None, description="s3 access key")
    secret_key: Optional[str] = Field(None, description="s3 secret key")
    auth_info: Optional[str] = Field(None, description="s3 session token")


class OpenUrlSourceConfig(BaseModel):
    url: str = Field(..., description="cloud storage url, such as oss, cos, etc.")


class OpenIdSourceConfig(BaseModel):
    id: str = Field(..., description="cloud storage file id, used for afts")


class YuqueSourceConfig(BaseModel):
    api_url: str = Field(
        default="https://www.yuque.com",
        description="the yuque api url",
    )
    group_login: str = Field(..., description="the yuque group id")
    book_slug: Optional[str] = Field(
        default=None,
        description="the yuque book id, if not set, will use the group all book",
    )
    document_id: Optional[Union[str, int]] = Field(
        default=None,
        description="the yuque document id in book, if not set, will use the book all doc",
    )
    auth_info: str = Field(..., description="authentication information")


class TextSourceConfig(BaseModel):
    text: str = Field(
        default="",
        min_length=1,
        max_length=30000,
        description="Text content, length range 1-30000 characters",
    )


KnowledgeSourceConfig = Union[
    GithubRepoSourceConfig,
    GithubFileSourceConfig,
    S3SourceConfig,
    OpenUrlSourceConfig,
    TextSourceConfig,
    YuqueSourceConfig,
]
