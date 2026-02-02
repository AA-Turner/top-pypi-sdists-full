#!/usr/bin/env Python
# -*- coding: utf-8 -*-

from meutils.pipe import *
from meutils.caches import rcache
from meutils.decorators.retry import retrying

username = "d1982743732"
password = "1h29rymg"


@rcache(ttl=30)
@retrying()
async def get_proxy_list(n: int = 1, threshold: int = 30, seed: float = 0, http_url: Optional[str] = None):
    secret_id = os.getenv("KDLAPI_SECRET_ID")
    signature = os.getenv("KDLAPI_SIGNATURE")

    http_url = http_url or f"https://dps.kdlapi.com/api/getdps/?secret_id={secret_id}&signature={signature}&num={n}&pt=1&format=json&f_et=1&generateType=4&f_auth=1"

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(http_url)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))
        proxy_list = data.get('data').get('proxy_list', [])

        logger.debug(f"获取到的代理: {proxy_list}")

        # t16405495401930:7merxc5t@i146.kdltps.com:15818

        if _ := [
            f"http://{proxy.split(',')[0]}"
            if "," in proxy and int(proxy.split(',')[-1]) > threshold
            else f"http://{proxy}"
            for proxy in proxy_list
        ]:
            return _
        else:
            if _ := await get_proxy_list(2, threshold, seed=time.time(), http_url=http_url):
                logger.debug(f"获取到的代理都小于 {threshold} 秒，重试一次")

                return _
            else:
                raise TimeoutError(f"获取到的代理都小于 {threshold} 秒")


async def get_one_proxy(http_url: Optional[str] = None):
    if http_url:
        # return "http://chatfire:chatfirechatfire@144.172.116.240:30000"
        proxy_list = await get_proxy_list(http_url=http_url)
        logger.debug(proxy_list)
        return proxy_list[-1]


