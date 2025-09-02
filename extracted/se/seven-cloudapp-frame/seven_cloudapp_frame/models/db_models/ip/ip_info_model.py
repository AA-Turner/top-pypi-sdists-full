# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-27 10:55:09
@LastEditTime: 2022-09-28 17:52:56
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class IpInfoModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(IpInfoModel, self).__init__(IpInfo, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class IpInfo:

    def __init__(self):
        super(IpInfo, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.ip_name = ""  # ip名称
        self.mode_type = 0  # 模式类型
        self.ip_type = 0  # ip类型
        self.ip_pic = ""  # ip图片
        self.show_pic = ""  # 展示图片
        self.ip_summary = ""  # ip描述
        self.sort_index = 0  # 排序
        self.is_release = 0  # 是否发布（1发布0未发布）
        self.is_del = 0  # 是否删除（1是0否）
        self.del_date = "1900-01-01 00:00:00"  # 删除时间
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.ip_config_json = ""  # 配置信息json


    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'ip_name', 'mode_type', 'ip_type', 'ip_pic', 'show_pic', 'ip_summary', 'sort_index', 'is_release', 'is_del', 'del_date', 'create_date', 'modify_date', 'ip_config_json']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "ip_info_tb"
