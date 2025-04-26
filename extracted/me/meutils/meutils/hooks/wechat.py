#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : wechat
# @Time         : 2024/8/8 18:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 摸鱼早报 https://api.52vmy.cn/api/wl/moyu

from meutils.pipe import *
from meutils.schemas.wechat_types import Message, HookResponse, HookResponses
from pyrate_limiter import Duration, Rate, Limiter, BucketFullException, RedisBucket

rates = [
    Rate(1, Duration.MINUTE),
    Rate(2, Duration.MINUTE * 15),

    Rate(2 ** 2, Duration.HOUR),
    Rate(2 ** 3, Duration.HOUR * 6),
    Rate(2 ** 4, Duration.HOUR * 24)
]
limiter = Limiter(rates)


# handler_group_msg
# pip install wget pyrate_limiter meutils -U --user && cd /app/channel/wechat && rm -rf wechat_channel.py* && python -m wget https://oss.ffire.cc/files/wechat_channel.py
# docker commit <container-name> chatfire/wechat:latest
# docker commit chatfire-wechat chatfire/wechat:latest
# docker push chatfire/wechat:latest

@background_task
def wechat_send(msg: Message, response: HookResponse, itchat_send: Callable):
    url = response.content
    if response.type == 'image':
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.txt') as file, \
                httpx.Client(follow_redirects=True, timeout=100) as client:
            response = client.get(url)
            file.write(response.content)
            file.seek(0)

            itchat_send(f'@fil@{file.name}', toUserName=msg.chatroom_id)  # ToUserName

    elif response.type == 'video':
        filename = wget.download(response.content)
        itchat_send(f"@vid@{filename}", toUserName=msg.chatroom_id)

    elif response.type == 'text':
        itchat_send(f"@{msg.ActualNickName}\n{response.content}", toUserName=msg.chatroom_id)

    elif response.type in {'audio', 'file'}:
        filename = wget.download(response.content)
        itchat_send(f"@fil@{filename}", toUserName=msg.chatroom_id)

    # debug
    else:
        itchat_send(f"@{msg.ActualNickName}\n未知消息类型\n{response.content}", toUserName=msg.chatroom_id)


@background_task
def post(msg: Message, itchat_send: Callable):
    try:
        url = os.getenv("WECHAT_HOOK_URL")
        api_key = os.getenv("WECHAT_HOOK_API_KEY")

        headers = {"Authorization": f"Bearer {api_key}"}
        data = httpx.post(
            url,
            headers=headers,
            json=msg.model_dump(),
            timeout=200
        ).json()

        response: HookResponse
        for response in HookResponses(responses=data).responses:
            logger.debug(response)
            wechat_send(msg, response, itchat_send)
    except Exception as e:
        wechat_send(msg, HookResponse(content=str(e)), itchat_send)


def create_reply(msg, itchat_send: Callable = None):  # 持续更新后端逻辑 解耦
    msg = obj_to_dict(msg)
    msg = Message(**msg)

    logger.debug(msg.Content)

    if (  # 拦截逻辑
            msg.IsAt
            and os.getenv("WECHAT_HOOK_URL") and os.getenv("WECHAT_HOOK_API_KEY")
            and msg.Content.split(maxsplit=1)[-1].startswith('/')
    ):

        try:
            if msg.ActualNickName.lower() not in {'betterme'}:
                limiter.try_acquire(msg.ActualNickName)  # 按昵称限制并发

            post(msg, itchat_send)
            return True

        except BucketFullException as err:
            logger.error(err)

            itchat_send(f"@{msg.ActualNickName}\n{err.meta_info}", toUserName=msg.chatroom_id)
            return True

    # yield "开始拼命执行任务"

    # {"type": "text",  "content": 'xx'}
    # {"type": "error", "content": 'https://oss.ffire.cc/files/vidu.mp4'}

    # {"type": "image", "content": 'https://oss.ffire.cc/files/xx.png'}

    # {"type": "audio", "content": 'https://oss.ffire.cc/files/xx.mp3'}
    # {"type": "file", "content": 'https://oss.ffire.cc/files/xx.mp3'}

    # {"type": "video", "content": 'https://oss.ffire.cc/files/vidu.mp4'}


def chat_group_hook(msg, debug: bool = False, send_fn: Callable = None):  # todo hk一个第三方服务
    # pip install meutils
    #     os.system("pip install meutils -U --user") 第一次的时候 加缓存 定期更新 并且重载
    logger.debug(msg)
    msg = obj_to_dict(msg)
    msg = Message(**msg)  # filter

    group_name = msg.chatroom_name  # msg.User.NickName
    # msg.ToUserName 加密的群名

    if debug:
        logger.debug(f"群名: {group_name}")
        # logger.debug(msg.model_dump_json(indent=4))
        logger.debug(f"[{type(msg)} => {msg.Type}]")

    # msg.ToUserName， msg.ActualNickName群里机器人的name
    # msg.FromUserName 群id【除非机器人本身发信息，就是他自己的id】

    # 时间内容
    prompt = msg.Content.split(maxsplit=1)[-1]
    if any(flag.lower() in group_name for flag in ['TEST']) or prompt.startswith('视频'):
        # itchat.send(f"FromUserName: {msg.FromUserName}", toUserName=msg.chatroom_id)  # msg.FromUserName
        # itchat.send('@fil@test.ipynb', toUserName=msg.chatroom_id)  # ToUserName
        # itchat.send('@fil@test.ipynb', toUserName=msg.ToUserName)  # ToUserName
        # itchat.send('@fil@test.ipynb', toUserName=msg.chatroom_id)  # ToUserName

        # send_fn('@vid@vidu.mp4', toUserName=msg.chatroom_id)  # ToUserName itchat.send
        # send_fn('@img@vidu.mp4', toUserName=msg.chatroom_id)  # ToUserName

        filename = wget.download('https://oss.ffire.cc/files/vidu.mp4')
        send_fn(f'@vid@{filename}', toUserName=msg.chatroom_id)  # ToUserName itchat.send

        # todo: 异步发送

        return None

    # try:
    #     cmsg = WechatMessage(msg, True)
    # except NotImplementedError as e:
    #     logger.debug("[WX]group message {} skipped: {}".format(msg["MsgId"], e))
    #     return None
    # WechatChannel().handle_group(cmsg)
    # return None
