#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : wechat_types
# @Time         : 2024/8/8 18:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from pydantic import constr


# {"type": "text",  "content": 'xx'}
# {"type": "error", "content": 'xx'}

# {"type": "image", "content": 'https://oss.ffire.cc/files/xx.png'}

# {"type": "audio", "content": 'https://oss.ffire.cc/files/xx.mp3'}
# {"type": "file", "content": 'https://oss.ffire.cc/files/xx.mp3'}

# {"type": "video", "content": 'https://oss.ffire.cc/files/vidu.mp4'}
class HookResponse(BaseModel):
    type: str = 'text'
    content: Optional[str] = ''


class HookResponses(BaseModel):
    responses: List[HookResponse]


class RecommendInfo(BaseModel):
    UserName: str = ''
    NickName: str = ''
    QQNum: int = '0'
    Province: str = ''
    City: str = ''
    Content: str = ''
    Signature: str = ''
    Alias: str = ''
    Scene: int = '0'
    VerifyFlag: int = '0'
    AttrStatus: int = '0'
    Sex: int = '0'
    Ticket: str = ''
    OpCode: int = '0'


class Member(BaseModel):
    MemberList: list = []
    Uin: int = '0'
    UserName: str = ''
    NickName: str = ''
    AttrStatus: int = 0
    PYInitial: str = ''
    PYQuanPin: str = ''
    RemarkPYInitial: str = ''
    RemarkPYQuanPin: str = ''
    MemberStatus: int = 0
    DisplayName: str = ''
    KeyWord: str = ''


# class Self(Member):
#     """机器人属性"""
#     pass


class User(BaseModel):
    """群属性"""
    MemberList: List[Member] = None

    Uin: int = '0'
    UserName: str = '@@...'
    NickName: constr(to_lower=True) = ''  # 群昵称
    HeadImgUrl: str = '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=805036502&username=@@...&skey='
    ContactFlag: int = 0
    MemberCount: int = 0
    RemarkName: str = ''
    HideInputBarFlag: int = 0
    Sex: int = 0
    Signature: str = ''
    VerifyFlag: int = 0
    OwnerUin: int = 0
    PYInitial: str = ''  # 'XCHATCHATLLM'
    PYQuanPin: str = ''  # 'Xchatchatllm'
    RemarkPYInitial: str = ''
    RemarkPYQuanPin: str = ''
    StarFriend: int = 0
    AppAccountFlag: int = 0
    Statues: int = 1
    AttrStatus: int = 0
    Province: str = ''
    City: str = ''
    Alias: str = ''
    SnsFlag: int = 0
    UniFriend: int = 0
    DisplayName: str = ''
    ChatRoomId: int = 0
    KeyWord: str = ''
    EncryChatRoomId: str = '@...'
    IsOwner: int = '1'
    IsAdmin: Optional[str] = None

    Self: Any = Member()  # 机器人微信信息 # Self


class Message(BaseModel):
    MsgId: str = ''
    FromUserName: str = '@...'
    ToUserName: str = '@@...'  # @@是接收信息的群ID
    MsgType: int = 49
    Content: str = ''
    Status: int = 3
    ImgStatus: int = 1
    CreateTime: int = Field(default_factory=lambda: int(time.time()))
    VoiceLength: int = 0
    PlayLength: int = 0
    FileName: str = ''  # 'xx.doc'
    FileSize: str = '633344'
    MediaId: str = '@crypt_...'
    Url: str = ''
    AppMsgType: int = 6
    StatusNotifyCode: int = 0
    StatusNotifyUserName: str = ''

    RecommendInfo: Any = RecommendInfo()

    ForwardFlag: int = '0'
    AppInfo: dict = {'AppID': '', 'Type': 0}
    HasProductId: int = '0'
    Ticket: str = ''
    ImgHeight: int = '0'
    ImgWidth: int = '0'
    SubMsgType: int = '0'
    NewMsgId: int = '1316678251262129000'
    OriContent: str = ''
    EncryFileName: str = '%E8%80%B6%E8%B7%AF%E6%92%92%E5%86%B7%E4%B8%89%E5%8D%83%E5%B9%B4%2Edoc'
    ActualNickName: str = ''  # 群里展示的昵称

    IsAt: bool = False
    ActualUserName: str = '@...'

    # user: User = Field(alias='User')
    User: User

    Type: str = 'Attachment'
    Text: Any = '{}'  # 可能是函数

    # 增强
    chatroom_name: str = None
    chatroom_id: str = None

    user_name: str = None

    # download: Callable = None

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.chatroom_name = self.User.NickName  # 已被转小写
        self.chatroom_id = self.User.UserName

        self.user_name = self.User.NickName  # 人昵称 不是机器人昵称


@dataclass(init=False)
class MessageType(object):
    """
    图片或表情（PICTURE）、录制（RECORDING）、附件（ATTACHMENT）、小视频（VIDEO）、文本（TEXT），地图（MAP），名片（CARD），
    通知（NOTE），好友邀请（FRIENDS）、语音（RECORDING）、系统消息（SYSTEM）
    分享（SHARING）:
        小程序     'AppMsgType': 33
        小视频     'AppMsgType': 51 'Type': 'Sharing', 'Text': '当前微信版本不支持展示该内容，请升级至最新版本。'
        微信看一看 ’AppMsgType': 5   'Type': 'Sharing', 'Text': '加沙一难民营被以色列“完全摧毁”' 'FileName': '加沙一难民营被以色列“完全摧毁”'
        公众号文章 'AppMsgType': 5   'Type': 'Sharing', 'Text': 'Skywork-13B：昆仑万维集团-天工团队彻底开源代码和数据集' 'FileName': 'Skywork-13B：昆仑万维集团-天工团队彻底开源代码和数据集'
    """
    TEXT = 'Text'
    MAP = 'Map'
    CARD = 'Card'
    NOTE = 'Note'
    SHARING = 'Sharing'
    PICTURE = 'Picture'
    RECORDING = 'Recording'  #
    VOICE = 'Recording'  #
    ATTACHMENT = 'Attachment'
    VIDEO = 'Video'
    FRIENDS = 'Friends'
    SYSTEM = 'System'

    INCOME_MSG = [TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, VOICE, ATTACHMENT, VIDEO, FRIENDS, SYSTEM]


