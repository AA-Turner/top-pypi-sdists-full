import logging
import traceback
from typing import Any, Optional

from pydantic import create_model, Field

from .executor.code_executor import CodeExecutor
from .generator.base import CodeGenerator
from ..elitea_base import BaseToolApiWrapper

logger = logging.getLogger(__name__)


class AtlassianToolkit(BaseToolApiWrapper):
    alita: Any = None
    llm: Any = None
    confluence_url: Optional[str] = None
    jira_url: Optional[str] = None
    atlassian_user: Optional[str] = None
    atlassian_password: Optional[str] = None
    atlassian_token: Optional[str] = None

    def generate_code(self, task_to_solve: str, error_trace: str = None) -> str:
        """Generate pandas code using LLM based on the task to solve."""
        code = CodeGenerator(
            llm=self.llm
        ).generate_code(task_to_solve, error_trace)
        return code

    def execute_code(self, code: str) -> str:
        """Execute the generated code and return the result."""
        executor = CodeExecutor()
        return executor.execute_and_return_result(code)

    def generate_code_with_retries(self, query: str) -> Any:
        """Execute the code with retry logic."""
        max_retries = 5
        attempts = 0
        try:
            return self.generate_code(query)
        except Exception as e:
            error_trace = traceback.format_exc()
            while attempts <= max_retries:
                try:
                    return self.generate_code(query, error_trace)
                except Exception as e:
                    attempts += 1
                    if attempts > max_retries:
                        logger.info(
                            f"Maximum retry attempts exceeded. Last error: {e}"
                        )
                        raise
                    logger.info(
                        f"Retrying Code Generation ({attempts}/{max_retries})..."
                    )

    def _get_meta(self) -> str:
        meta_parts = []
        if self.jira_url:
            meta_parts.append(f"Jira URL: {self.jira_url}")
        if self.confluence_url:
            meta_parts.append(f"Confluence URL: {self.confluence_url}")
        if self.atlassian_user:
            meta_parts.append(f"Username: {self.atlassian_user}")
        if self.atlassian_password:
            # This is a sensitive field, so we must redact it
            meta_parts.append(f"Password: {self.atlassian_password}")
        if self.atlassian_token:
            # This is a sensitive field, so we must redact it
            meta_parts.append(f"Token: {self.atlassian_token}")
        return "Metadata: " + ", ".join(meta_parts)

    def process_query(self, query: str) -> str:
        """Analyze and process using user's query"""
        user_request = (f"User's query: {query}.\n"
                        f"{self._get_meta()}")
        code = self.generate_code_with_retries(user_request)
        result = self.execute_code(code)
        return result

    def get_available_tools(self):
        return [
            {
                "name": "process_query",
                "ref": self.process_query,
                "description": self.process_query.__doc__,
                "args_schema": create_model(
                    "ProcessQueryModel",
                    query=(str, Field(description="Task to solve")),
                )
            }
        ]

