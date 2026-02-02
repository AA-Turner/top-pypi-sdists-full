#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/9/4 下午3:26
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 根据系统信息与聊天记录评价一个人
import re

from meutils.pipe import *

import xchat.itchat as itchat
from xchat.itchat.content import INCOME_MSG, TEXT, PICTURE, NOTE
from xchat.schemas.wechat.message import MessageType, QuoteMessage
from xchat.itchat.storage.messagequeue import Message
# from xchat.schemas.msg import Message as _Message, User

from xchat.schemas.wechat.message import Message as _Message


@decorator
def msg_filter(func, chatroom_regexp: Optional[str] = None, *msgs):
    """
        过滤群聊、私聊
    """
    msg = _Message(**obj_to_dict(msgs[0]))

    if (
            msg.CreateTime > time.time() - 5
            and (re.search(chatroom_regexp, msg.chatroom_name) if chatroom_regexp else True)

    ):
        return func(msg)


@itchat.msg_register([MessageType.TEXT, MessageType.ATTACHMENT], isGroupChat=True)  # 注册处理文本信息
@msg_filter
def reply(msg: Message):
    logger.debug(msg)
    _msg = msg
    msg = obj_to_dict(msg)
    # logger.debug(f"{msg}")
    # logger.debug(f"{User(**msg['User'])}")
    # logger.debug(f"UserUserUserUserUserUserUserUserUserUser")
    # user = msg.pop('User')

    msg = _Message(**msg)  # filter
    logger.debug(f"{msg}")

    group_name = msg.chatroom_name  # msg.User.NickName
    # msg.ToUserName 加密的群名
    logger.debug(f"群名: {group_name}")

    # msg.ToUserName， msg.ActualNickName群里机器人的name
    # msg.FromUserName 群id【除非机器人本身发信息，就是他自己的id】

    if (
            not hasattr(msg, 'CreateTime')
            or msg.CreateTime > time.time() - 10
            and "机器人调试" in group_name
    ):  # todo: 增加过滤函数
        logger.debug(f"[{type(msg)} => {msg.Type}]")

        ###############################################################

        from meutils.hooks.wechat import create_reply

        hook = create_reply(_msg, itchat_send=itchat.send)
        if hook: return

        ###############################################################
        logger.debug("测试发送")

        # itchat.send('@img@doc_watermark.jpg', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@img@doc_watermark.webp', toUserName=msg.chatroom_id)
        # itchat.send_image('doc_watermark.jpg', toUserName=msg.chatroom_id)
        # logger.debug('1')
        # itchat.send_image('doc_watermark.webp', toUserName=msg.chatroom_id)
        # logger.debug('2')




        # 使用上下文管理器自动处理文件的关闭和删除
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.txt') as temp: # suffix
            temp.write(b"This is a temporary file.")
            temp.seek(0)

            itchat.send(f'@fil@{temp.name}', toUserName=msg.chatroom_id)  # ToUserName

        # itchat.send_image(open('doc_watermark.jpg', 'rb'), toUserName=msg.chatroom_id)

        # itchat.send('@img@1.webp', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@img@1.webp', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@msg@1.webp', toUserName=msg.chatroom_id)  # ToUserName
        #
        # itchat.send('@vid@vidu.mp4', toUserName=msg.chatroom_id)  # ToUserName

        # itchat.send(f"FromUserName: {msg.FromUserName}", toUserName=msg.chatroom_id)  # msg.FromUserName
        # itchat.send('@fil@test.ipynb', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@fil@test.ipynb', toUserName=msg.ToUserName)  # ToUserName
        # itchat.send('@fil@test.ipynb', toUserName=msg.chatroom_id)  # ToUserName

        # itchat.send_image

        # itchat.send('@vid@vidu.mp4', toUserName=msg.chatroom_id)  # ToUserName

        # itchat.send('@img@1.webp', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@img@1.png', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@img@doc_watermark.jpg', toUserName=msg.chatroom_id)  # ToUserName

        # itchat.send('@fil@vidu.mp4', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@fil@doc_watermark.jpg', toUserName=msg.chatroom_id)  # ToUserName

        # itchat.send('@vid@x.mp3', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@img@x.mp3', toUserName=msg.chatroom_id)  # ToUserName

        # itchat.send(
        #     f'@fil@{"/Users/betterme/PycharmProjects/AI/aizoo/.idea/misc.xml"}',
        #     toUserName=msg.chatroom_id)  # ToUserName


# ['@fil@', '@img@', '@msg@', '@vid@']

# @itchat.msg_register(MessageType.SHARING)  # 注册处理文本信息
# def reply(msg):
#     print(str(msg))
#     print(requests.get(msg.Url).content)
#
#
# @itchat.msg_register([MessageType.TEXT, MessageType.ATTACHMENT], isGroupChat=True)
# def handler_group_msg(msg):
#     if not hasattr(msg, 'CreateTime') or msg.CreateTime > time.time() - 10:  # todo: 增加过滤函数
#         # ActualNickName
#         WECHAT_DATA = os.getenv('WECHAT_DATA', 'wechat_data').rstrip('/')
#         p = Path(f'{WECHAT_DATA}/{msg.User.NickName}')  # 用户【非机器人】todo: 常用信息封装
#         if msg.ToUserName == msg.User.UserName: p /= '机器返回'
#         p.mkdir(parents=True, exist_ok=True)
#         if msg["FileName"]:
#             msg.download(p / msg["FileName"])  # ['Picture', 'Recording', 'Attachment', 'Video']
#             # background_tasks
#
#         if msg.User.NickName == 'Wechat测试' and msg.IsAt:  # 被@回答问题
#             logger.debug(f"[{type(msg)} => {msg.type}]")
#             logger.debug(msg.keys())
#
#             print(str(msg))
#             # 'Text': '「Bettermeeeeeee：[文件]东北证券AI架构.pptx」\n- - - - - - - - - - - - - - -\n@Bettermeeeeeee\u2005qqqq'
#             logger.debug(msg.User)
#
#             msg.User.send_msg(f'@{msg.ActualNickName}\u2005「机器人回答1」')
#             # msg.User.send_msg(f'@{msg.ActualNickName} 「机器人回答2」')
#             # msg.User.send_msg(f'@{msg.ActualNickName}「机器人回答3」')


# 'ActualNickName', 'IsAt', 'ActualUserName'
# 'ActualNickName', 'IsAt', 'ActualUserName',

# import wxpy

# mp_username = itchat.search_mps(name='Python之禅')[0]['UserName']

if __name__ == '__main__':
    itchat.auto_login(hotReload=os.getenv('WECHAT_RELOAD'))  # hotReload=True表示短时间关闭程序后可重连
    # print(itchat.search_mps('Python之禅'))
    # mp_username = itchat.search_mps(name='Python之禅')[0]['UserName']

    # 'FromUserName': '@839adce9c446b9aa6284371d2a03ea74', 'ToUserName': '@65b692db46f1365b376891a856853124544b18b95e52e9e18985a466fd1e34d0'
    # print(itchat.search_friends(userName="@aa8e769e75daa860fd7bebf0a7c3af32bc4b731f920ef02a3830328ce936c492"))
    # itchat.run()

    itchat.run()
