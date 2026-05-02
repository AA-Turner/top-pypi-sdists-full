# coding=utf8
import threading
from contextlib import contextmanager
from functools import lru_cache
from typing import Any

# import redis2 as redis
import redis
from funboost.utils.decorators import flyweight

from redis.commands.core import Script

from funboost import funboost_config_deafult
from funboost.utils import decorators
from redis import asyncio as aioRedis


@flyweight
class AioRedis(aioRedis.Redis):
    """
    异步redis
    """

    def __init__(self, host, password, decode_responses, port: int, db=0):
        super().__init__(host=host, password=password, db=db, decode_responses=decode_responses, port=port, health_check_interval=60)


class RedisManager:
    """
    线程安全的Redis管理器单例
    相同配置返回同一个实例，避免重复创建连接
    """
    _instance_lock = threading.Lock()
    _instances: dict[tuple, 'RedisManager'] = {}  # 按配置缓存的实例
    _pools: dict[tuple, redis.ConnectionPool] = {}  # 按配置缓存的连接池

    def __new__(cls, host: str = '127.0.0.1', port: int = 6379,
                db: int = 0, password: str = None, **kwargs):
        """单例模式，相同配置返回同一个实例"""
        key = (host, port, db, password)

        # 第一次检查（无锁，提高性能）
        if key not in cls._instances:
            with cls._instance_lock:
                # 第二次检查（加锁，确保线程安全）
                if key not in cls._instances:
                    instance = super().__new__(cls)
                    instance._init_params(host, port, db, password, kwargs)
                    instance._init_redis(key)
                    cls._instances[key] = instance

        return cls._instances[key]

    def _init_params(self, host: str, port: int, db: int,
                     password: str, kwargs: dict[str, Any]):
        """初始化实例参数"""
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._kwargs = kwargs
        self._redis = None
        self._pool = None

    def _init_redis(self, key: tuple):
        """初始化Redis连接池和客户端"""
        # 检查并创建连接池
        if key not in self.__class__._pools:
            pool_kwargs = {
                'host': self._host,
                'port': self._port,
                'db': self._db,
                'password': self._password,
                'max_connections': 100,  # 限制最大连接数
                'socket_keepalive': True,
                'retry_on_timeout': True,
                'health_check_interval': 30,  # 健康检查间隔
            }

            # 合并额外的连接池参数
            pool_kwargs.update(self._kwargs)

            self.__class__._pools[key] = redis.ConnectionPool(**pool_kwargs)

        # 获取连接池
        self._pool = self.__class__._pools[key]

        # 创建Redis客户端
        self._redis = redis.Redis(connection_pool=self._pool)

        # 测试连接
        self._ping()

    def _ping(self):
        """测试连接是否正常"""
        try:
            self._redis.ping()
        except redis.ConnectionError as e:
            raise ConnectionError(f"Redis连接失败: {e}")

    def get_redis(self) -> redis.Redis:
        """
        获取Redis客户端实例
        :rtype: redis.Redis
        """
        return self._redis

    @property
    def connection_pool(self) -> redis.ConnectionPool:
        """获取连接池"""
        return self._pool

    @contextmanager
    def get_connection(self):
        """
        使用上下文管理器获取原生连接
        确保连接正确释放回连接池
        """
        conn = None
        try:
            conn = self._pool.get_connection('_')
            yield conn
        finally:
            if conn:
                self._pool.release(conn)

    def disconnect(self, inuse_connections: bool = True):
        """断开连接池中的所有连接"""
        self._pool.disconnect(inuse_connections=inuse_connections)

    def cleanup(self):
        """
        清理当前实例的Redis连接
        注意：这不会删除单例实例，只会清理连接
        """
        if self._redis:
            self._redis.close()
            self._redis = None

    @classmethod
    def cleanup_all(cls):
        """清理所有Redis连接（谨慎使用）"""
        for instance in cls._instances.values():
            instance.cleanup()

        # 清空连接池
        for pool in cls._pools.values():
            pool.disconnect()

        cls._instances.clear()
        cls._pools.clear()

    @classmethod
    def get_instance_count(cls) -> int:
        """获取当前管理的实例数量"""
        return len(cls._instances)

    @classmethod
    def get_pool_count(cls) -> int:
        """获取当前连接池数量"""
        return len(cls._pools)

    def __del__(self):
        """析构时清理连接"""
        try:
            self.cleanup()
        except:
            pass


# noinspection PyArgumentEqualDefault
class RedisMixin(object):
    """
    可以被作为万能mixin能被继承，也可以单独实例化使用。
    """

    def __init__(self, redis_host=None):
        self.redis_host = redis_host

    @property
    # @decorators.cached_method_result
    def redis_db0(self):
        return RedisManager(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                            password=funboost_config_deafult.REDIS_PASSWORD, db=0).get_redis()

    @property
    # @decorators.cached_method_result
    def redis_db8(self):
        return RedisManager(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                            password=funboost_config_deafult.REDIS_PASSWORD, db=8).get_redis()

    @property
    # @decorators.cached_method_result
    def redis_db7(self):
        return RedisManager(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                            password=funboost_config_deafult.REDIS_PASSWORD, db=7).get_redis()

    @property
    # @decorators.cached_method_result
    def redis_db6(self):
        return RedisManager(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                            password=funboost_config_deafult.REDIS_PASSWORD, db=6).get_redis()

    @property
    # @decorators.cached_method_result
    def redis_db_frame(self):
        return RedisManager(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                            password=funboost_config_deafult.REDIS_PASSWORD, db=funboost_config_deafult.REDIS_DB).get_redis()

    @property
    # @decorators.cached_method_result
    def async_redis_db_frame(self):
        return AioRedis(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                        password=funboost_config_deafult.REDIS_PASSWORD, db=funboost_config_deafult.REDIS_DB, decode_responses=True)

    @property
    # @decorators.cached_method_result
    def redis_db_frame_version3(self):
        ''' redis 3和2 入参和返回差别很大，都要使用'''
        return RedisManager(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                     password=funboost_config_deafult.REDIS_PASSWORD, db=funboost_config_deafult.REDIS_DB).get_redis()

    @property
    # @decorators.cached_method_result
    def redis_db_filter_and_rpc_result(self):
        return RedisManager(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                            password=funboost_config_deafult.REDIS_PASSWORD, db=funboost_config_deafult.REDIS_DB_FILTER_AND_RPC_RESULT).get_redis()


    def timestamp(self):
        """ 如果是多台机器做分布式控频 乃至确认消费，每台机器取自己的时间，如果各机器的时间戳不一致会发生问题，改成统一使用从redis服务端获取时间。"""
        time_tuple = self.redis_db_frame_version3.time()
        # print(time_tuple)
        return time_tuple[0] + time_tuple[1] / 1000000

    @lru_cache
    def register_script(self, script: str) -> Script:
        return self.redis_db_frame_version3.register_script(script)


class AioRedisMixin(object):
    def __init__(self, redis_host=None):
        self.redis_host = redis_host
    @property
    @decorators.cached_method_result
    def aioredis_db_filter_and_rpc_result(self):
        return AioRedis(host=self.redis_host or funboost_config_deafult.REDIS_HOST, port=funboost_config_deafult.REDIS_PORT,
                        password=funboost_config_deafult.REDIS_PASSWORD, db=funboost_config_deafult.REDIS_DB_FILTER_AND_RPC_RESULT, decode_responses=True)
