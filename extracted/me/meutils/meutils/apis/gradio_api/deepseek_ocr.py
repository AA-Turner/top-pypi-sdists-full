# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/8/7 09:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.schemas.openai_types import CompletionRequest
from meutils.io.files_utils import to_file

from meutils.apis.gradio_api.utils import create_client, handle_file


class Completions(object):

    def __init__(
            self,
            base_url: Optional[str] = None,
            api_key: Optional[str] = None,
    ):

        self.api_key = api_key

    async def create(self, request: CompletionRequest):

        if not (image_urls := request.last_urls.get("image_url")):
            yield "# Image is required"
            return

        if hasattr(request, "task_type"):
            task_type = request.task_type
        else:
            task_type = "Free OCR"

        image_url = image_urls[0]
        if image_url.startswith("http"):
            image = handle_file(image_url)
        else:
            image = await to_file(image_url)
            image = handle_file(image)

        for i in range(2):
            try:

                client = await create_client(request.model, hf_token=self.api_key)

                result = client.predict(
                    image=image,
                    model_size="Gundam (Recommended)",
                    # task_type="Convert to Markdown",
                    # task_type Literal['Free OCR', 'Convert to Markdown'] Default: "Convert to Markdown"
                    # task_type="Free OCR",
                    task_type=task_type,
                    api_name="/process_image",
                )
                # task_type = "📄 Convert to Markdown",
                # ref_text = "Hello!!",
                # api_name = "/process_ocr_task"
                _, _, text = result

                yield text
                break
            except Exception as e:
                logger.error(e)
                # proxy = await get_one_proxy()
                # httpx_kwargs = {
                #     "proxy": proxy,
                # }
                if i == 1:
                    raise e


if __name__ == '__main__':
    model = "khang119966/DeepSeek-OCR-DEMO"
    model = "axiilay/DeepSeek-OCR-Demo"

    request = CompletionRequest(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://s3.ffire.cc/files/pdf_to_markdown.jpg",
                        }
                    }
                ]
            }
        ],
        task_type="Convert to Markdown",
    )

    arun(Completions().create(request))
