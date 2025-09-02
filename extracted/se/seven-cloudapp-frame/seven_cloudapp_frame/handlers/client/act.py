# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 14:03:12
@LastEditTime: 2024-09-11 17:13:23
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.enum import PageCountMode
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.act_base_model import *
from seven_cloudapp_frame.models.cms_base_model import *
from seven_cloudapp_frame.models.prize_base_model import *
from seven_cloudapp_frame.models.price_base_model import *


class ActInfoHandler(ClientBaseHandler):
    """
    :description: 获取活动信息
    """
    def get_async(self):
        """
        :description: 获取活动信息
        :param act_id：活动标识
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        ver_no = invoke_result_data.data["ver_no"] if invoke_result_data.data.__contains__("ver_no") else '1'
        if ver_no == "1":
            self.get_act_info()
        else:
            self.get_act_info_v2()

    def get_act_info(self):
        """
        :description: 获取活动信息V1版本
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        app_base_model = AppBaseModel(context=self)
        act_base_model = ActBaseModel(context=self)
        app_info_dict = app_base_model.get_app_info_dict(app_id)
        if not app_info_dict:
            return self.response_json_error("error", "小程序不存在")
        act_info_dict = act_base_model.get_act_info_dict(act_id, True, False)
        if not act_info_dict or act_info_dict["is_del"] == 1 or SafeHelper.authenticat_app_id(act_info_dict["app_id"], app_id) == False:
            return self.response_json_error("error", "活动不存在")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        act_info_dict["seller_id"] = app_info_dict["seller_id"]
        act_info_dict["store_id"] = app_info_dict["store_id"]
        act_info_dict["store_name"] = app_info_dict["store_name"]
        act_info_dict["store_icon"] = app_info_dict["store_icon"]
        act_info_dict["app_icon"] = app_info_dict["app_icon"]
        act_info_dict["store_user_nick"] = app_info_dict["store_user_nick"]
        act_info_dict["expiration_date"] = app_info_dict["expiration_date"]

        act_info_dict = self.business_process_executed(act_info_dict, ref_params={"app_info" : app_info_dict})
        return self.response_json_success(act_info_dict)

    def get_act_info_v2(self):
        """
        :description: 获取活动信息V2版本
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        app_base_model = AppBaseModel(context=self)
        act_base_model = ActBaseModel(context=self)
        app_info_dict = app_base_model.get_app_info_dict(app_id, field="id,seller_id,store_id,store_name,store_icon,app_icon,store_user_nick")
        if not app_info_dict:
            return self.response_json_error("error", "小程序不存在")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        exclude_fields = invoke_result_data.data["exclude_fields"] if invoke_result_data.data.__contains__("exclude_fields") else "is_visit_store,store_url,theme_id,is_release,close_word,start_date,end_date,is_del,finish_menu_config_json,agreement_json,is_fictitious,task_asset_type_json,refund_count,is_finish,is_launch,brand_json,share_desc_json,rule_desc_json,release_date,sort_index,create_date,modify_date,i1,i2,i3,i4,i5,s1,s2,s3,s4,s5,d1,d2"
        act_info_dict = act_base_model.get_act_info_dict(act_id, True, False)
        if not act_info_dict or act_info_dict["is_del"] == 1 or SafeHelper.authenticat_app_id(act_info_dict["app_id"], app_id) == False:
            return self.response_json_error("error", "活动不存在")

        # 店铺配置
        act_info_dict['store'] = {}
        act_info_dict['store']['id'] = app_info_dict['id']
        act_info_dict['store']['seller_id'] = app_info_dict['seller_id']
        act_info_dict['store']['store_id'] = app_info_dict['store_id']
        act_info_dict['store']['seller_nick'] = app_info_dict['store_user_nick']
        act_info_dict['store']['is_open'] = act_info_dict['is_visit_store']
        act_info_dict['store']['store_url'] = act_info_dict['store_url']



        # 主题配置
        act_info_dict['theme'] = {}
        act_info_dict['theme']['id'] = act_info_dict['theme_id']
        # 小程序配置
        act_info_dict['mini_program'] = {}
        act_info_dict['mini_program']['is_open'] = act_info_dict['is_release']
        act_info_dict['mini_program']['close_word'] = act_info_dict['close_word']
        act_info_dict['mini_program']['start_date'] = act_info_dict['start_date']
        act_info_dict['mini_program']['end_date'] = act_info_dict['end_date']
        # 分享配置 {"taoword": "", "icon": "", "title": "", "desc": ""}
        act_info_dict["shares"] = {}
        act_info_dict["shares"]["default"] = {"taoword": "", "icon": "", "title": "", "desc": ""}
        if act_info_dict.__contains__("share_desc_json") and act_info_dict["share_desc_json"] not in ['', '{}']:
            share_desc = SevenHelper.json_loads(act_info_dict["share_desc_json"])
            if share_desc.__contains__("default"):
                act_info_dict["shares"] = share_desc
            else:
                act_info_dict["shares"]["default"] = share_desc
        # 规则配置 [{"title":"购买规则","desc":"在此填写规则"}]
        act_info_dict["rules"] = SevenHelper.json_loads(act_info_dict["rule_desc_json"]) if act_info_dict["rule_desc_json"] else []
        # 用户协议或隐私条款配置 [{"title":"购买规则","explain":"在此填写规则"}]
        act_info_dict["purchase_agreement"] = SevenHelper.json_loads(act_info_dict["agreement_json"]) if act_info_dict["agreement_json"] else []
        #品牌配置
        act_info_dict["brands"] = SevenHelper.json_loads(act_info_dict["brand_json"]) if act_info_dict["brand_json"] else {}

        act_info_dict = self.business_process_executed(act_info_dict, ref_params={})
        if act_info_dict:
            for item in exclude_fields.split(','):
                try:
                    del act_info_dict[item]
                except:
                    pass

        return self.response_json_success(act_info_dict)


class ActPrizeListHandler(ClientBaseHandler):
    """
    :description: 活动奖品列表
    """
    def get_async(self):
        """
        :description: 活动奖品列表
        :param act_id: 活动标识
        :param module_id: 活动模块标识
        :param prize_name: 奖品名称
        :param ascription_type: 奖品归属类型（0-活动奖品1-任务奖品）
        :param page_size: 条数
        :param page_index: 页数
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return: PageInfo
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = self.get_param_int("module_id", 0)
        prize_name = self.get_param("prize_name")
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 10)
        page_count_mode = self.get_param_int("page_count_mode", 1)
        ascription_type = self.get_param_int("ascription_type", 0)

        if not app_id or not act_id:
            return self.response_json_success({"data": []})
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        prize_base_model = PrizeBaseModel(context=self)
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        page_list = prize_base_model.get_act_prize_list(app_id, act_id, module_id, prize_name, ascription_type, 0, page_size, page_index, condition="is_release=1", page_count_mode=page_count_mode)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)


