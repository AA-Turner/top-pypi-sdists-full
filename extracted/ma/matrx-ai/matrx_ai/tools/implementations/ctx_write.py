"""Deferred context write tools — `context_patch` and the `create` action.

These are the write-side counterparts to the `context` reader. They let the
model mutate any context object (text, json, notes, code, documents, arbitrary
records) that was placed in the request's ContextManifest — without forcing a
round trip to the client and without inventing one narrow tool per widget.

`context_patch` edits an existing object; the `create` action (dispatched by
the `context` tool in ctx.py, which calls `ctx_create` here) spawns a new one.

Why this shape
--------------
Frontier models (Claude, GPT, Gemini) are heavily trained on two edit shapes:

  1. Anthropic's built-in `str_replace_based_edit_tool` with its
     ``command`` dispatcher (``str_replace``, ``insert``, etc.).
  2. RFC 6902 JSON Patch and RFC 7396 JSON Merge Patch.

`context_patch` exposes both through a single ``command`` field so the model
uses exactly the vocabulary it already knows. No novel DSL, no bespoke
arguments — just the patterns every modern model has seen tens of thousands
of times in its training data. It is kept SEPARATE from the `context` reader
(rather than folded in as another action) so the ``command`` patch dispatcher
never nests under an ``action`` dispatcher.

Flow
----
1. Model calls ``context_patch(key="<k>", command="str_replace", old_str=..., new_str=...)``.
2. We resolve the ContextObject from the manifest stored on AppContext.metadata.
3. We apply the edit to an in-memory copy (using the same 4-level fuzzy matcher
   that powers note_patch for text edits).
4. We write the new content back into the manifest and persist it on app_ctx
   so subsequent ``context`` / ``context_patch`` calls see the fresh value.
5. We emit a ``context_delta`` stream event carrying the edit's CONTENT (a
   compact splice, or the full new content) so the client applies it live,
   then a ``context_changed`` event (content-free, unchanged semantics) so
   legacy consumers can still schedule a re-read/persist downstream.

`ctx_create` is the same story for spawning a brand-new object: the model can
compose a fresh artifact (note draft, analysis result, structured record) and
put it in the manifest so later turns — and the client — can reach it.

DB rows register `context_patch` with ``source_kind='native'`` and NO
tool_binding row (it dispatches server-side via matrx-ai-core like every other
grouped native tool — note/memory/task/etc.).
"""

from __future__ import annotations

import itertools
import json
import time
import traceback
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import CtxPatchArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

# Valid `ctx_patch` commands are enforced by the CtxPatchArgs discriminated union
# (arg_models/dispatcher_args.py) + tool_def.parameters."$variants" — the source of truth.
# _TEXT_COMMANDS / _JSON_COMMANDS below classify a (already-validated) command for routing.
_TEXT_COMMANDS = frozenset({"str_replace", "insert", "append", "prepend", "overwrite"})
_JSON_COMMANDS = frozenset({"json_patch", "json_merge"})


# ---------------------------------------------------------------------------
# context_patch  (the consolidated successor name for the legacy ctx_patch)
# ---------------------------------------------------------------------------


