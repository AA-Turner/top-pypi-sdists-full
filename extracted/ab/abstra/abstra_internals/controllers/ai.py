import base64
import io
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pypdfium2 as pdfium

from abstra_internals.cloud_api import get_session_path, get_tunnel_secret_key
from abstra_internals.consts.filepaths import AI_UPLOADS_DIR_PATH
from abstra_internals.contracts_generated import (
    AbstraLibApiAiStreamRequest,
    CloudApiCliAiV2StreamRequest,
    CloudApiCliAiV2StreamRequestContentItem,
    CloudApiCliAiV2StreamRequestContentItemAssistantFileInput,
    CloudApiCliAiV2StreamRequestContentItemAssistantTextInput,
)
from abstra_internals.controllers.main import MainController
from abstra_internals.credentials import resolve_headers
from abstra_internals.repositories.project.project import StageWithFile
from abstra_internals.settings import Settings
from abstra_internals.utils.file import silent_traverse_code
from abstra_internals.utils.image import constrain_image_size
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

    def _save_file_to_project(
        self,
        file_name: str,
        file_content: Optional[str],
        conversation_id: str,
    ) -> Optional[str]:
        """Save an uploaded file to .abstra/ai_uploads/{conversation_id}/.

        Returns the relative path where the file was saved,
        or None if saving failed.
        """
        try:
            safe_file_name = os.path.basename(file_name)
            safe_conversation_id = sanitize_filename(conversation_id)
            relative_path = os.path.join(
                AI_UPLOADS_DIR_PATH, safe_conversation_id, safe_file_name
            )
            full_path = Settings.root_path / relative_path

            os.makedirs(full_path.parent, exist_ok=True)

            if file_content is None:
                full_path.write_bytes(b"")
            else:
                full_path.write_bytes(base64.b64decode(file_content))

            return relative_path
        except Exception as e:
            print(f"[AiController] Failed to save uploaded file: {e}")
            return None

    def _extract_pdf_images(self, pdf_bytes: bytes) -> List[bytes]:
        images = []
        pdf_io = io.BytesIO(pdf_bytes)
        for page in pdfium.PdfDocument(pdf_io):
            bitmap = page.render(
                scale=4,  # 288 dpi
                rotation=0,
            )
            pil_image = bitmap.to_pil()
            pil_image = constrain_image_size(pil_image)
            image_io = io.BytesIO()
            pil_image.save(image_io, format="png")
            image_io.seek(0)
            images.append(image_io.read())
        return images

    def _process_pdf_content(
        self,
        pdf_file: CloudApiCliAiV2StreamRequestContentItemAssistantFileInput,
        saved_path: Optional[str] = None,
    ) -> List[CloudApiCliAiV2StreamRequestContentItem]:
        processed_items = []
        path_info = f" (saved to project at: {saved_path})" if saved_path else ""
        if pdf_file.file_content is None:
            processed_items.append(
                CloudApiCliAiV2StreamRequestContentItemAssistantTextInput(
                    type="text",
                    text=f"[PDF Document: {pdf_file.file_name} - empty]{path_info}",
                )
            )
            return processed_items
        try:
            pdf_bytes = base64.b64decode(pdf_file.file_content)
            images = self._extract_pdf_images(pdf_bytes)

            processed_items.append(
                CloudApiCliAiV2StreamRequestContentItemAssistantTextInput(
                    type="text",
                    text=f"[PDF Document: {pdf_file.file_name} - {len(images)} page(s)]{path_info}",
                )
            )

            for idx, image_bytes in enumerate(images, 1):
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                processed_items.append(
                    CloudApiCliAiV2StreamRequestContentItemAssistantFileInput(
                        type="file",
                        file_name=f"{pdf_file.file_name}_page_{idx}.png",
                        file_content=image_base64,
                    )
                )
        except Exception as e:
            print(f"Error extracting PDF images: {e}")
            processed_items.append(
                CloudApiCliAiV2StreamRequestContentItemAssistantTextInput(
                    type="text",
                    text=f"[PDF Document: {pdf_file.file_name}]{path_info}\nNote: Could not extract images from this PDF.",
                )
            )
        return processed_items

    _TEXT_EXTENSIONS = {
        ".md",
        ".py",
        ".txt",
        ".json",
        ".csv",
        ".yaml",
        ".yml",
        ".toml",
        ".cfg",
        ".ini",
        ".html",
        ".css",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".xml",
        ".sql",
        ".sh",
        ".bash",
        ".env",
        ".lua",
        ".rb",
        ".go",
        ".rs",
        ".java",
        ".kt",
        ".swift",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".log",
        ".conf",
        ".properties",
    }

    def _try_decode_text_file(
        self,
        item: CloudApiCliAiV2StreamRequestContentItemAssistantFileInput,
        saved_path: Optional[str] = None,
    ) -> CloudApiCliAiV2StreamRequestContentItem:
        """Decode base64 file content to plain text for text-based files."""
        name_lower = item.file_name.lower()
        ext = "." + name_lower.rsplit(".", 1)[-1] if "." in name_lower else ""
        path_info = f" (saved to project at: {saved_path})" if saved_path else ""
        if ext not in self._TEXT_EXTENSIONS:
            return item
        if item.file_content is None:
            return CloudApiCliAiV2StreamRequestContentItemAssistantTextInput(
                type="text",
                text=f"[File: {item.file_name} - empty]{path_info}",
            )
        try:
            text = base64.b64decode(item.file_content).decode("utf-8")
            return CloudApiCliAiV2StreamRequestContentItemAssistantTextInput(
                type="text",
                text=f"[File: {item.file_name}]{path_info}\n{text}",
            )
        except Exception:
            if saved_path:
                return CloudApiCliAiV2StreamRequestContentItemAssistantTextInput(
                    type="text",
                    text=f"[File: {item.file_name}]{path_info}",
                )
            return item

    def _process_content(
        self,
        content: List[CloudApiCliAiV2StreamRequestContentItem],
        conversation_id: str,
    ) -> List[CloudApiCliAiV2StreamRequestContentItem]:
        processed_content = []

        for item in content:
            if isinstance(
                item, CloudApiCliAiV2StreamRequestContentItemAssistantTextInput
            ):
                processed_content.append(item)
                continue

            # Save all files to .abstra/ai_uploads/
            saved_path = self._save_file_to_project(
                item.file_name,
                item.file_content or "",
                conversation_id,
            )

            # All files: send filePath only, AI reads via tool when needed
            processed_content.append(
                CloudApiCliAiV2StreamRequestContentItemAssistantFileInput(
                    type="file",
                    file_name=item.file_name,
                    file_path=saved_path,
                )
            )

        return processed_content

    def send_ai_message(
        self,
        body: AbstraLibApiAiStreamRequest,
        user_jwt=None,
    ):
        try:
            processed_content = self._process_content(
                body.content, body.conversation_id
            )

            yield from self.repos.ai.get_ai_messages(
                CloudApiCliAiV2StreamRequest(
                    conversation_id=body.conversation_id,
                    content=processed_content,
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
