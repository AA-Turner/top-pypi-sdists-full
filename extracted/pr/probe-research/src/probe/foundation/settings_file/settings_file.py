"""settings.json: what each Probe setting should be, who chose it, and what was applied (plan app-never-waits).

Writers publish a value under settings.lock; one applier per revision claims it, makes it true and finishes it.
Stdlib only: the Probe service loads it at start, before an update can replace the CLI's files. Shape: DESIGN.md.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from probe.foundation.durable.durable import file_lock, write_text_atomic
from probe.foundation.service_api import procid
from probe.foundation.version_policy.version_policy import config_path
from probe.generated.settings_vocabulary import SetBy, SettingKey

FILE_NAME = "settings.json"
LOCK_NAME = "settings.lock"
SCHEMA_VERSION = 1
#: A claim whose owner's start time this platform cannot read counts as abandoned after this long (s).
UNREADABLE_CLAIM_LIMIT_S = 3600
#: An unreadable settings.json is moved to `settings.json.unreadable` by the next write.
UNREADABLE_SUFFIX = ".unreadable"


class SettingsUnreadable(ValueError):
    """settings.json exists but is not a settings file this version reads: readers fall back to live homes."""


class SettingsTooNew(SettingsUnreadable):
    """settings.json is a newer Probe's (a higher `version`): never set aside or rewritten by this one."""


@dataclass(frozen=True)
class Claim:
    """An applier working on `revision`: the process (pid + kernel start time) and since when."""

    revision: int
    pid: int
    start: str
    since: str


@dataclass(frozen=True)
class Applied:
    """The newest revision an applier made true, and the value it applied."""

    revision: int
    value: Any
    at: str


@dataclass(frozen=True)
class ApplyError:
    """Why applying `revision` failed. A retryable error is retried; a terminal one waits for a new choice."""

    revision: int
    code: str
    message: str
    is_retryable: bool


@dataclass(frozen=True)
class LogEntry:
    """One published transcripts value, kept until applied so a quick on-off-on still seals its off stretch."""

    revision: int
    value: Any
    by: str
    at: str


@dataclass
class Setting:
    """One setting's record: the newest choice and the applier's bookkeeping."""

    key: SettingKey
    revision: int = 0
    value: Any = None
    by: str | None = None
    at: str | None = None
    context: str | None = None
    account_id: str | None = None
    log: list[LogEntry] = field(default_factory=list)
    claim: Claim | None = None
    applied: Applied | None = None
    error: ApplyError | None = None

    @property
    def is_pending(self) -> bool:
        """Published but not yet applied at its newest revision."""
        return self.revision > 0 and (self.applied is None or self.applied.revision < self.revision)

    @property
    def unapplied_log(self) -> list[LogEntry]:
        """Transcripts entries newer than what was applied, oldest first."""
        done = self.applied.revision if self.applied else 0
        return [entry for entry in self.log if entry.revision > done]


@dataclass
class SettingsDoc:
    """The whole file."""

    settings: dict[SettingKey, Setting] = field(default_factory=dict)
    version: int = SCHEMA_VERSION
    #: Settings a newer writer added, kept as they are: an older writer never drops them.
    unknown: dict[str, Any] = field(default_factory=dict)

    def get(self, key: SettingKey) -> Setting:
        return self.settings.get(key) or Setting(key=key)


def get_default_folder() -> Path:
    """Probe's config folder: settings.json sits beside config.json (`PROBE_CONFIG_PATH`, XDG, ~/.config)."""
    return Path(config_path()).parent


