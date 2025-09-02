# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-08-24 15:02:41
@LastEditTime: 2023-12-29 13:42:56
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class StatUserReportModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(StatUserReportModel, self).__init__(StatUserReport, sub_table)
        db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_stat","redis_stat", db_connect_key)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class StatUserReport:

    def __init__(self):
        super(StatUserReport, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.module_id = 0  # 活动模块标识
        self.user_id = 0  # 用户标识
        self.open_id = ""  # open_id
        self.i1 = 0  # i1
        self.i2 = 0  # i2
        self.i3 = 0  # i3
        self.i4 = 0  # i4
        self.i5 = 0  # i5
        self.i6 = 0  # i6
        self.i7 = 0  # i7
        self.i8 = 0  # i8
        self.i9 = 0  # i9
        self.i10 = 0  # i10
        self.i11 = 0  # i11
        self.i12 = 0  # i12
        self.i13 = 0  # i13
        self.i14 = 0  # i14
        self.i15 = 0  # i15
        self.i16 = 0  # i16
        self.i17 = 0  # i17
        self.i18 = 0  # i18
        self.i19 = 0  # i19
        self.i20 = 0  # i20
        self.d1 = 0  # d1
        self.d2 = 0  # d2
        self.d3 = 0  # d3
        self.d4 = 0  # d4
        self.d5 = 0  # d5
        self.d6 = 0  # d6
        self.d7 = 0  # d7
        self.d8 = 0  # d8
        self.d9 = 0  # d9
        self.d10 = 0  # d10
        self.create_day = 0  # 创建天
        self.create_month = 0  # 创建月
        self.create_year = 0  # 创建年
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'module_id', 'user_id', 'open_id', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10', 'i11', 'i12', 'i13', 'i14', 'i15', 'i16', 'i17', 'i18', 'i19', 'i20', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'create_day', 'create_month', 'create_year', 'create_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "stat_user_report_tb"
