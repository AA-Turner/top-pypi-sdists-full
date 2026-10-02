"""Spend browse's response budget without advancing past undisclosed rows.

The backend owns every position. Delivery is depth first: a parent, its expanded
children, then its siblings. One pending parent is enough at the supported depth
of two; side lists are visited in order, not stored as a frontier in the cursor.
One source page is fetched per invocation, and already-fetched children are used
without per-parent requests. Mutable counts and heartbeats are never hashed.
"""

from __future__ import annotations

import base64
from collections.abc import Callable
from typing import Any
from uuid import UUID

_FIELDS = (
    "entity_type",
    "uuid",
    "name",
    "slug",
    "url",
    "kind",
    "description",
    "description_truncated",
    "workspace_id",
    "workspace_name",
    "parent_project_id",
    "experiment_count",
    "run_count",
    "active_run_count",
    "direct_run_count",
    "subproject_count",
    "contributor_count",
    "code_source_count",
    "repo",
    "status",
    "alive",
)
_EXCERPTS = {"name": 120, "description": 180, "workspace_name": 80, "repo": 120}
_CURSOR_PARAMETERS = {
    "projects": "cursor",
    "experiments": "cursor",
    "runs": "runs_cursor",
    "subprojects": "subprojects_cursor",
}


def _pack_state(state: dict) -> dict:
    """Compress opaque bytes once, avoiding base64 inside base64.

    Latin-1 is a reversible bytes-to-string mapping for the shared JSON cursor
    codec. No backend claims or positions are interpreted or reconstructed.
    Keeping two signed positions affordable matters at the 512-token minimum.
    """
    packed = dict(state)
    for source, target in (("native", "n"), ("root", "r")):
        token = packed.pop(source, None)
        if token is not None:
            raw = token.removeprefix("browse1.")
            packed[target] = base64.b64decode(
                raw + "=" * (-len(raw) % 4), altchars=b"-_", validate=True
            ).decode("latin-1")
    for source, target in (
        ("browse", "b"),
        ("phase", "i"),
        ("parent", "p"),
        ("root_more", "m"),
        ("streams", "l"),
    ):
        if source in packed:
            packed[target] = packed.pop(source)
    return packed


def _unpack_state(state: dict) -> dict:
    unpacked = dict(state)
    for source, target in (("n", "native"), ("r", "root")):
        if source in unpacked:
            raw = unpacked.pop(source).encode("latin-1")
            unpacked[target] = "browse1." + base64.urlsafe_b64encode(raw).decode().rstrip("=")
    for source, target in (
        ("b", "browse"),
        ("i", "phase"),
        ("p", "parent"),
        ("m", "root_more"),
        ("l", "streams"),
    ):
        if source in unpacked:
            unpacked[target] = unpacked.pop(source)
    return unpacked


def _compact(row: dict) -> dict:
    result = {key: row[key] for key in _FIELDS if row.get(key) is not None}
    trimmed = []
    for key, maximum in _EXCERPTS.items():
        value = result.get(key)
        if isinstance(value, str) and len(value) > maximum:
            result[key] = value[:maximum]
            trimmed.append(key)
            if key == "description":
                result["description_truncated"] = True
    # Never present a shortened address as an address. The stable UUID remains
    # usable through entity(view="record") for every omitted field.
    for key, maximum in (("slug", 160), ("url", 512)):
        if isinstance(result.get(key), str) and len(result[key]) > maximum:
            result.pop(key)
            trimmed.append(key)
    if trimmed:
        result["truncated_fields"] = trimmed
    return result