def get_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def to_text(doc: SettingsDoc) -> str:
    """The canonical bytes both languages write: sorted keys, two-space indent, UTF-8, one trailing newline."""
    return json.dumps(_build_wire(doc), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def parse_text(text: str) -> SettingsDoc:
    """Parse settings.json; raises SettingsUnreadable for anything this version cannot read."""
    try:
        raw = json.loads(text)
    except ValueError as exc:
        raise SettingsUnreadable(f"settings.json is not JSON: {exc}") from None
    version = raw.get("version") if isinstance(raw, dict) else None
    if isinstance(version, int) and version > SCHEMA_VERSION:
        raise SettingsTooNew(f"settings.json is version {version}, newer than this Probe reads; update Probe")
    if not isinstance(raw, dict) or version != SCHEMA_VERSION or not isinstance(raw.get("settings"), dict):
        raise SettingsUnreadable("settings.json is not a version 1 settings file")
    doc = SettingsDoc()
    for name, record in raw["settings"].items():
        try:
            key = SettingKey(name)
            doc.settings[key] = _parse_record(key, record)
        except (ValueError, SettingsUnreadable):
            # A newer writer's setting, or one record this version cannot read: written back untouched (a
            # publish of that setting replaces it), never a reason to set the whole file aside.
            doc.unknown[name] = record
    return doc


class SettingsFile:
    """settings.json and its lock, in one folder. Every change is a read-modify-write under settings.lock."""

    def __init__(self, folder: Path | None = None) -> None:
        self.folder = Path(folder) if folder is not None else get_default_folder()
        self.path = self.folder / FILE_NAME
        self.lock_path = self.folder / LOCK_NAME

    def load(self) -> SettingsDoc:
        """The file as it is now (no lock): an absent file is an empty document."""
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return SettingsDoc()
        except UnicodeDecodeError as exc:
            raise SettingsUnreadable(f"settings.json is not text: {exc}") from None  # set aside, as the app does
        return parse_text(text)

    def publish(self, key: SettingKey, value: Any, *, by: SetBy, context: str | None = None,
                account_id: str | None = None, then: Callable[[Setting], None] | None = None,
                is_claimed: bool = False, is_merged: bool = False) -> Setting:
        """A new choice: the next revision, its value, who and when. `then` runs inside the same locked
        step after the file is written (transcripts off drops its markers there). `is_claimed`: this process
        applies it itself, claimed in the same step, so no keeper takes it meanwhile. `is_merged`: a per-agent value
        names only the agents it changes, merged into the newest value under the lock. Returns the record."""
        with self._hold_document() as doc:
            record = doc.get(key)
            record.revision += 1
            record.value = {**(record.value or {}), **value} if is_merged and isinstance(value, dict) else value
            record.by = SetBy(by).value
            record.at = get_now_iso()
            if key is SettingKey.WORKSPACE:
                record.context, record.account_id = context, account_id
            if key is SettingKey.TRANSCRIPTS:
                record.log.append(LogEntry(record.revision, value, record.by, record.at))
            if record.error is not None and record.error.revision < record.revision:
                record.error = None  # a new choice replaces the old one's failure
            if is_claimed:
                pid = os.getpid()
                record.claim = Claim(record.revision, pid, procid.start_time(pid) or "", record.at)
            doc.settings[key] = record
            self._write(doc)
            if then is not None:
                then(record)
            return record

    def claim(self, key: SettingKey, *, pid: int | None = None, start: str | None = None) -> Setting | None:
        """Take the newest unapplied revision to apply, unless another live applier holds it (this process
        may take its own claim again). Returns the record with the claim set, or None (nothing pending, or
        claimed by another live process)."""
        pid = os.getpid() if pid is None else pid
        start = start or procid.start_time(pid) or ""
        with self._hold_document() as doc:
            record = doc.get(key)
            if not record.is_pending:
                return None
            held = record.claim
            is_mine = held is not None and (held.pid, held.start) == (pid, start)
            if held is not None and not is_mine and held.revision >= record.revision and self._is_live(held):
                return None
            record.claim = Claim(record.revision, pid, start, get_now_iso())
            doc.settings[key] = record
            self._write(doc)
            return record

    def finish(self, key: SettingKey, claim: Claim, *, applied_value: Any = None, error: ApplyError | None = None,
               applied_revision: int | None = None) -> bool:
        """End `claim`: record what was applied (a revision older than the newest still counts as progress) or
        the error (only for the newest revision: an older one's failure is moot). Returns whether the claimed
        revision is still the newest, i.e. False means a newer choice needs claiming."""
        with self._hold_document() as doc:
            record = doc.get(key)
            if record.claim is not None and (record.claim.pid, record.claim.start) == (claim.pid, claim.start):
                record.claim = None
            done = applied_revision if applied_revision is not None else claim.revision
            if error is None and (record.applied is None or record.applied.revision < done):
                record.applied = Applied(done, applied_value, get_now_iso())
                record.log = [entry for entry in record.log if entry.revision > done]
                if record.error is not None and record.error.revision <= done:
                    record.error = None
            if error is not None and error.revision == record.revision:
                record.error = error
            doc.settings[key] = record
            self._write(doc)
            return claim.revision == record.revision

    def release(self, key: SettingKey, claim: Claim) -> None:
        """Give `claim` back without a result: the choice stays pending for the next applier (the keeper)."""
        with self._hold_document() as doc:
            record = doc.get(key)
            if record.claim is not None and (record.claim.pid, record.claim.start) == (claim.pid, claim.start):
                record.claim = None
                doc.settings[key] = record
                self._write(doc)

    def adopt(self, key: SettingKey, value: Any) -> Setting:
        """A live home an older Probe copy changed directly: its value becomes the newest choice, already applied."""
        with self._hold_document() as doc:
            record = doc.get(key)
            record.revision += 1
            record.value = value
            record.by = SetBy.LEGACY.value
            record.at = get_now_iso()
            record.applied = Applied(record.revision, value, record.at)
            record.error = None
            record.log = []
            doc.settings[key] = record
            self._write(doc)
            return record

    def seed(self, read_live: Callable[[], dict[SettingKey, Any]]) -> list[SettingKey]:
        """Every setting the file has no record of gets the live home's value, as applied revision 1 (a new
        file, or one an unreadable file was replaced by). Returns the keys this call added."""
        with self._hold_document() as doc:
            missing = [key for key in SettingKey if key not in doc.settings]
            if not missing:
                return []
            live = read_live()
            now = get_now_iso()
            added = [key for key in missing if key in live]
            for key in added:
                doc.settings[key] = Setting(key=key, revision=1, value=live[key], by=SetBy.LEGACY.value, at=now,
                                            applied=Applied(1, live[key], now))
            if added:
                self._write(doc)
            return added

    @contextmanager
    def _hold_document(self) -> Iterator[SettingsDoc]:
        """The document under settings.lock. Held only for a read-modify-write, never across network I/O."""
        self._ensure_folder()
        with file_lock(self.lock_path):
            try:
                doc = self.load()
            except SettingsTooNew:
                raise  # a newer Probe's file: this one writes nothing over it
            except SettingsUnreadable:
                # Kept for a look, never lost; the live homes still hold every value (`seed` refills them).
                os.replace(self.path, self.path.with_name(FILE_NAME + UNREADABLE_SUFFIX))
                doc = SettingsDoc()
            yield doc

    def _write(self, doc: SettingsDoc) -> None:
        write_text_atomic(self.path, to_text(doc), mode=0o600)

    def _ensure_folder(self) -> None:
        self.folder.mkdir(mode=0o700, parents=True, exist_ok=True)

    @staticmethod
    def _is_live(claim: Claim) -> bool:
        """Is the claim's process still running? Unknown (no readable start time) counts as live for an hour."""
        alive = procid.alive(claim.pid, claim.start) if claim.start else None
        if alive is None:
            since = datetime.strptime(claim.since, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - since).total_seconds() < UNREADABLE_CLAIM_LIMIT_S
        return alive


def _build_wire(doc: SettingsDoc) -> dict:
    settings = {}
    for key, record in doc.settings.items():
        wire: dict[str, Any] = {
            "revision": record.revision,
            "value": record.value,
            "by": record.by,
            "at": record.at,
            "claim": None if record.claim is None else {
                "revision": record.claim.revision, "pid": record.claim.pid,
                "start": record.claim.start, "since": record.claim.since},
            "applied": None if record.applied is None else {
                "revision": record.applied.revision, "value": record.applied.value, "at": record.applied.at},
            "error": None if record.error is None else {
                "revision": record.error.revision, "code": record.error.code,
                "message": record.error.message, "retryable": record.error.is_retryable},
        }
        if key is SettingKey.WORKSPACE:
            wire["context"], wire["account_id"] = record.context, record.account_id
        if key is SettingKey.TRANSCRIPTS:
            wire["log"] = [{"revision": e.revision, "value": e.value, "by": e.by, "at": e.at} for e in record.log]
        settings[key.value] = wire
    return {"settings": {**doc.unknown, **settings}, "version": doc.version}


def _parse_record(key: SettingKey, raw: object) -> Setting:
    if not isinstance(raw, dict):
        raise SettingsUnreadable(f"settings.json: {key.value} is not an object")
    try:
        claim, applied, error = raw.get("claim"), raw.get("applied"), raw.get("error")
        return Setting(
            key=key,
            revision=int(raw["revision"]),
            value=raw.get("value"),
            by=raw.get("by"),
            at=raw.get("at"),
            context=raw.get("context"),
            account_id=raw.get("account_id"),
            log=[LogEntry(int(e["revision"]), e.get("value"), e["by"], e["at"]) for e in raw.get("log") or []],
            claim=None if claim is None else Claim(int(claim["revision"]), int(claim["pid"]),
                                                   str(claim["start"]), str(claim["since"])),
            applied=None if applied is None else Applied(int(applied["revision"]), applied.get("value"),
                                                         str(applied["at"])),
            error=None if error is None else ApplyError(int(error["revision"]), str(error["code"]),
                                                         str(error["message"]), bool(error["retryable"])),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise SettingsUnreadable(f"settings.json: {key.value} is malformed ({exc})") from None
