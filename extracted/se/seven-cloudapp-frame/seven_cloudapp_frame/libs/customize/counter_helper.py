# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-10-25 18:00:46
@LastEditTime: 2022-12-13 15:06:40
@LastEditors: HuangJianYi
@Description: 
"""

from seven_framework import *
from seven_cloudapp_frame.models.db_models.counter.counter_config_model import *
from seven_cloudapp_frame.libs.customize.redis_helper import *


class CounterHelper:
    """
    :description: 计数帮助类 配置字段说明{"expire":计数过期时间，单位秒,"计数key":{"db_connect_key": 上下文,"table_name": 表名,"id_field_name": 主键字段名,"value_field_name": 返回字段名}}
    :sence:使用场景：1.珀莱雅H5评论列表走缓存，评论数和喜欢数又想保证计数实时 2.库存走reids并自动从数据库同步redis
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def amount(self, key_name, object_id, value, sync_update_db=True):
        """
        :description: 计数
        :param key_name: 计数key
        :param object_id: 对象标识
        :param value: 值
        :param sync_update_db: 是否同步更新数据库
        :return: 
        :last_editors: HuangJianYi 
        """
        try:
            object_id = str(object_id)
            counter_key = "counter:" + key_name
            counter_config_model = CounterConfigModel()
            counter_config_dict = counter_config_model.get_cache_dict("key_name=%s", params=[key_name])
            if not counter_config_dict:
                counter_config_dict = {}
            key_expire = int(counter_config_dict.get("key_expire", 0))
            if counter_config_dict.get("is_release", 0) == 0:
                counter_config_dict = {}
            db_connect_key = counter_config_dict.get("db_connect_key", "db_cloudapp")
            table_name = counter_config_dict.get("table_name", "")
            id_field_name = counter_config_dict.get("id_field_name", "")
            value_field_name = counter_config_dict.get("value_field_name", "")
            db_update_count = 0
            if sync_update_db == True and table_name and id_field_name and value_field_name:
                db = MySQLHelper(config.get_value(db_connect_key))
                sql = f'UPDATE {table_name} SET {value_field_name}={value_field_name}+{value} WHERE {id_field_name}=' + '%s'
                db_update_count = db.update(sql, [object_id])
            if sync_update_db == False or (sync_update_db == True and db_update_count > 0):
                init = RedisExHelper.init()
                count = init.hincrby(counter_key, object_id, value)
                if count == value:
                    db_value = self.get_db_amount(key_name, object_id)
                    init.hincrby(counter_key, object_id, db_value - value)
                if key_expire > 0:
                    init.expire(counter_key, key_expire * 3600)
                return count
            else:
                return 0
        except Exception as ex:
            self.logger_error.error("【计数】" + traceback.format_exc())
            return 0

    @classmethod
    def increment(self, key_name, object_id, value, sync_update_db=True):
        """
        :description: 增加计数
        :param key_name: 计数key
        :param object_id: 对象标识
        :param value: 增加的值
        :param sync_update_db: 是否同步更新数据库
        :return: 
        :last_editors: HuangJianYi 
        """
        return self.amount(key_name, object_id, abs(int(value)), sync_update_db)

    @classmethod
    def decrement(self, key_name, object_id, value, sync_update_db=True):
        """
        :description: 减少计数
        :param key_name: 计数key
        :param object_id: 对象标识
        :param value: 减少的值
        :param sync_update_db: 是否同步更新数据库
        :return: 
        :last_editors: HuangJianYi 
        """
        return self.amount(key_name, object_id, -int(value), sync_update_db)

    @classmethod
    def get_value(self, key_name, object_id):
        """
        :description: 获取计数值
        :param key_name: 计数key
        :param object_id: 对象标识
        :return: 
        :last_editors: HuangJianYi 
        """
        values = self.get_values(key_name, object_id)
        if len(values) > 0:
            return values[0]["value"]
        else:
            return 0

    @classmethod
    def get_values(self, key_name, object_ids):
        """
        :description: 获取计数值
        :param key_name: 计数key
        :param object_id: 对象标识数组
        :return: 
        :last_editors: HuangJianYi 
        """
        counter_key = "counter:" + key_name
        values = []
        init = RedisExHelper.init()
        if isinstance(object_ids, str):
            object_ids = object_ids.split(',')
        if isinstance(object_ids, int):
            object_ids = [str(object_ids)]
        try:
            counter_config_model = CounterConfigModel()
            counter_config_dict = counter_config_model.get_cache_dict("key_name=%s", params=[key_name])
            if not counter_config_dict:
                counter_config_dict = {}
            key_expire = int(counter_config_dict.get("key_expire", 0))
            for object_id in object_ids:
                cur_value = init.hget(counter_key, object_id)
                if cur_value:
                    values.append({"key": object_id, "value": int(cur_value)})
                else:
                    db_value = self.get_db_amount(key_name, object_id)
                    init.hincrby(counter_key, object_id, db_value)
                    if key_expire > 0:
                        init.expire(counter_key, key_expire * 3600)
                    values.append({"key": object_id, "value": db_value})
        except Exception as ex:
            self.logger_error.error("【获取计数值】" + traceback.format_exc())
        return values

    @classmethod
    def get_db_amount(self, key_name, object_id):
        """
        :description: 获取数据库计数值
        :param key_name: 计数key
        :param object_id: 对象标识
        :return: 
        :last_editors: HuangJianYi 
        """
        db_value = 0
        try:
            counter_config_model = CounterConfigModel()
            counter_config_dict = counter_config_model.get_cache_dict("key_name=%s", params=[key_name])
            if not counter_config_dict or counter_config_dict["is_release"] == 0:
                counter_config_dict = {}
            db_connect_key = counter_config_dict.get("db_connect_key", "db_cloudapp")
            table_name = counter_config_dict.get("table_name", "")
            id_field_name = counter_config_dict.get("id_field_name", "")
            value_field_name = counter_config_dict.get("value_field_name", "")
            if table_name and id_field_name and value_field_name:
                db = MySQLHelper(config.get_value(db_connect_key))
                db_value = db.query(f'SELECT {value_field_name} FROM {table_name} WHERE {id_field_name}=' + '%s LIMIT 1;', params=[object_id])
                if len(db_value) <= 0:
                    db_value = 0
                else:
                    db_value = int(db_value[0][value_field_name])
        except Exception as ex:
            self.logger_error.error("【获取数据库计数值】" + traceback.format_exc())
        return db_value
