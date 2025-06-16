import re
from typing import List, Literal, Optional, Union

from langchain_text_splitters import Language
from pydantic import BaseModel, Field, field_validator, model_validator


class BaseSplitConfig(BaseModel):
    """Base split configuration class"""

    chunk_size: int = Field(default=1500, ge=1, description="chunk max size")
    chunk_overlap: int = Field(
        default=150,
        ge=0,
        description="chunk overlap size, must be less than chunk_size",
    )

    @model_validator(mode="after")
    def validate_config(self) -> "BaseSplitConfig":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return self


class BaseCharSplitConfig(BaseSplitConfig):
    """Base char split configuration class"""

    separators: Optional[List[str]] = Field(
        default=None, description="separator list, if None, use default separators"
    )
    split_regex: Optional[str] = Field(
        default=None, description="split_regex,if set, use it instead of separators"
    )

    @field_validator("split_regex")
    @classmethod
    def validate_regex(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                re.compile(v)
            except re.error as e:
                raise ValueError(f"Invalid regular expression: {str(e)}")
        return v


class MarkdownSplitConfig(BaseSplitConfig):
    type: Literal["markdown"] = "markdown"
    separators: List[str] = Field(
        ...,
        description="""List of separators to split the text. If None, uses default separators""",
    )
    is_separator_regex: bool = Field(
        ...,
        description="""If true, the separators should be in regular expression format.""",
    )
    keep_separator: Optional[Union[bool, Literal["start", "end"]]] = Field(
        default=False,
        description="""Whether to keep the separator and where to place it in each corresponding chunk (True='start')""",
    )
    extract_header_first: Optional[bool] = Field(
        default=False,
        description="""If true, will split markdown by header first""",
    )
    # TODO :extract images,table,code


class PDFSplitConfig(BaseSplitConfig):
    """PDF document split configuration"""

    type: Literal["pdf"] = "pdf"
    extract_images: bool = Field(default=False, description="Whether to extract images")
    table_extract_mode: str = Field(
        default="text", description="Table extraction mode: 'text' or 'structure'"
    )


class TextSplitConfig(BaseCharSplitConfig):
    """Plain text split configuration"""

    type: Literal["text"] = "text"
    separators: List[str] = Field(
        ...,
        description="""List of separators to split the text. If None, uses default separators""",
    )
    is_separator_regex: bool = Field(
        ...,
        description="""If true, the separators should be in regular expression format.""",
    )
    keep_separator: Optional[Union[bool, Literal["start", "end"]]] = Field(
        default=False,
        description="""Whether to keep the separator and where to place it in each corresponding chunk (True='start')""",
    )


class JSONSplitConfig(BaseModel):
    """
    JSON document split configuration
    @link {https://python.langchain.com/api_reference/text_splitters/json/langchain_text_splitters.json.RecursiveJsonSplitter.html}
    """

    type: Literal["json"] = "json"
    max_chunk_size: int = Field(
        default=2000,
        description=""" The maximum size for each chunk. Defaults to 2000 """,
    )
    min_chunk_size: Optional[int] = Field(
        default=200,
        description="""The minimum size for a chunk. If None,
                defaults to the maximum chunk size minus 200, with a lower bound of 50.""",
    )


class YuqueSplitConfig(BaseSplitConfig):
    type: Literal["yuque"] = "yuque"
    separators: List[str] = Field(
        ...,
        description="""List of separators to split the text. If None, uses default separators""",
    )
    is_separator_regex: bool = Field(
        ...,
        description="""If true, the separators should be in regular expression format.""",
    )


class GeaGraphSplitConfig(BaseModel):
    """
    JSON document split configuration
    @link {https://python.langchain.com/api_reference/text_splitters/json/langchain_text_splitters.json.RecursiveJsonSplitter.html}
    """

    type: Literal["geagraph"] = "geagraph"
    kisId: int = Field(
        ...,
        description=""" The Kis platform business id  """,
    )


class GithubRepoParseConfig(BaseSplitConfig):
    type: Literal["github_repo"] = "github_repo"
    include_patterns: Optional[list[str]] = Field(
        default=None,
        description="List of include patterns (comma-separated) to filter files in the repo.Only files matching these patterns will be included, unless excluded by ignore_patterns or .gitignore. Lower priority than ignore_patterns and .gitignore.",
    )
    ignore_patterns: Optional[list[str]] = Field(
        default=None,
        description="Additional ignore patterns (comma-separated) to exclude files in the repo. Highest priority, overrides include_patterns and .gitignore.",
    )
    use_gitignore: Optional[bool] = Field(
        default=True,
        description="Whether to respect .gitignore rules when filtering files. Priority is lower than ignore_patterns, higher than include_patterns.",
    )
    use_default_ignore: Optional[bool] = Field(
        default=True,
        description="Whether to use default ignore patterns (e.g. .git/*, *.pyc, etc). Lowest priority.",
    )


class BaseCodeSplitConfig(BaseModel):
    """
    Code document split configuration
    """

    type: Literal["base_code"] = "base_code"
    language: Language = Field(
        ...,
        description="""The programming language of the code.""",
    )
    chunk_size: int = Field(default=1500, ge=1, description="chunk max size for code")
    chunk_overlap: int = Field(
        default=150,
        ge=0,
        description="chunk overlap size for code, must be less than chunk_size",
    )


class ImageSplitConfig(BaseModel):
    type: Literal["image"] = "image"


KnowledgeSplitConfig = Union[
    BaseCharSplitConfig,
    MarkdownSplitConfig,
    TextSplitConfig,
    JSONSplitConfig,
    PDFSplitConfig,
    GeaGraphSplitConfig,
    GithubRepoParseConfig,
    BaseCodeSplitConfig,
]
