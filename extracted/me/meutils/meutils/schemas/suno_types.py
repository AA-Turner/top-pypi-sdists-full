#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno_types
# @Time         : 2024/3/28 19:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

_CLERK_JS_VERSION = "4.73.2"

STATUS = {"streaming", "complete", "error"}  # submitted queued streaming complete/error

# 反代
BASE_URL = "https://studio-api.suno.ai"
# BASE_URL = "https://suno.chatfire.cc"

CLIENT_BASE_URL = "https://clerk.suno.com/v1/client"
CLIENT_BASE_URL = "https://clerk.chatfire.cc/v1/client"

UPLOAD_BASE_UR = "https://suno-uploads.s3.amazonaws.com/"
# UPLOAD_BASE_UR = "https://suno-uploads.chatfire.cc/"

STUDIO_BASE_URL = "https://studio-api.prod.suno.com/"
STUDIO_BASE_URL = "https://studio-api.chatfire.cc/"

API_GENERATE_V2 = "/api/generate/v2/"
API_GENERATE_LYRICS = "/api/generate/lyrics/"

API_BILLING_INFO = "/api/billing/info/"
API_FEED = "/api/feed/"
API_SESSION = "/api/session/"

MODELS = [
    {
        "id": "b8f595a3-f331-4424-a349-0dee6d894e3b",
        "name": "v3.5",
        "external_key": "chirp-v3-5",
        "major_version": 3,
        "description": "Newest model, better song structure, max 4 minutes"
    },
    {
        "id": "b37ed11c-19dd-41d1-8730-9cc2b04b01af",
        "name": "v3",
        "external_key": "chirp-v3-0",
        "major_version": 3,
        "description": "Broad, versatile, max 2 minutes"
    },
    {
        "id": "9cf36d4c-2532-455b-8f99-1985c3641dc4",
        "name": "v2",
        "external_key": "chirp-v2-xxl-alpha",
        "major_version": 2,
        "description": "Vintage Suno model, max 1.3 minutes"
    }
]


class SunoAIRequest(BaseModel):  # 原始请求体

    prompt: str = ""  # 优先级最高

    gpt_description_prompt: Optional[str] = None
    gpt: Optional[str] = None

    title: str = ""
    tags: str = ""

    continue_at: Optional[float] = None
    continue_clip_id: Optional[str] = None

    infill_start_s: Optional[Any] = None
    infill_end_s: Optional[Any] = None

    make_instrumental: bool = False

    mv: str = "chirp-v4"  # chirp-v3-5-tau
    generation_type: str = "TEXT"

    task: Optional[str] = None  # "cover"
    cover_clip_id: Optional[str] = None  # "684fea1d-4480-475e-b764-3018c03b3254"

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.gpt_description_prompt = self.gpt_description_prompt or self.gpt

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "",
                    "gpt_description_prompt": "写首中国风的歌曲",
                    "title": "",
                    "tags": "",
                    "continue_at": None,
                    "continue_clip_id": None,
                    "infill_start_s": None,
                    "infill_end_s": None,
                    "make_instrumental": False,
                    "mv": "chirp-v3-5"
                },
                {
                    "prompt": "",
                    "tags": "piano",
                    "mv": "chirp-v3-5-upload",  # 只有自定义，不支持 gpt_description_prompt
                    "title": "",
                    "continue_clip_id": "7905ec2d-0e9b-4e2f-9aef-962ebf64aed4",
                    # 2d4c0153-8878-45f8-beef-3eee10c7d4d4.wav
                    "continue_at": 20.04,
                    "infill_start_s": None,
                    "infill_end_s": None
                }
            ]
        }

    }


class LyricsRequest(BaseModel):
    prompt: str = ""
    model: str = "suno"


class SongRequest(BaseModel):
    title: str = Field(description="song title")
    lyrics: str = Field(description="Enter lyrics, example: [Intro]...[Verse]...[Chorus]...")
    music_style: str = Field(description="the Style of Music, Maximum 10 words", examples=['syncopated country ...'])
    continue_clip_id: Optional[str] = Field(
        description="Continue creating based on song id/clip_id",
        examples=['8c7f666a-4df6-4657-8a83-d630b2b8ab56']
    )
    continue_at: Optional[int] = Field(120,
                                       description="Continue creating based on a certain point in time, for example at 10s")