def _smaller(row: dict):
    """Finite fallbacks for an unusually expensive identity at the minimum cap."""
    candidate = dict(row)
    trimmed = list(candidate.get("truncated_fields", []))
    for key in (
        "description",
        "url",
        "slug",
        "workspace_name",
        "workspace_id",
        "repo",
        "parent_project_id",
        "contributor_count",
        "code_source_count",
    ):
        if key in candidate:
            candidate.pop(key)
            trimmed.append(key)
            candidate["truncated_fields"] = list(dict.fromkeys(trimmed))
            yield dict(candidate)
    if isinstance(candidate.get("name"), str) and len(candidate["name"]) > 40:
        candidate["name"] = candidate["name"][:40]
        candidate["truncated_fields"] = list(dict.fromkeys(trimmed + ["name"]))
        yield dict(candidate)
    # Full values stay addressable using uuid + entity(view="record"). At the
    # minimum cap a signed nested cursor can leave room only for the identity.
    minimal = {
        key: row[key] for key in ("entity_type", "uuid", "experiments", "runs") if key in row
    }
    if isinstance(row.get("name"), str):
        minimal["name"] = row["name"][:8]
        minimal["truncated_fields"] = ["name"] if len(row["name"]) > 8 else []
    yield minimal
    yield {key: row[key] for key in ("uuid", "experiments", "runs") if key in row}


