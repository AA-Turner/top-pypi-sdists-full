# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-12-20 16:07:52
@LastEditTime: 2025-03-19 18:02:07
@LastEditors: HuangJianYi
@Description: 中台接口相关处理业务模型
"""
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.db_models.function.function_shop_model import *
from seven_cloudapp_frame.models.db_models.function.function_skin_model import *
from seven_cloudapp_frame.models.db_models.function.function_info_model import *
from seven_cloudapp_frame.models.db_models.function.function_module_model import *

class MPBaseModel():
    """
    :description: 中台接口相关处理业务模型
    """
    def __init__(self, context=None, logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def get_custom_function_list(self, store_user_nick, power_project_id=None):
        """
        :description: 获取定制功能列表
        :param store_user_nick: 店铺主帐号名称（会员名）
        :param power_project_id: 权限产品id(用于读取指定产品的权限)
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = power_project_id if power_project_id else share_config.get_value("power_project_id") # 权限产品id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数错误product_id不能为空"
            return invoke_result_data
        if not store_user_nick:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数错误store_user_nick不能为空"
            return invoke_result_data
        try:
            dependency_key = f"high_power_list:{product_id}"
            function_shop_dict_list = FunctionShopModel(context=self.context, is_auto=True).get_cache_dict_list("is_release=1 and product_id=%s and store_user_nick=%s", order_by="id desc", field="*", params=[product_id, store_user_nick], dependency_key=dependency_key, redis_config_dict=config.get_value("redis_function"))
            for item in function_shop_dict_list:
                function_ids = item['function_ids'] = SevenHelper.json_loads(item['function_ids']) if item['function_ids'] else []
                skin_ids = item['skin_ids'] = SevenHelper.json_loads(item['skin_ids']) if item['skin_ids'] else []
                item["function_info_second_list"] = []
                if function_ids:
                    condition_where = ConditionWhere()
                    condition_where.add_condition(SevenHelper.get_condition_by_int_list("id", function_ids))
                    condition_where.add_condition("is_release=1")
                    function_list = FunctionInfoModel(context=self.context, is_auto=True).get_cache_dict_list(condition_where.to_string(), field="function_name as name,key_name", dependency_key=dependency_key, redis_config_dict=config.get_value("redis_function"))
                    item["function_info_second_list"] = function_list or []

                item["skin_ids_second_list"] = []
                if skin_ids:
                    condition_where = ConditionWhere()
                    condition_where.add_condition(SevenHelper.get_condition_by_int_list("id", skin_ids))
                    condition_where.add_condition("is_release=1")
                    skin_list = FunctionSkinModel(context=self.context, is_auto=True).get_cache_dict_list(condition_where.to_string(), field="theme_name as name,theme_id", dependency_key=dependency_key, redis_config_dict=config.get_value("redis_function"))
                    item["skin_ids_second_list"] = skin_list or []
            invoke_result_data.data = function_shop_dict_list
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【获取中台定制功能列表】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【获取中台定制功能列表】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

    def get_public_function_list(self, project_code, app_code=""):
        """
        :description: 获取公共功能列表
        :param project_code: 项目编码
        :param app_code: 项目编码（淘系项目，收费项目列表查询）
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if not project_code:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数错误project_code不能为空"
            return invoke_result_data
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id,SaaS走project_name,SaaS定制走power_project_id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数错误product_id不能为空"
            return invoke_result_data
        try:
            dependency_key = f"high_power_list:{product_id}"
            params = [product_id, project_code]
            condition_where = ConditionWhere()
            condition_where.add_condition("is_release=1 and product_id=%s and project_code=%s")
            field = "id,product_id,module_type,module_name as name,app_code,project_code,skin_ids,function_ids"
            if app_code:
                condition_where.add_condition("app_code=%s")
                params.append(app_code)
            function_module_dict_list = FunctionModuleModel(context=self.context, is_auto=True).get_cache_dict_list(condition_where.to_string(), field=field, params=params, dependency_key=dependency_key,redis_config_dict=config.get_value("redis_function"))
            for item in function_module_dict_list:
                function_ids = item['function_ids'] = SevenHelper.json_loads(item['function_ids']) if item['function_ids'] else []
                skin_ids = item['skin_ids'] = SevenHelper.json_loads(item['skin_ids']) if item['skin_ids'] else []

                item["function_info_second_list"] = []
                if function_ids:
                    condition_where = ConditionWhere()
                    condition_where.add_condition(SevenHelper.get_condition_by_int_list("id", function_ids))
                    condition_where.add_condition("is_release=1")
                    function_list = FunctionInfoModel(context=self.context, is_auto=True).get_cache_dict_list(condition_where.to_string(), field="function_name as name,key_name", dependency_key=dependency_key,redis_config_dict=config.get_value("redis_function"))
                    item["function_info_second_list"] = function_list or []

                item["skin_ids_second_list"] = []
                if skin_ids:
                    condition_where = ConditionWhere()
                    condition_where.add_condition(SevenHelper.get_condition_by_int_list("id", skin_ids))
                    condition_where.add_condition("is_release=1")
                    skin_list = FunctionSkinModel(context=self.context, is_auto=True).get_cache_dict_list(condition_where.to_string(), field="theme_name as name,theme_id", dependency_key=dependency_key,redis_config_dict=config.get_value("redis_function"))
                    item["skin_ids_second_list"] = skin_list or []

            invoke_result_data.data = function_module_dict_list
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【获取中台公共功能列表】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【获取中台公共功能列表】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

    def get_key_power_list(self, store_user_nick, project_code, key_names, user_type=0):
        """
        :description: 指定模块权限列表
        :param store_user_nick: 店铺主帐号名称（会员名）
        :param project_code: 项目编码
        :param key_names: 权限代码，多个逗号分隔
        :param user_type:  0-不限1-SAAS用户2-SAAS定制用户
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id,SaaS走project_name,SaaS定制走power_project_id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数错误product_id不能为空"
            return invoke_result_data
        if not key_names:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "权限代码key_names不能为空"
            return invoke_result_data
        try:
            dependency_key = f"high_power_list:{product_id}"
            params = [product_id]
            condition_where = ConditionWhere()
            condition_where.add_condition("is_release=1 and product_id=%s")
            if store_user_nick:
                condition_where.add_condition("store_user_nick=%s")
                params.append(store_user_nick)
            if user_type:
                condition_where.add_condition("user_type=%s")
                params.append(user_type)
            function_shop_dict = FunctionShopModel(context=self.context, is_auto=True).get_cache_dict(condition_where.to_string(), field="function_ids", params=params, dependency_key=dependency_key, redis_config_dict=config.get_value("redis_function"))
            if function_shop_dict:
                function_id_list = SevenHelper.json_loads(function_shop_dict["function_ids"])
            else:
                function_module_dict = FunctionModuleModel(context=self.context, is_auto=True).get_cache_dict("is_release=1 and product_id=%s and project_code=%s", params=[product_id, project_code], dependency_key=dependency_key, redis_config_dict=config.get_value("redis_function"))
                if not function_module_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此产品无此项目编码"
                    return invoke_result_data
                function_id_list = SevenHelper.json_loads(function_module_dict["function_ids"])

            key_name_list = key_names.split(",")
            result_data = []
            function_info_list = FunctionInfoModel(context=self.context, is_auto=True).get_cache_dict_list("is_release=1 and " + SevenHelper.get_condition_by_str_list("key_name", key_name_list), field="id,key_name", dependency_key=dependency_key, redis_config_dict=config.get_value("redis_function"))
            for key_name in key_name_list:
                if function_info_list:
                    for function_info in function_info_list:
                        if key_name == function_info["key_name"]:
                            func_id = function_info["id"]
                            if func_id in function_id_list:
                                result_data.append({"key_name": key_name, "is_power": True})
                            else:
                                result_data.append({"key_name": key_name, "is_power": False})
                        else:
                            result_data.append({"key_name": key_name, "is_power": False})
                else:
                    result_data.append({"key_name": key_name, "is_power": False})
            invoke_result_data.data = result_data
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【获取中台指定模块权限列表】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【获取中台指定模块权限列表】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

    def check_high_power(self, store_user_nick, project_code, key_names, user_type=0):
        """
        :description:  检验是否有指定模块的权限
        :param store_user_nick:商家主账号昵称
        :param project_code:项目编码
        :param key_names:权限代码，多个逗号分隔 
        :param user_type:0-不限1-SAAS用户2-SAAS定制用户
        :return bool: 是否有权限
        :last_editors: HuangJianYi
        """
        is_power = True
        invoke_result_data = self.get_key_power_list(store_user_nick, project_code, key_names, user_type)
        if invoke_result_data.success == True:
            for key in invoke_result_data.data:
                if key["is_power"] == False:
                    is_power = False
                    break
        else:
            is_power = False
        return is_power

    def get_api_public_function_list(self, project_code, return_response_status=False):
        """
        :description:  获取公共功能列表
        :param project_code:收费项目代码（服务管理-收费项目列表）
        :param return_response_status:是否返回响应状态
        :return list: 
        :last_editors: HuangJianYi
        """
        response_status = False
        public_function_list = []
        if not project_code:
            if return_response_status:
                return public_function_list,response_status
            return public_function_list
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id,SaaS走project_name,SaaS定制走power_project_id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            if return_response_status:
                return public_function_list,response_status
            return public_function_list
        requst_url = share_config.get_value("mp_url","http://taobao-mp-s.gao7.com") + "/general/project_code_list"
        data = {}
        data["project_code"] = project_code
        data["product_id"] = product_id
        result = HTTPHelper.get(requst_url, data, {"Content-Type": "application/json"})
        if result and result.ok and result.text:
            obj_data = SevenHelper.json_loads(result.text)
            if obj_data and obj_data["Data"]:
                public_function_list = obj_data["Data"]
                response_status = True
        if return_response_status:
            return public_function_list,response_status
        return public_function_list

    def get_api_custom_function_list(self, store_user_nick, return_response_status=False):
        """
        :description:  获取定制功能列表，权限产品id（power_project_id）,SaaS定制走power_project_id必须配置，SaaS可不配置走project_name,对应中台表function_product_tb的app_id字段
        :param store_user_nick:商家主账号昵称
        :param return_response_status:是否返回响应状态
        :return list: 
        :last_editors: HuangJianYi
        """
        response_status = False
        custom_function_list = []
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            if return_response_status:
                return custom_function_list,response_status
            return custom_function_list
        requst_url = share_config.get_value("mp_url", "http://taobao-mp-s.gao7.com") + "/custom/query_skin_managemen_list"
        data = {}
        data["product_id"] = product_id
        data["store_user_nick"] = store_user_nick
        result = HTTPHelper.get(requst_url, data, {"Content-Type": "application/json"})
        if result and result.ok and result.text:
            obj_data = SevenHelper.json_loads(result.text)
            if obj_data and obj_data["Data"]:
                custom_function_list = obj_data["Data"]
                response_status = True
        if return_response_status:
            return custom_function_list,response_status
        return custom_function_list

    def get_api_key_power_list(self, store_user_nick, project_code, key_names, user_type=0, return_response_status=False):
        """
        :description:  指定模块权限列表，权限产品id（power_project_id）,SaaS定制走power_project_id必须配置，SaaS可不配置走project_name,对应中台表function_product_tb的app_id字段
        :param store_user_nick:商家主账号昵称
        :param project_code:项目编码
        :param key_names:权限代码，多个逗号分隔
        :param user_type:0-不限1-SAAS用户2-SAAS定制用户
        :param return_response_status:是否返回响应状态
        :return list: 
        :last_editors: HuangJianYi
        """
        response_status = False
        power_list = []
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            if return_response_status:
                return power_list,response_status
            return power_list
        requst_url = share_config.get_value("mp_url", "http://taobao-mp-s.gao7.com") + "/general/jurisdiction_list"
        data = {}
        data["product_id"] = product_id
        data["project_code"] = project_code
        data["store_user_nick"] = store_user_nick
        data["key_name"] = key_names
        if user_type > 0:
            data["user_type"] = user_type
        result = HTTPHelper.get(requst_url, data, {"Content-Type": "application/json"})
        if result and result.ok and result.text:
            obj_data = SevenHelper.json_loads(result.text)
            if obj_data and obj_data["Data"]:
                power_list = obj_data["Data"]
                response_status = True
        if return_response_status:
            return power_list,response_status
        return power_list

    def check_api_high_power(self, store_user_nick, project_code, key_names, user_type=0, return_response_status=False):
        """
        :description:  检验是否有指定模块的权限
        :param store_user_nick:商家主账号昵称
        :param project_code:项目编码
        :param key_names:权限代码，多个逗号分隔 
        :param user_type:0-不限1-SAAS用户2-SAAS定制用户
        :param return_response_status:是否返回响应状态
        :return bool: 是否有权限
        :last_editors: HuangJianYi
        """
        response_status = False
        if return_response_status == True:
            power_list, response_status = self.get_api_key_power_list(store_user_nick, project_code, key_names, user_type, return_response_status)
        else:
            power_list = self.get_key_power_list(store_user_nick, project_code, key_names, user_type)
        is_power = True
        for key in power_list:
            if key["is_power"] == False:
                is_power = False
                break
        if return_response_status == True:
            return is_power,response_status
        return is_power
