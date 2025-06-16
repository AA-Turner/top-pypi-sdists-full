import base64
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    TypeVar,
    Union,
)

from pydantic import BaseModel

from whiskerrag_types.model.knowledge import Knowledge

T = TypeVar("T", bound=BaseModel)

ContentType = Union[
    str, Dict[str, Any]
]  # dict用于图片输入，格式为{"type": "image", "data": bytes/str}


class BaseLLM(ABC, Generic[T]):
    """基础大语言模型接口，参考LangChain和OpenAI的设计"""

    def __init__(self, knowledge: Knowledge) -> None:
        self.knowledge = knowledge

    @abstractmethod
    async def chat(self, content: Union[str, List[ContentType]], **kwargs: Any) -> T:
        """
        异步聊天方法，类似于LangChain的invoke

        Args:
            content: 输入内容，可以是字符串或包含文本和图片的列表
            **kwargs: 其他参数，如temperature, max_tokens等

        Returns:
            返回模型响应
        """
        pass

    @abstractmethod
    async def stream_chat(
        self, content: Union[str, List[ContentType]], **kwargs: Any
    ) -> AsyncIterator[T]:
        """
        异步流式聊天方法，类似于LangChain的astream

        Args:
            content: 输入内容，可以是字符串或包含文本和图片的列表
            **kwargs: 其他参数，如temperature, max_tokens等

        Yields:
            流式返回模型响应块
        """
        # 这里需要yield而不是pass，但是为了抽象方法，使用以下方式
        if False:  # pragma: no cover
            yield  # pragma: no cover

    def chat_sync(self, content: Union[str, List[ContentType]], **kwargs: Any) -> T:
        """
        同步聊天方法，类似于LangChain的invoke的同步版本

        Args:
            content: 输入内容，可以是字符串或包含文本和图片的列表
            **kwargs: 其他参数，如temperature, max_tokens等

        Returns:
            返回模型响应
        """
        import asyncio

        # 检查是否在事件循环中
        try:
            asyncio.get_running_loop()
            # 如果在事件循环中，创建任务
            import concurrent.futures

            def run_in_thread() -> T:
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(self.chat(content, **kwargs))
                finally:
                    new_loop.close()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result()
        except RuntimeError:
            # 没有运行中的事件循环，可以直接调用
            return asyncio.run(self.chat(content, **kwargs))

    def stream_chat_sync(
        self, content: Union[str, List[ContentType]], **kwargs: Any
    ) -> Iterator[T]:
        """
        同步流式聊天方法，类似于LangChain的stream

        Args:
            content: 输入内容，可以是字符串或包含文本和图片的列表
            **kwargs: 其他参数，如temperature, max_tokens等

        Yields:
            流式返回模型响应块
        """
        import asyncio
        import concurrent.futures

        def run_in_thread() -> List[T]:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:

                async def _run() -> List[T]:
                    results = []
                    async for chunk in self.stream_chat(content, **kwargs):
                        results.append(chunk)
                    return results

                return new_loop.run_until_complete(_run())
            finally:
                new_loop.close()

        # 检查是否在事件循环中
        try:
            asyncio.get_running_loop()
            # 如果在事件循环中，在新线程中运行
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                results = future.result()
        except RuntimeError:
            # 没有运行中的事件循环，可以直接调用
            results = run_in_thread()

        for result in results:
            yield result

    @staticmethod
    def prepare_image_content(
        image_path: Optional[Union[str, Path]] = None,
        image_data: Optional[bytes] = None,
        image_url: Optional[str] = None,
        image_format: str = "auto",
    ) -> Dict[str, str]:
        """
        准备图片内容的辅助方法

        Args:
            image_path: 图片文件路径
            image_data: 图片二进制数据
            image_url: 图片URL
            image_format: 图片格式，auto表示自动检测

        Returns:
            格式化的图片内容字典
        """
        if image_path:
            image_path = Path(image_path)
            with open(image_path, "rb") as f:
                image_data = f.read()
            if image_format == "auto":
                image_format = image_path.suffix.lower().lstrip(".")

        if image_data:
            if isinstance(image_data, bytes):
                image_b64 = base64.b64encode(image_data).decode("utf-8")
            else:
                image_b64 = image_data

            return {
                "type": "image",
                "image_url": f"data:image/{image_format};base64,{image_b64}",
            }
        elif image_url:
            return {"type": "image", "image_url": image_url}
        else:
            raise ValueError("Must provide either image_path, image_data, or image_url")

    @classmethod
    async def sync_health_check(cls) -> bool:
        """
        同步健康检查方法，用于注册时验证

        Returns:
            True表示健康检查通过，False表示失败
        """
        # 默认实现返回True，子类可以重写进行具体检查
        return True
