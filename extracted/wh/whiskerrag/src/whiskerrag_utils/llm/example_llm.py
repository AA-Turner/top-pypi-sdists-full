from typing import Any, AsyncIterator, Dict, List, Union

from openai import BaseModel

from whiskerrag_types.interface.llm_interface import BaseLLM, ContentType
from whiskerrag_types.model.knowledge import Knowledge
from whiskerrag_utils.registry import RegisterTypeEnum, register


class ExampleResponse(BaseModel):
    """示例响应模型"""

    content: str
    model: str = "example-llm"
    usage: Dict[str, int] = {"tokens": 0}


@register(RegisterTypeEnum.LLM, "example", order=1)
class ExampleLLM(BaseLLM[ExampleResponse]):
    """示例LLM实现，用于演示注册系统"""

    def __init__(self, knowledge: Knowledge, model_name: str = "example-llm"):
        super().__init__(knowledge)
        self.model_name = model_name

    async def chat(
        self, content: Union[str, List[ContentType]], **kwargs: Any
    ) -> ExampleResponse:
        """示例聊天实现"""
        if isinstance(content, str):
            text_content = content
        else:
            # 处理混合内容
            text_parts = []
            for item in content:
                if isinstance(item, str):
                    text_parts.append(item)
                elif isinstance(item, dict) and item.get("type") == "image":
                    text_parts.append("[Image detected]")
            text_content = " ".join(text_parts)

        # 模拟响应
        response_text = f"Echo: {text_content}"

        return ExampleResponse(
            content=response_text,
            model=self.model_name,
            usage={"tokens": len(text_content.split())},
        )

    async def stream_chat(
        self, content: Union[str, List[ContentType]], **kwargs: Any
    ) -> AsyncIterator[ExampleResponse]:
        """示例流式聊天实现"""
        response = await self.chat(content, **kwargs)

        # 模拟流式输出，将响应分割为单词
        words = response.content.split()
        for i, word in enumerate(words):
            yield ExampleResponse(
                content=word + (" " if i < len(words) - 1 else ""),
                model=self.model_name,
                usage={"tokens": i + 1},
            )

    @classmethod
    async def sync_health_check(cls) -> bool:
        """健康检查"""
        try:
            from whiskerrag_types.model.knowledge import Knowledge, KnowledgeTypeEnum
            from whiskerrag_types.model.knowledge_source import (
                KnowledgeSourceEnum,
                TextSourceConfig,
            )
            from whiskerrag_types.model.splitter import TextSplitConfig

            test_knowledge = Knowledge(
                space_id="test-space",
                tenant_id="test-tenant",
                knowledge_name="测试知识",
                knowledge_type=KnowledgeTypeEnum.TEXT,
                source_type=KnowledgeSourceEnum.USER_INPUT_TEXT,
                source_config=TextSourceConfig(text="test"),
                split_config=TextSplitConfig(
                    type="text",
                    separators=["\n\n", "\n", " "],
                    is_separator_regex=False,
                    keep_separator=False,
                ),
            )

            instance = cls(test_knowledge)
            test_response = await instance.chat("test")
            return isinstance(test_response, ExampleResponse)
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
