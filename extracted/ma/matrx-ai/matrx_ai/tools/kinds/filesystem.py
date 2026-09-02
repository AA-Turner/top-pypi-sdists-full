"""Kinds for the ``fs_*`` workspace-filesystem tool results.

Ledger rows: `fs_read` `fs_write` `fs_list` `fs_search` `fs_patch` `fs_edit`
`fs_mkdir` (KIND_TOOL_LEDGER, agent ``claude-tools-01``).

EVERY ONE OF THESE TOOLS HAS TWO SUCCESS BRANCHES — a sandbox-proxy branch and a
local-filesystem branch — and the two did not return the same keys. The DB
``output_schema`` rows described only the local branch, so the declared shape was
already drifted from what actually flowed (``fs_read``'s paging keys, for one,
appear in NO declared schema). These kinds are the UNION, with branch-only fields
optional and documented as such — the shape has to be true on every path a caller
can actually land on, or the declaration is worse than nothing.

WHY NOT REUSE ``file_text_content`` FOR ``fs_read``
---------------------------------------------------
It looks like a match ({text, truncated, bytes_read, local_path}) and it is not.
``file_text_content.local_path`` means a path on a real local filesystem; an
``fs_read`` path is a workspace/sandbox VFS path, and ``fs_read`` also carries
paging state that kind has no room for. Reuse-first does not mean forcing a
payload into a kind whose fields mean something else — that lie is harder to find
later than a second slug is to justify now.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "file_read_result",
    label="File Read Result",
    family="filesystem",
    example={
        "path": "notes/todo.md",
        "content": "- ship the tools sweep\n",
        "size": 24,
        "truncated": False,
    },
    # PLACEHOLDER — the outer structure, honestly. ``content`` is opaque file
    # text by definition; nothing richer is being flattened away.
    maturity="placeholder",
)
class FileReadResult(KindModel):
    path: str = ""
    content: str = ""
    #: Total file size in bytes (not the length of ``content`` when truncated).
    size: int = 0
    truncated: bool = False
    #: Paging state — present on the sandbox-proxy branch only, which reads in
    #: pages. ``next_offset`` is None when the read reached the end.
    offset: int | None = None
    limit: int | None = None
    next_offset: int | None = None


@kind(
    "file_write_result",
    label="File Write Result",
    family="filesystem",
    example={"path": "notes/todo.md", "bytes_written": 24, "mode": "write"},
    maturity="placeholder",
)
class FileWriteResult(KindModel):
    path: str = ""
    #: Local branch: what was written, and how.
    bytes_written: int | None = None
    #: ``write`` or ``append``.
    mode: str | None = None
    #: Sandbox branch: the resulting file's size, and the proxy's stat block.
    size: int | None = None
    stat: dict | None = None


@kind(
    "directory_entry",
    label="Directory Entry",
    family="filesystem",
    example={
        "name": "todo.md",
        "path": "notes/todo.md",
        "size": 24,
        "is_dir": False,
        "mtime": 1755993600.0,
    },
    maturity="placeholder",
)
class DirectoryEntry(KindModel):
    name: str = ""
    #: Relative to the listed directory.
    path: str = ""
    #: Bytes; 0 for directories. None when the backend did not report a size —
    #: the sandbox branch leaves it unset for some entries, and 0 there would be
    #: a claim about the file rather than an absence of information.
    size: int | None = 0
    is_dir: bool = False
    #: POSIX mtime. Sandbox branch only — the local branch does not stat for it.
    mtime: float | None = None


@kind(
    "directory_listing",
    label="Directory Listing",
    family="filesystem",
    example={
        "path": "notes",
        "entries": [
            {"name": "todo.md", "path": "notes/todo.md", "size": 24, "is_dir": False}
        ],
        "count": 1,
    },
    maturity="placeholder",
)
class DirectoryListing(KindModel):
    path: str = ""
    entries: list[DirectoryEntry] = []
    count: int = 0
    #: The request echo + cap state, returned by the sandbox branch. ``truncated``
    #: is the one that matters to a reader: the listing hit ``limit`` and is
    #: incomplete.
    recursive: bool | None = None
    pattern: str | None = None
    limit: int | None = None
    truncated: bool | None = None


@kind(
    "file_search_match",
    label="File Search Match",
    family="filesystem",
    example={"path": "notes/todo.md", "matches": ["- ship the tools sweep"]},
    maturity="placeholder",
)
class FileSearchMatch(KindModel):
    path: str = ""
    #: Name-search only — the matching file's size.
    size: int | None = None
    #: Content-search only — the matching snippets.
    matches: list[str] = []


@kind(
    "file_search_results",
    label="File Search Results",
    family="filesystem",
    example={
        "results": [{"path": "notes/todo.md", "matches": ["- ship the tools sweep"]}],
        "count": 1,
        "content_search": True,
    },
    maturity="placeholder",
)
class FileSearchResults(KindModel):
    results: list[FileSearchMatch] = []
    count: int = 0
    #: Request echo, returned by the sandbox branch.
    pattern: str | None = None
    path: str | None = None
    #: Whether this searched file CONTENTS or file NAMES — which of
    #: ``FileSearchMatch.matches`` / ``.size`` is populated depends on it.
    content_search: bool | None = None


@kind(
    "file_edit_applied",
    label="Applied File Edit",
    family="filesystem",
    example={"edit_index": 0, "mode": "replace", "delta_chars": -12},
    maturity="placeholder",
)
class FileEditApplied(KindModel):
    #: Zero-based index into the request's ``edits`` array.
    edit_index: int = 0
    #: ``create`` · ``replace`` · ``replace_all``.
    mode: str = ""
    #: ``create`` mode only.
    added_chars: int | None = None
    #: ``replace`` / ``replace_all`` modes only.
    delta_chars: int | None = None
    #: ``replace_all`` mode only.
    matches_replaced: int | None = None


@kind(
    "file_edit_failure",
    label="Failed File Edit",
    family="filesystem",
    example={
        "edit_index": 1,
        "reason": "old_text not found",
        "old_text_preview": "def gone(",
    },
    maturity="placeholder",
)
class FileEditFailure(KindModel):
    edit_index: int = 0
    reason: str = ""
    old_text_preview: str = ""


@kind(
    "file_patch_result",
    label="File Patch Result",
    family="filesystem",
    example={
        "path": "src/main.py",
        "created": False,
        "edits_applied": [{"edit_index": 0, "mode": "replace", "delta_chars": -12}],
        "edits_failed": [],
        "size_before": 512,
        "size_after": 500,
    },
    # PLACEHOLDER, but a partial-success shape: a patch can apply some edits and
    # fail others in the SAME successful result, so ``edits_failed`` being
    # non-empty on a success is normal and must be read, not assumed away.
    maturity="placeholder",
)
class FilePatchResult(KindModel):
    path: str = ""
    created: bool = False
    edits_applied: list[FileEditApplied] = []
    edits_failed: list[FileEditFailure] = []
    #: Character counts around the patch. None = the backend did not report
    #: them; 0 would read as "the file was empty", which is a different claim.
    size_before: int | None = None
    size_after: int | None = None


@kind(
    "file_edit_result",
    label="File Edit Result",
    family="filesystem",
    example={
        "path": "src/main.py",
        "old_str_count": 1,
        "replaced": 1,
        "size_before": 512,
        "size_after": 500,
    },
    maturity="placeholder",
)
class FileEditResult(KindModel):
    path: str = ""
    #: How many times ``old_str`` matched. Diverges from ``replaced`` only when
    #: the caller passed ``replace_all=False`` against a single match.
    old_str_count: int = 0
    replaced: int = 0
    #: Character counts around the edit. None = the backend did not report them
    #: (the durable-VFS branch does not), never a claim that the file was empty.
    size_before: int | None = None
    size_after: int | None = None


@kind(
    "directory_create_result",
    label="Directory Create Result",
    family="filesystem",
    example={"created": "notes/2026"},
    maturity="placeholder",
)
class DirectoryCreateResult(KindModel):
    #: The directory path that was created.
    created: str = ""
    #: Sandbox branch echoes the resolved path as well.
    path: str | None = None
