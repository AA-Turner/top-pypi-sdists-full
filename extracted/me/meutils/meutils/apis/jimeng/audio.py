#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tts
# @Time         : 2025/5/13 10:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.io.files_utils import to_bytes, to_url
from meutils.schemas.openai_types import TTSRequest
from meutils.schemas.jimeng_types import BASE_URL

VOICE_MAPPING = {
    # 带情绪
    "柔美女友": "7382552865023201819",
    # "happy", "angry", "fear", "surprised", "coldness", "disgust", "excited", "hate"
    "妩媚女生": "7459778019725414962",  # "happy", "angry", "fear", "surprise"
    "京腔小爷": "7382048889659986458",  # "joy", "angry", "surprise", "disgust"

    # 角色演绎
    "猴哥": "7236944659547689531",
    "熊二": "7170964808357909005",
    "如来佛祖": "7327220560335737363",
    "咆哮哥": "7265204498308534840",
    "四郎": "7170966598528799263",
    "懒小羊": "7236944067072889405",
    "TVB女声": "7145775430832755230",
    "动漫小新": "6855162047320035854",
    "紫薇": "7281175385486660155",
    "黛玉": "7203252693555483196",
    "顾姐": "7170966542610338318",
    "动漫海绵": "6954271730848240136",
    "云龙哥": "7298191949306008102",
    "容嬷嬷": "7278285365335560762",
    "华妃": "7360900412167164470",

    # 方言
    "河南小哥": "7382049051304268339",
    "湾区大叔": "7382049147311886874",
    "广西老表": "7382049000242811442",
    "山东小哥": "7382048947646239259",
    "长沙妹坨": "7376856724151472679",
    "樱花小哥": "7275251697721545277",
    "上海阿姨": "7270784654867698237",
    "京腔": "7246701228736909879",
    "港普男声": "7236947484650508859",
    "天津小哥": "7023305056589976095",
    "西安掌柜": "7008044050917888548",
    "台湾女生": "6966423537611444767",
    "东北老铁": "6912251359693640199",
    "粤语男声": "7023302069004014117",
    "重庆小伙": "6939395229950677534",

    # 女青年
    "魅力姐姐": "7382879492752019995",
    "高冷御姐": "7382878375473320475",
    "魅力女友": "7382839113059144229",
    "耿直女声": "7367236342641594890",
    "活泼女声": "7366933865698431515",
    "随性女声": "7350942233593385508",
    "知性女声": "7023300712998113823",
    "温柔淑女": "7023300216061170213",
    "悲伤女声": "7367266428002505243",

    # 男青年
    "开朗学长": "7382879228393427493",
    "阳光青年": "7382878511217775130",
    "广告男声": "7382874510376047130",
    "悠悠君子": "7382878113916523035",
    "强势青年": "7367238853679125043",
    "阳光男生": "6912251288331751943",
    "沉稳男声": "7317623416691888650",
    "悲伤青年": "7367238720077959689",

    # 少女
    "病娇少女": "7382879331174847013",
    "撒娇学妹": "7382558138009915913",
    "冷静少女": "7367239175281578546",
    "元气少女": "7350221867958932031",
    "活泼女孩": "7462472428438950452",

    # 少年
    "阳光少年": "7382845921647661595",
    "活泼少年": "7367245673655177779",

    # 儿童
    "小男孩": "7367253020309983782",
    "小女孩": "7367252909815239206",
    "萌娃": "6855161957519987207",

    # 老人
    "沉稳老者": "7367253137486254629",
    "老婆婆": "7242563452026229305",

    # 中年
    "儒雅大叔": "7367250055360680474",
    "温柔阿姨": "7367247089916449289",
    "刚正大叔": "7367252353176572467"

}


@retrying()
async def create_tts(request: TTSRequest):  # audio.speech.create

    effect_id = VOICE_MAPPING.get(request.voice, "7382552865023201819")

    loki_info = {"effect_id": effect_id, "model_names": "", "effect_type": 0}

    payload = {
        "text": request.input,
        # "loki_info": json.dumps(loki_info),
        "audio_config": {
            "format": "mp3",
            "sample_rate": 24000,
            "speech_rate": request.speed or 0,
            "pitch_rate": 0,
            "enable_timestamp": True,

        },
        "id_info": {
            "id": effect_id,
            "item_platform": 1
        }
    }
    if request.instructions and request.voice in {"柔美女友", "妩媚女生", "京腔小爷", }:
        if request.voice == "京腔小爷" and request.instructions == "happy":
            request.emotion = "joy"

        if request.voice == "柔美女友" and request.instructions == "surprise":
            request.emotion = "surprised"

        payload["audio_config"].update(
            {
                # 情绪
                "emotion_scale": 5,
                "emotion": request.instructions,
            }
        )

    logger.debug(payload)

    headers = {
        "pf": "7"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=200) as client:
        response = await client.post("/mweb/v1/tts_generate", json=payload)
        response.raise_for_status()

        data = response.json()

        # logger.debug(data)

        if request.response_format == "url":
            if data.get("ret") == "0":
                data["data"]["data"] = await to_url(data["data"]["data"], filename=f'{shortuuid.random()}.mp3')
            return data
        else:
            data = await to_bytes(data["data"]["data"])
            return data


if __name__ == '__main__':
    text = """Chatfire tts-pro支持多种音色：
柔美女友 妩媚女生 京腔小爷 猴哥 熊二 如来佛祖 咆哮哥 四郎 懒小羊 TVB女声 动漫小新 紫薇 黛玉 顾姐 动漫海绵 云龙哥 容嬷嬷 华妃 河南小哥 湾区大叔 广西老表 山东小哥 长沙妹坨 樱花小哥 上海阿姨 京腔 港普男声 天津小哥 西安掌柜 台湾女生 东北老铁 粤语男声 重庆小伙 魅力姐姐 高冷御姐 魅力女友 耿直女声 活泼女声 随性女声 知性女声 温柔淑女 悲伤女声 开朗学长 阳光青年 广告男声 悠悠君子 强势青年 阳光男生 沉稳男声 悲伤青年 病娇少女 撒娇学妹 冷静少女 元气少女 活泼女孩 阳光少年 活泼少年 小男孩 小女孩 萌娃 沉稳老者 老婆婆 儒雅大叔 温柔阿姨 刚正大叔

    """

    text = """
    融合 创新 专注 至简

    “融合”：融入市场、融通资源、融合发展

    “创新”：勇于突破、追求卓越、超越自我

    “专注”：专一专业、忠诚敬业、重德守律、做到极致

    “至简”：简约简朴、脚踏实地、知行合一
    """
    request = TTSRequest(
        model="tts-1",
        # input="军杰 快来我的五指山下" * 1,
        input=text,
        # voice="柔美女友",
        voice="猴哥",

        # voice="妩媚女生",
        # voice="如来佛祖",
        # voice="京腔小爷",

        response_format="url",

        # emotion="happy",
        # emotion="fear"
        emotion="surprise"

    )

    arun(create_tts(request))
