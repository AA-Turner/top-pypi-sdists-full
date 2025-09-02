# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-30 15:46:34
@LastEditTime: 2022-07-14 10:08:14
@LastEditors: HuangJianYi
@Description: 投放模块
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.act_base_model import *
from seven_cloudapp_frame.models.top_base_model import *
from seven_cloudapp_frame.models.launch_base_model import *
from seven_cloudapp_frame.models.db_models.act.act_info_model import *
from seven_cloudapp_frame.models.db_models.act.act_prize_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_goods_model import *
from seven_cloudapp_frame.models.db_models.price.price_gear_model import *
from seven_cloudapp_frame.models.db_models.launch.launch_plan_model import *


class InitLaunchGoodsHandler(ClientBaseHandler):
    """
    :description: 初始化商品投放
    """
    def get_async(self):
        """
        :description: 初始化商品投放
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param source_types：商品来源，指定哪些位置的商品要进行投放（1活动奖品商品2价格档位商品） 多个逗号,分隔
        :return
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", 0))
        source_types = self.get_param("source_types","1,2")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        app_base_model = AppBaseModel(context=self)
        launch_base_model = LaunchBaseModel(context=self)
        online_url = app_base_model.get_online_url(act_id, app_id, module_id)
        invoke_result_data = launch_base_model.init_launch_goods(app_id, act_id, source_types, online_url)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)


class ResetLaunchGoodsHandler(ClientBaseHandler):
    """
    :description: 重置商品投放 删除已投放的记录并将活动投放状态改为未投放
    """
    def get_async(self):
        """
        :description: 重置商品投放 删除已投放的记录并将活动投放状态改为未投放
        :param app_id：应用标识
        :param act_id：活动标识
        :param close_goods_id：投放失败时关闭投放的商品ID  多个逗号,分隔
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()

        close_goods_id = self.get_param("close_goods_id")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        launch_base_model = LaunchBaseModel(context=self)
        invoke_result_data = launch_base_model.reset_launch_goods(app_id, act_id, close_goods_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class InitLaunchGoodsCallBackHandler(ClientBaseHandler):
    """
    :description: 初始化投放商品回调接口
    """
    def get_async(self):
        """
        :description: 初始化投放商品回调接口
        :param app_id：应用标识
        :param act_id：活动标识
        :param close_goods_id：投放失败时关闭投放的商品ID  多个逗号,分隔
        :param call_back_info：回调信息
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        close_goods_id = self.get_param("close_goods_id")
        call_back_info = self.get_param("call_back_info")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        launch_base_model = LaunchBaseModel(context=self)
        invoke_result_data = launch_base_model.init_launch_goods_callback(app_id, act_id, close_goods_id, call_back_info)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class UpdateLaunchGoodsStatusHandler(ClientBaseHandler):
    """
    :description: 更改投放商品的状态
    """
    def get_async(self):
        """
        :description: 保存更改投放商品的状态
        :param app_id：应用标识
        :param act_id：活动标识
        :param update_goods_id：更新商品ID（例：1）
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        goods_id = self.get_param("update_goods_id")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if goods_id != "":
            LaunchGoodsModel(context=self).update_table("is_launch=abs(is_launch-1),is_sync=0,launch_date=%s", "app_id=%s and act_id=%s and goods_id=%s", [self.get_now_datetime(), app_id, act_id, goods_id])
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class LaunchGoodsListHandler(ClientBaseHandler):
    """
    :description: 投放商品列表
    """
    def get_async(self):
        """
        :description: 投放商品列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param page_index：页索引
        :param page_size：页大小
        :return 列表
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        goods_id = self.get_param("goods_id")
        launch_status = self.get_param_int("launch_status", -1)
        access_token = self.get_access_token()

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        launch_base_model = LaunchBaseModel(context=self)
        app_key, app_secret = self.get_app_key_secret()
        invoke_result_data = launch_base_model.get_launch_goods_list(app_id, act_id, page_size, page_index, access_token, app_key, app_secret,goods_id,launch_status)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)


class AsyncLaunchGoodsHandler(ClientBaseHandler):
    """
    :description: 同步投放商品（小程序投放-商品绑定/解绑）
    """
    def get_async(self):
        """
        :description: 同步投放商品（小程序投放-商品绑定/解绑）
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", 0))
        access_token = self.get_access_token()

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        app_base_model = AppBaseModel(context=self)
        online_url = app_base_model.get_online_url(act_id, app_id, module_id)
        launch_base_model = LaunchBaseModel(context=self)

        app_key, app_secret = self.get_app_key_secret()
        launch_plan_model = LaunchPlanModel(context=self)
        launch_plan = launch_plan_model.get_entity("act_id=%s", order_by="id desc", params=[act_id])
        if launch_plan:
            invoke_result_data = launch_base_model.async_launch_goods(app_id, act_id, launch_plan.launch_url, access_token, app_key, app_secret)
        else:
            invoke_result_data = launch_base_model.async_launch_goods(app_id, act_id, online_url, access_token, app_key, app_secret)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class GetLaunchPlanStatusHandler(ClientBaseHandler):
    """
    :description: 获取投放计划状态
    :param act_id：活动标识
    :return 
    :last_editors: HuangJianYi
    """
    def get_async(self):
        act_id = self.get_param_int("act_id")
        access_token = self.get_access_token()
        app_key, app_secret = self.get_app_key_secret()
        launch_base_model = LaunchBaseModel(context=self)
        launch_status = launch_base_model.get_launch_plan_status(act_id, access_token, app_key, app_secret)
        return self.response_json_success(launch_status)


class AsyncLaunchGoodsStatusHandler(ClientBaseHandler):
    """
    :description: 同步投放商品（小程序投放-商品绑定）
    :return
    :last_editors: HuangJianYi
    """
    def get_async(self):
        act_id = self.get_act_id()
        redis_init = SevenHelper.redis_init()
        redis_init.rpush("queue_async_lauch", act_id)
        return self.response_json_success()


class AddLaunchGoodsHandler(ClientBaseHandler):
    """
    :description: 添加投放商品
    :param goods_ids：商品id串 逗号分隔
    :return
    :last_editors: HuangJianYi
    """
    def get_async(self):
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        goods_ids = self.get_param("goods_ids")
        launch_base_model = LaunchBaseModel(context=self)
        launch_base_model.add_launch_goods_v2(app_id, act_id, goods_ids)
        return self.response_json_success()


class CanLaunchGoodsListHandler(ClientBaseHandler):
    """
    :description: 获取可投放商品列表（获取当前会话用户出售中的商品列表）
    """
    def get_async(self):
        """
        :description: 导入商品列表（获取当前会话用户出售中的商品列表）
        :param goods_name：商品名称
        :param order_tag：order_tag
        :param order_by：排序类型
        :param page_index：页索引
        :param page_size：页大小
        :return: 列表
        :last_editors: HuangJianYi
        """
        access_token = self.get_access_token()
        goods_name = self.get_param("goods_name")
        order_tag = self.get_param("order_tag", "list_time")
        order_by = self.get_param("order_by", "desc")
        page_index = int(self.get_param("page_index", 0))
        page_size = self.get_param("page_size", 20)
        is_log = int(self.get_param("is_log", 0))
        is_log = True if is_log == 1 else False

        access_token = self.get_access_token()
        app_key, app_secret = self.get_app_key_secret()
        launch_base_model = LaunchBaseModel(context=self)
        invoke_result_data = launch_base_model.can_launch_goods_list(page_index,page_size,goods_name,order_tag,order_by,access_token,app_key,app_secret,is_log)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)


class GetLaunchProgressHandler(ClientBaseHandler):
    """
    :description: 获取投放进度
    :return 投放进度 0未完成  1：已完成
    :last_editors: HuangJianYi
    """
    def get_async(self):
        act_id = self.get_act_id()
        launch_base_model = LaunchBaseModel(context=self)
        return self.response_json_success(launch_base_model.get_launch_progress(act_id))