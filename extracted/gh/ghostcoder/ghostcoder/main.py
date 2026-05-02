import logging
from pathlib import Path
from typing import List, Optional

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from llama_index.vector_stores import ChromaVectorStore

from ghostcoder.codeblocks.coderepository import CodeRepository
from ghostcoder.runtime.base import Runtime
from ghostcoder.tools.base import BaseResponse
from ghostcoder.tools.code_writer import WriteCodeRequest, WriteCodeResponse
from ghostcoder.tools.file_explorer import FindFilesRequest, FindFilesResponse, ReadFileRequest, ReadFileResponse
from ghostcoder.tools.project_info import ProjectInfoRequest, ProjectInfoResponse
from ghostcoder.write_code import CodeWriter
from ghostcoder.actions.verify.code_verifier import CodeVerifier
from ghostcoder.actions.write_code.prompt import FIX_TESTS_PROMPT
from ghostcoder.callback import LogCallbackHandler
from ghostcoder.codeblocks import CodeBlockType, create_parser
from ghostcoder.display_callback import DisplayCallback
from ghostcoder.filerepository import FileRepository
from ghostcoder.index.code_index import CodeIndex
from ghostcoder.llm import LLMWrapper, ChatLLMWrapper
from ghostcoder.schema import Message, UpdatedFileItem, TextItem, FileItem, CreateBranchRequest
from ghostcoder.test_tools import TestTool
from ghostcoder.utils import count_tokens

logger = logging.getLogger(__name__)


def create_openai_client(
        log_dir: Path,
        llm_name: str,
        temperature: float,
        streaming: bool = True,
        openai_api_key: str = None,
        max_tokens: Optional[int] = None,
        stop_sequence: str = None):
    callback = LogCallbackHandler(str(log_dir))
    logger.info(f"create_openai_client(): llm_name={llm_name}, temperature={temperature}, log_dir={log_dir}")

    model_kwargs = {}
    if stop_sequence:
        model_kwargs["stop"] = [stop_sequence]

    return ChatLLMWrapper(ChatOpenAI(
        model=llm_name,
        openai_api_key=openai_api_key,
        model_kwargs=model_kwargs,
        max_tokens=max_tokens,
        temperature=temperature,
        streaming=streaming,
        callbacks=[callback]
    ))


