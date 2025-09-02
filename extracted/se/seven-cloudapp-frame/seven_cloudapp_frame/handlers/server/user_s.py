# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-27 10:52:51
@LastEditTime: 2023-05-05 19:22:10
@LastEditors: HuangJianYi
@Description: 用户模块
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.user_base_model import *
from seven_cloudapp_frame.models.asset_base_model import *
from seven_cloudapp_frame.libs.customize.oss2_helper import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.models.db_models.tao.tao_login_log_model import *
from seven_cloudapp_frame.models.db_models.price.price_gear_model import *


class LoginHandler(ClientBaseHandler):
    """
    :description: 登录处理
    """

    @filter_check_params("open_id")
    def get_async(self):
        """
        :description: 登录日志入库
        :param open_id：用户唯一标识
        :param user_nick：用户昵称
        :return: 
        :last_editors: HuangJianYi
        """
        open_id = self.get_open_id()
        user_nick = self.get_user_nick()

        request_params = str(self.request_params)

        if user_nick == "":
            return self.response_json_success()

        tao_login_log_model = TaoLoginLogModel(context=self)
        tao_login_log = tao_login_log_model.get_entity("open_id=%s", params=open_id)

        is_add = False
        if not tao_login_log:
            is_add = True
            tao_login_log = TaoLoginLog()

        tao_login_log.open_id = open_id
        tao_login_log.user_nick = user_nick
        if user_nick.__contains__(":"):
            tao_login_log.store_user_nick = user_nick.split(":")[0]
            tao_login_log.is_master = 0
        else:
            tao_login_log.store_user_nick = user_nick
            tao_login_log.is_master = 1
        tao_login_log.request_params = request_params
        tao_login_log.modify_date = self.get_now_datetime()

        try:
            if is_add:
                tao_login_log.create_date = tao_login_log.modify_date
                tao_login_log.id = tao_login_log_model.add_entity(tao_login_log)
            else:
                tao_login_log_model.update_entity(tao_login_log)

            #更新登录时间到app_info
            app_id = self.get_app_id()
            if app_id:
                AppInfoModel(context=self).update_table("modify_date=%s", "app_id=%s", [tao_login_log.modify_date, app_id])
        except:
            pass

        return self.response_json_success()


class UpdateUserStatusHandler(ClientBaseHandler):
    """
    :description: 更新用户状态
    """

    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 更新用户状态
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_code：用户标识
        :param user_state：用户状态（0正常1黑名单）
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        user_state = self.get_param_int("user_state")
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.update_user_state(app_id, act_id, user_id, user_state)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        title = "更新用户状态；"
        if user_state == 0:
            title = "解锁用户；"
        else:
            title = "拉黑用户；"
        title = title + "用户昵称：" + invoke_result_data.data["user_nick"] + "，openid：" + invoke_result_data.data["open_id"]
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="user_info_tb", title=title)
        return self.response_json_success()


class UpdateUserStatusByBlackHandler(ClientBaseHandler):
    """
    :description: 用户拉入黑名单(黑名单管理模式)
    """

    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 用户拉入黑名单
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_code：用户标识
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.update_user_state_by_black(app_id, act_id, user_id)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        title = "拉黑用户；用户昵称：" + invoke_result_data.data["user_nick"] + "，openid：" + invoke_result_data.data["open_id"]
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="user_info_tb", title=title)
        ref_params = {}
        self.business_process_executed(invoke_result_data, ref_params)
        return self.response_json_success()


class AuditUserBlackHandler(ClientBaseHandler):
    """
    :description 审核黑名单状态
    """

    @filter_check_params("black_id,audit_status")
    def get_async(self):
        """
        :description: 审核黑名单状态
        :param black_id：用户黑名单管理标识
        :param audit_status：审核状态(0黑名单1申请中2同意3拒绝)
        :param audit_remark：审核备注
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        black_id = int(self.get_param("black_id", 0))
        audit_status = int(self.get_param("audit_status", 0))
        audit_remark = self.get_param("audit_remark")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.audit_user_black(app_id, black_id, audit_status, audit_remark)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        title = "操作审核黑名单；"
        if audit_status == 2:
            title = "同意解锁用户；"
        elif audit_status == 3:
            title = "拒绝解锁用户；"
        title = title + "用户昵称：" + invoke_result_data.data["user_info"]["user_nick"] + "，openid：" + invoke_result_data.data["user_info"]["open_id"]
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="user_black_tb", title=title)
        ref_params = {}
        self.business_process_executed(invoke_result_data, ref_params)
        return self.response_json_success()


class UpdateAuditRemarkHandler(ClientBaseHandler):
    """
    :description 修改审核备注
    """

    @filter_check_params("black_id,audit_status")
    def get_async(self):
        """
        :description: 修改审核备注
        :param black_id：用户黑名单管理标识
        :param audit_remark：审核备注
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        black_id = int(self.get_param("black_id", 0))
        audit_remark = self.get_param("audit_remark")
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.update_audit_remark(app_id, black_id, audit_remark)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        title = "修改黑名单审核备注；用户昵称：" + invoke_result_data.data["user_black"]["user_nick"] + "，openid：" + invoke_result_data.data["user_black"]["open_id"]
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="user_black_tb", title=title)
        return self.response_json_success()


