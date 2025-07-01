# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-09-13 16:26:10
@LastEditTime: 2025-06-30 19:11:43
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class QueueupLogModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(QueueupLogModel, self).__init__(QueueupLog, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class QueueupLog:
    def __init__(self):
        super(QueueupLog, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.user_id = 0  # 用户标识
        self.open_id = ""  # open_id
        self.user_nick = ""  # 用户昵称
        self.queue_name = ""  # 队列名称
        self.queue_no = ""  # 排队号
        self.operate_type = 0  # 操作类型(1-加入队列 2-排到队列 3-参与抽赏 4-自动退出 5-手动退出)
        self.ip_name = ""  # 主题名称
        self.ip_id = 0  # 主题标识
        self.module_name = ""  # 模块名称
        self.module_id = 0  # 模块标识
        self.remain_time = 0  # 剩余时间(单位秒)
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_day = 0  # 创建时间天

    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'user_id', 'open_id', 'user_nick', 'queue_name', 'queue_no', 'operate_type', 'ip_name', 'ip_id', 'module_name', 'module_id', 'remain_time', 'create_date', 'create_day']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "queueup_log_tb"