if __name__ == '__main__':
    # arun(get_proxy_list())

    page_url = "https://icanhazip.com/"  # 要访问的目标网页

    # page_url = "https://httpbin.org/ip"

    headers = {
        # 'bx-ua': '231!2PG3NkmUmFS+jm04UA3apMEjUq/YvqY2leOxacSC80vTPuB9lMZY9mRWFzrwLEV0PmcfY4rL2yQQzv4epFzCDXCN39IsbtzKjZV3BwK/R5DDDxuDiKaulHZWSpMXZKNwEGeLDZWdu3zSO4SgWJLtk5br+R4ag259rqHbr17eiw4tpiDr47wde+me8qgDK+CT+RuXSpWH8c8OIxzZEAOFjEoE76Ok+I8GUPyFoypr+MnepADqk+I9xGdFCQLMlFlCok+++4mWYi++6b8uo7z+DI0DjD3rFSeXTWNF7nfJ3U3OoIvrrng7X2cudzCjQE5n4QS6EQ92JXb6R4gklSbZOxtQxdCvPYXwO39wq6ptgVDCxigK1ABY9z/ewy2QlX7Wgk9XHAQExytzoOwzYaWqhhWafyBfreQikIL72BKnEfBPyYYS3MSDvpRIv0T5Wbw8HgnR8bik8hxvevqLz/lJ624AzneIrYuzb0tBQRx5SKD8VjTl4dc/+tiw9AKatwj/FyUnj8go3T66LfVa75RfSXkVnjkqGfPkriHKWVcKVrUraSr5wkKhSDJUxwZOR94ZF8IT1jyV7KxZh6uXvsAjS2peHI8C/l7FWH3dyi5tPHzaWOPis4tr7RkQ1no5WY4sdqIYA1Qf/hOaVUliBL5nRHSp/Ap/oH98HkKDyY23DjQ3Z296gpSqLWeIa6iRAqUqVlf5LCXE+CODvrb2tal2TPdIcjE+/u0oQbN+3HDA4axJ25z+LzubDTv9c/GiDDuvGRFIYTyGt0zbM+5Mo5q3Ut6Jn+B4XzE7jXVR1/YidaVWtlH2HQ0n9OSDSvrSlVuQNTYRwvgSJ1QlEFJh1Sh0yKgjtFdKFRhUzp7GwgtS7+R5ht5KlNTtGd7GiCpi2+86QwLoJaPUfj5up2zfkAtyKcRkOJqA2yRmMNPpa5dqh3a6dpfvzmyqiTewm+uXs7Q55cGDvmtRsyKvJnRIVNvSxAwfcdcQgrvg8pwJKVvaYRq2Nnq3AQ6KtTb7dqG5yThASJoNWr2kpQXtW0JHpLKLgLBNYuoIrA5CX4BFsufK7F+BRGk8Xgn+lhRvp4moHHwGgRH+g3rL5qB0oo9s69CtmHG5EoBjvHCR51SBtrHRUhQcQwKxWFza/PwqasPvMjAjf1MY3/BG3r8sSKPxFqzK00LXzpEzpbKzfFcZ78NY/faDGHdrTfhwgl911PM0ngFwPlvU7epBBsN/I3b+WKeZNWr/0/+z7mhNM2GOkBH4sDpVSfL5aK8EI6EC3egf8QBIgqppIZM+U0yWtbdbM5EeS+dybOL+o4LZgg//TnqQI0yK7+cr7ieIyiCmA5/gm3NRMaG8U8UFOrwnO3ZMDj/0gCPVGSWgzZOFBXUWOj4LAVWnhp7Mvrocd19elVnIsMcoWrd3kahJX1KlG7rpLG90eopBX5jvMPHW1G9YWXMSl3EYKZ5vymkn2Rgt7HGZ+AWlzfWKlexgvShpM94woxjjciVnls2qiXpV6bSDCQEvVtVJm4kvGydHPjy8ZVR9+at7fbgxjGLgD2CREZ0o0UpIDPCwbm5/fyc4PeYYnBPPS1NcuOVE0eOMFHgA6C9INoAHCvZRtzdASoCDekwsrrrE5pu86ZuWTfPN0V3xdYj2PIiftaXlsCDREQqu1am51nECtnOOoMluM6SR0cH9u8hOwE84iACMsCiAU73=',
        # 'bx-umidtoken': 'T2gAAyjt66jOpRButLKRHR8E7mD4PtXm27y5ac2i2RVJlhU3K2b-QcDkOXYqiCTMkwk=',
        # 'bx-v': '2.5.31',
        # 'source': 'web',
        # 'timezone': 'Mon Nov 17 2025 10:18:14 GMT+0800',
        # 'x-accel-buffering': 'no',
        # 'x-request-id': '19ef82fa-8400-4803-a955-2e717f644891',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'content-type': 'application/json; charset=UTF-8'
    }


    async def fetch(url):
        http_url = None

        # http_url = "https://tps.kdlapi.com/api/gettps/?secret_id=o7248wrh6fhckhw63e1f&signature=hzvgzqfv0llgmcb3ovyaudputo44i1pa&num=1&format=json&sep=1&generateType=4"
        proxy = await get_one_proxy(http_url)
        # proxy = "http://154.9.253.9:38443"
        # # proxy="https://tinyproxy.chatfire.cn"
        # # proxy="https://pp.chatfire.cn"
        # proxy = "http://110.42.51.201:38443"
        # proxy = "http://110.42.51.223:38443"
        # proxy = "http://110.42.51.223:38443"

        # proxy=None
        # proxy = "https://npjdodcrxljt.ap-northeast-1.clawcloudrun.com"

        async with httpx.AsyncClient(proxy=proxy, timeout=30, headers=headers) as client:
            resp = await client.get(url)
            logger.debug((f"{url}\n status_code: {resp.status_code}, content: {resp.text}"))


    def run():
        loop = asyncio.get_event_loop()
        # 异步发出5次请求
        tasks = [fetch(page_url) for _ in range(3)] + [fetch("https://chat.qwen.ai/api/models")]

        loop.run_until_complete(asyncio.wait(tasks))


    # run()

    url = "https://dps.kdlapi.com/api/getdps/?secret_id=o0xwup2fyhkd5qelqvoo&signature=ych2e3mdwbwo0hzwezswri5e5ob45901&num=1&format=json&sep=1&f_auth=1&generateType=4&f_et=1"
    # url = None
    arun(get_one_proxy(url))
