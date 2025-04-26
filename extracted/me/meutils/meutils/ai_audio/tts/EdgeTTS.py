#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tts
# @Time         : 2023/11/3 15:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 增加固定时长的生成
# https://github.com/rany2/edge-tts/blob/master/examples/streaming_with_subtitles.py

import edge_tts

from meutils.pipe import *
from meutils.decorators.retry import retrying


class EdgeTTS(object):

    def __init__(self):
        pass

    def create(
            self,
            text: Union[str, List[str]],
            role: str = '云希',
            rate: float = 0,
            volume: float = 0,
            filename: Optional[None] = None,
            **kwargs
    ):
        """ todo：增加字幕合成，增加 多进程，多线程
            for i, srtitem in enumerate(tqdm(pysrt.open('subtitle.srt'))):
                create(srtitem.text, filename=f"wav/{i:0>6}.wav")
        """
        if isinstance(text, str):
            text = [text]

        acreate = partial(self.acreate, role=role, rate=rate, volume=volume, filename=filename)

        return text | xmap(acreate) | xAsyncio

    @alru_cache
    async def acreate(
            self,
            text: str,
            role: str = '云希',
            rate: float = 0,
            volume: float = 0,
            filename: Optional[None] = None,
    ):
        voices = (await edge_tts.VoicesManager.create()).find(**{'ShortName': role}) or [{}]  # todo: 优化
        voice = voices[0].get('ShortName', 'zh-CN-YunxiNeural')

        rate = f"{'+' if rate >= 0 else ''}{rate}%"
        volume = f"{'+' if volume >= 0 else ''}{volume}%"

        communicate = edge_tts.Communicate(text, voice=voice, rate=rate, volume=volume)  # todo: 文件流

        filename = filename or f"{time.time()}.mp3"  # f"{str(datetime.datetime.now())[:19]}.mp3"
        await communicate.save(filename)

        return filename

    @retrying()
    async def stream_acreate(
            self,
            text: str,
            voice: str = '云希',  # "晓晓", "晓伊", "云健", "云希", "云夏", "云扬", "辽宁晓北", "陕西晓妮"
            rate: float = 0,
            volume: float = 0,
            **kwargs
    ):
        voices = {
            '晓晓': 'zh-CN-XiaoxiaoNeural', '女声': 'zh-CN-XiaoxiaoNeural',
            '晓伊': 'zh-CN-XiaoyiNeural',
            '云健': 'zh-CN-YunjianNeural',
            '云希': 'zh-CN-YunxiNeural', '男声': 'zh-CN-YunxiNeural',
            '云夏': 'zh-CN-YunxiaNeural',
            '云扬': 'zh-CN-YunyangNeural',
            '辽宁晓北': 'zh-CN-liaoning-XiaobeiNeural',
            '陕西晓妮': 'zh-CN-shaanxi-XiaoniNeural',
        }
        voice = voices.get(voice, 'zh-CN-YunxiNeural')

        rate = f"{'+' if rate >= 0 else ''}{rate}%"
        volume = f"{'+' if volume >= 0 else ''}{volume}%"

        communicate = edge_tts.Communicate(text, voice=voice, rate=rate, volume=volume)
        async for chunk in communicate.stream():  # 构建生成器，流式输出， todo: 字幕结构体
            # {'type': 'WordBoundary', 'offset': 1000000, 'duration': 6750000, 'text': '你好'} # 断句字幕
            # https://github.com/rany2/edge-tts/blob/master/examples/streaming_with_subtitles.py
            # if chunk.get('type') == 'WordBoundary':
            #     logger.debug(chunk)
            #     continue
            if chunk.get('type') == "audio":
                yield chunk["data"]

    @staticmethod
    @lru_cache
    def find_voices(**kwargs: Any):  # @alru_cache
        """https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4
            find_voices(**{"Locale": "en-US"})
            find_voices(**{'ShortName': 'zh-CN-XiaoxiaoNeural'})
        """
        return asyncio.run(edge_tts.VoicesManager.create()).find(**kwargs or {"Locale": "zh-CN"})

    async def acreate_for_openai(
            self,
            input: str,
            model: str = 'edge-tts',
            voice: str = '云希',  # 男声 女声
            **kwargs
    ):
        data = {
            "text": input,
            "voice": voice,
        }
        return self.stream_acreate(**data)


if __name__ == '__main__':
    # print(EdgeTTS().create(['不知道'] * 10))

    cls = EdgeTTS()
    # cls.create('不知道')
    # cls.create('不知道')

    from meutils.async_utils import async2sync_generator

    input = "健身需要注意适度和平衡，过度的锻炼可能会导致身体受伤。因此，进行健身活动前，最好先咨询医生或专业的健身教练，制定一个适合自己的健身计划。一般来说，一周内进行150分钟的适度强度的有氧运动，或者75分钟的高强度有氧运动，加上每周两天的肌肉锻炼，就能达到保持健康的目标。"

    text = """
    陕西省，简称“陕”或“秦”，中华人民共和国省级行政区，省会西安，位于中国内陆腹地，黄河中游，东邻山西、河南，西连宁夏、甘肃，南抵四川、重庆、湖北，北接内蒙古，介于东经105°29′—111°15′，北纬31°42′—39°35′之间，总面积205624.3平方千米。 [1] [5]截至2022年11月，陕西省下辖10个地级市（其中省会西安为副省级市）、31个市辖区、7个县级市、69个县。 [121]截至2022年末，陕西省常住人口3956万人。
    """

    print(cls.find_voices(Locale="zh-CN"))
    # for i in async2sync_generator(cls.stream_acreate(input)):
        # print(i)

    # EDGE_TTS_DICT = {
    #     "用英语": "en-US-AriaNeural",
    #     "用日语": "ja-JP-NanamiNeural",
    #     "用法语": "fr-BE-CharlineNeural",
    #     "用韩语": "ko-KR-SunHiNeural",
    #     "用德语": "de-AT-JonasNeural",
    #     # add more here
    # }

    arun(cls.acreate(input))
