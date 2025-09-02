# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-10 10:41:13
@LastEditTime: 2025-06-12 19:12:12
@LastEditors: HuangJianYi
@Description: 
"""
from asq.initiators import query
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.top_base_model import *
from seven_cloudapp_frame.models.frame_base_model import FrameBaseModel
from seven_cloudapp_frame.models.asset_base_model import *
from seven_cloudapp_frame.models.stat_base_model import *
from seven_cloudapp_frame.models.user_base_model import *
from seven_cloudapp_frame.models.app_base_model import *
from seven_cloudapp_frame.models.order_base_model import *
from seven_cloudapp_frame.models.db_models.user.user_info_model import *
from seven_cloudapp_frame.models.db_models.task.task_info_model import *
from seven_cloudapp_frame.models.db_models.task.task_count_model import *
from seven_cloudapp_frame.models.db_models.invite.invite_log_model import *
from seven_cloudapp_frame.models.db_models.invite.invite_help_model import *
from seven_cloudapp_frame.models.db_models.collect.collect_log_model import *
from seven_cloudapp_frame.models.db_models.browse.browse_log_model import *
from seven_cloudapp_frame.models.db_models.task.task_gear_count_model import *
from seven_cloudapp_frame.models.db_models.task.task_log_model import *



class TaskBaseModel(FrameBaseModel):
    """
    :description: 任务业务模型
    """
    def __init__(self, context=None, logging_error=None, logging_info=None, check_user_type=UserType.act.value):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info
        self.db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_task","redis_task")
        super(TaskBaseModel, self).__init__(context, check_user_type)

    def _delete_task_info_dependency_key(self, act_id, task_id=0, delay_delete_time=0.01):
        """
        :description: 删除任务依赖建
        :param act_id: 活动标识
        :param task_id: 任务标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: HuangJianYi
        """
        dependency_key_list = []
        if task_id:
            dependency_key_list.append(DependencyKey.task_info(task_id))
        if act_id:
            dependency_key_list.append(DependencyKey.task_info_list(act_id))
        TaskInfoModel().delete_dependency_key(dependency_key_list, delay_delete_time)

    def _get_task_count_id_md5(self, act_id, module_id, task_type, task_sub_type, user_id):
        """
        :description: 获取任务计数标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param task_type:任务类型
        :param task_sub_type:任务子类型
        :param user_id:用户标识
        :return 获取任务计数标识
        :last_editors: HuangJianYi
        """
        if not act_id or not task_type or not user_id:
            return 0
        return CryptoHelper.md5_encrypt_int(f"{act_id}_{module_id}_{task_type}_{task_sub_type}_{user_id}")

    def __covert_task_config_json(self, config_json, task_sub_type):
        """
        :description: 任务配置转换
        :param config_json:任务配置
        :param task_sub_type:任务子类型
        :return 任务配置
        :last_editors: HuangJianYi
        """
        if task_sub_type:
            sub_config_json = []
            if isinstance(config_json, list): # 每个子任务使用单独的计数
                sub_config_json = [sub_config_json for sub_config_json in config_json if str(sub_config_json["id"]) == task_sub_type]
            elif config_json.__contains__("gear_list") == True: # 每个子任务使用总的累加计数
                sub_config_json = [sub_config_json for sub_config_json in config_json["gear_list"] if str(sub_config_json["id"]) == task_sub_type]
            config_json = sub_config_json[0] if len(sub_config_json) > 0 else {}
        return config_json

    def get_task_info_dict_list(self, app_id, act_id, module_id, is_release, is_cache=True, source_object_id='', is_del=-1, order_by="sort_index desc,id asc"):
        """
        :description: 获取任务列表
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param module_id: 活动模块标识
        :param is_release: 是否发布
        :param is_cache: 是否缓存
        :param source_object_id: 来源对象标识
        :param is_del: 是否删除（1-是 0-否）
        :param order_by: 排序
        :return: 
        :last_editors: HuangJianYi
        """
        params = [act_id]
        condition_where = ConditionWhere()
        condition_where.add_condition("act_id=%s")
        if is_release !=-1:
            condition_where.add_condition("is_release=%s")
            params.append(is_release)
        if module_id !=-1:
            condition_where.add_condition("module_id=%s")
            params.append(module_id)
        if app_id:
            condition_where.add_condition("app_id=%s")
            params.append(app_id)
        if source_object_id:
            condition_where.add_condition("source_object_id=%s")
            params.append(source_object_id)
        if is_del !=-1:
            condition_where.add_condition("is_del=%s")
            params.append(is_del)

        if is_cache:
            dict_list = TaskInfoModel(context=self.context, is_auto=True).get_cache_dict_list(condition_where.to_string(), group_by="", order_by=order_by, params=params, dependency_key=DependencyKey.task_info_list(act_id), cache_expire=300)
        else:
            dict_list = TaskInfoModel(context=self.context).get_dict_list(condition_where.to_string(), group_by="", order_by=order_by, params=params)
        for task_info in dict_list:
            task_info["config_json"] = SevenHelper.json_loads(task_info["config_json"]) if task_info["config_json"] else {}
        return dict_list

    def get_task_info_dict(self, task_id, is_cache=True, is_filter=True):
        """
        :description: 获取任务信息
        :param task_id: 任务标识
        :param is_cache: 是否缓存
        :param is_filter: 是否过滤未发布的数据
        :return: 
        :last_editors: HuangJianYi
        """
        task_info_dict = None
        if is_cache:
            task_info_dict = TaskInfoModel(context=self.context, is_auto=True).get_cache_dict_by_id(task_id,dependency_key=DependencyKey.task_info(task_id))
        else:
            task_info_dict = TaskInfoModel(context=self.context).get_dict_by_id(task_id)
        if is_filter == True:
            if not task_info_dict or task_info_dict["is_release"] == 0 or task_info_dict["is_del"] == 1:
                return None
        return task_info_dict

    def get_task_asset_type(self, task_asset_type_json, task_type):
        """
        :description: 获取任务奖励资产类型 (先取配置文件的值没有用默认值，如果数据库有配置则使用数据库的值)
        :param task_asset_type:任务资产类型配置  key:1次数2积分3价格档位4店铺会员积分9999其他（混合搭配）
        :param task_type:任务类型
        :return 任务奖励资产类型
        :last_editors: HuangJianYi
        """
        asset_type = int(share_config.get_value("task_asset_type",2))
        if task_asset_type_json == "":
            return asset_type
        task_asset_type_dict = SevenHelper.json_loads(task_asset_type_json)
        if not task_asset_type_dict:
            return asset_type
        if int(task_asset_type_dict["key"]) != 9999:
            asset_type = int(task_asset_type_dict["key"])
            return asset_type
        value_dict = task_asset_type_dict["value"]
        if not value_dict:
            return asset_type
        if str(task_type) in value_dict.keys():
            asset_type = value_dict[str(task_type)]
        return asset_type

    def get_business_map_frame_task_type(self,task_type):
        """
        :description: 映射任务类型，如果配置文件有配置相应的任务类型key，则会替换key对应枚举中的值，使用场景：用于在把业务写的方法整合到框架的时候，任务类型不一致的情况，业务可以使用原本定义的任务类型调用框架里的方法
        :param task_type:任务类型值
        :return 最终的任务类型值
        :last_editors: HuangJianYi
        """
        key = ""
        try:
            key = TaskType(task_type).name
        except ValueError:
            pass
        task_type_dict = share_config.get_value("business_map_frame_task_type",{})
        if key and str(key) in task_type_dict.keys():
            task_type = int(task_type_dict[str(key)])
        return task_type

    def check_task_info(self,act_id,module_id,task_type=0,task_id=0):
        """
        :description: 校验任务信息
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param task_type:任务类型
        :param task_id:任务标识
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            task_info_model = TaskInfoModel(context=self.context, is_auto=True)
            if task_id > 0:
                task_info_dict = self.get_task_info_dict(task_id)
            else:
                task_info_dict = task_info_model.get_cache_dict("act_id=%s and task_type=%s and module_id=%s and is_del=0",limit="1",params=[act_id,task_type,module_id],dependency_key=f"task_info_list:actid_{act_id}")
            if not task_info_dict or task_info_dict["is_release"] == 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "任务信息不存在"
                return invoke_result_data
            config_json = SevenHelper.json_loads(task_info_dict["config_json"])
            if not config_json:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "任务信息配置不存在"
                return invoke_result_data
            task_info_dict["config_json"] = config_json
            invoke_result_data.data = task_info_dict
        except Exception as ex:
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "任务信息不存在"
            return invoke_result_data
        return invoke_result_data

    def get_only_id(self,user_id,complete_type,task_type,task_sub_type="",complete_count=1):
        """
        :description: 获取only_id
        :param user_id:用户标识
        :param complete_type:完成类型(1每日任务2每周任务3持久任务)
        :param task_type:任务类型
        :param task_sub_type:任务子类型
        :param complete_count:完成次数
        :return only_id
        :last_editors: HuangJianYi
        """
        only_id = f"task_{user_id}_{task_type}_{task_sub_type}"
        if complete_type == 1:
            only_id += f"_{TimeExHelper.get_now_day_int()}"
        elif complete_type == 2:
            only_id += f"_{str(datetime.datetime.now().year)+str(datetime.datetime.now().isocalendar()[1])}"
        else:
            only_id += f"_0"
        only_id += f"_{complete_count}"
        return only_id

    def add_task_stat(self, task_type, app_id, act_id, module_id, user_id, open_id, reward_value, is_stat=True, complete_count=1):
        """
        :description: 添加任务统计
        :param task_type:任务类型
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:模块标识
        :param user_id:用户标识
        :param open_id:open_id
        :param open_id:open_id
        :param reward_value:奖励值
        :param is_stat:是否统计
        :param complete_count:完成次数
        :last_editors: HuangJianYi
        """
        if is_stat == True:
            stat_base_model = StatBaseModel(context=self.context)
            key_list_dict = {}
            if task_type == int(TaskType.collect_goods.value):
                key_list_dict["CollectUserCount"] = 1 #完成人数
                key_list_dict["CollectCount"] = complete_count #完成次数
                key_list_dict["CollectRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.browse_goods.value):
                key_list_dict["BrowseUserCount"] = 1 #完成人数
                key_list_dict["BrowseCount"] = complete_count #完成次数
                key_list_dict["BrowseRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.invite_new_user.value):
                key_list_dict["InviteUserCount"] = 1 #完成人数
                key_list_dict["InviteCount"] = complete_count #完成次数
                key_list_dict["InviteRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.invite_join_member.value):
                key_list_dict["InviteJoinMemberUserCount"] = 1 #完成人数
                key_list_dict["InviteJoinMemberCount"] = complete_count #完成次数
                key_list_dict["InviteJoinMemberRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.invite_user_help.value):
                key_list_dict["InviteHelpUserCount"] = 1 #完成人数
                key_list_dict["InviteHelpCount"] = complete_count #完成次数
                key_list_dict["InviteHelpRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.browse_store.value):
                key_list_dict["BrowseStoreUserCount"] = 1 #完成人数
                key_list_dict["BrowseStoreCount"] = complete_count #完成次数
                key_list_dict["BrowseStoreRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.browse_live_room.value):
                key_list_dict["BrowseLiveRoomUserCount"] = 1 #完成人数
                key_list_dict["BrowseLiveRoomCount"] = complete_count #完成次数
                key_list_dict["BrowseLiveRoomRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.browse_special_topic.value):
                key_list_dict["BrowseSpecialTopicUserCount"] = 1 #完成人数
                key_list_dict["BrowseSpecialTopicCount"] = complete_count #完成次数
                key_list_dict["BrowseSpecialTopicRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.share.value):
                key_list_dict["TaskShareUserCount"] = 1 #完成人数
                key_list_dict["TaskShareCount"] = complete_count #完成次数
                key_list_dict["TaskShareRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.free_gift.value):
                key_list_dict["FreeGiftUserCount"] = 1 #完成人数
                key_list_dict["FreeGiftCount"] = complete_count #完成次数
                key_list_dict["FreeGiftRewardCount"] = reward_value #完成奖励值
            elif task_type == int(TaskType.one_sign.value):
                key_list_dict["OneSignUserCount"] = 1 #完成人数
                key_list_dict["OneSignCount"] = complete_count #完成次数
                key_list_dict["OneSignRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.weekly_sign.value):
                key_list_dict["WeeklySignUserCount"] = 1 #完成人数
                key_list_dict["WeeklySignCount"] = complete_count #完成次数
                key_list_dict["WeeklySignRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.cumulative_sign.value):
                key_list_dict["CumulativeSignUserCount"] = 1 #完成人数
                key_list_dict["CumulativeSignCount"] = complete_count #完成次数
                key_list_dict["CumulativeSignRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.successive_sign.value):
                key_list_dict["SuccessiveSignUserCount"] = 1 #完成人数
                key_list_dict["SuccessiveSignCount"] = complete_count #完成次数
                key_list_dict["SuccessiveSignRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.favor_store.value):
                key_list_dict["FollowUserCount"] = 1 #完成人数
                key_list_dict["FollowCount"] = complete_count #完成次数
                key_list_dict["FollowRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.join_member.value):
                key_list_dict["MemberUserCount"] = 1 #加入会员完成人数
                key_list_dict["MemberCount"] = complete_count #加入会员完成次数
                key_list_dict["MemberRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.secret_code.value):
                key_list_dict["SecretCodeUserCount"] = 1 #完成人数
                key_list_dict["SecretCodeCount"] = complete_count #完成次数
                key_list_dict["SecretCodeRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.crm_point_exchange_asset.value):
                key_list_dict["CrmPointExchangeAssetUserCount"] = 1 #完成人数
                key_list_dict["CrmPointExchangeAssetCount"] = complete_count #完成次数
                key_list_dict["CrmPointExchangeAssetRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.buy_appoint_goods.value):
                key_list_dict["BuyAppointGoodsUserCount"] = 1   #完成人数
                key_list_dict["BuyAppointGoodsCount"] = complete_count #完成次数
                key_list_dict["BuyAppointGoodsRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.buy_appoint_goods_price.value):
                key_list_dict["BuyAppointGoodsPriceUserCount"] = 1   #完成人数
                key_list_dict["BuyAppointGoodsPriceCount"] = complete_count #完成次数
                key_list_dict["BuyAppointGoodsPriceRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.buy_appoint_goods_price_gear.value):
                key_list_dict["BuyAppointGoodsPriceGearUserCount"] = 1   #完成人数
                key_list_dict["BuyAppointGoodsPriceGearCount"] = complete_count #完成次数
                key_list_dict["BuyAppointGoodsPriceGearRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.buy_store_price.value):
                key_list_dict["BuyStorePriceUserCount"] = 1   #完成人数
                key_list_dict["BuyStorePriceCount"] = complete_count  #完成次数
                key_list_dict["BuyStorePriceRewardCount"] = reward_value  #奖励值
            elif task_type == int(TaskType.buy_store_price_gear.value):
                key_list_dict["BuyStorePriceGearUserCount"] = 1   #完成人数
                key_list_dict["BuyStorePriceGearCount"] = complete_count #完成次数
                key_list_dict["BuyStorePriceGearRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.lottery.value):
                key_list_dict["LotteryTaskUserCount"] = 1   #完成人数
                key_list_dict["LotteryTaskCount"] = complete_count #完成次数
                key_list_dict["LotteryTaskRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.lottery_try.value):
                key_list_dict["TryLotteryTaskUserCount"] = 1   #完成人数
                key_list_dict["TryLotteryTaskCount"] = complete_count  #完成次数
                key_list_dict["TryLotteryTaskRewardCount"] = reward_value #奖励值
            elif task_type == int(TaskType.lottery_gear.value):
                key_list_dict["LotteryGearTaskUserCount"] = 1   #完成人数
                key_list_dict["LotteryGearTaskCount"] = complete_count #完成次数
                key_list_dict["LotteryGearTaskRewardCount"] = reward_value  #奖励值

            key_list_dict["JoinTaskUserCount"] = 1  #参与任务完成人数
            key_list_dict["AddJoinTaskUserCount"] = 1  #新增参与任务完成人数
            key_list_dict["JoinTaskCount"] = 1  #参与任务完成次数
            key_list_dict["JoinTaskRewardCount"] = reward_value  #参与任务奖励值

            stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, open_id, key_list_dict)

    def init_task_count(self, task_info_dict, task_count_list, task_sub_type=""):
        """
        :description: 初始化任务计数
        :param task_info_dict:任务信息字典
        :param task_count_list:任务计数列表
        :param task_sub_type:子任务类型标识
        :return 
        :last_editors: HuangJianYi
        """
        if task_sub_type:
            task_count = [task_count for task_count in task_count_list if task_info_dict["task_type"] == task_count.task_type and task_count.task_sub_type == str(task_sub_type)]
        else:
            task_count = [task_count for task_count in task_count_list if task_info_dict["task_type"] == task_count.task_type]
        if not task_count:
            task_count = TaskCount()
        else:
            task_count = task_count[0]
        if task_info_dict["complete_type"] == TaskCompleteType.day.value and task_count.modify_day != SevenHelper.get_now_day_int():
            task_count.complete_count = 0
            task_count.now_count = 0
            task_count.remark = ""
        elif task_info_dict["complete_type"] == TaskCompleteType.week.value and not TimeHelper.is_this_week(task_count.modify_date):
            task_count.complete_count = 0
            task_count.now_count = 0
            task_count.remark = ""
        elif task_info_dict["complete_type"] == TaskCompleteType.month.value and not TimeHelper.is_this_month(task_count.modify_date):
            task_count.complete_count = 0
            task_count.now_count = 0
            task_count.remark = ""
        elif task_info_dict["complete_type"] == TaskCompleteType.long.value and task_count.id == 0:
            task_count.complete_count = 0
            task_count.now_count = 0
        return task_count

    def get_complete_type_name(self, complete_type):
        """
        :description: 获取任务类型名称
        :param complete_type:任务类型
        :param now_day:当前时间天
        :return 
        :last_editors: HuangJianYi
        """
        complete_type_name = ""
        if complete_type == TaskCompleteType.day.value:
            complete_type_name = "每日"
        elif complete_type == TaskCompleteType.week.value:
            complete_type_name = "每周"
        elif complete_type == TaskCompleteType.month.value:
            complete_type_name = "每月"
        return complete_type_name

    def add_task_log(self, task_type, task_sub_type, app_id, act_id, module_id, user_id, open_id, user_nick, task_name, log_title, reward_type, reward_object_id, reward_name, reward_num, handler_name, request_code, info_json={}):
        """
        :description: 添加任务日志
        :param task_type:任务类型
        :param task_sub_type:任务子类型
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param open_id:open_id
        :param user_nick:user_nick
        :param task_name:任务名称
        :param log_title:标题
        :param reward_type: 奖励类型
        :param reward_object_id: 奖励对象标识
        :param reward_name: 奖励名称
        :param reward_num: 奖励数量
        :param handler_name:接口名称
        :param request_code:请求代码
        :param info_json:日志详细信息
        :return 
        :last_editors: HuangJianYi
        """
        task_config = share_config.get_value("task_config",{})
        if task_config.get("is_task_log",False) == True:
            try:
                task_log = TaskLog()
                task_log.app_id = app_id
                task_log.act_id = act_id
                task_log.module_id = module_id
                task_log.user_id = user_id
                task_log.open_id = open_id
                task_log.user_nick = user_nick
                task_log.log_title = log_title
                task_log.task_type = task_type
                task_log.task_sub_type =task_sub_type
                task_log.task_name = task_name if task_name else ""
                task_log.reward_type = reward_type if reward_type else 0
                task_log.reward_object_id = str(reward_object_id) if reward_object_id else ""
                task_log.reward_name = reward_name if reward_name else ""
                task_log.reward_num = reward_num if reward_num else 0
                task_log.handler_name = handler_name
                task_log.request_code = request_code
                task_log.info_json = SevenHelper.json_dumps(info_json) if info_json else {}
                task_log.create_date = SevenHelper.get_now_datetime()
                task_log.create_day = SevenHelper.get_now_day_int()
                task_log_model = TaskLogModel(context=self.context).set_sub_table(app_id)
                task_log_model.add_entity(task_log)
            except Exception as ex:
                self.context.logging_link_error("【添加任务日志】" + traceback.format_exc())

    def add_gear_task_count(self, app_id, act_id, module_id, user_id, open_id, task_type, value, remark='', is_async=True):
        """
        :description: 添加档位任务累计值，目前支持消费类任务、累计抽盒/抽奖次数档位任务
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识(比传)
        :param open_id：open_id
        :param task_type：任务类型
        :param value：计数值
        :param remark：备注
        :param is_async：是否异步处理（1-是 0-否）
        :return:
        :last_editors: HuangJianYi
        """
        if is_async == True:
            task_gear_count = TaskGearCount()
            task_gear_count.app_id = app_id
            task_gear_count.act_id = act_id
            task_gear_count.module_id = module_id
            task_gear_count.user_id = user_id
            task_gear_count.open_id = open_id
            task_gear_count.task_type = task_type
            task_gear_count.now_count = value
            task_gear_count.create_day = SevenHelper.get_now_day_int()
            task_gear_count.create_month = SevenHelper.get_now_month_int()
            task_gear_count.create_date = SevenHelper.get_now_datetime()
            task_gear_count.remark = remark
            redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
            redis_init.rpush(f"task_gear_list:{str(user_id % 10)}", SevenHelper.json_dumps(task_gear_count))
        else:
            self.add_gear_task_count_to_db(app_id, act_id, module_id, user_id, open_id, task_type, value, remark)

    def add_gear_task_count_to_db(self, app_id, act_id, module_id, user_id, open_id, task_type, value, remark=''):
        """
        :description: 添加档位任务累计值，目前支持消费类任务、累计抽盒/抽奖次数档位任务
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识(比传)
        :param open_id：open_id
        :param task_type：任务类型
        :param value：计数值
        :param remark：备注
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            create_day = SevenHelper.get_now_day_int()
            create_month = SevenHelper.get_now_month_int()
            task_info_model = TaskInfoModel(context=self.context)
            db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key), context=self.context)
            task_count_model = TaskCountModel(db_transaction=db_transaction).set_sub_table(app_id)
            task_gear_count_model = TaskGearCountModel(db_transaction=db_transaction).set_sub_table(app_id)
            task_info_dict = task_info_model.get_dict("act_id=%s and module_id=%s and task_type=%s", params=[act_id, module_id, task_type])
            task_gear_count_id_md5 = CryptoHelper.md5_encrypt_int(f"{act_id}_{module_id}_{task_type}_{user_id}")
            task_count_acquire_lock_name = f"task_gear_count_idmd5:{task_gear_count_id_md5}"
            acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
            if acquire_lock_status == False:
                invoke_result_data.success = False
                invoke_result_data.error_code = "acquire_lock"
                invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                return invoke_result_data
            task_gear_count = task_gear_count_model.get_entity("id_md5=%s and create_day=%s", params=[task_gear_count_id_md5, create_day])
            db_transaction.begin_transaction()
            if not task_gear_count:
                task_gear_count = TaskGearCount()
                task_gear_count.id_md5 = task_gear_count_id_md5
                task_gear_count.app_id = app_id
                task_gear_count.act_id = act_id
                task_gear_count.module_id = module_id
                task_gear_count.user_id = user_id
                task_gear_count.open_id = open_id
                task_gear_count.task_type = task_type
                task_gear_count.now_count = value
                task_gear_count.create_day = create_day
                task_gear_count.create_month = create_month
                task_gear_count.create_date = SevenHelper.get_now_datetime()
                task_gear_count.remark = remark
                task_gear_count_model.add_entity(task_gear_count)
            else:
                task_gear_count.now_count = decimal.Decimal(task_gear_count.now_count) + decimal.Decimal(value)
                task_gear_count.remark = task_gear_count.remark + "," + remark if  task_gear_count.remark else remark
                task_gear_count_model.update_table("now_count=%s,remark=%s,modify_date=%s", "id=%s", params=[task_gear_count.now_count, task_gear_count.remark, task_gear_count.create_date, task_gear_count.id])
            if task_info_dict:
                #判断子任务是否完成
                config_json = SevenHelper.json_loads(task_info_dict["config_json"])
                if config_json and config_json.__contains__("gear_list"):
                    now_count = decimal.Decimal(self.get_gear_task_count(app_id, act_id, module_id, user_id, task_type, task_info_dict["complete_type"])) + decimal.Decimal(value)
                    task_count_list = task_count_model.get_list("act_id=%s and module_id=%s and user_id=%s and task_type=%s", params=[act_id, module_id, user_id, task_type])
                    config_json = config_json["gear_list"]
                    for sub_config_json in config_json:
                        task_count = self.init_task_count(task_info_dict, task_count_list, sub_config_json["id"])
                        if task_count.complete_count == 1:
                            continue
                        task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_type,sub_config_json["id"],user_id)
                        if now_count >= decimal.Decimal(sub_config_json["gear"]):
                            task_count = TaskCount()
                            task_count.id_md5 = task_count_id_md5
                            task_count.app_id = app_id
                            task_count.act_id = act_id
                            task_count.module_id = module_id
                            task_count.user_id = user_id
                            task_count.open_id = open_id
                            task_count.task_type = task_type
                            task_count.task_sub_type = sub_config_json["id"]
                            task_count.complete_count = 0
                            task_count.now_count = 1
                            task_count.create_date = SevenHelper.get_now_datetime()
                            task_count.modify_date = SevenHelper.get_now_datetime()
                            task_count.modify_day = SevenHelper.get_now_day_int()
                            task_count_model.add_update_entity(task_count, "complete_count=0,now_count=1,modify_date=%s,modify_day=%s", params=[task_count.modify_date, task_count.modify_day])

            result, message = db_transaction.commit_transaction(True)
            if result == False:
                raise Exception("执行事务失败", message)
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【添加档位任务累计值】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【添加档位任务累计值】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "添加档位任务累计值失败"
        finally:
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name,task_count_identifier)

        return invoke_result_data

    def add_task_count(self, app_id, act_id, module_id, user_id, open_id, task_type, value, task_info_dict=None, task_sub_type=''):
        """
        :description: 添加常规任务计数
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识(比传)
        :param open_id：open_id
        :param task_type：任务类型
        :param value：计数值
        :param task_info_dict：任务信息
        :param task_sub_type：任务子类型
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            if not task_info_dict:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
            if task_info_dict:
                if task_sub_type and isinstance(task_info_dict["config_json"],list):
                    sub_config_json = [sub_config_json for sub_config_json in task_info_dict["config_json"] if task_sub_type == sub_config_json["id"]]
                    if not sub_config_json:
                        invoke_result_data.succsess = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "完成上限"
                        return invoke_result_data
                    limit_num = int(sub_config_json["limit_num"]) if sub_config_json.__contains__("limit_num") else 1
                    satisfy_num = int(sub_config_json["satisfy_num"]) if sub_config_json.__contains__("satisfy_num") else 1
                else:
                    config_json = task_info_dict["config_json"]
                    limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                    satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],task_sub_type,user_id)
                task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                if acquire_lock_status == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "acquire_lock"
                    invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                    return invoke_result_data
                task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                task_count_list = [task_count] if task_count else []
                task_count = self.init_task_count(task_info_dict, task_count_list, task_sub_type)
                count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                is_limit = True if count >= (limit_num * satisfy_num) else False
                if is_limit == True:
                    invoke_result_data.succsess = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "完成上限"
                    return invoke_result_data
                now_datetime = SevenHelper.get_now_datetime()
                now_day = SevenHelper.get_now_day_int()
                task_count.id_md5 = task_count_id_md5
                task_count.app_id = app_id
                task_count.act_id = act_id
                task_count.module_id = module_id
                task_count.user_id = user_id
                task_count.open_id = open_id
                task_count.task_type = task_info_dict["task_type"]
                task_count.task_sub_type = task_sub_type
                task_count.now_count = task_count.now_count + int(value)
                task_count.create_date = now_datetime
                task_count.modify_date = now_datetime
                task_count.modify_day = now_day
                update_sql = "complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s"
                params = [task_count.complete_count, task_count.now_count, task_count.modify_date, task_count.modify_day]
                if task_count.complete_count > 0:
                    update_sql = "now_count=%s,modify_date=%s,modify_day=%s"
                    params = [task_count.now_count, task_count.modify_date, task_count.modify_day]
                task_count_model.add_update_entity(task_count, update_sql, params=params)
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【添加任务累计值】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【添加任务累计值】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "添加任务累计值失败"
        finally:
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name, task_count_identifier)

        return invoke_result_data

    def get_gear_task_count(self, app_id, act_id, module_id, user_id, task_type, complete_type):
        """
        :description: 获取累计消费金额，累计抽盒次数等等
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识(比传)
        :param task_type：任务类型
        :param complete_type：完成类型
        :return:
        :last_editors: HuangJianYi
        """
        task_gear_count_model = TaskGearCountModel(context=self.context).set_sub_table(app_id)
        condition_where = ConditionWhere()
        task_gear_count_id_md5 = CryptoHelper.md5_encrypt_int(f"{act_id}_{module_id}_{task_type}_{user_id}")
        condition_where.add_condition("id_md5=%s")
        params = [task_gear_count_id_md5]
        if complete_type == TaskCompleteType.day.value:
            condition_where.add_condition("create_day=%s")
            params.append(SevenHelper.get_now_day_int())
        elif complete_type == TaskCompleteType.week.value:
            start_day = int(TimeHelper.get_first_day_of_the_week().strftime('%Y%m%d'))
            end_day = int(TimeHelper.get_last_day_of_the_week().strftime('%Y%m%d'))
            condition_where.add_condition("create_day>=%s and create_day<=%s")
            params.append(start_day)
            params.append(end_day)
        elif complete_type == TaskCompleteType.month.value:
            condition_where.add_condition("create_month=%s")
            params.append(SevenHelper.get_now_month_int())
        if module_id:
            condition_where.add_condition("module_id=%s")
            params.append(module_id)
        task_gear_count_dict = task_gear_count_model.get_dict(condition_where.to_string(),field="sum(now_count) as now_count",params=params)
        current = task_gear_count_dict["now_count"] if task_gear_count_dict["now_count"] else 0  # 当前总累计值
        return current

    def convert_task_node(self, task_id, sort_index, task_type, task_type_name, title, desc='', current=0, total=1, data=[], complete_count=1, current_complete_count=0, reward_value=0, completed_ids=[], get_ways=0, status=0, btn_text=[], route_url=''):
        """
        :description: 合成任务节点
        :param task_id：任务id
        :param sort_index：排序
        :param task_type：任务类型
        :param task_type_name：任务类型名称
        :param title：标题
        :param desc：描述
        :param current：当前轮计数值
        :param total：当前轮领取阀值(消费任务表示领取奖励需要消费的金额)
        :param data：如果有额外数据放这里，如果商品数据，或者子任务数据
        :param complete_count：可以完成的次数
        :param current_complete_count：当前完成的次数
        :param reward_value：奖励值
        :param completed_ids：完成的ids，比如：已收藏的商品ids或者已完成的子任务ids
        :param get_ways：领取方式(0-直接领取 1-通过领取接口领取)
        :param status：状态
        :param btn_text：按钮文本数组
        :param route_url：路由地址
        :return:
        :last_editors: HuangJianYi
        """
        result = {}
        result["sort_index"] = sort_index
        result["id"] = task_id
        result["task_type"] = task_type
        result["task_type_name"] = task_type_name
        result["title"] = title
        result["desc"] = desc
        result["current"] = current
        result["total"] = total
        result["data"] = data
        result["complete_count"] = complete_count
        result["current_complete_count"] = current_complete_count
        result["reward_value"] = reward_value
        result["completed_ids"] = completed_ids
        result["get_ways"] = get_ways
        result["status"] = status
        result["btn_text"] = btn_text
        result["route_url"] = route_url
        return result

    def convert_gear_task_node(self, app_id, act_id, module_id, user_id, task_info_dict, config_json, task_count_list):
        """
        :description: 合成档位任务结果
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param task_info_dict:任务信息
        :param config_json:{"gear_list":[{"id":1,"gear":0,"reward_type":1,"reward_name":"","asset_object_id":"","reward_value":0}]} 字段说明：id:前端生成的唯一标识 gear:档位阀值 reward_value:奖励值(等于0无法领取) satisfy_num:满足数 reward_type:奖励类型 reward_name:奖励奖品名称 asset_object_id:对象标识(如果奖励类型是资产对应资产对象标识，如果是奖品对应奖品标识，如果是卡片对应卡片标识)
        :param task_count_list:计数列表
        :return 
        :last_editors: HuangJianYi
        """
        result = deepcopy(self.convert_task_node(task_info_dict["id"],task_info_dict["sort_index"],task_info_dict["task_type"],SevenHelper.get_enum_key(TaskType, task_info_dict["task_type"]),task_info_dict["task_name"],get_ways=1,route_url="receive_reward"))
        result["current"] =  self.get_gear_task_count(app_id, act_id, module_id, user_id, task_info_dict["task_type"], task_info_dict["complete_type"])
        #只要判断到“消费金额”或“购买金额”中的任意一个在 task_info_dict["task_name"] 中就返回true
        if not any(word in task_info_dict["task_name"] for word in ["消费金额","购买金额"]):
            result["current"] = int(result["current"])
        for sub_config_json in config_json["gear_list"]:
            sub_task_count = self.init_task_count(task_info_dict, task_count_list, sub_config_json["id"])
            #避免档位任务新增子任务没有重新操作导致无法领取，需要初始化下数据
            if sub_task_count.id <= 0 and decimal.Decimal(result["current"]) >= decimal.Decimal(sub_config_json["gear"]):
                task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                task_count = TaskCount()
                task_count.id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict['task_type'],sub_config_json["id"],user_id)
                task_count.app_id = app_id
                task_count.act_id = act_id
                task_count.module_id = module_id
                task_count.user_id = user_id
                task_count.open_id = ''
                task_count.task_type = task_info_dict["task_type"]
                task_count.task_sub_type = sub_config_json["id"]
                task_count.complete_count = 0
                task_count.now_count = 1
                task_count.create_date = SevenHelper.get_now_datetime()
                task_count.modify_date = SevenHelper.get_now_datetime()
                task_count.modify_day = SevenHelper.get_now_day_int()
                task_count_model.add_update_entity(task_count, "complete_count=0,now_count=1,modify_date=%s,modify_day=%s", params=[task_count.modify_date, task_count.modify_day])

            if sub_task_count.complete_count > 0:
                result["completed_ids"].append(sub_config_json["id"])
            sub_info = {}
            sub_info["id"] = sub_config_json["id"] #子任务id
            sub_info["gear"] = sub_config_json["gear"] #档位阀值
            sub_info["reward_name"] = sub_config_json["reward_name"] #奖励名称
            sub_info["reward_value"] = sub_config_json["reward_value"] #奖励数量
            result["data"].append(sub_info)
        result["current_complete_count"] = 1 if len(result["completed_ids"]) == len(sub_config_json) else 0

        return result

    def get_client_task_list(self, app_id, act_id, module_id, user_id, task_types="", app_key="", app_secret="", is_log=False, daily_repeat_browse=False, mix_nick="", order_by="sort_index desc,id asc", browse_site_task_types=None):
        """
        :description: 获取任务列表
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param task_types:任务类型 多个逗号,分隔
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log:是否记录top请求日志
        :param daily_repeat_browse:单个商品可每日重复浏览 True是False否
        :param mix_nick:混淆昵称
        :param order_by:排序
        :param browse_site_task_types:浏览任务类型数组
        :return 
        :last_editors: HuangJianYi
        """
        task_info_list = self.get_task_info_dict_list(app_id, act_id, module_id, 1, True, source_object_id='', is_del=0, order_by=order_by)
        task_count_model = TaskCountModel(context=self.context, is_auto=True).set_sub_table(app_id)
        task_count_list = task_count_model.get_list("act_id=%s and module_id=%s and user_id=%s", params=[act_id, module_id, user_id])
        now_day = TimeExHelper.get_now_day_int()
        app_info_dict = None
        result_list = []
        if not browse_site_task_types:
            browse_site_task_types = [TaskType.browse_store.value,TaskType.browse_live_room.value,TaskType.browse_special_topic.value]
        for task_info_dict in task_info_list:
            if task_types:
                if str(task_info_dict["task_type"]) not in task_types.split(','):
                    continue
            config_json = SevenHelper.json_loads(task_info_dict["config_json"])
            if not config_json:
                continue

            result = {}
            result["sort_index"] = task_info_dict["sort_index"]
            result["task_id"] = task_info_dict["id"]
            result["task_type"] = task_info_dict["task_type"]
            result["title"] = task_info_dict["task_name"]
            result["config_json"] = config_json
            result["reward_value"] = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0

            task_count = self.init_task_count(task_info_dict, task_count_list)

            #掌柜有礼、免费领取、新人有礼
            if task_info_dict["task_type"] == TaskType.free_gift.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["text"] = ["领取", "已领取"]
                result_list.append(result)
            #单次签到
            elif task_info_dict["task_type"] == TaskType.one_sign.value:
                result["content"] = ""
                result["status"] = 1 if task_count.complete_count > 0 else 0
                result["text"] = ["签到", "已签到"]
                result_list.append(result)
            #每周签到(指定天数签到)(status:0当天未签到1当天已签到2已完成)
            elif task_info_dict["task_type"] == TaskType.weekly_sign.value:
                result["complete_count"] = task_count.complete_count
                result["content"] = f"已签到{task_count.complete_count}天"
                if isinstance(config_json["day_list"],list):
                    max_sign_day = max(query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list())
                else:
                    max_sign_day = int(max(config_json["day_list"])) if len(config_json["day_list"].keys()) > 0 else 0
                if task_count.complete_count >= max_sign_day:
                    result["status"] = 2
                else:
                    result["status"] = 1 if task_count.modify_day == now_day else 0
                result["text"] = ["签到", "已签到","已完成"]
                result_list.append(result)
            #累计签到(status:0当天未签到1当天已签到2已完成)
            elif task_info_dict["task_type"] == TaskType.cumulative_sign.value:
                result["complete_count"] = task_count.complete_count
                result["content"] = f"已签到{task_count.complete_count}天"
                if isinstance(config_json["day_list"],list):
                    max_sign_day = max(query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list())
                else:
                    max_sign_day = int(max(config_json["day_list"])) if len(config_json["day_list"].keys()) > 0 else 0
                if task_count.complete_count >= max_sign_day:
                    result["status"] = 2
                else:
                    result["status"] = 1 if task_count.modify_day == now_day else 0
                result["text"] = ["签到", "已签到","已完成"]
                result_list.append(result)
            #连续签到(status:0当天未签到1当天已签到2已完成)
            elif task_info_dict["task_type"] == TaskType.successive_sign.value:
                result["complete_count"] = task_count.complete_count
                result["content"] = f"已签到{task_count.complete_count}天"
                if isinstance(config_json["day_list"],list):
                    max_sign_day = max(query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list())
                else:
                    max_sign_day = int(max(config_json["day_list"])) if len(config_json["day_list"].keys()) > 0 else 0
                if task_count.complete_count >= max_sign_day:
                    result["status"] = 2
                else:
                    result["status"] = 1 if task_count.modify_day == now_day else 0
                result["text"] = ["签到", "已签到","已完成"]
                result_list.append(result)
            #邀请新用户
            elif task_info_dict["task_type"] == TaskType.invite_new_user.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["complete_count"] = task_count.complete_count
                result["now_count"] = task_count.now_count
                result["limit_num"] = limit_num
                result["satisfy_num"] = satisfy_num
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去邀请", "领取", "已完成"]
                result_list.append(result)
            #邀请加入会员
            elif task_info_dict["task_type"] == TaskType.invite_join_member.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["complete_count"] = task_count.complete_count
                result["now_count"] = task_count.now_count
                result["limit_num"] = limit_num
                result["satisfy_num"] = satisfy_num
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去邀请", "领取", "已完成"]
                result_list.append(result)
            #关注店铺
            elif task_info_dict["task_type"] == TaskType.favor_store.value:
                if not app_info_dict:
                    app_base_model = AppBaseModel(context=self.context)
                    app_info_dict = app_base_model.get_app_info_dict(app_id)
                once_favor_reward = int(config_json["once_favor_reward"]) if config_json.__contains__("once_favor_reward") else 1
                user_base_model = UserBaseModel(context=self.context)
                user_info_dict = user_base_model.get_user_info_dict(app_id,act_id,user_id)
                if not user_info_dict:
                    result["status"] = 0
                else:
                    if module_id:
                        if task_count.complete_count >= 1:
                            result["status"] = 1
                        elif user_info_dict["is_favor_before"] == 1 and once_favor_reward == 0:
                            result["status"] = 1
                        else:
                            result["status"] = 0
                    else:
                        if user_info_dict["is_favor"] == 1:
                            result["status"] = 1
                        elif user_info_dict["is_favor_before"] == 1 and once_favor_reward == 0:
                            result["status"] = 1
                        else:
                            result["status"] = 0
                result["content"] = ""
                result["store_name"] = app_info_dict["store_name"] if app_info_dict else ""
                result["text"] = ["去关注", "已关注"]
                result_list.append(result)
            #加入会员
            elif task_info_dict["task_type"] == TaskType.join_member.value:
                if not app_info_dict:
                    app_base_model = AppBaseModel(context=self.context)
                    app_info_dict = app_base_model.get_app_info_dict(app_id)
                once_member_reward = int(config_json["once_member_reward"]) if config_json.__contains__("once_member_reward") else 1
                plat_type = share_config.get_value("plat_type", PlatType.tb.value)  # 平台类型
                user_base_model = UserBaseModel(context=self.context)
                user_info_dict = user_base_model.get_user_info_dict(app_id,act_id,user_id)
                if not user_info_dict:
                    result["status"] = 0
                else:
                    if module_id:
                        if task_count.complete_count >= 1:
                            result["status"] = 2
                        elif user_info_dict["is_member_before"] == 1 and once_member_reward == 0:
                            result["status"] = 2
                        else:
                            if plat_type == PlatType.tb.value:
                                access_token = app_info_dict["access_token"] if app_info_dict else ""
                                top_base_model = TopBaseModel(context=self.context)
                                if top_base_model.check_is_member(mix_nick,'',access_token,app_key,app_secret,is_log) == True:
                                    result["status"] = 1
                                else:
                                    result["status"] = 0
                            else:
                                result["status"] = user_info_dict["is_member"]
                    else:
                        if user_info_dict["is_member"] == 1:
                            result["status"] = 2
                        elif user_info_dict["is_member_before"] == 1 and once_member_reward == 0:
                            result["status"] = 2
                        else:
                            if plat_type == PlatType.tb.value:
                                access_token = app_info_dict["access_token"] if app_info_dict else ""
                                top_base_model = TopBaseModel(context=self.context)
                                if top_base_model.check_is_member(mix_nick,'',access_token,app_key,app_secret,is_log) == True:
                                    result["status"] = 1
                                else:
                                    result["status"] = 0
                            else:
                                result["status"] = user_info_dict["is_member"]
                result["content"] = ""
                result["text"] = ["立即入会", "立即领取", "已领取"]
                result_list.append(result)
            #收藏商品
            elif task_info_dict["task_type"] == TaskType.collect_goods.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                collect_log_model = CollectLogModel(context=self.context)
                condition = "act_id=%s and user_id=%s"
                params = [act_id, user_id]
                user_goods_list = collect_log_model.get_cache_list(condition, params=params,dependency_key=f"collect_log:actid_{act_id}_userid_{user_id}")
                result["goods_list"] = config_json["goods_list"] if config_json.__contains__("goods_list") else []
                result["user_goods_list"] = [str(i.goods_id) for i in user_goods_list] if len(user_goods_list) > 0 else []
                result["complete_count"] = task_count.complete_count
                result["now_count"] = task_count.now_count
                result["limit_num"] = limit_num
                result["satisfy_num"] = satisfy_num
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去收藏", "已收藏","已完成"]
                result_list.append(result)
            #浏览商品
            elif task_info_dict["task_type"] == TaskType.browse_goods.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                browse_log_model = BrowseLogModel(context=self.context)
                condition = "act_id=%s and user_id=%s"
                params = [act_id,user_id]
                if daily_repeat_browse == True:
                    condition += " and create_day=%s"
                    params.append(now_day)
                user_goods_list = browse_log_model.get_cache_list(condition, params=params,dependency_key=f"browse_log:actid_{act_id}_userid_{user_id}")
                result["goods_list"] = config_json["goods_list"] if config_json.__contains__("goods_list") else []
                result["user_goods_list"] = [str(i.goods_id) for i in user_goods_list] if len(user_goods_list) > 0 else []
                result["complete_count"] = task_count.complete_count
                result["now_count"] = task_count.now_count
                result["limit_num"] = limit_num
                result["satisfy_num"] = satisfy_num
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去浏览", "已浏览","已完成"]
                result_list.append(result)
            #浏览网址
            elif isinstance(config_json, list) and task_info_dict["task_type"] in browse_site_task_types:
                for sub_config_json in config_json:
                    sub_task_count = [task_count for task_count in task_count_list if task_info_dict["task_type"] == task_count.task_type and task_count.task_sub_type == sub_config_json["id"]]
                    if not sub_task_count:
                        sub_task_count = TaskCount()
                    else:
                        sub_task_count = sub_task_count[0]
                    if task_info_dict["complete_type"] == 1 and sub_task_count.modify_day != now_day:
                        sub_task_count.complete_count = 0
                        sub_task_count.now_count = 0
                    elif task_info_dict["complete_type"] == 2 and not TimeHelper.is_this_week(sub_task_count.modify_date):
                        sub_task_count.complete_count = 0
                        sub_task_count.now_count = 0
                    elif task_info_dict["complete_type"] == 3 and sub_task_count.id == 0:
                        sub_task_count.complete_count = 0
                        sub_task_count.now_count = 0
                    limit_num = int(sub_config_json["limit_num"]) if sub_config_json.__contains__("limit_num") else 1
                    satisfy_num = int(sub_config_json["satisfy_num"]) if sub_config_json.__contains__("satisfy_num") else 1
                    result = {}
                    result["sort_index"] = task_info_dict["sort_index"]
                    result["task_id"] = task_info_dict["id"]
                    result["task_type"] = task_info_dict["task_type"]
                    result["task_sub_type"] = sub_config_json["id"]
                    result["title"] = task_info_dict["task_name"]
                    result["config_json"] = sub_config_json
                    result["reward_value"] = int(sub_config_json["reward_value"]) if sub_config_json.__contains__("reward_value") else 0
                    if sub_task_count.complete_count >= limit_num:
                        result["status"] = 1
                    else:
                        result["status"] = 0
                    result["link_url"] = sub_config_json["link_url"] if sub_config_json.__contains__("link_url") else ""
                    result["complete_count"] = sub_task_count.complete_count
                    result["now_count"] = sub_task_count.now_count
                    result["limit_num"] = limit_num
                    result["satisfy_num"] = satisfy_num
                    result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-sub_task_count.complete_count}次"
                    result["text"] = ["去浏览", "已完成"]
                    result_list.append(result)
            #分享奖励
            elif task_info_dict["task_type"] == TaskType.share.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去分享", "领取","已完成"]
                result_list.append(result)
            #浏览店铺
            elif task_info_dict["task_type"] == TaskType.browse_store.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去完成", "领取","已完成"]
                result_list.append(result)
            #浏览直播间
            elif task_info_dict["task_type"] == TaskType.browse_live_room.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["complete_count"] = task_count.complete_count
                result["limit_num"] = limit_num
                result["satisfy_num"] = satisfy_num
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去浏览", "领取","已完成"]
                result_list.append(result)
            #邀请助力
            elif task_info_dict["task_type"] == TaskType.invite_user_help.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 2
                elif task_count.now_count >= satisfy_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                invite_help_model = InviteHelpModel(context=self.context)
                help_type = 1
                help_object_id = ''
                help_id_md5 = CryptoHelper.md5_encrypt_int(f"{app_id}_{act_id}_{module_id}_{help_type}_{help_object_id}")
                invite_help_list = invite_help_model.get_cache_dict_list("id_md5=%s and user_id=%s and create_day=%s", "", order_by="id desc", field="invited_avatar", params=[help_id_md5, user_id, SevenHelper.get_now_day_int()], dependency_key=DependencyKey.invite_user_help_list(help_id_md5,user_id))
                result["data"] = invite_help_list if len(invite_help_list) > 0 else []
                result["complete_count"] = task_count.complete_count
                result["now_count"] = task_count.now_count
                result["limit_num"] = limit_num
                result["satisfy_num"] = satisfy_num
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["去邀请", "领取", "已完成"]
                result_list.append(result)
            #神秘暗号
            elif task_info_dict["task_type"] == TaskType.secret_code.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["输入暗号","已完成"]
                result_list.append(result)
            #店铺会员积分兑换资产
            elif task_info_dict["task_type"] == TaskType.crm_point_exchange_asset.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["complete_count"] = task_count.complete_count
                result["limit_num"] = limit_num
                result["satisfy_num"] = satisfy_num
                result["content"] = f"完成次数上限{limit_num}次，当前剩余{limit_num-task_count.complete_count}次"
                result["text"] = ["兑换","已完成"]
                result_list.append(result)

        return result_list,task_info_list,task_count_list

    def get_client_task_list_v2(self, app_id, act_id, module_id, user_id, task_types="", daily_repeat_browse=False, order_by="sort_index desc,id asc", param_dict={}):
        """
        :description: 获取任务列表
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param task_types:任务类型 多个逗号,分隔
        :param daily_repeat_browse:单个商品可每日重复浏览 True是False否
        :param order_by:排序
        :param param_dict:参数字典
        :return 
        :last_editors: HuangJianYi
        """
        task_info_list = self.get_task_info_dict_list(app_id, act_id, module_id, 1, True, source_object_id='', is_del=0, order_by=order_by)
        task_count_model = TaskCountModel(context=self.context, is_auto=True).set_sub_table(app_id)
        task_count_list = task_count_model.get_list("act_id=%s and module_id=%s and user_id=%s", params=[act_id, module_id, user_id])
        now_day = TimeExHelper.get_now_day_int()
        result_list = []
        for task_info_dict in task_info_list:
            if task_types:
                if str(task_info_dict["task_type"]) not in task_types.split(','):
                    continue
            config_json = SevenHelper.json_loads(task_info_dict["config_json"])
            if not config_json:
                continue
            result = self.convert_task_node(task_info_dict["id"],
                                       task_info_dict["sort_index"],
                                       task_info_dict["task_type"],
                                       SevenHelper.get_enum_key(TaskType, task_info_dict["task_type"]),
                                       task_info_dict["task_name"]
                                       )
            if result["task_type"] == TaskType.weekly_sign.value:
                if isinstance(config_json["day_list"],list):
                    result["data"] = query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list()
                    result["reward_value"] = query(config_json["day_list"]).select(lambda x: int(x["reward_value"])).to_list()
                else:
                    result["data"] = list(config_json["day_list"].keys())
                    result["reward_value"] = list(config_json["day_list"].values())

            elif result["task_type"] in [TaskType.cumulative_sign.value, TaskType.successive_sign.value]:
                if isinstance(config_json["day_list"],list):
                    if len(config_json["day_list"]) == 0:
                        result["reward_value"] = 0
                    elif config_json["day_list"] == 1:
                        result["data"] = [config_json["day_list"][0]["day"]]
                        result["reward_value"] = config_json["day_list"][0]["reward_value"]
                        result["total"] = int(result["data"][0])
                    else:
                        result["data"] = query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list()
                        result["reward_value"] = query(config_json["day_list"]).select(lambda x: int(x["reward_value"])).to_list()
                else:
                    result["data"] = list(config_json["day_list"].keys())
                    if len(result["data"]) == 0:
                        result["reward_value"] = 0
                    elif len(result["data"]) == 1:
                        result["total"] = int(result["data"][0])
                        result["reward_value"] = config_json["day_list"][str(result["data"][0])]
                    else:
                        result["reward_value"] = list(config_json["day_list"].values())

            else:
                result["reward_value"] = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0

            complete_type_name = self.get_complete_type_name(task_info_dict["complete_type"]) # 完成类型名称
            task_count = self.init_task_count(task_info_dict, task_count_list)

            #掌柜有礼、免费领取、新人有礼
            if task_info_dict["task_type"] == TaskType.free_gift.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["current"] = task_count.complete_count
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["btn_text"] = ["领取", "已领取"]
                result["route_url"] = "free_gift"
                result_list.append(result)
            #单次签到
            elif task_info_dict["task_type"] == TaskType.one_sign.value:
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["current"] = task_count.complete_count
                result["status"] = 1 if task_count.complete_count > 0 else 0
                result["btn_text"] = ["签到", "已签到"]
                result["route_url"] = "one_sign"
                result_list.append(result)
            #每周签到(status:0当天未签到1当天已签到2已完成)
            elif task_info_dict["task_type"] == TaskType.weekly_sign.value:
                result["current"] = task_count.complete_count
                if isinstance(config_json["day_list"],list):
                    max_sign_day = max(query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list())
                else:
                    max_sign_day = int(max(config_json["day_list"])) if len(config_json["day_list"].keys()) > 0 else 0
                if task_count.complete_count >= max_sign_day:
                    result["status"] = 2
                else:
                    result["status"] = 1 if task_count.modify_day == now_day else 0
                result["total"] = max_sign_day
                result["complete_count"] = 1 #可以完成的次数
                result["current_complete_count"] = 1 if task_count.complete_count == max_sign_day else 0 #当前完成的次数
                result["btn_text"] = ["签到", "已签到","已完成"]
                result["route_url"] = "weekly_sign"
                result_list.append(result)
            #累计签到(status:0当天未签到1当天已签到2已完成)
            elif task_info_dict["task_type"] == TaskType.cumulative_sign.value:
                result["current"] = task_count.complete_count
                if isinstance(config_json["day_list"],list):
                    max_sign_day = max(query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list())
                else:
                    max_sign_day = int(max(config_json["day_list"])) if len(config_json["day_list"].keys()) > 0 else 0
                if task_count.complete_count >= max_sign_day:
                    result["status"] = 2
                else:
                    result["status"] = 1 if task_count.modify_day == now_day else 0
                result["total"] = max_sign_day
                result["complete_count"] = 1 #可以完成的次数
                result["current_complete_count"] = 1 if task_count.complete_count == max_sign_day else 0 #当前完成的次数
                result["btn_text"] = ["签到", "已签到","已完成"]
                result["route_url"] = "cumulative_sign"
                result_list.append(result)
            #连续签到(status:0当天未签到1当天已签到2已完成)
            elif task_info_dict["task_type"] == TaskType.successive_sign.value:
                result["current"] = task_count.complete_count
                if isinstance(config_json["day_list"],list):
                    max_sign_day = max(query(config_json["day_list"]).select(lambda x: int(x["day"])).to_list())
                else:
                    max_sign_day = int(max(config_json["day_list"])) if len(config_json["day_list"].keys()) > 0 else 0
                if task_count.complete_count >= max_sign_day:
                    result["status"] = 2
                else:
                    result["status"] = 1 if task_count.modify_day == now_day else 0
                result["total"] = max_sign_day
                result["complete_count"] = 1 #可以完成的次数
                result["current_complete_count"] = 1 if task_count.complete_count == max_sign_day else 0 #当前完成的次数
                result["btn_text"] = ["签到", "已签到","已完成"]
                result["route_url"] = "successive_sign"
                result_list.append(result)
            #邀请新用户
            elif task_info_dict["task_type"] == TaskType.invite_new_user.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                if task_count.complete_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                invite_log_model = InviteLogModel(context=self.context)
                invite_log_list = invite_log_model.get_cache_dict_list("act_id=%s and user_id=%s and create_day=%s", "", order_by="id desc", field="invite_avatar", params=[act_id, user_id, SevenHelper.get_now_day_int()], dependency_key=DependencyKey.invite_log_list(act_id,user_id))
                result["data"] = invite_log_list if len(invite_log_list) > 0 else []
                result["title"] = f"每日邀请{satisfy_num}名新用户"
                result["total"] = satisfy_num
                result["current"] = task_count.now_count
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["desc"] = f"{complete_type_name}完成上限{limit_num}次，当前剩余" + "{remain_complete_count}次"
                result["get_ways"] = get_ways
                result["btn_text"] = ["去邀请", "已完成"]
                result["route_url"] = "task_inivite"
                result_list.append(result)
            #邀请加入会员
            elif task_info_dict["task_type"] == TaskType.invite_join_member.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                invite_count = task_count.complete_count * satisfy_num + task_count.now_count
                if invite_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                invite_log_model = InviteLogModel(context=self.context, sub_table="member")
                invite_log_list = invite_log_model.get_cache_dict_list("act_id=%s and user_id=%s and create_day=%s", "", order_by="id desc", field="invite_avatar", params=[act_id, user_id, SevenHelper.get_now_day_int()], dependency_key=DependencyKey.invite_log_member_list(act_id,user_id))
                result["data"] = invite_log_list if len(invite_log_list) > 0 else []
                result["title"] = f"每日邀请{satisfy_num}名入会"
                result["total"] = satisfy_num
                result["current"] = task_count.now_count
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["desc"] = f"{complete_type_name}完成上限{limit_num}次，当前剩余" + "{remain_complete_count}次"
                result["get_ways"] = get_ways
                result["btn_text"] = ["去邀请", "已完成"]
                result["route_url"] = "task_invite_member"
                result_list.append(result)
            #关注店铺
            elif task_info_dict["task_type"] == TaskType.favor_store.value:
                once_favor_reward = int(config_json["once_favor_reward"]) if config_json.__contains__("once_favor_reward") else 1
                user_base_model = UserBaseModel(context=self.context)
                user_info_dict = user_base_model.get_user_info_dict(app_id,act_id,user_id)
                if not user_info_dict:
                    result["status"] = 0
                else:
                    if module_id:
                        if task_count.complete_count >= 1:
                            result["status"] = 1
                        elif user_info_dict["is_favor_before"] == 1 and once_favor_reward == 0:
                            result["status"] = 1
                        else:
                            result["status"] = 0
                    else:
                        if task_count.complete_count >= 1 or user_info_dict["is_favor"] == 1:
                            result["status"] = 1
                        elif user_info_dict["is_favor_before"] == 1 and once_favor_reward == 0:
                            result["status"] = 1
                        else:
                            result["status"] = 0
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去关注", "已关注"]
                result["route_url"] = "task_favor"
                result_list.append(result)
            #加入会员
            elif task_info_dict["task_type"] == TaskType.join_member.value:
                once_member_reward = int(config_json["once_member_reward"]) if config_json.__contains__("once_member_reward") else 1
                user_base_model = UserBaseModel(context=self.context)
                user_info_dict = user_base_model.get_user_info_dict(app_id,act_id,user_id)
                if not user_info_dict:
                    result["status"] = 0
                else:
                    if module_id:
                        if task_count.complete_count >= 1:
                            result["status"] = 1
                        elif user_info_dict["is_member_before"] == 1 and once_member_reward == 0:
                            result["status"] = 1
                        else:
                            result["status"] = 0
                    else:
                        if task_count.complete_count >= 1 or user_info_dict["is_member"] == 1:
                            result["status"] = 1
                        elif user_info_dict["is_member_before"] == 1 and once_member_reward == 0:
                            result["status"] = 1
                        else:
                            result["status"] = 0
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["立即入会", "已领取"]
                result["route_url"] = "task_member"
                result_list.append(result)
            #收藏商品
            elif task_info_dict["task_type"] == TaskType.collect_goods.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                collect_log_model = CollectLogModel(context=self.context)
                condition = "act_id=%s and user_id=%s"
                params = [act_id, user_id]
                user_goods_list = collect_log_model.get_cache_list(condition, params=params,dependency_key=DependencyKey.collect_log(act_id,user_id))
                result["data"] = config_json["goods_list"] if config_json.__contains__("goods_list") else []
                result["completed_ids"] = [str(i.goods_id) for i in user_goods_list] if len(user_goods_list) > 0 else []
                result["current"] = task_count.now_count
                result["total"] = len(result["data"])
                result["status"] = 1 if len(result["data"]) == len(result["completed_ids"]) else 0
                result["get_ways"] = get_ways
                result["current_complete_count"] = 1 if result["status"] == 1 else 0 #当前完成的次数
                result["btn_text"] = ["去收藏", "已完成"]
                result["route_url"] = "task_collect"
                result_list.append(result)
            #浏览商品
            elif task_info_dict["task_type"] == TaskType.browse_goods.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                browse_log_model = BrowseLogModel(context=self.context)
                condition = "act_id=%s and user_id=%s"
                params = [act_id,user_id]
                if daily_repeat_browse == True:
                    condition += " and create_day=%s"
                    params.append(now_day)
                user_goods_list = browse_log_model.get_cache_list(condition, params=params,dependency_key=DependencyKey.browse_log(act_id,user_id))
                result["data"] = config_json["goods_list"] if config_json.__contains__("goods_list") else []
                result["completed_ids"] = [str(i.goods_id) for i in user_goods_list] if len(user_goods_list) > 0 else []
                result["current"] = task_count.now_count
                result["total"] = len(result["data"])
                result["status"] = 1 if len(result["data"]) == len(result["completed_ids"]) else 0
                result["get_ways"] = get_ways
                result["current_complete_count"] = 1 if result["status"] == 1 else 0 #当前完成的次数
                result["btn_text"] = ["去浏览", "已完成"]
                result["route_url"] = "task_browse"
                result_list.append(result)
            #分享奖励
            elif task_info_dict["task_type"] == TaskType.share.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 0
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                result["current"] = task_count.now_count
                result["total"] = satisfy_num
                if task_count.complete_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去分享","已完成"]
                result["route_url"] = "task_share"
                result_list.append(result)
            #浏览店铺
            elif task_info_dict["task_type"] == TaskType.browse_store.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                result["current"] = task_count.complete_count
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去浏览", "已完成"]
                result["route_url"] = "task_browse_store"
                result_list.append(result)
            #浏览直播间
            elif task_info_dict["task_type"] == TaskType.browse_live_room.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                result["data"] = [config_json["link_url"]] if config_json.__contains__("link_url") else []
                result["current"] = task_count.complete_count
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去浏览", "已完成"]
                result["route_url"] = "task_browse_liveroom"
                result_list.append(result)
            #邀请助力
            elif task_info_dict["task_type"] == TaskType.invite_user_help.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                invite_count = task_count.complete_count * satisfy_num + task_count.now_count
                if invite_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                invite_help_model = InviteHelpModel(context=self.context)
                help_type = 1
                help_object_id = ''
                help_id_md5 = CryptoHelper.md5_encrypt_int(f"{app_id}_{act_id}_{module_id}_{help_type}_{help_object_id}")
                invite_help_condition = "id_md5=%s and user_id=%s"
                invite_help_is_handle = param_dict.get("invite_help_is_handle", -1)
                if invite_help_is_handle != -1:
                    invite_help_condition += f" and is_handle={invite_help_is_handle}"
                invite_help_list = invite_help_model.get_cache_dict_list(invite_help_condition, "", order_by="id desc", field="invited_avatar", params=[help_id_md5, user_id], dependency_key=DependencyKey.invite_user_help_list(help_id_md5, user_id))
                result["data"] = invite_help_list if len(invite_help_list) > 0 else []
                result["title"] = f"每日邀请{satisfy_num}名用户"
                result["total"] = satisfy_num
                result["current"] = task_count.now_count
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去邀请", "已完成"]
                result["route_url"] = "task_inivite_help"
                result_list.append(result)
            #神秘暗号
            elif task_info_dict["task_type"] == TaskType.secret_code.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                result["current"] = task_count.complete_count
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["输入暗号", "已完成"]
                result["route_url"] = "task_secret_code"
                result_list.append(result)
            #店铺会员积分兑换资产
            elif task_info_dict["task_type"] == TaskType.crm_point_exchange_asset.value:
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["total"] = satisfy_num
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["兑换", "已完成"]
                result["route_url"] = "task_crm_exchange_asset"
                result_list.append(result)
            #购买指定商品
            elif task_info_dict["task_type"] == TaskType.buy_appoint_goods.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                remark = SevenHelper.json_loads(task_count.remark) if task_count.remark else {"goods_id_list":[]}
                result["data"] = config_json["goods_list"] if config_json.__contains__("goods_list") else []
                result["completed_ids"] = list(set(remark.get("goods_id_list",[])))
                result["total"] = satisfy_num
                result["current"] = task_count.now_count
                if task_count.complete_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["desc"] = f"{complete_type_name}完成上限{limit_num}次，当前剩余" + "{remain_complete_count}次"
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去完成", "已完成"]
                result["route_url"] = "receive_reward"
                result_list.append(result)
            #购买指定商品每多少金额
            elif task_info_dict["task_type"] == TaskType.buy_appoint_goods_price.value:
                total_price =  self.get_gear_task_count(app_id, act_id, module_id, user_id, task_info_dict["task_type"], task_info_dict["complete_type"])
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = decimal.Decimal(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                result["data"] = config_json["goods_list"] if config_json.__contains__("goods_list") else []
                result["total"] = satisfy_num
                result["current"] = decimal.Decimal(total_price) - (satisfy_num * task_count.complete_count)
                if task_count.complete_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["desc"] = f"{complete_type_name}完成上限{limit_num}次，当前剩余" + "{remain_complete_count}次"
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去完成", "已完成"]
                result["route_url"] = "receive_reward"
                result_list.append(result)
            #购买全店商品每多少金额
            elif task_info_dict["task_type"] == TaskType.buy_store_price.value:
                total_price =  self.get_gear_task_count(app_id, act_id, module_id, user_id, task_info_dict["task_type"], task_info_dict["complete_type"])
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = decimal.Decimal(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                result["data"] = config_json["goods_list"] if config_json.__contains__("goods_list") else []
                result["total"] = satisfy_num
                result["current"] = decimal.Decimal(total_price) - (satisfy_num * task_count.complete_count)
                if task_count.complete_count >= limit_num:
                    result["status"] = 1
                else:
                    result["status"] = 0
                result["desc"] = f"{complete_type_name}完成上限{limit_num}次，当前剩余" + "{remain_complete_count}次"
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去完成", "已完成"]
                result["route_url"] = "receive_reward"
                result_list.append(result)
            #抽盒/抽包/抽奖
            elif task_info_dict["task_type"] == TaskType.lottery.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                result["current"] = task_count.now_count
                result["total"] = satisfy_num
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去完成", "已完成"]
                result["route_url"] = "receive_reward"
                result_list.append(result)
            #试抽
            elif task_info_dict["task_type"] == TaskType.lottery_try.value:
                get_ways = config_json["get_ways"] if config_json.__contains__("get_ways") else 1
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                result["current"] = task_count.now_count
                result["total"] = satisfy_num
                result["status"] = 1 if task_count.complete_count >= limit_num else 0
                result["get_ways"] = get_ways
                result["complete_count"] = limit_num #可以完成的次数
                result["current_complete_count"] = task_count.complete_count #当前完成的次数
                result["btn_text"] = ["去完成", "已完成"]
                result["route_url"] = "receive_reward"
                result_list.append(result)
            #有档位任务列表的相关累计任务
            elif config_json.__contains__("gear_list") == True:
                result = self.convert_gear_task_node(app_id,act_id,module_id,user_id,task_info_dict,config_json,task_count_list)
                result_list.append(result)

        return result_list,task_info_list,task_count_list

    def process_free_gift(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,check_new_user=False,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None):
        """
        :description: 处理掌柜有礼、新人有礼、免费领取等相似任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_free_gift:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.free_gift.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = task_info_dict["config_json"]
                    reward_value = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0
                    limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                    asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    act_module_dict = invoke_result_data.data["act_module_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                    task_count = TaskCount() if not task_count else task_count
                    limit_meaasge = ""
                    if task_info_dict["complete_type"] == 1:
                        limit_meaasge = "今日领取上限"
                        if task_count.modify_day != now_day:
                            task_count.complete_count = 0
                            task_count.now_count = 0
                    elif task_info_dict["complete_type"] == 2:
                        limit_meaasge = "每周领取上限"
                        if TimeHelper.is_this_week(task_count.modify_date) == False:
                            task_count.complete_count = 0
                            task_count.now_count = 0
                    else:
                        limit_meaasge = "领取上限"
                    is_limit = True if task_count.complete_count >= limit_num else False
                    if is_limit == True:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = limit_meaasge
                    else:
                        task_count.id_md5 = task_count_id_md5
                        task_count.app_id = app_id
                        task_count.act_id = act_id
                        task_count.module_id = module_id
                        task_count.user_id = user_id
                        task_count.open_id = user_info_dict["open_id"]
                        task_count.task_type = task_type
                        task_count.task_sub_type = ""
                        task_count.complete_count = task_count.complete_count+1
                        task_count.now_count = 0
                        task_count.create_date = now_datetime
                        task_count.modify_date = now_datetime
                        task_count.modify_day = now_day
                        task_count_model.add_update_entity(task_count,"complete_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.modify_date,now_day])

                        reward_object_id = ""
                        if reward_value > 0:
                            only_id = self.get_only_id(user_id,task_info_dict["complete_type"],task_type,complete_count=task_count.complete_count)
                            if module_id > 0:
                                only_id = f"{module_id}_{only_id}"
                            asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                            reward_object_id = asset_type
                            asset_base_model = AssetBaseModel(context=self.context)
                            asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],task_info_dict["task_name"],only_id,handler_name,request_code,info_json=info_json)
                            if asset_invoke_result_data.success == False:
                                reward_value = 0
                        invoke_result_data.data["reward_value"] = reward_value
                        self.add_task_stat(task_type, app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                        self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=task_info_dict["task_name"],reward_type=1, reward_object_id=reward_object_id, reward_name="", reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            self.context.logging_link_error("【掌柜有礼任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_one_sign(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,check_new_user=False,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None):
        """
        :description: 处理单次签到任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_one_sign:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.one_sign.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = task_info_dict["config_json"]
                    reward_value = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0
                    asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    act_module_dict = invoke_result_data.data["act_module_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                    task_count = TaskCount() if not task_count else task_count
                    if task_info_dict["complete_type"] == 1 and task_count.modify_day == now_day:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "今日已签到"
                    elif task_info_dict["complete_type"] == 2 and TimeHelper.is_this_week(task_count.modify_date):
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "本周已签到"
                    elif task_info_dict["complete_type"] == 3 and task_count:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "已签到"
                    else:
                        task_count.id_md5 = task_count_id_md5
                        task_count.app_id = app_id
                        task_count.act_id = act_id
                        task_count.module_id = module_id
                        task_count.user_id = user_id
                        task_count.open_id = user_info_dict["open_id"]
                        task_count.task_type = task_type
                        task_count.task_sub_type = ""
                        task_count.complete_count = 1
                        task_count.now_count = 1
                        task_count.create_date = now_datetime
                        task_count.modify_date = now_datetime
                        task_count.modify_day = now_day
                        task_count_model.add_update_entity(task_count,"complete_count=1,now_count=1,modify_date=%s,modify_day=%s",params=[task_count.modify_date,now_day])
                        reward_object_id = ""
                        if reward_value > 0:
                            only_id = self.get_only_id(user_id,task_info_dict["complete_type"],task_type,complete_count=task_count.complete_count)
                            if module_id > 0:
                                only_id = f"{module_id}_{only_id}"
                            asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                            reward_object_id = asset_type
                            asset_base_model = AssetBaseModel(context=self.context)
                            asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],"签到1天",only_id,handler_name,request_code,info_json=info_json)
                            if asset_invoke_result_data.success == False:
                                reward_value = 0
                        invoke_result_data.data["reward_value"] = reward_value
                        self.add_task_stat(task_type,app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                        self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=task_info_dict["task_name"],reward_type=1, reward_object_id=reward_object_id, reward_name="", reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            self.context.logging_link_error("【单次签到任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_weekly_sign(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,check_new_user=False,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None,check_act_info_release=True,check_act_module_release=True):
        """
        :description: 处理每周签到任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :param check_act_info_release:校验活动信息是否发布
        :param check_act_module_release:校验活动模块是否发布
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_weekly_sign:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.weekly_sign.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name,check_act_info_release=check_act_info_release,check_act_module_release=check_act_module_release)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = task_info_dict["config_json"]
                    asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""
                    day_list = config_json["day_list"] if config_json.__contains__("day_list") else {}
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    act_module_dict = invoke_result_data.data["act_module_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                    task_count = TaskCount() if not task_count else task_count
                    if task_count.modify_day == now_day:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "今日已签到"
                    else:
                        task_count.id_md5 = task_count_id_md5
                        task_count.app_id = app_id
                        task_count.act_id = act_id
                        task_count.module_id = module_id
                        task_count.user_id = user_id
                        task_count.open_id = user_info_dict["open_id"]
                        task_count.task_type = task_type
                        task_count.task_sub_type = ""
                        task_count.complete_count = task_count.complete_count+1 if TimeHelper.is_this_week(task_count.modify_date) else 1
                        task_count.now_count = 1
                        task_count.create_date = now_datetime
                        task_count.modify_date = now_datetime
                        task_count.modify_day = now_day
                        task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])
                        if isinstance(day_list,list):
                            cur_day = query(day_list).first_or_default(None,lambda x: int(x["day"]) == task_count.complete_count)
                            if cur_day:
                                reward_value = int(cur_day["reward_value"])
                            else:
                                reward_value = 0
                        else:
                            reward_value = int(day_list[str(task_count.complete_count)]) if day_list.__contains__(str(task_count.complete_count)) else 0
                        reward_object_id = ""
                        if reward_value > 0:
                            only_id = self.get_only_id(user_id,2,task_type,complete_count=task_count.complete_count)
                            if module_id > 0:
                                only_id = f"{module_id}_{only_id}"
                            asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                            reward_object_id = asset_type
                            asset_base_model = AssetBaseModel(context=self.context)
                            asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],f"签到{task_count.complete_count}天",only_id,handler_name,request_code,info_json=info_json)
                            if asset_invoke_result_data.success == False:
                                reward_value = 0
                        invoke_result_data.data["reward_value"] = reward_value
                        self.add_task_stat(task_type,app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                        self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=f"签到{task_count.complete_count}天",reward_type=1, reward_object_id=reward_object_id, reward_name="", reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            self.context.logging_link_error("【每周签到任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_cumulative_sign(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,check_new_user=False,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None,task_type=0):
        """
        :description: 处理累计签到任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :param task_type:任务类型
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_cumulative_sign:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.cumulative_sign.value if task_type == 0 else task_type
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = task_info_dict["config_json"]
                    asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""
                    day_list = config_json["day_list"] if config_json.__contains__("day_list") else {}
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    act_module_dict = invoke_result_data.data["act_module_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                    task_count = TaskCount() if not task_count else task_count
                    if task_count.modify_day == now_day:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "今日已签到"
                    else:
                        task_count.id_md5 = task_count_id_md5
                        task_count.app_id = app_id
                        task_count.act_id = act_id
                        task_count.module_id = module_id
                        task_count.user_id = user_id
                        task_count.open_id = user_info_dict["open_id"]
                        task_count.task_type = task_type
                        task_count.task_sub_type = ""

                        if isinstance(day_list,list):
                            max_sign_day = max(query(day_list).select(lambda x: int(x["day"])).to_list())
                        else:
                            max_sign_day = int(max(day_list)) if len(day_list.keys()) > 0 else 0
                        if task_count.complete_count == max_sign_day:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = "任务已完成"
                        else:
                            task_count.complete_count = task_count.complete_count+1 if task_count.complete_count < max_sign_day else 1
                            task_count.now_count = 1
                            task_count.create_date = now_datetime
                            task_count.modify_date = now_datetime
                            task_count.modify_day = now_day
                            task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])
                            if isinstance(day_list,list):
                                cur_day = query(day_list).first_or_default(None,lambda x: int(x["day"]) == task_count.complete_count)
                                if cur_day:
                                    reward_value = int(cur_day["reward_value"])
                                else:
                                    reward_value = 0
                            else:
                                reward_value = int(day_list[str(task_count.complete_count)]) if day_list.__contains__(str(task_count.complete_count)) else 0
                            reward_object_id = asset_object_id
                            reward_name = config_json.get("reward_name","")
                            task_reward_type = config_json.get("reward_type", TaskRewardType.asset.value)
                            #奖励类型为资产走资产系统
                            if task_reward_type == TaskRewardType.asset.value:
                                only_id = self.get_only_id(user_id,3,task_type,complete_count=task_count.complete_count)
                                if module_id > 0:
                                    only_id = f"{module_id}_{only_id}"
                                asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                                reward_object_id = asset_type
                                asset_base_model = AssetBaseModel(context=self.context)
                                asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],f"签到{task_count.complete_count}天",only_id,handler_name,request_code,info_json=info_json)
                                if asset_invoke_result_data.success == False:
                                    reward_value = 0
                            invoke_result_data.data["reward_value"] = reward_value
                            invoke_result_data.data["config_json"] = config_json
                            self.add_task_stat(task_type,app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                            self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=f"签到{task_count.complete_count}天",reward_type=task_reward_type, reward_object_id=reward_object_id, reward_name=reward_name, reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            self.context.logging_link_error("【累计签到任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_invite_user(self,app_id,act_id,module_id,user_id,login_token,from_user_id,handler_name,check_user_nick=True,check_new_user=True,continue_request_expire=0,close_invite_limit=False,check_act_info_release=True,check_act_module_release=True):
        """
        :description: 处理邀请用户任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:当前用户标识
        :param login_token:访问令牌
        :param from_user_id:邀请人用户标识
        :param handler_name:接口名称
        :param check_user_nick:是否校验昵称为空
        :param check_new_user:是否校验新用户
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param close_invite_limit:是否关闭邀请限制 True是 False否
        :param check_act_info_release:校验活动信息是否发布
        :param check_act_module_release:校验活动模块是否发布
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_invite_user:{act_id}_{module_id}_{from_user_id}"
        task_type = TaskType.invite_new_user.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = InvokeResultData()
            if user_id == from_user_id:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "无效邀请"
                return invoke_result_data

            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name,check_act_info_release=check_act_info_release,check_act_module_release=check_act_module_release)
            if invoke_result_data.success == True:
                # act_info_dict = invoke_result_data.data["act_info_dict"]
                # act_module_dict = invoke_result_data.data["act_module_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]

                user_base_model = UserBaseModel(context=self.context)
                from_user_info_dict = user_base_model.get_user_info_dict(app_id,act_id,from_user_id)
                invite_log_model = InviteLogModel(context=self.context)
                invite_log_dict = invite_log_model.get_dict("act_id=%s and invite_user_id=%s", params=[act_id, user_id])
                if invite_log_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此用户已经被邀请过"
                elif not from_user_info_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "邀请人不存在"
                else:
                    task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                    if task_invoke_result_data.success == True:
                        task_info_dict = task_invoke_result_data.data
                        config_json = task_info_dict["config_json"]
                        limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                        satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                        task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                        task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",from_user_id)
                        task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                        acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                        if acquire_lock_status == False:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "acquire_lock"
                            invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                        else:
                            task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                            task_count = TaskCount() if not task_count else task_count
                            limit_meaasge = ""
                            if task_info_dict["complete_type"] == 1:
                                limit_meaasge = "今日邀请上限"
                                if task_count.modify_day != now_day:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            elif task_info_dict["complete_type"] == 2:
                                limit_meaasge = "每周邀请上限"
                                if TimeHelper.is_this_week(task_count.modify_date) == False:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            else:
                                limit_meaasge = "邀请上限"
                            invite_count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                            is_invite_limit = True if invite_count >= limit_num else False
                            if is_invite_limit == True and close_invite_limit == False:
                                invoke_result_data.success = False
                                invoke_result_data.error_code = "error"
                                invoke_result_data.error_message = limit_meaasge
                            else:
                                invite_log = InviteLog()
                                invite_log.app_id = app_id
                                invite_log.act_id = act_id
                                invite_log.user_id = from_user_id
                                invite_log.open_id = from_user_info_dict["open_id"]
                                invite_log.invite_user_id = user_info_dict["user_id"]
                                invite_log.invite_open_id = user_info_dict["open_id"]
                                invite_log.invite_user_nick = user_info_dict["user_nick"]
                                invite_log.invite_avatar = user_info_dict["avatar"]
                                invite_log.is_handle = 0
                                invite_log.create_date = now_datetime
                                invite_log.create_day = now_day
                                invite_log_model.add_entity(invite_log)

                                task_count.id_md5 = task_count_id_md5
                                task_count.app_id = app_id
                                task_count.act_id = act_id
                                task_count.module_id = module_id
                                task_count.user_id = from_user_id
                                task_count.open_id = from_user_info_dict["open_id"]
                                task_count.task_type = task_type
                                task_count.task_sub_type = ""
                                task_count.now_count = task_count.now_count + 1
                                task_count.create_date = now_datetime
                                task_count.modify_date = now_datetime
                                task_count.modify_day = now_day
                                task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])
                                invite_log_model.delete_dependency_key(DependencyKey.invite_log_list(act_id,from_user_id))
                    else:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = task_invoke_result_data.error_code
                        invoke_result_data.error_message = task_invoke_result_data.error_message

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【邀请新用户任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【邀请新用户任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name, task_count_identifier)

        return invoke_result_data

    def process_invite_join_member(self, app_id, act_id, module_id, user_id, login_token, from_user_id, handler_name, check_user_nick=True, continue_request_expire=0, close_invite_limit=False):
        """
        :description: 处理邀请加入会员任务,目前只支持淘宝会员体系
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:当前用户标识
        :param login_token:访问令牌
        :param from_user_id:邀请人用户标识
        :param handler_name:接口名称
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param close_invite_limit:是否关闭邀请限制 True是 False否
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_invite_join_member:{act_id}_{module_id}_{from_user_id}"
        task_type = TaskType.invite_join_member.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = InvokeResultData()
            if user_id == from_user_id:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "无效邀请"
                return invoke_result_data

            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)

            if invoke_result_data.success == True:
                # act_info_dict = invoke_result_data.data["act_info_dict"]
                # act_module_dict = invoke_result_data.data["act_module_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]

                user_base_model = UserBaseModel(context=self.context)
                from_user_info_dict = user_base_model.get_user_info_dict(app_id, act_id, from_user_id)
                invite_log_model = InviteLogModel(context=self.context,sub_table="member")
                invite_log_dict = invite_log_model.get_dict("act_id=%s and invite_user_id=%s", params=[act_id, user_id])
                if invite_log_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此用户已经被邀请过"
                elif not from_user_info_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "邀请人不存在"
                else:
                    task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                    if task_invoke_result_data.success == True:
                        task_info_dict = task_invoke_result_data.data
                        config_json = task_info_dict["config_json"]
                        limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                        satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                        task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                        task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",from_user_id)
                        task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                        acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                        if acquire_lock_status == False:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "acquire_lock"
                            invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                        else:
                            task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                            task_count = TaskCount() if not task_count else task_count
                            limit_meaasge = ""
                            if task_info_dict["complete_type"] == 1:
                                limit_meaasge = "今日邀请上限"
                                if task_count.modify_day != now_day:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            elif task_info_dict["complete_type"] == 2:
                                limit_meaasge = "每周邀请上限"
                                if TimeHelper.is_this_week(task_count.modify_date) == False:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            else:
                                limit_meaasge = "邀请上限"
                            invite_count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                            is_invite_limit = True if invite_count >= limit_num else False
                            if is_invite_limit == True and close_invite_limit == False:
                                invoke_result_data.success = False
                                invoke_result_data.error_code = "error"
                                invoke_result_data.error_message = limit_meaasge
                            else:

                                invite_log = InviteLog()
                                invite_log.app_id = app_id
                                invite_log.act_id = act_id
                                invite_log.user_id = from_user_id
                                invite_log.open_id = from_user_info_dict["open_id"]
                                invite_log.invite_user_id = user_info_dict["user_id"]
                                invite_log.invite_open_id = user_info_dict["open_id"]
                                invite_log.invite_user_nick = user_info_dict["user_nick"]
                                invite_log.invite_avatar = user_info_dict["avatar"]
                                invite_log.is_handle = 0
                                invite_log.create_date = now_datetime
                                invite_log.create_day = now_day
                                invite_log_model.add_entity(invite_log)

                                task_count.id_md5 = task_count_id_md5
                                task_count.app_id = app_id
                                task_count.act_id = act_id
                                task_count.module_id = module_id
                                task_count.user_id = from_user_id
                                task_count.open_id = from_user_info_dict["open_id"]
                                task_count.task_type = task_type
                                task_count.task_sub_type = ""
                                task_count.now_count = task_count.now_count + 1
                                task_count.create_date = now_datetime
                                task_count.modify_date = now_datetime
                                task_count.modify_day = now_day
                                task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])
                                invite_log_model.delete_dependency_key(DependencyKey.invite_log_member_list(act_id,from_user_id))
                    else:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = task_invoke_result_data.error_code
                        invoke_result_data.error_message = task_invoke_result_data.error_message

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【邀请加入会员任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【邀请加入会员任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name,task_count_identifier)

        return invoke_result_data

    def process_collect_goods(self,app_id,act_id,module_id,user_id,login_token,goods_id,handler_name,check_user_nick=True,continue_request_expire=0):
        """
        :description: 处理收藏商品任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param goods_id:收藏商品ID
        :param handler_name:接口名称
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_collect_goods:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.collect_goods.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                user_info_dict = invoke_result_data.data["user_info_dict"]
                collect_log_model = CollectLogModel(context=self.context)
                where = "act_id=%s and user_id=%s and goods_id=%s"
                params = [act_id, user_id, goods_id]
                collect_log_dict = collect_log_model.get_dict(where, params=params)
                if collect_log_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此商品已经收藏过"
                    return invoke_result_data
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
                    return invoke_result_data
                task_info_dict = task_invoke_result_data.data
                config_json = task_info_dict["config_json"]
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                goods_ids_list = list(set(str(config_json["goods_ids"]).split(','))) if config_json.__contains__("goods_ids") else []
                task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                if acquire_lock_status == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "acquire_lock"
                    invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                    return invoke_result_data
                task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                task_count = TaskCount() if not task_count else task_count
                limit_meaasge = ""
                if str(goods_id) not in goods_ids_list:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此商品不在收藏任务里"
                    return invoke_result_data
                if task_info_dict["complete_type"] == 1:
                    limit_meaasge = "今日收藏上限"
                    if task_count.modify_day != now_day:
                        task_count.complete_count = 0
                        task_count.now_count = 0
                elif task_info_dict["complete_type"] == 2:
                    limit_meaasge = "每周收藏上限"
                    if TimeHelper.is_this_week(task_count.modify_date) == False:
                        task_count.complete_count = 0
                        task_count.now_count = 0
                else:
                    limit_meaasge = "收藏上限"
                collect_count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                is_collect_limit = True if collect_count >= (limit_num * satisfy_num) else False
                if is_collect_limit == True:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = limit_meaasge
                else:
                    collect_log_model = CollectLogModel(context=self.context)
                    collect_log = CollectLog()
                    collect_log.app_id = app_id
                    collect_log.act_id = act_id
                    collect_log.user_id = user_id
                    collect_log.open_id = user_info_dict["open_id"]
                    collect_log.goods_id = goods_id
                    collect_log.is_handle = 0
                    collect_log.create_date = now_datetime
                    collect_log.create_day = now_day
                    collect_log_model.add_entity(collect_log)
                    collect_log_model.delete_dependency_key(DependencyKey.collect_log(act_id,user_id))

                    task_count.id_md5 = task_count_id_md5
                    task_count.app_id = app_id
                    task_count.act_id = act_id
                    task_count.module_id = module_id
                    task_count.user_id = user_id
                    task_count.open_id = user_info_dict["open_id"]
                    task_count.task_type = task_type
                    task_count.task_sub_type = ""
                    task_count.now_count = task_count.now_count + 1
                    task_count.create_date = now_datetime
                    task_count.modify_date = now_datetime
                    task_count.modify_day = now_day
                    task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【收藏商品任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【收藏商品任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name, task_count_identifier)

        return invoke_result_data

    def process_browse_goods(self,app_id,act_id,module_id,user_id,login_token,goods_id,handler_name,daily_repeat_browse=True,check_user_nick=True,continue_request_expire=0):
        """
        :description: 处理浏览商品任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param goods_id:浏览商品ID
        :param handler_name:接口名称
        :param daily_repeat_browse:单个商品可每日重复浏览 True是False否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_browse_goods:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.browse_goods.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                user_info_dict = invoke_result_data.data["user_info_dict"]
                browse_log_model = BrowseLogModel(context=self.context)
                where = "act_id=%s and user_id=%s and goods_id=%s"
                params = [act_id, user_id, goods_id]
                if daily_repeat_browse == True:
                    where+=" and create_day=%s"
                    params.append(TimeExHelper.get_now_day_int())
                browse_log_dict = browse_log_model.get_dict(where, params=params)
                if browse_log_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此商品已经浏览过"
                    return invoke_result_data
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
                    return invoke_result_data
                task_info_dict = task_invoke_result_data.data
                config_json = task_info_dict["config_json"]
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                goods_ids_list = list(set(str(config_json["goods_ids"]).split(','))) if config_json.__contains__("goods_ids") else []
                task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                if acquire_lock_status == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "acquire_lock"
                    invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                    return invoke_result_data
                task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                task_count = TaskCount() if not task_count else task_count
                limit_meaasge = ""
                if str(goods_id) not in goods_ids_list:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此商品不在浏览任务里"
                    return invoke_result_data
                if task_info_dict["complete_type"] == 1:
                    limit_meaasge = "今日浏览上限"
                    if task_count.modify_day != now_day:
                        task_count.complete_count = 0
                        task_count.now_count = 0
                elif task_info_dict["complete_type"] == 2:
                    limit_meaasge = "每周浏览上限"
                    if TimeHelper.is_this_week(task_count.modify_date) == False:
                        task_count.complete_count = 0
                        task_count.now_count = 0
                else:
                    limit_meaasge = "浏览上限"
                browse_count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                is_browse_limit = True if browse_count >= (limit_num * satisfy_num) else False
                if is_browse_limit == True:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = limit_meaasge
                else:
                    browse_log_model = BrowseLogModel(context=self.context)
                    browse_log = BrowseLog()
                    browse_log.app_id = app_id
                    browse_log.act_id = act_id
                    browse_log.user_id = user_id
                    browse_log.open_id = user_info_dict["open_id"]
                    browse_log.goods_id = goods_id
                    browse_log.is_handle = 0
                    browse_log.create_date = now_datetime
                    browse_log.create_day = now_day
                    browse_log_model.add_entity(browse_log)
                    browse_log_model.delete_dependency_key(DependencyKey.browse_log(act_id,user_id))

                    task_count.id_md5 = task_count_id_md5
                    task_count.app_id = app_id
                    task_count.act_id = act_id
                    task_count.module_id = module_id
                    task_count.user_id = user_id
                    task_count.open_id = user_info_dict["open_id"]
                    task_count.task_type = task_type
                    task_count.task_sub_type = ""
                    task_count.now_count = task_count.now_count + 1
                    task_count.create_date = now_datetime
                    task_count.modify_date = now_datetime
                    task_count.modify_day = now_day
                    task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【浏览商品任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【浏览商品任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name,task_count_identifier)

        return invoke_result_data

    def process_favor_store(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None):
        """
        :description: 处理关注店铺,有任务给奖励，没有则直接关注
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_favor_store:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.favor_store.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        stat_base_model = StatBaseModel(context=self.context)
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                act_info_dict = invoke_result_data.data["act_info_dict"]
                act_module_dict = invoke_result_data.data["act_module_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]

                if user_info_dict["is_favor_before"] == 0:
                    if is_stat == True:
                        #新增关注用户数
                        stat_base_model.add_stat(app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], "AddFollowUserCount",1)
                is_limit = False
                task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_type,"",user_id)
                task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                task_count = task_count if task_count else TaskCount()
                if module_id:
                    is_limit = True if task_count.complete_count >= 1 else False
                else:
                    is_limit = True if task_count.complete_count >= 1 or user_info_dict["is_favor"] == 1 else False
                if is_limit == True:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "已经关注过店铺了"
                else:
                    user_info_model = UserInfoModel(context=self.context).set_sub_table(app_id)
                    user_info_model.update_table("is_favor=1","id=%s",params=[user_info_dict["id"]])
                    UserBaseModel(context=self.context)._delete_user_info_cache(user_info_dict["act_id"],user_info_dict["id_md5"])
                    reward_value = 0
                    reward_object_id =""
                    task_info_dict = {"task_name":"关注店铺"}
                    task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                    if task_invoke_result_data.success == True:
                        task_info_dict = task_invoke_result_data.data
                        config_json = task_info_dict["config_json"]
                        reward_value = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0
                        once_favor_reward = int(config_json["once_favor_reward"]) if config_json.__contains__("once_favor_reward") else 1
                        asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""

                        task_count.id_md5 = task_count_id_md5
                        task_count.app_id = app_id
                        task_count.act_id = act_id
                        task_count.module_id = module_id
                        task_count.user_id = user_id
                        task_count.open_id = user_info_dict["open_id"]
                        task_count.task_type = task_type
                        task_count.task_sub_type = ""
                        task_count.complete_count = task_count.complete_count+1
                        task_count.now_count = 0
                        task_count.create_date = now_datetime
                        task_count.modify_date = now_datetime
                        task_count.modify_day = now_day
                        task_count_model.add_update_entity(task_count,"complete_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.modify_date,now_day])

                        if user_info_dict["is_favor_before"] == 1 and once_favor_reward == 0:
                            reward_value = 0
                        if reward_value > 0:
                            only_id = self.get_only_id(user_id,task_info_dict["complete_type"],task_type)
                            if module_id > 0:
                                only_id = f"{module_id}_{only_id}"
                            asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                            reward_object_id = asset_type
                            asset_base_model = AssetBaseModel(context=self.context)
                            asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],task_info_dict["task_name"],only_id,handler_name,request_code,info_json=info_json)
                            if asset_invoke_result_data.success == False:
                                reward_value = 0
                    invoke_result_data.data["reward_value"] = reward_value
                    self.add_task_stat(task_type, app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                    self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=task_info_dict["task_name"],reward_type=1, reward_object_id=reward_object_id, reward_name="", reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【关注店铺】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【关注店铺】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_join_member(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None):
        """
        :description: 处理加入店铺会员,有任务给奖励，没有则直接加入
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_join_member:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.join_member.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        stat_base_model = StatBaseModel(context=self.context)
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                act_info_dict = invoke_result_data.data["act_info_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]

                if user_info_dict["is_member_before"] == 0:
                    #新增入会用户数
                    if is_stat == True:
                        stat_base_model.add_stat(app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], "AddMemberUserCount",1)
                is_limit = False
                task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_type,"",user_id)
                task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                task_count = task_count if task_count else TaskCount()
                if module_id:
                    is_limit = True if task_count.complete_count >= 1 else False
                else:
                    is_limit = True if task_count.complete_count >= 1 or user_info_dict["is_member"] == 1 else False
                if is_limit == True:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "已经完成入会任务"
                else:
                    user_info_model = UserInfoModel(context=self.context).set_sub_table(app_id)
                    user_info_model.update_table("is_member=1","id=%s",params=[user_info_dict["id"]])
                    UserBaseModel(context=self.context)._delete_user_info_cache(user_info_dict["act_id"],user_info_dict["id_md5"])
                    reward_value = 0
                    reward_object_id = ""
                    task_info_dict = {"task_name":"加入店铺会员"}
                    task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                    if task_invoke_result_data.success == True:
                        task_info_dict = task_invoke_result_data.data
                        config_json = task_info_dict["config_json"]
                        reward_value = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0
                        once_member_reward = int(config_json["once_member_reward"]) if config_json.__contains__("once_member_reward") else 1
                        asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""

                        task_count.id_md5 = task_count_id_md5
                        task_count.app_id = app_id
                        task_count.act_id = act_id
                        task_count.module_id = module_id
                        task_count.user_id = user_id
                        task_count.open_id = user_info_dict["open_id"]
                        task_count.task_type = task_type
                        task_count.task_sub_type = ""
                        task_count.complete_count = task_count.complete_count+1
                        task_count.now_count = 0
                        task_count.create_date = now_datetime
                        task_count.modify_date = now_datetime
                        task_count.modify_day = now_day
                        task_count_model.add_update_entity(task_count,"complete_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.modify_date,now_day])

                        if user_info_dict["is_member_before"] == 1 and once_member_reward == 0: #判断已经入会是否给奖励
                            reward_value = 0
                        if reward_value > 0:
                            only_id = self.get_only_id(user_id,task_info_dict["complete_type"],task_type)
                            if module_id > 0:
                                only_id = f"{module_id}_{only_id}"
                            asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                            reward_object_id = asset_type
                            asset_base_model = AssetBaseModel(context=self.context)
                            asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],task_info_dict["task_name"],only_id,handler_name,request_code,info_json=info_json)
                            if asset_invoke_result_data.success == False:
                                reward_value = 0
                    invoke_result_data.data["reward_value"] = reward_value
                    self.add_task_stat(task_type, app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                    self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=task_info_dict["task_name"],reward_type=1, reward_object_id=reward_object_id, reward_name="", reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【加入店铺会员】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【加入店铺会员】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_browse_site(self,app_id,act_id,module_id,user_id,login_token,task_type,task_sub_type,handler_name,check_user_nick=True,continue_request_expire=0):
        """
        :description: 处理浏览网址任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param task_type:任务类型
        :param task_sub_type:子任务类型
        :param handler_name:接口名称
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_browse_site:{act_id}_{module_id}_{user_id}_{task_type}"
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                act_info_dict = invoke_result_data.data["act_info_dict"]
                act_module_dict = invoke_result_data.data["act_module_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]

                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    sub_config_json = [sub_config_json for sub_config_json in task_info_dict["config_json"] if task_sub_type == sub_config_json["id"]]
                    if sub_config_json:
                        limit_num = int(sub_config_json["limit_num"]) if sub_config_json.__contains__("limit_num") else 1
                        satisfy_num = int(sub_config_json["satisfy_num"]) if sub_config_json.__contains__("satisfy_num") else 1
                        task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                        task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],task_sub_type,user_id)
                        task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                        acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                        if acquire_lock_status == False:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "acquire_lock"
                            invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                        else:
                            task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                            task_count = TaskCount() if not task_count else task_count
                            limit_meaasge = ""
                            if task_info_dict["complete_type"] == 1:
                                limit_meaasge = "今日浏览上限"
                                if task_count.modify_day != now_day:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            elif task_info_dict["complete_type"] == 2:
                                limit_meaasge = "每周浏览上限"
                                if TimeHelper.is_this_week(task_count.modify_date) == False:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            else:
                                limit_meaasge = "浏览上限"

                            count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                            is_limit = True if count >= (limit_num * satisfy_num) else False
                            if is_limit == True:
                                invoke_result_data.success = False
                                invoke_result_data.error_code = "error"
                                invoke_result_data.error_message = limit_meaasge
                            else:
                                task_count.id_md5 = task_count_id_md5
                                task_count.app_id = app_id
                                task_count.act_id = act_id
                                task_count.module_id = module_id
                                task_count.user_id = user_id
                                task_count.open_id = user_info_dict["open_id"]
                                task_count.task_type = task_type
                                task_count.task_sub_type = task_sub_type
                                task_count.now_count = task_count.now_count + 1
                                task_count.create_date = now_datetime
                                task_count.modify_date = now_datetime
                                task_count.modify_day = now_day
                                task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count, task_count.now_count, task_count.modify_date, now_day])
                    else:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "子任务不存在"
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【浏览网址任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【浏览网址任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name, task_count_identifier)

        return invoke_result_data

    def process_share(self,app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user=False,check_user_nick=True,continue_request_expire=0):
        """
        :description: 处理分享奖励任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_share:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.share.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = task_info_dict["config_json"]
                    limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                    acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                    if acquire_lock_status == False:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "acquire_lock"
                        invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                    else:
                        task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                        task_count = TaskCount() if not task_count else task_count
                        limit_meaasge = ""
                        if task_info_dict["complete_type"] == 1:
                            limit_meaasge = "今日领取上限"
                            if task_count.modify_day != now_day:
                                task_count.complete_count = 0
                                task_count.now_count = 0
                        elif task_info_dict["complete_type"] == 2:
                            limit_meaasge = "每周领取上限"
                            if TimeHelper.is_this_week(task_count.modify_date) == False:
                                task_count.complete_count = 0
                                task_count.now_count = 0
                        else:
                            limit_meaasge = "领取上限"
                        is_limit = True if task_count.complete_count >= limit_num else False
                        if is_limit == True:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = limit_meaasge
                        else:
                            task_count.id_md5 = task_count_id_md5
                            task_count.app_id = app_id
                            task_count.act_id = act_id
                            task_count.module_id = module_id
                            task_count.user_id = user_id
                            task_count.open_id = user_info_dict["open_id"]
                            task_count.task_type = task_type
                            task_count.task_sub_type = ""
                            task_count.now_count = task_count.now_count + 1
                            task_count.create_date = now_datetime
                            task_count.modify_date = now_datetime
                            task_count.modify_day = now_day
                            task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【分享任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【分享任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name,task_count_identifier)

        return invoke_result_data

    def process_invite_user_help(self,app_id,act_id,module_id,user_id,login_token,from_user_id,handler_name,check_new_user=False,check_user_nick=True,continue_request_expire=0,check_act_info_release=True,check_act_module_release=True):
        """
        :description: 处理邀请用户助力
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:当前用户标识
        :param login_token:访问令牌
        :param from_user_id:邀请人用户标识
        :param handler_name:接口名称
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param check_act_info_release:校验活动信息是否发布
        :param check_act_module_release:校验活动模块是否发布
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_invite_user_help:{act_id}_{module_id}_{from_user_id}"
        task_type = TaskType.invite_user_help.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = InvokeResultData()
            if user_id == from_user_id:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "无效邀请"
                return invoke_result_data

            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name,check_act_info_release=check_act_info_release,check_act_module_release=check_act_module_release)
            if invoke_result_data.success == True:
                user_info_dict = invoke_result_data.data["user_info_dict"]

                user_base_model = UserBaseModel(context=self.context)
                from_user_info_dict = user_base_model.get_user_info_dict(app_id,act_id,from_user_id)
                invite_help_model = InviteHelpModel(context=self.context)
                help_type = 1
                help_object_id = ''
                help_id_md5 = CryptoHelper.md5_encrypt_int(f"{app_id}_{act_id}_{module_id}_{help_type}_{help_object_id}")
                invite_help_dict = invite_help_model.get_dict("id_md5=%s and user_id=%s and invited_user_id=%s", params=[help_id_md5, from_user_id, user_id])
                if invite_help_dict:
                    error_message = "您已助力过了"
                    if from_user_info_dict and from_user_info_dict["user_nick_encrypt"]:
                        error_message = f"您已帮【{CryptographyHelper.base64_decrypt(from_user_info_dict['user_nick_encrypt'])}】助力过了~请勿重复助力"
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = error_message
                elif not from_user_info_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "邀请人不存在"
                else:
                    task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                    if task_invoke_result_data.success == True:
                        task_info_dict = task_invoke_result_data.data
                        config_json = task_info_dict["config_json"]
                        limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                        satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                        task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                        task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",from_user_id)
                        task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                        acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                        if acquire_lock_status == False:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "acquire_lock"
                            invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                        else:
                            task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                            task_count = TaskCount() if not task_count else task_count
                            limit_meaasge = ""
                            if task_info_dict["complete_type"] == 1:
                                limit_meaasge = "今日邀请上限"
                                if task_count.modify_day != now_day:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            elif task_info_dict["complete_type"] == 2:
                                limit_meaasge = "每周邀请上限"
                                if TimeHelper.is_this_week(task_count.modify_date) == False:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            else:
                                limit_meaasge = "邀请上限"
                            invite_count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                            is_invite_limit = True if invite_count >= limit_num else False
                            if is_invite_limit == True:
                                invoke_result_data.success = False
                                invoke_result_data.error_code = "error"
                                invoke_result_data.error_message = limit_meaasge
                            else:
                                invite_help = InviteHelp()
                                invite_help.id_md5 = help_id_md5
                                invite_help.app_id = app_id
                                invite_help.act_id = act_id
                                invite_help.module_id = module_id
                                invite_help.help_type = 1
                                invite_help.object_id = ''
                                invite_help.user_id = from_user_id
                                invite_help.open_id = from_user_info_dict["open_id"]
                                invite_help.invited_user_id = user_info_dict["user_id"]
                                invite_help.invited_open_id = user_info_dict["open_id"]
                                invite_help.invited_user_nick = user_info_dict["user_nick"]
                                invite_help.invited_avatar = user_info_dict["avatar"]
                                invite_help.is_handle = 0
                                invite_help.create_date = now_datetime
                                invite_help.create_day = now_day
                                invite_help_model.add_entity(invite_help)

                                task_count.id_md5 = task_count_id_md5
                                task_count.app_id = app_id
                                task_count.act_id = act_id
                                task_count.module_id = module_id
                                task_count.user_id = from_user_id
                                task_count.open_id = from_user_info_dict["open_id"]
                                task_count.task_type = task_type
                                task_count.task_sub_type = ""
                                task_count.now_count = task_count.now_count + 1
                                task_count.create_date = now_datetime
                                task_count.modify_date = now_datetime
                                task_count.modify_day = now_day
                                task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])
                                invite_help_model.delete_dependency_key(DependencyKey.invite_user_help_list(help_id_md5,from_user_id))
                    else:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = task_invoke_result_data.error_code
                        invoke_result_data.error_message = task_invoke_result_data.error_message

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【邀请用户助力任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【邀请用户助力任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name,task_count_identifier)

        return invoke_result_data

    def process_secret_code(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,secret_code,check_new_user=False,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None):
        """
        :description: 处理神秘暗号任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param secret_code:暗号
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_secret_code:{act_id}_{module_id}_{user_id}"
        task_type = TaskType.secret_code.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = task_info_dict["config_json"]
                    reward_value = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0
                    asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""
                    limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                    cur_secret_code = config_json["secret_code"] if config_json.__contains__("secret_code") else ''
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                    task_count = TaskCount() if not task_count else task_count
                    limit_meaasge = ""

                    if task_info_dict["complete_type"] == 1:
                        limit_meaasge = "今日领取上限"
                        if task_count.modify_day != now_day:
                            task_count.complete_count = 0
                            task_count.now_count = 0
                    elif task_info_dict["complete_type"] == 2:
                        limit_meaasge = "每周领取上限"
                        if TimeHelper.is_this_week(task_count.modify_date) == False:
                            task_count.complete_count = 0
                            task_count.now_count = 0
                    else:
                        limit_meaasge = "领取上限"
                    is_limit = True if task_count.complete_count >= limit_num else False
                    if is_limit == True:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = limit_meaasge
                    elif cur_secret_code != secret_code:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "暗号不正确"
                    else:
                        task_count.id_md5 = task_count_id_md5
                        task_count.app_id = app_id
                        task_count.act_id = act_id
                        task_count.module_id = module_id
                        task_count.user_id = user_id
                        task_count.open_id = user_info_dict["open_id"]
                        task_count.task_type = task_type
                        task_count.task_sub_type = ""
                        task_count.complete_count = task_count.complete_count+1
                        task_count.now_count = 0
                        task_count.create_date = now_datetime
                        task_count.modify_date = now_datetime
                        task_count.modify_day = now_day
                        task_count_model.add_update_entity(task_count,"complete_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.modify_date,now_day])
                        reward_object_id = ""
                        if reward_value > 0:
                            only_id = self.get_only_id(user_id,task_info_dict["complete_type"],task_type,complete_count=task_count.complete_count)
                            if module_id > 0:
                                only_id = f"{module_id}_{only_id}"
                            asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                            reward_object_id = asset_type
                            asset_base_model = AssetBaseModel(context=self.context)
                            asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],task_info_dict["task_name"],only_id,handler_name,request_code,info_json=info_json)
                            if asset_invoke_result_data.success == False:
                                reward_value = 0
                        invoke_result_data.data["reward_value"] = reward_value
                        self.add_task_stat(task_type, app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                        self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=task_info_dict["task_name"],reward_type=1, reward_object_id=reward_object_id, reward_name="", reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)

                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【神秘暗号任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【神秘暗号任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_crm_point_exchange_asset(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_code,mix_nick,access_token,app_key,app_secret,check_new_user=False,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None):
        """
        :description: 处理店铺会员积分兑换资产
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_code:请求代码
        :param mix_nick:mix_nick
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_crm_point_exchange_asset:{act_id}_{module_id}_{user_id}"

        task_type = TaskType.crm_point_exchange_asset.value
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        if not info_json:
            info_json = {}
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
                    return invoke_result_data
                task_info_dict = task_invoke_result_data.data
                config_json = task_info_dict["config_json"]
                reward_value = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0
                asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""
                limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                need_crm_point = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 0
                act_info_dict = invoke_result_data.data["act_info_dict"]
                user_info_dict = invoke_result_data.data["user_info_dict"]
                task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                task_count = TaskCount() if not task_count else task_count
                limit_meaasge = ""
                top_base_model = TopBaseModel(context=self.context)
                if task_info_dict["complete_type"] == 1:
                    limit_meaasge = "今日领取上限"
                    if task_count.modify_day != now_day:
                        task_count.complete_count = 0
                        task_count.now_count = 0
                elif task_info_dict["complete_type"] == 2:
                    limit_meaasge = "每周领取上限"
                    if TimeHelper.is_this_week(task_count.modify_date) == False:
                        task_count.complete_count = 0
                        task_count.now_count = 0
                else:
                    limit_meaasge = "领取上限"
                is_limit = True if task_count.complete_count >= limit_num else False
                if is_limit == True:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = limit_meaasge
                    return invoke_result_data
                if not need_crm_point:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "配置异常无法兑换"
                    return invoke_result_data
                if reward_value <= 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "配置异常无法兑换"
                    return invoke_result_data
                member_invoke_result_data = top_base_model.get_crm_point_available(mix_nick, access_token, app_key, app_secret, False, user_info_dict["open_id"])
                if member_invoke_result_data.success == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "member_error"
                    invoke_result_data.error_message = "获取会员积分失败"
                    return invoke_result_data
                elif member_invoke_result_data.data < need_crm_point:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "member_error"
                    invoke_result_data.error_message = f"会员积分不足，当前只有{member_invoke_result_data.data}积分"
                    return invoke_result_data
                crm_point_invoke_result_data = top_base_model.change_crm_point(user_info_dict["open_id"], mix_nick, 1, 1, need_crm_point, access_token, app_key, app_secret, 0, "", True)
                if crm_point_invoke_result_data.success == False:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = crm_point_invoke_result_data.error_code
                    invoke_result_data.error_message = crm_point_invoke_result_data.error_message
                    return invoke_result_data
                task_count.id_md5 = task_count_id_md5
                task_count.app_id = app_id
                task_count.act_id = act_id
                task_count.module_id = module_id
                task_count.user_id = user_id
                task_count.open_id = user_info_dict["open_id"]
                task_count.task_type = task_type
                task_count.task_sub_type = ""
                task_count.complete_count = task_count.complete_count+1
                task_count.now_count = 0
                task_count.create_date = now_datetime
                task_count.modify_date = now_datetime
                task_count.modify_day = now_day
                task_count_model.add_update_entity(task_count,"complete_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.modify_date,now_day])
                only_id = self.get_only_id(user_id,task_info_dict["complete_type"],task_type,complete_count=task_count.complete_count)
                if module_id > 0:
                    only_id = f"{module_id}_{only_id}"
                asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                reward_object_id = asset_type
                asset_base_model = AssetBaseModel(context=self.context)
                asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_type,task_info_dict["task_name"],task_info_dict["task_name"],only_id,handler_name,request_code,info_json=info_json)
                if asset_invoke_result_data.success == False:
                    reward_value = 0
                invoke_result_data.data["need_crm_point"] = need_crm_point
                invoke_result_data.data["reward_value"] = reward_value
                self.add_task_stat(task_type, app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat)
                self.add_task_log(task_type=task_type, task_sub_type='', app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=task_info_dict["task_name"],reward_type=1, reward_object_id=reward_object_id, reward_name="", reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【店铺会员积分兑换资产任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【店铺会员积分兑换资产任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
        return invoke_result_data

    def process_routine_task(self,app_id,act_id,module_id,user_id,login_token,handler_name,task_type,task_sub_type,check_new_user=False,check_user_nick=True,continue_request_expire=0):
        """
        :description: 处理常规任务 只计数不领取奖励
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param task_type:任务类型
        :param task_sub_type:子任务类型，没有传空
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_routine_task:{act_id}_{module_id}_{user_id}_{task_type}"
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                user_info_dict = invoke_result_data.data["user_info_dict"]
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    task_count_invoke_result_data = self.add_task_count(app_id, act_id, module_id, user_id, user_info_dict["open_id"], task_type, 1, task_info_dict, task_sub_type)
                    if task_count_invoke_result_data.success == False:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = task_count_invoke_result_data.error_code
                        invoke_result_data.error_message = task_count_invoke_result_data.error_message
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【通用任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【通用任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"

        self.business_process_executed()

        return invoke_result_data

    def process_routine_invite_task(self,task_type,invite_sub_table,app_id,act_id,module_id,user_id,login_token,from_user_id,handler_name,check_new_user=True,check_user_nick=True,continue_request_expire=0,close_invite_limit=False):
        """
        :description: 处理常规邀请任务(当一个活动有多个邀请任务时，可以使用当前方法)
        :param task_type:任务类型
        :param invite_sub_table:分表名
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:当前用户标识
        :param login_token:访问令牌
        :param from_user_id:邀请人用户标识
        :param handler_name:接口名称
        :param check_new_user:是否校验新用户
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param close_invite_limit:是否关闭邀请限制 True是(老用户也可以邀请成功) False否
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        acquire_lock_name = f"process_routine_invite_task:{act_id}_{module_id}_{from_user_id}_{task_type}"
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = InvokeResultData()
            if user_id == from_user_id:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "无效邀请"
                return invoke_result_data

            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                user_info_dict = invoke_result_data.data["user_info_dict"]
                user_base_model = UserBaseModel(context=self.context)
                from_user_info_dict = user_base_model.get_user_info_dict(app_id,act_id,from_user_id)
                invite_log_model = InviteLogModel(context=self.context,sub_table=invite_sub_table)
                is_invite = invite_log_model.get_total("act_id=%s and invite_user_id=%s", params=[act_id, user_id])
                if is_invite > 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "此用户已经被邀请过"
                elif not from_user_info_dict:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "邀请人不存在"
                else:
                    task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                    if task_invoke_result_data.success == True:
                        task_info_dict = task_invoke_result_data.data
                        config_json = task_info_dict["config_json"]
                        limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                        satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                        task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                        task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",from_user_id)
                        task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                        acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                        if acquire_lock_status == False:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "acquire_lock"
                            invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                        else:
                            task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                            task_count = TaskCount() if not task_count else task_count
                            limit_meaasge = ""
                            if task_info_dict["complete_type"] == TaskCompleteType.day.value:
                                limit_meaasge = "今日邀请上限"
                                if task_count.modify_day != now_day:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            elif task_info_dict["complete_type"] == TaskCompleteType.week.value:
                                limit_meaasge = "每周邀请上限"
                                if TimeHelper.is_this_week(task_count.modify_date) == False:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            elif task_info_dict["complete_type"] == TaskCompleteType.month.value:
                                limit_meaasge = "每月邀请上限"
                                if TimeHelper.is_this_month(task_count.modify_date) == False:
                                    task_count.complete_count = 0
                                    task_count.now_count = 0
                            else:
                                limit_meaasge = "邀请上限"
                            invite_count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                            is_invite_limit = True if invite_count >= limit_num else False
                            if is_invite_limit == True and close_invite_limit == False:
                                invoke_result_data.success = False
                                invoke_result_data.error_code = "error"
                                invoke_result_data.error_message = limit_meaasge
                            else:
                                invite_log = InviteLog()
                                invite_log.app_id = app_id
                                invite_log.act_id = act_id
                                invite_log.user_id = from_user_id
                                invite_log.open_id = from_user_info_dict["open_id"]
                                invite_log.invite_user_id = user_info_dict["user_id"]
                                invite_log.invite_open_id = user_info_dict["open_id"]
                                invite_log.invite_user_nick = user_info_dict["user_nick"]
                                invite_log.invite_avatar = user_info_dict["avatar"]
                                invite_log.is_handle = 0
                                invite_log.create_date = now_datetime
                                invite_log.create_day = now_day
                                invite_log_model.add_entity(invite_log)

                                task_count.id_md5 = task_count_id_md5
                                task_count.app_id = app_id
                                task_count.act_id = act_id
                                task_count.module_id = module_id
                                task_count.user_id = from_user_id
                                task_count.open_id = from_user_info_dict["open_id"]
                                task_count.task_type = task_type
                                task_count.task_sub_type = ""
                                task_count.now_count = task_count.now_count + 1
                                task_count.create_date = now_datetime
                                task_count.modify_date = now_datetime
                                task_count.modify_day = now_day
                                task_count_model.add_update_entity(task_count,"complete_count=%s,now_count=%s,modify_date=%s,modify_day=%s",params=[task_count.complete_count,task_count.now_count,task_count.modify_date,now_day])
                    else:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = task_invoke_result_data.error_code
                        invoke_result_data.error_message = task_invoke_result_data.error_message

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【处理常规邀请任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【处理常规邀请任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name, task_count_identifier)

        return invoke_result_data

    def process_buy_appoint_goods_task(self,app_id,act_id,module_id,user_id,login_token,handler_name,order_data=[],app_key="",app_secret="",is_log=False,check_user_nick=True,continue_request_expire=0,is_stat=True,support_presale_order=False):
        """
        :description: 购买指定商品任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param order_data:订单数据
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log:是否记录top请求日志
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param support_presale_order:是否支持预售订单
        :return 
        :last_editors: HuangJianYi
        """
        task_type = TaskType.buy_appoint_goods.value
        acquire_lock_name = f"process_buy_appoint_goods_task:{act_id}_{module_id}_{user_id}"
        now_day = TimeExHelper.get_now_day_int()
        now_datetime = TimeHelper.get_now_format_time()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,False,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = task_info_dict["config_json"]
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    act_module_dict = invoke_result_data.data["act_module_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    goods_ids_list = list(set(str(config_json["goods_ids"]).split(','))) if config_json.__contains__("goods_ids") else []
                    limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                    satisfy_num = int(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                    task_count_model = TaskCountModel(context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                    acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                    if acquire_lock_status == False:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "acquire_lock"
                        invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                    else:
                        task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                        task_count = TaskCount() if not task_count else task_count
                        limit_meaasge = ""
                        if task_info_dict["complete_type"] == 1:
                            limit_meaasge = "今日购买上限"
                            if task_count.modify_day != now_day:
                                task_count.complete_count = 0
                                task_count.now_count = 0
                                task_count.remark = ""
                        elif task_info_dict["complete_type"] == 2:
                            limit_meaasge = "每周购买上限"
                            if TimeHelper.is_this_week(task_count.modify_date) == False:
                                task_count.complete_count = 0
                                task_count.now_count = 0
                                task_count.remark = ""
                        else:
                            limit_meaasge = "购买上限"
                        buy_count = int(task_count.complete_count * satisfy_num) + task_count.now_count
                        is_buy_limit = True if buy_count >= (limit_num * satisfy_num) else False
                        if is_buy_limit == True:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = limit_meaasge
                        else:
                            app_info_dict = AppBaseModel(context=self.context).get_app_info_dict(app_id=app_id,is_cache=True,field="access_token")
                            access_token = app_info_dict["access_token"] if app_info_dict else ""
                            top_base_model = TopBaseModel(context=self.context)
                            if len(order_data) <= 0:
                                start_date = act_info_dict['start_date']
                                start_date = act_module_dict['start_date'] if act_module_dict and act_module_dict['start_date'] else start_date
                                if start_date and start_date != '1900-01-01 00:00:00':
                                    invoke_result_data = top_base_model.get_buy_order_list(user_info_dict["open_id"], access_token, app_key, app_secret, start_date, is_log=is_log)
                                    if invoke_result_data.success == True:
                                        order_data = invoke_result_data.data
                                else:
                                    invoke_result_data = top_base_model.get_buy_order_list(user_info_dict["open_id"], access_token, app_key, app_secret, is_log=is_log)
                                    if invoke_result_data.success == True:
                                        order_data = invoke_result_data.data
                            if len(order_data) > 0:
                                invoke_result_data.data = {}
                                order_base_model = OrderBaseModel(context=self.context)
                                pay_order_no_list, redis_init, pay_order_cache_key = order_base_model._get_tao_pay_order_no_list(app_id,user_id)

                                #满足奖励条件的订单
                                reward_order_list = []
                                for item in order_data:
                                    for order in item["orders"]["order"]:
                                        if str(order["num_iid"]) in goods_ids_list:
                                            order["step_paid_fee"] = item["step_paid_fee"] if "step_paid_fee" in item.keys() else 0
                                            order["type"] = item["type"]
                                            if "pay_time" in item:
                                                order["pay_time"] = item["pay_time"]
                                                order["tid"] = item["tid"]
                                            if support_presale_order == True:
                                                if order["status"] in self.rewards_status() or (order["type"] == "step" and order["step_trade_status"] != "FRONT_NOPAID_FINAL_NOPAID"):
                                                    reward_order_list.append(order)
                                            else:
                                                if order["status"] in self.rewards_status():
                                                    reward_order_list.append(order)

                                pay_price = 0 #总支付金额
                                pay_num = 0  #总支付笔数
                                buy_num = 0  #总购买数量
                                appoint_goods_id_list = [] #购买指定商品ID集合
                                tao_pay_order_list = []

                                for order in reward_order_list:
                                    try:
                                        #判断是否已经统计过
                                        if order["oid"] not in pay_order_no_list:
                                            appoint_goods_id_list.append(str(order["num_iid"]))
                                            tao_pay_order = TaoPayOrder()
                                            tao_pay_order.app_id = app_id
                                            tao_pay_order.act_id = act_id
                                            tao_pay_order.ascription_type = 2
                                            tao_pay_order.user_id = user_id
                                            tao_pay_order.open_id = user_info_dict["open_id"]
                                            tao_pay_order.user_nick = user_info_dict["user_nick"]
                                            tao_pay_order.main_pay_order_no = order['tid']
                                            tao_pay_order.sub_pay_order_no = order['oid']
                                            tao_pay_order.goods_code = order['num_iid']
                                            tao_pay_order.goods_name = order['title']
                                            if "sku_id" in order.keys():
                                                tao_pay_order.sku_id = order['sku_id']
                                                sku_invoke_result_data = top_base_model.get_sku_name(int(order['num_iid']), int(order['sku_id']), access_token, app_key, app_secret,is_log)
                                                tao_pay_order.sku_name = sku_invoke_result_data.data if sku_invoke_result_data.success == True else ""
                                            tao_pay_order.buy_num = order['num']
                                            tao_pay_order.pay_price = order['payment']
                                            tao_pay_order.order_status = order['status']
                                            tao_pay_order.create_date = SevenHelper.get_now_datetime()
                                            tao_pay_order.pay_date = order['pay_time']
                                            tao_pay_order_list.append(tao_pay_order)
                                            if support_presale_order == True:
                                                payment = decimal.Decimal(order["step_paid_fee"]) if order["type"] == "step" and decimal.Decimal(order["step_paid_fee"]) > 0 else decimal.Decimal(order["payment"])
                                            else:
                                                payment = decimal.Decimal(order["payment"])
                                            pay_price = decimal.Decimal(pay_price) + payment
                                            pay_num = pay_num + 1
                                            buy_num = buy_num + order['num']
                                    except Exception as ex:
                                        if self.context:
                                            self.context.logging_link_info(str(order) + "【购买指定商品任务】" + traceback.format_exc())
                                        elif self.logging_link_info:
                                            self.logging_link_info(str(order) + "【购买指定商品任务】" + traceback.format_exc())
                                        continue
                                if len(tao_pay_order_list) > 0:
                                    task_count.id_md5 = task_count_id_md5
                                    task_count.app_id = app_id
                                    task_count.act_id = act_id
                                    task_count.module_id = module_id
                                    task_count.user_id = user_id
                                    task_count.open_id = user_info_dict["open_id"]
                                    task_count.task_type = task_type
                                    task_count.now_count = task_count.now_count + pay_num
                                    task_count.create_date = now_datetime
                                    task_count.modify_date = now_datetime
                                    task_count.modify_day = now_day
                                    remark = SevenHelper.json_loads(task_count.remark) if task_count.remark else {"goods_id_list":[]}
                                    remark["goods_id_list"].extend(appoint_goods_id_list)
                                    task_count.remark = SevenHelper.json_dumps(remark)
                                    TaoPayOrderModel(context=self.context).add_list(tao_pay_order_list)
                                    task_count_model.add_update_entity(task_count,"complete_count=%s,modify_date=%s,modify_day=%s,remark=%s",params=[task_count.complete_count,task_count.modify_date,now_day,task_count.remark])
                                    for item in tao_pay_order_list:
                                        redis_init.lpush(pay_order_cache_key,item.sub_pay_order_no)
                                        redis_init.expire(pay_order_cache_key, 30 * 24 * 3600)

                                    invoke_result_data.data["buy_num"] = buy_num
                                    invoke_result_data.data["pay_price"] = pay_price
                                    invoke_result_data.data["pay_num"] = pay_num
                                    if is_stat == True:
                                        stat_base_model = StatBaseModel(context=self.context)
                                        key_list_dict = {}
                                        key_list_dict["TotalBuyAppointGoodsMoneyCount"] = pay_price #支付金额
                                        stat_base_model.add_stat_list(app_id, act_id, 0, user_id, user_info_dict["open_id"], key_list_dict)
                                else:
                                    invoke_result_data.success = False
                                    invoke_result_data.error_code = "error"
                                    invoke_result_data.error_message = "没有匹配订单"
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "error"
                    invoke_result_data.error_message = "没有开启或配置购买指定商品任务"
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【购买指定商品任务】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【购买指定商品任务】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name, task_count_identifier)

        return invoke_result_data

    def process_receive_reward(self,app_id,act_id,module_id,user_id,login_token,task_id,task_sub_type,handler_name,request_code,task_type=0,check_new_user=False,check_user_nick=True,continue_request_expire=0,is_stat=True,info_json=None,check_act_info_release=True,check_act_module_release=True):
        """
        :description: 处理领取任务奖励
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param task_id:任务标识
        :param task_sub_type:子任务类型,对应配置里的id字段
        :param handler_name:接口名称
        :param request_code:请求代码
        :param task_type:任务类型，task_type和task_id二选一，task_id有的话用task_id，没有用task_type
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param is_stat:是否统计上报
        :param info_json:资产日志详细信息
        :param check_act_info_release:校验活动信息是否发布
        :param check_act_module_release:校验活动模块是否发布
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        task_count_acquire_lock_name = ""
        task_count_identifier = ""
        if not task_id and not task_type:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数错误,task_id和task_type不能同时为空"
            return invoke_result_data
        if task_id:
            source_object_id = f"taskid_{task_id}"
            acquire_lock_name = f"process_receive_reward_taskid:{act_id}_{module_id}_{task_id}_{user_id}"
        else:
            source_object_id = f"tasktype_{task_type}"
            acquire_lock_name = f"process_receive_reward_tasktype:{act_id}_{module_id}_{task_type}_{user_id}"

        log_title = ""
        now_day = TimeExHelper.get_now_day_int()
        db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key), context=self.context)
        try:
            invoke_result_data = self.business_process_executing(app_id, act_id, module_id, user_id, login_token, handler_name, check_new_user, check_user_nick, continue_request_expire, acquire_lock_name, source_object_id=source_object_id,check_act_info_release=check_act_info_release,check_act_module_release=check_act_module_release)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type=task_type,task_id=task_id)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    config_json = self.__covert_task_config_json(task_info_dict["config_json"], task_sub_type)
                    task_type = task_info_dict["task_type"]
                    reward_value = int(config_json["reward_value"]) if config_json.__contains__("reward_value") else 0
                    asset_object_id = config_json["asset_object_id"] if config_json.__contains__("asset_object_id") else ""
                    satisfy_num = decimal.Decimal(config_json["satisfy_num"]) if config_json.__contains__("satisfy_num") else 1
                    limit_num = int(config_json["limit_num"]) if config_json.__contains__("limit_num") else 1
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    invoke_result_data.data["task_info_dict"] = task_info_dict
                    task_count_model = TaskCountModel(db_transaction=db_transaction, context=self.context).set_sub_table(app_id)
                    task_count_id_md5 = self._get_task_count_id_md5(act_id,module_id,task_type,task_sub_type,user_id)
                    task_count_acquire_lock_name = f"task_count_idmd5:{task_count_id_md5}"
                    acquire_lock_status, task_count_identifier = SevenHelper.redis_acquire_lock(task_count_acquire_lock_name)
                    if acquire_lock_status == False:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "acquire_lock"
                        invoke_result_data.error_message = "当前人气火爆,请稍后再试"
                    else:
                        task_count = task_count_model.get_entity("id_md5=%s",params=[task_count_id_md5])
                        task_count = TaskCount() if not task_count else task_count
                        if task_info_dict["complete_type"] == TaskCompleteType.day.value and task_count.modify_day != now_day:
                            task_count.complete_count = 0
                            task_count.now_count = 0
                            task_count.remark = ""
                        elif task_info_dict["complete_type"] == TaskCompleteType.week.value and not TimeHelper.is_this_week(task_count.modify_date):
                            task_count.complete_count = 0
                            task_count.now_count = 0
                            task_count.remark = ""
                        elif task_info_dict["complete_type"] == TaskCompleteType.month.value and not TimeHelper.is_this_month(task_count.modify_date):
                            task_count.complete_count = 0
                            task_count.now_count = 0
                            task_count.remark = ""
                        if task_type in [TaskType.buy_appoint_goods_price.value, TaskType.buy_store_price.value]:
                            total_price =  decimal.Decimal(self.get_gear_task_count(app_id, act_id, module_id, user_id, task_type, task_info_dict["complete_type"]))
                            task_count.now_count = total_price - (task_count.complete_count * satisfy_num)
                        if reward_value <= 0 or task_count.now_count <= 0:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = "无法领取"
                        elif task_count.now_count < satisfy_num:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = "任务未完成"
                        elif task_count.complete_count >= limit_num:
                            invoke_result_data.success = False
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = "领取奖励已达上限"
                        else:
                            invite_list = None
                            collect_list = None
                            browse_list = None
                            invite_help_list = None

                            cur_complete_count = limit_num - task_count.complete_count if task_count.complete_count + int(task_count.now_count/satisfy_num) > limit_num else int(task_count.now_count / satisfy_num)
                            reward_value = cur_complete_count * reward_value
                            cur_now_count = task_count.now_count - (cur_complete_count * satisfy_num)

                            if task_type in [TaskType.invite_new_user.value, TaskType.invite_join_member.value]:
                                if task_type == TaskType.invite_new_user.value:
                                    invite_sub_table = ""
                                else:
                                    invite_sub_table = "member"
                                invite_log_model = InviteLogModel(sub_table=invite_sub_table,db_transaction=db_transaction,context=self.context)
                                #获取邀请用户数
                                if task_info_dict["complete_type"] == 1:
                                    invite_list = invite_log_model.get_list("act_id=%s and user_id=%s and is_handle=0 and create_day=%s",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id, now_day])
                                elif task_info_dict["complete_type"] == 2:
                                    start_day = int(TimeHelper.get_first_day_of_the_week().strftime('%Y%m%d'))
                                    end_day = int(TimeHelper.get_last_day_of_the_week().strftime('%Y%m%d'))
                                    invite_list = invite_log_model.get_list("act_id=%s and user_id=%s and is_handle=0 and create_day>=%s and create_day<=%s",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id, start_day,end_day])
                                else:
                                    invite_list = invite_log_model.get_list("act_id=%s and user_id=%s and is_handle=0",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id])
                                if not info_json:
                                    info_json = {}
                                    info_json["title"] = f"邀请{len(invite_list)}人"
                                    info_json["list"] = invite_list
                                invite_user_nick_list = []
                                for invite_log in invite_list:
                                    if invite_log.invite_user_nick:
                                        invite_user_nick_list.append(invite_log.invite_user_nick)
                                    else:
                                        invite_user_nick_list.append(invite_log.invite_open_id)
                                log_title = "被邀请用户：" + ",".join(invite_user_nick_list)
                            elif task_type == TaskType.invite_user_help.value:
                                invite_help_model = InviteHelpModel(db_transaction=db_transaction,context=self.context)
                                #获取邀请用户数
                                help_type = 1
                                help_object_id = ''
                                help_id_md5 = CryptoHelper.md5_encrypt_int(f"{app_id}_{act_id}_{module_id}_{help_type}_{help_object_id}")
                                invite_help_list = invite_help_model.get_list("id_md5=%s and user_id=%s and is_handle=0",limit=str(cur_complete_count * satisfy_num), params=[help_id_md5,user_id])
                                if not info_json:
                                    info_json = {}
                                    info_json["title"] = f"邀请{len(invite_help_list)}人"
                                    info_json["list"] = invite_help_list
                                invited_user_nick_list = []
                                for invite_help in invite_help_list:
                                    if invite_help.invited_user_nick:
                                        invited_user_nick_list.append(invite_help.invited_user_nick)
                                    else:
                                        invited_user_nick_list.append(invite.invited_open_id)
                                log_title = "被邀请用户：" + ",".join(invited_user_nick_list)
                            elif task_type in [TaskType.collect_goods.value, TaskType.browse_goods.value]:
                                if task_type == TaskType.collect_goods.value:
                                    collect_log_model = CollectLogModel(db_transaction=db_transaction,context=self.context)
                                    if task_info_dict["complete_type"] == 1:
                                        collect_list = collect_log_model.get_list("act_id=%s and user_id=%s and is_handle=0 and create_day=%s",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id, now_day])
                                    elif task_info_dict["complete_type"] == 2:
                                        start_day = int(TimeHelper.get_first_day_of_the_week().strftime('%Y%m%d'))
                                        end_day = int(TimeHelper.get_last_day_of_the_week().strftime('%Y%m%d'))
                                        collect_list = collect_log_model.get_list("act_id=%s and user_id=%s and is_handle=0 and create_day>=%s and create_day<=%s",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id, start_day,end_day])
                                    else:
                                        collect_list = collect_log_model.get_list("act_id=%s and user_id=%s and is_handle=0",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id])
                                    if not info_json:
                                        info_json = {}
                                        info_json["title"] = f"收藏{len(collect_list)}个"
                                        info_json["list"] = collect_list
                                    collect_goods_id_list = [str(i.goods_id) for i in collect_list]
                                    log_title = "被收藏商品ID：" + ",".join(collect_goods_id_list)
                                else:
                                    browse_log_model = BrowseLogModel(db_transaction=db_transaction,context=self.context)
                                    if task_info_dict["complete_type"] == 1:
                                        browse_list = browse_log_model.get_list("act_id=%s and user_id=%s and is_handle=0 and create_day=%s",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id, now_day])
                                    elif task_info_dict["complete_type"] == 2:
                                        start_day = int(TimeHelper.get_first_day_of_the_week().strftime('%Y%m%d'))
                                        end_day = int(TimeHelper.get_last_day_of_the_week().strftime('%Y%m%d'))
                                        browse_list = browse_log_model.get_list("act_id=%s and user_id=%s and is_handle=0 and create_day>=%s and create_day<=%s",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id, start_day,end_day])
                                    else:
                                        browse_list = browse_log_model.get_list("act_id=%s and user_id=%s and is_handle=0",limit=str(cur_complete_count * satisfy_num), params=[act_id,user_id])
                                    if not info_json:
                                        info_json = {}
                                        info_json["title"] = f"收藏{len(browse_list)}个"
                                        info_json["list"] = browse_list
                                    browse_goods_id_list = [str(i.goods_id) for i in browse_list]
                                    log_title = "被浏览商品ID：" + ",".join(browse_goods_id_list)
                            elif task_type == TaskType.buy_appoint_goods.value:
                                remark = SevenHelper.json_loads(task_count.remark) if task_count.remark else {"goods_id_list":[]}
                                goods_id_list = []
                                task_goods_id_list = remark.get("goods_id_list",[])
                                if len(task_goods_id_list) >= (cur_complete_count * satisfy_num):
                                    start_index = 0
                                    end_index = int(cur_complete_count * satisfy_num)
                                    goods_id_list = task_goods_id_list[start_index : end_index]
                                    del task_goods_id_list[start_index : end_index]
                                if not info_json:
                                    info_json = {}
                                    info_json["title"] = f"购买{len(goods_id_list)}个"
                                    info_json["list"] = goods_id_list
                                log_title = "购买商品ID：" + ",".join(goods_id_list)
                                task_count.remark = SevenHelper.json_dumps({"goods_id_list":task_goods_id_list})

                            if invoke_result_data.success == True:
                                try:
                                    db_transaction.begin_transaction()
                                    task_count.complete_count += cur_complete_count
                                    task_count.now_count = cur_now_count

                                    #更新邀请记录表
                                    if invite_list:
                                        for invite in invite_list:
                                            invite.is_handle = 1
                                        invite_log_model.update_list(invite_list, "is_handle")
                                    #更新收藏记录表
                                    elif collect_list:
                                        for collect in collect_list:
                                            collect.is_handle = 1
                                        collect_log_model.update_list(collect_list, "is_handle")
                                    #更新浏览记录表
                                    elif browse_list:
                                        for browse in browse_list:
                                            browse.is_handle = 1
                                        browse_log_model.update_list(browse_list, "is_handle")
                                    #更新邀请助力记录表
                                    elif invite_help_list:
                                        for invite_help in invite_help_list:
                                            invite_help.is_handle = 1
                                        invite_help_model.update_list(invite_help_list, "is_handle")

                                    #更新任务计数表
                                    task_count_model.update_entity(task_count, "complete_count,now_count,remark")
                                    result,message = db_transaction.commit_transaction(True)
                                    if result == False:
                                        raise Exception("执行事务失败",message)
                                    if invite_help_list:
                                        invite_help_model.delete_dependency_key(DependencyKey.invite_user_help_list(help_id_md5, user_info_dict["user_id"]))
                                except Exception as ex:
                                    if self.context:
                                        self.context.logging_link_error("【领取任务奖励】" + traceback.format_exc())
                                    elif self.logging_link_error:
                                        self.logging_link_error("【领取任务奖励】" + traceback.format_exc())
                                    self.business_process_executed()
                                    invoke_result_data.success = False
                                    invoke_result_data.error_code = "exception"
                                    invoke_result_data.error_message = "系统繁忙,请稍后再试"
                                    return invoke_result_data

                                reward_object_id = asset_object_id
                                reward_name = config_json.get("reward_name","")
                                task_reward_type = config_json.get("reward_type", TaskRewardType.asset.value)
                                #奖励类型为资产走资产系统
                                if task_reward_type == TaskRewardType.asset.value:
                                    only_id = self.get_only_id(user_id,task_info_dict["complete_type"],task_info_dict["task_type"],task_sub_type,task_count.complete_count)
                                    if module_id > 0:
                                        only_id = f"{module_id}_{only_id}"
                                    asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_info_dict["task_type"])
                                    reward_object_id = asset_type
                                    asset_base_model = AssetBaseModel(context=self.context)
                                    log_title = log_title if log_title else task_info_dict["task_name"]
                                    asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,asset_object_id,2,task_info_dict["task_type"],task_info_dict["task_name"],log_title,only_id,handler_name,request_code,info_json=info_json)
                                    if asset_invoke_result_data.success == False:
                                        reward_value = 0
                                invoke_result_data.data["config_json"] = config_json
                                invoke_result_data.data["reward_value"] = reward_value

                                self.add_task_stat(task_type, app_id, act_id, module_id, user_info_dict["user_id"], user_info_dict["open_id"], reward_value, is_stat, cur_complete_count)
                                self.add_task_log(task_type=task_type, task_sub_type=task_sub_type, app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_info_dict["user_id"], open_id=user_info_dict["open_id"], user_nick=user_info_dict["user_nick"],task_name=task_info_dict["task_name"],log_title=log_title,reward_type=task_reward_type, reward_object_id=reward_object_id, reward_name=reward_name, reward_num=reward_value, handler_name=handler_name, request_code=request_code, info_json=info_json)
                else:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = task_invoke_result_data.error_code
                    invoke_result_data.error_message = task_invoke_result_data.error_message
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【领取任务奖励】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【领取任务奖励】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            self.business_process_executed()
            if task_count_acquire_lock_name and task_count_identifier:
                SevenHelper.redis_release_lock(task_count_acquire_lock_name, task_count_identifier)

        return invoke_result_data
