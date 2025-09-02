# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-19 13:37:16
@LastEditTime: 2025-05-07 09:51:55
@LastEditors: HuangJianYi
@Description: 
"""
import threading, multiprocessing
from seven_cloudapp_frame.libs.common.frame_console import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData
from seven_cloudapp_frame.models.frame_base_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.console_models.timing_work_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_queue_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_orm_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_report_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_log_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_user_report_model import *
from seven_cloudapp_frame.models.db_models.stat.stat_user_log_model import *

class StatConsoleModel():
    """
    :description: 统计控制台业务模型
    """
    def __init__(self):
        """
        :description: 初始化
        :return: 
        :last_editors: HuangJianYi
        """
        self.db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_stat","redis_stat")

    def console_stat_queue(self, mod_count=1):
        """
        :description: 控制台统计上报
        :param mod_count: 单表队列数
        :return: 
        :last_editors: HuangJianYi
        """
        stat_config = share_config.get_value("stat_config", {})
        is_process_stat = stat_config.get("is_process_stat", True)
        if is_process_stat:
            stat_process_ways = share_config.get_value("stat_process_ways", "redis")
            if stat_process_ways == "mysql":
                for i in range(mod_count):
                    t = threading.Thread(target=self._process_stat_queue, args=[i, mod_count])
                    t.start()
            else:
                for i in range(10):
                    j = threading.Thread(target=self._process_redis_stat_queue, args=[i])
                    j.start()

            clea_data_work = ClearDataWork()
            clea_data_work.start_hours = 2
            clea_data_work.end_hours = 4
            clea_data_work.sleep_time = 3600
            clea_data_work.db_connect_key = self.db_connect_key
            clea_data_work.start_work("清理统计流水数据作业")

        is_process_stat_user = stat_config.get("is_process_stat_user",False)
        if is_process_stat_user:
            for i in range(10):
                k = threading.Thread(target=self._process_redis_stat_user_queue, args=[i])
                k.start()

            stat_user_data_work = StatUserDataWork()
            stat_user_data_work.start_hours = 2
            stat_user_data_work.end_hours = 4
            stat_user_data_work.sleep_time = 3600
            stat_user_data_work.db_connect_key = self.db_connect_key
            stat_user_data_work.start_work("处理统计用户数据作业")


    def _process_stat_queue(self, mod_value, mod_count):
        """
        :description: 处理mysql统计队列
        :param mod_value: 当前队列值
        :param mod_count: 队列数
        :return: 
        :last_editors: HuangJianYi
        """
        print(f"{TimeHelper.get_now_format_time()} 统计队列{mod_value}启动")
        while True:
            try:
                time.sleep(0.1)
                heart_beat_monitor(f"_process_stat_queue_{mod_value}")
                db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key))
                stat_queue_model = StatQueueModel(db_transaction=db_transaction)
                stat_orm_model = StatOrmModel(is_auto=True)
                now_date = TimeHelper.get_now_format_time()
                if mod_count == 1:
                    # 为了避免删数据导致空表进行主键重置，所以默认不删除第一条数据
                    stat_queue_list = stat_queue_model.get_list(f"process_count<10 and '{now_date}'>process_date and id>1", order_by="process_date asc", limit="200")
                else:
                    stat_queue_list = stat_queue_model.get_list(f"MOD(user_id,{mod_count})={mod_value} and process_count<10 and '{now_date}'>process_date and id>1", order_by="process_date asc", limit="200")
                if len(stat_queue_list) > 0:
                    for stat_queue in stat_queue_list:
                        try:
                            stat_report_model = StatReportModel(db_transaction=db_transaction)
                            stat_orm = stat_orm_model.get_cache_entity("((act_id=%s and module_id=%s and object_id=%s) or (act_id=0 and module_id=0 and object_id='')) and key_name=%s", params=[stat_queue.act_id, stat_queue.module_id, stat_queue.object_id, stat_queue.key_name])
                            if not stat_orm:
                                stat_queue_model.del_entity("id=%s", params=[stat_queue.id])
                                continue
                            create_date = TimeHelper.format_time_to_datetime(stat_queue.create_date)
                            create_day_int = int(create_date.strftime('%Y%m%d'))
                            create_month_int = int(create_date.strftime('%Y%m'))
                            create_year_int = int(create_date.strftime('%Y'))
                            stat_log_model = StatLogModel(db_transaction=db_transaction).set_sub_table(stat_queue.app_id)
                            is_add = True
                            if stat_orm.repeat_type > 0:
                                if stat_orm.repeat_type == 2:
                                    stat_log_dict = stat_log_model.get_cache_dict("act_id=%s and module_id=%s and orm_id=%s and user_id=%s and object_id=%s", field="id", params=[stat_queue.act_id, stat_queue.module_id, stat_orm.id, stat_queue.user_id, stat_queue.object_id])
                                else:
                                    stat_log_dict = stat_log_model.get_cache_dict("act_id=%s and module_id=%s and orm_id=%s and user_id=%s and create_day=%s and object_id=%s", field="id", params=[stat_queue.act_id, stat_queue.module_id, stat_orm.id, stat_queue.user_id, create_day_int, stat_queue.object_id])
                                if stat_log_dict:
                                    is_add = False

                            stat_log = StatLog()
                            stat_log.app_id = stat_queue.app_id
                            stat_log.act_id = stat_queue.act_id
                            stat_log.module_id = stat_queue.module_id
                            stat_log.orm_id = stat_orm.id
                            stat_log.user_id = stat_queue.user_id
                            stat_log.open_id = stat_queue.open_id
                            stat_log.key_value = stat_queue.key_value
                            stat_log.create_day = create_day_int
                            stat_log.create_month = create_month_int
                            stat_log.create_date = create_date

                            stat_report_condition = "act_id=%s and module_id=%s and object_id=%s and key_name=%s and create_day=%s"
                            stat_report_param = [stat_queue.act_id, stat_queue.module_id, stat_queue.object_id, stat_queue.key_name, create_day_int]
                            stat_report_dict = stat_report_model.get_dict(stat_report_condition, params=stat_report_param)

                            db_transaction.begin_transaction()
                            if is_add:
                                if not stat_report_dict:
                                    stat_report = StatReport()
                                    stat_report.app_id = stat_queue.app_id
                                    stat_report.act_id = stat_queue.act_id
                                    stat_report.module_id = stat_queue.module_id
                                    stat_report.object_id = stat_queue.object_id
                                    stat_report.key_name = stat_queue.key_name
                                    stat_report.key_value = stat_queue.key_value
                                    stat_report.create_date = create_date
                                    stat_report.create_year = create_year_int
                                    stat_report.create_month = create_month_int
                                    stat_report.create_day = create_day_int
                                    stat_report_model.add_entity(stat_report)
                                else:
                                    stat_report_model.update_table(f"key_value=key_value+{stat_queue.key_value}", stat_report_condition, params=stat_report_param)
                                stat_log_model.add_entity(stat_log)
                            stat_queue_model.del_entity("id=%s", params=[stat_queue.id])
                            result,message = db_transaction.commit_transaction(True)
                            if result == False:
                                raise Exception("执行事务失败", message)
                        except Exception as ex:
                            stat_queue.process_count += 1
                            if stat_queue.process_count <= 10:
                                stat_queue.process_result = f"出现异常,json串:{SevenHelper.json_dumps(stat_queue)},ex:{traceback.format_exc()}"
                                minute = 1 if stat_queue.process_count <= 5 else 5
                                stat_queue.process_date = TimeHelper.add_minutes_by_format_time(minute=minute)
                                stat_queue_model.update_entity(stat_queue, "process_count,process_result,process_date")
                            else:
                                logger_error.error(f"统计队列{mod_value}异常,json串:{SevenHelper.json_dumps(stat_queue)},ex:{traceback.format_exc()}")
                            continue
                else:
                    time.sleep(1)
            except Exception as ex:
                logger_error.error(f"统计队列{mod_value}异常,ex:{traceback.format_exc()}")
                time.sleep(5)


    def _process_redis_stat_queue(self, mod_value):
        """
        :description: 处理redis统计队列
        :param mod_value: 当前队列值
        :return: 
        :last_editors: HuangJianYi
        """
        print(f"{TimeHelper.get_now_format_time()} 统计队列{mod_value}启动")

        while True:
            try:
                time.sleep(0.1)
                heart_beat_monitor(f"_process_redis_stat_queue_{mod_value}")
                redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
                redis_stat_key = f"stat_queue_list:{mod_value}"
                check_redis_stat_key = f"stat_queue_list:check:{mod_value}"
                stat_queue_json = redis_init.rpoplpush(redis_stat_key, check_redis_stat_key)
                if not stat_queue_json:
                    time.sleep(1)
                    continue
                try:
                    stat_queue_dict = SevenHelper.json_loads(stat_queue_json)
                    db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key))
                    stat_orm_model = StatOrmModel(is_auto=True)
                    stat_report_model = StatReportModel(db_transaction=db_transaction)
                    stat_orm = stat_orm_model.get_cache_entity("((act_id=%s and module_id=%s and object_id=%s) or (act_id=0 and module_id=0 and object_id='')) and key_name=%s", params=[stat_queue_dict["act_id"], stat_queue_dict["module_id"], stat_queue_dict.get("object_id", ''), stat_queue_dict["key_name"]])
                    if not stat_orm:
                        redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)
                        continue
                    create_date = TimeHelper.format_time_to_datetime(stat_queue_dict["create_date"])
                    create_day_int = int(create_date.strftime('%Y%m%d'))
                    create_month_int = int(create_date.strftime('%Y%m'))
                    create_year_int = int(create_date.strftime('%Y'))
                    stat_log_model = StatLogModel(db_transaction=db_transaction).set_sub_table(stat_queue_dict["app_id"])
                    is_add = True
                    if stat_orm.repeat_type > 0:
                        if stat_orm.repeat_type == 2:
                            stat_log_dict = stat_log_model.get_cache_dict("act_id=%s and module_id=%s and orm_id=%s and user_id=%s and object_id=%s", field="id", params=[stat_queue_dict["act_id"], stat_queue_dict["module_id"], stat_orm.id, stat_queue_dict["user_id"], stat_queue_dict.get("object_id",'')])
                        else:
                            stat_log_dict = stat_log_model.get_cache_dict("act_id=%s and module_id=%s and orm_id=%s and user_id=%s and create_day=%s and object_id=%s", field="id", params=[stat_queue_dict["act_id"], stat_queue_dict["module_id"], stat_orm.id, stat_queue_dict["user_id"], create_day_int, stat_queue_dict.get("object_id",'')])
                        if stat_log_dict:
                            is_add = False

                    stat_log = StatLog()
                    stat_log.app_id = stat_queue_dict["app_id"]
                    stat_log.act_id = stat_queue_dict["act_id"]
                    stat_log.module_id = stat_queue_dict["module_id"]
                    stat_log.object_id = stat_queue_dict.get("object_id",'')
                    stat_log.orm_id = stat_orm.id
                    stat_log.user_id = stat_queue_dict["user_id"]
                    stat_log.open_id = stat_queue_dict["open_id"]
                    stat_log.key_value = stat_queue_dict["key_value"]
                    stat_log.create_day = create_day_int
                    stat_log.create_month = create_month_int
                    stat_log.create_date = create_date

                    stat_report = StatReport()
                    stat_report.app_id = stat_queue_dict["app_id"]
                    stat_report.act_id = stat_queue_dict["act_id"]
                    stat_report.module_id = stat_queue_dict["module_id"]
                    stat_report.object_id = stat_queue_dict.get("object_id",'')
                    stat_report.key_name = stat_queue_dict["key_name"]
                    stat_report.key_value = stat_queue_dict["key_value"]
                    stat_report.create_date = create_date
                    stat_report.create_year = create_year_int
                    stat_report.create_month = create_month_int
                    stat_report.create_day = create_day_int

                    if is_add:
                        db_transaction.begin_transaction()
                        stat_report_model.add_update_entity(stat_report, update_sql=f"key_value=key_value+{stat_queue_dict['key_value']}")
                        stat_log_model.add_entity(stat_log)
                        result, message = db_transaction.commit_transaction(True)
                        if result == False:
                            raise Exception("执行事务失败", message)

                    redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)

                except Exception as ex:
                    if "Duplicate entry" not in traceback.format_exc():
                        redis_init.lpush(redis_stat_key, stat_queue_json)
                        redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)
                        logger_error.error(f"统计队列{mod_value}异常,json串:{SevenHelper.json_dumps(stat_queue_dict)},ex:{traceback.format_exc()}")
                    continue

            except Exception as ex:
                logger_error.error(f"统计队列{mod_value}异常,ex:{traceback.format_exc()}")
                time.sleep(5)


    def _process_redis_stat_user_queue(self, mod_value):
        """
        :description: 处理redis统计用户队列
        :param mod_value: 当前队列值
        :return: 
        :last_editors: HuangJianYi
        """
        print(f"{TimeHelper.get_now_format_time()} 统计用户队列{mod_value}启动")

        while True:
            try:
                time.sleep(0.1)
                heart_beat_monitor(f"_process_redis_stat_user_queue_{mod_value}")
                db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key))
                redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
                redis_stat_key = f"stat_user_queue_list:{mod_value}"
                check_redis_stat_key = f"stat_user_queue_list:check:{mod_value}"
                stat_queue_json = redis_init.rpoplpush(redis_stat_key, check_redis_stat_key)
                if not stat_queue_json:
                    time.sleep(1)
                    continue
                try:
                    stat_queue_dict = SevenHelper.json_loads(stat_queue_json)
                    stat_user_log_model = StatUserLogModel(db_transaction=db_transaction).set_sub_table(stat_queue_dict["app_id"])
                    stat_user_report_model = StatUserReportModel(db_transaction=db_transaction)
                    create_date = TimeHelper.format_time_to_datetime(stat_queue_dict["create_date"])
                    create_day_int = int(create_date.strftime('%Y%m%d'))
                    create_month_int = int(create_date.strftime('%Y%m'))
                    create_year_int = int(create_date.strftime('%Y'))
                    field_name = stat_queue_dict["key_name"]

                    stat_user_log = StatUserLog()
                    stat_user_log.app_id = stat_queue_dict["app_id"]
                    stat_user_log.act_id = stat_queue_dict["act_id"]
                    stat_user_log.module_id = stat_queue_dict["module_id"]
                    stat_user_log.user_id = stat_queue_dict["user_id"]
                    stat_user_log.open_id = stat_queue_dict["open_id"]
                    stat_user_log.key_name = field_name
                    stat_user_log.key_value = stat_queue_dict["key_value"]
                    stat_user_log.request_code = stat_queue_dict.get("request_code","")
                    stat_user_log.create_day = create_day_int
                    stat_user_log.create_month = create_month_int
                    stat_user_log.create_date = create_date

                    stat_report_condition = "act_id=%s and module_id=%s and create_day=%s and user_id=%s and app_id=%s"
                    stat_report_param = [stat_queue_dict["act_id"], stat_queue_dict["module_id"], create_day_int, stat_queue_dict["user_id"], stat_queue_dict["app_id"]]
                    stat_report_dict = stat_user_report_model.get_dict(stat_report_condition, params=stat_report_param)
                    if not stat_report_dict:
                        stat_user_report = StatUserReport()
                        stat_user_report.app_id = stat_queue_dict["app_id"]
                        stat_user_report.act_id = stat_queue_dict["act_id"]
                        stat_user_report.module_id = stat_queue_dict["module_id"]
                        stat_user_report.user_id = stat_queue_dict["user_id"]
                        stat_user_report.open_id = stat_queue_dict["open_id"]
                        stat_user_report.create_date = create_date
                        stat_user_report.create_year = create_year_int
                        stat_user_report.create_month = create_month_int
                        stat_user_report.create_day = create_day_int
                        stat_user_report_model.add_entity(stat_user_report)

                    db_transaction.begin_transaction()
                    key_value = stat_queue_dict["key_value"]
                    stat_user_report_model.update_table(f"{field_name}={field_name}+{key_value}", stat_report_condition, params=stat_report_param)
                    stat_user_log_model.add_entity(stat_user_log)
                    result,message = db_transaction.commit_transaction(True)
                    if result == False:
                        raise Exception("执行事务失败", message)

                    redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)

                except Exception as ex:
                    if "Duplicate entry" not in traceback.format_exc():
                        redis_init.lpush(redis_stat_key, stat_queue_json)
                        redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)
                        logger_error.error(f"统计用户队列{mod_value}异常,json串:{SevenHelper.json_dumps(stat_queue_dict)},ex:{traceback.format_exc()}")
                    continue

            except Exception as ex:
                logger_error.error(f"统计用户队列{mod_value}异常,ex:{traceback.format_exc()}")
                time.sleep(5)


class ClearDataWork(TimingWork):
    """
    :description: 清理数据
    :return: 
    :last_editors: HuangJianYi
    """
    def execute(self):
        heart_beat_monitor("ClearDataWork", check_time=2*24*60)
        invoke_result_data = InvokeResultData()
        self.process_only_table()

        return invoke_result_data

    def process_only_table(self):
        """
        :description: 处理单表
        :return: 
        :last_editors: HuangJianYi
        """
        stat_log_model = StatLogModel()
        stat_orm_model = StatOrmModel()
        page_index = 0
        while True:
            stat_orm_dict_list, is_next = stat_orm_model.get_dict_page_list(field="id,repeat_type", page_index=page_index, page_size=200, order_by="id asc", page_count_mode="next")
            if len(stat_orm_dict_list) <= 0:
                break
            for stat_orm_dict in stat_orm_dict_list:
                if stat_orm_dict["repeat_type"] != 2:
                    while True:
                        is_del = stat_log_model.del_entity("orm_id=%s and create_day<%s", params=[stat_orm_dict["id"], SevenHelper.get_now_day_int(-24 * 15)], limit="100")
                        if is_del == False:
                            break
            page_index += 1


class StatUserDataWork(TimingWork):
    """
    :description: 处理统计用户数据（用户汇总报表只保留1年的记录，流水只保留1个月）
    :return: 
    :last_editors: HuangJianYi
    """

    def execute(self):
        heart_beat_monitor("StatUserDataWork", check_time=2*24*60)
        invoke_result_data = InvokeResultData()
        self.clear_log()
        self.clear_report()
        return invoke_result_data

    def clear_log(self):
        """
        :description: 清理流水
        :return: 
        :last_editors: HuangJianYi
        """
        stat_log_model = StatUserLogModel()
        stat_config = share_config.get_value("stat_config", {})
        space_day = int(stat_config.get("user_log_space_day", 30))
        while True:
            is_del = stat_log_model.del_entity("create_day<%s", params=[SevenHelper.get_now_day_int(-24 * space_day)], limit="100")
            if is_del == False:
                break

    def clear_report(self):
        """
        :description: 清理报表(用户统计表需要按年创建分表，然后把数据加入到对应的年分表中，没建表则无法清理报表)
        :return: 
        :last_editors: HuangJianYi
        """
        stat_user_report_model = StatUserReportModel()
        stat_config = share_config.get_value("stat_config", {})
        space_day = int(stat_config.get("user_report_space_day", 365))
        while True:
            stat_user_report_list = stat_user_report_model.get_list(where="create_day<%s", order_by="id asc", limit="200", params=[SevenHelper.get_now_day_int(-24 * space_day)])
            if len(stat_user_report_list) <= 0:
                break
            for item in stat_user_report_list:
                create_year = item.create_year
                stat_user_report_year_model = StatUserReportModel(sub_table=f"{create_year}")
                stat_user_report_year_model.add_entity(item)
                stat_user_report_model.del_entity("id=%s", params=[item.id])
