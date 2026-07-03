import os
import time
from pathlib import Path
from typing import Any, Callable, Optional, Union

import click
from watchdog.events import (
    DirDeletedEvent,
    FileDeletedEvent,
    PatternMatchingEventHandler,
)
from watchdog.observers import Observer

from tinybird.datafile.common import Datafile, DatafileKind
from tinybird.tb.modules.datafile.fixture import FixtureExtension
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project


class WatchProjectHandler(PatternMatchingEventHandler):
    valid_extensions = [
        ".datasource",
        ".pipe",
        "connection",
        FixtureExtension.CSV,
        FixtureExtension.NDJSON,
        ".sql",
        ".env",
        ".env.local",
    ]

    def __init__(self, project: Project, config: dict[str, Any], process: Callable):
        self.project = project
        self.config = config
        self.process = process
        self.datafiles = project.get_project_datafiles()
        patterns = [f"**/*{ext}" for ext in self.valid_extensions]
        super().__init__(patterns=patterns)

    def should_process(self, event: Any) -> Optional[str]:
        if event.is_directory:
            return None

        if not any(event.src_path.endswith(ext) for ext in self.valid_extensions):
            return None

        if os.path.exists(event.src_path):
            return event.src_path

        if os.path.exists(event.dest_path):
            return event.dest_path

        return event.src_path

    def _process(self, path: Optional[str] = None) -> None:
        click.echo(FeedbackManager.highlight(message="» Rebuilding project..."))
        self.process(watch=True, file_changed=path, diff=self.diff(path), config=self.config)

    def diff(self, path: Optional[str] = None) -> Optional[str]:
        if not path:
            return None

        current_datafile = self.datafiles.get(path, None)
        new_datafile = self.project.get_datafile(path)
        table_name = None
        if current_datafile and new_datafile:
            if current_datafile.kind == DatafileKind.datasource:
                table_name = self.datasource_diff(current_datafile, new_datafile)
            elif current_datafile.kind == DatafileKind.pipe:
                table_name = self.pipe_diff(current_datafile, new_datafile)

        self.refresh_datafiles()
        return table_name

    def refresh_datafiles(self) -> None:
        self.datafiles = self.project.get_project_datafiles()

    def datasource_diff(self, current_datafile: Datafile, new_datafile: Datafile) -> Optional[str]:
        current_schema = current_datafile.nodes[0].get("schema")
        new_schema = new_datafile.nodes[0].get("schema")
        if current_schema != new_schema:
            return current_datafile.nodes[0].get("name")
        return None

    def pipe_diff(self, current_datafile: Datafile, new_datafile: Datafile) -> Optional[str]:
        current_nodes = current_datafile.nodes
        current_sql_dict = {node.get("name"): node.get("sql") for node in current_nodes}
        new_nodes = new_datafile.nodes
        new_sql_dict = {node.get("name"): node.get("sql") for node in new_nodes}
        for node in new_sql_dict.keys():
            if node and node not in current_sql_dict:
                return node

        for node_name, sql in new_sql_dict.items():
            current_sql = current_sql_dict.get(node_name)
            if current_sql and current_sql != sql:
                return node_name

        return None

    def on_any_event(self, event):
        if str(event.src_path).endswith("~"):
            return None

        if event.event_type == "modified":
            self.modified(event)
        elif event.event_type == "deleted":
            self.deleted(event)

    def created(self, event: Any) -> None:
        if path := self.should_process(event):
            filename = Path(path).name
            click.echo(FeedbackManager.highlight(message=f"\n\n⟲ New file detected: {filename}\n"))
            self._process(path)

    def modified(self, event: Any) -> None:
        if path := self.should_process(event):
            filename = Path(path).name
            click.echo(FeedbackManager.highlight(message=f"\n\n⟲ Changes detected in {filename}\n"))
            self._process(path)

    def deleted(self, event: Union[DirDeletedEvent, FileDeletedEvent]) -> None:
        filename = Path(str(event.src_path)).name
        if event.is_directory:
            click.echo(FeedbackManager.highlight(message=f"\n\n⟲ Deleted directory: {filename}\n"))
        else:
            click.echo(FeedbackManager.highlight(message=f"\n\n⟲ Deleted file: {filename}\n"))
        self._process()


def watch_project(
    process: Callable[[bool, Optional[str], Optional[str]], None],
    project: Project,
    config: dict[str, Any],
) -> None:
    event_handler = WatchProjectHandler(project=project, process=process, config=config)
    observer = Observer()
    observer.schedule(event_handler, path=str(project.path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
