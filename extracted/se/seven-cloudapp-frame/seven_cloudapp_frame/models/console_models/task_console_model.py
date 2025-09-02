# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-19 13:37:16
@LastEditTime: 2023-07-19 10:43:02
@LastEditors: HuangJianYi
@Description: 
"""
import threading
from seven_cloudapp_frame.libs.common.frame_console import *
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.frame_base_model import *
from seven_cloudapp_frame.models.task_base_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.db_models.task.task_gear_count_model import *
from seven_cloudapp_frame.models.db_models.task.task_info_model import *
from seven_cloudapp_frame.models.db_models.task.task_count_model import *


class TaskConsoleModel():
    """
    :description: 任务控制台业务模型
    """

    def __init__(self):
        """
        :description: 初始化
        :return: 
        :last_editors: HuangJianYi
        """
        self.db_connect_key, self.redis_config_dict = SevenHelper.get_connect_config("db_task","redis_task")

    def console_task_queue(self):
        """
        :description: 控制台统计上报
        :return: 
        :last_editors: HuangJianYi
        """
        for i in range(10):
            j = threading.Thread(target=self.process_task_queue, args=[i])
            j.start()

    def process_task_queue(self, mod_value):
        """
        :description: 处理档位任务队列
        :param mod_value: 当前队列值
        :return: 
        :last_editors: HuangJianYi
        """
        print(f"{TimeHelper.get_now_format_time()} 档位任务队列{mod_value}启动")

        while True:
            try:
                time.sleep(0.1)
                heart_beat_monitor("process_task_queue")
                redis_init = SevenHelper.redis_init(config_dict=self.redis_config_dict)
                redis_key = f"task_gear_list:{mod_value}"
                task_queue_json = redis_init.lindex(redis_key, index=0)
                if not task_queue_json:
                    time.sleep(1)
                    continue
                task_queue_dict = SevenHelper.json_loads(task_queue_json)
                task_base_model = TaskBaseModel(logging_error=logger_error, logging_info=logger_info)
                invoke_result_data = task_base_model.add_gear_task_count_to_db(task_queue_dict["app_id"], task_queue_dict["act_id"], task_queue_dict["module_id"], task_queue_dict["user_id"], task_queue_dict["open_id"], task_queue_dict["task_type"], task_queue_dict["now_count"], task_queue_dict["remark"])
                if invoke_result_data.success == True:
                    redis_init.lpop(redis_key)

            except Exception as ex:
                logger_error.error(f"档位任务队列{mod_value}异常,ex:{traceback.format_exc()}")
                time.sleep(5)
