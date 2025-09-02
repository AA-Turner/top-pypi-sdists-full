# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-10 10:05:38
@LastEditTime: 2024-09-06 11:06:26
@LastEditors: HuangJianYi
@Description: 任务模块
"""

from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.task_base_model import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.db_models.task.task_info_model import *


class TaskInfoListHandler(ClientBaseHandler):
    """
    :description: 获取任务列表
    """
    def get_async(self):
        """
        :description: 获取任务列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param is_release：是否发布
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = self.get_param_int("module_id", 0)
        is_release = self.get_param_int("is_release", -1)
        is_del = self.get_param_int("is_del", -1)
        source_object_id = self.get_param("source_object_id")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc,id asc"
        task_base_model = TaskBaseModel(context=self)
        return self.response_json_success(self.business_process_executed(task_base_model.get_task_info_dict_list(app_id, act_id, module_id, is_release, False, source_object_id, is_del, order_by), ref_params={}))


class SaveTaskInfoHandler(ClientBaseHandler):
    """
    :description 保存任务
    """
    @filter_check_params("task_list")
    def post_async(self):
        """
        :description: 保存任务
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param task_list：任务列表
        :return response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = self.get_param_int("module_id")
        source_object_id = self.get_param("source_object_id")
        task_list = self.get_param("task_list")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else "任务"
        operate_user_id = invoke_result_data.data["operate_user_id"] if invoke_result_data.data.__contains__("operate_user_id") else ""
        operate_user_name = invoke_result_data.data["operate_user_name"] if invoke_result_data.data.__contains__("operate_user_name") else ""
        operate_role_id = invoke_result_data.data["operate_role_id"] if invoke_result_data.data.__contains__("operate_role_id") else ""
        update_field_list = invoke_result_data.data["update_field_list"] if invoke_result_data.data.__contains__("update_field_list") else "complete_type,task_name,sort_index,is_release,route_url,i1,i2,s1,s2,config_json,modify_date"

        try:
            task_list = SevenHelper.json_loads(task_list)
        except Exception as ex:
            task_list = []
        task_base_model = TaskBaseModel(context=self)
        task_info_model = TaskInfoModel(context=self)
        for item in task_list:
            if not item.__contains__("task_type"):
                continue
            task_name = str(item["task_name"]) if item.__contains__("task_name") else ""
            complete_type = int(item["complete_type"]) if item.__contains__("complete_type") else 1
            sort_index = int(item["sort_index"]) if item.__contains__("sort_index") else 0
            is_release = int(item["is_release"]) if item.__contains__("is_release") else 0
            route_url = item["route_url"] if item.__contains__("route_url") else ''
            i1 = int(item["i1"]) if item.__contains__("i1") else 0
            i2 = int(item["i2"]) if item.__contains__("i2") else 0
            s1 = item["s1"] if item.__contains__("s1") else ''
            s2 = item["s2"] if item.__contains__("s2") else ''
            config_json = SevenHelper.json_dumps(item["config_json"]) if item.__contains__("config_json") else {}
            title = title_prefix + ";" + task_name if title_prefix else task_name
            now_datetime = SevenHelper.get_now_datetime()
            if "id" in item.keys():
                task_info = task_info_model.get_entity_by_id(int(item["id"]))
                if task_info:
                    old_task_info = deepcopy(task_info)
                    task_info.task_type = int(item["task_type"])
                    task_info.task_name = task_name
                    task_info.complete_type = complete_type
                    task_info.config_json = config_json
                    task_info.sort_index = sort_index
                    task_info.is_release = is_release
                    task_info.route_url = route_url
                    task_info.i1 = i1
                    task_info.i2 = i2
                    task_info.s1 = s1
                    task_info.s2 = s2
                    task_info.modify_date = now_datetime
                    task_info_model.update_entity(task_info, update_field_list)
                    task_base_model._delete_task_info_dependency_key(0,task_info.id)
                    self.create_operation_log(operation_type=OperationType.update.value, model_name=task_info.__str__(), old_detail=old_task_info.__dict__, update_detail=task_info.__dict__, title=title, operate_user_id=operate_user_id, operate_user_name=operate_user_name, operate_role_id=operate_role_id)
                    ref_params = {}
                    ref_params['old_task_info'] = old_task_info
                    self.business_process_executed(task_info, ref_params)
            else:
                task_info = TaskInfo()
                task_info.app_id = app_id
                task_info.act_id = act_id
                task_info.module_id = module_id
                task_info.source_object_id = source_object_id
                task_info.task_type = int(item["task_type"])
                task_info.task_name = task_name
                task_info.complete_type = complete_type
                task_info.config_json = config_json
                task_info.sort_index = sort_index
                task_info.is_release = is_release
                task_info.route_url = route_url
                task_info.i1 = i1
                task_info.i2 = i2
                task_info.s1 = s1
                task_info.s2 = s2
                task_info.create_date = now_datetime
                task_info.modify_date = now_datetime
                task_info_model.add_entity(task_info)
                self.create_operation_log(operation_type=OperationType.add.value, model_name=task_info.__str__(), old_detail=None, update_detail=task_info.__dict__, title=title, operate_user_id=operate_user_id, operate_user_name=operate_user_name, operate_role_id=operate_role_id)
                ref_params = {}
                self.business_process_executed(task_info, ref_params)

        task_base_model._delete_task_info_dependency_key(act_id)

        return self.response_json_success()
