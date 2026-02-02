#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kolors
# @Time         : 2024/7/25 08:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://huggingface.co/spaces/gokaygokay/KolorsPlusPlus
# https://huggingface.co/spaces/Kwai-Kolors/Kolors-Virtual-Try-On

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.config_utils.lark_utils import get_next_token_for_polling

from meutils.apis.hf.gradio import create_client, handle_file
from meutils.io.files_utils import to_file

FEISHU_URL_HF = "https://xchatllm.feishu.cn/sheets/MekfsfVuohfUf1tsWV0cCvTmn3c?sheet=NlJ2h0"
FEISHU_URL_MODELSCOPE = "https://xchatllm.feishu.cn/sheets/MekfsfVuohfUf1tsWV0cCvTmn3c?sheet=305f17"

CLOTH_IMAGES = [
    "https://oss.ffire.cc/files/x.png",
    "https://s5k.cn/api/v1/studio/Kwai-Kolors/Kolors-Virtual-Try-On/gradio/file=/tmp/gradio/9d1842bb0c1f9dfa52696e3d8a63fa006e158f00/garment1.png",
    "https://s5k.cn/api/v1/studio/Kwai-Kolors/Kolors-Virtual-Try-On/gradio/file=/tmp/gradio/6349e792201f972c10904fa71cef3559bae35b28/10_dress.png"
]


class KolorsTryOnRequest(BaseModel):
    model: str = "kolors-virtual-try-on"
    human_image: str = "https://oss.ffire.cc/files/try-on.png"
    cloth_image: str = Field(default_factory=lambda: np.random.choice(CLOTH_IMAGES))
    seed: int = 0

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.cloth_image == self.human_image:
            self.cloth_image = np.random.choice(CLOTH_IMAGES)


@retrying(max_retries=2, min=3, predicate=lambda r: not r["data"])
async def create(request: KolorsTryOnRequest, endpoint: Optional[str] = None, token: Optional[str] = None):
    logger.debug(request)

    endpoint = endpoint or "https://s5k.cn/api/v1/studio/Kwai-Kolors/Kolors-Virtual-Try-On/gradio/"
    if endpoint.startswith('https://s5k.cn'):
        FEISHU_URL = FEISHU_URL_MODELSCOPE
    else:
        FEISHU_URL = FEISHU_URL_HF

    token = token or await get_next_token_for_polling(FEISHU_URL, from_redis=True)
    logger.info(token)

    try:
        client = await create_client(endpoint, hf_token=token)

        human_image, cloth_image = map(
            handle_file,
            await asyncio.gather(*map(to_file, [request.human_image, request.cloth_image]))
        )
        result = client.predict(
            # person_img=handle_file("tryon.png"),

            person_img=human_image,  # 有oss限制
            garment_img=cloth_image,
            seed=request.seed,
            randomize_seed=True,
            api_name="/tryon"
        )

        logger.debug(result)

        url = result[0]["url"]
        return {
            "data": [{"url": url}]
        }

    except Exception as e:
        logger.error(e)
        return {
            "data": [],
        }


if __name__ == '__main__':
    token = "e3f5804a-869e-460c-9470-946be0624963"
    request = KolorsTryOnRequest(
        # human_image="https://oss.ffire.cc/files/try-on.png",
        # person_image="https://oss.ffire.cc/files/kling_watermark.png",
        # cloth_image='xx'
    )

    print(request)
    with timer():
        arun(create(request))

    # from gradio_client import Client, handle_file
    #
    # client = Client("https://s5k.cn/api/v1/studio/Kwai-Kolors/Kolors-Virtual-Try-On/gradio/", hf_token=token, download_files=False)
    # result = client.predict(
    #     person_img=handle_file(request.person_image),
    #     garment_img=handle_file(request.garment_image),
    #     seed=0,
    #     randomize_seed=True,
    #     api_name="/tryon",
    # )
    # print(result)