class UserBlackListHandler(ClientBaseHandler):
    """
    :description: 获取黑名单管理列表
    """

    def get_async(self):
        """
        :description: 获取黑名单管理列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param audit_status：审核状态(0黑名单1申请中2同意3拒绝)
        :param user_code：用户标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param nick_name：用户昵称
        :param user_open_id：open_id
        :param page_size：条数
        :param page_index：页数
        :return: list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        audit_status = int(self.get_param("audit_status", -1))
        user_id = self.get_user_id()
        user_nick = self.get_param("nick_name")
        open_id = self.get_param("user_open_id")
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")
        page_size = int(self.get_param("page_size", 20))
        page_index = int(self.get_param("page_index", 0))

        user_base_model = UserBaseModel(context=self)
        return self.response_json_success(user_base_model.get_black_list(app_id, act_id, page_size, page_index, audit_status, user_id, start_date, end_date, user_nick, open_id))


class UpdateUserAssetHandler(ClientBaseHandler):
    """
    :description: 变更资产
    """
    @filter_check_params("asset_type,asset_value", check_user_code=True)
    def post_async(self):
        """
        :description: 变更资产
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：模块标识
        :param user_code：用户标识
        :param asset_type：资产类型
        :param asset_value：变更的资产值
        :param asset_object_id：资产对象标识
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id", 0)
        asset_type = self.get_param_int("asset_type", 0)
        asset_value = self.get_param_int("asset_value", 0)
        asset_object_id = self.get_param("asset_object_id")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        user_base_model = UserBaseModel(context=self)
        user_info_dict = user_base_model.get_user_info_dict(app_id, act_id, user_id)
        if not user_info_dict:
            return self.response_json_error("error", "用户信息不存在")

        asset_base_model = AssetBaseModel(context=self)
        invoke_result_data = asset_base_model.update_user_asset(app_id=app_id,
                                                                act_id=act_id,
                                                                module_id=module_id,
                                                                user_id=user_id,
                                                                open_id=user_info_dict["open_id"],
                                                                user_nick=user_info_dict["user_nick"],
                                                                asset_type=asset_type,
                                                                asset_value=asset_value,
                                                                asset_object_id=asset_object_id,
                                                                source_type=3,
                                                                source_object_id="",
                                                                source_object_name="手动配置",
                                                                log_title="手动配置",
                                                                only_id="",
                                                                handler_name=self.__class__.__name__,
                                                                request_code=self.request_code,
                                                                info_json={"operate_user_id":self.get_open_id(),"operate_user_name":self.get_user_nick()
                                                                           })
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        default_prefix = "资产配置"
        operation_desc = ""
        if asset_type == 1:
            default_prefix = "次数配置"
        elif asset_type == 2:
            default_prefix = "积分配置"
        elif asset_type == 3:
            default_prefix = "价格档位配置"
            price_gear_model = PriceGearModel(context=self, is_auto=True)
            asset_object_id = int(asset_object_id)
            if asset_object_id > 0:
                price_gear = price_gear_model.get_entity_by_id(asset_object_id)
                if price_gear:
                    operation_desc = "价格档位:" + price_gear.price_gear_name + "，次数：" + str(asset_value)
        title_prefix = invoke_result_data.data["title_prefix"] if invoke_result_data.data.__contains__("title_prefix") else default_prefix
        title = title_prefix + ";" + "用户昵称：" + user_info_dict["user_nick"] + "，openid：" + user_info_dict["open_id"]
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="user_asset_tb", title=title, operation_desc=operation_desc)
        ref_params = {}
        self.business_process_executed(invoke_result_data, ref_params)
        return self.response_json_success()


