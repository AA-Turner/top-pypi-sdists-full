import json
import threading
from pathlib import Path
from typing import List, Optional

import flask_sock
from dotenv import load_dotenv

from abstra_internals.contracts_generated import AbstraLibApiEditorCodebaseEventsMessage
from abstra_internals.controllers.linter_events import LinterEventController
from abstra_internals.logger import AbstraLogger
from abstra_internals.modules import reload_module
from abstra_internals.repositories.factory import Repositories
from abstra_internals.repositories.linter.rules import (
    run_after_abstra_json_change,
    run_after_env_or_gitignore_change,
    run_after_py_change,
    run_after_requirements_change,
)
from abstra_internals.services.file_watcher import FSEventType
from abstra_internals.settings import Settings


class CodebaseEventController:
    listeners: List[flask_sock.Server] = []

    _lock = threading.Lock()

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
        message = AbstraLibApiEditorCodebaseEventsMessage(
            filepath=str(filepath.relative_to(absolute_root_path)),
            event=event,
            content=content,
        )
        with cls._lock:
            listeners = list(cls.listeners)

        failed = []
        for listener in listeners:
            try:
                with cls._lock:
                    listener.send(json.dumps(message.to_dict()))
            except Exception:
                failed.append(listener)

        for listener in failed:
            cls.unregister(listener)

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
        filename = filepath.name

        if filename == "requirements.txt":
            target_rules = run_after_requirements_change
        elif filename == "abstra.json":
            target_rules = run_after_abstra_json_change
        elif filename in (".env", ".gitignore"):
            target_rules = run_after_env_or_gitignore_change
        elif filepath.suffix == ".py":
            target_rules = run_after_py_change
        else:
            return

        checks = self.repositories.linter.update_specific_checks(target_rules)
        LinterEventController.broadcast(checks)
