# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-04-24 15:15:19
@LastEditTime: 2025-05-30 19:05:52
@LastEditors: HuangJianYi
@Description: 
"""

from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.customize.cryptography_helper import *
from seven_cloudapp_frame.libs.customize.safe_helper import *
from seven_cloudapp_frame.models.app_base_model import *
from urllib.parse import parse_qs


def filter_check_sign(sign_key, sign_lower=False, reverse=False, is_sign_key=False, expired_seconds=300, exclude_params=None):
    """
    :description: http请求签名验证装饰器
    :param sign_key: 参与签名的私钥
    :param sign_lower: 返回签名是否小写(默认大写)
    :param reverse: 是否反排序 False:升序 True:降序
    :param is_sign_key: 参数名是否参与签名(默认False不参与)
    :param expired_seconds: 接口timestamp过期时间(秒)
    :param exclude_params: 不参与签名的参数,支持list,str(英文逗号分隔)
    :last_editors: ChenXiaolei
    """
    def check_sign(handler):
        def wrapper(self, *args):
            # 签名参数
            sign_params = {}
            # 获取排除不需要签名的字段
            exclude_array = []
            if type(exclude_params) == str:
                exclude_array = exclude_params.split(",")
            if type(exclude_params) == list:
                exclude_array = exclude_params
            # 获取签名参数
            if not hasattr(self, "request_params"):
                if "Content-Type" in self.request.headers and self.request.headers[
                        "Content-type"].lower().find(
                            "application/json") >= 0 and self.request.body:
                    json_params = {}
                    try:
                        json_params = json.loads(self.request.body)
                    except:
                        self.response_json_error_params()
                        return
                    if json_params:
                        for field in json_params:
                            sign_params[field] = json_params[field]
                if self.request.arguments and len(self.request.arguments)>0:
                    for field in self.request.arguments:
                        sign_params[field] = self.get_param(field)
            else:
                sign_params = self.request_params

            if not sign_params or len(sign_params) < 2 or "timestamp" not in sign_params or "sign" not in sign_params:
                self.response_json_error_params("sign params error!")
                return

            sign_timestamp = int(sign_params["timestamp"])

            if expired_seconds and (not sign_timestamp or TimeHelper.add_seconds_by_timestamp(sign_timestamp, expired_seconds) < TimeHelper.get_now_timestamp() or sign_timestamp > TimeHelper.add_seconds_by_timestamp(second=expired_seconds)):
                self.response_json_error("error", "请求已失效.")
                return

            # 排除签名参数
            if exclude_array:
                for exclude_key in exclude_array:
                    if exclude_key in sign_params:
                        del sign_params[exclude_key]
            # 构建签名
            build_sign = SignHelper.params_sign_md5(
                sign_params, sign_key, sign_lower, reverse, is_sign_key)

            if not build_sign or build_sign != sign_params["sign"]:
                print(
                    f"http请求验签不匹配,收到sign:{sign_params['sign']},构建sign:{build_sign} 加密明文信息:{SignHelper.get_sign_params_str(sign_params,sign_key,reverse,is_sign_key)}")
                self.response_json_error("error", "sign error!")
                return

            return handler(self, *args)

        return wrapper

    return check_sign


def filter_check_params(must_params=None, check_user_code=False):
    """
    :description: 参数过滤装饰器 仅限handler使用,
                  提供参数的检查及获取参数功能
                  装饰器使用方法:
                  @client_filter_check_params("param_a,param_b,param_c")  或
                  @client_filter_check_params(["param_a","param_b,param_c"])
                  参数获取方法:
                  self.request_params[param_key]
    :param must_params: 必须传递的参数集合
    :param check_user_code: 是否校验用户标识必传
    :last_editors: HuangJianYi
    """
    def check_params(handler):
        def wrapper(self, **args):
            finally_must_params = must_params
            if hasattr(self, "must_params"):
                finally_must_params = self.must_params
            if type(finally_must_params) == str:
                must_array = finally_must_params.split(",")
            if type(finally_must_params) == list:
                must_array = finally_must_params

            if finally_must_params:
                for must_param in must_array:
                    if not must_param in self.request_params or self.request_params[must_param] == "":
                        self.response_json_error("param_error", f"参数错误,缺少必传参数{must_param}")
                        return
            if check_user_code == True and not self.get_user_id():
                self.response_json_error("param_error", f"参数错误,缺少必传参数user_code")
                return

            return handler(self, **args)

        return wrapper

    return check_params


def filter_check_current_limit(handler_name=None, current_limit_count=0, limit_params_dict={}):
    """
    :description: 流量限制过滤装饰器(UV) 仅限handler使用
    :param handler_name: handler名字
    :param current_limit_count: 流量限制数量
    :last_editors: HuangJianYi
    """
    def check_current(handler):
        def wrapper(self, **args):
            # 是否流量控制
            safe_config = share_config.get_value("safe_config", {})
            if safe_config.get("is_current_control", False) is True:  # 是否开启流量控制 0-关闭 1-开启
                app_id = self.get_app_id()
                object_id = self.get_open_id()
                if not object_id:
                    object_id = self.get_user_id()
                if SafeHelper.check_current_limit(app_id, current_limit_count, handler_name=handler_name, object_id=object_id) is True:
                    self.response_json_error("current_limit", "当前人数过多,请稍后再试")
                    return
                if handler_name:
                    SafeHelper.add_current_limit_count(app_id, object_id, current_limit_count, handler_name)

            return handler(self, **args)

        return wrapper

    return check_current


def filter_check_flow_limit(handler_name=None, flow_limit_api_count=0):
    """
    :description: 流量限制过滤装饰器(次数) 仅限handler使用
    :param handler_name: handler名字
    :param flow_limit_api_count: 流量限制数量
    :last_editors: HuangJianYi
    """
    def check_current(handler):
        def wrapper(self, **args):
            # 是否流量控制
            safe_config = share_config.get_value("safe_config", {})
            if safe_config.get("is_current_control", False) is True:  # 是否开启流量控制 0-关闭 1-开启
                app_id = self.get_app_id()
                limit_name = handler_name if handler_name else self.__class__.__name__
                limit_name += ":" + app_id
                limit_count = flow_limit_api_count if flow_limit_api_count else safe_config.get("flow_limit_api_count", 1000)
                if limit_count > 0:
                    if SafeHelper.check_current_limit_by_time_window(limit_name, limit_count, 1) is True:
                        self.response_json_error("current_limit", "当前人数过多,请稍后再试~")
                        return

            return handler(self, **args)

        return wrapper

    return check_current