class Ghostcoder(Runtime):

    def __init__(self,
                 model_name: str = "gpt-4",
                 llm: LLMWrapper = None,
                 basic_llm: LLMWrapper = None,
                 verify_code: bool = False,
                 test_tool: TestTool = None,
                 auto_mode: bool = True,
                 language: str = None,
                 callback: DisplayCallback = None,
                 max_retries: int = 3,
                 log_dir: str = None,
                 openai_api_key: str = None,
                 search_limit: int = 5,
                 debug_mode: bool = False,
                 **kwargs):
        super().__init__(**kwargs)

        log_dir = log_dir or self.repository.repo_path / ".prompt_log"
        log_path = Path(log_dir)
        # self.llm = llm or create_openai_client(log_dir=log_path, llm_name=model_name, temperature=0.01, streaming=True, max_tokens=2000, openai_api_key=openai_api_key)
        # self.basic_llm = basic_llm or create_openai_client(log_dir=log_path, llm_name="gpt-3.5-turbo", temperature=0.0, streaming=True, openai_api_key=openai_api_key)

        self.code_writer = CodeWriter()

        self.max_retries = max_retries
        self.auto_mode = auto_mode
        self.callback = callback

        self.message_history = []
        self.file_context = []
        self.updated_files = []

        if verify_code:
            self.verifier = CodeVerifier(repository=self.repository, test_tool=test_tool, language=language,
                                         callback=callback)
        else:
            self.verifier = None

        self.debug_mode = debug_mode
        self.file_context: List[FileItem] = []

        self.filter_context = False

    def write_code(self, request: WriteCodeRequest) -> WriteCodeResponse:
        return self.run_function("write_code", request.dict())

    def get_project_info(self, request: ProjectInfoRequest) -> ProjectInfoResponse:
        return self.run_function("project_info", request.dict())

    def find_files(self, request: FindFilesRequest) -> FindFilesResponse:
        return self.run_function("find_files", request.dict())

    def read_file(self, request: ReadFileRequest) -> ReadFileResponse:
        return self.run_function("read_file", request.dict())

    def run(self, message: Message) -> List[Message]:
        file_items = message.find_items_by_type(item_type="file")
        for file_item in file_items:
            if not file_item.content and self.repository:
                logger.debug(f"Get current file content for {file_item.file_path}")
                content = self.repository.get_file_content(file_path=file_item.file_path)
                if content:
                    file_item.content = content
                elif file_item.new:
                    file_item.content = ""
                else:
                    raise Exception(f"File {file_item.file_path} not found in repository.")

        if self.callback:
            self.callback.display_message(message)

        return self._run(message)

    def _run(self, incoming_message: Message) -> List[Message]:
        outgoing_messages = self.code_writer.execute(incoming_messages=[incoming_message])
        outgoing_messages.extend(self.verify(messages=[incoming_message] + outgoing_messages))
        return outgoing_messages

    def verify(self, messages: List[Message], retry: int = 0, last_run: int = 0) -> [Message]:
        if not self.verifier:
            return []

        updated_files = dict()

        for message in messages:
            for item in message.items:
                if isinstance(item, UpdatedFileItem) and not item.invalid:
                    updated_files[item.file_path] = item

        if not updated_files:
            # TODO: Handle if no files where updated in last run?
            return []

        file_items = []
        for file_item in updated_files.values():
            if self.repository:
                content = self.repository.get_file_content(file_path=file_item.file_path)
            else:
                content = file_item.content

            file_items.append(FileItem(file_path=file_item.file_path,
                                       content=content,
                                       invalid=file_item.invalid))

        outgoing_messages = []

        logger.info(f"Updated files, verifying...")
        verification_message = self.verifier.execute()
        if self.callback:
            self.callback.display_message(verification_message)
        outgoing_messages.append(verification_message)

        failures = verification_message.find_items_by_type("verification_failure")
        if failures:
            if retry < self.max_retries or len(failures) < last_run:
                verification_message.items.extend(file_items)

                retry += 1
                incoming_messages = self.make_summary(messages)

                logger.info(
                    f"{len(failures)} verifications failed (last run {last_run}, retrying ({retry}/{self.max_retries})...")
                incoming_messages.append(verification_message)
                response_messages = self.test_fix_writer.execute(incoming_messages=incoming_messages)
                return self.verify(messages=messages + [verification_message] + response_messages,
                                   retry=retry,
                                   last_run=len(failures))
            else:
                logger.info(f"Verification failed, giving up...")

        return outgoing_messages

    def make_summary(self, messages: List[Message]) -> List[Message]:
        summarized_messages = []
        sys_prompt = """Make a short summary of the provided message."""

        for message in messages:
            if message.role == "Human":
                text_items = message.find_items_by_type("text")
                summarized_messages.append(Message(sender=message.role, items=text_items))
            else:
                if not message.summary and self.basic_llm:
                    message.summary, stats = self.basic_llm.generate(sys_prompt, messages=[message])
                    logger.debug(f"Created summary {stats.json}")
                if message.summary:
                    summarized_messages.append(Message(sender=message.role, items=[TextItem(text=message.summary)]))

        return summarized_messages

    def create_branch(self, request: CreateBranchRequest) -> BaseResponse:
        branch_name = request.branch_name
        try:
            self.repository.create_branch(branch_name)
        except Exception as e:
            return BaseResponse(success=False, error=f"Failed to create branch {branch_name}: {e}")

        try:
            self.repository.checkout(branch_name)
        except Exception as e:
            logger.warning(f"Failed to checkout branch {branch_name}: {e}")
            return BaseResponse(success=False, error=f"Failed to checkout branch {branch_name}: {e}")

        return BaseResponse(success=True)

    def discard_changes(self, file_paths: List[str] = None) -> BaseResponse:
        try:
            if file_paths:
                self.repository.discard_files(file_paths=file_paths)
            else:
                self.repository.discard_all_files()
        except Exception as e:
            return BaseResponse(success=False, error=f"Failed to discard changes for {file_paths}: {e}")

        return BaseResponse(success=True)


    def get_definitions(self) -> List[dict]:
        definitions = []
        definitions.append(self._create_function_definition("get_project_info", "Get project info", ProjectInfoRequest.schema()["properties"]))
        definitions.append(self._create_function_definition("find_files", "Find files", FindFilesRequest.schema()["properties"]))
        definitions.append(self._create_function_definition("read_file", "Read file", ReadFileRequest.schema()["properties"]))

        return None

    def _create_function_definition(self, name: str, description: str, properties: dict) -> dict:
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": properties,
            },
        }

    def get_file_context(self):
        files = [file.file_path for file in self.file_context]
        files.sort()
        return files

    def add_file_to_context(self, file_path):
        content = self.repository.get_file_content(file_path=file_path)
        if content:
            self.file_context.append(FileItem(file_path=file_path, content=content))

    def remove_file_from_context(self, file_path):
        self.file_context = [file for file in self.file_context if file.file_path != file_path]

    def get_file_context_tokens(self):
        tokens = [count_tokens(file.content) for file in self.file_context]
        return sum(tokens)
