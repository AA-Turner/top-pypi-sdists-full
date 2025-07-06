import asyncio

from aiocache import multi_cached, Cache

DICT = {
    'a': "Z",
    'b': "Y",
    'c': "X",
    'd': "W"
}


# @multi_cached("ids", cache=Cache.REDIS, namespace="main")
# async def multi_cached_ids(ids=None):
#     return {id_: DICT[id_] for id_ in ids}


@multi_cached("keys", cache=Cache.REDIS, namespace="main")
async def multi_cached_keys(keys=None):
    return keys

# cache = Cache(Cache.REDIS, endpoint="127.0.0.1", port=6379, namespace="main")





if __name__ == "__main__":
    # test_multi_cached()
    asyncio.run(multi_cached_keys('xxx'))