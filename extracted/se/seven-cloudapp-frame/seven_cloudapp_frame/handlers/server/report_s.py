# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-11-16 13:44:20
@LastEditTime: 2023-04-04 16:41:30
@LastEditors: HuangJianYi
:description: 报表模块
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.stat_base_model import *


class StatReportListHandler(ClientBaseHandler):
    """
    :description: 报表数据列表(表格)
    """
    def get_async(self):
        """
        :description: 报表数据列表(表格) 
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param start_date：开始时间
        :param end_date：结束时间 比如：查当天的数据 传过来开始时间是2021-09-02 00:00:00 结束时间则是2021-09-03 00:00:00 前端自动把结束时间加一天
        :param object_id：对象标识
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", 0))
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")
        object_id = self.get_param("object_id")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        report_condition = invoke_result_data.data["report_condition"] if invoke_result_data.data.__contains__("report_condition") else None
        report_params = invoke_result_data.data["report_params"] if invoke_result_data.data.__contains__("report_params") else None
        orm_condition = invoke_result_data.data["orm_condition"] if invoke_result_data.data.__contains__("orm_condition") else None
        orm_params = invoke_result_data.data["orm_params"] if invoke_result_data.data.__contains__("orm_params") else None
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index asc"
        is_only_module = invoke_result_data.data["is_only_module"] if invoke_result_data.data.__contains__("is_only_module") else False

        stat_base_model = StatBaseModel(context=self)
        stat_report_list = stat_base_model.get_stat_report_list(app_id=app_id, act_id=act_id, module_id=module_id, start_date=start_date, end_date=end_date, order_by=order_by, is_only_module=is_only_module, orm_condition=orm_condition, orm_params=orm_params, report_condition=report_condition, report_params=report_params, object_id=object_id)
        ref_params = {}
        stat_report_list = self.business_process_executed(stat_report_list, ref_params)
        return self.response_json_success(stat_report_list)



class TrendReportListHandler(ClientBaseHandler):
    """
    :description: 报表数据列表(趋势图) 
    """
    def get_async(self):
        """
        :description: 报表数据列表(趋势图) 
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param start_date：开始时间
        :param end_date：结束时间 比如：查当天的数据 传过来开始时间是2021-09-02 00:00:00 结束时间则是2021-09-03 00:00:00 前端自动把结束时间加一天
        :param object_id：对象标识
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", 0))
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")
        object_id = self.get_param("object_id")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        report_condition = invoke_result_data.data["report_condition"] if invoke_result_data.data.__contains__("report_condition") else None
        report_params = invoke_result_data.data["report_params"] if invoke_result_data.data.__contains__("report_params") else None
        orm_condition = invoke_result_data.data["orm_condition"] if invoke_result_data.data.__contains__("orm_condition") else None
        orm_params = invoke_result_data.data["orm_params"] if invoke_result_data.data.__contains__("orm_params") else None
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index asc"
        is_only_module = invoke_result_data.data["is_only_module"] if invoke_result_data.data.__contains__("is_only_module") else False

        stat_base_model = StatBaseModel(context=self)
        trend_report_list = stat_base_model.get_trend_report_list(app_id=app_id, act_id=act_id, module_id=module_id, start_date=start_date, end_date=end_date, order_by=order_by, is_only_module=is_only_module, orm_condition=orm_condition, orm_params=orm_params, report_condition=report_condition, report_params=report_params, object_id=object_id)
        ref_params = {}
        trend_report_list = self.business_process_executed(trend_report_list, ref_params)
        return self.response_json_success(trend_report_list)
