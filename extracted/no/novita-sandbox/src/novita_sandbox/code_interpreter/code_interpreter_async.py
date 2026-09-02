import logging
import httpx

from typing import Optional, Dict, overload, Union, Literal, List
from httpx import AsyncClient
from novita_sandbox.core.api.client.types import UNSET
from novita_sandbox.core.connection_config import ApiParams
from typing_extensions import Self, Unpack

from novita_sandbox.core import (
    AsyncSandbox as BaseAsyncSandbox,
    InvalidArgumentException,
)

from .constants import (
    DEFAULT_TEMPLATE,
    JUPYTER_PORT,
    DEFAULT_TIMEOUT,
)
from .models import (
    Execution,
    ExecutionError,
    Context,
    Result,
    aextract_exception,
    parse_output,
    OutputHandler,
    OutputMessage,
)
from .exceptions import (
    format_execution_timeout_error,
    format_request_timeout_error,
)

logger = logging.getLogger(__name__)

class AsyncSandbox(BaseAsyncSandbox):
    """
    Novita Agent Sandbox is a secure and isolated cloud environment.

    The sandbox allows you to:
    - Access Linux OS
    - Create, list, and delete files and directories
    - Run commands
    - Run isolated code
    - Access the internet

    Check docs [here](https://novita.ai/docs/guides/sandbox-overview).

    Use the `AsyncSandbox.create()` to create a new sandbox.

    Example:
    ```python
    from novita_sandbox.code_interpreter import AsyncSandbox
    sandbox = await AsyncSandbox.create()
    ```
    """

    default_template = DEFAULT_TEMPLATE

    @classmethod
    async def create(
        cls,
        template: Optional[str] = None,
        timeout: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        envs: Optional[Dict[str, str]] = None,
        secure: Optional[bool] = None,
        auto_pause: Optional[bool] = None,
        node_id: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        return await super().create(
            template=template,
            timeout=timeout,
            metadata=metadata,
            envs=envs,
            secure=secure,
            auto_pause=auto_pause,
            node_id=node_id,
            **opts,
        )

    @classmethod
    async def _cls_connect_sandbox(
        cls,
        sandbox_id: str,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        return await super()._cls_connect_sandbox(
            sandbox_id,
            timeout=timeout,
            **opts,
        )

    @property
    def _jupyter_url(self) -> str:
        return f"{'http' if self.connection_config.debug else 'https'}://{self.get_host(JUPYTER_PORT)}"

    @property
    def _client(self) -> AsyncClient:
        return AsyncClient(transport=self._transport)

    @property
    def _jupyter_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self._envd_access_token is not UNSET and self._envd_access_token is not None:
            headers["X-Access-Token"] = self._envd_access_token
        if self.traffic_access_token:
            headers["E2B-Traffic-Access-Token"] = self.traffic_access_token
        return headers

    @overload
    async def run_code(
        self,
        code: str,
        language: Union[Literal["python"], None] = None,
        on_stdout: Optional[OutputHandler[OutputMessage]] = None,
        on_stderr: Optional[OutputHandler[OutputMessage]] = None,
        on_result: Optional[OutputHandler[Result]] = None,
        on_error: Optional[OutputHandler[ExecutionError]] = None,
        envs: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        request_timeout: Optional[float] = None,
    ) -> Execution:
        """
        Runs the code as Python.

        Specify the `language` or `context` option to run the code as a different language or in a different `Context`.

        You can reference previously defined variables, imports, and functions in the code.

        :param code: Code to execute
        :param language: Language to use for code execution. If not defined, the default Python context is used.
        :param on_stdout: Callback for stdout messages
        :param on_stderr: Callback for stderr messages
        :param on_result: Callback for the `Result` object
        :param on_error: Callback for the `ExecutionError` object
        :param envs: Custom environment variables
        :param timeout: Timeout for the code execution in **seconds**
        :param request_timeout: Timeout for the request in **seconds**

        :return: `Execution` result object
        """
        ...

    @overload
    async def run_code(
        self,
        code: str,
        language: Optional[str] = None,
        on_stdout: Optional[OutputHandler[OutputMessage]] = None,
        on_stderr: Optional[OutputHandler[OutputMessage]] = None,
        on_result: Optional[OutputHandler[Result]] = None,
        on_error: Optional[OutputHandler[ExecutionError]] = None,
        envs: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        request_timeout: Optional[float] = None,
    ) -> Execution:
        """
        Runs the code for the specified language.

        Specify the `language` or `context` option to run the code as a different language or in a different `Context`.
        If no language is specified, Python is used.

        You can reference previously defined variables, imports, and functions in the code.

        :param code: Code to execute
        :param language: Language to use for code execution. If not defined, the default Python context is used.
        :param on_stdout: Callback for stdout messages
        :param on_stderr: Callback for stderr messages
        :param on_result: Callback for the `Result` object
        :param on_error: Callback for the `ExecutionError` object
        :param envs: Custom environment variables
        :param timeout: Timeout for the code execution in **seconds**
        :param request_timeout: Timeout for the request in **seconds**

        :return: `Execution` result object
        """
        ...

    @overload
    async def run_code(
        self,
        code: str,
        context: Optional[Context] = None,
        on_stdout: Optional[OutputHandler[OutputMessage]] = None,
        on_stderr: Optional[OutputHandler[OutputMessage]] = None,
        on_result: Optional[OutputHandler[Result]] = None,
        on_error: Optional[OutputHandler[ExecutionError]] = None,
        envs: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        request_timeout: Optional[float] = None,
    ) -> Execution:
        """
        Runs the code in the specified context, if not specified, the default context is used.

        Specify the `language` or `context` option to run the code as a different language or in a different `Context`.

        You can reference previously defined variables, imports, and functions in the code.

        :param code: Code to execute
        :param context: Concrete context to run the code in. If not specified, the default context for the language is used. It's mutually exclusive with the language.
        :param on_stdout: Callback for stdout messages
        :param on_stderr: Callback for stderr messages
        :param on_result: Callback for the `Result` object
        :param on_error: Callback for the `ExecutionError` object
        :param envs: Custom environment variables
        :param timeout: Timeout for the code execution in **seconds**
        :param request_timeout: Timeout for the request in **seconds**

        :return: `Execution` result object
        """
        ...

    async def run_code(
        self,
        code: str,
        language: Optional[str] = None,
        context: Optional[Context] = None,
        on_stdout: Optional[OutputHandler[OutputMessage]] = None,
        on_stderr: Optional[OutputHandler[OutputMessage]] = None,
        on_result: Optional[OutputHandler[Result]] = None,
        on_error: Optional[OutputHandler[ExecutionError]] = None,
        envs: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        request_timeout: Optional[float] = None,
    ) -> Execution:
        logger.debug(f"Executing code {code}")

        if context and language:
            raise InvalidArgumentException(
                "You can provide context or language, but not both at the same time."
            )

        timeout = None if timeout == 0 else (timeout or DEFAULT_TIMEOUT)
        request_timeout = request_timeout or self.connection_config.request_timeout
        context_id = context.id if context else None

        try:
            async with self._client.stream(
                "POST",
                f"{self._jupyter_url}/execute",
                json={
                    "code": code,
                    "context_id": context_id,
                    "language": language,
                    "env_vars": envs,
                },
                headers=self._jupyter_headers,
                timeout=(request_timeout, timeout, request_timeout, request_timeout),
            ) as response:

                err = await aextract_exception(response)
                if err:
                    raise err

                execution = Execution()

                async for line in response.aiter_lines():
                    parse_output(
                        execution,
                        line,
                        on_stdout=on_stdout,
                        on_stderr=on_stderr,
                        on_result=on_result,
                        on_error=on_error,
                    )

                return execution
        except httpx.ReadTimeout:
            raise format_execution_timeout_error()
        except httpx.TimeoutException:
            raise format_request_timeout_error()

    async def create_code_context(
        self,
        cwd: Optional[str] = None,
        language: Optional[str] = None,
        request_timeout: Optional[float] = None,
    ) -> Context:
        """
        Creates a new context to run code in.

        :param cwd: Set the current working directory for the context, defaults to `/home/user`
        :param language: Language of the context. If not specified, defaults to Python
        :param request_timeout: Timeout for the request in **milliseconds**

        :return: Context object
        """
        logger.debug(f"Creating new {language} context")

        data = {}
        if language:
            data["language"] = language
        if cwd:
            data["cwd"] = cwd

        try:
            response = await self._client.post(
                f"{self._jupyter_url}/contexts",
                headers=self._jupyter_headers,
                json=data,
                timeout=request_timeout or self.connection_config.request_timeout,
            )

            err = await aextract_exception(response)
            if err:
                raise err

            data = response.json()
            return Context.from_json(data)
        except httpx.TimeoutException:
            raise format_request_timeout_error()

    async def list_code_contexts(
        self,
    ) -> List[Context]:
        """
        Lists all code execution contexts in the sandbox.

        :return: List of context objects
        """
        logger.debug("Listing code contexts")

        try:
            response = await self._client.get(
                f"{self._jupyter_url}/contexts",
                headers=self._jupyter_headers,
                timeout=self.connection_config.request_timeout,
            )

            err = await aextract_exception(response)
            if err:
                raise err

            data = response.json()
            contexts = data if isinstance(data, list) else data.get("contexts", [])
            return [Context.from_json(context) for context in contexts]
        except httpx.TimeoutException:
            raise format_request_timeout_error()

    async def remove_code_context(
        self,
        context: Union[Context, str],
    ) -> None:
        """
        Removes a code execution context from the sandbox.

        :param context: Context object or context ID to remove
        """
        context_id = context.id if isinstance(context, Context) else context
        logger.debug(f"Removing code context {context_id}")

        try:
            response = await self._client.delete(
                f"{self._jupyter_url}/contexts/{context_id}",
                headers=self._jupyter_headers,
                timeout=self.connection_config.request_timeout,
            )

            err = await aextract_exception(response)
            if err:
                raise err
        except httpx.TimeoutException:
            raise format_request_timeout_error()

    async def restart_code_context(
        self,
        context: Union[Context, str],
    ) -> None:
        """
        Restarts a code execution context in the sandbox.

        :param context: Context object or context ID to restart
        :return: None
        """
        context_id = context.id if isinstance(context, Context) else context
        logger.debug(f"Restarting code context {context_id}")

        try:
            response = await self._client.post(
                f"{self._jupyter_url}/contexts/{context_id}/restart",
                headers=self._jupyter_headers,
                timeout=self.connection_config.request_timeout,
            )

            err = await aextract_exception(response)
            if err:
                raise err
        except httpx.TimeoutException:
            raise format_request_timeout_error()

    async def delete_code_context(
        self,
        context: Union[Context, str],
    ) -> None:
        """
        Deletes a code execution context from the sandbox.

        Alias for `remove_code_context`.

        :param context: Context object or context ID to delete
        """
        return await self.remove_code_context(context)