async def context_patch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    tool_name = "context_patch"

    # Validate against the per-command discriminated union (the executor already
    # did this pre-dispatch; re-derive here so the body is bound to the contract
    # the drift gate proves against the DB).
    try:
        parsed = CtxPatchArgs.model_validate(args).root
    except ValidationError as exc:
        return _validation_err(
            tool_name,
            ctx.call_id,
            started_at,
            format_args_error(exc),
            "Re-read the tool's input schema and call it again with exactly the "
            "documented arguments for that command.",
        )
    key = parsed.key.strip()
    command = parsed.command

    try:
        manifest, app_ctx = _load_manifest_or_none()
        if manifest is None:
            return _not_found(
                tool_name,
                ctx.call_id,
                started_at,
                "No context objects are available for this request.",
                "The caller must include a context dict in the request body.",
            )

        obj = manifest.get(key)

        # Allow create-on-miss for ergonomics; opt-in so the model doesn't
        # silently spawn objects when it meant to edit an existing one.
        if obj is None:
            if args.get("create_if_missing") and command in {"overwrite", "append", "prepend"}:
                return await _create_from_patch(args, ctx, started_at)
            available = [o.key for o in manifest.all()]
            return _not_found(
                tool_name,
                ctx.call_id,
                started_at,
                f"Context object '{key}' not found.",
                f"Available keys: {available}. Pass create_if_missing=true to create it.",
            )

        # Access control: caller must have flagged the object mutable.
        if not obj.mutable:
            return _validation_err(
                tool_name,
                ctx.call_id,
                started_at,
                f"Context object '{key}' is read-only and cannot be edited.",
                f"Editable keys: {manifest.mutable_keys() or '(none)'}. "
                "Tell the user you cannot modify this item directly; suggest "
                "an alternative or ask them to mark the item editable.",
            )

        # Text commands operate on stringified content.
        if command in _TEXT_COMMANDS:
            old_content = obj.content_as_str()
            new_content, pass_info = _apply_text_command(command, old_content, args)
            updated = _write_back(app_ctx, manifest, key, new_content)
            # Delta FIRST so a client that applied it can skip the re-read the
            # follow-up context_changed would otherwise trigger.
            await _emit_context_delta(
                ctx,
                obj=updated,
                command=command,
                old_content=old_content,
                new_content=new_content,
            )
            await _emit_context_changed(ctx, obj=updated, command=command)
            _schedule_writeback(ctx, updated, command=command)
            from matrx_ai.tools.kinds.context_tools import ContextWriteResult

            return _success(
                tool_name,
                ctx.call_id,
                started_at,
                output=ContextWriteResult(
                    key=key,
                    command=str(command),
                    matched_at_pass=pass_info,
                    new_size_chars=len(new_content),
                    persist=updated.persist.value,
                ),
            )

        # JSON commands require dict/list content; stringify only for the envelope.
        if command in _JSON_COMMANDS:
            if not isinstance(obj.content, (dict, list)):
                # Try to parse JSON strings — common when text was stored as JSON.
                parsed = _try_parse_json(obj.content)
                if parsed is None:
                    return _validation_err(
                        tool_name,
                        ctx.call_id,
                        started_at,
                        f"Context object '{key}' is not JSON-structured; "
                        f"command '{command}' requires dict/list content.",
                        "Use command='str_replace', 'insert', 'append', 'prepend', "
                        "or 'overwrite' for text content.",
                    )
                working = parsed
            else:
                working = obj.content

            new_content = _apply_json_command(command, working, args)
            updated = _write_back(app_ctx, manifest, key, new_content)
            await _emit_context_delta(
                ctx,
                obj=updated,
                command=command,
                old_content=None,  # structured content → full form
                new_content=new_content,
            )
            await _emit_context_changed(ctx, obj=updated, command=command)
            _schedule_writeback(ctx, updated, command=command)
            from matrx_ai.tools.kinds.context_tools import ContextWriteResult

            return _success(
                tool_name,
                ctx.call_id,
                started_at,
                output=ContextWriteResult(
                    key=key,
                    command=str(command),
                    persist=updated.persist.value,
                ),
            )

        # Defensive — validated above.
        return _validation_err(
            tool_name,
            ctx.call_id,
            started_at,
            f"Unhandled command: {command}",
            None,
        )

    except _PatchApplyError as pe:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type=pe.error_type,
                message=pe.message,
                suggested_action=pe.suggestion,
                is_retryable=pe.retryable,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"context_patch failed: {e}",
                traceback=traceback.format_exc(),
                is_retryable=False,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )


# ---------------------------------------------------------------------------
# ctx_create — internal impl for the `context` dispatcher's `create` action.
# The dispatcher validates the call against ContextArgs and enforces the
# allow_context_create gate before routing here.
# ---------------------------------------------------------------------------


