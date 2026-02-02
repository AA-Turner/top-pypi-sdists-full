#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/6/20 09:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.schemas.openai_types import CompletionRequest


def oneturn2multiturn(messages: Union[List[dict], CompletionRequest], template: Optional[str] = None,
                      ignore_system: bool = True):
    """todo: https://github.com/hiyouga/LLaMA-Factory/blob/e898fabbe3efcd8b44d0e119e7afaed4542a9f39/src/llmtuner/data/template.py#L423-L427

    _register_template(
    name="qwen",
    format_user=StringFormatter(slots=["<|im_start|>user\n{{content}}<|im_end|>\n<|im_start|>assistant\n"]),
    format_system=StringFormatter(slots=["<|im_start|>system\n{{content}}<|im_end|>\n"]),
    format_observation=StringFormatter(slots=["<|im_start|>tool\n{{content}}<|im_end|>\n<|im_start|>assistant\n"]),
    format_separator=EmptyFormatter(slots=["\n"]),
    default_system="You are a helpful assistant.",
    stop_words=["<|im_end|>"],
    replace_eos=True,
)
    :return:
    """
    # from jinja2 import Template, Environment, PackageLoader, FileSystemLoader
    #
    # system_template = Template("<|im_start|>system\n{{content}}<|im_end|>\n")  # .render(content='xxxx')
    # user_template = Template("<|im_start|>user\n{{content}}<|im_end|>\n")  # 最后<|im_start|>assistant\n
    # assistant_template = Template("<|im_start|>assistant\n{{content}}<|im_end|>\n")

    # todo: [{"type": "image_url", "image_url": {"url": ""}}]] 单独处理
    # 混元不是很感冒
    # context = "\n"
    # for message in messages:
    #     role, content = message.get("role"), message.get("content")
    #     context += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    # context += "<|im_start|>assistant\n"
    if isinstance(messages, CompletionRequest):
        messages = messages.messages

    if len(messages) == 1:
        content = messages[0].get("content")
        if isinstance(content, list):
            for c in content:
                if c.get("type") == "text":
                    content = c.get("text", "")
                    break
        return content

    context = "\n"
    for message in messages:
        role = message.get("role")
        content = message.get("content", "")

        if role == "system" and ignore_system:
            continue

        if isinstance(content, list):  # content: {'type': 'text', 'text': ''}
            for c in content:
                if c.get("type") == "text":
                    content = c.get("text", "")
                    break

        context += f"{role}:\n{content}\n\n"

        # logger.debug(context)

    return context


if __name__ == '__main__':
    content = [
        {
            "type": "text",
            "text": """
            # 身份
    你是一个高精度的【视频内容转录员】。

    # 核心任务
    你的唯一任务是：以【时间戳】为单位，逐字逐句、逐个动作地记录视频中的所有视听信息。你必须像法庭书记员一样，做到100%的客观和精确。

    # 输出格式 (必须严格遵守)
    使用以下格式，为每个独立事件创建新的一行：
    [HH:MM:SS] [类别]: [内容]

    # “类别”包括：
    - **[台词]**: 记录人物说的每一句话。如果能识别说话人，格式为 `[台词-人名]`. 如果不能，格式为 `[台词-男/女]`.
    - **[画面]**: 描述场景、环境、人物外貌、表情和关键物品。
    - **[动作]**: 描述人物的所有具体动作。
    - **[音效]**: 记录所有非对话的声音，如(敲门声), (汽车鸣笛)。

    # 绝对禁止
    - 禁止进行任何总结、分析或评论。
    - 禁止使用任何剧本格式。
    - 禁止省略任何细节。
    - 你的所有输出都必须是简体中文。
            """
        },
        {"type": "video_url", "video_url": {
            "url": "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/310cbdaf-3754-461c-a3ff-9ec8005329c9/b813de59-c7d6-4c58-9f0d-0a8a283ca41b_1%20%282%29.mp4?x-oss-security-token=CAISzwJ1q6Ft5B2yfSjIr5nsCI7Qt5tAhKunaFGDilI6QLpppIPvoDz2IHhMenlvAewetvg2nGBT7fkflrN6SJtIXleCZtF94plR7QKoZ73Zocur7LAJksVu3r1e%2F0WpsvXJasDVEfn%2FGJ70GX2m%2BwZ3xbzlD0bAO3WuLZyOj7N%2Bc90TRXPWRDFaBdBQVGAAwY1gQhm3D%2Fu2NQPwiWf9FVdhvhEG6Vly8qOi2MaRmHG85R%2FYsrZN%2BNmgecP%2FNpE3bMwiCYyPsbYoJvab4kl58ANX8ap6tqtA9Arcs8uVa1sruE3ebbqLqoE3dFMgPvhhQPEZtpj6krhxuanUj5Q8SO%2FTtljJOs62Z%2FdDoKOscIvBXr6yRaJvreicfPqb1%2FQnHpLpLAPa1a4HqTQbIAuUI3bCJL8U1AEJVr6kzHkNhYYrssUUla4R5TGOWbJLJyr%2BHN3xuRqAAZjIuAflHa2njQWXjxvTYM83wepsCAQnJw79bVYI%2FDbZWdln2va6OOjJNxwvdbV42mujTd5qofC%2Bb39J0q5fX6w%2FRanfViZwgN0Bd9tLLLzrjMl02ZLDtq14O5yVY2Z0qyJGw7AAy01Hsjn8BmYaWX19LEfLWe6hrq%2FjSnA9JCUfIAA%3D&x-oss-date=20251008T091359Z&x-oss-expires=300&x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-credential=STS.NZYC4dZDa3iLjw2nRoL5EKFDB%2F20251008%2Fap-southeast-1%2Foss%2Faliyun_v4_request&x-oss-signature=96ae6ce2d0e12e73cc709a1855b772ca2dc9f63be10399fbcdfd4d63f8e53e8d"}}
    ]
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "你是数学家"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "1+1"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "2"
                }
            ]
        },

        {
            "role": "user",
            "content": content
        },

    ]

    # print(oneturn2multiturn(messages, ignore_system=False))
    print(oneturn2multiturn(messages, ignore_system=True))