class BatchUpdateUserAssetHandler(ClientBaseHandler):
    """
    :description: 批量变更资产
    """
    @filter_check_params("asset_object_json", check_user_code=True)
    def post_async(self):
        """
        :description: 批量变更资产
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：模块标识
        :param user_code：用户标识
        :param asset_object_json：变更的资产值列表
        :return: response_json_success
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id", 0)
        #{"asset_type":0,"asset_object_id":"","asset_value":0}
        asset_object_json = self.get_param("asset_object_json")

        user_base_model = UserBaseModel(context=self)
        user_info_dict = user_base_model.get_user_info_dict(app_id, act_id, user_id)
        if not user_info_dict:
            return self.response_json_error("error", "用户信息不存在")

        asset_base_model = AssetBaseModel(context=self)
        asset_object_json = SevenHelper.json_loads(asset_object_json)
        asset_object_ids = ""
        for asset_object in asset_object_json:
            invoke_result_data = asset_base_model.update_user_asset(app_id=app_id,
                                                                    act_id=act_id,
                                                                    module_id=module_id,
                                                                    user_id=user_id,
                                                                    open_id=user_info_dict["open_id"],
                                                                    user_nick=user_info_dict["user_nick"],
                                                                    asset_type=int(asset_object["asset_type"]),
                                                                    asset_value=int(asset_object["asset_value"]),
                                                                    asset_object_id=asset_object["asset_object_id"],
                                                                    source_type=3,
                                                                    source_object_id="",
                                                                    source_object_name="手动配置",
                                                                    log_title="手动配置",
                                                                    only_id="",
                                                                    handler_name=self.__class__.__name__,
                                                                    request_code=self.request_code,
                                                                    info_json={
                                                                        "operate_user_id": self.get_open_id(),
                                                                        "operate_user_name": self.get_user_nick()
                                                                    })
            if invoke_result_data.success == False:
                return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message, asset_object_ids)
            else:
                if asset_object_ids:
                    asset_object_ids += ","
                asset_object_ids += asset_object["asset_object_id"]
        title = "批量变更资产配置；用户昵称：" + user_info_dict["user_nick"] + "，openid：" + user_info_dict["open_id"]
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="user_asset_tb", title=title)
        return self.response_json_success()


class UserAssetListHandler(ClientBaseHandler):
    """
    :description: 获取用户资产列表
    """

    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 获取用户资产列表
        :param act_id：活动标识
        :param user_code：用户标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        asset_type = int(self.get_param("asset_type", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        asset_base_model = AssetBaseModel(context=self)
        ref_params = {}
        return self.response_json_success(self.business_process_executed(asset_base_model.get_user_asset_list(app_id, act_id, user_id, asset_type), ref_params))


class AssetLogListHandler(ClientBaseHandler):
    """
    :description: 资产流水记录
    """

    def get_async(self):
        """
        :description: 资产流水记录
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：模块标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param page_size：条数
        :param page_index：页数
        :param user_id：用户标识
        :param asset_object_id：资产对象标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param user_nick：昵称
        :param open_id：open_id
        :param source_type：来源类型（1-购买2-任务3-手动配置4-抽奖5-回购）
        :param source_object_id：来源对象标识(比如来源类型是任务则对应任务类型)
        :param operate_type：操作类型(0累计 1消耗)
        :return list
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = self.get_param_int("module_id", 0)
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 20)
        user_id = self.get_user_id()
        user_open_id = self.get_param("user_open_id")
        user_nick = self.get_param("nick_name")
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")
        source_type = self.get_param_int("source_type", 0)
        source_object_id = self.get_param("source_object_id")
        asset_type = self.get_param_int("asset_type", 0)
        asset_object_id = self.get_param("asset_object_id")
        operate_type = self.get_param_int("operate_type", -1)

        field = "*"
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        else:
            field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        asset_base_model = AssetBaseModel(context=self)
        page_list, total = asset_base_model.get_asset_log_list(app_id, act_id, asset_type, page_size, page_index, user_id, asset_object_id, start_date, end_date, user_nick, user_open_id, source_type, source_object_id, field, is_cache=False, operate_type=operate_type, module_id=module_id)
        ref_params = {}
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params))
        return self.response_json_success(page_info)


class UserInfoListHandler(ClientBaseHandler):
    """
    :description: 用户信息列表
    """

    def get_async(self):
        """
        :description: 用户信息列表
        :param act_id：活动标识
        :param user_id：用户标识
        :param user_open_id：_open_id
        :param nick_name：用户昵称
        :param user_state：_用户状态0正常1黑名单
        :param page_index：页索引
        :param page_size：页大小
        :param start_date：创建时间开始
        :param end_date：创建时间结束
        :return PageInfo
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        open_id = self.get_param("user_open_id")
        user_nick = self.get_param("nick_name")
        user_state = int(self.get_param("user_state", -1))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")
        user_base_model = UserBaseModel(context=self)
        page_info = user_base_model.get_user_list(app_id, act_id, page_size, page_index, user_state, user_id, start_date, end_date, user_nick, open_id)
        ref_params = {}
        return self.response_json_success(self.business_process_executed(page_info, ref_params))