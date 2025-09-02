# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2023-02-10 09:28:07
@LastEditTime: 2025-08-04 16:16:35
@LastEditors: HuangJianYi
@Description: console引用
"""
# 框架引用
from seven_framework.console.base_console import *
from seven_cloudapp_frame.libs.common import *

# 初始化配置,执行顺序需先于调用模块导入
share_config.init_config("share_config.json")  # 全局配置,只需要配置一次


work_process_date_dict = {}  # 作业心跳监控时间


def heart_beat_monitor(work_name, interval_time=30, data={}, check_time=60, redis_config_dict=None):
    """
    :description: 作业心跳监控
    :param work_name: 作业名称
    :param interval_time: 上报间隔时间，单位：秒
    :param data: 数据字典
    :param check_time: 预警间隔时间，单位：分钟
    :param redis_config_dict: redis配置
    :return: 
    :last_editors: HuangJianYi
    """
    from seven_cloudapp_frame.libs.customize.redis_helper import RedisExHelper
    heart_beat_name = share_config.get_value("heart_beat_name", '')
    monitor_key = f"heart_beat_monitor:{work_name}" if not heart_beat_name else f"heart_beat_monitor:{heart_beat_name}:{work_name}"
    is_heart_beat_monitor = share_config.get_value("is_heart_beat_monitor", True)
    if is_heart_beat_monitor is True:
        try:
            is_init = False
            now_date = TimeHelper.get_now_format_time()
            process_date = work_process_date_dict.get(work_name)
            if not process_date:
                work_process_date_dict[work_name] = now_date
                process_date = now_date
                is_init = True
            if abs(TimeHelper.difference_seconds(process_date, now_date)) > interval_time or is_init is True:
                RedisExHelper.init(config_dict=redis_config_dict).set(monitor_key, JsonHelper.json_dumps({"process_date": now_date, "check_time": check_time, "data": data}), 30 * 24 * 3600)
                work_process_date_dict[work_name] = now_date
        except Exception as ex:
            logger_error.error(f"{work_name}-作业心跳监控异常,ex:{traceback.format_exc()}")


def heart_beat_check(redis_config_dict=None, wx_send_key=""):
    """
    :description: 作业心跳检测
    :param redis_config_dict: redis配置
    :param wx_send_key: 企业微信群推送密钥
    :return: 
    :last_editors: HuangJianYi
    """
    from seven_cloudapp_frame.libs.customize.redis_helper import RedisExHelper
    try:
        heart_beat_name = share_config.get_value("heart_beat_name", '')
        monitor_key = "heart_beat_monitor:*" if not heart_beat_name else f"heart_beat_monitor:{heart_beat_name}:*"
        delete_keys = []
        redis_init = RedisExHelper.init(config_dict=redis_config_dict)
        match_result = redis_init.scan_iter(match=monitor_key)
        for item in match_result:
            delete_keys.append(item)
        if len(delete_keys) > 0:
            redis_init.delete(*delete_keys)

        while True:
            try:
                time.sleep(60)
                get_keys = []
                match_result = redis_init.scan_iter(match=monitor_key)
                for item in match_result:
                    get_keys.append(item)
                if len(get_keys) <= 0:
                    continue
                value_list = redis_init.mget(get_keys)
                for i in range(len(value_list)):
                    info_json = value_list[i]
                    if not info_json:
                        continue
                    info = json.loads(info_json)
                    check_time = int(info.get("check_time", 0))
                    process_date = info.get("process_date", "")
                    if process_date and check_time > 0:
                        now_date = TimeHelper.get_now_format_time()
                        if abs(TimeHelper.difference_minutes(process_date, now_date)) > check_time:
                            if not wx_send_key:
                                logger_error.error(f"{get_keys[i]}-作业没有检测到心跳,最后上报时间：{process_date}")
                            else:
                                webhook = WorkWechatWebhookHelper(wx_send_key)
                                webhook.send_webhook_message_markdown(f"{get_keys[i]}-作业没有检测到心跳,最后上报时间：{process_date}")
            except Exception as ex:
                logger_error.error(f"作业心跳检测异常,ex:{traceback.format_exc()}")
    except Exception as ex:
        logger_error.error(f"作业心跳检测异常,ex:{traceback.format_exc()}")
