"""Canonical package for SDK-provided builtin capabilities."""

import sys
from importlib import import_module
from types import ModuleType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ask_user_question_tool import (
        Answer,
        AskUserQuestionArgs,
        AskUserQuestionResult,
        Choice,
        Question,
        ask_user_question,
    )
    from .bash_tool import BashArgs, BashResult, bash
    from .grep_tool import GrepArgs, GrepResult, grep
    from .read_file_tool import ReadFileArgs, ReadFileResult, read_file
    from .sandbox_dispatch import (
        SANDBOX_DISPATCHABLE_TOOLS,
        SandboxTool,
        SandboxToolArgs,
        SandboxToolResult,
        parse_sandbox_tool_args,
        parse_sandbox_tool_result,
        sandbox_tool,
        sandbox_tool_for,
    )
    from .search_replace_tool import (
        SEARCH_REPLACE_ANNOTATION_KEY,
        SearchReplaceAnnotations,
        SearchReplaceArgs,
        SearchReplaceBlock,
        SearchReplaceContext,
        SearchReplacePreviewBlock,
        SearchReplaceResult,
        search_replace,
    )
    from .skill_tool import SkillArgs, SkillResult, SkillToolContext, skill
    from .todo_tool import TodoArgs, TodoCounts, TodoItem, TodoResult, todo
    from .web_fetch import WebFetchArgs, WebFetchResult, web_fetch
    from .web_search import (
        WebSearchArgs,
        WebSearchContext,
        WebSearchResult,
        WebSearchSource,
        web_search,
    )
    from .write_file_tool import (
        WRITE_FILE_ANNOTATION_KEY,
        WriteFileAnnotations,
        WriteFileArgs,
        WriteFileResult,
        write_file,
    )

__all__ = [
    "Answer",
    "AskUserQuestionArgs",
    "AskUserQuestionResult",
    "BashArgs",
    "BashResult",
    "Choice",
    "GrepArgs",
    "GrepResult",
    "Question",
    "ReadFileArgs",
    "ReadFileResult",
    "SANDBOX_DISPATCHABLE_TOOLS",
    "SEARCH_REPLACE_ANNOTATION_KEY",
    "SandboxTool",
    "SandboxToolArgs",
    "SandboxToolResult",
    "SearchReplaceAnnotations",
    "SearchReplaceArgs",
    "SearchReplaceBlock",
    "SearchReplaceContext",
    "SearchReplacePreviewBlock",
    "SearchReplaceResult",
    "SkillArgs",
    "SkillResult",
    "SkillToolContext",
    "TodoArgs",
    "TodoCounts",
    "TodoItem",
    "TodoResult",
    "WebFetchArgs",
    "WebFetchResult",
    "WebSearchArgs",
    "WebSearchContext",
    "WebSearchResult",
    "WebSearchSource",
    "WriteFileArgs",
    "WriteFileAnnotations",
    "WriteFileResult",
    "WRITE_FILE_ANNOTATION_KEY",
    "ask_user_question",
    "bash",
    "grep",
    "parse_sandbox_tool_args",
    "parse_sandbox_tool_result",
    "read_file",
    "sandbox_tool",
    "sandbox_tool_for",
    "search_replace",
    "skill",
    "todo",
    "web_fetch",
    "web_search",
    "write_file",
]

