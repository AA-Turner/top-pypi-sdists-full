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


class FunctionModuleModel(CacheModel):

    def __init__(self, db_connect_key='db_middler_platform', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(FunctionModuleModel, self).__init__(FunctionModule, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class FunctionModule:
    def __init__(self):
        super(FunctionModule, self).__init__()
        self.id = 0  # id
        self.product_id = 0  # 产品id
        self.module_type = 0  # 模块类型：1基础模块2中级模块3高级模块
        self.module_name = ""  # 模块名称
        self.is_release = 0  # 是否发布：0未发布1已发布
        self.app_code = ""  # 应用编码（淘系项目，收费项目列表查询）
        self.project_code = ""  # 项目编码（淘系项目，收费项目列表查询）
        self.skin_ids = ""  # 皮肤id列表（逗号隔开）
        self.function_ids = ""  # 功能id列表（逗号隔开）
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'product_id', 'module_type', 'module_name', 'is_release', 'app_code', 'project_code', 'skin_ids', 'function_ids', 'modify_date', 'create_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "function_module_tb"
