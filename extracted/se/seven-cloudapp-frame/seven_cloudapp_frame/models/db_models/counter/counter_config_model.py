# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-26 09:40:36
@LastEditTime: 2022-12-07 14:18:05
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class CounterConfigModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(CounterConfigModel, self).__init__(CounterConfig, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class CounterConfig:

    def __init__(self):
        super(CounterConfig, self).__init__()
        self.id = 0  # id
        self.key_name = ""  # 计数key
        self.key_expire = 0  # 计数key过期时间
        self.db_connect_key = ""  # 数据库连接串Key
        self.table_name = ""  # 表名
        self.id_field_name = ""  # 主键字段名称
        self.value_field_name = ""  # 值字段名称
        self.is_release = 0  # 是否发布(1是0否)
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'key_name', 'key_expire', 'db_connect_key', 'table_name', 'id_field_name', 'value_field_name', 'is_release', 'create_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "counter_config_tb"
