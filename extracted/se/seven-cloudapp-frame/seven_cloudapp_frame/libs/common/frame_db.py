# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2024-01-18 18:19:58
@LastEditTime: 2025-05-28 19:46:16
@LastEditors: HuangJianYi
:Description: 框架DB操作类
"""
from seven_framework.base_model import *
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *


class FrameDbModel(BaseModel):

    def __init__(self, model_class, sub_table):
        """
        :Description: 框架DB操作类
        :param model_class: 实体对象类
        :param sub_table: 分表标识
        :last_editors: HuangJianYi
        """
        super(FrameDbModel,self).__init__(model_class, sub_table)

    def add_list_batch(self, data_list, batch_num=100):
        """
        :description: 分批添加数据
        :param data_list：数据列表
        :param batch_num：分批数量
        :return 成功添加的数量
        :last_editors: HuangJianYi
        """
        page_index = 0
        total = 0
        while True:
            add_list = data_list[page_index * batch_num:(page_index + 1) * batch_num]
            if not add_list:
                return total
            result = self.add_list(add_list)
            if result == True:
                total += len(add_list)
            page_index += 1

    def set_sub_table(self, object_id=''):
        """
        :description: 设置分表
        :param object_id:object_id
        :return:
        :last_editors: HuangJianYi
        """
        table_name = str(self.model_obj).lower()
        sub_table_config = share_config.get_value("sub_table_config",{})
        table_config = sub_table_config.get(table_name, None)
        if table_config and object_id:
            calculate_type = sub_table_config.get("calculate_type", 1) # 1-默认 2-去掉最后1位再取模（淘宝的应用标识尾数只有1-5会导致分布不均）
            if calculate_type == 2:
                from seven_cloudapp_frame.models.enum import PlatType
                calculate_value = sub_table_config.get("calculate_value")
                plat_type = share_config.get_value("plat_type", PlatType.tb.value)  # 平台类型
                if calculate_value and plat_type == PlatType.tb.value:
                    first_value = int(object_id[0:11]) # 取前11位
                    if first_value >= int(calculate_value):
                        object_id = object_id[:-1]
                else:
                    object_id = object_id[:-1]

            sub_table = SevenHelper.get_sub_table(object_id, table_config.get("sub_count", 10))
            if sub_table:
                # 数据库表名
                self.table_name = table_name.replace("_tb", f"_{sub_table}_tb")
        return self

    def set_view(self, view_name=''):
        """
        :description: 设置视图
        :param view_name:视图名
        :return:
        :last_editors: HuangJianYi
        """
        table_name = str(self.model_obj).lower()
        if not view_name:
            self.table_name = table_name.replace("_tb", "_view")
        else:
            self.table_name = view_name
        return self

    def relation_and_merge_dict_list(self, primary_dict_list, relation_db_model, relation_key_field, field="*", primary_key_field="id", is_cache=True, dependency_key="", cache_expire=1800):
        """
        :description: 根据给定的主键表关联ID数组从关联表获取字典列表合并。
        :param primary_dict_list: 主表字典列表
        :param relation_db_model: 关联表关联model
        :param relation_key_field:  关联表关联字段
        :param field: 关联表查询字段
        :param primary_key_field: 主表关联字段
        :param is_cache: 是否开启缓存（1-是 0-否）
        :param dependency_key: 缓存依赖键
        :param cache_expire: 缓存过期时间（秒）
        :return:
        :last_editors: HuangJianYi
        """
        if len(primary_dict_list) <= 0:
            return primary_dict_list
        # 检查relation_key_field是否已经在field中
        if field != "*" and relation_key_field not in field.split(","):
            field = f"{relation_key_field},{field}"
        ext_table_ids = [i[primary_key_field] for i in primary_dict_list]
        where = SevenHelper.get_condition_by_int_list(relation_key_field, ext_table_ids)
        if is_cache == True:
            relation_dict_list = relation_db_model.get_cache_dict_list(where, field=field, dependency_key=dependency_key, cache_expire=cache_expire)
        else:
            relation_dict_list = relation_db_model.get_dict_list(where, field=field)
        dict_list = SevenHelper.merge_dict_list(primary_dict_list, primary_key_field, relation_dict_list, relation_key_field, exclude_merge_columns_names="id")
        return dict_list

    def relation_and_merge_dict(self, primary_dict, relation_db_model, field="*", primary_key_field="id", is_cache=True, dependency_key="", cache_expire=1800):
        """
        :description: 根据给定的主键表字典合并关联表字典。
        :param primary_dict: 主表字典
        :param relation_db_model: 关联表关联model
        :param field: 关联表查询字段
        :param primary_key_field: 主表关联字段
        :param is_cache: 是否开启缓存（1-是 0-否）
        :param dependency_key: 缓存依赖键
        :param cache_expire: 缓存过期时间（秒）
        :return:
        :last_editors: HuangJianYi
        """
        if not primary_dict:
            return primary_dict
        if is_cache == True:
            relation_dict = relation_db_model.get_cache_dict_by_id(primary_dict[primary_key_field], field=field, dependency_key=dependency_key, cache_expire=cache_expire)
        else:
            relation_dict = relation_db_model.get_dict_by_id(primary_dict[primary_key_field], field=field)
        if relation_dict and "id" in relation_dict:
            del relation_dict["id"]
        if relation_dict:
            primary_dict.update(relation_dict)
        return primary_dict

    def call_procedure(self, procedure_name: str, params: list = None):
        """
        :Description: 调用存储过程
        :param procedure_name: 存储过程名称
        :param params: 参数值(数组)
        :return: 存储过程的结果
        """
        self.db.connection()
        try:
            with self.db._conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.callproc(procedure_name, params)
                result = cursor.fetchall()
            self.db._conn.commit()
            return result
        except Exception as e:
            self.db._conn.rollback()
            print(traceback.print_exc())
            raise Exception("mysql execute error:" + str(e) + " procedure:" +
                            str(procedure_name) + " 参数:" + str(params))
        finally:
            self.db._conn.close()

    def convert_db_config(self, db_connect_key, is_auto=False):
        """
        :Description: 转换最终的连接串配置
        :param db_connect_key: db_connect_key
        :param is_auto: True-有主从配置，根据语句自动分配读写库
        :return: 
        """
        if isinstance(db_connect_key, str):
            db_config = config.get_value(db_connect_key)
        else:
            db_config = db_connect_key
        if not db_config:
            return db_config
        covert_config = {}
        if is_auto:
            covert_config["host"] = db_config.get("auto_host", db_config.get("host", ""))
            covert_config["port"] = db_config.get("auto_port", db_config.get("port", ""))
            covert_config["user"] = db_config.get("auto_user", db_config.get("user", ""))
            covert_config["passwd"] = db_config.get("auto_password", db_config.get("passwd", ""))
        else:
            covert_config["host"] = db_config.get("host", "")
            covert_config["port"] = db_config.get("port", "")
            covert_config["user"] = db_config.get("user", "")
            covert_config["passwd"] = db_config.get("passwd", "")

        covert_config["db"] = db_config.get("db", "")
        covert_config["charset"] = db_config.get("charset", "")
        return covert_config

    def add_values(self, model_list, ignore=False, is_doris=False, update_feild_list=None, exclude_update_feild_list=None):
        """
        :description: 一次性数据写入(insert into... values(...),(...),(...);)
        :param model_list: 数据模型列表
        :param ignore: 忽略已存在的记录
        :param is_doris: 是否doris
        :param update_feild_list: 触发唯一键时需要更新的字段列表(doris=True)
        :param exclude_update_feild_list: 触发唯一键时需排除更新的字段列表(doris=True)
        :return 成功True 失败False
        :last_editors: HuangJingCan
        """
        if not model_list or len(model_list) == 0:
            return False

        field_list = self.model_obj.get_field_list()
        if len(field_list) == 0:
            return False

        if is_doris is True:
            if update_feild_list:
                field_list = [field for field in field_list if field in update_feild_list]
            elif exclude_update_feild_list:
                field_list = [field for field in field_list if field not in exclude_update_feild_list]

        insert_field_str = ""
        for field_str in field_list:
            if str(field_str).lower() == self.primary_key_field.lower() and not is_doris:
                continue
            insert_field_str += str(f"`{field_str}`,")

        insert_field_str = insert_field_str.rstrip(',')
        doris_sql = "set enable_unique_key_partial_update=true; set enable_insert_strict=false;" if is_doris else ""
        sql = f"{doris_sql} INSERT{' IGNORE' if ignore else ''} INTO {self.table_name}({insert_field_str}) VALUES "
        param = []

        for model in model_list:
            insert_value_str = ""
            for field_str in field_list:
                param_value = str(getattr(model, field_str))
                if str(field_str).lower() == self.primary_key_field.lower() and not is_doris:
                    continue
                insert_value_str += "%s,"
                param.append(param_value)

            insert_value_str = insert_value_str.rstrip(',')
            sql += f"({insert_value_str}),"

        sql = sql.rstrip(',') + ";"

        if self.is_transaction():
            sql_item = {}
            sql_item["sql"] = sql
            sql_item["params"] = tuple(param)
            self.db_transaction.transaction_list.append(sql_item)
        else:
            self.db.insert(sql, tuple(param), False)
        return True
