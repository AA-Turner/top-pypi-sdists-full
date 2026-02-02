#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tokens
# @Time         : 2025/10/12 00:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import asyncio
import datetime as dt

from meutils.pipe import *
from meutils.db.redis_db import redis_client, redis_aclient
from meutils.schemas.openai_types import CompletionRequest, CompletionUsage


class TokenPool(object):
    def __init__(self, biz: Optional[str] = None, redis_url: str = "redis://localhost"):
        # self.r = redis.from_url(redis_url, decode_responses=True)

        self.r = redis_aclient
        self.biz = biz or "biz"

    # ---------- 内部工具 ----------
    def _hash_key(self, model: str, day: str = None) -> str:
        day = day or dt.date.today().strftime("%Y%m%d")
        return f"{self.biz}:tk:{day}:{model}"

    def _zset_key(self, model: str, day: str = None) -> str:
        day = day or dt.date.today().strftime("%Y%m%d")
        return f"{self.biz}:rk:{day}:{model}"

    async def set_tokens(self, model: str, api_key: str, tokens: int):  # 手动加入 没钱的key
        """强制把某个 api_key 的 tokens 设成指定值"""
        pipe = self.r.pipeline(transaction=True)
        pipe.hset(self._hash_key(model), api_key, tokens)  # 覆盖 HASH
        pipe.zadd(self._zset_key(model), {api_key: tokens})  # 覆盖 ZSET
        await pipe.execute()

    # ---------- 1. 记录/回写 tokens ----------
    async def incr_tokens(self, model: str, api_key: str, tokens: int, day: str = None):
        h_key = self._hash_key(model, day)
        z_key = self._zset_key(model, day)

        pipe = self.r.pipeline(transaction=True)
        pipe.hincrby(h_key, api_key, tokens)  # HASH 自增
        pipe.zincrby(z_key, tokens, api_key)  # ZSET 同步 排序
        # 给两个 key 都设 7 天后过期（秒数 7*24*3600=604800）
        if await self.r.ttl(h_key) == -1:
            pipe.expire(h_key, 7 * 24 * 3600)
            pipe.expire(z_key, 7 * 24 * 3600)

        await pipe.execute()

    # ---------- 2. 取当前最小 tokens 的 api_key ----------

    async def pick_min_key(self, model: str, day: str = None):
        z_key = self._zset_key(model, day)
        logger.debug(z_key)
        lst = await self.r.zrange(z_key, 0, 0, withscores=True)
        logger.debug(lst)
        return lst or []

    # ---------- 3. 一站式「取 + 写」 ----------
    async def consume(self, model: str, tokens: int) -> Optional[str]:
        """tokens or freq 都可以用这个方法
        1. 选出该 model 下 tokens 最小的 api_key
        2. 立即把本次 tokens 写回
        3. 返回被消耗的 api_key；无可用返回 None
        """
        if api_keys := await self.pick_min_key(model):
            api_key, _ = api_keys[0]
            pass  # todo: 完善具体的业务逻辑

            await self.incr_tokens(model, api_key, tokens)

        return "业务逻辑"

    # ---------- 辅助：查任意 key 当前 tokens ----------
    async def get_tokens(self, model: str, api_key: str) -> int:
        val = await self.r.hget(self._hash_key(model), api_key)
        return int(val) if val else 0

    async def close(self):
        await self.r.close()


async def create_volc_request(request: CompletionRequest):
    # todo: 去掉这些判断 是否有更好的方式
    # request.thinking = {"type": "enabled"}
    # 后期通过参数覆盖 强行覆盖  传入exclude_models
    choices = {}
    mini_api_key = None
    if request.model.startswith("doubao-seed") and request.thinking.get("type") == "disabled":  # 不思考
        choices = {
            "doubao-seed-1-6-250615",
            "doubao-seed-1-6-vision-250815"
        }

    elif request.model.startswith("doubao-seed"):  # 思考
        request.thinking = {"type": "enabled"}
        choices = {
            "doubao-seed-1-6-250615",
            "doubao-seed-1-6-vision-250815",
            "doubao-seed-1-6-thinking-250715"
        }

    elif request.model.startswith(("deepseek-",)):  # deepseek => v3-1
        if request.model.startswith("deepseek-v3"):
            choices = {
                "deepseek-v3-1-terminus",
                "deepseek-v3-250324"
            }
        if request.model.startswith("deepseek-r"):
            request.thinking = {"type": "enabled"}
            choices = {
                "deepseek-v3-1-terminus",
                "deepseek-r1-250528",
            }


    ######## 低频
    elif request.model in {"doubao-1-5-thinking-vision-pro-250428"}:  # vision thinking
        choices = {
            "doubao-1-5-ui-tars-250428",
        }

    elif request.model.startswith(("doubao-1-5-thinking",)):  # thinking
        request.thinking = None
        choices = {
            "doubao-1-5-thinking-pro-250415",
            "doubao-1-5-ui-tars-250428",
        }

    elif request.model.startswith(("doubao-1-5", "doubao-1.5")):  # nothinking
        request.thinking = {"type": "disabled"}

        choices = {
            "doubao-1-5-pro-32k-250115",
            "doubao-1-5-pro-256k-250115",
            "doubao-1-5-pro-32k-character-250715",
            "doubao-1-5-pro-32k-character-250228",
            "doubao-1.5-vision-pro-250328",
            "doubao-1-5-vision-pro-32k-250115",
            "doubao-1-5-thinking-pro-250415",
            "doubao-1-5-ui-tars-250428",
        }

    if hasattr(request, "exclude_models"):  # 参数覆盖
        choices -= set(request.exclude_models.split(','))

    l = []
    for model in choices:
        k, s = await TokenPool('volc').pick_min_key(model)
        l.append((model, k, s))

    if l:
        l.sort(key=lambda x: x[2])
        request.model, mini_api_key, _ = l[0]

    if mini_api_key is None:  # 初始化时 必须有一个 api_key
        feishu = "https://xchatllm.feishu.cn/sheets/Z59Js10DbhT8wdt72LachSDlnlf?sheet=Sgw6q1"
        logger.error(f"请先初始化 {feishu}")
        for k in "keys":
            await TokenPool('volc').incr_tokens(request.model, k, 0)

        # models keys 笛卡尔积

    return request, mini_api_key


if __name__ == '__main__':

    async def main():
        pool = TokenPool('volc')
        model = "gpt-4"
        # model = "gpt-4o"

        # 初始导入一些 api_key（可批量）
        await pool.incr_tokens(model, "ak-1", 0)  # 0 表示初始没消耗
        await pool.incr_tokens(model, "ak-2", 0)
        await pool.incr_tokens(model, "ak-3", 0)
        await pool.incr_tokens(model, "ak-4", 0)
        # api_keys = [f"k{i}" for i in range(100)]
        # await pool.incr_tokens(model, api_keys, 888)  # 0 表示初始没消耗

        # 模拟 5 次调用，每次 100 tokens
        for i in range(5):
            key = await pool.consume(model, i * 50)
            print("consume ->", key)

        # 查看各 key 累计
        for ak in ["ak-1", "ak-2", "ak-3", "ak-4"]:
            print(ak, await pool.get_tokens(model, ak))

        await pool.close()


    asyncio.run(main())
    # model = "gpt-4"
    # model = "gpt-4o"
    # arun(TokenPool('volc').pick_min_key(model))  # 取出最小的key

    # arun(TokenPool().incr_tokens(model, "no_money", 888))

"""
m1 k1
m2 k11
m3 k111

"""
