"""Dataset and source refs, and the checks a ref, share or name must pass before it is sent."""

from __future__ import annotations
import math
import re
import threading
from dataclasses import dataclass, field
from typing import Any, Mapping
#: `share` values must sum to 1 within this (C10, V12).
SHARE_TOLERANCE = 0.01
#: Dataset names (C3, Q8): no `@`, `/` or uuid shape, so the ref grammar holds.
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


class CatalogRefused(Exception):
    """A catalog call that cannot go ahead, with the sentence that says why.
    The CLI prints it; the SDK verbs warn it."""


@dataclass(eq=False)  # hashable by identity: a ref is a `{ref: share}` key
class SourceRef:
    """What `probe.source(...)` registered: ``ref`` is ``source:<id>``, or None
    when it could not be registered (the warning said why)."""

    ref: str | None = None
    id: str | None = None
    uri: str | None = None
    canonical_key: str | None = None
    provider: str | None = None
    kind: str | None = None
    revision: str | None = None
    created: bool | None = None

    def __str__(self) -> str:
        return self.ref or ""

    @classmethod
    def from_row(cls, row: Mapping[str, Any], *, uri: str | None = None) -> "SourceRef":
        source_id = row.get("id")
        ref = row.get("ref") or (f"source:{source_id}" if source_id else None)
        return cls(
            ref=ref,
            id=str(source_id) if source_id else None,
            uri=uri,
            canonical_key=row.get("canonical_key"),
            provider=row.get("provider"),
            kind=row.get("kind"),
            revision=row.get("revision"),
            created=row.get("created"),
        )


@dataclass(eq=False)  # hashable by identity: a ref is a `{ref: share}` key
class DatasetRef:
    """What `log_dataset` recorded. ``ref`` is ``dataset:<name>@<n>`` once
    registered (``artifact:<id>`` with ``register=False``). ``pending``: the
    registration had not answered within the wait; the fields fill in when it
    does (``wait()``), and stay empty if it was queued in the outbox."""

    ref: str | None = None
    name: str | None = None
    version_id: str | None = None
    content_hash: str | None = None
    identity: str | None = None
    pending: bool = False
    created_version: bool | None = None
    recorded_step: bool | None = None
    #: The run's own file row (the dataset file the version pins), when known.
    artifact_id: str | None = None
    _done: threading.Event = field(default_factory=threading.Event, repr=False, compare=False)

    def __str__(self) -> str:
        return self.ref or ""

    def wait(self, timeout: float | None = None) -> bool:
        """Block until a pending registration has answered (or was queued).
        True when it is settled."""
        return self._done.wait(timeout)

    def _fill(self, answer: Mapping[str, Any]) -> None:
        version = answer.get("version") if isinstance(answer.get("version"), dict) else {}
        entry = answer.get("entry") if isinstance(answer.get("entry"), dict) else {}
        self.ref = version.get("ref") or entry.get("ref") or self.ref
        self.version_id = version.get("id") or self.version_id
        self.content_hash = version.get("content_hash") or self.content_hash
        self.identity = version.get("identity") or self.identity
        self.created_version = answer.get("created_version")
        self.recorded_step = answer.get("recorded_step")
        self.pending = False


def ref_of(value: Any) -> str | None:
    """The ref string of a `str`, `SourceRef` or `DatasetRef` (None when it has none)."""
    if isinstance(value, (SourceRef, DatasetRef)):
        return value.ref or None
    if isinstance(value, str):
        return value.strip() or None
    return None


#: `@latest` after a dataset name or id.
_DATASET_LATEST = "latest"
#: `@step<N>` after a checkpoint's run: one save.
_CHECKPOINT_STEP = re.compile(r"^step[0-9]+$")
#: `@latest`, `@best` and `@best:<callback>` after a checkpoint's run.
_CHECKPOINT_MOVING = ("latest", "best")


def is_moving_ref(ref: Any) -> bool:
    """Whether `ref` names whatever is newest when the use is RECORDED, not one version:
    a dataset with no version or `@latest`, a checkpoint `@latest`/`@best[:<callback>]`,
    a source key with no `@<revision>`. The server resolves a ref when it arrives, so a
    later link (agent, or replayed from the outbox) could name a newer version than the
    run used (D16, D17). Unreadable forms are left to the server to refuse."""
    raw = ref_of(ref) or ""
    kind, sep, body = raw.partition(":")
    kind, body = kind.strip().lower(), body.strip()
    if not sep or not body:
        return False
    _, at, selector = body.rpartition("@")
    selector = selector.strip().lower()
    if kind == "dataset":
        return not at or selector == _DATASET_LATEST
    if kind == "checkpoint":
        if not at or _CHECKPOINT_STEP.fullmatch(selector):
            return False
        return selector.partition(":")[0] in _CHECKPOINT_MOVING
    if kind == "source":
        return not at and not _UUID.fullmatch(body)
    return False


