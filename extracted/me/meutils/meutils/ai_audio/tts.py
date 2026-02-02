#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tts
# @Time         : 2023/11/3 15:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 增加固定时长的生成

from meutils.pipe import *

import edge_tts


@lru_cache()
def voicesmanager_cls():
    return asyncio.run(edge_tts.VoicesManager.create())


def find_voices(**kwargs: Any):
    """
        find_voices(**{"Locale": "en-US"})
    """
    return voicesmanager_cls().find(**kwargs or {"Locale": "zh-CN"})


# @lru_cache()
async def tts(text, role: str = '云希', filename: Optional[None] = None):
    # https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4
    SUPPORTED_VOICES = {
        "晓晓": "zh-CN-XiaoxiaoNeural",
        "晓伊": "zh-CN-XiaoyiNeural",
        "云健": "zh-CN-YunjianNeural",
        "云希": "zh-CN-YunxiNeural",
        "云夏": "zh-CN-YunxiaNeural",
        "云扬": "zh-CN-YunyangNeural",
        "晓北辽宁": "zh-CN-liaoning-XiaobeiNeural",
        "陕西晓妮": "zh-CN-shaanxi-XiaoniNeural",
        "en-US-AriaNeural": "en-US-AriaNeural",
        "en-US-AnaNeural": "en-US-AnaNeural",
        "en-US-ChristopherNeural": "en-US-ChristopherNeural",
        "en-US-EricNeural": "en-US-EricNeural",
        "en-US-GuyNeural": "en-US-GuyNeural",
        "en-US-JennyNeural": "en-US-JennyNeural",
        "en-US-MichelleNeural": "en-US-MichelleNeural",
        "en-US-RogerNeural": "en-US-RogerNeural",
        "en-US-SteffanNeural": "en-US-SteffanNeural"
    }

    # rate: str = "+0%", 加速
    communicate = edge_tts.Communicate(text or "文本为空", voice=SUPPORTED_VOICES.get(role, '陕西晓妮'))

    filename = filename or f"{str(datetime.datetime.now())[:19]} {text[:5]}.mp3"

    await communicate.save(filename)

    return filename


if __name__ == '__main__':
    import asyncio


    def main(text='不知道'):
        # import nest_asyncio
        # nest_asyncio.apply()

        # asyncio.run(tts(text))
        cls = edge_tts.VoicesManager.create()
        asyncio.run(cls)
        return edge_tts.VoicesManager.find(**{"Locale": "zh-CN"})


    #
    #
    # main(text="不知道" * 66)
    # main(text="不知道" * 66)
    #
    # main("不知道11" * 10)
    # main("不知道22" * 10)

    vs = find_voices(**{"Locale": "en-US"})

    print({v['ShortName']: v['ShortName'] for v in vs})
