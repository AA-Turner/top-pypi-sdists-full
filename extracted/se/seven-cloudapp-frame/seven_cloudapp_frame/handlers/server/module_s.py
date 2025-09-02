# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-03 15:42:53
@LastEditTime: 2024-02-02 09:09:11
@LastEditors: HuangJianYi
@Description: 小活动模块（机台）
"""
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.module_base_model import *
from seven_cloudapp_frame.models.seven_model import PageInfo


class SaveActModuleHandler(ClientBaseHandler):
    """
    :description: 保存活动模块信息
    """
    def post_async(self):
        """
        :description: 添加活动信息
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param business_type: 业务类型(0无1机台2活动)
        :param module_id: 活动模块标识
        :param module_name: 模块名称
        :param module_sub_name: 模块短名称
        :param module_type: 模块类型
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param module_pic: 模块图片
        :param module_desc: 描述信息
        :param price: 价格
        :param price_gear_id: 档位标识
        :param ip_id: IP标识
        :param join_ways: 活动参与条件（0所有1关注店铺2加入会员3指定用户）
        :param is_fictitious: 是否开启虚拟中奖（1是0否）
        :param sort_index: 排序
        :param is_release: 是否发布（1是0否）
        :param i1: i1
        :param i2: i2
        :param i3: i3
        :param i4: i4
        :param i5: i5
        :param s1: s1
        :param s2: s2
        :param s3: s3
        :param s4: s4
        :param s5: s5
        :param d1: d1
        :param d2: d2
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        business_type = int(self.get_param("business_type",0))
        module_id = int(self.get_param("module_id",0))
        module_name = self.get_param("module_name")
        module_sub_name = self.get_param("module_sub_name")
        module_type = self.get_param_int("module_type",0)
        start_date = self.get_param("start_date", "1900-01-01 00:00:00")
        end_date = self.get_param("end_date", "1900-01-01 00:00:00")
        module_pic = self.get_param("module_pic")
        module_desc = self.get_param("module_desc")
        price = self.get_param("price")
        price_gear_id = int(self.get_param("price_gear_id",0))
        ip_id = int(self.get_param("ip_id", 0))
        join_ways = int(self.get_param("join_ways",0))
        is_fictitious = int(self.get_param("is_fictitious",0))
        sort_index = int(self.get_param("sort_index",0))
        is_release = int(self.get_param("is_release",0))
        i1 = int(self.get_param("i1",0))
        i2 = int(self.get_param("i2",0))
        i3 = int(self.get_param("i3",0))
        i4 = int(self.get_param("i4",0))
        i5 = int(self.get_param("i5",0))
        s1 = self.get_param("s1")
        s2 = self.get_param("s2")
        s3 = self.get_param("s3")
        s4 = self.get_param("s4")
        s5 = self.get_param("s5")
        d1 = self.get_param("d1", "1900-01-01 00:00:00")
        d2 = self.get_param("d2", "1900-01-01 00:00:00")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        default_prefix = ""
        if business_type == 1:
            default_prefix = "机台"
        elif business_type == 2:
            default_prefix = "活动"
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else default_prefix
        exclude_field_list = invoke_result_data.data["exclude_field_list"] if invoke_result_data.data.__contains__("exclude_field_list") else ''
        module_base_model = ModuleBaseModel(context=self)
        invoke_result_data = module_base_model.save_act_module(app_id, act_id, module_id, module_name, module_sub_name, start_date, end_date, module_pic, module_desc, price, price_gear_id, ip_id, join_ways, is_fictitious, sort_index, is_release, i1, i2, i3, i4, i5, s1, s2, s3, s4, s5, d1, d2, business_type, module_type, exclude_field_list)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if invoke_result_data.data["is_add"] == True:
            # 记录日志
            self.create_operation_log(operation_type=OperationType.add.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=None, update_detail=invoke_result_data.data["new"], title= title_prefix + ";" + module_name)
        else:
            self.create_operation_log(operation_type=OperationType.update.value, model_name=invoke_result_data.data["new"].__str__(), old_detail=invoke_result_data.data["old"], update_detail=invoke_result_data.data["new"], title= title_prefix + ";" + module_name)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.response_json_success(invoke_result_data.data["new"].id)


