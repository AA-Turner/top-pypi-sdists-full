# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-10 10:09:06
@LastEditTime: 2024-01-03 10:43:54
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class TaskGearCountModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(TaskGearCountModel, self).__init__(TaskGearCount, sub_table)
        db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_task","redis_task", db_connect_key)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context
        self.redis_config_dict = config.get_value("redis_task")

    #方法扩展请继承此类


class TaskGearCount:

    def __init__(self):
        super(TaskGearCount, self).__init__()
        self.id = 0  # 标识
        self.id_md5 = 0  # id_md5(actid+moduleid+tasktype+userid)md5int生成
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.module_id = 0  # 活动模块标识
        self.user_id = 0  # 用户标识
        self.open_id = ""  # open_id
        self.task_type = 0  # 任务类型（枚举TaskType）
        self.now_count = 0  # 当前计数
        self.create_day = 0  # 创建天(19000101)
        self.create_month = 0  # 创建天(19000101)
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.remark = ""  # 备注

    @classmethod
    def get_field_list(self):
        return ['id', 'id_md5', 'app_id', 'act_id', 'module_id', 'user_id', 'open_id', 'task_type', 'now_count', 'create_day', 'create_month', 'create_date', 'modify_date', 'remark']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "task_gear_count_tb"
