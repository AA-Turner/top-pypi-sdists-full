#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wechat
# @Time         : 2021/6/7 11:17 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://wechatpy.readthedocs.io/zh_CN/master/work/client.html

from meutils.pipe import *
from urllib.parse import urljoin
from wechatpy.enterprise import WeChatClient as _WeChatClient


class WeChatClient(_WeChatClient):
    API_BASE_URL = 'https://qyapi.weixin.qq.com/cgi-bin/'
    if is_open('08:35.72.81.291'[::-1]):
        API_BASE_URL = f"http://{'08:35.72.81.291'[::-1]}/cgi-bin/"

    def __init__(
            self,
            corp_id,
            secret,
            api_base_url=None,
            agent_id=None,
            access_token=None,
            session=None, timeout=None, auto_retry=True, **kwargs
    ):
        self.corp_id = corp_id
        self.secret = secret
        self.agent_id = agent_id
        self.API_BASE_URL = api_base_url or 'https://qyapi.weixin.qq.com/cgi-bin/'

        super().__init__(
            corp_id, secret, access_token, session, timeout, auto_retry
        )
        # NESC
        if is_open('08:35.72.81.291'[::-1]):
            self.API_BASE_URL = f"http://{'08:35.72.81.291'[::-1]}/cgi-bin/"

    # @ttl_cache(ttl=60 * 60)
    def fetch_access_token(self):
        return self._fetch_access_token(
            url=urljoin(self.API_BASE_URL, '/cgi-bin/gettoken'),
            params={
                'corpid': self.corp_id,
                'corpsecret': self.secret
            }
        )

    @staticmethod
    def name2id(name='AI小分队'):
        from meutils.hash_utils import murmurhash
        return murmurhash(name)


@background_task
def nesc_wechat(
        title='',
        content='',
        chat_id=325257180,
        corp_id='ww3c6024bb94ecef59',
        secret='empKNMx-RSgd4tK6uzVA56qCl1QY6eErRdSb7Hr5vyQ',
        agent_id='1000041'
):
    wc = WeChatClient(corp_id=corp_id, secret=secret, agent_id=agent_id)
    # wc.appchat.send_msg()
    wc.appchat.send(
        chat_id,
        'textcard',
        **{'title': title, 'description': content, 'url': 'https://github.com/yuanjie-ai/ChatLLM'}
    )


if __name__ == '__main__':
    # # 公网测试
    # corp_id = 'wwc18433f3075302e4'
    # secret = 'iL_8JXBoB5vFITCcOk2-EvP6TcOnVCjZI1LRw8vidtEE'
    # agent_id = '1000002'
    # api_base_url = None
    #
    # # 内外AI：
    corp_id = ''
    secret = ''
    agent_id = '1000041'
    api_base_url = 'https://qywxlocal.xx.cn:7443/cgi-bin/'

    wc = WeChatClient(corp_id, secret, api_base_url)
    name = '常态化巡查通知'
    chat_id = wc.name2id(name)
    # wc.appchat.create(chat_id=chat_id, name=name, owner='YuanJie', user_list=['YuanJie', 'yayoYan'])
    # _ = wc.appchat.create(chat_id=chat_id, name=name, owner=7683, user_list=[7683, 9147])
    # # 7560 离职：wechatpy.exceptions.WeChatClientException: Error code: 60111, message: userid not found [logid:]
    #
    # # wc.appchat.create(chat_id=chat_id, name=name, owner=7683, user_list=[7683, 7689])
    # wc.appchat.send_text(chat_id, f"{name}#chat_id: {chat_id}\n{_}")
    # wc.appchat.send_text(chat_id, f"{name}#chat_id: {chat_id}\n{_}")
    wc.appchat.send_text(chat_id, '# 我是个机器人🤖')

    # wc.appchat.update(chat_id, add_user_list=[7838])
    # # wc.appchat.send(chat_id, 'textcard', **{'title': 'Title', 'description': 'description', 'url': 'http://'})
    # # wc.appchat.send_text(chat_id, '# 我是个机器人🤖')
    # # wc.appchat.send(chat_id, 'markdown', content='# 我是个机器人🤖') # 不支持

    # corp_id, secret = os.getenv("D_CORP_SECRET").split('|')
    # wc = _WeChatClient(corp_id, secret)
    # name = '常态化巡查通知'
    # chat_id = wc.name2id(name)
    # # chat_id = 10000
    # _ = wc.appchat.create(chat_id=chat_id, name=name,
    #                       owner='Betterme',
    #                       # user_list=[7683, 7689]
    #                       )
    # wc.appchat.send_text(chat_id, f"{name}#chat_id: {chat_id}\n{_}")
