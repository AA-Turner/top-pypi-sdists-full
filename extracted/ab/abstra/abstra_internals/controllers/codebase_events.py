import hashlib
import json
import threading
from collections import OrderedDict
from pathlib import Path
from typing import List, Optional, TypeVar

import flask_sock
from dotenv import load_dotenv

from abstra_internals.contracts_generated import AbstraLibApiEditorCodebaseEventsMessage
from abstra_internals.controllers.linter_events import LinterEventController
from abstra_internals.logger import AbstraLogger
from abstra_internals.modules import reload_module
from abstra_internals.repositories.factory import Repositories
from abstra_internals.repositories.linter.rules import (
    run_after_abstra_json_change,
    run_after_css_change,
    run_after_env_or_gitignore_change,
    run_after_html_change,
    run_after_js_change,
    run_after_py_change,
    run_after_requirements_change,
)
from abstra_internals.services.file_watcher import FSEventType
from abstra_internals.settings import Settings


def rules_for_path(filepath: Path) -> Optional[list]:
    """Map a changed file to the linter rule group that should re-run, or None
    when no rule cares about it. Shared by both the FileWatcher and CodebaseEventController"""
    filename = filepath.name
    if filename == "requirements.txt":
        return run_after_requirements_change
    if filename == "abstra.json":
        return run_after_abstra_json_change
    if filename in (".env", ".gitignore"):
        return run_after_env_or_gitignore_change
    suffix = filepath.suffix
    if suffix == ".py":
        return run_after_py_change
    if suffix == ".html":
        return run_after_html_change
    if suffix == ".css":
        return run_after_css_change
    if suffix == ".js":
        return run_after_js_change
    return None


# Source-file events affect only the saved file, so path-scoped rules can
# re-lint just that file.
_PATH_SCOPED_SUFFIXES = (".py", ".html", ".css", ".js")


def lint_scope_for_path(filepath: Path) -> Optional[Path]:
    if filepath.suffix in _PATH_SCOPED_SUFFIXES:
        return filepath
    return None


_K = TypeVar("_K")
_V = TypeVar("_V")


def _lru_set(od: "OrderedDict[_K, _V]", key: _K, value: _V, max_size: int) -> None:
    """Bounded LRU upsert: assign, move to the MRU end, evict the oldest entries
    until len(od) <= max_size."""
    od[key] = value
    od.move_to_end(key)
    while len(od) > max_size:
        od.popitem(last=False)