class Response(BaseModel):
    code: Optional[int] = 0
    msg: Optional[str] = "success"
    data: Optional[Any] = None


class GenerateBase(BaseModel):
    prompt: str = ""
    mv: str = "chirp-v3"
    title: str = ""
    tags: str = ""
    continue_at: Optional[str] = None
    continue_clip_id: Optional[str] = None


class SunoRequest(BaseModel):
    """
    Welcome to Custom Mode 欢迎使用自定义模式

    Start with Lyrics: Write down your thoughts, or hit “Make Random Lyrics” for spontaneous creativity. Prefer no words? Opt for “Instrumental” and let the tunes express themselves.
    从歌词开始写下你的想法，或点击 "制作随机歌词 "进行即兴创作。不喜欢歌词？选择 "乐器"，让曲调来表达自己。

    Choose a Style: Select your “Style of Music” to set the vibe, mood, tempo and voice. Not sure? “Use Random Style” might surprise you with the perfect genre.
    选择风格：选择您的 "音乐风格"，设定氛围、情绪、节奏和声音。不确定？"使用随机风格 "可能会让你惊喜地发现完美的音乐风格。

    Extend Your Song: Want to go longer? Use the more actions (…) menu, select "Continue From This Song", select the desired time to extend your song from, and press Create. Use “Get Full Song” to put the full song together.
    延长您的歌曲：想延长时间？使用 "更多操作"（...）菜单，选择 "从这首歌开始继续"，选择想要延长歌曲的时间，然后按 "创建"。使用 "获取完整歌曲 "将完整歌曲放在一起。

    Unleash Your Creativity: Dive into the world of music-making and let your imagination run wild. Happy composing! 🎉
    释放你的创造力：潜入音乐创作世界，尽情发挥你的想象力。祝您创作愉快🎉
    """

    song_description: str = ""  # '一首关于在雨天寻找爱情的富有感染力的朋克歌曲' todo: gpt润色
    """
        Describe the style of music and topic youwant (e.g. acoustic pop about theholidays).
        Use genres and vibes insteadof specific artists and songs
    """

    instrumental: bool = False
    """创作一首没有歌词的歌曲。"""

    custom_mode: bool = True
    """Suno 专为创作原创音乐而设计。请确认您只提交人工智能生成的歌词、原创歌词或您有权继续使用的歌词。"""

    title: str = ''

    music_style: str = "R&B and soul"  # 可随机
    tags: str = music_style

    mv: str = 'chirp-v3-5'  # 模型

    lyrics: Optional[str] = None  # 自动生成
    prompt: Optional[str] = None  # 自动生成
    gpt_description_prompt: Optional[str] = None  # 自动生成
    """
        [Verse]
        Wake up in the morning, feeling kind of tired
        Rub my eyes, stretch my limbs, try to get inspired
        Open up the cupboard, see that shiny little jar
        It's my secret weapon, helps me reach the stars

        [Verse 2]
        Fill my favorite mug with that dark and steamy brew
        Inhale the aroma, it's my daily rendezvous
        Sip it nice and slow, feel the warmth flow through my veins
        Oh, coffee in the morning, you're my sugar, you're my dreams

        [Chorus]
        Coffee in the morning, you're my lifeline, can't deny
        You bring me energy when the day is looking gray
        Coffee in the morning, you're my sunshine in a cup
        With every sip, I'm feeling alive, ready to seize the day
    """
    # 继续创作
    continue_at: Optional[float] = None
    continue_clip_id: Optional[str] = None  # "8c7f666a-4df6-4657-8a83-d630b2b8ab56"

    input: dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = self.song_description

        self.input.update({"mv": self.mv, })

        # if self.custom_mode:
        #
        #
        #     self.input = self.input or {
        #         "gpt_description_prompt": self.gpt_description_prompt,
        #         "make_instrumental": False,
        #         "prompt": "",
        #
        #         "mv": self.mv,
        #     }
        #
        # else:
        #
        #     self.input = self.input or {
        #         "title": self.title,
        #         "tags": self.tags,
        #         "prompt": self.prompt,
        #         "continue_clip_id": self.continue_clip_id,
        #         "continue_at": self.continue_at,
        #
        #         "mv": self.mv,
        #
        #     }


