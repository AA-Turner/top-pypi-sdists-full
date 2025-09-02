# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-10-22 13:32:07
@LastEditTime: 2025-05-12 10:08:35
@LastEditors: HuangJianYi
@Description: 风险控制帮助类
"""
from seven_framework import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.enum import PlatType
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.app_base_model import AppBaseModel
from seven_cloudapp_frame.models.mp_base_model import MPBaseModel
import re

class SafeHelper:
    """
    :description:安全帮助类
    """

    #sql关键字
    _sql_pattern_key = r"\b(and|like|exec|execute|insert|create|select|drop|grant|alter|delete|update|asc|count|chr|mid|limit|union|substring|declare|master|truncate|char|delclare|or)\b|(\*|;)"
    #Url攻击正则
    _url_attack_key = r"\b(alert|xp_cmdshell|xp_|sp_|restore|backup|administrators|localgroup)\b"

    @classmethod
    def get_redis_config(self, config_dict=None):
        """
        :Description: redis初始化
        :param config_dict: config_dict
        :return: redis_init
        :last_editors: HuangJianYi
        """
        config_dict = config.get_value("redis_safe")
        if not config_dict:
            config_dict = config.get_value("redis")
        if config_dict and config_dict.get("is_cluster", False):
            self.is_cluster = True
        else:
            self.is_cluster = False
        return config_dict

    @classmethod
    def authenticat_app_id(self, old_value, new_value):
        """
        :description: app_id鉴权
        :param old_value:旧值
        :param new_value:新值
        :return: 是否鉴权成功 True-成功 False-失败
        :last_editors: HuangJianYi
        """
        safe_config = share_config.get_value("safe_config", {})
        is_authenticat_app_id = safe_config.get("is_authenticat_app_id", True)
        if is_authenticat_app_id == True and old_value != new_value:
            return False
        else:
            return True

    @classmethod
    def is_contain_sql(self, str):
        """
        :description: 是否包含sql关键字
        :param str:参数值
        :return:
        :last_editors: HuangJianYi
        """
        result = re.search(self._sql_pattern_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def is_attack(self, str):
        """
        :description: 是否攻击请求
        :param str:当前请求地址
        :return:True是 False否
        :last_editors: HuangJianYi
        """
        if ":" in str:
            return True
        result = re.search(self._url_attack_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def filter_routine_key(self, key):
        """
        :description: 过滤常规字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        routine_key_list = ["\u200b"]
        if not isinstance(key, str):
            return key
        for item in routine_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def filter_sql(self, key):
        """
        :description: 过滤sql关键字
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        result = re.findall(self._sql_pattern_key, key.lower())
        for item in result:
            key = key.replace(item[0], "")
            key = key.replace(item[0].upper(), "")
        return key

    @classmethod
    def filter_special_key(self, key):
        """
        :description: 过滤sql特殊字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        special_key_list = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@","!"]
        for item in special_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def check_attack_request(self, context):
        """
        :description: 校验是否攻击请求和是否包含非法参数值
        :param context:context
        :return:True满足条件直接拦截 False不拦截
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        safe_config = share_config.get_value("safe_config",{})
        if safe_config.get("is_check_referer", False) == True:
            if not context.request.headers or not context.request.headers.get("Referer", ""):
                invoke_result_data.success = False
                invoke_result_data.error_code = "referer_error"
                invoke_result_data.error_message = f"请求不合法"
                return invoke_result_data
            authenticat_app_id = ""
            plat_type = share_config.get_value("plat_type", PlatType.wx.value)
            if plat_type == PlatType.wx.value:
                result = re.search(r"https://servicewechat.com/(\w+)/\d+", context.request.headers.get("Referer", ""))
                authenticat_app_id = result.group(1)
            elif plat_type == PlatType.jd.value:
                group_list = context.request.headers.get("Referer", "").split("/")
                authenticat_app_id = group_list[3] if len(group_list) >= 5 else ""
            if authenticat_app_id != share_config.get_value("app_id"):
                invoke_result_data.success = False
                invoke_result_data.error_code = "referer_error"
                invoke_result_data.error_message = f"请求不合法"
                return invoke_result_data

        is_filter_attack = safe_config.get("is_filter_attack", False)
        if is_filter_attack == True and context.request_params:
            for key in context.request_params.keys():
                if self.is_contain_sql(context.request_params[key]) or self.is_attack(context.request_params[key]):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "attack_error"
                    invoke_result_data.error_message = f"参数{key}:值不合法"
                    break
        return invoke_result_data

    @classmethod
    def check_params(self, must_params):
        """
        :description: 校验必传参数
        :return:InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        must_array = []
        if type(must_params) == str:
            must_array = must_params.split(",")
        if type(must_params) == list:
            must_array = must_params
        for must_param in must_array:
            if not must_param in self.request_params or self.request_params[must_param] == "":
                invoke_result_data.success = False
                invoke_result_data.error_code = "param_error"
                invoke_result_data.error_message = f"参数错误,缺少必传参数{must_param}"
                break
        return invoke_result_data

    @classmethod
    def check_handler_power(self, request_params, uri, handler_name, request_prefix="server"):
        """
        :description: 校验是否有权限访问接口
        :param request_params: 请求参数
        :param uri: 请求uri
        :param handler_name: handler_name
        :param request_prefix: 请求前缀(server或client)
        :return:True有False没有
        :last_editors: HuangJianYi
        """
        result = True
        if request_params and request_params.get("app_id", "") and f"/{request_prefix}/" in uri:
            server_power_config = config.get_value(f"{request_prefix}_power_config", {})
            power_codes = server_power_config.get(handler_name, "")
            if power_codes:
                app_base_model = AppBaseModel(context=self.context)
                app_info_dict = app_base_model.get_app_info_dict(request_params.get("app_id", ""))
                if app_info_dict:
                    mp_base_model = MPBaseModel(context=self.context)
                    result = mp_base_model.check_high_power(store_user_nick=app_info_dict["store_user_nick"], project_code=app_info_dict["project_code"], key_names=power_codes)
        return result

    @classmethod
    def check_current_limit_by_time_window(self, limit_name, limit_count, request_limit_time=1):
        """
        :description: 流量限流校验(采用时间窗口滑动算法)
        :param limit_name: 限量名称
        :param limit_count: 限制数
        :param request_limit_time: 限制时间，单位秒
        :return:是否进行限流 True-是 False-否
        :last_editors: HuangJianYi
        """
        try:
            safe_config = share_config.get_value("safe_config", {})
            project_name = config.get_value('project_name', '') if not safe_config.get("current_project_name") else safe_config.get("current_project_name")
            redis_config = self.get_redis_config()
            redis_init = RedisExHelper.init(config_dict=redis_config, decode_responses=True)
            current_time = int(time.time())
            window_start = current_time // request_limit_time * request_limit_time
            window_start = f"{limit_name}:{window_start}:db_{project_name}"
            request_count = redis_init.incr(window_start, 1)
            # 如果当前请求数超过限制数，则返回 True，表示需要限流
            if request_count > limit_count:
                return True
            redis_init.expire(window_start, request_limit_time * 2 )
            return False
        except Exception as ex:
            return False

    @classmethod
    def check_current_limit(self, app_id, current_limit_count, handler_name='', object_id=''):
        """
        :description: 流量限流校验
        :param app_id: 应用标识
        :param current_limit_count: 流量限制数
        :param handler_name: handler名字
        :param object_id: 用户唯一标识
        :return: True代表满足限制条件进行拦截
        :last_editors: HuangJianYi
        """
        try:
            if not app_id:
                app_id = 'global'
            safe_config = share_config.get_value("safe_config", {})
            project_name = config.get_value('project_name', '') if not safe_config.get("current_project_name") else safe_config.get("current_project_name")
            cache_key = f"request_user_list_{app_id}:{str(SevenHelper.get_now_int(fmt='%Y%m%d%H%M'))}"
            if handler_name:
                cache_key = f"{cache_key}:{handler_name}"
            else:
                current_limit_count = 0
            cache_key =  f"{cache_key}:db_{project_name}"
            redis_config = self.get_redis_config()
            redis_init = RedisExHelper.init(config_dict=redis_config, decode_responses=True)
            if current_limit_count == 0: # 如果没有传入流量限制数，则从配置中获取
                current_limit_count = safe_config.get("current_limit_user_count", 500) # 默认流量限制数量
                if safe_config.get("is_current_white", False) is True: # 是否开启白名单
                    count = redis_init.get(f"current_limit_white_list:{app_id}:db_{project_name}")
                    if count and int(count) > 0:
                        current_limit_count = int(count)
            if current_limit_count == 0:
                return False
            if object_id and redis_init.sismember(cache_key, object_id) == 1:
                return False
            if int(redis_init.scard(cache_key)) >= current_limit_count:
                return True
            else:
                return False
        except Exception as ex:
            return False

    @classmethod
    def add_current_limit_count(self, app_id, object_id, current_limit_count, handler_name=''):
        """
        :description: 流量UV限流计数
        :param app_id: 应用标识
        :param object_id: 用户唯一标识
        :param current_limit_count: 流量限制数
        :param handler_name: handler名字
        :return:
        :last_editors: HuangJianYi
        """
        if not app_id:
            app_id = 'global'
        redis_config = self.get_redis_config()
        cache_key = f"request_user_list_{app_id}:{str(SevenHelper.get_now_int(fmt='%Y%m%d%H%M'))}"
        next_cache_key = f"request_user_list_{app_id}:{str(int((datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%Y%m%d%H%M')))}"
        if handler_name:
            cache_key = f"{cache_key}:{handler_name}"
            next_cache_key = f"{next_cache_key}:{handler_name}"
        safe_config = share_config.get_value("safe_config", {})
        project_name = config.get_value('project_name', '') if not safe_config.get("current_project_name") else safe_config.get("current_project_name")
        cache_key = f"{cache_key}:db_{project_name}"
        next_cache_key = f"{next_cache_key}:db_{project_name}"
        redis_init = RedisExHelper.init(config_dict=redis_config, decode_responses=True)
        if current_limit_count == 0:
            current_limit_count = safe_config.get("current_limit_user_count", 500) # 默认流量限制数量
            if safe_config.get("is_current_white", False) is True: # 是否开启白名单
                count = redis_init.get(f"current_limit_white_list:{app_id}:db_{project_name}")
                if count and int(count) > 0:
                    current_limit_count = int(count)
        if int(redis_init.scard(cache_key)) < current_limit_count: # 达到限制数，则不能添加
            if self.is_cluster == False:
                pipeline = redis_init.pipeline()
                pipeline.sadd(cache_key, object_id)
                pipeline.expire(cache_key, 120)
                pipeline.sadd(next_cache_key, object_id)
                pipeline.expire(next_cache_key, 120)
                pipeline.execute()
            else:
                redis_init.sadd(cache_key, object_id)
                redis_init.expire(cache_key, 120)
                redis_init.sadd(next_cache_key, object_id)
                redis_init.expire(next_cache_key, 120)

    @classmethod
    def operate_current_limit_white_list(self, app_id, current_limit_count, operate_expire_time, operate_type=1):
        """
        :description: 增加UV限流商家白名单
        :param app_id: 应用标识
        :param object_id: 用户唯一标识
        :param current_limit_count: 流量限制数
        :param operate_type: 操作类型 1-添加 2-删除
        :return:
        :last_editors: HuangJianYi
        """
        safe_config = share_config.get_value("safe_config", {})
        project_name = config.get_value('project_name', '') if not safe_config.get("current_project_name") else safe_config.get("current_project_name")
        redis_config = self.get_redis_config()
        redis_init = RedisExHelper.init(config_dict=redis_config, decode_responses=True)
        key_name = f"current_limit_white_list:{app_id}:db_{project_name}"
        if operate_type == 1:
            cur_expire_time = redis_init.ttl(key_name)
            if not cur_expire_time:
                cur_expire_time = 0
            cur_expire_time = int(cur_expire_time) + int(operate_expire_time)
            redis_init.set(key_name, str(current_limit_count), ex=cur_expire_time)
        else:
            redis_init.delete(key_name)

    @classmethod
    def desensitize_word(self, word):
        """
        :description: 脱敏文字,变成*号
        :param word 文字
        :return:
        :last_editors: HuangJianYi
        """
        if len(word) == 0:
            return ""
        elif len(word) == 1:
            return "*"
        elif len(word) == 2:
            return word[0:1] + "*"
        elif len(word) == 3:
            return word[0:1] + "*" + word[2:3]
        else:
            num = 3 if len(word) - 3 > 3 else len(word) - 3
            star = '*' * num
            return word[0:2] + star + word[len(word) - 1:len(word)]

    @classmethod
    def desensitize_word_v2(self, word, head_chars=1, tail_chars=1):
        """
        :description: 自定义脱敏文字,变成*号
        :param word: 文字
        :param head_chars: 头部保留的字符数，默认为1
        :param tail_chars: 尾部保留的字符数，默认为1
        :return:
        :last_editors: HuangJianYi
        """
        from math import ceil

        if len(word) <= head_chars + tail_chars:
            if len(word) == 1:
                return '*'  # 对于长度为1的字符串显示为单个星号
            elif len(word) == 2:
                return word[0] + '*'  # 对于长度为2的字符串显示为首字符加一个星号
            else:
                return word  # 当长度不足但大于等于2时直接返回原文

        num = ceil((len(word) - head_chars - tail_chars) * 2 / 3)
        star = '*' * num
        return word[:head_chars] + star + word[-tail_chars:]
