from abc import ABC
from enum import Enum
from typing import Annotated, Any, ClassVar, Literal

from pydantic import BaseModel, Field

WRITE_STRATEGY_FULL_FILE_REWRITE: Literal["FULL_FILE_REWRITE"] = "FULL_FILE_REWRITE"
DEFAULT_CODE_BLOCK_TIMEOUT = 30
WRITE_STRATEGY_NATURAL_EDIT: Literal["NATURAL_EDIT"] = "NATURAL_EDIT"
WRITE_STRATEGY_SEARCH_REPLACE: Literal["SEARCH_REPLACE"] = "SEARCH_REPLACE"
WRITE_STRATEGY_UDIFF: Literal["UDIFF"] = "UDIFF"

FileWriteStrategyName = Literal[
    "FULL_FILE_REWRITE", "UDIFF", "SEARCH_REPLACE", "NATURAL_EDIT"
]


class CommandType(str, Enum):
    THINKING = "thinking"
    FILE_READ = "file_read"
    SUMMARIZE = "summarize"
    STEP_OUTPUT = "step_output"
    PROTOTYPE = "prototype"
    DB_QUERY = "db_query"
    DB_GET_TABLE_NAMES = "db_get_table_names"
    DB_GET_TABLE_SCHEMA = "db_get_table_schema"
    ANSWER = "answer"
    ASK = "ask"
    SHELL = "shell"
    PYTHON = "python"
    FILE_WRITE = "file_write"


class CommandData(BaseModel):
    executable: ClassVar[bool]


class FileReadCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.FILE_READ] = CommandType.FILE_READ

    file_path: str
    language: str
    limit: int | None = None
    offset: int | None = None


class ThinkingCommandData(CommandData):
    executable: ClassVar[bool] = False
    type: Literal[CommandType.THINKING] = CommandType.THINKING

    content: str
    signature: str | None = None


class PrototypeCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.PROTOTYPE] = CommandType.PROTOTYPE

    command_name: str
    # Structured data extracted from LLM output
    content_json: dict[str, Any]
    # Raw text extracted from LLM output
    content_raw: str
    # Rendered LLM output for frontend display
    content_rendered: str

    llm_command_name_override: str | None = None

    @property
    def llm_command_name(self) -> str:
        return self.llm_command_name_override or self.command_name


# deprecated, use StepOutputCommandData instead
class SummarizeCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.SUMMARIZE] = CommandType.SUMMARIZE

    summary: str


class StepOutputCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.STEP_OUTPUT] = CommandType.STEP_OUTPUT

    step_output_raw: str


DEFAULT_DB_QUERY_TIMEOUT_SECONDS = 300  # 5 minutes
MAX_DB_QUERY_TIMEOUT_SECONDS = 900  # 15 minutes


class DBQueryCommandData(CommandData):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    executable: ClassVar[bool] = True
    type: Literal[CommandType.DB_QUERY] = CommandType.DB_QUERY

    query: str
    max_gigabytes_billed: float | None = None  # BigQuery only
    timeout_seconds: int = DEFAULT_DB_QUERY_TIMEOUT_SECONDS


class DBGetTableNamesCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.DB_GET_TABLE_NAMES] = CommandType.DB_GET_TABLE_NAMES


class DBGetTableSchemaCommandData(CommandData):
    executable: ClassVar[bool] = True
    type: Literal[CommandType.DB_GET_TABLE_SCHEMA] = CommandType.DB_GET_TABLE_SCHEMA

    table_name: str


class AnswerCommandData(CommandData):
    executable: ClassVar[bool] = False
    type: Literal[CommandType.ANSWER] = CommandType.ANSWER

    answer_raw: str


class AskCommandData(CommandData):
    executable: ClassVar[bool] = False
    type: Literal[CommandType.ASK] = CommandType.ASK

    ask_raw: str


class ShellCommandData(CommandData):
    exclude_from_schema_gen: ClassVar[bool] = True

    executable: ClassVar[bool] = True
    type: Literal[CommandType.SHELL] = CommandType.SHELL

    timeout: int = DEFAULT_CODE_BLOCK_TIMEOUT
    content: str


class PythonCommandData(CommandData):
    exclude_from_schema_gen: ClassVar[bool] = True

    executable: ClassVar[bool] = True
    type: Literal[CommandType.PYTHON] = CommandType.PYTHON

    content: str


class EditContent(BaseModel):
    content: str
    original_file: str | None = None


class NaturalEditContent(BaseModel):
    natural_edit: str
    intermediate_edit: str | None
    original_file: str | None
    new_file: str | None
    error_content: str | None

    @property
    def is_resolved(self) -> bool:
        return self.new_file is not None or self.error_content is not None

    @property
    def is_noop(self) -> bool:
        return bool(
            self.new_file is not None
            and self.original_file is not None
            and self.new_file == self.original_file
        )


class FileWriteCommandData(CommandData):
    exclude_from_schema_gen: ClassVar[bool] = True

    executable: ClassVar[bool] = True
    type: Literal[CommandType.FILE_WRITE] = CommandType.FILE_WRITE

    file_path: str
    language: str
    write_strategy: FileWriteStrategyName
    write_content: NaturalEditContent | EditContent
    content: str


CommandDataType = Annotated[
    FileReadCommandData
    | ThinkingCommandData
    | PrototypeCommandData
    | SummarizeCommandData
    | DBQueryCommandData
    | DBGetTableNamesCommandData
    | DBGetTableSchemaCommandData
    | StepOutputCommandData
    | AnswerCommandData
    | AskCommandData
    | ShellCommandData
    | PythonCommandData
    | FileWriteCommandData,
    Field(discriminator="type"),
]


class CommandImpl(ABC):
    command_data_type: ClassVar[type[CommandData]]
