# coding=UTF-8
"""
@Author: HuangJianYi
@Date: 2023-06-26 08:26:10
@LastEditTime: 2023-08-30 13:50:39
@LastEditors: HuangJianYi
@Description: 物流处理类（阿里云）
"""

import requests
from difflib import SequenceMatcher
from seven_cloudapp_frame.handlers.frame_base import *


class AliLogisticsHelper:
    """
    :description: 阿里物流处理类
    """
    logistics_url = 'https://wuliu.market.alicloudapi.com/kdi'  # 物流信息接口
    express_company_url = 'https://wuliu.market.alicloudapi.com/exCompany'  # 快递公司信息接口
    logger_error = Logger.get_logger_by_name("log_error")
    express_company_redis_key = "express_company_info"  # 快递公司redis_key

    @classmethod
    def get_logistics_info(self, express_no, express_company, recipient_phone):
        """
        :description: 获取物流信息
        :param express_no：快递单号
        :param express_company：快递公司
        :param recipient_phone：收件人手机号
        :return: InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            wuliu_config = share_config.get_value("wuliu_config")
            if not wuliu_config or not wuliu_config["app_code"]:
                invoke_result_data.success = False
                invoke_result_data.error_message = "缺少配置信息"
                return invoke_result_data
            platform_redis = share_config.get_value("platform_redis") if share_config.get_value("platform_redis") else config.get_value("redis")
            redis_init = RedisExHelper.init(config_dict=platform_redis, decode_responses=True)
            # 获取redis缓存物流公司类型（缩写）
            express_company_type = redis_init.hget(self.express_company_redis_key, express_company)
            if not express_company_type:
                express_company_invoke_result_data = self.get_express_company(express_no, express_company)
                if express_company_invoke_result_data.success == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_message = express_company_invoke_result_data.error_message
                    return invoke_result_data
                express_company_type = express_company_invoke_result_data.data['express_company_type']
            if '顺丰' in express_company:
                express_no += f":{str(recipient_phone[-4:])}"
            url = self.logistics_url + '?' + f'no={express_no}&type={express_company_type}'
            header = {"Authorization": 'APPCODE ' + wuliu_config["app_code"]}
            res = requests.get(url, headers=header)
            if res.status_code != 200:
                error_msg = self.get_error_info(res.status_code, res.headers['X-Ca-Error-Message'])
                invoke_result_data.success = False
                invoke_result_data.error_message = error_msg
                return invoke_result_data
            else:
                result_data = SevenHelper.json_loads(res.text)
                if result_data['status'] == '0':
                    invoke_result_data.data = result_data['result']
                else:
                    invoke_result_data.success = False
                    if result_data['status'] == '201':
                        invoke_result_data.error_message = "快递单号错误"
                    elif result_data['status'] == '203':
                        invoke_result_data.error_message = "快递公司不存在"
                    elif result_data['status'] == '204':
                        invoke_result_data.error_message = "快递公司识别失败"
                    elif result_data['status'] == '205':
                        invoke_result_data.error_message = "快递单号无法查询到信息"
                    elif result_data['status'] == '207':
                        invoke_result_data.error_message = "该单号被限制，错误单号"

        except Exception as ex:
            self.logger_error.error("【获取物流信息异常】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_message = "获取物流信息异常，请联系客服"
        return invoke_result_data

    @classmethod
    def get_express_company(self, express_no, express_company):
        """
        :description: 获取快递公司（根据快递单号）
        :param express_no：快递单号
        :param express_company：快递公司
        :return: list
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            wuliu_config = share_config.get_value("wuliu_config")
            if not wuliu_config or not wuliu_config["app_code"]:
                invoke_result_data.success = False
                invoke_result_data.error_message = "缺少配置信息"
                return invoke_result_data
            url = self.express_company_url + '?' + f'no={express_no}'
            header = {"Authorization": 'APPCODE ' + wuliu_config["app_code"]}
            res = requests.get(url, headers=header)
            if res.status_code != 200:
                error_msg = self.get_error_info(res.status_code, res.headers['X-Ca-Error-Message'])
                invoke_result_data.success = False
                invoke_result_data.error_message = error_msg
                return invoke_result_data
            else:
                result_data = SevenHelper.json_loads(res.text)
                if result_data['status'] == '0' and result_data['list']:
                    invoke_result_data.data = {"express_company_type": ""}  # 快递公司类型（缩写）
                    similarity_ratio = 0  # 匹配度
                    for express_company_dict in result_data['list']:
                        curr_similarity_ratio = SequenceMatcher(None, express_company, express_company_dict['name']).ratio()
                        if similarity_ratio < curr_similarity_ratio:
                            similarity_ratio = curr_similarity_ratio
                            invoke_result_data.data['express_company_type'] = express_company_dict['type']
                    if not invoke_result_data.data['express_company_type']:
                        invoke_result_data.success = False
                        invoke_result_data.error_message = "无法匹配快递公司信息"
                        return invoke_result_data
                    # 匹配度超过90%，保存到redis
                    if similarity_ratio > 0.9:
                        platform_redis = share_config.get_value("platform_redis") if share_config.get_value("platform_redis") else config.get_value("redis")
                        redis_init = RedisExHelper.init(config_dict=platform_redis)
                        redis_init.hset(self.express_company_redis_key, express_company, str(invoke_result_data.data['express_company_type']))
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_message = "未找到快递公司信息"
                    return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【获取快递公司（根据快递单号）】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_message = "获取快递公司信息异常，请联系客服"
        return invoke_result_data

    @classmethod
    def get_error_info(self, http_status_code, http_reason):
        """
        :description: 获取快递公司（根据快递单号）
        :param http_status_code：http状态码
        :param http_reason：原因
        :return: str
        :last_editors: HuangJianYi
        """
        error_msg = ""
        if (http_status_code == 400 and http_reason == 'Invalid Param Location'):
            error_msg = "参数错误"
        elif (http_status_code == 400 and http_reason == 'Invalid AppCode'):
            error_msg = "AppCode错误"
        elif (http_status_code == 400 and http_reason == 'Invalid Url'):
            error_msg = "请求的 Method、Path 或者环境错误"
        elif (http_status_code == 403 and http_reason == 'Unauthorized'):
            error_msg = "服务未被授权（或URL和Path不正确）"
        elif (http_status_code == 403 and http_reason == 'Quota Exhausted'):
            error_msg = "套餐包次数用完"
        elif (http_status_code == 403 and http_reason == 'Api Market Subscription quota exhausted'):
            error_msg = "套餐包次数用完，请续购套餐"
        elif (http_status_code == 500):
            error_msg = "API网关错误"
        else:
            error_msg = "参数名错误 或 其他错误"
        return error_msg