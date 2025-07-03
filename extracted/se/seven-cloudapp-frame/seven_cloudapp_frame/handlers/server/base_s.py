# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 17:00:55
@LastEditTime: 2025-03-19 17:21:04
@LastEditors: HuangJianYi
@Description: 基础模块
"""

from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.sms_helper import *
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.db_models.marketing.marketing_program_model import *


class LeftNavigationHandler(ClientBaseHandler):
    """
    :description: 左侧导航栏
    """
    def get_async(self):
        """
        :description: 左侧导航栏
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message,invoke_result_data.data)
        app_base_model = AppBaseModel(context=self)
        access_token = self.get_access_token()
        app_key, app_secret = self.get_app_key_secret()
        invoke_result_data = app_base_model.get_left_navigation(self.get_user_nick(), access_token, app_key, app_secret, self.get_app_id())
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)


class FriendLinkListHandler(ClientBaseHandler):
    """
    :description: 获取友情链接产品互推列表
    """
    def get_async(self):
        """
        :description: 获取友情链接产品互推列表
        :return list
        :last_editors: HuangJianYi
        """
        friend_link_model = FriendLinkModel(context=self, is_auto=True)
        friend_link_list = friend_link_model.get_cache_list(where="is_release=1")
        return self.response_json_success(friend_link_list)


class SendSmsHandler(ClientBaseHandler):
    """
    :description: 发送短信
    """
    @filter_check_params("telephone")
    def get_async(self):
        """
        :description: 发送短信
        :param thelephone：电话号码
        :return 
        :last_editors: HuangJianYi
        """
        open_id = self.get_open_id()
        telephone = self.get_param("telephone")
        sms_type = share_config.get_value("sms_type",SmsType.tencent.value)
        result_code = str(random.randint(100000, 999999))
        invoke_result_data = InvokeResultData()
        if sms_type == SmsType.ali.value:
            invoke_result_data = AliSmsHelper.send_message(result_code, telephone)
        elif sms_type == SmsType.tencent.value:
            invoke_result_data = TencentSmsHelper.send_message(result_code, telephone)
        else:
            invoke_result_data = BceSmsHelper.send_message(result_code, telephone)
        if invoke_result_data.success == True:
            #记录验证码
            SevenHelper.redis_init().set(f"user_bind_phone_code:{open_id}_{telephone}", result_code, ex=300)
            return self.response_json_success()
        else:
            return self.response_json_error("error","发送失败")


class MarketingProgramListHandler(ClientBaseHandler):
    """
    :description: 获取营销方案列表获取营销方案列表
    """
    def get_async(self):
        """
        :description: 获取营销方案列表
        :return: 列表
        :last_editors: HuangJianYi
        """
        marketing_program_list = MarketingProgramModel(context=self, is_auto=True).get_cache_dict_list()
        return self.response_json_success(marketing_program_list)


class GetProductPriceHandler(ClientBaseHandler):
    """
    :description: 获取产品价格信息
    """
    def get_async(self):
        """
        :description: 获取产品价格信息
        :param project_code：项目编码
        :return 
        :last_editors: HuangJianYi
        """
        project_code = self.get_param("project_code")
        product_price_model = ProductPriceModel(context=self, is_auto=True)
        now_date = SevenHelper.get_now_datetime()
        condition_where = ConditionWhere()
        condition_where.add_condition("%s>=begin_time and %s<=end_time and is_release=1")
        params = [now_date, now_date]
        if project_code:
            condition_where.add_condition("project_code=%s")
            params.append(project_code)
        product_price = product_price_model.get_dict(where=condition_where.to_string(), order_by="create_time desc", limit="1", params=params)
        if not product_price:
            return self.response_json_error("error", "找不到产品价格信息")
        try:
            product_price["content"] = SevenHelper.json_loads(product_price["content"])
        except:
            return self.response_json_error("error", "产品价格信息格式有误")

        return self.response_json_success(product_price)