def invoke(arguments: dict, call: Callable[[dict], dict], scope: str) -> dict:
    # Import lazily: ordinary SDK imports must not initialize tokenizer assets.
    from .budget import Budget
    from .continuation import ContinuationError, binding, decode, omit_defaults
    from .continuation import encode as encode_cursor

    def fail():
        raise ContinuationError(
            "Invalid browse continuation; repeat the original browse without cursor."
        )

    budget = Budget(arguments.get("token_budget", 2000))
    request_id = binding("browse", arguments, scope)
    decoded = decode(arguments.get("cursor"), request_id)
    try:
        state = _unpack_state(decoded)
    except (ValueError, TypeError, AttributeError):
        fail()

    def encode(state: dict, request: str) -> str:
        if stream_mask is not None:
            state = {**state, "streams": stream_mask}
        return encode_cursor(_pack_state(state), request)

    stream_mask = None
    root_ref = arguments.get("ref")
    if root_ref is None:
        phases = ["projects"]
    elif isinstance(root_ref, str) and root_ref.startswith("project:"):
        phases = ["experiments", "runs", "subprojects"]
        stream_mask = state.get("streams")
        if stream_mask is None:
            # Remember the original selection, since `cursor` becomes our
            # delivery token and is no longer an initial primary-list cursor.
            stream_mask = (
                sum(
                    1 << i
                    for i, name in enumerate(phases)
                    if arguments.get(_CURSOR_PARAMETERS[name])
                )
                or 7
            )
        if type(stream_mask) is not int or not 1 <= stream_mask <= 7:
            fail()
        phases = [name for i, name in enumerate(phases) if stream_mask & (1 << i)]
    elif isinstance(root_ref, str) and root_ref.startswith("experiment:"):
        phases = ["runs"]
    else:
        # Preserve the source's normal scope validation/error behavior.
        return call(arguments)
    phase = state.get("phase", 0)
    if type(phase) is not int or not 0 <= phase < len(phases):
        fail()
    level = phases[phase]
    parent = state.get("parent")
    if parent is not None:
        try:
            UUID(parent)
        except (ValueError, TypeError, AttributeError):
            fail()
        if level not in ("projects", "subprojects", "experiments"):
            fail()
        if type(state.get("root_more")) is not bool:
            fail()
        if state["root_more"] and not isinstance(state.get("root"), str):
            fail()
    native = state.get("native")
    if native is not None and (not isinstance(native, str) or not native.startswith("browse1.")):
        raise ContinuationError(
            "Legacy browse cursor cannot be safely translated; restart without cursor."
        )
    child_level = "experiments" if level in ("projects", "subprojects") else "runs"
    target_level = child_level if parent is not None else level
    target_ref = (
        f"{'project' if child_level == 'experiments' else 'experiment'}:{parent}"
        if parent is not None
        else root_ref
    )
    parameter = (
        "cursor"
        if parent is not None or not (root_ref or "").startswith("project:")
        else _CURSOR_PARAMETERS[level]
    )
    if native is None and ("browse" not in state or (parent is None and parameter != "cursor")):
        native = arguments.get(parameter)
        if native is not None and not str(native).startswith("browse1."):
            raise ContinuationError(
                "Legacy browse cursor cannot be safely translated; restart without cursor."
            )
    fetch_args = {
        **arguments,
        "ref": target_ref,
        "cursor": None,
        "runs_cursor": None,
        "subprojects_cursor": None,
        parameter: native,
        "depth": 1 if parent is not None else arguments.get("depth", 1),
        "limit": min(arguments.get("limit") or 10, 25),
    }
    if parent is not None:
        fetch_args["workspace_id"] = None
    payload = call(fetch_args)
    handles = payload.get("_browse_handles")
    if not isinstance(handles, list):
        raise ContinuationError(
            "Backend browse continuation support is unavailable; reconnect after the backend update."
        )
    descriptors = {tuple(item.get("path", [])): item for item in handles if isinstance(item, dict)}
    data = payload.get("data", {})
    rows = data.get(target_level)
    descriptor = descriptors.get((target_level,))
    if not isinstance(rows, list) or not isinstance(descriptor, dict):
        fail()

    # Runs filed nowhere yet (daemon v2) ride the lab root's FIRST page only,
    # outside the traversal: they are no level of the tree and have no cursor.
    unfiled_rows = (
        [
            {
                **_compact(row),
                **{key: row[key] for key in ("created_at", "tags") if row.get(key)},
            }
            for row in data.get("unfiled") or []
            if isinstance(row, dict)
        ]
        if root_ref is None and parent is None and "browse" not in state
        else []
    )

    # A fixed cost on the first page, decided ONCE: carried if it fits beside
    # the first row, else dropped for the whole page with a marker. Deciding per
    # candidate would let the rows squeeze it out one by one.
    unfiled_state = {"dropped": False}

    def positions(desc: dict, values: list):
        after = desc.get("after")
        if not isinstance(after, list) or len(after) != len(values):
            fail()
        for value in [desc.get("start"), *after]:
            if not isinstance(value, str) or not value.startswith("browse1."):
                fail()
        if desc.get("next_cursor") is not None and not isinstance(desc["next_cursor"], str):
            fail()
        return after

    after = positions(descriptor, rows)

    def phase_after() -> dict | None:
        return {"browse": 1, "phase": phase + 1} if phase + 1 < len(phases) else None

    def root_after(index: int) -> dict | None:
        if index + 1 < len(rows) or descriptor.get("next_cursor"):
            return {"browse": 1, "phase": phase, "native": after[index]}
        return phase_after()

    def child_done() -> dict | None:
        if state["root_more"]:
            return {"browse": 1, "phase": phase, "native": state["root"]}
        return phase_after()

    def follow(index: int) -> dict | None:
        if parent is None:
            return root_after(index)
        if index + 1 < len(rows) or descriptor.get("next_cursor"):
            return {**state, "native": after[index]}
        return child_done()

    def pending(index: int, row_id: str, position: str) -> dict:
        more = bool(index + 1 < len(rows) or descriptor.get("next_cursor"))
        return {
            "browse": 1,
            "phase": phase,
            "native": position,
            "parent": row_id,
            **({"root": after[index]} if more else {}),
            "root_more": more,
        }

    def result(values: list, continuation: dict | None) -> dict:
        output_data: dict[str, Any] = {
            "scope": target_ref,
            "depth": fetch_args["depth"],
            target_level: values,
        }
        carried = unfiled_rows if not unfiled_state["dropped"] else []
        if carried:
            output_data["unfiled"] = carried
        available = data.get("available_views")
        if isinstance(available, dict):
            kinds = {row.get("entity_type") for row in [*values, *carried]}
            for row in values:
                for field in ("experiments", "runs"):
                    kinds.update(child.get("entity_type") for child in row.get(field) or [])
            output_data["available_views"] = {
                kind: available[kind] for kind in kinds if kind in available
            }
        # Backend's bounded-list truncation is now represented by reachable
        # delivery cursors. Preserve every unrelated source limitation.
        source = payload.get("completeness") or {}
        missing = [
            item for item in source.get("missing", []) if item != "truncated_by_token_budget"
        ]
        if continuation is not None:
            missing.append("truncated_by_token_budget")
        if unfiled_state["dropped"]:
            # Said to be missing, never silently absent (absent means "none").
            missing.append("unfiled_runs")
        output = omit_defaults(
            {
                "data": output_data,
                "completeness": {
                    "state": "partial" if missing else "complete",
                    "missing": missing,
                },
                "next_cursor": (
                    encode(continuation, request_id) if continuation is not None else None
                ),
            }
        )
        if not budget.fits(output):
            output["data"].pop("available_views", None)
        return output

    if unfiled_rows:
        opening = [_compact(rows[0])] if rows else []
        if not budget.fits(result(opening, None)):
            unfiled_state["dropped"] = True

    # Keep the ordinary small-tree response (including all project side lists)
    # in one call. A partially fetched tree takes the ordered traversal below;
    # no array of pending handles is ever put into the delivery cursor.
    if (
        parent is None
        and "browse" not in state
        and all(isinstance(data.get(name), list) for name in phases)
        and not any(item.get("next_cursor") for item in handles)
    ):

        def tree_row(raw: dict) -> dict:
            row = _compact(raw)
            for child in ("experiments", "runs"):
                if child in raw:
                    row[child] = (
                        [tree_row(value) for value in raw[child]]
                        if isinstance(raw[child], list)
                        else None
                    )
            return row

        whole = result([], None)
        kept_unfiled = whole["data"].get("unfiled")
        whole["data"] = {
            "scope": target_ref,
            "depth": fetch_args["depth"],
            **{
                name: [tree_row(row) for row in data[name]]
                if isinstance(data.get(name), list)
                else None
                for name in ("projects", "experiments", "runs", "subprojects")
            },
        }
        if kept_unfiled:
            whole["data"]["unfiled"] = kept_unfiled
        if data.get("available_views"):
            whole["data"]["available_views"] = data["available_views"]
        if budget.fits(whole):
            return whole

    if not rows:
        return result([], child_done() if parent is not None else phase_after())
    emitted: list[dict] = []
    last = None
    for index, raw in enumerate(rows):
        row = _compact(raw)
        next_state = follow(index)
        nested = raw.get(child_level) if parent is None else None
        row_id = str(raw.get("uuid", "")).partition(":")[2]
        child_descriptor = (
            descriptors.get((level, row_id, child_level)) if isinstance(nested, list) else None
        )
        if isinstance(nested, list) and child_descriptor is None:
            fail()
        if child_descriptor is not None:
            child_after = positions(child_descriptor, nested)
            child_more = child_descriptor.get("next_cursor")
            row[child_level] = [_compact(child) for child in nested]
            if child_more:
                next_state = pending(index, row_id, child_more)
        elif child_level in raw and parent is None:
            row[child_level] = None
        candidate = result(emitted + [row], next_state)
        full_next_state = next_state
        if budget.fits(candidate):
            emitted.append(row)
            last = candidate
            if child_descriptor is not None and child_descriptor.get("next_cursor"):
                return candidate
            continue
        # Spend remaining room on this parent's already-fetched child prefix.
        if child_descriptor is not None and nested:
            base = {**row, child_level: None}
            next_state = pending(index, row_id, child_descriptor["start"])
            head = result(emitted + [base], next_state)
            if not budget.fits(head) and not emitted:
                for smaller in _smaller(base):
                    head = result([smaller], next_state)
                    if budget.fits(head):
                        base = smaller
                        break
            if budget.fits(head):
                selected = head
                children = []
                for child_index, child in enumerate(nested):
                    end = child_index + 1 == len(nested)
                    next_state = (
                        root_after(index)
                        if end and not child_descriptor.get("next_cursor")
                        else pending(index, row_id, child_after[child_index])
                    )
                    trial = result(
                        emitted + [{**base, child_level: children + [_compact(child)]}], next_state
                    )
                    if not budget.fits(trial):
                        break
                    children.append(_compact(child))
                    selected = trial
                return selected
        if emitted:
            return last
        for smaller in _smaller(row):
            candidate = result([smaller], full_next_state)
            if budget.fits(candidate):
                return candidate
        raise ContinuationError("Browse identity exceeds this budget; use a larger token_budget.")
    return last
