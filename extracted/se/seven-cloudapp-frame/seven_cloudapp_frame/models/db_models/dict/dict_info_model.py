# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-09-26 15:19:56
@LastEditTime: 2022-09-28 11:13:26
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class DictInfoModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(DictInfoModel, self).__init__(DictInfo, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class DictInfo:

    def __init__(self):
        super(DictInfo, self).__init__()
        self.id = 0  # id
        self.dict_type = 0  # 字典类型
        self.dict_name = ""  # 字典名称
        self.dict_value = ""  # 字典值
        self.dict_pic = ""  # 字典图片
        self.sort_index = 0  # 排序
        self.is_release = 0  # 是否发布（1发布0未发布）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间
        self.parent_id = 0  # 父节点
        self.i1 = 0  # i1
        self.i2 = 0  # i2
        self.s1 = ""  # s1
        self.s2 = ""  # s2

    @classmethod
    def get_field_list(self):
        return ['id', 'dict_type', 'dict_name', 'dict_value', 'dict_pic', 'sort_index', 'is_release', 'create_date', 'modify_date', 'parent_id', 'i1', 'i2', 's1', 's2']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "dict_info_tb"