async def ctx_create(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    return await _create_from_patch(args, ctx, started_at, tool_name="context")


async def _create_from_patch(
    args: dict[str, Any],
    ctx: ToolContext,
    started_at: float,
    tool_name: str = "context_patch",
) -> ToolResult:
    key = (args.get("key") or "").strip()
    content = args.get("content")
    if content is None:
        # ctx_patch create-on-miss flavor uses new_str as the seed.
        content = args.get("new_str", "")

    if not key:
        return _validation_err(
            tool_name,
            ctx.call_id,
            started_at,
            "key is required.",
            "Provide a unique key for the new context object.",
        )

    obj_type_raw = (args.get("type") or "").strip()
    label = (args.get("label") or "").strip() or key.replace("_", " ").title()
    description = args.get("description") or ""
    overwrite = bool(args.get("overwrite_existing", False))

    try:
        from matrx_ai._ext import get_ext
        from matrx_ai.context.app_context import get_app_context

        ContextObject = get_ext("context_object_cls")
        ContextObjectType = get_ext("context_object_type_cls")
        ContextSource = get_ext("context_source_cls")
        PersistMode = get_ext("persist_mode_cls")

        app_ctx = get_app_context()
        manifest, _ = _load_manifest_or_none(app_ctx=app_ctx)

        if manifest is None:
            # No manifest yet — create an empty one so we can host the new object.
            ContextManifest = get_ext("context_manifest_cls")
            manifest = ContextManifest([])

        if manifest.get(key) is not None and not overwrite:
            return _validation_err(
                tool_name,
                ctx.call_id,
                started_at,
                f"Context object '{key}' already exists.",
                "Pass overwrite_existing=true, or use context_patch with command='overwrite'.",
            )

        inferred_type: ContextObjectType
        if obj_type_raw:
            try:
                inferred_type = ContextObjectType(obj_type_raw)
            except ValueError:
                return _validation_err(
                    tool_name,
                    ctx.call_id,
                    started_at,
                    f"Invalid type '{obj_type_raw}'.",
                    f"Use one of: {[t.value for t in ContextObjectType]}",
                )
        else:
            if isinstance(content, (dict, list)):
                inferred_type = ContextObjectType.json
            else:
                inferred_type = ContextObjectType.text

        # Access-control fields — newly created objects default to mutable
        # (the model just created them, so it should be allowed to keep
        # editing them for this request).
        mutable = bool(args.get("mutable", True))
        persist_raw = (args.get("persist") or "never").strip()
        try:
            persist_mode = PersistMode(persist_raw)
        except ValueError:
            persist_mode = PersistMode.never

        source_raw = args.get("source")
        source_obj: ContextSource | None = None
        if isinstance(source_raw, dict):
            try:
                source_obj = ContextSource(**source_raw)
            except Exception:
                source_obj = None

        new_obj = ContextObject(
            key=key,
            type=inferred_type,
            label=label,
            description=description,
            content=content,
            mutable=mutable,
            persist=persist_mode,
            source=source_obj,
        )

        manifest.set(new_obj)
        manifest.store_on_ctx(app_ctx)

        await _emit_context_delta(
            ctx,
            obj=new_obj,
            command="create",
            old_content=None,  # nothing existed before → full form
            new_content=content,
        )
        await _emit_context_changed(ctx, obj=new_obj, command="create")
        _schedule_writeback(ctx, new_obj, command="create")

        from matrx_ai.tools.kinds.context_tools import ContextWriteResult

        return _success(
            tool_name,
            ctx.call_id,
            started_at,
            output=ContextWriteResult(
                key=key,
                command="create",
                type=inferred_type.value,
                label=label,
                size_hint=new_obj.size_hint,
                mutable=mutable,
                persist=persist_mode.value,
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"{tool_name} failed: {e}",
                traceback=traceback.format_exc(),
                is_retryable=False,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )


# ---------------------------------------------------------------------------
# Text command implementations
# ---------------------------------------------------------------------------


class _PatchApplyError(Exception):
    def __init__(
        self,
        error_type: str,
        message: str,
        suggestion: str | None = None,
        retryable: bool = False,
    ) -> None:
        self.error_type = error_type
        self.message = message
        self.suggestion = suggestion
        self.retryable = retryable
        super().__init__(message)


def _apply_text_command(command: str, content: str, args: dict[str, Any]) -> tuple[str, str | None]:
    """Return (new_content, matched_at_pass or None)."""
    if command == "str_replace":
        old_str = args.get("old_str", "")
        new_str = args.get("new_str", "")
        if not old_str:
            raise _PatchApplyError(
                "validation",
                "str_replace requires old_str (the verbatim excerpt to find).",
                "Provide a unique excerpt of the current content as old_str.",
            )
        return _fuzzy_replace(content, old_str, new_str)

    if command == "insert":
        insert_line = args.get("insert_line")
        new_str = args.get("new_str", "")
        if insert_line is None:
            raise _PatchApplyError(
                "validation",
                "insert requires insert_line (0-based line number to insert AFTER; "
                "use 0 to insert at the very top).",
                "Pass insert_line=N. The new content is inserted after line N.",
            )
        try:
            line_idx = int(insert_line)
        except (TypeError, ValueError):
            raise _PatchApplyError(
                "validation",
                f"insert_line must be an integer (got {insert_line!r}).",
            ) from None
        lines = content.splitlines(keepends=True)
        if line_idx < 0 or line_idx > len(lines):
            raise _PatchApplyError(
                "validation",
                f"insert_line={line_idx} is out of range (content has {len(lines)} lines).",
                f"Use 0..{len(lines)} inclusive.",
            )
        # Make sure the inserted block ends with a newline so it doesn't glue
        # to the following line.
        payload = new_str if new_str.endswith("\n") else new_str + "\n"
        new_lines = lines[:line_idx] + [payload] + lines[line_idx:]
        return "".join(new_lines), None

    if command == "append":
        new_str = args.get("new_str", "")
        sep = args.get("separator", "\n\n")
        return (content.rstrip() + sep + new_str) if content else new_str, None

    if command == "prepend":
        new_str = args.get("new_str", "")
        sep = args.get("separator", "\n\n")
        return (new_str + sep + content.lstrip()) if content else new_str, None

    if command == "overwrite":
        new_str = args.get("new_str", "")
        return new_str, None

    raise _PatchApplyError("validation", f"Unhandled text command: {command}")


def _fuzzy_replace(content: str, old_str: str, new_str: str) -> tuple[str, str]:
    """Four-pass fuzzy replace using the shared patch_utils helper."""
    from matrx_ai.db.content_types.patch_utils import PatchError, apply_patch

    try:
        result = apply_patch(
            content=content,
            search_text=old_str,
            replacement_text=new_str,
            note_id="<ctx_object>",
        )
    except PatchError as pe:
        raise _PatchApplyError(
            error_type="patch_no_match",
            message=pe.message,
            suggestion=(
                "Call context with action='get' and this key to read the current content, then retry "
                "with a verbatim excerpt from it. The excerpt must be unique enough "
                "to identify a single location."
            ),
            retryable=True,
        ) from pe
    return result.new_content, result.matched_at.value


# ---------------------------------------------------------------------------
# JSON command implementations
# ---------------------------------------------------------------------------


def _apply_json_command(command: str, content: Any, args: dict[str, Any]) -> Any:
    if command == "json_patch":
        operations = args.get("operations")
        if not isinstance(operations, list):
            raise _PatchApplyError(
                "validation",
                "json_patch requires 'operations' as a list of RFC 6902 ops.",
                'Example: [{"op":"replace","path":"/name","value":"Alice"}]',
            )
        return _apply_rfc6902(content, operations)

    if command == "json_merge":
        patch = args.get("patch")
        if not isinstance(patch, dict):
            raise _PatchApplyError(
                "validation",
                "json_merge requires 'patch' as a dict (RFC 7396 merge patch).",
                'Example: {"status":"active","tags":["new"]}. null removes fields.',
            )
        return _apply_rfc7396(content, patch)

    raise _PatchApplyError("validation", f"Unhandled json command: {command}")


def _apply_rfc6902(doc: Any, operations: list[dict[str, Any]]) -> Any:
    """Minimal dependency-free RFC 6902 implementation.

    Supports: add, remove, replace, move, copy, test. No jsonpatch dep so we
    stay lean and this stays portable across deployments.
    """
    doc = _deepcopy_json(doc)
    for i, op in enumerate(operations):
        if not isinstance(op, dict):
            raise _PatchApplyError("validation", f"operations[{i}] is not an object.")
        op_name = op.get("op")
        path = op.get("path")
        if op_name not in {"add", "remove", "replace", "move", "copy", "test"}:
            raise _PatchApplyError("validation", f"Unsupported json_patch op: {op_name!r}")
        if not isinstance(path, str):
            raise _PatchApplyError(
                "validation", f"operations[{i}].path must be a JSON pointer string."
            )

        if op_name == "add":
            doc = _jp_add(doc, path, op.get("value"))
        elif op_name == "remove":
            doc = _jp_remove(doc, path)
        elif op_name == "replace":
            doc = _jp_replace(doc, path, op.get("value"))
        elif op_name == "move":
            frm = op.get("from")
            if not isinstance(frm, str):
                raise _PatchApplyError(
                    "validation", f"operations[{i}] 'move' requires string 'from'."
                )
            value = _jp_get(doc, frm)
            doc = _jp_remove(doc, frm)
            doc = _jp_add(doc, path, value)
        elif op_name == "copy":
            frm = op.get("from")
            if not isinstance(frm, str):
                raise _PatchApplyError(
                    "validation", f"operations[{i}] 'copy' requires string 'from'."
                )
            doc = _jp_add(doc, path, _deepcopy_json(_jp_get(doc, frm)))
        elif op_name == "test":
            actual = _jp_get(doc, path)
            if actual != op.get("value"):
                raise _PatchApplyError(
                    "test_failed",
                    f"json_patch test at {path} failed (expected {op.get('value')!r}, got {actual!r}).",
                    retryable=False,
                )
    return doc


def _apply_rfc7396(target: Any, patch: Any) -> Any:
    """RFC 7396 JSON Merge Patch."""
    if not isinstance(patch, dict):
        return _deepcopy_json(patch)
    if not isinstance(target, dict):
        target = {}
    else:
        target = _deepcopy_json(target)
    for k, v in patch.items():
        if v is None:
            target.pop(k, None)
        else:
            target[k] = _apply_rfc7396(target.get(k), v)
    return target


# --- JSON pointer helpers (RFC 6901) ---------------------------------------


def _jp_split(path: str) -> list[str]:
    if path == "":
        return []
    if not path.startswith("/"):
        raise _PatchApplyError(
            "validation", f"JSON pointer must be empty or start with '/', got {path!r}."
        )
    parts = path.split("/")[1:]
    return [p.replace("~1", "/").replace("~0", "~") for p in parts]


def _jp_get(doc: Any, path: str) -> Any:
    node = doc
    for token in _jp_split(path):
        if isinstance(node, list):
            try:
                node = node[int(token)]
            except (ValueError, IndexError):
                raise _PatchApplyError(
                    "validation", f"Invalid list index at {path}: {token!r}."
                ) from None
        elif isinstance(node, dict):
            if token not in node:
                raise _PatchApplyError("validation", f"Missing key at {path}: {token!r}.")
            node = node[token]
        else:
            raise _PatchApplyError("validation", f"Cannot traverse into scalar at {path}.")
    return node


def _jp_add(doc: Any, path: str, value: Any) -> Any:
    tokens = _jp_split(path)
    if not tokens:
        return _deepcopy_json(value)
    parent = _jp_get(doc, "/" + "/".join(tokens[:-1])) if len(tokens) > 1 else doc
    leaf = tokens[-1]
    if isinstance(parent, list):
        idx = len(parent) if leaf == "-" else int(leaf)
        parent.insert(idx, value)
    elif isinstance(parent, dict):
        parent[leaf] = value
    else:
        raise _PatchApplyError("validation", f"Cannot add to scalar parent at {path}.")
    return doc


def _jp_remove(doc: Any, path: str) -> Any:
    tokens = _jp_split(path)
    if not tokens:
        raise _PatchApplyError("validation", "Cannot remove the root document.")
    parent = _jp_get(doc, "/" + "/".join(tokens[:-1])) if len(tokens) > 1 else doc
    leaf = tokens[-1]
    if isinstance(parent, list):
        try:
            parent.pop(int(leaf))
        except (ValueError, IndexError):
            raise _PatchApplyError(
                "validation", f"Invalid list index at {path}: {leaf!r}."
            ) from None
    elif isinstance(parent, dict):
        if leaf not in parent:
            raise _PatchApplyError("validation", f"Missing key at {path}: {leaf!r}.")
        del parent[leaf]
    else:
        raise _PatchApplyError("validation", f"Cannot remove from scalar parent at {path}.")
    return doc


def _jp_replace(doc: Any, path: str, value: Any) -> Any:
    tokens = _jp_split(path)
    if not tokens:
        return _deepcopy_json(value)
    parent = _jp_get(doc, "/" + "/".join(tokens[:-1])) if len(tokens) > 1 else doc
    leaf = tokens[-1]
    if isinstance(parent, list):
        try:
            parent[int(leaf)] = value
        except (ValueError, IndexError):
            raise _PatchApplyError(
                "validation", f"Invalid list index at {path}: {leaf!r}."
            ) from None
    elif isinstance(parent, dict):
        if leaf not in parent:
            raise _PatchApplyError("validation", f"Missing key at {path}: {leaf!r}.")
        parent[leaf] = value
    else:
        raise _PatchApplyError("validation", f"Cannot replace inside scalar parent at {path}.")
    return doc


def _deepcopy_json(value: Any) -> Any:
    # JSON-safe deep copy via round-trip. Faster than copy.deepcopy and ensures
    # the content is serialization-stable.
    try:
        return json.loads(json.dumps(value))
    except (TypeError, ValueError):
        import copy

        return copy.deepcopy(value)


def _try_parse_json(value: Any) -> Any | None:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return None
    return None


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------


def _load_manifest_or_none(app_ctx: Any | None = None) -> tuple[Any | None, Any]:
    """Return (manifest_or_None, app_ctx). Uses the registered _ext hook."""
    from matrx_ai._ext import get_ext
    from matrx_ai.context.app_context import get_app_context

    if app_ctx is None:
        app_ctx = get_app_context()
    load_manifest_from_ctx = get_ext("load_manifest_from_ctx")
    manifest = load_manifest_from_ctx(app_ctx)
    return manifest, app_ctx


def _write_back(app_ctx: Any, manifest: Any, key: str, new_content: Any) -> Any:
    """Mutate the target ContextObject in the manifest and re-persist.

    Returns the updated ContextObject so callers can read back the refreshed
    access-control / persistence fields without reloading the manifest.
    """
    try:
        replacement = manifest.replace_content(key, new_content)
    except KeyError:
        raise _PatchApplyError("not_found", f"Context object '{key}' vanished mid-patch.") from None
    manifest.store_on_ctx(app_ctx)
    return replacement


# ---------------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------------

# Monotonic sequence for context_delta events. Per-process (shared across
# streams) — clients only need ordering WITHIN one stream, which a globally
# increasing counter satisfies.
_DELTA_SEQ = itertools.count(1)


def _compute_splice(old: str, new: str) -> tuple[int, int, str]:
    """The minimal single-region replacement turning ``old`` into ``new``.

    Returns ``(start, end, text)`` such that
    ``old[:start] + text + old[end:] == new`` — the longest common prefix and
    suffix are excluded, so the shipped text is only the changed region.
    """
    max_p = min(len(old), len(new))
    p = 0
    while p < max_p and old[p] == new[p]:
        p += 1
    s = 0
    max_s = max_p - p
    while s < max_s and old[len(old) - 1 - s] == new[len(new) - 1 - s]:
        s += 1
    return p, len(old) - s, new[p : len(new) - s]


async def _emit_context_delta(
    ctx: ToolContext,
    *,
    obj: Any,
    command: str,
    old_content: str | None,
    new_content: Any,
) -> None:
    """Best-effort stream the applied edit's CONTENT (see ContextDeltaData).

    Emitted immediately when the in-memory patch lands — before the
    fire-and-forget DB writeback — so the client renders the agent's edit
    live instead of re-reading the row after the turn (defect D9).

    ``old_content`` must be the pre-edit STRING content to get the compact
    splice form; pass ``None`` (create / structured JSON content) to ship the
    full post-edit content instead.
    """
    emitter = ctx.emitter
    if emitter is None:
        return

    source_kind = obj.source.kind if obj.source else ""
    source_id = obj.source.id if obj.source else None

    new_str = (
        new_content
        if isinstance(new_content, str)
        else json.dumps(new_content, ensure_ascii=False)
    )

    delta_kind = "full"
    start: int | None = None
    end: int | None = None
    text: str | None = None
    base_len: int | None = None
    content: str | None = new_str
    if old_content is not None:
        s, e, t = _compute_splice(old_content, new_str)
        # Ship the splice only when it is actually smaller than the content
        # (an `overwrite` of everything gains nothing from splice form).
        if len(t) < len(new_str):
            delta_kind = "splice"
            start, end, text = s, e, t
            base_len = len(old_content)
            content = None

    try:
        try:
            from matrx_connect.context.data_types import ContextDeltaData

            payload: Any = ContextDeltaData(
                key=obj.key,
                command=command,
                object_type=obj.type.value,
                source_kind=source_kind,
                source_id=source_id,
                seq=next(_DELTA_SEQ),
                delta_kind=delta_kind,
                start=start,
                end=end,
                text=text,
                base_len=base_len,
                new_len=len(new_str),
                content=content,
            )
        except Exception:
            payload = {
                "type": "context_delta",
                "key": obj.key,
                "command": command,
                "object_type": obj.type.value,
                "source_kind": source_kind,
                "source_id": source_id,
                "seq": next(_DELTA_SEQ),
                "delta_kind": delta_kind,
                "start": start,
                "end": end,
                "text": text,
                "base_len": base_len,
                "new_len": len(new_str),
                "content": content,
            }
        await emitter.send_data(payload)
    except Exception:
        # Streaming is best-effort; never fail the tool on an emitter hiccup.
        pass


async def _emit_context_changed(
    ctx: ToolContext,
    *,
    obj: Any,
    command: str,
) -> None:
    """Best-effort notify the client that a context object mutated.

    We use send_data (not send_tool_event) because this is a domain event the
    frontend may want to consume independently of the tool-call UI (e.g. to
    re-render a document or schedule a persist-back).
    """
    emitter = ctx.emitter
    if emitter is None:
        return

    source_kind = obj.source.kind if obj.source else ""
    source_id = obj.source.id if obj.source else None

    try:
        try:
            from matrx_connect.context.data_types import ContextChangedData

            payload: Any = ContextChangedData(
                key=obj.key,
                command=command,
                object_type=obj.type.value,
                mutable=bool(obj.mutable),
                persist=obj.persist.value,
                source_kind=source_kind,
                source_id=source_id,
            )
        except Exception:
            payload = {
                "type": "context_changed",
                "key": obj.key,
                "command": command,
                "object_type": obj.type.value,
                "mutable": bool(obj.mutable),
                "persist": obj.persist.value,
                "source_kind": source_kind,
                "source_id": source_id,
            }
        await emitter.send_data(payload)
    except Exception:
        # Streaming is best-effort; never fail the tool on an emitter hiccup.
        pass


def _schedule_writeback(ctx: ToolContext, obj: Any, *, command: str) -> None:
    """Fire-and-forget DB writeback via a host-injected dispatcher.

    The host supplies a `schedule_context_writeback` callable via
    `matrx_ai.configure(...)`. If it isn't configured (standalone use, or a
    host that doesn't care about persisting context edits), this is a no-op.

    Safe to call for any mutation: the dispatcher itself no-ops when persist
    is disabled, when no source is set, or when no handler is registered.
    """
    from matrx_ai._ext import get_ext, has_ext

    if not has_ext("schedule_context_writeback"):
        return
    try:
        schedule_writeback = get_ext("schedule_context_writeback")
        schedule_writeback(
            obj,
            user_id=ctx.user_id or "",
            emitter=ctx.emitter,
            command=command,
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def _success(tool_name: str, call_id: str, started_at: float, output: Any) -> ToolResult:
    return ToolResult(
        success=True,
        output=output,
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


def _validation_err(
    tool_name: str,
    call_id: str,
    started_at: float,
    message: str,
    suggestion: str | None,
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="validation",
            message=message,
            suggested_action=suggestion,
            is_retryable=False,
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


def _not_found(
    tool_name: str,
    call_id: str,
    started_at: float,
    message: str,
    suggestion: str | None,
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="not_found",
            message=message,
            suggested_action=suggestion,
            is_retryable=False,
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )
