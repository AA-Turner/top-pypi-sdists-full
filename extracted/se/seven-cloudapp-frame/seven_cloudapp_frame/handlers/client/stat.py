# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-09-10 11:29:31
@LastEditTime: 2023-04-11 15:19:25
@LastEditors: HuangJianYi
@Description: 处理数据统计上报
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.stat_base_model import *



class StatReportHandler(ClientBaseHandler):
    """
    :description: 统计上报
    """
    @filter_check_params(check_user_code=True)
    def post_async(self):
        """
        :description: 统计上报
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param object_id:对象标识
        :param user_code:用户标识
        :param open_id:open_id
        :param data:统计数据json 格式：[{"key":"key1","value":1},{"key":"key2","value":1},{"key":"key3","value":1}] 或 {"key1":1,"key2":1,"key3":1}
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        open_id = self.get_param("open_id")
        module_id = self.get_param_int("module_id", 0)
        object_id = self.get_param("object_id")
        stat_data = self.get_param("data",[])
        if stat_data:
            stat_data = self.json_loads(stat_data)
        stat_base_model = StatBaseModel(context=self)
        stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, open_id, stat_data, object_id=object_id)
        return self.response_json_success()


class ShareReportHandler(ClientBaseHandler):
    """
    :description: 处理分享统计上报
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 处理分享统计上报
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        open_id = self.get_param("open_id")
        module_id = self.get_param_int("module_id", 0)
        stat_base_model = StatBaseModel(context=self)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        invoke_result_data = stat_base_model.process_share_report(app_id, act_id, module_id, user_id, open_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()


class InviteReportHandler(ClientBaseHandler):
    """
    :description: 处理邀请进入统计上报
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 处理邀请进入统计上报
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param invite_user_id:邀请人用户标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        from_user_id = int(self.get_param("invite_user_id", 0))
        open_id = self.get_param("open_id")
        module_id = int(self.get_param("module_id", 0))
        stat_base_model = StatBaseModel(context=self)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        invoke_result_data = stat_base_model.process_invite_report(app_id, act_id, module_id, user_id, open_id, from_user_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success()
