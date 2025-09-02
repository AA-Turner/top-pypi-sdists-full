# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-15 17:17:08
@LastEditTime: 2024-01-03 10:44:22
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class TaskLogModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(TaskLogModel, self).__init__(TaskLog, sub_table)
        db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_task","redis_task", db_connect_key)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class TaskLog:

    def __init__(self):
        super(TaskLog, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.module_id = 0  # 活动模块标识
        self.user_id = 0  # 用户标识
        self.open_id = ""  # open_id
        self.user_nick = ""  # 昵称
        self.log_title = ""  # 标题
        self.info_json = ""  # 详情信息
        self.task_type = 0  # 任务类型
        self.task_sub_type = ""  # 任务子类型
        self.task_name = ""  # 任务名称
        self.reward_type = ""  # 奖励类型
        self.reward_object_id = ""  # 奖励对象标识
        self.reward_name = ""  # 奖励名称
        self.reward_num = 0  # 奖励数量
        self.handler_name = ""  # 接口名称
        self.request_code = ""  # 请求代码
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_day = 0  # 创建天
        self.i1 = 0  # i1
        self.s1 = ""  # s1

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'module_id', 'user_id', 'open_id', 'user_nick', 'log_title', 'info_json', 'task_type', 'task_sub_type', 'task_name', 'reward_type', 'reward_object_id', 'reward_name', 'reward_num', 'handler_name', 'request_code', 'create_date', 'create_day', 'i1', 's1']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "task_log_tb"
