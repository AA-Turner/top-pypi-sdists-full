import mimetypes
import pkgutil
from datetime import datetime
from os.path import sep
from pathlib import Path
from typing import List, Optional, Union, cast

import flask

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorCodebaseDirPostResponse,
    AbstraLibApiEditorCodebaseFilesDeleteResponse,
    AbstraLibApiEditorCodebaseFilesGetResponse,
    AbstraLibApiEditorCodebaseFilesGetResponseItem,
    AbstraLibApiEditorCodebaseFilesGetResponseItemStagesItem,
    AbstraLibApiEditorCodebaseFilesPatchResponse,
    AbstraLibApiEditorCodebaseFilesPutRequest,
    AbstraLibApiEditorCodebaseFilesPutResponse,
    AbstraLibApiEditorCodebaseSettingsGetResponse,
    CommonFileNode,
    CommonFileNodeType,
)
from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.controllers.language_server import (
    notify_file_changed as _lsp_notify_file_changed,
)
from abstra_internals.repositories.factory import Repositories
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings
from abstra_internals.templates import (
    new_agent_code,
    new_form_code,
    new_hook_code,
    new_job_code,
    new_page_code,
    new_script_code,
)
from abstra_internals.utils.file import safe_write_file

_PY_SUFFIXES = (".py", ".pyi")


def _notify_lsp(path: Path, change_type: int) -> None:
    # Pyrefly only cares about Python sources; ignore other writes.
    if path.suffix in _PY_SUFFIXES:
        _lsp_notify_file_changed(path, change_type)


def _path_inside_root(path: Path) -> bool:
    root = Settings.root_path.resolve()
    resolved = path.resolve()
    return resolved == root or resolved.is_relative_to(root)


