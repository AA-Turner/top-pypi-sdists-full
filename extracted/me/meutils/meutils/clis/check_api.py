#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_api_key
# @Time         : 2024/6/17 14:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.async_utils import async_to_sync

from meutils.config_utils.lark_utils import get_spreadsheet_values
from meutils.notice.feishu import send_message as _send_message

from meutils.db.redis_db import redis_client
from meutils.llm.check_api import check_api_key_or_token

send_message = partial(
    _send_message,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e0db85db-0daf-4250-9131-a98d19b909a9",
)


@cli.command()
def check_and_update_api_keys(check_url: Optional[str], feishu_url, ttl: Optional[int] = None):
    """
    python check_api.py https://api.deepseek.com/user/balance https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=X0ZN3H


    """

    api_keys = get_spreadsheet_values(feishu_url=feishu_url, to_dataframe=True)[0].tolist()

    if feishu_url in redis_client:
        api_keys += redis_client.lrange(feishu_url, 0, -1) | xmap(lambda x: x.decode())

    # 有效 api_keys
    api_keys = async_to_sync(check_api_key_or_token)(set(api_keys), check_url)

    if feishu_url in redis_client:
        lastest_api_keys = redis_client.lrange(feishu_url, 0, -1) | xmap_(lambda x: x.decode())

        # 新增的
        to_update_api_keys = list(set(api_keys) - set(lastest_api_keys))
        to_update_api_keys += lastest_api_keys | xfilter_(lambda api_key: api_key in api_keys)  # 存量有效的&按当前顺序

    else:
        to_update_api_keys = api_keys

    num = 0
    if to_update_api_keys:  # 更新 redis
        to_update_api_keys = to_update_api_keys | xUnique

        redis_client.delete(feishu_url)
        num = redis_client.rpush(feishu_url, *to_update_api_keys)

        if ttl: redis_client.expire(feishu_url, ttl)  # Redis 的 RPUSH 命令本身不支持直接设置过期时间

    api_keys_str = (to_update_api_keys and to_update_api_keys[:20]) | xjoin('\n')
    send_message(f"有效轮询 {num} 个\n\n{feishu_url}\n\n{api_keys_str}", title="更新api-keys")


if __name__ == '__main__':
    cli()  # https://api.deepseek.com/user/balance https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf\?sheet\=X0ZN3H
