# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-02 10:11:35
@LastEditTime: 2024-01-03 10:38:13
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class OperationLogModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(OperationLogModel, self).__init__(OperationLog, sub_table)
        db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_cms","redis_cms", db_connect_key)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类

class OperationLog:

    def __init__(self):
        super(OperationLog, self).__init__()
        self.id = 0  # id
        self.app_id = ""  # 应用标识
        self.act_id = 0  # 活动标识
        self.operation_type = 0  # 操作类型：1-add，2-update，3-delete 4-还原 5-复制
        self.title = ""  # 标题
        self.operation_desc = "" # 描述
        self.detail = ""  # 当前信息
        self.update_detail = ""  # 更新之后的信息
        self.request_params = ""  # 传入的参数
        self.model_name = ""  # 模块或表名称
        self.operation_ways = 1  # 操作方式(1单一操作2批量操作)
        self.protocol = ""  # protocol(http或https)
        self.method = ""  # method
        self.handler_name = ""  # handler_name
        self.request_host = ""  # request_host
        self.request_uri = ""  # request_uri
        self.remote_ip = ""  # remote_ip
        self.request_code = "" # 请求代码
        self.operate_user_id = ""  # 操作人标识
        self.operate_user_name = ""  # 操作人名称
        self.operate_role_id = ""  # 操作角色标识
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_day = 0  # 创建天


    @classmethod
    def get_field_list(self):
        return ['id', 'app_id', 'act_id', 'operation_type', 'title', 'operation_desc', 'detail', 'update_detail', 'request_params', 'model_name', 'operation_ways', 'protocol', 'method', 'handler_name', 'request_host', 'request_uri', 'remote_ip', 'request_code', 'operate_user_id', 'operate_user_name', 'operate_role_id', 'create_date', 'create_day']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "operation_log_tb"