if __name__ == '__main__':
    pass
    # d = {"input": {
    #     "prompt": "小嘛小儿郎\n\n背着那书包进学堂\n\n不怕太阳晒也不怕那风雨狂\n\n只怕那先生骂我懒哪\n\n没有学问\n\n无脸见爹娘\n\n郎里格郎里格郎里格郎\n\n没有学问\n\n无脸见爹娘\n\n小嘛小儿朗\n\n背着那书包进学堂\n\n不是为做官也不是为面子光\n\n只为穷人要翻身哪\n\n不受人欺负\n\n为不做牛和羊\n\n郎里格郎里格郎里格郎\n\n不受人欺负\n\n为不做牛和羊\n\n小嘛小儿郎\n\n背着那书包进学堂\n\n不怕太阳晒也不怕那风雨狂\n\n只怕先生骂我懒哪\n\n没有学问\n\n无脸见爹娘\n\n郎里格郎里格郎里格郎\n\n没有学问\n\n无脸见爹娘\n\n小嘛小儿朗\n\n背着那书包进学堂\n\n不是为做官也不是为面子光\n\n只为穷人要翻身哪\n\n不受人欺负\n\n为不做牛和羊\n\n郎里格郎里格郎里格郎\n\n不受人欺负\n\n为不做牛和羊",
    #     "title": "小二郎", "tags": "pop,inspirational", "continue_at": 0, "continue_clip_id": ""}, "custom_mode": True}
    #
    # print(SunoRequest(**d))
    #
    # import requests
    # import json
    #
    # url = "http://0.0.0.0:8000/v1/suno/v1/music"
    #
    # payload = json.dumps({
    #     "custom_mode": True,
    #     "input": {
    #         "prompt": "[Verse]\nTesla riding\nBatteries flying\nElon Musk\nHe's got the future on his mind\nSolar panels shining\nRockets reaching for the skies\nInnovation's flowing\nHe's the tech wizard of our times\n\n[Verse]\nNeuralink connecting minds\nAI running wild\nMars colonization\nHe's making it his style\nFrom PayPal he came and shook the world with his touch\nElon Musk\nThe eccentric genius\nHe's too much\n\n[Chorus]\nElon Musk\nHe's the man with electric dreams\nChanging the world with his technology schemes\nFrom PayPal to SpaceX\nHe's a force to be seen\nElectric cars and rockets\nHe's living the dream",
    #         "title": "Electric Dreams",
    #         "tags": "epic reggae",
    #         "continue_at": 0,
    #         # the second that this clip started from last clip. 0 means start over. Note that only GoAPI developer or above plan can use value not zero
    #         "continue_clip_id": ""  # the id of the clip that you need to continue; empty string means brand new clip.
    #     }
    # })
    # headers = {
    #     'Authorization': "Bearer sk-VPoyeW5lRW3HRvWCBb565a441b4c4eB4Ab2560AbBa0f968f",
    #     'Content-Type': 'application/json'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload)
    #
    # print(response.text)
    print(isinstance(SunoRequest(), BaseModel))

    # 续写获取完整歌曲

    """
    curl 'https://studio-api.suno.ai/api/generate/concat/v2/' \
  -H 'accept: */*' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'affiliate-id: undefined' \
  -H 'authorization: Bearer eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yT1o2eU1EZzhscWRKRWloMXJvemY4T3ptZG4iLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJzdW5vLWFwaSIsImF6cCI6Imh0dHBzOi8vc3Vuby5jb20iLCJleHAiOjE3MjE2NDE2MDMsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJ1c2VyXzJqWWdqUDYyNUxmUXZyTTRSdWRscmhOSXpsZyIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvZW1haWwiOiJ3ZWRkaHJydDh5QG5idmlkYXBwLmNjIiwiaHR0cHM6Ly9zdW5vLmFpL2NsYWltcy9waG9uZSI6bnVsbCwiaWF0IjoxNzIxNjQxNTQzLCJpc3MiOiJodHRwczovL2NsZXJrLnN1bm8uY29tIiwianRpIjoiZWExOGYyOGJiMGQ3YjU2YjNjZDEiLCJuYmYiOjE3MjE2NDE1MzMsInNpZCI6InNlc3NfMmpiMENzSHZzWXRuQktQQUNtQ0c3aGF0ZGVlIiwic3ViIjoidXNlcl8yallnalA2MjVMZlF2ck00UnVkbHJoTkl6bGcifQ.NXLXVy_4rURrqjKvH4-lSkEcQde9ChXj1BsfL7hlJZGMtYv3x9b1EL9TxqZJNdlbkuYsKMLPESCWVI5P-HZQT9ID4FRW44U_YCgxbbyry7nn5wzTqSPktLVj1lNx48mEzO-RCMseUzO_6YCOj9GVq4V_soxX0whZbo68VGvCoBz8A0pKTL3CVxgmnMI4k3cAFCrm0QmCaER38A0AQTc0qBF89sFQN-2FXisHR_RPPi4qu-zkTm0_xG2wtgY-8VgFFM4ruGhQR7y4UbRKIwyK6D0mWik8dFOsWE-sOF1L-X5ZQO0gJGcqAjy1BqOgKIeO6nhafT4EJ8l0ru8oQiY3ew' \
  -H 'content-type: text/plain;charset=UTF-8' \
  -H 'origin: https://suno.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://suno.com/' \
  -H 'sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' \
  --data-raw '{"clip_id":"996aad74-afbb-4e9f-bd8d-be855310fc8e","is_infill":false}'

curl 'https://studio-api.suno.ai/api/feed/v2?ids=b2c7d913-b42b-42b7-988c-89bcfaad72bf' \
  -H 'accept: */*' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'affiliate-id: undefined' \
  -H 'authorization: Bearer eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yT1o2eU1EZzhscWRKRWloMXJvemY4T3ptZG4iLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJzdW5vLWFwaSIsImF6cCI6Imh0dHBzOi8vc3Vuby5jb20iLCJleHAiOjE3MjE2NDE2MDMsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJ1c2VyXzJqWWdqUDYyNUxmUXZyTTRSdWRscmhOSXpsZyIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvZW1haWwiOiJ3ZWRkaHJydDh5QG5idmlkYXBwLmNjIiwiaHR0cHM6Ly9zdW5vLmFpL2NsYWltcy9waG9uZSI6bnVsbCwiaWF0IjoxNzIxNjQxNTQzLCJpc3MiOiJodHRwczovL2NsZXJrLnN1bm8uY29tIiwianRpIjoiZWExOGYyOGJiMGQ3YjU2YjNjZDEiLCJuYmYiOjE3MjE2NDE1MzMsInNpZCI6InNlc3NfMmpiMENzSHZzWXRuQktQQUNtQ0c3aGF0ZGVlIiwic3ViIjoidXNlcl8yallnalA2MjVMZlF2ck00UnVkbHJoTkl6bGcifQ.NXLXVy_4rURrqjKvH4-lSkEcQde9ChXj1BsfL7hlJZGMtYv3x9b1EL9TxqZJNdlbkuYsKMLPESCWVI5P-HZQT9ID4FRW44U_YCgxbbyry7nn5wzTqSPktLVj1lNx48mEzO-RCMseUzO_6YCOj9GVq4V_soxX0whZbo68VGvCoBz8A0pKTL3CVxgmnMI4k3cAFCrm0QmCaER38A0AQTc0qBF89sFQN-2FXisHR_RPPi4qu-zkTm0_xG2wtgY-8VgFFM4ruGhQR7y4UbRKIwyK6D0mWik8dFOsWE-sOF1L-X5ZQO0gJGcqAjy1BqOgKIeO6nhafT4EJ8l0ru8oQiY3ew' \
  -H 'origin: https://suno.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://suno.com/' \
  -H 'sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    """
