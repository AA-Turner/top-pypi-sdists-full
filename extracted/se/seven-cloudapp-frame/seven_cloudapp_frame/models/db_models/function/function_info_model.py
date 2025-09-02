# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2022-12-15 10:52:33
:LastEditTime: 2022-12-15 13:57:08
:LastEditors: HuangJingCan
:Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class FunctionInfoModel(CacheModel):

    def __init__(self, db_connect_key='db_middler_platform', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(FunctionInfoModel, self).__init__(FunctionInfo, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class FunctionInfo:
    def __init__(self):
        super(FunctionInfo, self).__init__()
        self.id = 0  # id
        self.product_id = 0  # 产品id
        self.function_name = ""  # 功能名称
        self.key_name = ""  # key名称
        self.sort_index = 0  # 排序
        self.is_release = 0  # 是否发布：0未发布1已发布
        self.operation_user = ""  # 操作用户
        self.use_count = 0  # 使用数量
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'product_id', 'function_name', 'key_name', 'sort_index', 'is_release', 'operation_user', 'use_count', 'create_date', 'modify_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "function_info_tb"
