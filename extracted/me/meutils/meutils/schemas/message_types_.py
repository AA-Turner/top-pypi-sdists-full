from typing import List, Optional, Union, Dict, Literal
from pydantic import BaseModel

from itertools import groupby


class Url(BaseModel):
    url: str
    detai: str = "auto"


class TextContent(BaseModel):
    type: Literal["text"]
    text: str


class ImageContent(BaseModel):
    type: Literal["image_url"]
    image_url: Url


class VideoContent(BaseModel):
    type: Literal["video_url"]
    video_url: Url


class FileContent(BaseModel):
    type: Literal["file_url"]
    file_url: Url


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: Union[str, List[Union[TextContent, ImageContent, VideoContent, FileContent]]]


class Messages(BaseModel):
    messages: List[Message]

    def get_last_message(self) -> Optional[Message]:
        """获取最后一条消息"""
        return self.messages[-1] if self.messages else None

    def get_messages_by_role(self, role: str) -> List[Message]:
        """获取指定角色的所有消息"""
        return [msg for msg in self.messages if msg.role == role]

    def get_all_file_urls(self) -> List[str]:
        """获取所有文件URL"""
        file_urls = []
        for msg in self.messages:
            if isinstance(msg.content, list):
                for item in msg.content:
                    if isinstance(item, FileContent):
                        file_urls.append(item.file_url.url)
            elif isinstance(msg.content, FileContent):
                file_urls.append(msg.content.file_url.url)
        return file_urls

    def get_conversation_pairs(self) -> List[tuple]:
        """获取对话对（用户问题和助手回答的配对）"""
        pairs = []
        user_msg = None
        for msg in self.messages:
            if msg.role == 'user':
                user_msg = msg
            elif msg.role == 'assistant' and user_msg:
                pairs.append((user_msg, msg))
                user_msg = None
        return pairs

    def get_text_content(self) -> List[str]:
        """获取所有文本内容"""
        texts = []
        for msg in self.messages:
            if isinstance(msg.content, str):
                texts.append(msg.content)
            elif isinstance(msg.content, list):
                for item in msg.content:
                    if isinstance(item, TextContent):
                        texts.append(item.text)
        return texts

    def get_message_at_index(self, index: int) -> Optional[Message]:
        """获取指定索引的消息"""
        try:
            return self.messages[index]
        except IndexError:
            return None

    def get_message_count(self) -> int:
        """获取消息总数"""
        return len(self.messages)

    def get_role_distribution(self) -> Dict[str, int]:
        """获取各角色消息数量分布"""
        return {role: len(list(msgs))
                for role, msgs in groupby(sorted(self.messages, key=lambda x: x.role),
                                          key=lambda x: x.role)}

    def clear_messages(self):
        """清空所有消息"""
        self.messages = []


# 使用示例:
if __name__ == "__main__":
    messages_data = {
        "messages": [
            {
                "role": "system",
                "content": "你是一个文件问答助手"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "这个文件讲了什么？"
                    },
                    {
                        "type": "file_url",
                        "file_url": {
                            "url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf",
                            "detai": "auto"
                        }
                    }
                ]
            },
            {
                "role": "assistant",
                "content": "好的"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "错了 继续回答"
                    }
                ]
            }
        ]
    }

    # 验证数据
    chat_messages = Messages(**messages_data)

    # chat_messages.

    chat_messages.messages[1].content.model_dump()

# 使用示例:
if __name__ == "__main__":
    messages_data = {
        "messages": [
            {
                "role": "system",
                "content": "你是一个文件问答助手"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "这个文件讲了什么？"
                    },
                    {
                        "type": "file_url",
                        "file_url": {
                            "url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf",
                            "detai": "auto"
                        }
                    }
                ]
            },
            {
                "role": "assistant",
                "content": "好的"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "错了 继续回答"
                    }
                ]
            }
        ]
    }

    # 创建实例
    chat = ChatMessages(**messages_data)

    # 使用示例：
    # 获取最后一条消息
    last_message = chat.get_last_message()
    print("最后一条消息:", last_message)

    # 获取所有用户消息
    user_messages = chat.get_messages_by_role('user')
    print("用户消息:", user_messages)

    # 获取所有文件URL
    file_urls = chat.get_all_file_urls()
    print("文件URLs:", file_urls)

    # 获取所有文本内容
    texts = chat.get_text_content()
    print("文本内容:", texts)

    # 获取对话对
    conversation_pairs = chat.get_conversation_pairs()
    print("对话对:", conversation_pairs)

    # 获取指定索引的消息
    message_at_2 = chat.get_message_at_index(2)
    print("索引2的消息:", message_at_2)
