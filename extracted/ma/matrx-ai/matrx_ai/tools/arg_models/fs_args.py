from pydantic import BaseModel, Field

from matrx_ai.tools.declared import ToolArgs


class FsReadArgs(BaseModel):
    path: str
    offset: int = Field(default=0, ge=0, le=9_223_372_036_854_775_807)
    limit: int = Field(default=0, ge=0, le=4_194_304)


class FsWriteArgs(BaseModel):
    path: str
    content: str
    create_dirs: bool = True
    append: bool = False


class FsListArgs(ToolArgs):
    path: str = "."
    recursive: bool = False
    pattern: str = ""


class FsSearchArgs(BaseModel):
    pattern: str
    path: str = "."
    content_search: bool = False
    max_results: int = Field(default=50, ge=1, le=500)


class FsMkdirArgs(BaseModel):
    path: str
    parents: bool = True


class FsEditArgs(BaseModel):
    path: str
    old_str: str
    new_str: str
    replace_all: bool = False


class FsPatchEdit(BaseModel):
    old_text: str
    new_text: str
    replace_all: bool = False


class FsPatchArgs(BaseModel):
    path: str
    edits: list[FsPatchEdit] = Field(min_length=1)
    create_if_missing: bool = False