# 朋友信息
{
    "MemberList": "<ContactList: []>",
    "Uin": 0,
    "UserName": "@aa8e769e75daa860fd7bebf0a7c3af32bc4b731f920ef02a3830328ce936c492",
    "NickName": "firebot",
    "HeadImgUrl": "/cgi-bin/mmwebwx-bin/webwxgeticon?seq=766248947&username=@aa8e769e75daa860fd7bebf0a7c3af32bc4b731f920ef02a3830328ce936c492&skey=@crypt_9ee03a29_289538cfb03502fc9947971cb5f890d5",
    "ContactFlag": 2051,
    "MemberCount": 0,
    "RemarkName": "",
    "HideInputBarFlag": 0,
    "Sex": 1,
    "Signature": "搞钱<span class=\"emoji emoji1f4b0\"></span>",
    "VerifyFlag": 0,
    "OwnerUin": 0,
    "PYInitial": "FIREBOT",
    "PYQuanPin": "firebot",
    "RemarkPYInitial": "",
    "RemarkPYQuanPin": "",
    "StarFriend": 0,
    "AppAccountFlag": 0,
    "Statues": 0,
    "AttrStatus": 102725,
    "Province": "江苏",
    "City": "苏州",
    "Alias": "",
    "SnsFlag": 257,
    "UniFriend": 0,
    "DisplayName": "",
    "ChatRoomId": 0,
    "KeyWord": "",
    "EncryChatRoomId": "",
    "IsOwner": 0
}

# USer
{
    "MemberList": "<ContactList: []>",
    "Uin": 0,
    "UserName": "@aa8e769e75daa860fd7bebf0a7c3af32bc4b731f920ef02a3830328ce936c492",
    "NickName": "firebot",
    "HeadImgUrl": "/cgi-bin/mmwebwx-bin/webwxgeticon?seq=766248947&username=@aa8e769e75daa860fd7bebf0a7c3af32bc4b731f920ef02a3830328ce936c492&skey=@crypt_9ee03a29_289538cfb03502fc9947971cb5f890d5",
    "ContactFlag": 2051,
    "MemberCount": 0,
    "RemarkName": "",
    "HideInputBarFlag": 0,
    "Sex": 1,
    "Signature": "搞钱<span class=\"emoji emoji1f4b0\"></span>",
    "VerifyFlag": 0,
    "OwnerUin": 0,
    "PYInitial": "FIREBOT",
    "PYQuanPin": "firebot",
    "RemarkPYInitial": "",
    "RemarkPYQuanPin": "",
    "StarFriend": 0,
    "AppAccountFlag": 0,
    "Statues": 0,
    "AttrStatus": 102725,
    "Province": "江苏",
    "City": "苏州",
    "Alias": "",
    "SnsFlag": 257,
    "UniFriend": 0,
    "DisplayName": "",
    "ChatRoomId": 0,
    "KeyWord": "",
    "EncryChatRoomId": "",
    "IsOwner": 0
}

messagetype_map = {

    "[文件]": MessageType.ATTACHMENT,  # 语音也算
    "[链接]": MessageType.SHARING,

    # 无法绝对定位，只能相对【根据最新图片或者视频】
    "[视频]": MessageType.VIDEO,
    "[图片]": MessageType.PICTURE,

}


class QuoteMessage(object):
    """
    「firebot：qqqqqqq」
    「NickName：[文件]hello.mp3」
    「firebot：[文件]耶路撒冷三千年.doc」
    「Betterme：[链接]国产AI火爆海外，7个月收入近千万」

    「Betterme：[图片]」
    「Betterme：[视频]」
    - - - - - - - - - - - - - - -
    这是个问题

    @firebot 这是个问题 # todo


    """

    def __init__(self, text_msg: str):
        q1, q2 = text_msg.split('\n- - - - - - - - - - - - - - -\n')  # ['「Betterme：[链接]国产AI火爆海外，7个月收入近千万」', '这是个问题']
        self.text_msg = text_msg.strip()
        self.nickname, quote = q1.strip()[1:-1].split('：', maxsplit=1)
        self.context_type = messagetype_map.get(quote[:4], MessageType.TEXT)  # [链接]国产AI火爆海外，7个月收入近千万
        self.context = quote[4:] if self.context_type != MessageType.TEXT else quote  # 上下文

        self.question = q2.strip()


# python#获取公众号名称为“Python之禅”的信息
# mp_username = itchat.search_mps(name='Python之禅')[0]['UserName']
# mp_info = itchat.update_friend(username=mp_username, detailed=True)


if __name__ == '__main__':
    # msg = """
    # 「Betterme：东北证券AI架构.pptx」\n- - - - - - - - - - - - - - -\n@Betterme\u2005/tts不知道
    # """.strip()
    # rprint(QuoteMessage(msg).__dict__)
    # rprint(QuoteMessage(msg).question.split('/tts', 1)[-1])
    User