class CodebaseEventController:
    listeners: List[flask_sock.Server] = []

    _lock = threading.Lock()

    # Controller-driven events (EDITOR_MODE=web, where the file watcher DON'T run).
    # In local the watcher already does both, so the controller path is a no-op.
    _repositories: Optional[Repositories] = None
    _controller_driven: bool = False
    _lint_lock = threading.Lock()
    _lint_timer: Optional[threading.Timer] = None
    _pending_rules: dict = {}  # rule.name -> rule, accumulated across debounce
    # rule.name -> Optional[set[Path]]: the paths to scope that rule's run to.
    # None means unscoped (full scan) and is sticky — once a config event
    # demands a full run for a rule, later scoped events can't narrow it.
    _pending_scopes: dict = {}
    _pending_full: bool = False

    # Content-hash gate: skip a lint pass when the file's bytes are identical to
    # the previous pass (idempotent saves, mtime/metadata touches). Bounded LRU
    # so long sessions don't accumulate dead paths.
    _MAX_TRACKED_FILES: int = 500
    _content_hashes: "OrderedDict[Path, str]" = OrderedDict()
    _content_hash_lock = threading.Lock()

    @classmethod
    def configure(cls, repositories: Repositories, controller_driven: bool) -> None:
        cls._repositories = repositories
        cls._controller_driven = controller_driven

    @classmethod
    def _content_changed(cls, filepath: Path) -> bool:
        try:
            data = filepath.read_bytes()
        except OSError:
            # File gone/inaccessible — forget the entry and treat as a real
            # event (a deletion is a real change worth re-linting).
            with cls._content_hash_lock:
                cls._content_hashes.pop(filepath, None)
            return True
        digest = hashlib.sha256(data).hexdigest()
        with cls._content_hash_lock:
            if cls._content_hashes.get(filepath) == digest:
                cls._content_hashes.move_to_end(filepath)
                return False
            _lru_set(cls._content_hashes, filepath, digest, cls._MAX_TRACKED_FILES)
        return True

    @classmethod
    def register(cls, listener: flask_sock.Server):
        with cls._lock:
            cls.listeners.append(listener)

    @classmethod
    def unregister(cls, listener: flask_sock.Server):
        with cls._lock:
            try:
                cls.listeners.remove(listener)
            except ValueError:
                pass

    @classmethod
    def broadcast_changes(
        cls, filepath: Path, event: FSEventType, content: Optional[str]
    ):
        absolute_root_path = Settings.root_path.resolve()
        absolute_filepath = filepath.resolve()
        message = AbstraLibApiEditorCodebaseEventsMessage(
            filepath=str(absolute_filepath.relative_to(absolute_root_path)),
            event=event,
            content=content,
        )
        cls.broadcast_raw(message.to_dict())

    @classmethod
    def broadcast_raw(cls, message: dict) -> None:
        with cls._lock:
            listeners = list(cls.listeners)

        failed = []
        for listener in listeners:
            try:
                with cls._lock:
                    listener.send(json.dumps(message))
            except Exception:
                failed.append(listener)

        for listener in failed:
            cls.unregister(listener)

    @classmethod
    def notify_requirements_changed(cls) -> None:
        path = Settings.root_path / "requirements.txt"
        cls.broadcast_changes(path, "changed", None)
        cls.schedule_lint_for_path(path)

    @classmethod
    def notify_change(cls, filepath: Path, event: FSEventType) -> None:
        if not cls._controller_driven:
            return
        cls.broadcast_changes(filepath, event, None)
        cls.schedule_lint_for_path(filepath)

    @classmethod
    def notify_project_saved(cls) -> None:
        cls.notify_change(Settings.root_path / "abstra.json", "changed")

    @classmethod
    def schedule_lint_for_path(cls, filepath: Path) -> None:
        """This method is used by the CodebaseEventController.notify_change (web-editor)"""
        # Gate on _controller_driven first: in local mode the FileWatcher owns
        # lint_files, so recording the hash here would gate that lint out.
        if not cls._controller_driven or cls._repositories is None:
            return
        rules = rules_for_path(filepath)
        if not rules:
            return
        if not cls._content_changed(filepath):
            return
        cls._schedule_lint(rules=rules, scope=lint_scope_for_path(filepath))

    @classmethod
    def schedule_full_lint(cls) -> None:
        """Re-run every rule. Used after git ops that rewrite the working tree
        (checkout/pull/revert/stash) where we don't track which files changed.
        """
        cls._schedule_lint(full=True)

    @classmethod
    def _schedule_lint(
        cls,
        rules: Optional[list] = None,
        full: bool = False,
        scope: Optional[Path] = None,
    ) -> None:
        if not cls._controller_driven or cls._repositories is None:
            return
        with cls._lint_lock:
            if full:
                cls._pending_full = True
            for rule in rules or []:
                cls._pending_rules[rule.name] = rule
                if scope is None:
                    cls._pending_scopes[rule.name] = None
                elif rule.name not in cls._pending_scopes:
                    cls._pending_scopes[rule.name] = {scope}
                elif cls._pending_scopes[rule.name] is not None:
                    cls._pending_scopes[rule.name].add(scope)
            if cls._lint_timer is not None:
                cls._lint_timer.cancel()
            cls._lint_timer = threading.Timer(0.5, cls._run_pending_lint)
            cls._lint_timer.daemon = True
            cls._lint_timer.start()

    @classmethod
    def _run_pending_lint(cls) -> None:
        with cls._lint_lock:
            full = cls._pending_full
            rules = list(cls._pending_rules.values())
            scopes = dict(cls._pending_scopes)
            cls._pending_full = False
            cls._pending_rules = {}
            cls._pending_scopes = {}
        repositories = cls._repositories
        if repositories is None:
            return
        try:
            if full:
                checks = repositories.linter.update_checks()
            elif rules:
                checks = cls._run_partitioned_lint(repositories, rules, scopes)
            else:
                return
            LinterEventController.broadcast(checks)
        except Exception as e:
            AbstraLogger.error(f"[Editor] controller-driven lint failed: {e}")

    @staticmethod
    def _run_partitioned_lint(
        repositories: Repositories, rules: list, scopes: dict
    ) -> list:
        """Run unscoped rules with a full scan and scoped rules restricted to
        their accumulated paths, grouping rules that share the same path set
        into a single repository call."""
        unscoped = [r for r in rules if scopes.get(r.name) is None]
        by_paths: dict = {}  # frozenset[Path] -> list[rule]
        for rule in rules:
            paths = scopes.get(rule.name)
            if paths is not None:
                by_paths.setdefault(frozenset(paths), []).append(rule)

        checks = []
        if unscoped:
            checks = repositories.linter.update_specific_checks(unscoped)
        for paths, scoped_rules in by_paths.items():
            checks = repositories.linter.update_specific_checks(
                scoped_rules, paths=list(paths)
            )
        return checks

    def __init__(self, repositories: Repositories):
        self.repositories = repositories

    def reload_env(self, filepath: Path, event: FSEventType, content: Optional[str]):
        if filepath.name == ".env":
            AbstraLogger.info("Reloading .env and all modules")
            load_dotenv(filepath, override=True)
            for dep in self.repositories.project.load().get_local_dependencies():
                reload_module(dep)
            return

    def reload_modules(
        self, filepath: Path, event: FSEventType, content: Optional[str]
    ):
        if filepath.suffix == ".py":
            resolved_deps = [
                dep.resolve()
                for dep in self.repositories.project.load().get_local_dependencies()
            ]

            if filepath.resolve() in resolved_deps:
                AbstraLogger.info(f"Reloading modified module: {filepath}")
                reload_module(filepath)
                return

    def lint_files(self, filepath: Path, event: FSEventType, content: Optional[str]):
        """This method is used by the FileWatcher"""
        # PyreflyLSP rewrites .pyrefly_buffer.py on every type-check; that
        # scratch file must not retrigger the whole Python lint group.
        if filepath.name == ".pyrefly_buffer.py":
            return
        target_rules = rules_for_path(filepath)
        if not target_rules:
            return
        # Content-hash gate: skip idempotent saves / mtime-only touches.
        if not self._content_changed(filepath):
            return

        scope = lint_scope_for_path(filepath)
        checks = self.repositories.linter.update_specific_checks(
            target_rules, paths=[scope] if scope is not None else None
        )
        LinterEventController.broadcast(checks)
