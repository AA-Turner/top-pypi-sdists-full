import os
from dataclasses import dataclass
from typing import Any, Dict, List

from werkzeug.datastructures import FileStorage

from abstra_internals.cloud_api import get_session_path, get_tunnel_secret_key
from abstra_internals.consts.filepaths import AI_UPLOADS_DIR_PATH
from abstra_internals.contracts_generated import (
    AbstraLibApiAiStreamRequest,
    CloudApiCliAiV2StreamRequest,
)
from abstra_internals.controllers.main import MainController
from abstra_internals.credentials import resolve_headers
from abstra_internals.repositories.project.project import StageWithFile
from abstra_internals.settings import Settings
from abstra_internals.utils.file import silent_traverse_code
from abstra_internals.utils.packages import get_local_package_version
from abstra_internals.utils.paths import get_relative_path
from abstra_internals.utils.string import sanitize_filename

RETRY_FLAG = "abstra__trigger__retry"


@dataclass
class PythonFile:
    filename: str
    content: str
    stage: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PythonFile":
        return PythonFile(data["filename"], data["content"], data["stage"])


def runtime_from_stage(stage: StageWithFile):
    if stage.type_name == "form":
        return "forms"
    elif stage.type_name == "hook":
        return "hooks"
    elif stage.type_name == "script":
        return "scripts"
    elif stage.type_name == "job":
        return "jobs"
    else:
        raise ValueError(f"Unknown stage type: {stage.type_name}")


def find_imported_code(stage: StageWithFile) -> Dict[str, str]:
    seen_files = set()
    conflict_counter = 0
    files = {}
    for path in silent_traverse_code(stage.file_path):
        if path in seen_files:
            conflict_counter += 1
            if conflict_counter > 10:  # Circular imports?
                break
            continue
        seen_files.add(path)
        if stage.file_path.absolute() == path.absolute():
            continue
        relative_path = str(get_relative_path(path, Settings.root_path))
        files[relative_path] = "\n".join(
            [
                f"# {relative_path}",
                "```python",
                path.read_text(encoding="utf-8"),
                "````",
            ]
        )
    return files


class AiController:
    def __init__(self, controller: MainController):
        self.controller = controller
        self.repos = controller.repositories

    def _ai_uploads_root(self) -> "os.PathLike[str]":
        return Settings.root_path / AI_UPLOADS_DIR_PATH

    def save_uploaded_file(
        self, file_storage: FileStorage, conversation_id: str
    ) -> Dict[str, Any]:
        """Stream an uploaded file to .abstra/ai_uploads/{conversation_id}/.

        Returns metadata describing the saved file so the desktop can reference
        it by path in subsequent chat messages.
        """
        safe_file_name = os.path.basename(file_storage.filename or "file")
        safe_conversation_id = sanitize_filename(conversation_id)
        relative_path = os.path.join(
            AI_UPLOADS_DIR_PATH, safe_conversation_id, safe_file_name
        )
        full_path = Settings.root_path / relative_path
        os.makedirs(full_path.parent, exist_ok=True)
        file_storage.save(str(full_path))
        file_size = os.path.getsize(full_path)
        mime_type = file_storage.mimetype or "application/octet-stream"
        return {
            "filePath": relative_path,
            "fileName": safe_file_name,
            "fileSize": file_size,
            "mimeType": mime_type,
        }

    def delete_uploaded_file(self, relative_path: str) -> None:
        """Remove a previously uploaded attachment.

        Refuses to touch anything that is not a file strictly inside
        .abstra/ai_uploads/. Any filesystem error is normalized to ValueError
        so the route can return a single 400 status.
        """
        uploads_root = os.path.realpath(str(self._ai_uploads_root()))
        full_path = os.path.realpath(str(Settings.root_path / relative_path))
        if not full_path.startswith(uploads_root + os.sep):
            raise ValueError(
                "Path must reference a file inside the AI uploads directory"
            )
        if not os.path.exists(full_path):
            return
        if not os.path.isfile(full_path):
            raise ValueError(
                "Path must reference a file inside the AI uploads directory"
            )
        try:
            os.remove(full_path)
        except OSError as exc:
            raise ValueError("Failed to delete uploaded file") from exc

    def send_ai_message(
        self,
        body: AbstraLibApiAiStreamRequest,
        user_jwt=None,
    ):
        try:
            yield from self.repos.ai.get_ai_messages(
                CloudApiCliAiV2StreamRequest(
                    conversation_id=body.conversation_id,
                    content=body.content,
                    context={
                        **body.context,
                        "libVersion": str(get_local_package_version()),
                    },
                    secret_key=get_tunnel_secret_key(),
                    tunnel_session_path=get_session_path(),
                    human_approval=body.human_approval,
                    tool_calls_approval=body.tool_calls_approval,
                    browser_tools=body.browser_tools,
                    browser_tool_responses=body.browser_tool_responses,
                    auto_approve_tool_calls=body.auto_approve_tool_calls,
                ),
                user_jwt=user_jwt,
            )
        except Exception as e:
            print(f"Error in send_ai_message: {e}")
            yield RETRY_FLAG
            return

    def get_history(self, limit: int, offset: int, user_jwt=None):
        headers = resolve_headers()
        if headers is None:
            return None
        if user_jwt:
            headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
        return self.repos.ai.get_history(headers, limit, offset)

    def create_thread(self, user_jwt=None):
        headers = resolve_headers()
        if headers is None:
            return None
        if user_jwt:
            headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
        return self.repos.ai.create_thread(headers)

    def delete_thread(self, thread_id: str, user_jwt=None):
        if headers := resolve_headers():
            if user_jwt:
                headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
            return self.repos.ai.delete_thread(headers, thread_id)

    def abort_thread(self, thread_id: str, user_jwt=None):
        if headers := resolve_headers():
            if user_jwt:
                headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
            return self.repos.ai.abort_thread(headers, thread_id)

    def init_stages(self, python_files: List[PythonFile]):
        for file in python_files:
            if file.stage == "form":
                script = self.controller.create_form(file.filename[:-3], file.filename)
            elif file.stage == "hook":
                script = self.controller.create_hook(file.filename[:-3], file.filename)
            elif file.stage == "script":
                script = self.controller.create_tasklet(
                    file.filename[:-3], file.filename
                )
            elif file.stage == "job":
                script = self.controller.create_job(file.filename[:-3], file.filename)
            else:
                raise Exception(f"Invalid stage {file.stage}")
            script.file_path.write_text(file.content, encoding="utf-8")
            script.file_path.write_text(file.content, encoding="utf-8")
            script.file_path.write_text(file.content, encoding="utf-8")
            script.file_path.write_text(file.content, encoding="utf-8")
            script.file_path.write_text(file.content, encoding="utf-8")
            script.file_path.write_text(file.content, encoding="utf-8")

    def start_conversation(self, user_jwt=None):
        return self.repos.ai.start_conversation(
            secret_key=get_tunnel_secret_key(),
            tunnel_session_path=get_session_path(),
            user_jwt=user_jwt,
        )

    def compact_conversation(self, conversation_id: str, user_jwt=None):
        headers = resolve_headers()
        if headers is None:
            return None
        if user_jwt:
            headers["Web-Editor-Authorization"] = f"Bearer {user_jwt}"
        return self.repos.ai.compact_conversation(headers, conversation_id)
