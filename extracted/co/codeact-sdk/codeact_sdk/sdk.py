"""
CodeAct SDK - 脚本侧 IPC 通信封装（异步版本）。

在 CodeAct 脚本中使用此 SDK 与 Runtime 通信，发起工具调用、LLM 调用并提交执行结果。

使用方式：
    import asyncio
    from codeact_sdk import CodeActSDK

    async def main():
        sdk = CodeActSDK()
        # schema_version 由 main agent 在生成脚本时注入
        result = await sdk.call_tool("echo_tool", {"message": "hello"}, schema_version="v1_xxx")
        await sdk.submit_result(status="success", data={"output": result})

    asyncio.run(main())

并发调用多个工具：
    results = await asyncio.gather(
        sdk.call_tool("tool_a", {"key": "val_a"}, schema_version="v1_xxx"),
        sdk.call_tool("tool_b", {"key": "val_b"}, schema_version="v1_xxx"),
    )

LLM 调用（结构化输出）：
    from pydantic import BaseModel

    class SearchTerms(BaseModel):
        terms: list[str]
        reasoning: str

    result = await sdk.call_llm(
        messages=[{"role": "user", "content": "生成搜索词"}],
        response_format=SearchTerms,
    )
    print(result.terms)
"""

import base64
import inspect
import json
import os
import uuid
import zlib

import aiohttp
from typing import Any, Dict, Optional, Type, Union

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = None


class LLMError(Exception):
    """LLM 调用失败时抛出的异常"""
    pass


class ToolError(Exception):
    """工具调用失败时抛出的异常"""
    pass


class Artifact:
    """脚本产出附件"""

    def __init__(self, type: str, path: str, title: str = ""):
        """
        Args:
            type: 附件类型（如 "file"、"image"、"chart"）
            path: 文件绝对路径（如 "/data/output/report.csv"）
            title: 展示标题
        """
        self.type = type
        self.path = path
        self.title = title

    def to_dict(self) -> Dict[str, str]:
        return {"type": self.type, "path": self.path, "title": self.title}


