# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-20 10:09:52
@LastEditTime: 2023-12-25 14:48:41
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class AppTemplateModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(AppTemplateModel, self).__init__(AppTemplate, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class AppTemplate:

    def __init__(self):
        super(AppTemplate, self).__init__()
        self.id = 0  # id
        self.template_id = ""  # 模板标识
        self.product_name = "" # 产品名称
        self.product_icon = "" # 产品图标
        self.product_desc = "" # 产品简介
        self.client_ver = "" # 客户端版本号
        self.update_function = ""  # 版本更新内容
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', "template_id", 'product_name', 'product_icon', 'product_desc', 'client_ver', 'update_function', "create_date", "modify_date"]

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "app_template_tb"