class CmsInfoListHandler(ClientBaseHandler):
    """
    :description: 获取位置信息列表
    """
    @filter_check_params("place_id")
    def get_async(self):
        """
        :description: 获取位置信息列表
        :params place_id:位置标识
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        place_id = self.get_param_int("place_id", 0)
        page_size = self.get_param_int("page_size", 20)
        page_index = self.get_param_int("page_index", 0)
        page_count_mode = self.get_param_int("page_count_mode", 1)


        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else None
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else None
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "id desc"
        field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        cms_base_model = CmsBaseModel(context=self)
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        if condition and params:
            page_list = cms_base_model.get_cms_info_list_v2(place_id=place_id, page_size=page_size, page_index=page_index, order_by=order_by, field=field, condition=condition, params=params, is_cache=True, page_count_mode=page_count_mode)
        else:
            page_list = cms_base_model.get_cms_info_list(place_id=place_id, page_size=page_size, page_index=page_index, order_by=order_by, field=field, app_id=app_id, act_id=act_id, is_cache=True, page_count_mode=page_count_mode)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)


class PriceGearListHandler(ClientBaseHandler):
    """
    :description: 获取价格档位列表
    """
    def get_async(self):
        """
        :description: 获取价格档位列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param page_index：页索引
        :param page_size：页大小
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :param business_type：业务类型
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        page_size = self.get_param_int("page_size", 20)
        page_index = self.get_param_int("page_index", 0)
        page_count_mode = self.get_param_int("page_count_mode", 1)
        business_type = self.get_param_int("business_type", -1)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc"
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        page_list = PriceBaseModel(context=self).get_price_gear_list(app_id, act_id, page_size, page_index, order_by, page_count_mode=page_count_mode, business_type=business_type)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)
