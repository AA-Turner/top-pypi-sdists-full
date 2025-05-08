#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_asr
# @Time         : 2023/11/23 13:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 更多模型

from meutils.pipe import *
from openai import OpenAI

# base_url = 'http://0.0.0.0:8000/v1'
# base_url='http://154.3.0.117:39009/tts/v1'
# base_url="https://openai-dev.chatfire.cn/audio/v1"
# base_url="https://openai.chatfire.cn/audio/v1"
# base_url="https://api.chatfire.cn/v2"

client = OpenAI(
    # base_url=base_url,
    # api_key=os.getenv('OPENAI_API_KEY'),

    # api_key=os.getenv('OPENAI_API_KEY_OPENAI') + "-2738",
    api_key=os.getenv('OPENAI_API_KEY_OPENAI') + "-364",

)

# text = """
# 陕西省，简称“陕”或“秦”，中华人民共和国省级行政区，省会西安，位于中国内陆腹地，黄河中游，东邻山西、河南，西连宁夏、甘肃，南抵四川、重庆、湖北，北接内蒙古，介于东经105°29′—111°15′，北纬31°42′—39°35′之间，总面积205624.3平方千米。 [1] [5]截至2022年11月，陕西省下辖10个地级市（其中省会西安为副省级市）、31个市辖区、7个县级市、69个县。 [121]截至2022年末，陕西省常住人口3956万人。
# """
# # text = "你好哇"*20
# _ = client.audio.speech.create(input=text, model="tts", voice="晓晓")
# _.stream_to_file("hi.mp3")

with timer():
    voice = "晓晓"
    speech_file_path = f"{voice}.mp3"
    response = client.audio.speech.create(
        # input="健身需要注意适度和平衡，过度的锻炼可能会导致身体受伤。因此，进行健身活动前，最好先咨询医生或专业的健身教练，制定一个适合自己的健身计划。一般来说，一周内进行150分钟的适度强度的有氧运动，或者75分钟的高强度有氧运动，加上每周两天的肌肉锻炼，就能达到保持健康的目标。",
        input="健身需要注意适度和平衡，过度的锻炼可能会导致身体受伤",

        model="tts-1",
        voice=voice,
        # voice="54a5170264694bfc8e9ad98df7bd89c3"
    )
    # logger.debug(response)
    response.stream_to_file(speech_file_path)
