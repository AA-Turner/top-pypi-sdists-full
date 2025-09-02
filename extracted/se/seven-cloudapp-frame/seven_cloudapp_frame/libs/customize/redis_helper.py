# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-03-10 14:05:22
@LastEditTime: 2024-07-09 11:55:16
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework import *
from seven_framework.redis import *
from seven_cloudapp_frame.libs.common import *

class RedisExHelper:
    """
    :description: redis帮助类
    """

    redis_clients = {}

    @classmethod
    def init(self, config_dict=None, decode_responses=True, go_heavy_connection=False):
        """
        :description: redis初始化
        :param config_dict：连接串配置
        :param decode_responses：是否解码输出
        :param go_heavy_connection：是否启用连接池对象去重,共用连接池对象
        :return: redis_client
        :last_editors: HuangJianYi
        """
        if not config_dict:
            config_dict = config.get_value("redis")
        config_go_heavy_connection = share_config.get_value("go_heavy_connection", None)
        if config_go_heavy_connection != None:
            go_heavy_connection = config_go_heavy_connection
        if go_heavy_connection == False:
            redis_client = RedisHelper.redis_init(config_dict=config_dict, decode_responses=decode_responses)
            return redis_client
        else:
            key = CryptoHelper.md5_encrypt(str(config_dict))
            if key in self.redis_clients.keys():
                return self.redis_clients[key]
            redis_client = RedisHelper.redis_init(config_dict=config_dict, decode_responses=decode_responses)
            if redis_client:
                self.redis_clients[key] = redis_client
            return redis_client

    @classmethod
    def check_llen(self, queue_name, queue_lenth=100, config_dict=None):
        """
        :description: 校验队列长度
        :param queue_name：自定义队列名称
        :param queue_lenth：队列长度
        :param config_dict：连接串配置
        :return: bool False-代表达到长度限制，进行拦截
        :last_editors: HuangJianYi
        """
        redis_init = self.init(config_dict)
        list_len = redis_init.llen(queue_name)
        if int(list_len) >= int(queue_lenth):
            return True
        else:
            return False

    @classmethod
    def lpush(self, queue_name, value, expire, config_dict=None):
        """
        :description: 入队列
        :param queue_name：自定义队列名称
        :param value：加入队列的数据
        :param expire：过期时间，单位秒
        :param config_dict：连接串配置
        :return:
        :last_editors: HuangJianYi
        """
        redis_init = self.init(config_dict)
        redis_init.lpush(queue_name, json.dumps(value))
        redis_init.expire(queue_name,expire)

    @classmethod
    def lpop(self, queue_name, config_dict=None):
        """
        :description: 出队列
        :param queue_name：队列名称
        :param config_dict：连接串配置
        :return: 
        :last_editors: HuangJianYi
        """
        result = self.init(config_dict).lpop(queue_name)
        return result

    @classmethod
    def acquire_lock(self, lock_name, acquire_time=10, time_out=5, sleep_time=0.1, config_dict=None):
        """
        :description: 创建分布式锁 基于setnx命令的特性，我们就可以实现一个最简单的分布式锁了。我们通过向Redis发送 setnx 命令，然后判断Redis返回的结果是否为1，结果是1就表示setnx成功了，那本次就获得锁了，可以继续执行业务逻辑；如果结果是0，则表示setnx失败了，那本次就没有获取到锁，可以通过循环的方式一直尝试获取锁，直至其他客户端释放了锁（delete掉key）后，就可以正常执行setnx命令获取到锁
        :param lock_name：锁定名称
        :param acquire_time: 客户端等待获取锁的时间,单位秒,正常配置acquire_time<time_out
        :param time_out: 锁的超时时间,单位秒
        :param sleep_time: 轮询休眠时间,单位秒(需根据系统性能进行调整，值越小系统压力越大对系统的性能要求越高)
        :param config_dict：连接串配置
        :return 返回元组，分布式锁是否获得（True获得False未获得）和解锁钥匙（释放锁时需传入才能解锁成功）
        :last_editors: HuangJianYi
        """
        identifier = str(uuid.uuid4())
        if share_config.get_value("is_pressure_test",False): #是否进行压力测试
            return True,identifier
        end = time.time() + acquire_time
        lock = "lock:" + lock_name
        redis_init = self.init(config_dict=config_dict)
        while time.time() < end:
            if redis_init.setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                redis_init.expire(lock, time_out)
                return True,identifier
            if redis_init.ttl(lock) in [-1, None]:
                redis_init.expire(lock, time_out)
            time.sleep(sleep_time)
        return False,""

    @classmethod
    def release_lock(self, lock_name, identifier, config_dict=None):
        """
        :description: 释放分布式锁
        :param lock_name：锁定名称
        :param identifier: identifier
        :param config_dict：连接串配置
        :return bool
        :last_editors: HuangJianYi
        """
        if share_config.get_value("is_pressure_test",False): #是否进行压力测试
            return True
        lock = "lock:" + lock_name
        redis_init = self.init(config_dict=config_dict)
        pip = redis_init.pipeline(True)
        try:
            pip.watch(lock)
            lock_value = redis_init.get(lock)
            if not lock_value:
                return True
            if lock_value == identifier:
                pip.multi()
                pip.delete(lock)
                pip.execute()
                return True
            pip.unwatch()
            return False
        except Exception:
            pip.unwatch()
            return False