class CodebaseController:
    def __init__(self, repos: Repositories):
        self.repos = repos

    def file_node(
        self, path: Path, type_override: Optional[str] = None
    ) -> CommonFileNode:
        if type_override:
            is_dir = type_override == "package"
            type_name = type_override
            size = 0
            mtime = 0.0
        else:
            is_dir = path.is_dir()
            type_name = "directory" if is_dir else "file"
            try:
                stats = path.stat()
                size = stats.st_size
                mtime = stats.st_mtime
            except OSError:
                size = 0
                mtime = 0.0

        return CommonFileNode(
            path_parts=list(path.parts),
            size=size,
            last_modified=datetime.fromtimestamp(mtime),
            type=cast(CommonFileNodeType, type_name),
        )

    def list_files(
        self, path: Union[str, Path, None], mode: str = "file"
    ) -> AbstraLibApiEditorCodebaseFilesGetResponse:
        if path is None:
            path = Path()
        elif isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise ValueError(f"Invalid path: {path}")

        project = self.repos.project.load(include_disabled_stages=True)

        if mode == "module":
            modules = []
            search_path = (
                str(Settings.root_path / path)
                if str(path) != "."
                else str(Settings.root_path)
            )
            for _, name, ispkg in pkgutil.iter_modules([search_path]):
                # Basic check to avoid unrelated modules if path is not in sys.path
                # But pkgutil.iter_modules needs a list of paths
                module_path = path / name
                modules.append(
                    AbstraLibApiEditorCodebaseFilesGetResponseItem(
                        file=self.file_node(
                            module_path, type_override="package" if ispkg else "module"
                        ),
                        stages=[],
                    )
                )
            return modules

        allowed_suffixes = None
        if mode == "image":
            allowed_suffixes = [
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".svg",
                ".webp",
                ".jfif",
                ".pjp",
                ".pjpeg",
            ]
        elif mode == "python-file":
            allowed_suffixes = [".py"]

        # Ensure we are listing relative to root
        full_path = Settings.root_path / path

        ALWAYS_HIDDEN = {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            ".pyrefly_buffer.py",
            "pyrefly.toml",
            ".ruff_cache",
            ".vscode",
            "ruff.toml",
        }

        stages_by_path = project.get_stages_by_file_path_map()

        return [
            AbstraLibApiEditorCodebaseFilesGetResponseItem(
                file=self.file_node(
                    child_path.relative_to(Settings.root_path)
                    if child_path.is_relative_to(Settings.root_path)
                    else child_path
                ),
                stages=[
                    AbstraLibApiEditorCodebaseFilesGetResponseItemStagesItem(
                        id=stage.id,
                        type=stage.type_name,
                    )
                    for stage in stages_by_path.get(child_path.absolute().resolve(), [])
                    if stage.type_name != "component"
                ],
            )
            for child_path in FileSystemService.list_files(
                full_path,
                include_dirs=True,
                use_ignore=False,
                recursive=False,
                allowed_suffixes=allowed_suffixes,
            )
            if child_path != full_path and child_path.name not in ALWAYS_HIDDEN
        ]

    def init_file(self, path: str, type: str):
        if type == "scripts":
            code = new_script_code
        elif type == "forms":
            code = new_form_code
        elif type == "hooks":
            code = new_hook_code
        elif type == "jobs":
            code = new_job_code
        elif type == "pages":
            code = new_page_code
        elif type == "agents":
            code = new_agent_code
        else:
            raise ValueError(f"Invalid type: {type}")

        self.create_file(path, code.encode("utf-8"), overwrite=False)

    def create_file(
        self, path, content: Optional[bytes] = None, overwrite: bool = False
    ) -> CommonFileNode:
        from abstra_internals.settings import Settings

        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise ValueError(f"Invalid path: {path}")

        relative_path = path

        if not path.is_absolute():
            path = Settings.root_path / path
        elif not _path_inside_root(path):
            raise ValueError("Path is outside project root")

        path = path.resolve()
        if not _path_inside_root(path):
            raise ValueError("Path is outside project root")
        relative_path = path.relative_to(Settings.root_path.resolve())

        if path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {path}")

        from abstra_internals.services import file_history

        file_history.safe_track_edit(path)

        if path.exists() and overwrite:
            path.unlink()

        path.parent.mkdir(parents=True, exist_ok=True)

        if content is not None:
            path.write_bytes(content)
        else:
            path.touch()
        _notify_lsp(path, 1)
        CodebaseEventController.notify_change(path, "created")
        return CommonFileNode(
            path_parts=list(relative_path.parts),
            size=path.stat().st_size,
            last_modified=datetime.fromtimestamp(path.stat().st_mtime),
            type="directory" if path.is_dir() else "file",
        )

    def delete_file(
        self, path_parts: List[str]
    ) -> AbstraLibApiEditorCodebaseFilesDeleteResponse:
        from abstra_internals.controllers.file_locks import FileLockController
        from abstra_internals.settings import Settings

        path = Path(*path_parts)
        if not path.is_absolute():
            path = Settings.root_path / path

        if path.is_dir():
            py_files = [p for p in path.rglob("*") if p.suffix in _PY_SUFFIXES]
            FileSystemService.rm_tree(path)
            for p in py_files:
                _notify_lsp(p, 3)
        else:
            was_python = path.suffix in _PY_SUFFIXES
            path.unlink()
            if was_python:
                _notify_lsp(path, 3)
        CodebaseEventController.notify_change(path, "deleted")

        try:
            relative = path.relative_to(Settings.root_path.resolve())
            FileLockController.release_for_path(str(relative))
        except ValueError:
            pass

        return AbstraLibApiEditorCodebaseFilesDeleteResponse(ok=True)

    def rename_file(
        self, path, new_name
    ) -> AbstraLibApiEditorCodebaseFilesPatchResponse:
        from abstra_internals.settings import Settings

        if isinstance(path, str):
            path = Path(path)
        elif isinstance(path, List):
            path = Path(*path)
        elif not isinstance(path, Path):
            raise ValueError(f"Invalid path: {path}")

        if not path.is_absolute():
            path = Settings.root_path / path

        if isinstance(new_name, str):
            new_path = path.parent / new_name
        elif isinstance(new_name, List):
            new_path = Path(*new_name)
            if not new_path.is_absolute():
                new_path = Settings.root_path / new_path
        else:
            raise ValueError(f"Invalid new name: {new_name}")

        # Never overwrite an existing file
        if new_path.exists() and not path.samefile(new_path):
            raise FileExistsError(f"File already exists: {new_path}")

        # Check if the renamed file is a workflow stage
        project = self.repos.project.load(include_disabled_stages=True)
        stages = project.get_stages_by_file_path(path)

        # Capture .py files inside a directory rename before the move, so we
        # can notify pyrefly of every (old → new) path pair.
        dir_py_files: List[Path] = []
        if path.is_dir():
            dir_py_files = [p for p in path.rglob("*") if p.suffix in _PY_SUFFIXES]

        path.rename(new_path)

        if dir_py_files:
            for old_p in dir_py_files:
                new_p = new_path / old_p.relative_to(path)
                _lsp_notify_file_changed(old_p, 3)
                _lsp_notify_file_changed(new_p, 1)
        else:
            _notify_lsp(path, 3)
            _notify_lsp(new_path, 1)

        if stages:
            from abstra_internals.settings import Settings

            relative_new_path = new_path.relative_to(Settings.root_path)
            stages[0].update({"file": str(relative_new_path)})
            self.repos.project.save(project)

        CodebaseEventController.notify_change(path, "deleted")
        CodebaseEventController.notify_change(new_path, "created")

        from abstra_internals.controllers.file_locks import FileLockController
        from abstra_internals.settings import Settings

        try:
            relative_old = path.relative_to(Settings.root_path.resolve())
            FileLockController.release_for_path(str(relative_old))
        except ValueError:
            pass

        return AbstraLibApiEditorCodebaseFilesPatchResponse(ok=True)

    def edit_file(
        self, path, content: AbstraLibApiEditorCodebaseFilesPutRequest
    ) -> AbstraLibApiEditorCodebaseFilesPutResponse:
        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise ValueError(f"Invalid path: {path}")

        if not path.is_absolute():
            path = Settings.root_path / path

        resolved_path = path.resolve()
        if not resolved_path.is_relative_to(Settings.root_path.resolve()):
            raise ValueError(f"Path is outside project root: {path}")

        write_ok = safe_write_file(resolved_path, content.content)
        if not write_ok:
            return AbstraLibApiEditorCodebaseFilesPutResponse(ok=False)

        _notify_lsp(resolved_path, 2)
        CodebaseEventController.notify_change(resolved_path, "changed")
        return AbstraLibApiEditorCodebaseFilesPutResponse(ok=True)

    def get_file(self, path):
        from abstra_internals.constants import get_persistent_dir
        from abstra_internals.environment import WORKER_FILES_FOLDER

        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise ValueError(f"Invalid path: {path}")

        if path.is_absolute():
            try:
                relative_to_worker = path.relative_to(WORKER_FILES_FOLDER)
                path = get_persistent_dir() / relative_to_worker
            except ValueError:
                pass  # not a worker path, leave alone

        resolved = (
            (Settings.root_path / path).resolve()
            if not path.is_absolute()
            else path.resolve()
        )
        if not path.is_absolute() and not resolved.is_relative_to(
            Settings.root_path.resolve()
        ):
            flask.abort(403)
        if not resolved.exists():
            flask.abort(404)
        mtype, _ = mimetypes.guess_type(resolved)
        return flask.send_file(resolved, mimetype=mtype)

    def mkdir(
        self, path: Union[str, Path, List[str]]
    ) -> AbstraLibApiEditorCodebaseDirPostResponse:
        from abstra_internals.settings import Settings

        if isinstance(path, str):
            path = Path(path)
        elif isinstance(path, list):
            path = Path(*path)
        elif not isinstance(path, Path):
            raise ValueError(f"Invalid path: {path}")

        if not path.is_absolute():
            path = Settings.root_path / path

        path.mkdir(parents=True, exist_ok=True)
        CodebaseEventController.notify_change(path, "created")
        return AbstraLibApiEditorCodebaseDirPostResponse(ok=True)

    def check_file(self, path: str) -> dict:
        full_path = Settings.root_path / path
        return {"exists": full_path.exists()}

    def check_files(self, paths: List[str]) -> dict:
        return {path: (Settings.root_path / path).exists() for path in paths}

    def settings(self) -> AbstraLibApiEditorCodebaseSettingsGetResponse:
        return AbstraLibApiEditorCodebaseSettingsGetResponse(
            separator=sep,
        )
