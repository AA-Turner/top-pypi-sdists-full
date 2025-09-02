# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-27 10:55:09
@LastEditTime: 2022-07-13 17:51:05
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class LaunchPlanModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(LaunchPlanModel, self).__init__(LaunchPlan, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class LaunchPlan:

    def __init__(self):
        super(LaunchPlan, self).__init__()
        self.id = 0  # 标识
        self.app_id = ""  # 应用唯一标识
        self.act_id = 0  # 活动标识
        self.tb_launch_id = 0  # 淘宝投放计划标识
        self.launch_url = ""  # 投放链接
        self.start_date = "1900-01-01 00:00:00" # 投放开始时间
        self.end_date = "1900-01-01 00:00:00"  # 投放结束时间
        self.status = 0  # 投放状态
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'tb_launch_id', 'launch_url', 'start_date', 'end_date', 'status', 'create_date', 'modify_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "launch_plan_tb"
