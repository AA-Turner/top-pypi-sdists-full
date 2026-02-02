#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/12/2 12:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.schemas.video_types import SoraVideoRequest, Video

BASE_URL = "https://api.moark.com/v1"


class Tasks(object):

    def __init__(self, base_url: Optional[str] = None, api_key: str = None):
        base_url = base_url or BASE_URL
        api_key = api_key or os.getenv("GITEE_API_KEY")
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def create(self, request: SoraVideoRequest):
        payload = request.model_dump(exclude_none=True)

        ###
        payload['fps'] = 24
        payload['num_frames'] = int(request.seconds or 5) * 24

        logany(payload)

        response = await self.client.post(
            "/async/videos/generations",
            body=payload,
            cast_to=object
        )
        response.pop('urls', None)
        return response

    async def get(self, task_id: str):
        response = await self.client.get(
            f"/task/{task_id}",
            cast_to=object
        )
        response.pop('urls', None)
        """
        {'completed_at': 1764649848058,
 'created_at': 1764649799871,
 'output': {'file_url': 'https://gitee-ai.su.bcebos.com/serverless-api/2025-12-02/YBPDHH4CF7AA7NL4R7KTOVE1ZDGFDN5I.mp4?authorization=bce-auth-v1%2FALTAKZc1TWR1oEpkHMlwBs5YXU%2F2025-12-02T04%3A30%3A47Z%2F604800%2F%2Fba79eabb9d46bebbcf212ce0bffd54bad9c31f0f8e8180d06f54018069426d50'},
 'started_at': 1764649800184,
 'status': 'success',
 'task_id': 'YBPDHH4CF7AA7NL4R7KTOVE1ZDGFDN5I'}
        """
        video = Video(**response)

        video.video_url = (response.get("output") or {}).get("file_url")

        return video


if __name__ == '__main__':
    data = {
        "prompt": "年轻的中国女性穿着传统红色古装，红色纱布轻轻遮盖在头上，营造出一种朦胧美感。她轻轻撩起自己头上的红纱盖头，脸上带着温柔的微笑。她的眼睛大而明亮，眉心有一粒小红点，脸部白皙细腻。她黑色长发梳成古典发型，戴着金色和红色相间的耳环。特写镜头，焦段中等，浅景深使人物动作和面部细节更加突出，背景模糊，色调温暖柔和，整体构图细腻精致，具有浓厚的传统文化氛围。",
        "model": "HunyuanVideo-1.5",
        "aspect_ratio": "16:9",
        "negative_prompt": "指导模型避免生成所描述的内容。",
        "num_inferenece_steps": 4,
        "num_frames": 81,
        "fps": 16
    }

    # data = {
    #     "prompt": "年轻的中国女性穿着传统红色古装，红色纱布轻轻遮盖在头上，营造出一种朦胧美感。她轻轻撩起自己头上的红纱盖头，脸上带着温柔的微笑。她的眼睛大而明亮，眉心有一粒小红点，脸部白皙细腻。她黑色长发梳成古典发型，戴着金色和红色相间的耳环。特写镜头，焦段中等，浅景深使人物动作和面部细节更加突出，背景模糊，色调温暖柔和，整体构图细腻精致，具有浓厚的传统文化氛围。",
    #     "model": "LongCat-Video",
    #     "mode": "t2v",
    #     "size": "832x480",
    #     "duration": 5,
    # }
    request = SoraVideoRequest(**data)
    # request.prompt = "一个裸体女人"

    logger.info(request)

    arun(Tasks().create(request))

    # task_id = "YBPDHH4CF7AA7NL4R7KTOVE1ZDGFDN5I"
    # task_id = "EWQPOYTNVJ3MDFSM1HYI4N03A7E73TSG"
    #
    # arun(Tasks().get(task_id))

"""

	"num_frames": 81,
	取值范围：支持 [29, 289] 区间内所有满足 25 + 4n 格式的整数值，其中 n 为正整数。
	
		"fps": 16
		
		# 24
"""
