# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-03 10:43:58
@LastEditTime: 2025-07-01 10:52:12
@LastEditors: HuangJianYi
@Description: 应用模块
"""
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.top_base_model import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.mp_base_model import *
from seven_cloudapp_frame.models.asset_base_model import *
from seven_cloudapp_frame.models.db_models.app.app_template_model import *
from seven_cloudapp_frame.models.db_models.app.app_relation_model import *
from asq.initiators import query


class InstantiateAppHandler(ClientBaseHandler):
    """
    :description: 实例化小程序
    """
    def get_async(self):
        """
        :description: 实例化小程序
        :param app_id:应用标识
        :param user_nick:用户昵称
        :param access_token:access_token
        :param is_log：是否记录返回信息
        :return app_info
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        user_nick = self.get_user_nick()
        access_token = self.get_access_token()
        main_user_open_id = self.get_param("main_user_open_id")
        is_log = int(self.get_param("is_log", 0))
        is_log = True if is_log == 1 else False

        redis_init = RedisExHelper.init(config_dict=config.get_value("redis_safe"))
        cache_key = f"instantiate:{user_nick}"
        if SevenHelper.is_continue_request(cache_key, 60000) == True:
            return self.response_json_error("error","操作太频繁,请60秒后再试")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            redis_init.delete(cache_key)
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message,invoke_result_data.data)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        template_version = invoke_result_data.data.get("template_version", '')
        app_key, app_secret = self.get_app_key_secret()
        top_base_model = TopBaseModel(context=self)
        invoke_result_data = top_base_model.instantiate(app_id, user_nick, access_token, app_key, app_secret, is_log, main_user_open_id, template_version=template_version)
        if invoke_result_data.success == False:
            redis_init.delete(cache_key)
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message,invoke_result_data.data)
        ref_params = {}
        if user_nick and share_config.get_value("is_multiple_instantiate", False) == True:
            relation_app_list = []
            app_template_model = AppTemplateModel(context=self)
            app_relation_model = AppRelationModel(context=self)
            app_template_dict_list = app_template_model.get_dict_list()
            if len(app_template_dict_list) > 0:
                store_user_nick = user_nick.split(':')[0] if user_nick else ""
                app_info_dict_list = AppInfoModel(context=self).get_dict_list("store_user_nick=%s", field="template_id", params=[store_user_nick])
                for app_template_dict in app_template_dict_list:
                    if query(app_info_dict_list).count(lambda x: x["template_id"] == app_template_dict["template_id"]) > 0:
                        continue
                    relation_invoke_result_data = top_base_model.instantiate("", user_nick, access_token, app_key, app_secret, is_log, main_user_open_id, app_name=app_template_dict["product_name"], description=app_template_dict["product_desc"], icon=app_template_dict["product_icon"],
                                                                             template_id=app_template_dict["template_id"], template_version=app_template_dict["client_ver"], is_instance=2)
                    if relation_invoke_result_data.success == False:
                        self.logging_link_error(f"模板ID：{app_template_dict['template_id']}实例化失败，原因：{relation_invoke_result_data.error_message}")
                    else:
                        app_relation = AppRelation()
                        app_relation.app_id = invoke_result_data.data["app_id"]
                        app_relation.template_id = share_config.get_value("client_template_id")
                        app_relation.ref_app_id = relation_invoke_result_data.data["app_id"]
                        app_relation.ref_template_id = app_template_dict["template_id"]
                        app_relation.create_date = TimeHelper.get_now_format_time()
                        relation_app_list.append(app_relation)
                if len(relation_app_list) > 0:
                    app_relation_model.add_list(relation_app_list)
                    app_relation_model.delete_dependency_key(DependencyKey.app_relation(invoke_result_data.data["app_id"]))
                ref_params["relation_app_list"] = relation_app_list

        # 判断是否首次实例化，是的话更新项目版本号
        if invoke_result_data.data.get("is_first_instance", False) == True:
            base_info = BaseInfoModel(context=self).get_entity()
            if base_info and base_info.project_ver:
                AppInfoModel(context=self).update_table("project_ver=%s", "app_id=%s", [base_info.project_ver, invoke_result_data.data["app_id"]])

        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            redis_init.delete(cache_key)
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        redis_init.delete(cache_key)
        return self.response_json_success(invoke_result_data.data)


