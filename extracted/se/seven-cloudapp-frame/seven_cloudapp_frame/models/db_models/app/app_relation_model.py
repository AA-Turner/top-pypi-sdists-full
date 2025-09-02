# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-20 10:09:52
@LastEditTime: 2023-12-25 11:57:08
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class AppRelationModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(AppRelationModel, self).__init__(AppRelation, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class AppRelation:

    def __init__(self):
        super(AppRelation, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.template_id = "" # 应用模板ID
        self.ref_app_id = ""  # 关联应用标识
        self.ref_template_id = "" # 关联应用模板ID
        self.create_date = "1900-01-01 00:00:00"  # 创建时间


    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'template_id', 'ref_app_id', 'ref_template_id', 'create_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "app_relation_tb"
