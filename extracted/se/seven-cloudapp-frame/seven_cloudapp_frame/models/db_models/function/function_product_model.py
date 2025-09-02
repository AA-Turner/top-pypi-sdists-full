# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2022-12-15 10:52:33
:LastEditTime: 2022-12-15 13:58:26
:LastEditors: HuangJingCan
:Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class FunctionProductModel(CacheModel):
    def __init__(self, db_connect_key='db_middler_platform', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(FunctionProductModel, self).__init__(FunctionProduct, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class FunctionProduct:
    def __init__(self):
        super(FunctionProduct, self).__init__()
        self.app_id = 0  # 程序标识
        self.app_code = ""  # 程序代码
        self.app_name = ""  # 程序名称
        self.parent_id = 0  # 父标识
        self.name_path = ""  # 程序名路径
        self.id_path = ""  # 父路经
        self.sort_index = 0  # 排序
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['app_id', 'app_code', 'app_name', 'parent_id', 'name_path', 'id_path', 'sort_index', 'create_date']

    @classmethod
    def get_primary_key(self):
        return "app_id"

    def __str__(self):
        return "function_product_tb"
