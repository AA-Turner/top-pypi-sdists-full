# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-12 17:38:51
@LastEditTime: 2024-01-03 10:36:02
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class InviteHelpModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(InviteHelpModel, self).__init__(InviteHelp, sub_table)
        db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_task","redis_task", db_connect_key)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class InviteHelp:

    def __init__(self):
        super(InviteHelp, self).__init__()
        self.id = 0  # id
        self.id_md5 = 0  # id_md5(act_id+module_id+object_id)md5int
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.module_id = 0  # 模块标识
        self.help_type = 0  # 助力类型（0无1邀请用户）
        self.object_id = 0  # 对象标识
        self.user_id = 0  # 邀请人用户标识
        self.open_id = ""  # 邀请人OpenID
        self.invited_user_id = "" # 受邀人用户标识
        self.invited_open_id = ""  # 受邀人OpenID
        self.invited_user_nick = ""  # 受邀人昵称
        self.invited_avatar = ""  # 受邀人头像
        self.is_handle = 0  # 是否处理（1处理0未处理）
        self.is_invited_handle = 0  #受邀人是否处理（1处理0未处理）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_day = 0  # 创建天
        self.i1 = 0  # i1
        self.i2 = 0  # i2
        self.s1 = ''  # s1
        self.s2 = ''  # s2

    @classmethod
    def get_field_list(self):
        return ['id', 'id_md5', 'app_id', 'act_id', 'module_id', 'help_type', 'object_id', 'user_id', 'open_id', 'invited_user_id', 'invited_open_id', 'invited_user_nick', 'invited_avatar', 'is_handle', 'is_invited_handle', 'create_date', 'create_day', 'i1', 'i2', 's1', 's2']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "invite_help_tb"