class UpdateTelephoneHandler(ClientBaseHandler):
    """
    :description: 更新手机号
    """
    @filter_check_params("telephone")
    def get_async(self):
        """
        :description: 更新手机号
        :param app_id:应用标识
        :param telephone：手机号
        :param check_code：验证码
        :return: 
        :last_editors: HuangJianYi
        """
        open_id = self.get_open_id()
        app_id = self.get_app_id()
        telephone = self.get_param("telephone")
        check_code = self.get_param("check_code")
        modify_date = self.get_now_datetime()

        check_code_re = SevenHelper.redis_init().get(f"user_bind_phone_code:{open_id}_{telephone}")
        if check_code_re == None:
            return self.response_json_error("error", "验证码已过期")
        if check_code != check_code_re:
            return self.response_json_error("error", "验证码错误")
        app_info_model = AppInfoModel(context=self)
        app_info_model.update_table("app_telephone=%s,modify_date=%s", "app_id=%s", [telephone, modify_date, app_id])
        app_info_model.delete_dependency_key(DependencyKey.app_info(app_id))
        return self.response_json_success()


class VersionUpgradeHandler(ClientBaseHandler):
    """
    :description: 前端版本更新
    """
    def get_async(self):
        """
        :description: 前端版本更新
        :param app_id:应用标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        access_token = self.get_access_token()
        user_nick = self.get_user_nick()
        is_log = int(self.get_param("is_log", 0))
        is_log = True if is_log == 1 else False

        base_info = BaseInfoModel(context=self).get_entity()
        client_ver = base_info.client_ver
        store_user_nick = user_nick.split(':')[0]

        app_info_model = AppInfoModel(context=self)
        app_info = app_info_model.get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.response_json_error("no_app", "小程序不存在")
        test_config = share_config.get_value("test_config", {})
        test_client_ver = test_config.get("client_ver","")
        client_template_id = share_config.get_value("client_template_id")
        #配置文件指定账号升级
        if test_client_ver and store_user_nick and store_user_nick == test_config.get("user_nick",""):
            client_ver = test_client_ver
        else:
            #中台指定账号升级
            version_info = VersionInfoModel(context=self).get_entity(where="type_id=1",order_by="id desc")
            if version_info:
                if version_info.update_scope == 2 and version_info.white_lists:
                    white_lists = SevenHelper.json_loads(version_info.white_lists)
                    if isinstance(white_lists, str):
                        white_lists = white_lists.split(',')
                    if store_user_nick in white_lists:
                        client_ver = version_info.version_number

        invoke_result_data = InvokeResultData()
        top_base_model = TopBaseModel(context=self)
        app_key, app_secret = self.get_app_key_secret()
        if client_ver != app_info.template_ver:
            invoke_result_data = top_base_model.version_upgrade(app_id, client_template_id, client_ver, access_token, app_key, app_secret, app_info, is_log)
            if invoke_result_data.success == False:
                return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
            app_info_model.delete_dependency_key(DependencyKey.app_info(app_id))

        return self.response_json_success(invoke_result_data.data)


class AppInfoHandler(ClientBaseHandler):
    """
    :description: 获取小程序信息
    """
    @filter_check_params()
    def get_async(self):
        """
        :description: 获取小程序信息
        :return app_info
        :last_editors: HuangJianYi
        """
        main_user_open_id = self.get_param("main_user_open_id")
        app_base_model = AppBaseModel(context=self)
        app_key, app_secret = self.get_app_key_secret()
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        invoke_result_data = app_base_model.get_app_info_result(self.get_user_nick(), self.get_open_id(), self.get_access_token(), app_key, app_secret, main_user_open_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data = self.business_process_executed(invoke_result_data, {})
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)


class CheckGmPowerHandler(ClientBaseHandler):
    """
    :description: 校验是否有GM工具权限
    """
    def get_async(self):
        """
        :description: 校验是否有GM工具权限
        :param 
        :return: True是 False否
        :last_editors: HuangJianYi
        """
        is_power = False
        user_nick = self.get_user_nick()
        if not user_nick:
            return self.response_json_error("error", "对不起,请先授权登录")
        store_user_nick = user_nick.split(':')[0]
        condition_where = ConditionWhere()
        condition_where.add_condition("store_user_nick=%s")
        params = [store_user_nick]
        template_id = share_config.get_value("client_template_id")
        if template_id:
            condition_where.add_condition("template_id=%s")
            params.append(template_id)
        app_info_dict = AppInfoModel(context=self).get_dict(condition_where.to_string(), field="is_gm", params=params)
        if not app_info_dict:
            is_power = False
        if app_info_dict["is_gm"] == 1:
            is_power = True
        return self.response_json_success(is_power)


class GetAppidByGmHandler(ClientBaseHandler):
    """
    :description: GM工具获取应用标识
    """
    @filter_check_params("store_name")
    def get_async(self):
        """
        :description: 获取应用标识
        :param store_name:店铺名称
        :return app_id
        :last_editors: HuangJianYi
        """
        app_id = ""
        store_name = self.get_param("store_name")
        user_nick = self.get_user_nick()
        if not user_nick:
            return self.response_json_error("error", "对不起,请先授权登录")
        store_user_nick = user_nick.split(':')[0]
        is_power = False
        condition_where = ConditionWhere()
        condition_where.add_condition("store_user_nick=%s")
        params = [store_user_nick]
        template_id = share_config.get_value("client_template_id")
        if template_id:
            condition_where.add_condition("template_id=%s")
            params.append(template_id)
        app_info_dict = AppInfoModel(context=self).get_dict(condition_where.to_string(), field="is_gm", params=params)
        if app_info_dict and app_info_dict["is_gm"] == 1:
            is_power = True
        if is_power == True:
            condition_where = ConditionWhere()
            condition_where.add_condition("store_name=%s")
            params = [store_name]
            template_id = share_config.get_value("client_template_id")
            if template_id:
                condition_where.add_condition("template_id=%s")
                params.append(template_id)
            app_info_dict = AppInfoModel(context=self).get_dict(condition_where.to_string(), field="app_id", params=params)
            if app_info_dict:
                app_id = app_info_dict["app_id"]
        return self.response_json_success(app_id)


class GetShortUrlHandler(ClientBaseHandler):
    """
    :description: 获取淘宝短链接
    """
    def get_async(self):
        """
        :description: 获取淘宝短链接
        :param url:链接地址
        :return: 
        :last_editors: HuangJianYi
        """
        access_token = self.get_access_token()
        is_log = int(self.get_param("is_log", 0))
        is_log = True if is_log == 1 else False
        url = self.get_param("url")
        top_base_model = TopBaseModel(context=self)
        app_key, app_secret = self.get_app_key_secret()
        invoke_result_data = top_base_model.get_short_url(url, access_token, app_key, app_secret, is_log)
        if invoke_result_data.success == False:
            return self.response_json_success("")
        else:
            return self.response_json_success(invoke_result_data.data)


class GetHighPowerListHandler(ClientBaseHandler):
    """
    :description: 获取中台配置的高级权限列表
    """
    def get_async(self):
        """
        :description: 获取中台配置的高级权限列表
        :return: list
        :last_editors: HuangJianYi
        """
        user_nick = self.get_user_nick()
        if not user_nick:
            return self.response_json_error("Error", "对不起,请先授权登录")
        store_user_nick = user_nick.split(':')[0]
        access_token = self.get_access_token()
        top_base_model = TopBaseModel(context=self)
        mp_base_model = MPBaseModel(context=self)
        # 如果登录账号的主账号等于配置文件指定的测试账号，则取子账号进行权限的获取，方便不同子账号进到不同的SaaS定制
        test_config = share_config.get_value("test_config", {})
        invoke_result_data = mp_base_model.get_custom_function_list(user_nick) if store_user_nick and store_user_nick == test_config.get("user_nick", "") else mp_base_model.get_custom_function_list(store_user_nick)
        if invoke_result_data.success == True:
            custom_function_list = invoke_result_data.data if invoke_result_data.data else []
        else:
            custom_function_list = mp_base_model.get_api_custom_function_list(user_nick) if store_user_nick and store_user_nick == test_config.get("user_nick", "") else mp_base_model.get_api_custom_function_list(store_user_nick)
        config_data_list = []
        if len(custom_function_list) == 0:
            config_data = {}
            config_data["is_customized"] = 0
            config_data["name"] = ""
            config_data["project_code"] = ""
            config_data["cloud_app_id"] = 0
            config_data["function_config_list"] = []
            config_data["skin_config_list"] = []
            app_key, app_secret = self.get_app_key_secret()
            #获取项目编码
            project_code = top_base_model.get_project_code(store_user_nick, access_token, app_key, app_secret)
            invoke_result_data = mp_base_model.get_public_function_list(project_code)
            if invoke_result_data.success == True:
                public_function_list = invoke_result_data.data if invoke_result_data.data else []
            else:
                public_function_list = mp_base_model.get_api_public_function_list(project_code)
            if len(public_function_list) > 0:
                config_data["function_config_list"] = query(public_function_list[0]["function_info_second_list"]).select(lambda x: {"name": x["name"], "key_name": x["key_name"]}).to_list()
                config_data["skin_config_list"] = query(public_function_list[0]["skin_ids_second_list"]).select(lambda x: {"name": x["name"], "theme_id": x["theme_id"]}).to_list()
                config_data["name"] = public_function_list[0]["name"]
                config_data["project_code"] = public_function_list[0]["project_code"]
            config_data_list.append(config_data)
        else:
            for custom_function in custom_function_list:
                config_data = {}
                config_data["is_customized"] = 1
                config_data["name"] = "定制版"
                config_data["project_code"] = ""
                config_data["cloud_app_id"] = custom_function["cloud_app_id"]
                config_data["function_config_list"] = query(custom_function["function_info_second_list"]).select(lambda x: {"name": x["name"], "key_name": x["key_name"]}).to_list()
                config_data["skin_config_list"] = query(custom_function["skin_ids_second_list"]).select(lambda x: {"name": x["name"], "theme_id": x["theme_id"]}).to_list()
                config_data["module_name"] = custom_function["module_name"]
                config_data["module_pic"] = custom_function["module_pic"]
                config_data_list.append(config_data)
        self.response_json_success(config_data_list)


class UpdateStoreAssetHandler(ClientBaseHandler):
    """
    :description: 变更商家资产
    """
    @filter_check_params("asset_type,asset_value")
    def post_async(self):
        """
        :description: 变更资产
        :param app_id：应用标识
        :param asset_type：资产类型
        :param asset_value：变更的资产值
        :param asset_object_id：资产对象标识
        :param store_id：商家ID
        :param store_name：商家名称
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        asset_type = int(self.get_param("asset_type", 0))
        asset_value = int(self.get_param("asset_value", 0))
        asset_object_id = self.get_param("asset_object_id")
        store_id = self.get_param("store_id")
        store_name = self.get_param("store_name")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code,invoke_result_data.error_message)

        asset_base_model = AssetBaseModel(context=self)
        invoke_result_data = asset_base_model.update_store_asset(app_id, store_id, store_name, asset_type, asset_value, asset_object_id, 3, "", "手动配置", "手动配置")
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code,invoke_result_data.error_message)
        title = "资产配置；"
        if asset_type == 1:
            title = "次数配置；"
        elif asset_type == 2:
            title = "积分配置；"
        elif asset_type == 3:
            title = "档位配置；"
        title = title + "店铺名称：" + store_name + "，store_id：" + store_id
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="store_asset_tb", title=title)
        ref_params = {}
        self.business_process_executed(invoke_result_data, ref_params)
        return self.response_json_success()


