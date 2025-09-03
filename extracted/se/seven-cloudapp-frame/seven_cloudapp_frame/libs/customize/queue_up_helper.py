# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-30 09:22:51
@LastEditTime: 2025-09-02 15:20:51
@LastEditors: HuangJianYi
@Description: 排队系统帮助类
"""
from seven_framework import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.db_models.queueup.queueup_log_model import *


class QueueUpHelper:
    """
    :description: 排队系统帮助类 提供获取小程序总排队人数、获取用户当前排队数、获取用户正在办理中的队列信息、加入排队、退出排队、查询单个排队情况、批量查询某用户排队情况(只包含已排队的信息)、批量查询某用户排队情况(包含已排队和未排队的信息)、更新可操作时间、签到等功能；
    踢人规则1：第一个在办理中，第二个用户的过期时间=第一个结束时间+8*1，第三个=第一个结束时间+8*2，以此类推；第一个没在办理中，第一个过期时间是8*1，第二个是8*2，第三个是8*3，以此类推；
    踢人规则2：如果都没有正在办理中，那么取上次办理人退出的时间作为排在第一位人员的开始时间，进行倒计时，没有上次办理人退出时间的话，则取当前第一位人员的入队时间进行倒计时；
    用户信息存在hash,排行信息存在zset,排队次数存在user_zset
    """
    logger_error = Logger.get_logger_by_name("log_error")
    logger_info = Logger.get_logger_by_name("log_info")

    @classmethod
    def _get_zset_name(self, app_id, queue_name):
        """
        :description: 排行信息集合名称（集合用于排行榜，排第一的优先操作）
        :param app_id：应用标识
        :param queue_name：队列名称
        :return: 
        :last_editors: HuangJianYi
        """
        zset_name = "queueup_zset"
        if app_id:
            zset_name += "_" + str(app_id)
        if queue_name:
            zset_name += ":" + str(queue_name)
        return zset_name

    @classmethod
    def _get_count_name(self, app_id, queue_name):
        """
        :description: 获取排队号计数名称
        :param app_id：应用标识
        :param queue_name：队列名称
        :return: 
        :last_editors: HuangJianYi
        """
        count_name = "queueup_count"
        if app_id:
            count_name += "_" + str(app_id)
        if queue_name:
            count_name += ":" + str(SevenHelper.get_now_day_int()) + "_" + str(queue_name)
        return count_name

    @classmethod
    def _get_user_hash_name(self, app_id):
        """
        :description: 用户关联队列的hash名称
        :param app_id：应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        hash_name = "queueup_user_list"
        if app_id:
            hash_name += "_" + str(app_id)
        return hash_name

    @classmethod
    def _get_user_zset_name(self, app_id):
        """
        :description: 用户在小程序内的排队次数集合名称
        :param app_id：应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        zset_name = "queueup_zset_user"
        if app_id:
            zset_name += "_" + str(app_id)
        return zset_name

    @classmethod
    def _get_popdate_hash_name(self, app_id):
        """
        :description: 办理中的用户退出队列的时间列表名称
        :param app_id：应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        hash_name = "queueup_popdate_list"
        if app_id:
            hash_name += "_" + str(app_id)
        return hash_name

    @classmethod
    def _get_queue_no(self, app_id, queue_name):
        """
        :description: 获取排队号
        :param app_id：应用标识
        :param queue_name：队列名称
        :return: 
        :last_editors: HuangJianYi
        """
        count_name = self._get_count_name(app_id, queue_name)
        redis_init = SevenHelper.redis_init()
        queue_no = redis_init.incr(count_name, 1)
        redis_init.expire(count_name, 24 * 3600)
        return queue_no

    @classmethod
    def _get_queue_num(self, app_id, queue_name):
        """
        :description: 获取当前排队人数
        :param app_id：应用标识
        :param queue_name：队列名称
        :return: 
        :last_editors: HuangJianYi
        """
        zset_name = self._get_zset_name(app_id, queue_name)
        redis_init = SevenHelper.redis_init()
        return redis_init.zcard(zset_name)

    @classmethod
    def _get_app_user_num(self, app_id):
        """
        :description: 获取小程序总排队人数
        :param app_id：应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        user_zset_name = self._get_user_zset_name(app_id)
        redis_init = SevenHelper.redis_init()
        return redis_init.zcount(user_zset_name, 1, 1000000000000)

    @classmethod
    def get_user_queue_num(self, app_id, user_id):
        """
        :description: 获取用户当前排队数
        :param app_id：应用标识
        :param user_id：用户标识
        :return: 
        :last_editors: HuangJianYi
        """
        user_zset_name = self._get_user_zset_name(app_id)
        redis_init = SevenHelper.redis_init()
        queue_num = redis_init.zscore(user_zset_name, str(user_id))
        if queue_num is None:
            return 0
        return queue_num

    @classmethod
    def get_process_user_queue(self, app_id, user_id):
        """
        :description: 获取用户正在办理中的队列信息
        :param app_id：应用标识
        :param user_id：用户标识
        :return: 队列信息，没有返回None
        :last_editors: HuangJianYi
        """
        process_queue = None
        invoke_result_data = self.muti_user_query(app_id, user_id)
        if invoke_result_data.success == False:
            return process_queue
        else:
            for item in invoke_result_data.data:
                if item["progress_status"] == 2:
                    process_queue = item
                    break
            return process_queue

    @classmethod
    def queue(self, app_id, queue_name, user_id, user_nick="", avatar="", queue_length=10, app_limit_user_num=500, info_dict={}, limit_user_queue_num=0):
        """
        :description: 加入排队
        :param app_id：应用标识
        :param queue_name：队列名称
        :param user_id 用户标识
        :param user_nick 用户昵称
        :param avatar 头像
        :param queue_length：队列的长度
        :param app_limit_user_num：小程序内总排队人数上限
        :param info_dict：信息字典,用于存储业务端需要的数据
        :param limit_user_queue_num：限制用户可以加入的队列数
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            acquire_lock_name = "queueup_queue"
            if app_id:
                acquire_lock_name += "_" + str(app_id)
            acquire_lock_name += ":" + str(queue_name)

            acquire_lock_status, identifier = SevenHelper.redis_acquire_lock(acquire_lock_name)
            if acquire_lock_status == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "acquire_lock"
                invoke_result_data.error_message = "系统繁忙,请稍后再试"
                return invoke_result_data
            redis_init = SevenHelper.redis_init()
            if app_limit_user_num > 0 and self._get_app_user_num(app_id) >= app_limit_user_num:
                # 防止有些队列，用户排到队之后直接退出，导致没有请求，无法触发自动踢人的清理，需要全应用清理一次，释放异常占用的应用总人数
                self.muti_expire_user_pop(app_id)
                invoke_result_data.success = False
                invoke_result_data.error_code = "total_limit"
                invoke_result_data.error_message = "抱歉~当前活动排队人数过多，请稍后再试"
                return invoke_result_data
            if limit_user_queue_num > 0 and QueueUpHelper.get_user_queue_num(app_id, user_id) >= limit_user_queue_num:
                invoke_result_data.success = False
                invoke_result_data.error_code = "user_limit"
                invoke_result_data.error_message = "抱歉~当前可排队列已达上限，请稍后再试"
                return invoke_result_data

            zset_name = self._get_zset_name(app_id, queue_name)
            data = str(user_id)
            expire_time = 7 * 24 * 3600
            if not redis_init.zscore(zset_name, data):
                if self._get_queue_num(app_id, queue_name) >= queue_length:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "queue_limit"
                    invoke_result_data.error_message = "排队失败,当前排队人数已达上限"
                    return invoke_result_data
                queue_no = int(str(SevenHelper.get_now_day_int()) + str(self._get_queue_no(app_id, queue_name)).zfill(4))
                redis_init.zadd(zset_name, {data: queue_no})
                redis_init.expire(zset_name, expire_time)

                user_zset_name = self._get_user_zset_name(app_id)
                redis_init.zincrby(user_zset_name, 1, data)
                redis_init.expire(user_zset_name, expire_time)

                start_timestamp = TimeHelper.get_now_timestamp()

                hash_value = {}
                hash_value["queue_name"] = queue_name  # 排队名称
                hash_value["queue_no"] = queue_no  # 排队号
                hash_value["user_id"] = data  # 用户标识
                hash_value["user_nick"] = user_nick  # 用户昵称
                hash_value["avatar"] = avatar  # 头像
                hash_value["progress_status"] = 1  # 进度0未排队1已排队2办理中
                hash_value["queue_timestamp"] = start_timestamp  # 入队时间搓
                hash_value["queue_date"] = TimeHelper.timestamp_to_format_time(start_timestamp)  # 入队时间
                hash_value["info_json"] = info_dict
                info_dict['queue_no'] = queue_no

                queue_index = SevenHelper.to_int(redis_init.zrank(zset_name, data)) + 1
                if queue_index == 1:
                    redis_init.hdel(self._get_popdate_hash_name(app_id), zset_name)
                # 添加排队信息
                hash_name = self._get_user_hash_name(app_id)
                hash_key = f"userid_{data}_queuename_{queue_name}"
                redis_init.hsetnx(hash_name, hash_key, SevenHelper.json_dumps(hash_value))
                redis_init.expire(hash_name, expire_time)

                result_data = {}
                result_data["queue_no"] = hash_value["queue_no"]  #排队号
                result_data["queue_num"] = self._get_queue_num(app_id, queue_name)  #当前排队人数
                result_data["queue_index"] = queue_index  #当前位置
                result_data["before_num"] = queue_index - 1  #排在前面的人数
                invoke_result_data.data = result_data

                if share_config.get_value("queue_is_log", False):
                    self.add_log(app_id=app_id, queue_name=queue_name, user_id=user_id, operate_type=QueueupOperateType.join.value, remain_time=0, info_json=info_dict)

                return invoke_result_data
            else:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "您已在队列中，请勿重复排队"
                return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【加入排队】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起，加入队列失败，请稍后再试"
            return invoke_result_data
        finally:
            SevenHelper.redis_release_lock(acquire_lock_name, identifier)

    @classmethod
    def _set_last_pop_date(self, app_id, redis_init, hash_key):
        """
        :description: 设置办理中的用户退出队列的时间
        :param app_id：应用标识
        :param redis_init：redis_init
        :param hash_key：hash_key
        :return: 
        :last_editors: HuangJianYi
        """
        hash_name = self._get_popdate_hash_name(app_id)
        redis_init.hset(hash_name, hash_key, str(TimeHelper.get_now_timestamp()))
        redis_init.expire(hash_name, 7 * 24 * 3600)

    @classmethod
    def pop(self, app_id, queue_name, user_id, is_user_operate=True):
        """
        :description: 退出排队
        :param app_id：应用标识
        :param queue_name：队列名称
        :param user_id 用户标识
        :param is_user_operate 是否用户操作(1-是 0-否)
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            cache_key = f"queueup_pop"
            if app_id:
                cache_key += "_" + str(app_id)
            cache_key += ":" + str(queue_name) + "_" + str(user_id)
            if SevenHelper.is_continue_request(cache_key, expire=1 * 1000) == True:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "对不起,请1秒后再试"
                return invoke_result_data
            zset_name = self._get_zset_name(app_id, queue_name)
            data = str(user_id)
            redis_init = SevenHelper.redis_init()
            if redis_init.zscore(zset_name, data):
                if SevenHelper.to_int(redis_init.zrank(zset_name, data)) + 1 == 1:
                    self._set_last_pop_date(app_id, redis_init, zset_name)

                hash_value = redis_init.hget(self._get_user_hash_name(app_id), f"userid_{data}_queuename_{queue_name}")
                hash_value = SevenHelper.json_loads(hash_value) if hash_value else {}
                end_timestamp = hash_value["end_timestamp"] if hash_value.__contains__("end_timestamp") else 0

                pipeline = redis_init.pipeline()
                pipeline.zrem(zset_name, data)
                pipeline.zincrby(self._get_user_zset_name(app_id), -1, data)
                pipeline.hdel(self._get_user_hash_name(app_id), f"userid_{data}_queuename_{queue_name}")
                pipeline.execute()
                if share_config.get_value("queue_is_log", False):
                    operate_type = QueueupOperateType.manual_exit.value if is_user_operate else QueueupOperateType.auto_exit.value
                    remain_time = end_timestamp - TimeHelper.get_now_timestamp()
                    remain_time = remain_time if remain_time > 0 else 0
                    self.add_log(app_id=app_id, queue_name=queue_name, user_id=user_id, operate_type=operate_type, remain_time=remain_time, info_json=hash_value['info_json'])
                return invoke_result_data
            else:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "未查到该用户的排队情况,请先排队"
                return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【退出排队】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "退出排队失败"
            return invoke_result_data

    @classmethod
    def pop_by_user_id(self, app_id, user_id, progress_status=1, is_user_operate=True):
        """
        :description: 指定用户退出参与的队列
        :param app_id：应用标识
        :param user_id：用户标识
        :param progress_status：0-全部 1-已排队 2-办理中
        :param is_user_operate 是否用户操作(1-是 0-否)
        :return: 
        :last_editors: HuangJianYi
        """
        if SevenHelper.is_continue_request(f"pop_by_user_id:{app_id}_{user_id}", 200) == False:
            redis_init = SevenHelper.redis_init()
            data = str(user_id)
            hash_name = self._get_user_hash_name(app_id)
            match_result = redis_init.hscan_iter(hash_name, match=f'userid_{data}_*')
            for item in match_result:
                hash_value = SevenHelper.json_loads(item[1])
                if progress_status > 0 and hash_value["progress_status"] != progress_status:
                    continue
                self.pop(app_id, hash_value["queue_name"], data, is_user_operate)

    @classmethod
    def expire_user_pop(self, app_id, queue_name):
        """
        :description: 将过期用户从队列中退出
        :param app_id：应用标识
        :param queue_name：队列名称
        :return: 
        :last_editors: HuangJianYi
        """
        if SevenHelper.is_continue_request(f"expire_user_pop:{app_id}_{queue_name}", 300) == False:
            try:
                redis_init = SevenHelper.redis_init()
                #删除用户排队次数小于等于0的数据
                redis_init.zremrangebyscore(self._get_user_zset_name(app_id), -10, 0)

                zset_name = self._get_zset_name(app_id, queue_name)
                hash_name = self._get_user_hash_name(app_id)
                value_list = redis_init.zrange(zset_name, 0, 1000)
                if len(value_list) > 0:
                    now_timestamp = TimeHelper.get_now_timestamp()
                    first_is_process = False
                    first_end_timestamp = 0
                    first_hash_key = f"userid_{value_list[0]}_queuename_{queue_name}"
                    first_hash_value = redis_init.hget(hash_name, first_hash_key)
                    if first_hash_value:
                        first_hash_value = SevenHelper.json_loads(first_hash_value)
                        if first_hash_value["progress_status"] == 2:
                            first_is_process = True
                            first_end_timestamp = first_hash_value["end_timestamp"]
                    hash_key_list = []
                    for data in value_list:
                        hash_key = f"userid_{data}_queuename_{queue_name}"
                        hash_key_list.append(hash_key)
                    string_list = redis_init.hmget(hash_name, hash_key_list)
                    hash_value_list = []
                    if len(string_list) > 0:
                        for item in string_list:
                            value = SevenHelper.json_loads(item)
                            if value:
                                hash_value_list.append(value)
                    for i in range(len(value_list)):
                        data = value_list[i]
                        hash_value = [hash_value for hash_value in hash_value_list if hash_value["user_id"] == data]
                        hash_value = hash_value[0] if len(hash_value) > 0 else None
                        is_delete = False
                        if hash_value:
                            if first_is_process == True and i == 0:
                                if now_timestamp > hash_value["end_timestamp"]:
                                    is_delete = True
                                    self.logger_info.info("【踢掉办理用户1】" + SevenHelper.json_dumps({"zset_name": zset_name, "first_hash_value": first_hash_value, "user_id": data, "now_timestamp": now_timestamp, "pop_timestamp": hash_value["end_timestamp"]}))
                            elif first_is_process == True and i > 0:
                                if now_timestamp > first_end_timestamp + (i * int(share_config.get_value("queue_confirm_time", 8))):
                                    is_delete = True
                                    self.logger_info.info("【踢掉办理用户2】" + SevenHelper.json_dumps({"zset_name": zset_name, "first_hash_value": first_hash_value, "user_id": data, "now_timestamp": now_timestamp, "pop_timestamp": first_end_timestamp + (i * int(share_config.get_value("queue_confirm_time", 8)))}))
                            else:
                                pop_timestamp = redis_init.hget(self._get_popdate_hash_name(app_id), zset_name)
                                if pop_timestamp:
                                    pop_timestamp = int(pop_timestamp)
                                else:
                                    pop_timestamp = hash_value["queue_timestamp"]
                                if now_timestamp > pop_timestamp + ((i + 1) * int(share_config.get_value("queue_confirm_time", 8))):
                                    is_delete = True
                                    self.logger_info.info("【踢掉办理用户3】" + SevenHelper.json_dumps({"zset_name": zset_name, "first_hash_value": first_hash_value, "user_id": data, "now_timestamp": now_timestamp, "pop_timestamp": pop_timestamp + ((i + 1) * int(share_config.get_value("queue_confirm_time", 8)))}))
                        else:
                            is_delete = True
                        if is_delete == True:
                            self._set_last_pop_date(app_id, redis_init, zset_name)
                            pipeline = redis_init.pipeline()
                            pipeline.hdel(hash_name, f"userid_{data}_queuename_{queue_name}")
                            pipeline.zrem(zset_name, data)
                            pipeline.zincrby(self._get_user_zset_name(app_id), -1, data)
                            pipeline.execute()
                            if share_config.get_value("queue_is_log", False):
                                info_json = hash_value['info_json'] if hash_value else {}
                                self.add_log(app_id=app_id, queue_name=queue_name, user_id=data, operate_type=QueueupOperateType.auto_exit.value, remain_time=0, info_json=info_json)
            except Exception as ex:
                self.logger_error.error("【删除未操作的排队信息】" + traceback.format_exc())

    @classmethod
    def muti_expire_user_pop(self, app_id):
        """
        :description: 批量踢掉过期用户，防止占用队列和应用总人数
        :param app_id：应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        zset_keys = []
        pattern = f"queueup_zset_{app_id}:*"
        redis_init = SevenHelper.redis_init()
        if SevenHelper.is_continue_request(f"muti_expire_user_pop:{app_id}", 1000 * 60) is False:
            try:
                cursor = '0'
                while cursor != 0:
                    cursor, keys = redis_init.scan(cursor=cursor, match=pattern)
                    for key in keys:
                        if redis_init.type(key) == 'zset':  # 检查键类型
                            zset_keys.append(key)
                for item in zset_keys:
                    app_id = str(item.split(':')[0]).replace("queueup_zset_", "")
                    queue_name = str(item.split(':')[1])
                    QueueUpHelper.expire_user_pop(app_id, queue_name)
            except Exception as ex:
                pass

    @classmethod
    def query(self, app_id, queue_name, user_id, is_pop=True):
        """
        :description: 查询某用户排队情况
        :param app_id：应用标识
        :param queue_name：队列名称
        :param user_id：用户标识
        :param is_pop：是否踢掉过期用户
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            redis_init = SevenHelper.redis_init()
            zset_name = self._get_zset_name(app_id, queue_name)
            data = str(user_id)
            #踢掉过期用户
            if is_pop == True:
                self.expire_user_pop(app_id, queue_name)

            #判断是否存在排队信息
            score = redis_init.zscore(zset_name, data)
            index = redis_init.zrank(zset_name, data)
            if score and index is not None:
                query_user = {}
                query_user["queue_name"] = queue_name  #队列名称
                query_user["queue_no"] = int(score)  #排队号
                query_user["total_num"] = self._get_queue_num(app_id, queue_name)  #总排队人数
                query_user["queue_index"] = int(index) + 1  #当前位置
                query_user["before_num"] = query_user["queue_index"] - 1  #排在前面的人数
                hash_value = redis_init.hget(self._get_user_hash_name(app_id), f"userid_{data}_queuename_{queue_name}")
                hash_value = SevenHelper.json_loads(hash_value) if hash_value else {}
                query_user["user_id"] = hash_value["user_id"] if hash_value.__contains__("user_id") else ''
                query_user["user_nick"] = hash_value["user_nick"] if hash_value.__contains__("user_nick") else ''
                query_user["avatar"] = hash_value["avatar"] if hash_value.__contains__("avatar") else ''
                query_user["start_date"] = hash_value["start_date"] if hash_value.__contains__("start_date") else ''
                query_user["end_date"] = hash_value["end_date"] if hash_value.__contains__("end_date") else ''
                query_user["end_timestamp"] = hash_value["end_timestamp"] if hash_value.__contains__("end_timestamp") else ''
                query_user["queue_date"] = hash_value["queue_date"] if hash_value.__contains__("queue_date") else ''
                query_user["queue_timestamp"] = hash_value["queue_timestamp"] if hash_value.__contains__("queue_timestamp") else 0
                query_user["progress_status"] = hash_value["progress_status"] if hash_value.__contains__("progress_status") else 0  #进度0未排队1已排队2办理中
                query_user["info_json"] = hash_value["info_json"] if hash_value.__contains__("info_json") else {}
                invoke_result_data.data = query_user
                return invoke_result_data
            else:
                query_user = {}
                query_user["queue_name"] = queue_name  #队列名称
                query_user["progress_status"] = 0  #进度0未排队1已排队2办理中
                query_user["before_num"] = self._get_queue_num(app_id, queue_name)  #排在前面的人数
                invoke_result_data.data = query_user
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "您当前不在队列中，请先排队"
                return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【查询某用户排队情况】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "您当前不在队列中，请先排队"
            return invoke_result_data

    @classmethod
    def query_all(self, app_id, queue_name):
        """
        :description: 查询指定队列的所有用户信息，出现请求时间太长，请使用query_list方法
        :param app_id：应用标识
        :param queue_name：队列名称
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.data = []
        zset_name = QueueUpHelper._get_zset_name(app_id, queue_name)
        redis_init = SevenHelper.redis_init()
        user_id_list = redis_init.zrange(zset_name, 0, -1)
        if len(user_id_list) <= 0:
            return invoke_result_data
        key_list = []
        for user_id in user_id_list:
            key = f"userid_{user_id}_queuename_{queue_name}"
            key_list.append(key)
        # 用户列表
        user_list = []
        # 踢掉过期用户
        QueueUpHelper.expire_user_pop(app_id, queue_name)
        # 总排队人数
        total_num = QueueUpHelper._get_queue_num(app_id, queue_name)
        hash_value_list = redis_init.hmget(QueueUpHelper._get_user_hash_name(app_id), key_list)
        for item in hash_value_list:
            hash_value = SevenHelper.json_loads(item) if item else {}
            if not isinstance(hash_value, dict):
                continue
            query_user = {}
            query_user["queue_name"] = hash_value.get("queue_name", '')
            query_user["total_num"] = total_num
            query_user["user_id"] = hash_value.get("user_id", '')
            query_user["user_nick"] = hash_value.get("user_nick", '')
            query_user["avatar"] = hash_value.get("avatar",'')
            query_user["queue_timestamp"] = hash_value.get("queue_timestamp", 0)
            query_user["progress_status"] = hash_value.get("progress_status", 0)  #进度0未排队1已排队2办理中
            query_user["start_date"] = hash_value.get("start_date", '')
            query_user["end_date"] = hash_value.get("end_date", '')
            index = redis_init.zrank(zset_name, str(query_user["user_id"]))
            if index is not None:
                query_user["queue_index"] = int(index) + 1  #当前位置
                query_user["before_num"] = query_user["queue_index"] - 1  #排在前面的人数
                user_list.append(query_user)
        invoke_result_data.data = user_list
        return invoke_result_data

    @classmethod
    def query_list(self, app_id, queue_name, user_id, limit=10, is_pop=True):
        """
        :description: 查询指定队列的所有用户信息
        :param app_id：应用标识
        :param queue_name：队列名称
        :param user_id：用户标识
        :param limit：查询数量
        :param is_pop：是否踢掉过期用户
        :return: dict
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.data = {}
        zset_name = self._get_zset_name(app_id, queue_name)
        redis_init = SevenHelper.redis_init()
        user_id_list = redis_init.zrange(zset_name,0,limit)
        if len(user_id_list) <= 0:
            return invoke_result_data

        result = {}
        result["queue_name"] = queue_name  #队列名称
        result["user_list"] = [] # 用户列表
        result["current_user"] = {} # 当前用户

        query_invoke_result_data = self.query(app_id, queue_name, user_id, is_pop)
        if query_invoke_result_data.success == True:
            result["current_user"] = query_invoke_result_data.data
            result["current_user"]["service_timestamp"] = TimeHelper.get_now_timestamp()
        result["total_num"] = self._get_queue_num(app_id, queue_name)  #总排队人数
        key_list = []
        for item in user_id_list:
            key_list.append(f"userid_{item}_queuename_{queue_name}")
        hash_value_list = redis_init.hmget(self._get_user_hash_name(app_id), key_list)
        for item in hash_value_list:
            if not item:
                continue
            hash_value = SevenHelper.json_loads(item)
            if not isinstance(hash_value, dict):
                continue
            query_user = {}
            query_user["user_id"] = hash_value.get("user_id", "")
            query_user["user_nick"] = hash_value.get("user_nick", "")
            query_user["avatar"] = hash_value.get("avatar", "")
            query_user["queue_timestamp"] = hash_value.get("queue_timestamp", 0)
            query_user["progress_status"] = hash_value.get("progress_status", 0)  #进度0未排队1已排队2办理中
            result["user_list"].append(query_user)

        invoke_result_data.data = result
        return invoke_result_data

    @classmethod
    def muti_user_query(self, app_id, user_id):
        """
        :description: 批量查询某用户排队情况(只包含已排队的信息)
        :param app_id：应用标识
        :param user_id：用户标识
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.data = []
        try:
            redis_init = SevenHelper.redis_init()
            hash_name = self._get_user_hash_name(app_id)
            data = str(user_id)
            match_result = redis_init.hscan_iter(hash_name, match=f'userid_{data}_*')
            for item in match_result:
                hash_value = SevenHelper.json_loads(item[1])
                query_invoke_result_data = self.query(app_id, hash_value["queue_name"], user_id, False)
                if query_invoke_result_data.success == True:
                    invoke_result_data.data.append(query_invoke_result_data.data)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【批量查询某用户排队情况】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "您当前不在队列中，请先排队"
            return invoke_result_data

    @classmethod
    def muti_queue_query(self, app_id, queue_name_list, user_id):
        """
        :description: 批量查询某用户排队情况(包含已排队和未排队的信息)
        :param app_id：应用标识
        :param queue_name_list：查询队列集合
        :param user_id：用户标识
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.data = []
        try:
            for queue_name in queue_name_list:
                query_invoke_result_data = self.query(app_id, queue_name, user_id, False)
                invoke_result_data.data.append(query_invoke_result_data.data)
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【批量查询排队情况】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "未查到排队情况"
            return invoke_result_data

    @classmethod
    def update_time(self, app_id, queue_name, user_id, operate_time=0, is_reset=False):
        """
        :description: 更新可操作时间，用于操作倒计时，时间到则踢出队列
        :param app_id：应用标识
        :param queue_name：队列名称
        :param user_id：用户标识
        :param operate_time：增加的操作时间，单位秒
        :param is_reset：是否重置开始时间和结束时间
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            redis_init = SevenHelper.redis_init()
            zset_name = self._get_zset_name(app_id, queue_name)
            data = str(user_id)
            score = redis_init.zscore(zset_name, data)
            if score and operate_time > 0:
                hash_name = self._get_user_hash_name(app_id)
                hash_key = f"userid_{data}_queuename_{queue_name}"
                hash_value = redis_init.hget(hash_name, hash_key)
                if not hash_value:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "更新可操作时间失败"
                    return invoke_result_data
                hash_value = SevenHelper.json_loads(hash_value)
                if hash_value["progress_status"] != 2:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "未签到,不能更新可操作时间"
                    return invoke_result_data
                if is_reset == True:
                    start_timestamp = TimeHelper.get_now_timestamp()
                    hash_value["start_timestamp"] = start_timestamp
                    hash_value["start_date"] = TimeHelper.timestamp_to_format_time(start_timestamp)
                    end_timestamp = start_timestamp + int(operate_time)
                    hash_value["end_timestamp"] = end_timestamp
                    hash_value["end_date"] = TimeHelper.timestamp_to_format_time(end_timestamp)
                else:
                    queue_operate_total_time = int(share_config.get_value("queue_operate_total_time", 0))
                    now_date = TimeHelper.get_now_datetime()
                    expire_date = TimeHelper.timestamp_to_datetime(hash_value["end_timestamp"])
                    if expire_date > now_date and queue_operate_total_time > 0:
                        remain_time = TimeHelper.difference_seconds(expire_date, now_date)
                        operate_time = queue_operate_total_time - remain_time if remain_time + operate_time > queue_operate_total_time else operate_time
                    end_timestamp = hash_value["end_timestamp"] + int(operate_time)
                    hash_value["end_timestamp"] = end_timestamp
                    hash_value["end_date"] = TimeHelper.timestamp_to_format_time(end_timestamp)
                redis_init.hset(hash_name, hash_key, SevenHelper.json_dumps(hash_value))
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【更新可操作时间】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "更新可操作时间失败"
            return invoke_result_data

    @classmethod
    def sign(self, app_id, queue_name, user_id, pop_other_queue=True, queue_operate_time=None):
        """
        :description: 签到操作（证明排队的人做出应答，开始办理业务，更新开始操作时间）
        :param app_id：应用标识
        :param queue_name：队列名称
        :param user_id：用户标识
        :param queue_operate_time：排到队可操作时间
        :param user_id：用户标识
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            acquire_lock_name = f"queueup_sign"
            if app_id:
                acquire_lock_name += "_" + str(app_id)
            acquire_lock_name += ":" + str(queue_name)
            acquire_lock_name += ":" + str(user_id)
            acquire_lock_status, identifier = SevenHelper.redis_acquire_lock(acquire_lock_name)
            if acquire_lock_status == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "acquire_lock"
                invoke_result_data.error_message = "系统繁忙,请稍后再试"
                return invoke_result_data

            redis_init = SevenHelper.redis_init()
            zset_name = self._get_zset_name(app_id, queue_name)
            data = str(user_id)
            #判断是否存在排队信息
            score = redis_init.zscore(zset_name, data)
            if score:
                queue_index = SevenHelper.to_int(redis_init.zrank(zset_name, data)) + 1  #当前位置
                if queue_index != 1:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "前面还有人在队列中，请耐心等待"
                    return invoke_result_data
                start_timestamp = TimeHelper.get_now_timestamp()
                if not queue_operate_time:
                    queue_operate_time = share_config.get_value("queue_operate_time", 300)
                end_timestamp = start_timestamp + int(queue_operate_time)  #操作时间，单位秒
                hash_name = self._get_user_hash_name(app_id)
                hash_key = f"userid_{data}_queuename_{queue_name}"
                hash_value = redis_init.hget(hash_name, hash_key)
                if not hash_value:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "您当前不在队列中，请先排队"
                    return invoke_result_data
                hash_value = SevenHelper.json_loads(hash_value)
                if hash_value["progress_status"] == 2:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "您已在队列中，请勿重复排队"
                    return invoke_result_data

                hash_value["start_timestamp"] = start_timestamp
                hash_value["end_timestamp"] = end_timestamp
                hash_value["start_date"] = TimeHelper.timestamp_to_format_time(start_timestamp)
                hash_value["end_date"] = TimeHelper.timestamp_to_format_time(end_timestamp)
                hash_value["progress_status"] = 2
                redis_init.hset(hash_name, hash_key, SevenHelper.json_dumps(hash_value))
                if share_config.get_value("queue_is_log", False):
                    self.add_log(app_id=app_id, queue_name=queue_name, user_id=user_id, operate_type=QueueupOperateType.line_up.value, remain_time=queue_operate_time, info_json=hash_value['info_json'])
                if pop_other_queue == True:
                    #踢掉在其他队列中的排队
                    match_result = redis_init.hscan_iter(hash_name, match=f'userid_{data}_*')
                    for item in match_result:
                        hash_value = SevenHelper.json_loads(item[1])
                        if hash_value["queue_name"] == queue_name:
                            continue
                        self.pop(app_id, hash_value["queue_name"], data, False)
                invoke_result_data.data = hash_value
                return invoke_result_data
            else:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "您当前不在队列中，请先排队"
                return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【签到操作】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "您当前不在队列中，请先排队"
            return invoke_result_data
        finally:
            SevenHelper.redis_release_lock(acquire_lock_name, identifier)

    @classmethod
    def add_log(self, app_id, queue_name, user_id, operate_type, remain_time, info_json={}):
        """
        :description: 添加日志
        :param app_id：应用标识
        :param queue_name：队列名称
        :param user_id：用户标识
        :param operate_type：操作类型(1-加入队列 2-排到队列 3-参与抽赏 4-自动退出 5-手动退出)
        :param remain_time：剩余排队时间（单位秒）
        :param info_json：扩展信息
        :return: 
        :last_editors: HuangJianYi
        """
        ip_name = info_json.get('ip_name', '')
        ip_id = info_json.get('ip_id', 0)
        module_name = info_json.get('module_name', '')
        module_id = info_json.get('module_id', 0)
        open_id = info_json.get('open_id', '')
        user_nick = info_json.get('user_nick', '')
        act_id = info_json.get('act_id', 0)
        queue_no = info_json.get('queue_no', '')

        for key in {'ip_name', 'ip_id', 'module_name', 'module_id', 'open_id', 'user_nick', 'act_id', 'queue_no'}.intersection(info_json):
            del info_json[key]

        try:
            queueup_log_model = QueueupLogModel()
            queueup_log = QueueupLog()
            queueup_log.app_id = app_id
            queueup_log.act_id = act_id
            queueup_log.user_id = user_id
            queueup_log.open_id = open_id
            queueup_log.user_nick = user_nick
            queueup_log.queue_name = queue_name
            queueup_log.queue_no = queue_no
            queueup_log.operate_type = operate_type
            queueup_log.ip_name = ip_name
            queueup_log.ip_id = ip_id
            queueup_log.module_name = module_name
            queueup_log.module_id = module_id
            queueup_log.info_json = SevenHelper.json_dumps(info_json)
            queueup_log.remain_time = remain_time
            queueup_log.create_date = SevenHelper.get_now_datetime()
            queueup_log.create_day = SevenHelper.get_now_day_int()
            queueup_log_model.add_entity(queueup_log)
        except Exception as ex:
            self.logger_error.error("【添加日志】" + traceback.format_exc())
