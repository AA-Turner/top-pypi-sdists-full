# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-03-27 11:02:53
@LastEditTime: 2024-03-27 11:36:51
@LastEditors: HuangJianYi
@Description: access_token获取控制台
"""
from seven_cloudapp_frame.libs.common.frame_console import *
from seven_cloudapp_frame.libs.customize.seven_helper import SevenHelper
from seven_cloudapp_frame.models.seven_model import InvokeResultData



def process_access_token(app_id, app_secret):
    """
    :description: 处理微信access_token
    :param app_id: app_id
    :param app_secret: app_secret
    :return 
    :last_editors: HuangJianYi
    """
    from seven_cloudapp_frame.libs.customize.wechat_helper import WeChatHelper

    while True:
        if "--production" in sys.argv:
            invoke_result_data = WeChatHelper.set_access_token(app_id, app_secret)
            if invoke_result_data.success == False:
                logger_info.info("【控制台获取微信access_token】" + SevenHelper.json_dumps(invoke_result_data))
            invoke_result_data = WeChatHelper.set_jsapi_ticket(app_id, app_secret)
            if invoke_result_data.success == False:
                logger_info.info("【控制台获取微信jsapi_ticket】" + SevenHelper.json_dumps(invoke_result_data))
        time.sleep(60 * 60)


def process_shakeshop_access_token(app_key, app_secret, shop_id, code=''):
    """
    :description: 处理抖店access_token
    :param app_id: app_id
    :param app_secret: app_secret
    :param shop_id: shop_id
    :param code: code
    :return 
    :last_editors: HuangJianYi
    """
    from seven_cloudapp_frame.models.third.shakeshop_base_model import ShakeShopBaseModel

    while True:
        if "--production" in sys.argv:
            shake_shop_base_model = ShakeShopBaseModel(app_key=app_key, app_secret=app_secret, shop_id=shop_id)
            shake_shop_base_model.init_token(code)
        time.sleep(60 * 60)