class ActModuleHandler(ClientBaseHandler):
    """
    :description: 单条活动模块信息
    """
    def get_async(self):
        """
        :description: 活动模块列表
        :param app_id：应用标识
        :param module_id：活动模块标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        module_id = int(self.get_param("module_id", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        module_base_model = ModuleBaseModel(context=self)
        act_module_dict = module_base_model.get_act_module_dict(module_id, False)
        if act_module_dict:
            if SafeHelper.authenticat_app_id(act_module_dict["app_id"], app_id) == False:
                act_module_dict = {}
                return self.response_json_success(act_module_dict)
        ref_params = {}
        return self.response_json_success(self.business_process_executed(act_module_dict, ref_params))


class ActModuleListHandler(ClientBaseHandler):
    """
    :description: 活动模块列表
    """
    def get_async(self):
        """
        :description: 活动模块列表
        :param app_id：应用标识
        :param business_type：业务类型(0无1机台2活动)
        :param act_name：模块名称
        :param start_date：开始时间
        :param end_date：结束时间
        :param page_index：页索引
        :param page_size：页大小
        :return: PageInfo
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 10)
        is_del = self.get_param_int("is_del", 0)
        business_type = self.get_param_int("business_type", -1)
        module_name = self.get_param("module_name")
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else ""
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else []
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc,id asc"
        condition_where = ConditionWhere()
        if condition:
            condition_where.add_condition(condition)
        if business_type != -1:
            condition_where.add_condition("business_type=%s")
            params.append(business_type)

        if not app_id or not act_id:
            return self.response_json_success({"data": []})
        module_base_model = ModuleBaseModel(context=self)
        page_list, total = module_base_model.get_act_module_list(app_id, act_id, module_name, start_date, end_date, is_del, page_size, page_index, order_by=order_by, condition=condition_where.to_string(), params=params, is_cache=False)
        ref_params = {}
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params))
        return self.response_json_success(page_info)


class DeleteActModuleHandler(ClientBaseHandler):
    """
    :description: 删除活动模块
    """
    @filter_check_params("module_id")
    def get_async(self):
        """
        :description: 删除活动模块
        :param app_id：应用标识
        :param module_id：模块标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        module_id = int(self.get_param("module_id", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        module_base_model = ModuleBaseModel(context=self)
        invoke_result_data = module_base_model.update_act_module_status(app_id, module_id, 1)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        default_prefix = ""
        if invoke_result_data.data["business_type"] == 1:
            default_prefix = "机台"
        elif invoke_result_data.data["business_type"] == 2:
            default_prefix = "活动"
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else default_prefix
        self.create_operation_log(operation_type=OperationType.delete.value, model_name="act_module_tb", title= title_prefix + ";" + invoke_result_data.data["module_name"])
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class ReviewActModuleHandler(ClientBaseHandler):
    """
    :description: 还原活动模块
    """
    @filter_check_params("module_id")
    def get_async(self):
        """
        :description: 还原活动模块
        :param app_id：应用标识
        :param module_id：模块标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        module_id = int(self.get_param("module_id", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        module_base_model = ModuleBaseModel(context=self)
        invoke_result_data = module_base_model.update_act_module_status(app_id, module_id, 0)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        default_prefix = ""
        if invoke_result_data.data["business_type"] == 1:
            default_prefix = "机台"
        elif invoke_result_data.data["business_type"] == 2:
            default_prefix = "活动"
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else default_prefix
        self.create_operation_log(operation_type=OperationType.review.value, model_name="act_module_tb", title= title_prefix + ";" + invoke_result_data.data["module_name"])
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class ReleaseActModuleHandler(ClientBaseHandler):
    """
    :description: 上下架活动模块
    """
    @filter_check_params("module_id")
    def get_async(self):
        """
        :description: 上下架活动模块
        :param app_id：应用标识
        :param module_id：模块标识
        :param is_release: 是否发布 1-是 0-否
        :return:
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        module_id = int(self.get_param("module_id", 0))
        is_release = int(self.get_param("is_release", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        module_base_model = ModuleBaseModel(context=self)
        invoke_result_data = module_base_model.release_act_module(app_id, module_id, is_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        operation_type = OperationType.release.value if is_release == 1 else OperationType.un_release.value
        default_prefix = ""
        if invoke_result_data.data["business_type"] == 1:
            default_prefix = "机台"
        elif invoke_result_data.data["business_type"] == 2:
            default_prefix = "活动"
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else default_prefix
        self.create_operation_log(operation_type=operation_type, model_name="act_module_tb", title= title_prefix + ";" + invoke_result_data.data["module_name"])
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class UpdateActModulePriceHandler(ClientBaseHandler):
    """
    :description: 更新活动模块价格
    """
    @filter_check_params("prize_gear_id")
    def get_async(self):
        """
        :description:更新活动模块价格
        :param app_id：应用标识
        :param act_id：活动标识
        :param prize_gear_id：档位标识
        :return:
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        prize_gear_id = int(self.get_param("prize_gear_id", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        module_base_model = ModuleBaseModel(context=self)
        invoke_result_data = module_base_model.update_act_module_price(app_id, act_id, prize_gear_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()