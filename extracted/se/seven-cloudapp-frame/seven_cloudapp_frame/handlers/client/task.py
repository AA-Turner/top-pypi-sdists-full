# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-17 11:19:05
@LastEditTime: 2024-11-05 19:26:46
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.task_base_model import *


class TaskInfoListHandler(ClientBaseHandler):
    """
    :description: 获取任务列表
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 获取任务列表
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_code：用户标识
        :param task_types:任务类型 多个逗号,分隔
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        mix_nick = self.get_param("mix_nick")
        module_id = self.get_param_int("module_id")
        task_types = self.get_param("task_types")
        is_log = self.get_param_int("is_log", 0)
        is_log = True if is_log == 1 else False
        task_base_model = TaskBaseModel(context=self)
        app_key, app_secret = self.get_app_key_secret()
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc,id asc"
        daily_repeat_browse = invoke_result_data.data["daily_repeat_browse"] if invoke_result_data.data.__contains__("daily_repeat_browse") else False
        ver_no = invoke_result_data.data["ver_no"] if invoke_result_data.data.__contains__("ver_no") else '1'
        param_dict = invoke_result_data.data["param_dict"] if invoke_result_data.data.__contains__("param_dict") else {}
        browse_site_task_types = invoke_result_data.data["browse_site_task_types"] if invoke_result_data.data.__contains__("browse_site_task_types") else None
        if ver_no == "1":
            result_list,task_info_list,task_count_list = task_base_model.get_client_task_list(app_id, act_id, module_id, user_id, task_types, app_key, app_secret, is_log, daily_repeat_browse, mix_nick, order_by, browse_site_task_types)
        else:
            result_list,task_info_list,task_count_list = task_base_model.get_client_task_list_v2(app_id, act_id, module_id, user_id, task_types, daily_repeat_browse, order_by, param_dict)
        ref_params = {}
        ref_params["task_info_list"] = task_info_list
        ref_params["task_count_list"] = task_count_list
        return self.response_json_success(self.business_process_executed(result_list, ref_params))


class ReceiveRewardHandler(ClientBaseHandler):
    """
    :description: 处理领取任务奖励
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理领取任务奖励
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :param task_id:任务标识
        :param task_sub_type:子任务类型
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        task_id = self.get_param_int("task_id")
        task_type = self.get_param_int("task_type")
        task_sub_type = str(self.get_param("task_sub_type"))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        check_act_info_release = invoke_result_data.data["check_act_info_release"] if invoke_result_data.data.__contains__("check_act_info_release") else True
        check_act_module_release = invoke_result_data.data["check_act_module_release"] if invoke_result_data.data.__contains__("check_act_module_release") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_receive_reward(app_id, act_id, module_id, user_id, login_token, task_id, task_sub_type, self.__class__.__name__, self.request_code, task_type, check_new_user, check_user_nick, 0, is_stat, info_json, check_act_info_release=check_act_info_release, check_act_module_release=check_act_module_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class FreeGiftHandler(ClientBaseHandler):
    """
    :description: 处理掌柜有礼、新人有礼、免费领取等相似任务
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理掌柜有礼、新人有礼、免费领取等相似任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}

        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else True
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_free_gift(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_new_user, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class OneSignHandler(ClientBaseHandler):
    """
    :description: 处理单次签到任务
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理单次签到任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}

        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else {}
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_one_sign(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_new_user, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class WeeklySignHandler(ClientBaseHandler):
    """
    :description: 处理每周签到任务
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理每周签到任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        check_act_info_release = invoke_result_data.data["check_act_info_release"] if invoke_result_data.data.__contains__("check_act_info_release") else True
        check_act_module_release = invoke_result_data.data["check_act_module_release"] if invoke_result_data.data.__contains__("check_act_module_release") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_weekly_sign(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_new_user, check_user_nick, 0, is_stat, info_json, check_act_info_release=check_act_info_release, check_act_module_release=check_act_module_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class CumulativeSignHandler(ClientBaseHandler):
    """
    :description: 处理累计签到任务
    """
    @filter_check_params("login_token",check_user_code=True)
    def get_async(self):
        """
        :description: 处理累计签到任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_type = invoke_result_data.data["task_type"] if invoke_result_data.data.__contains__("task_type") else 0
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_cumulative_sign(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_new_user, check_user_nick, 0, is_stat, info_json, task_type)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class SuccessiveSignHandler(ClientBaseHandler):
    """
    :description: 处理连续签到任务（天数是连续递增）
    """
    @filter_check_params("login_token",check_user_code=True)
    def get_async(self):
        """
        :description: 处理连续签到任务（天数是连续递增）
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_type = TaskType.successive_sign.value
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_cumulative_sign(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_new_user, check_user_nick, 0, is_stat, info_json, task_type)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class InviteNewUserHandler(ClientBaseHandler):
    """
    :description: 处理邀请用户任务(被邀请人进入调用)
    """
    @filter_check_params("invite_user_id,login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理邀请用户任务(被邀请人进入调用)
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param invite_user_id:邀请人用户标识
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = TaskType.invite_new_user.value
        login_token = self.get_param("login_token")
        from_user_id = int(self.get_param("invite_user_id", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else True
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        check_act_info_release = invoke_result_data.data["check_act_info_release"] if invoke_result_data.data.__contains__("check_act_info_release") else True
        check_act_module_release = invoke_result_data.data["check_act_module_release"] if invoke_result_data.data.__contains__("check_act_module_release") else True
        close_invite_limit = invoke_result_data.data["close_invite_limit"] if invoke_result_data.data.__contains__("close_invite_limit") else False #是否关闭邀请限制
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False #是否直接领取奖励
        response_data_type = invoke_result_data.data["response_data_type"] if invoke_result_data.data.__contains__("response_data_type") else 2  #输出值类型（1-对象 2-奖励值）
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)

        stat_base_model = StatBaseModel(context=self)
        if is_stat == True:
            stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, "", {"BeInvitedUserCount": 1, "BeInvitedCount": 1})

        invoke_result_data = task_base_model.process_invite_user(app_id, act_id, module_id, user_id, login_token, from_user_id, self.__class__.__name__, check_user_nick, check_new_user, 0, close_invite_limit, check_act_info_release=check_act_info_release, check_act_module_release=check_act_module_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if is_stat == True:
            stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, "", {"AddBeInvitedUserCount": 1})
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=from_user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if response_data_type == 1:
            return self.response_json_success(invoke_result_data.data)
        else:
            return self.response_json_success(invoke_result_data.data["reward_value"])


class InviteJoinMemberHandler(ClientBaseHandler):
    """
    :description: 处理邀请加入会员任务
    """
    @filter_check_params("invite_user_id,login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理邀请加入会员任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param invite_user_id:邀请人用户标识
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = TaskType.invite_join_member.value
        login_token = self.get_param("login_token")
        from_user_id = self.get_param_int("invite_user_id", 0)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        close_invite_limit = invoke_result_data.data["close_invite_limit"] if invoke_result_data.data.__contains__("close_invite_limit") else False
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False  #是否直接领取奖励
        response_data_type = invoke_result_data.data["response_data_type"] if invoke_result_data.data.__contains__("response_data_type") else 2  #输出值类型（1-对象 2-奖励值）
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)

        invoke_result_data = task_base_model.process_invite_join_member(app_id, act_id, module_id, user_id, login_token, from_user_id, self.__class__.__name__, check_user_nick, 0, close_invite_limit)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=from_user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if response_data_type == 1:
            return self.response_json_success(invoke_result_data.data)
        else:
            return self.response_json_success(invoke_result_data.data["reward_value"])


class CollectGoodsHandler(ClientBaseHandler):
    """
    :description: 处理收藏商品任务
    """
    @filter_check_params("login_token,goods_id", check_user_code=True)
    def get_async(self):
        """
        :description: 处理收藏商品任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param goods_id:商品ID
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = TaskType.collect_goods.value
        goods_id = self.get_param("goods_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_collect_goods(app_id, act_id, module_id, user_id, login_token, goods_id, self.__class__.__name__, check_user_nick, 0)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class BrowseGoodsHandler(ClientBaseHandler):
    """
    :description: 处理浏览商品任务
    """
    @filter_check_params("login_token,goods_id", check_user_code=True)
    def get_async(self):
        """
        :description: 处理浏览商品任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param goods_id:商品ID
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = TaskType.browse_goods.value
        goods_id = self.get_param("goods_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        daily_repeat_browse = invoke_result_data.data["daily_repeat_browse"] if invoke_result_data.data.__contains__("daily_repeat_browse") else False
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False  #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_browse_goods(app_id, act_id, module_id, user_id, login_token, goods_id, self.__class__.__name__, daily_repeat_browse, check_user_nick, 0)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class FavorStoreHandler(ClientBaseHandler):
    """
    :description: 处理关注店铺
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理关注店铺
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_favor_store(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class JoinMemberHandler(ClientBaseHandler):
    """
    :description: 处理加入店铺会员
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理加入店铺会员
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_join_member(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class BrowseSiteHandler(ClientBaseHandler):
    """
    :description: 处理浏览网址相关任务 如：浏览会场/专题
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理浏览商品任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param task_type:活动模块标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param task_sub_type:子任务类型
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = self.get_param_int("task_type", TaskType.browse_special_topic.value)
        task_sub_type = self.get_param("task_sub_type")
        login_token = self.get_param("login_token")
        invoke_result_data = InvokeResultData()
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False  #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        browse_site_task_types = invoke_result_data.data["browse_site_task_types"] if invoke_result_data.data.__contains__("browse_site_task_types") else [TaskType.browse_special_topic.value, TaskType.browse_store.value, TaskType.browse_live_room.value]

        if task_type not in browse_site_task_types:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "非法操作"
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_browse_site(app_id, act_id, module_id, user_id, login_token, task_type, task_sub_type, self.__class__.__name__, check_user_nick, 0)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, login_token='', task_id=0, task_sub_type=task_sub_type, handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class ShareHandler(ClientBaseHandler):
    """
    :description: 分享任务
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 分享任务
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
        module_id = self.get_param_int("module_id")
        task_type = TaskType.share.value
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False  #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_share(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, False, check_user_nick, 0)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class BrowseStoreHandler(ClientBaseHandler):
    """
    :description: 浏览店铺任务
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 浏览店铺任务
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
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        task_type = TaskType.browse_store.value
        task_sub_type = self.get_param("task_sub_type")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False  #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_routine_task(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, task_type, task_sub_type, False, check_user_nick)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, login_token='', task_id=0, task_sub_type=task_sub_type, handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class BrowseLiveRoomHandler(ClientBaseHandler):
    """
    :description: 浏览直播间任务
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 浏览直播间任务
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
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        task_type = TaskType.browse_live_room.value
        task_sub_type = self.get_param("task_sub_type")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False  #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_routine_task(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, task_type, task_sub_type, False, check_user_nick)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, login_token='', task_id=0, task_sub_type=task_sub_type, handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class InviteUserHelpHandler(ClientBaseHandler):
    """
    :description: 处理邀请用户助力任务(被邀请人进入调用)
    """
    @filter_check_params("invite_user_id,login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理邀请用户助力任务(被邀请人进入调用)
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param invite_user_id:邀请人用户标识
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = TaskType.invite_user_help.value
        login_token = self.get_param("login_token")
        from_user_id = int(self.get_param("invite_user_id", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None

        stat_base_model = StatBaseModel(context=self)
        if is_stat == True:
            stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, "", {"BeInvitedHelpUserCount": 1, "BeInvitedHelpCount": 1})
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_invite_user_help(app_id, act_id, module_id, user_id, login_token, from_user_id, self.__class__.__name__, check_new_user, check_user_nick, 0, True, True)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if is_stat == True:
            stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, "", {"AddBeInvitedHelpUserCount": 1})

        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=from_user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class SecretCodeHandler(ClientBaseHandler):
    """
    :description: 神秘暗号任务
    """
    @filter_check_params("login_token,secret_code", check_user_code=True)
    def get_async(self):
        """
        :description: 神秘暗号任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :param secret_code:暗号
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        secret_code = self.get_param("secret_code")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        invoke_result_data = task_base_model.process_secret_code(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, secret_code, check_new_user, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class CrmPointExchangeAssetHandler(ClientBaseHandler):
    """
    :description: 店铺积分兑换资产
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 神秘暗号任务
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
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        mix_nick = self.get_param("mix_nick", "")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        check_user_type = invoke_result_data.data["check_user_type"] if invoke_result_data.data.__contains__("check_user_type") else UserType.act.value
        task_base_model = TaskBaseModel(context=self, check_user_type=check_user_type)
        app_base_model = AppBaseModel(context=self)
        app_info_dict = app_base_model.get_app_info_dict(app_id,field="access_token")
        if not app_info_dict:
            return self.response_json_error("error", "对不起，找不到该应用")
        access_token = app_info_dict["access_token"]
        app_key, app_secret = self.get_app_key_secret()
        invoke_result_data = task_base_model.process_crm_point_exchange_asset(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, mix_nick, access_token, app_key, app_secret, check_new_user, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])
