# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2022-12-15 10:52:33
@LastEditTime: 2023-04-07 16:09:03
@LastEditors: HuangJianYi
:Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class FunctionShopModel(CacheModel):
    def __init__(self, db_connect_key='db_middler_platform', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(FunctionShopModel, self).__init__(FunctionShop, sub_table)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class FunctionShop:
    def __init__(self):
        super(FunctionShop, self).__init__()
        self.id = 0  # id
        self.product_id = 0  # 产品id
        self.cloud_app_id = 0  # 云应用id
        self.store_name = ""  # 店铺名称
        self.store_user_nick = ""  # 店铺主帐号名称（会员名）
        self.user_type = 0  # 用户类型：1-SAAS用户2-SAAS定制用户
        self.app_key = ""  # 商家实例化的app_key
        self.app_id = ""  # app_id
        self.trade_type = 0  # 行业类型（枚举型）
        self.service_date_start = "1900-01-01 00:00:00"  # 服务开始时间
        self.service_date_end = "1900-01-01 00:00:00"  # 服务结束时间
        self.skin_ids = ""  # 皮肤id列表（逗号隔开）
        self.function_ids = ""  # 功能id列表（逗号隔开）
        self.is_erp = 0  # 是否开启erp：0未开启1已开启
        self.erp_id = 0  # erp关联id（遁甲系统获取）
        self.erp_config_info = ""  # erp信息（json列表：{key:'字段名',value:'值'}）
        self.module_name = ""  # 模块名称
        self.module_pic = ""  # 模块图片
        self.is_release = 0  # 是否发布：0未发布1已发布
        self.release_date = "1900-01-01 00:00:00"  # 发布时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'product_id', 'cloud_app_id', 'store_name', 'store_user_nick', 'user_type', 'app_key', 'app_id', 'trade_type', 'service_date_start', 'service_date_end', 'skin_ids', 'function_ids', 'is_erp', 'erp_id', 'erp_config_info', 'module_name', 'module_pic', 'is_release', 'release_date', 'modify_date', 'create_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "function_shop_tb"
