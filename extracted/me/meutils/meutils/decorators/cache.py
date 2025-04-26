#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : cache
# @Time         : 2023/8/24 09:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 通用缓存， todo: redis缓存

from meutils.pipe import *
from cachetools import cached, cachedmethod, LRUCache, RRCache, TTLCache
from joblib import hashing  # hashing.hash
from joblib.func_inspect import filter_args

key_fn = lambda *args, **kwargs: hashing.hash((args, kwargs))


def ttl_cache(maxsize=128, ttl=np.inf):
    cache = cached(TTLCache(maxsize, ttl), key=key_fn)

    @wrapt.decorator
    def inner(wrapped, instance, args, kwargs):
        wrapped = cache(wrapped)
        return wrapped(*args, **kwargs)

    return inner


def hash_key(func: Callable, ignore: Optional[List] = None, *args, **kwargs):
    fn_name = func.__name__ if hasattr(func, '__name__') else 'fn'

    raw_key = dict(filter_args(func, [], list(args), kwargs))  # {'x': 1, '**': {'a': 1, 'b': 2, 'c': 3}, '*': [2, 3]}
    raw_key = {**raw_key.pop('**', {}), **raw_key}

    # self cls 看场景选择
    for arg in ignore or []:
        raw_key.pop(arg, None)

    key = hashing.hash(raw_key)

    return f"cache:{fn_name}:{key}"


def redis_cache(maxsize=128, ttl=np.inf, ignore=None, verbose=1, tag=None):
    cache = cached(TTLCache(maxsize, ttl), key=key_fn)

    @wrapt.decorator
    def inner(wrapped, instance, args, kwargs):
        wrapped = cache(wrapped)
        return wrapped(*args, **kwargs)

    return inner


@decorator
def redis_cache(func, rc=None, ttl=3, ignore=None, verbose=1, tag=None, *args, **kwargs):
    """redis 缓存"""
    ##############################################################################
    raw_key = dict(filter_args(func, [], list(args), kwargs))
    raw_key = {**raw_key.pop('**', {}), **raw_key, '__tag__': tag or func.__name__}

    # self cls 看场景选择
    ignore = (ignore or []) + [
        'api_base', 'api_key', 'openai_api_base', 'openai_api_key',
        'organization', 'openai_organization',
        'request_timeout'
    ]
    for arg in ignore:
        raw_key.pop(arg, None)

    key = hashing.hash(raw_key)

    k = f"cache:{func.__name__}:{key}"

    ##############################################################################

    if k in rc:
        return pickle.loads(rc.get(k))
    else:
        if verbose: logger.info(f"CacheKey: {k}")

        _ = func(*args, **kwargs)
        rc.set(k, pickle.dumps(_), ex=ttl)
        return _


if __name__ == '__main__':
    @ttl_cache()
    def f(x):
        time.sleep(1)
        return x

    # with timer(1):
    #     print(f([1, 2]))
    # with timer(1):
    #     print(f([1, 2]))
    #
    # with timer(2):
    #     print(f(range(10)))

    # def fn(x):
    #     time.sleep(1)
    #     return x

    # hash_key(fn, ignore=[], a=1, b=2, c=3)

    # print(filter_args(fn, [], [1, 2, 3], {'a': 1, 'b': 2, 'c': 3}))
