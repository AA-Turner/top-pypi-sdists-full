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
from abstra_internals.repositories.factory import Repositories
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings
from abstra_internals.templates import (
    new_agent_code,
    new_form_code,
    new_hook_code,
    new_job_code,
    new_script_code,
)
from abstra_internals.utils.file import safe_write_file


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

        return [
            AbstraLibApiEditorCodebaseFilesGetResponseItem(
                file=self.file_node(child_path.relative_to(Settings.root_path)),
                stages=[
                    AbstraLibApiEditorCodebaseFilesGetResponseItemStagesItem(
                        id=stage.id,
                        type=stage.type_name,
                    )
                    for stage in project.get_stages_by_file_path(child_path)
                    if stage.type_name != "component"
                ],
            )
            for child_path in FileSystemService.list_files(
                full_path,
                include_dirs=True,
                use_ignore=True,
                recursive=False,
                allowed_suffixes=allowed_suffixes,
            )
            if child_path != full_path
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

        if path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {path}")

        if path.exists() and overwrite:
            path.unlink()

        path.parent.mkdir(parents=True, exist_ok=True)

        if content is not None:
            path.write_bytes(content)
        else:
            path.touch()
        return CommonFileNode(
            path_parts=list(relative_path.parts),
            size=path.stat().st_size,
            last_modified=datetime.fromtimestamp(path.stat().st_mtime),
            type="directory" if path.is_dir() else "file",
        )

    def delete_file(
        self, path_parts: List[str]
    ) -> AbstraLibApiEditorCodebaseFilesDeleteResponse:
        from abstra_internals.settings import Settings

        path = Path(*path_parts)
        if not path.is_absolute():
            path = Settings.root_path / path

        if path.is_dir():
            FileSystemService.rm_tree(path)
        else:
            path.unlink()
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
            new_path = path.parent / Path(*new_name)
        else:
            raise ValueError(f"Invalid new name: {new_name}")

        # Check if the renamed file is a workflow stage
        project = self.repos.project.load(include_disabled_stages=True)
        stages = project.get_stages_by_file_path(path)

        path.rename(new_path)

        if stages:
            from abstra_internals.settings import Settings

            relative_new_path = new_path.relative_to(Settings.root_path)
            stages[0].update({"file": str(relative_new_path)})
            self.repos.project.save(project)

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

        return AbstraLibApiEditorCodebaseFilesPutResponse(ok=True)

    def get_file(self, path):
        if isinstance(path, str):
            path = Path(path).absolute()
        elif isinstance(path, Path):
            path = path.absolute()
        elif not isinstance(path, Path):
            raise ValueError(f"Invalid path: {path}")
        mtype, _ = mimetypes.guess_type(path)
        return flask.send_file(path, mimetype=mtype)

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
