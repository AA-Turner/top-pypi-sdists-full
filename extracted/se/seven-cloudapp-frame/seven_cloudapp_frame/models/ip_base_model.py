# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 09:44:36
@LastEditTime: 2025-03-28 18:46:45
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.customize.safe_helper import SafeHelper
from seven_cloudapp_frame.models.db_models.ip.ip_info_model import *
from seven_cloudapp_frame.models.db_models.ip.ip_type_model import *

class IpBaseModel():
    """
    :description: IP信息业务模型
    """
    def __init__(self,context=None,logging_error=None,logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def _delete_ip_info_dependency_key(self, act_id, ip_id=0, delay_delete_time=0.01):
        """
        :description: 删除ip信息依赖建
        :param act_id: 活动标识
        :param ip_id: ip标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: HuangJianYi
        """
        dependency_key_list = [DependencyKey.ip_info_list(act_id)]
        if ip_id:
            dependency_key_list.append(DependencyKey.ip_info(ip_id))
        IpInfoModel().delete_dependency_key(dependency_key_list, delay_delete_time)
        
    def _delete_ip_type_dependency_key(self, act_id, type_id=0, delay_delete_time=0.01):
        """
        :description: 删除ip类型依赖建
        :param act_id: 活动标识
        :param type_id: ip类型标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: HuangJianYi
        """
        dependency_key_list = [DependencyKey.ip_type(type_id)]
        if type_id:
            dependency_key_list.append(DependencyKey.ip_type_list(act_id))
        IpTypeModel().delete_dependency_key(dependency_key_list, delay_delete_time)

    def save_ip_info(self, app_id,act_id,ip_id,ip_name,ip_pic,show_pic,sort_index,is_release,ip_type,ip_summary,mode_type=0,ip_config_json=None, is_set_cache=True):
        """
        :description: 保存ip信息
        :param app_id：应用标识
        :param act_id：活动标识
        :param ip_id: ip标识
        :param ip_name：ip名称
        :param ip_pic：ip图片
        :param show_pic：展示图片
        :param sort_index：排序
        :param is_release：是否发布
        :param ip_type：ip类型
        :param ip_summary：ip描述
        :param mode_type：模式类型
        :param ip_config_json：ip配置
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not act_id or not ip_name:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        ip_info = None
        old_ip_info = None
        is_add = False
        ip_info_model = IpInfoModel(context=self.context)
        if ip_id > 0:
            ip_info = ip_info_model.get_entity_by_id(ip_id)
            if not ip_info or ip_info.app_id != app_id:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "ip信息不存在"
                return invoke_result_data
            old_ip_info = deepcopy(ip_info)
        if not ip_info:
            is_add = True
            ip_info = IpInfo()
        ip_info.app_id = app_id
        ip_info.act_id = act_id
        ip_info.ip_name = ip_name
        ip_info.ip_type = ip_type
        ip_info.ip_pic = ip_pic
        ip_info.show_pic = show_pic
        ip_info.ip_summary = ip_summary
        ip_info.sort_index = sort_index
        ip_info.is_release = is_release
        ip_info.mode_type = mode_type
        if ip_config_json != None:
            ip_info.ip_config_json = ip_config_json
        ip_info.modify_date = SevenHelper.get_now_datetime()
        if is_add:
            ip_info.create_date = ip_info.modify_date
            ip_info.id = ip_info_model.add_entity(ip_info)
        else:
            ip_info_model.update_entity(ip_info,exclude_field_list="app_id,act_id")
        result = {}
        result["is_add"] = is_add
        result["new"] = ip_info
        result["old"] = old_ip_info
        invoke_result_data.data = result
        if is_set_cache == True and ip_id > 0:
            self._delete_ip_info_dependency_key(act_id, 0)
            ip_info_model.set_cache_dict_by_id(ip_id, ip_info.__dict__, dependency_key=DependencyKey.ip_info(ip_id))
        else:
            self._delete_ip_info_dependency_key(act_id, ip_id)
        return invoke_result_data

    def get_ip_info_list(self, app_id, act_id, page_size, page_index, is_del=0,is_release=-1, field="*", condition="", params=[], order_by="sort_index desc", is_cache=True, page_count_mode="total", dependency_key=""):
        """
        :description: 获取IP列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param page_size：页大小
        :param page_index：页索引
        :param is_del: 是否回收站1是0否
        :param is_release: 是否发布1是0否
        :param field：字段
        :param condition：条件
        :param params：参数数组
        :param order_by：排序
        :param is_cache：是否缓存
        :param page_count_mode: 分页计数模式 total-计算总数(默认) next-计算是否有下一页(bool) none-不计算
        :param dependency_key：依赖建
        :return: list
        :last_editors: HuangJianYi
        """
        params_list = []
        condition_where = ConditionWhere()
        if app_id:
            condition_where.add_condition("app_id=%s")
            params_list.append(app_id)
        if act_id != 0:
            condition_where.add_condition("act_id=%s")
            params_list.append(act_id)
        if condition:
            condition_where.add_condition(condition)
            params_list.extend(params)
        if is_del != -1:
            condition_where.add_condition("is_del=%s")
            params_list.append(is_del)
        if is_release != -1:
            condition_where.add_condition("is_release=%s")
            params_list.append(is_release)
        if is_cache == True:
            if not dependency_key:
                dependency_key = DependencyKey.ip_info_list(act_id)
            page_list = IpInfoModel(context=self.context, is_auto=True).get_cache_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params_list, dependency_key=dependency_key, cache_expire=600, page_count_mode=page_count_mode)
        else:
            page_list = IpInfoModel(context=self.context).get_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params_list, page_count_mode=page_count_mode)
        return page_list

    def update_ip_info_status(self, app_id, ip_id, is_del, is_set_cache=True):
        """
        :description: 删除ip
        :param app_id：应用标识
        :param ip_id：ip标识
        :param is_del：0-还原，1-删除
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        ip_info_model = IpInfoModel(context=self.context)
        ip_info_dict = ip_info_model.get_dict_by_id(ip_id)
        if not ip_info_dict or SafeHelper.authenticat_app_id(ip_info_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "ip信息不存在"
            return invoke_result_data
        is_release = 0
        del_date = SevenHelper.get_now_datetime()

        invoke_result_data.success = ip_info_model.update_table("is_del=%s,is_release=%s,modify_date=%s,del_date=%s", "id=%s", [is_del, is_release, del_date, del_date, ip_id])
        if is_set_cache == True:
            ip_info_dict['is_del'] = is_del
            ip_info_dict['is_release'] = is_release
            ip_info_dict['modify_date'] = del_date
            ip_info_dict['del_date'] = del_date
            self._delete_ip_info_dependency_key(ip_info_dict["act_id"], 0)
            ip_info_model.set_cache_dict_by_id(ip_id, ip_info_dict, dependency_key=DependencyKey.ip_info(ip_id))
        else:
            self._delete_ip_info_dependency_key(ip_info_dict["act_id"], ip_id)
        invoke_result_data.data = ip_info_dict
        return invoke_result_data

    def release_ip_info(self, app_id, ip_id, is_release, is_set_cache=True):
        """
        :description: ip上下架
        :param app_id：应用标识
        :param ip_id：ip标识
        :param is_release: 是否发布 1-是 0-否
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        ip_info_model = IpInfoModel(context=self.context)
        ip_info_dict = ip_info_model.get_dict_by_id(ip_id)
        if not ip_info_dict or SafeHelper.authenticat_app_id(ip_info_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "ip信息不存在"
            return invoke_result_data
        modify_date = SevenHelper.get_now_datetime()
        invoke_result_data.success = ip_info_model.update_table("is_release=%s,modify_date=%s", "id=%s", [is_release, modify_date, ip_id])
        if is_set_cache == True:
            ip_info_dict['is_release'] = is_release
            ip_info_dict['modify_date'] = modify_date
            self._delete_ip_info_dependency_key(ip_info_dict["act_id"], 0)
            ip_info_model.set_cache_dict_by_id(ip_id, ip_info_dict, dependency_key=DependencyKey.ip_info(ip_id))
        else:
            self._delete_ip_info_dependency_key(ip_info_dict["act_id"], ip_id)
        invoke_result_data.data = ip_info_dict
        return invoke_result_data

    def save_ip_type(self,app_id,act_id,ip_type_id,type_name,sort_index,is_release,type_pic="", is_set_cache=True):
        """
        :description: 保存ip类型
        :param app_id：应用标识
        :param act_id：活动标识
        :param ip_type_id：ip类型标识
        :param type_name：类型名称
        :param sort_index：排序
        :param is_release：是否发布
        :param type_pic：类型图片
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not act_id or not type_name:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        ip_type = None
        old_ip_type = None
        is_add = False
        ip_type_model = IpTypeModel(context=self.context)
        if ip_type_id > 0:
            ip_type = ip_type_model.get_entity_by_id(ip_type_id)
            if not ip_type or SafeHelper.authenticat_app_id(ip_type.app_id, app_id) == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "ip类型信息不存在"
                return invoke_result_data
            old_ip_type = deepcopy(ip_type)
        if not ip_type:
            is_add = True
            ip_type = IpType()
        ip_type.app_id = app_id
        ip_type.act_id = act_id
        ip_type.type_name = type_name
        ip_type.type_pic = type_pic
        ip_type.sort_index = sort_index
        ip_type.is_release = is_release
        ip_type.modify_date = SevenHelper.get_now_datetime()
        if is_add:
            ip_type.create_date = ip_type.modify_date
            ip_type.id = ip_type_model.add_entity(ip_type)
        else:
            ip_type_model.update_entity(ip_type,exclude_field_list="app_id,act_id")
        result = {}
        result["is_add"] = is_add
        result["new"] = ip_type
        result["old"] = old_ip_type
        invoke_result_data.data = result
        if is_set_cache == True and ip_type_id > 0:
            self._delete_ip_type_dependency_key(act_id, 0)
            ip_type_model.set_cache_dict_by_id(ip_type_id, ip_type.__dict__, dependency_key=DependencyKey.ip_type(ip_type_id))
        else:
            self._delete_ip_type_dependency_key(act_id, ip_type_id)
        return invoke_result_data

    def get_ip_type_list(self, app_id, act_id, page_size, page_index,is_release=-1, field="*", condition="", params=[], order_by="sort_index desc", is_cache=True, page_count_mode="total"):
        """
        :description: 获取IP类型列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param page_size：页大小
        :param page_index：页索引
        :param is_release: 是否发布1是0否
        :param field：字段
        :param condition：条件
        :param params：参数数组
        :param order_by：排序
        :param is_cache：是否缓存
        :param page_count_mode: 分页计数模式 total-计算总数(默认) next-计算是否有下一页(bool) none-不计算
        :return:
        :last_editors: HuangJianYi
        """
        params_list = []
        condition_where = ConditionWhere()
        if app_id:
            condition_where.add_condition("app_id=%s")
            params_list.append(app_id)
        if act_id != 0:
            condition_where.add_condition("act_id=%s")
            params_list.append(act_id)
        if condition:
            condition_where.add_condition(condition)
            params_list.extend(params)
        if is_release != -1:
            condition_where.add_condition("is_release=%s")
            params_list.append(is_release)
        if is_cache == True:
            page_list = IpTypeModel(context=self.context, is_auto=True).get_cache_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params_list, dependency_key=DependencyKey.ip_type_list(act_id), cache_expire=600, page_count_mode=page_count_mode)
        else:
            page_list = IpTypeModel(context=self.context).get_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by, params=params_list, page_count_mode=page_count_mode)
        return page_list

    def release_ip_type(self,app_id, ip_type_id, is_release, is_set_cache=True):
        """
        :description: ip上下架
        :param app_id：应用标识
        :param ip_type_id：ip类型标识
        :param is_release: 是否发布 1-是 0-否
        :param is_set_cache: 是否设置缓存，默认True False-则是删除依赖建
        :return: 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        ip_type_model = IpTypeModel(context=self.context)
        ip_type_dict = ip_type_model.get_dict_by_id(ip_type_id)
        if not ip_type_dict or SafeHelper.authenticat_app_id(ip_type_dict["app_id"], app_id) == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "ip信息不存在"
            return invoke_result_data
        modify_date = SevenHelper.get_now_datetime()
        invoke_result_data.success = ip_type_model.update_table("is_release=%s,modify_date=%s", "id=%s", [is_release, modify_date, ip_type_id])
        if is_set_cache == True and ip_type_id > 0:
            ip_type_dict['is_release'] = is_release
            ip_type_dict['modify_date'] = modify_date
            self._delete_ip_type_dependency_key(ip_type_dict["act_id"], 0)
            ip_type_model.set_cache_dict_by_id(ip_type_id, ip_type_dict, dependency_key=DependencyKey.ip_type(ip_type_id))
        else:
            self._delete_ip_type_dependency_key(ip_type_dict["act_id"], ip_type_id)
        invoke_result_data.data = ip_type_dict
        return invoke_result_data