def moving_ref_refusal(ref: str) -> str:
    """Why the CLI will not record `ref`, and the command listing fixed refs to use."""
    kind, _, body = ref.partition(":")
    kind = kind.strip().lower()
    head = body.rpartition("@")[0] or body
    if kind == "checkpoint":
        run = head or "RUN"
        return (
            f"{ref} names whichever save is newest or best when the link is made, not the one the run used. "
            f"Name the save: checkpoint:{run}@step<N> or checkpoint:<id> (`probe checkpoint list --run {run}` "
            "lists them)."
        )
    if kind == "source":
        return (
            f"{ref} names whichever revision is newest when the link is made, not the one the run used. "
            f"Name the revision: source:{body}@<revision> or source:<id> (`probe source list` lists them)."
        )
    name = head or "NAME"
    return (
        f"{ref} names whichever version is newest when the link is made, not the one the run used. "
        f"Name the version: dataset:{name}@<N> (`probe dataset show dataset:{name}` lists them)."
    )


def check_share(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CatalogRefused(f"a share must be a number between 0 and 1, not {value!r}")
    share = float(value)
    if not math.isfinite(share) or share <= 0 or share > 1:
        raise CatalogRefused(f"a share must be more than 0 and at most 1, not {value!r}")
    return share


def mixture_parts(parts: Mapping[Any, Any]) -> list[dict]:
    """`{ref: share}` as the wire's `[{target, share}]`, checked the way the
    server checks it (finite, > 0, summing to 1 within `SHARE_TOLERANCE`)."""
    if not isinstance(parts, Mapping) or not parts:
        raise CatalogRefused("a mixture needs at least one {dataset ref: share}")
    out = []
    for target, share in parts.items():
        ref = ref_of(target)
        if not ref:
            raise CatalogRefused(f"{target!r} has no ref (was it registered?)")
        out.append({"target": ref, "share": check_share(share)})
    total = sum(p["share"] for p in out)
    if abs(total - 1.0) > SHARE_TOLERANCE:
        raise CatalogRefused(f"a mixture's shares must sum to 1 (+-{SHARE_TOLERANCE}); these sum to {total:g}")
    return out


def composition_parts(composition: Mapping[Any, Any]) -> list[dict]:
    """`log_dataset(composition=...)` (C10) as the wire's `[{target, rows?, share}]`.
    A target is a dataset version or a source (`probe.source(...)`'s ref).

    Row counts (ints) give shares computed from them; shares (floats summing to
    1 within `SHARE_TOLERANCE`) are sent as given. Never both kinds at once."""
    if not isinstance(composition, Mapping) or not composition:
        raise CatalogRefused("a composition needs at least one {dataset or source ref: rows or share}")
    refs = []
    for target in composition:
        ref = ref_of(target)
        if not ref:
            raise CatalogRefused(f"{target!r} has no ref (was it registered?)")
        refs.append(ref)
    values = list(composition.values())
    if all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        if any(v <= 0 for v in values):
            raise CatalogRefused("a composition's row counts must be more than 0")
        total = sum(values)
        return [{"target": ref, "rows": int(v), "share": v / total} for ref, v in zip(refs, values)]
    shares = [check_share(v) for v in values]
    total = sum(shares)
    if abs(total - 1.0) > SHARE_TOLERANCE:
        raise CatalogRefused(
            f"a composition's shares must sum to 1 (+-{SHARE_TOLERANCE}); these sum to {total:g}. "
            "Pass row counts (ints) to have the shares computed"
        )
    return [{"target": ref, "share": share} for ref, share in zip(refs, shares)]


def check_name(name: Any) -> str:
    """A dataset name the server takes (C3, Q8), or `CatalogRefused`."""
    if not isinstance(name, str) or not NAME_PATTERN.match(name) or _UUID.match(name):
        raise CatalogRefused(
            f"{name!r} is not a dataset name: lower-case letters, digits, `.`, `_` and `-`, "
            "starting with a letter or digit, at most 128 characters (no `@`, `/` or id)"
        )
    return name
