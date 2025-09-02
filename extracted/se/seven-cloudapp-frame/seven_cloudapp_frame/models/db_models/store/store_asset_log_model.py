# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-15 17:17:08
@LastEditTime: 2023-07-19 09:47:20
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *


class StoreAssetLogModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None, is_auto=False):
        super(StoreAssetLogModel, self).__init__(StoreAssetLog, sub_table)
        db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_asset","redis_asset", db_connect_key)
        self.db = MySQLHelper(self.convert_db_config(db_connect_key, is_auto))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class StoreAssetLog:

    def __init__(self):
        super(StoreAssetLog, self).__init__()
        self.id = 0  # id
        self.store_id = 0  # 店铺ID
        self.store_name = 0  # 店铺名称
        self.app_id = ""  # 应用标识
        self.log_title = ""  # 标题
        self.info_json = ""  # 详情信息
        self.asset_type = 0  # 资产类型(1-次数2-积分3-价格档位)
        self.asset_object_id = ""  # 资产对象标识（比如资产类型是价格档位则对应档位id）
        self.source_type = 0  # 来源类型（1-购买2-任务3-手动配置4-抽奖5-回购6-兑换.业务自定义类型从101起，避免跟公共冲突）
        self.source_object_id = ""  # 来源对象标识(比如来源类型是任务则对应任务类型)
        self.source_object_name = ""  # 来源对象名称(比如来源类型是任务则对应任务名称)
        self.only_id = ""  # 唯一标识(用于并发操作时校验避免重复操作)
        self.operate_type = 0  # 操作类型 （0累计 1消耗）
        self.operate_value = 0  # 操作值
        self.history_value = 0  # 历史值
        self.now_value = 0  # 当前值
        self.handler_name = ""  # 接口名称
        self.request_code = ""  # 请求代码
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_day = 0  # 创建天
        self.warn_date = "1900-01-01 00:00:00"  # 预警时间
        self.warn_day = 0  # 预警天
        self.i1 = 0  # i1
        self.s1 = ""  # s1

    @classmethod
    def get_field_list(self):
        return ['id', 'store_id', 'store_name', 'app_id', 'log_title', 'info_json', 'asset_type', 'asset_object_id', 'source_type', 'source_object_id', 'source_object_name', 'only_id', 'operate_type', 'operate_value', 'history_value', 'now_value', 'handler_name', 'request_code', 'create_date', 'create_day', 'warn_date', 'warn_day', 'i1', 's1']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "store_asset_log_tb"