class StoreAssetListHandler(ClientBaseHandler):
    """
    :description: 获取商家资产列表
    """
    def get_async(self):
        """
        :description: 获取商家资产列表
        :param app_id：应用标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        asset_type = int(self.get_param("asset_type", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        asset_base_model = AssetBaseModel(context=self)
        ref_params = {}
        return self.response_json_success(self.business_process_executed(asset_base_model.get_store_asset_list(app_id, asset_type), ref_params))


class StoreAssetLogListHandler(ClientBaseHandler):
    """
    :description: 商家资产流水记录
    """
    def get_async(self):
        """
        :description: 商家资产流水记录
        :param app_id：应用标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param page_size：条数
        :param page_index：页数
        :param asset_object_id：资产对象标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param source_type：来源类型（1-购买2-任务3-手动配置4-抽奖5-回购）
        :param source_object_id：来源对象标识(比如来源类型是任务则对应任务类型)
        :param operate_type：操作类型(0累计 1消耗)
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")
        store_id = self.get_param_int("store_id", 0)
        store_name = self.get_param("store_name")
        source_type = int(self.get_param("source_type", 0))
        source_object_id = self.get_param("source_object_id")
        asset_type = int(self.get_param("asset_type", 0))
        asset_object_id = self.get_param("asset_object_id")
        operate_type = int(self.get_param("operate_type", -1))

        field = "*"
        db_connect_key = "db_cloudapp"
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        else:
            field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
            db_connect_key = invoke_result_data.data["db_connect_key"] if invoke_result_data.data.__contains__("db_connect_key") else "db_cloudapp"
        asset_base_model = AssetBaseModel(context=self)
        page_list, total = asset_base_model.get_store_asset_log_list(app_id, asset_type, db_connect_key, page_size, page_index, store_id, store_name, asset_object_id, start_date, end_date, source_type, source_object_id, field, is_cache=False, operate_type=operate_type)
        ref_params = {}
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params))
        return self.response_json_success(page_info)


class QueueLogListHandler(ClientBaseHandler):
    """
    :description: 排队系统日志列表
    """
    def get_async(self):
        """
        :description: 排队系统日志列表
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        page_size = self.get_param_int("page_size", 20)
        page_index = self.get_param_int("page_index", 0)

        from seven_cloudapp_frame.models.db_models.queueup.queueup_log_model import QueueupLogModel

        condition_where = ConditionWhere()
        condition_where.add_condition("app_id=%s")
        params = [app_id]
        if act_id > 0:
            condition_where.add_condition("act_id=%s")
            params.append(act_id)
        if user_id > 0:
            condition_where.add_condition("user_id=%s")
            params.append(user_id)

        order_by = "id desc"
        field = "*"
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success is False:
            return self.response_json_success({"data": []})

        queueup_log_model = QueueupLogModel(context=self)
        page_list, total = queueup_log_model.get_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), order_by=order_by, params=params)
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params={}))
        return self.response_json_success(page_info)
