# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 10:11:35
@LastEditTime: 2023-08-18 14:39:49
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class OperationConfigModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(OperationConfigModel, self).__init__(OperationConfig, sub_table)
        db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_cms","redis_cms", db_connect_key)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class OperationConfig:

    def __init__(self):
        super(OperationConfig, self).__init__()
        self.id = 0  # id
        self.model_name = ""  # 模块或表名称
        self.config_json = ""  # 配置信息json
        self.create_date = "1900-01-01 00:00:00"  # 创建时间



    @classmethod
    def get_field_list(self):
        return ['id', 'model_name', 'config_json', 'create_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "operation_config_tb"
