#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : usage_types
# @Time         : 2025/11/26 23:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from openai.types.completion_usage import CompletionUsage
from openai.types.images_response import UsageInputTokensDetails, Usage as ImageUsage


class Usage(CompletionUsage, ImageUsage):
    # CompletionUsage
    completion_tokens: int = 0
    """Number of tokens in the generated completion."""

    prompt_tokens: int = 0  # text_tokens
    """Number of tokens in the prompt."""

    total_tokens: int = 0
    """Total number of tokens used in the request (prompt + completion)."""

    # ImageUsage
    input_tokens: int = 0
    input_tokens_details: Optional[UsageInputTokensDetails] = None

    output_tokens: int = 0

    # extra
    text_tokens: int = 0
    image_tokens: int = 0

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        # self.prompt_tokens + self.completion_tokens +

        if not self.input_tokens:
            self.input_tokens = self.text_tokens + self.image_tokens

        if not self.input_tokens_details:
            self.input_tokens_details = UsageInputTokensDetails(
                image_tokens=self.image_tokens,
                text_tokens=self.prompt_tokens
            )

        self.prompt_tokens = self.prompt_tokens or self.input_tokens
        self.completion_tokens = self.completion_tokens or self.output_tokens

        self.input_tokens = self.input_tokens or self.prompt_tokens + self.image_tokens
        self.output_tokens = self.output_tokens or self.completion_tokens

        if not self.total_tokens:
            self.total_tokens = self.input_tokens + self.output_tokens


if __name__ == '__main__':
    print(Usage(input_tokens=1, output_tokens=10))