_LAZY_EXPORTS = {
    "Answer": "mistralai.vibe.sdk.capabilities.builtins.ask_user_question_tool",
    "AskUserQuestionArgs": "mistralai.vibe.sdk.capabilities.builtins.ask_user_question_tool",
    "AskUserQuestionResult": "mistralai.vibe.sdk.capabilities.builtins.ask_user_question_tool",
    "BashArgs": "mistralai.vibe.sdk.capabilities.builtins.bash_tool",
    "BashResult": "mistralai.vibe.sdk.capabilities.builtins.bash_tool",
    "Choice": "mistralai.vibe.sdk.capabilities.builtins.ask_user_question_tool",
    "GrepArgs": "mistralai.vibe.sdk.capabilities.builtins.grep_tool",
    "GrepResult": "mistralai.vibe.sdk.capabilities.builtins.grep_tool",
    "Question": "mistralai.vibe.sdk.capabilities.builtins.ask_user_question_tool",
    "ReadFileArgs": "mistralai.vibe.sdk.capabilities.builtins.read_file_tool",
    "ReadFileResult": "mistralai.vibe.sdk.capabilities.builtins.read_file_tool",
    "SANDBOX_DISPATCHABLE_TOOLS": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "SEARCH_REPLACE_ANNOTATION_KEY": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "SandboxTool": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "SandboxToolArgs": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "SandboxToolResult": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "SearchReplaceAnnotations": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "SearchReplaceArgs": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "SearchReplaceBlock": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "SearchReplaceContext": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "SearchReplacePreviewBlock": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "SearchReplaceResult": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "SkillArgs": "mistralai.vibe.sdk.capabilities.builtins.skill_tool",
    "SkillResult": "mistralai.vibe.sdk.capabilities.builtins.skill_tool",
    "SkillToolContext": "mistralai.vibe.sdk.capabilities.builtins.skill_tool",
    "TodoArgs": "mistralai.vibe.sdk.capabilities.builtins.todo_tool",
    "TodoCounts": "mistralai.vibe.sdk.capabilities.builtins.todo_tool",
    "TodoItem": "mistralai.vibe.sdk.capabilities.builtins.todo_tool",
    "TodoResult": "mistralai.vibe.sdk.capabilities.builtins.todo_tool",
    "WebFetchArgs": "mistralai.vibe.sdk.capabilities.builtins.web_fetch",
    "WebFetchResult": "mistralai.vibe.sdk.capabilities.builtins.web_fetch",
    "WebSearchArgs": "mistralai.vibe.sdk.capabilities.builtins.web_search",
    "WebSearchContext": "mistralai.vibe.sdk.capabilities.builtins.web_search",
    "WebSearchResult": "mistralai.vibe.sdk.capabilities.builtins.web_search",
    "WebSearchSource": "mistralai.vibe.sdk.capabilities.builtins.web_search",
    "WriteFileArgs": "mistralai.vibe.sdk.capabilities.builtins.write_file_tool",
    "WriteFileAnnotations": "mistralai.vibe.sdk.capabilities.builtins.write_file_tool",
    "WriteFileResult": "mistralai.vibe.sdk.capabilities.builtins.write_file_tool",
    "WRITE_FILE_ANNOTATION_KEY": "mistralai.vibe.sdk.capabilities.builtins.write_file_tool",
    "ask_user_question": "mistralai.vibe.sdk.capabilities.builtins.ask_user_question_tool",
    "bash": "mistralai.vibe.sdk.capabilities.builtins.bash_tool",
    "grep": "mistralai.vibe.sdk.capabilities.builtins.grep_tool",
    "parse_sandbox_tool_args": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "parse_sandbox_tool_result": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "read_file": "mistralai.vibe.sdk.capabilities.builtins.read_file_tool",
    "sandbox_tool": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "sandbox_tool_for": "mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch",
    "search_replace": "mistralai.vibe.sdk.capabilities.builtins.search_replace_tool",
    "skill": "mistralai.vibe.sdk.capabilities.builtins.skill_tool",
    "todo": "mistralai.vibe.sdk.capabilities.builtins.todo_tool",
    "web_fetch": "mistralai.vibe.sdk.capabilities.builtins.web_fetch",
    "web_search": "mistralai.vibe.sdk.capabilities.builtins.web_search",
    "write_file": "mistralai.vibe.sdk.capabilities.builtins.write_file_tool",
}

_COLLIDING_SUBPACKAGE_EXPORTS = {"web_fetch", "web_search"}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value


class _BuiltinsModule(ModuleType):
    def __getattribute__(self, name: str) -> Any:
        # Preserve root barrel exports when Python has written a same-named
        # imported subpackage onto this parent module.
        if name in _COLLIDING_SUBPACKAGE_EXPORTS and isinstance(globals().get(name), ModuleType):
            return __getattr__(name)
        return super().__getattribute__(name)


sys.modules[__name__].__class__ = _BuiltinsModule
