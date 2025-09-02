# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-12-20 16:07:52
@LastEditTime: 2025-03-19 18:03:30
@LastEditors: HuangJianYi
@Description: 操作日志相关处理业务模型
"""
from seven_framework import *
from seven_cloudapp_frame.libs.customize.seven_helper import SevenHelper
from seven_cloudapp_frame.models.seven_model import *
from asq.initiators import query

from seven_cloudapp_frame.models.db_models.operation.operation_log_model import *
from seven_cloudapp_frame.models.db_models.operation.operation_config_model import *

class OperateBaseModel():
    """
    :description: 操作日志相关处理业务模型   操作配置字段说明{"field": 数据库字段,"remark": 要显示的字段名字,"value": 值,"is_show": 是否显示（1是0否）,"sort_index":排序，默认按数组顺序,"out_ways":输出方式（默认0文本1图片）}
    """
    def __init__(self, context=None, logging_error=None, logging_info=None):
        
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def add_operation_log(self, operation_type, title, operation_desc, model_name, handler_name, old_detail, update_detail, app_id, act_id, operate_user_id, operate_user_name, operate_role_id, request_dict, ip , request_code, add_action_to_title=True):
        """
        :description: 创建操作日志
        :param operation_type：操作类型（查看枚举类OperationType）
        :param title：标题(对象)
        :param operation_desc：描述
        :param model_name：模块或表名称
        :param handler_name：handler名称
        :param old_detail：变更前对象
        :param update_detail：变更后对象
        :param app_id： 应用标识
        :param act_id：活动标识
        :param operate_user_id：操作人标识
        :param operate_user_name：操作人名称
        :param operate_role_id：操作人角色标识
        :param ip：ip地址
        :param request_code：请求代码
        :param add_action_to_title:标题追加操作类型名称（True是False否）
        :return: 
        :last_editors: HuangJianYi
        """
        operation_log_model = OperationLogModel(context=self.context)
        operation_log = OperationLog()
        operation_log.app_id = app_id
        operation_log.act_id = act_id
        request_dict = request_dict if request_dict else {}
        operation_log.request_params = request_dict.get("request_params","")
        self_request = request_dict.get("request",None)
        if self_request:
            operation_log.method = self_request.method
            operation_log.protocol = self_request.protocol
            operation_log.request_host = self_request.host
            operation_log.request_uri = self_request.uri
        operation_log.remote_ip = ip
        operation_log.request_code = request_code
        operation_log.operation_type = operation_type
        operation_log.model_name = model_name
        operation_log.handler_name = handler_name
        operation_log.detail = SevenHelper.json_dumps(old_detail) if old_detail else {}
        operation_log.update_detail = SevenHelper.json_dumps(update_detail) if update_detail else {}
        operation_log.operate_role_id = operate_role_id
        operation_log.operate_user_id = operate_user_id
        operation_log.operate_user_name = operate_user_name
        if add_action_to_title == True:
            operation_log.title = self.get_operation_type_name(operation_type) + title if operation_type != 10 else title
        else:
            operation_log.title = title
        operation_log.operation_desc = operation_desc
        operation_log.create_date = TimeHelper.get_now_format_time()
        operation_log.create_day = SevenHelper.get_now_day_int()
        id = operation_log_model.add_entity(operation_log)
        return id

    def get_operate_log_list(self, app_id, title="", operation_type=-1, operate_user_name="", operate_user_id="", operate_role_id="", create_date_start="", create_date_end="", page_index = 0, page_size = 10, is_contrast = False, is_all_fields=False):
        """
        :description:  获取操作日志列表
        :param app_id:应用标识
        :param title:标题(后置模糊匹配)
        :param operation_type:操作类型
        :param operate_user_name:操作人名称
        :param operate_user_id:操作人标识
        :param operate_role_id:操作角色标识
        :param create_date_start:操作开始时间
        :param create_date_end:操作结束时间
        :param create_date_end:操作结束时间
        :param page_index:页数
        :param page_size:条数
        :param is_contrast:是否对比新旧值返回contrast_info
        :param is_all_fields:是否返回所有匹配的字段包含没有变动的字段
        :return list: 
        :last_editors: HuangJianYi
        """
        operation_log_model = OperationLogModel(context=self.context, is_auto=True)
        condition_where = ConditionWhere()
        condition_where.add_condition("app_id=%s")
        params = [app_id]
        if title:
            title = f"{title}%"
            condition_where.add_condition("title like %s")
            params.append(title)
        if operate_user_name:
            condition_where.add_condition("operate_user_name=%s")
            params.append(operate_user_name)
        if operate_user_id:
            condition_where.add_condition("operate_user_id=%s")
            params.append(operate_user_id)
        if operate_role_id:
            condition_where.add_condition("operate_role_id=%s")
            params.append(operate_role_id)
        if operation_type != -1:
            condition_where.add_condition("operation_type=%s")
            params.append(operation_type)
        if create_date_start:
            condition_where.add_condition("create_date>=%s")
            params.append(create_date_start)
        if create_date_end:
            condition_where.add_condition("create_date<=%s")
            params.append(create_date_end)

        operation_log_list,total = operation_log_model.get_dict_page_list("*", page_index, page_size, condition_where.to_string(),"","id desc", params=params)
        for operation_log in operation_log_list:
            operation_log["detail"] = SevenHelper.json_loads(operation_log["detail"]) if operation_log["detail"] else {}
            operation_log["update_detail"] = SevenHelper.json_loads(operation_log["update_detail"]) if operation_log["update_detail"] else {}
            if is_contrast:
                operation_log = self.get_contrast_info(operation_log, is_all_fields)
        return operation_log_list,total

    def get_operate_log(self,id, is_contrast = True, is_all_fields=False):
        """
        :description:  获取操作日志列表
        :param id:操作日志标识
        :param model_name:模块或表名称
        :param operation_type:操作类型
        :param page_index:页数
        :param page_size:条数
        :param is_contrast:是否对比新旧值返回contrast_info
        :param is_all_fields:是否返回所有匹配的字段包含没有变动的字段
        :return list: 
        :last_editors: HuangJianYi
        """
        operation_log_model = OperationLogModel(context=self.context)
        operation_log = operation_log_model.get_dict_by_id(id)
        if is_contrast and operation_log:
            operation_log["detail"] = SevenHelper.json_loads(operation_log["detail"]) if operation_log["detail"] else {}
            operation_log["update_detail"] = SevenHelper.json_loads(operation_log["update_detail"]) if operation_log["update_detail"] else {}
            operation_log = self.get_contrast_info(operation_log, is_all_fields)
        return operation_log
    
    def _convert_remark(self, config_field, value):
        """
        :description:  转换备注
        :param config_field:配置字段
        :param value:处理值
        :return: 
        :last_editors: HuangJianYi
        """
        db = None
        value_remark = "-"
        if value not in [None,""]:
            read_config = config_field.get("read_config",{})
            if len(read_config) > 0:
                db = MySQLHelper(config.get_value(OperationLogModel(context=self.context).db_connect_key))
                sql = "select %s from %s where %s=%s limit 1;" % (str(read_config["return_field"]), str(read_config["table_name"]), str(read_config["search_field"]), str(value))
                result = db.query(sql)
                if result:
                    value_remark = result[0][str(read_config["return_field"])] if result[0][str(read_config["return_field"])] else "-"
                else:
                    value_remark = "-"
            elif len(config_field.get("value", {})) > 0:
                default = config_field.get("value", {}).get("default", "")
                if default:
                    value_remark = default.replace("{0}", str(value))
                elif ',' in value:
                    for item in value.split(','):
                        cur_remark = config_field.get("value", {}).get(str(item), "")
                        if cur_remark:
                            value_remark = "" if value_remark == "-" else value_remark
                            value_remark += "," + cur_remark if value_remark != "" else cur_remark
                else:
                    value_remark = config_field.get("value", {}).get(str(value), "-")
            else:
                value_remark = value
        return value_remark
        
    def get_contrast_info(self, operation_log, is_all_fields=False):
        """
        :description:  获取操作日志对比信息
        :param operation_log:日志信息字典
        :param is_all_fields:是否返回所有匹配的字段包含没有变动的字段
        :return info: 
        :last_editors: HuangJianYi
        """
        try:
            operation_log["contrast_info"] = []
            if operation_log["update_detail"] and isinstance(operation_log["update_detail"], dict):
                operation_config_model = OperationConfigModel(context=self.context)
                operation_config = operation_config_model.get_dict("model_name=%s",params=[operation_log["model_name"]])
                if operation_config:
                    for key in operation_log["update_detail"]:
                        old_value_remark = ""
                        new_value_remark = ""
                        config_list = SevenHelper.json_loads(operation_config["config_json"]) if operation_config["config_json"] else {}
                        config_fields =  query(config_list).where(lambda x: x["field"] == key).to_list()
                        for config_field in config_fields:
                            if config_field.get("is_show",1) == 0:
                                continue
                            old_value = str(operation_log["detail"].get(key, ""))
                            new_value = str(operation_log["update_detail"].get(key, ""))
                            old_value_remark = self._convert_remark(config_field, old_value)
                            new_value_remark = self._convert_remark(config_field, new_value)
                            sort_index = config_list.index(config_field)
                            if is_all_fields == True:
                                info = {}
                                info["field"] = key
                                info["out_ways"] = config_field.get("out_ways",0)
                                info["sort_index"] = config_field.get("sort_index",sort_index)
                                info["old_value"] = old_value
                                info["new_value"] = new_value
                                info["is_update"] = 1 if info["old_value"] != info["new_value"] else 0
                                info["remark"] = config_field.get("remark","-")
                                info["old_value_remark"] = old_value_remark
                                info["new_value_remark"] = new_value_remark
                                operation_log["contrast_info"].append(info)
                            else:
                                if new_value != old_value:
                                    info = {}
                                    info["field"] = key
                                    info["out_ways"] = config_field.get("out_ways",0)
                                    info["sort_index"] = config_field.get("sort_index",sort_index)
                                    info["old_value"] = old_value
                                    info["new_value"] = new_value
                                    info["is_update"] = 1
                                    info["remark"] = config_field.get("remark", "-")
                                    info["old_value_remark"] = old_value_remark
                                    info["new_value_remark"] = new_value_remark
                                    operation_log["contrast_info"].append(info)
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【获取操作日志对比信息】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【获取操作日志对比信息】" + traceback.format_exc())
        operation_log["contrast_info"] = sorted(operation_log["contrast_info"], key=lambda x:x['sort_index'])
        return operation_log
    
    def get_operation_type_name(self, operation_type):
        """
        :description:  获取操作类型名称
        :param operation_type:操作类型
        :return : 
        :last_editors: HuangJianYi
        """
        if operation_type == 1:
            return "新增"
        elif operation_type == 2:
            return "编辑"
        elif operation_type == 3:
            return "删除"
        elif operation_type == 4:
            return "还原"
        elif operation_type == 5:
            return "复制"
        elif operation_type == 6:
            return "导出"
        elif operation_type == 7:
            return "导入"
        elif operation_type == 8:
            return "上架"
        elif operation_type == 9:
            return "下架"
        elif operation_type == 10:
            return "操作"
        else:
            return ""