# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 09:39:08
@LastEditTime: 2025-03-19 18:12:10
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.frame_base_model import FrameBaseModel
from seven_cloudapp_frame.models.db_models.stat.stat_queue_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_report_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_orm_model import *

class StatBaseModel(FrameBaseModel):
    """
    :description: 统计上报业务模型
    """
    def __init__(self, context=None,logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info
        self.db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_stat","redis_stat")
        super(StatBaseModel,self).__init__(context)
    
    def init_stat_orm(self, app_id, act_id, module_id, group_name, group_sub_name, key_name, key_value, value_type, repeat_type, sort_index, is_show, tip_title='', object_id=''):
        """
        :description: 初始化统计orm
        :param app_id   应用标识
        :param act_id   活动标识
        :param module_id    活动模块标识
        :param group_name   分组名称
        :param group_sub_name   分组子名称
        :param key_name key名称
        :param key_value    key值
        :param value_type   输出类型(1-int，2-decimal)
        :param repeat_type  去重方式(0不去重1当日去重2全部去重) 
        :param sort_index   排序号
        :param is_show  是否显示(1是0否)
        :param tip_title  提示标题
        :param object_id  对象标识
        :return
        :last_editors: HuangJianYi
        """
        stat_orm = StatOrm()
        stat_orm.app_id = app_id
        stat_orm.act_id = act_id
        stat_orm.module_id = module_id
        stat_orm.object_id = object_id
        stat_orm.group_name = group_name
        stat_orm.group_sub_name = group_sub_name
        stat_orm.key_name = key_name
        stat_orm.key_value = key_value
        stat_orm.tip_title = tip_title
        stat_orm.value_type = value_type
        stat_orm.repeat_type = repeat_type
        stat_orm.sort_index = sort_index
        stat_orm.create_date = TimeHelper.get_now_datetime()
        stat_orm.is_show = is_show
        return stat_orm

    def add_stat(self, app_id, act_id, module_id, user_id, open_id, key_name, key_value, object_id=''):
        """
        :description: 添加活动（模块）上报
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识(比传)
        :param open_id：open_id(可不传)
        :param key_name：统计key
        :param key_value：统计value
        :param object_id：对象标识
        :return:
        :last_editors: HuangJianYi
        """
        stat_queue = StatQueue()
        stat_queue.app_id = app_id
        stat_queue.act_id = act_id
        stat_queue.module_id = module_id
        stat_queue.object_id = object_id
        stat_queue.user_id = user_id
        stat_queue.open_id = open_id
        stat_queue.key_name = key_name
        stat_queue.key_value = key_value
        stat_queue.create_date = SevenHelper.get_now_datetime()
        stat_queue.process_date = SevenHelper.get_now_datetime()

        redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
        stat_process_ways = share_config.get_value("stat_process_ways","redis")
        if stat_process_ways == "mysql":
            stat_queue_model = StatQueueModel(context=self.context)
            stat_queue_model.add_entity(stat_queue)
        else:
            redis_init.rpush(f"stat_queue_list:{str(user_id % 10)}", SevenHelper.json_dumps(stat_queue))

    def add_stat_list(self, app_id, act_id, module_id, user_id, open_id, stat_data, object_id=''):
        """
        :description: 添加活动（模块）上报
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识(比传)
        :param open_id：open_id(可不传)
        :param stat_data:统计数据
        :param object_id：对象标识
        :return:
        :last_editors: HuangJianYi
        """
        stat_process_ways = share_config.get_value("stat_process_ways","redis")
        stat_queue_list = []
        if isinstance(stat_data,list):
            for item in stat_data:
                stat_queue = StatQueue()
                stat_queue.app_id = app_id
                stat_queue.act_id = act_id
                stat_queue.module_id = module_id
                stat_queue.object_id = object_id
                stat_queue.user_id = user_id
                stat_queue.open_id = open_id
                stat_queue.key_name = item["key"]
                stat_queue.key_value = item["value"]
                stat_queue.create_date = SevenHelper.get_now_datetime()
                stat_queue.process_date = SevenHelper.get_now_datetime()
                if stat_process_ways == "mysql":
                    stat_queue_list.append(stat_queue)
                else:
                    stat_queue_list.append(SevenHelper.json_dumps(stat_queue))
        else:
            for key,value in stat_data.items():
                stat_queue = StatQueue()
                stat_queue.app_id = app_id
                stat_queue.act_id = act_id
                stat_queue.module_id = module_id
                stat_queue.object_id = object_id
                stat_queue.user_id = user_id
                stat_queue.open_id = open_id
                stat_queue.key_name = key
                stat_queue.key_value = value
                stat_queue.create_date = SevenHelper.get_now_datetime()
                stat_queue.process_date = SevenHelper.get_now_datetime()
                if stat_process_ways == "mysql":
                    stat_queue_list.append(stat_queue)
                else:
                    stat_queue_list.append(SevenHelper.json_dumps(stat_queue))

        if stat_process_ways == "mysql":
            stat_queue_model = StatQueueModel(context=self.context)
            return stat_queue_model.add_list(stat_queue_list)
        else:
            if len(stat_queue_list) > 0:
                redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
                redis_init.rpush(f"stat_queue_list:{str(user_id % 10)}", *stat_queue_list)

    def get_stat_report_list(self, app_id, act_id, module_id, start_date, end_date, order_by="sort_index asc", is_only_module=False, orm_condition=None, orm_params=None, report_condition=None, report_params=None, object_id=''):
        """
        :description: 报表数据列表(表格)
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param order_by：orm排序
        :param is_only_module：是否只取module的数据
        :param orm_condition：orm查询条件
        :param orm_params：orm参数数组
        :param report_condition：report查询条件
        :param report_params：report参数数组
        :param object_id：对象标识
        :return list
        :last_editors: HuangJianYi
        """
        stat_report_condition = deepcopy(report_condition)
        stat_report_params = deepcopy(report_params)
        stat_orm_condition = deepcopy(orm_condition)
        stat_orm_params = deepcopy(orm_params)
        if not stat_report_condition:
            stat_report_condition = "app_id=%s and act_id=%s and module_id=%s and object_id=%s" if app_id else "act_id=%s and module_id=%s and object_id=%s"
        if not stat_report_params:
            stat_report_params = [app_id, act_id, module_id, object_id] if app_id else [act_id, module_id, object_id]
        if start_date != "":
            stat_report_condition += " and create_date>=%s"
            stat_report_params.append(start_date)
        if end_date != "":
            stat_report_condition += " and create_date<%s"
            stat_report_params.append(end_date)
        if is_only_module == True:
            if not stat_orm_condition:
                stat_orm_condition = "act_id=%s and module_id=%s and object_id=%s and is_show=1"
            if not stat_orm_params:
                stat_orm_params = [act_id, module_id, object_id]
        else:
            if not stat_orm_condition:
                stat_orm_condition = "((act_id=%s and module_id=%s and object_id=%s) or (act_id=0 and module_id=0 and object_id='')) and is_show=1"
            if not stat_orm_params:
                stat_orm_params = [act_id, module_id, object_id]
        stat_orm_list = StatOrmModel(context=self.context, is_auto=True).get_list(where=stat_orm_condition, group_by="key_name", order_by=order_by, params=stat_orm_params)
        if len(stat_orm_list)<=0:
            return []
        key_name_s = ','.join(["'%s'" % str(stat_orm.key_name) for stat_orm in stat_orm_list])
        stat_report_condition += f" and key_name in({key_name_s})"
        stat_report_model = StatReportModel(context=self.context, is_auto=True)
        behavior_report_list = stat_report_model.get_dict_list(stat_report_condition, group_by="key_name", field="key_name,SUM(key_value) AS key_value",params=stat_report_params)
        #公共映射组（未去重）
        common_groups_1 = [orm.group_name for orm in stat_orm_list]
        #公共映射组(去重)
        common_groups = list(set(common_groups_1))
        common_groups.sort(key=common_groups_1.index)

        common_group_data_list = []

        for common_group in common_groups:
            group_data = {}
            group_data["group_name"] = common_group
            data_list = []

            # 无子节点
            orm_list = [orm for orm in stat_orm_list if orm.group_name == common_group and orm.group_sub_name == '']
            for orm in orm_list:
                data = {}
                data["title"] = orm.key_value
                data["tip_title"] = orm.tip_title
                data["name"] = orm.key_name
                data["value"] = 0
                for behavior_report in behavior_report_list:
                    if behavior_report["key_name"] == orm.key_name:
                        if orm.value_type == 2:
                            data["value"] = behavior_report["key_value"]
                        else:
                            data["value"] = int(behavior_report["key_value"])
                data_list.append(data)
            if len(data_list) > 0:
                group_data["data_list"] = data_list

            # 有子节点
            orm_list_sub = [orm for orm in stat_orm_list if orm.group_name == common_group and orm.group_sub_name != '']
            if orm_list_sub:
                groups_sub_name = [orm.group_sub_name for orm in orm_list_sub]
                #公共映射组(去重)
                sub_names = list(set(groups_sub_name))
                sub_names.sort(key=groups_sub_name.index)
                sub_group_data_list = []
                for sub_name in sub_names:
                    sub_group_data = {}
                    sub_group_data["group_name"] = sub_name
                    sub_data_list = []

                    # 无子节点
                    orm_list_1 = [orm for orm in stat_orm_list if orm.group_sub_name == sub_name]
                    for orm in orm_list_1:
                        data = {}
                        data["title"] = orm.key_value
                        data["tip_title"] = orm.tip_title
                        data["name"] = orm.key_name
                        data["value"] = 0
                        for behavior_report in behavior_report_list:
                            if behavior_report["key_name"] == orm.key_name:
                                if orm.value_type == 2:
                                    data["value"] = behavior_report["key_value"]
                                else:
                                    data["value"] = int(behavior_report["key_value"])
                        sub_data_list.append(data)
                    sub_group_data["data_list"] = sub_data_list
                    sub_group_data_list.append(sub_group_data)
                group_data["sub_data_list"] = sub_group_data_list

            common_group_data_list.append(group_data)

        return common_group_data_list

    def get_trend_report_list(self, app_id, act_id, module_id, start_date, end_date, order_by="sort_index asc", is_only_module=False, orm_condition=None, orm_params=None, report_condition=None, report_params=None, object_id=''):
        """
        :description: 报表数据列表(趋势图)
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param order_by：orm排序
        :param is_only_module：是否只取module的数据
        :param orm_condition：orm查询条件
        :param orm_params：orm参数数组
        :param report_condition：report查询条件
        :param report_params：report参数数组
        :param object_id：对象标识
        :return list
        :last_editors: HuangJianYi
        """
        trend_report_condition = deepcopy(report_condition)
        trend_report_params = deepcopy(report_params)
        trend_orm_condition = deepcopy(orm_condition)
        trend_orm_params = deepcopy(orm_params)
        if not trend_report_condition:
            trend_report_condition = "app_id=%s and act_id=%s and module_id=%s and object_id=%s" if app_id else "act_id=%s and module_id=%s and object_id=%s"
        if not trend_report_params:
            trend_report_params = [app_id, act_id, module_id, object_id] if app_id else [act_id, module_id, object_id]
        if start_date != "":
            trend_report_condition += " and create_date>=%s"
            trend_report_params.append(start_date)
        if end_date != "":
            trend_report_condition += " and create_date<%s"
            trend_report_params.append(end_date)
        if is_only_module == True:
            if not trend_orm_condition:
                trend_orm_condition = "act_id=%s and module_id=%s and object_id=%s and is_show=1"
            if not trend_orm_params:
                trend_orm_params = [act_id, module_id, object_id]
        else:
            if not trend_orm_condition:
                trend_orm_condition = "((act_id=%s and module_id=%s and object_id=%s) or (act_id=0 and module_id=0 and object_id='')) and is_show=1"
            if not trend_orm_params:
                trend_orm_params = [act_id, module_id, object_id]
        stat_orm_list = StatOrmModel(context=self.context, is_auto=True).get_list(where=trend_orm_condition, group_by="key_name", order_by=order_by, params=trend_orm_params)
        if len(stat_orm_list)<=0:
            return []
        key_name_s = ','.join(["'%s'" % str(stat_orm.key_name) for stat_orm in stat_orm_list])
        trend_report_condition += f" and key_name in({key_name_s})"
        stat_report_model = StatReportModel(context=self.context, is_auto=True)
        stat_report_list = stat_report_model.get_dict_list(trend_report_condition, field="key_name,key_value,DATE_FORMAT(create_date,'%%Y-%%m-%%d') AS create_date",params=trend_report_params)
        date_list = SevenHelper.get_date_list(start_date, end_date)
        #公共映射组（未去重）
        common_groups_1 = [orm.group_name for orm in stat_orm_list]
        #公共映射组(去重)
        common_groups = list(set(common_groups_1))
        common_groups.sort(key=common_groups_1.index)

        common_group_data_list = []

        for common_group in common_groups:
            group_data = {}
            group_data["group_name"] = common_group
            data_list = []

            # 无子节点
            orm_list = [orm for orm in stat_orm_list if orm.group_name == common_group and orm.group_sub_name == '']
            for orm in orm_list:
                data = {}
                data["title"] = orm.key_value
                data["name"] = orm.key_name
                data["value"] = []
                for date_day in date_list:
                    behavior_date_report = {}
                    for behavior_report in stat_report_list:
                        if behavior_report["key_name"] == orm.key_name and behavior_report["create_date"] == date_day:
                            if orm.value_type != 2:
                                behavior_report["key_value"] = int(behavior_report["key_value"])
                            behavior_date_report = {"title": orm.key_value, "date": date_day, "value": behavior_report["key_value"]}
                            break
                    if not behavior_date_report:
                        behavior_date_report = {"title": orm.key_value, "date": date_day, "value": 0}
                    data["value"].append(behavior_date_report)
                data_list.append(data)
            if len(data_list) > 0:
                group_data["data_list"] = data_list

            # 有子节点
            orm_list_sub = [orm for orm in stat_orm_list if orm.group_name == common_group and orm.group_sub_name != '']
            if orm_list_sub:
                groups_sub_name = [orm.group_sub_name for orm in orm_list_sub]
                #公共映射组(去重)
                sub_names = list(set(groups_sub_name))
                sub_names.sort(key=groups_sub_name.index)
                sub_group_data_list = []
                for sub_name in sub_names:
                    sub_group_data = {}
                    sub_group_data["group_name"] = sub_name
                    sub_data_list = []

                    # 无子节点
                    orm_list_1 = [orm for orm in stat_orm_list if orm.group_sub_name == sub_name]
                    for orm in orm_list_1:
                        data = {}
                        data["title"] = orm.key_value
                        data["name"] = orm.key_name
                        data["value"] = []
                        for date_day in date_list:
                            behavior_date_report = {}
                            for behavior_report in stat_report_list:
                                if behavior_report["key_name"] == orm.key_name and behavior_report["create_date"] == date_day:
                                    if orm.value_type != 2:
                                        behavior_report["key_value"] = int(behavior_report["key_value"])
                                    behavior_date_report = {"title": orm.key_value, "date": date_day, "value": behavior_report["key_value"]}
                                    break
                            if not behavior_date_report:
                                behavior_date_report = {"title": orm.key_value, "date": date_day, "value": 0}
                            data["value"].append(behavior_date_report)
                        sub_data_list.append(data)
                    sub_group_data["data_list"] = sub_data_list
                    sub_group_data_list.append(sub_group_data)
                group_data["sub_data_list"] = sub_group_data_list

            common_group_data_list.append(group_data)

        return common_group_data_list

    def process_invite_report(self, app_id, act_id, module_id, user_id, open_id, invite_user_id):
        """
        :description: 处理邀请进入上报
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param open_id:open_id
        :param invite_user_id:邀请人用户标识
        :param handler_name:接口名称
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            if user_id == invite_user_id:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "无效邀请"
                return invoke_result_data
            key_list_dict = {}
            key_list_dict["AddBeInvitedUserCount"] = 1 #从分享进入新增用户数
            key_list_dict["BeInvitedUserCount"] = 1  #从分享进入用户数
            key_list_dict["BeInvitedCount"] = 1  #从分享进入次数
            self.add_stat_list(app_id, act_id, module_id, user_id, open_id, key_list_dict)
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【处理邀请上报】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【处理邀请上报】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

        return invoke_result_data

    def process_share_report(self, app_id, act_id, module_id, user_id, open_id):
        """
        :description: 处理分享上报
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param open_id:open_id
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            key_list_dict = {}
            key_list_dict["ShareUserCount"] = 1 #分享用户数
            key_list_dict["ShareCount"] = 1 #分享次数
            self.add_stat_list(app_id, act_id, module_id, user_id, open_id, key_list_dict)
        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【处理分享上报】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【处理分享上报】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

        return invoke_result_data

    def add_stat_user_list(self, app_id, act_id, module_id, user_id, open_id, stat_data, object_id=''):
        """
        :description: 添加用户行为上报
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_id：用户标识
        :param open_id：open_id
        :param stat_data:统计数据
        :param object_id：对象标识
        :return:
        :last_editors: HuangJianYi
        """
        stat_queue_list = []
        if isinstance(stat_data,list):
            for item in stat_data:
                stat_queue = StatQueue()
                stat_queue.app_id = app_id
                stat_queue.act_id = act_id
                stat_queue.module_id = module_id
                stat_queue.object_id = object_id
                stat_queue.user_id = user_id
                stat_queue.open_id = open_id
                stat_queue.key_name = item["key"]
                stat_queue.key_value = item["value"]
                if hasattr(self.context, "request_code"):
                    stat_queue.request_code = self.context.request_code
                stat_queue.create_date = SevenHelper.get_now_datetime()
                stat_queue.process_date = SevenHelper.get_now_datetime()
                stat_queue_list.append(SevenHelper.json_dumps(stat_queue))
        else:
            for key,value in stat_data.items():
                stat_queue = StatQueue()
                stat_queue.app_id = app_id
                stat_queue.act_id = act_id
                stat_queue.module_id = module_id
                stat_queue.object_id = object_id
                stat_queue.user_id = user_id
                stat_queue.open_id = open_id
                stat_queue.key_name = key
                stat_queue.key_value = value
                if hasattr(self.context, "request_code"):
                    stat_queue.request_code = self.context.request_code
                stat_queue.create_date = SevenHelper.get_now_datetime()
                stat_queue.process_date = SevenHelper.get_now_datetime()
                stat_queue_list.append(SevenHelper.json_dumps(stat_queue))

        redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
        redis_init.rpush(f"stat_user_queue_list:{str(user_id % 10)}", *stat_queue_list)    