class CodeActSDK:
    """CodeAct 脚本 IPC 通信 SDK（异步版本）"""

    def __init__(self, ipc_url: Optional[str] = None):
        self.ipc_url = ipc_url or os.environ.get('CODEACT_IPC_URL', 'http://127.0.0.1:9999')
        self.task_id = os.environ.get('CODEACT_TASK_ID', 'unknown')
        self.execution_id = os.environ.get('CODEACT_EXECUTION_ID', 'unknown')
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """懒初始化 aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=600),
            )
        return self._session

    async def _close_session(self):
        """关闭 HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _post(self, path: str, data: dict) -> dict:
        """向 IPC server 发送 POST 请求"""
        url = f"{self.ipc_url}{path}"
        session = await self._get_session()
        async with session.post(url, json=data) as resp:
            return await resp.json()

    async def call_tool(
        self,
        tool: str,
        query: Dict[str, Any],
        schema_version: str,
        call_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        调用一个工具并等待结果。

        此调用会阻塞直到 Runtime 回传工具执行结果。
        支持 asyncio.gather 并发调用多个工具。

        Args:
            tool: 工具名称
            query: 工具参数
            schema_version: 生成脚本时获取的 schema 版本号（必填）
            call_id: 调用 ID（可选，自动生成）

        Returns:
            工具调用结果（成功时直接返回 result 内容，失败时抛出 ToolError）
        """
        if call_id is None:
            call_id = str(uuid.uuid4())

        caller_info = self._get_caller_info()

        data = {
            'call_id': call_id,
            'type': 'tool_call',
            'tool': tool,
            'query': query,
            'caller': caller_info,
            'schema_version': schema_version,
        }

        resp = await self._post('/tool_call', data)
        payload = resp.get('payload', resp)
        if not payload.get('success', False):
            raise ToolError(payload.get('error', f'Tool {tool} call failed'))
        return payload.get('result', {})

    async def call_llm(
        self,
        messages: list[dict[str, str]],
        *,
        response_format: Optional[Type["BaseModel"]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Union["BaseModel", str]:
        """
        调用大模型进行推理（脚本暂停 → IPC → Runtime 调用方舟 API → 结果返回 → 脚本恢复）。

        Args:
            messages: OpenAI 格式消息列表，如 [{"role": "user", "content": "..."}]
            response_format: Pydantic BaseModel 类型，用于结构化输出
            model: 指定模型（默认使用平台配置）
            temperature: 生成温度
            max_tokens: 最大 token 数

        Returns:
            - 传入 response_format 时：返回对应的 BaseModel 实例
            - 未传入时：返回 str

        Example:
            class SearchTerms(BaseModel):
                terms: list[str]

            result = await sdk.call_llm(
                messages=[{"role": "user", "content": "生成搜索词"}],
                response_format=SearchTerms,
            )
            print(result.terms)
        """
        schema = None
        if response_format is not None:
            schema = {
                'schema_name': response_format.__name__,
                'schema': response_format.model_json_schema(),
            }

        query = {
            'messages': messages,
            'temperature': temperature,
        }
        if schema is not None:
            query['response_format'] = schema
        if model is not None:
            query['model'] = model
        if max_tokens is not None:
            query['max_tokens'] = max_tokens

        # zlib 压缩 + base64 编码，减少 IPC 传输量
        query_json = json.dumps(query, ensure_ascii=False).encode('utf-8')
        compressed = zlib.compress(query_json)
        query_encoded = base64.b64encode(compressed).decode('ascii')

        call_id = str(uuid.uuid4())
        caller_info = self._get_caller_info()

        data = {
            'call_id': call_id,
            'type': 'tool_call',
            'tool': '__internal__llm_call',
            'query': {'_compressed': query_encoded},
            'caller': caller_info,
        }

        # LLM 调用使用更长的超时
        session = await self._get_session()
        url = f"{self.ipc_url}/tool_call"
        timeout = aiohttp.ClientTimeout(total=1800)
        async with session.post(url, json=data, timeout=timeout) as raw_resp:
            resp = await raw_resp.json()

        payload = resp.get('payload', resp)
        if not payload.get('success', False):
            raise LLMError(payload.get('error', 'LLM call failed'))

        result = payload.get('result', {})
        if not isinstance(result, dict):
            return str(result) if result else ''

        content = result.get('content', '')

        if response_format is not None and result.get('parsed'):
            return response_format.model_validate(result['parsed'])
        return content

    @staticmethod
    def _get_caller_info() -> Dict[str, Any]:
        """获取调用方的上下文信息（文件、行号、函数、进程 ID）"""
        info: Dict[str, Any] = {'pid': os.getpid()}
        # stack: [0]=_get_caller_info, [1]=call_tool, [2]=实际调用方
        frame = inspect.currentframe()
        try:
            caller = frame.f_back.f_back if frame and frame.f_back else None
            if caller:
                info['file'] = caller.f_code.co_filename
                info['line'] = caller.f_lineno
                info['function'] = caller.f_code.co_name
        finally:
            del frame
        return info

    async def submit_result(
        self,
        result_mode: str,
        status: str = "success",
        message: str = "",
        artifacts: Optional[list["Artifact"]] = None,
        data: Optional[Dict[str, Any]] = None,
    ):
        """
        提交脚本最终执行结果。

        Args:
            result_mode: 结果返回模式，控制父 session 的行为。可选值：
                - "notify": 立即触发父 agent 模型调用并回复用户
                - "display_only": 仅展示 message 给用户，不立即触发模型调用
                - "no_reply": 静默写入上下文，不展示也不立即触发模型调用
            status: 执行状态 ("success" / "error")
            message: 给用户展示的结果描述（上屏内容）
            artifacts: 产出附件列表。示例：
                [Artifact(type="file", path="/data/output/report.csv", title="数据报表")]
            data: 附加数据（会作为模型上下文）
        """
        payload = {'status': status, 'message': message, 'result_mode': result_mode}
        if artifacts is not None:
            payload['artifacts'] = [a.to_dict() for a in artifacts]
        if data is not None:
            payload['data'] = data
        try:
            return await self._post('/submit_result', payload)
        finally:
            await self._close_session()
