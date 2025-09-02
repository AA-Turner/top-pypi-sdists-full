# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2023-02-09 18:29:31
@LastEditTime: 2025-06-25 16:01:40
@LastEditors: HuangJianYi
:Description: tornado引用
"""
# 框架引用
from seven_framework.web_tornado.base_tornado import *
from seven_cloudapp_frame.libs.common import *

# 初始化配置,执行顺序需先于调用模块导入
share_config.init_config("share_config.json")  # 全局配置,只需要配置一次


# nacos配置获取
nacos_share_config = config.get_value("nacos_share", None)
if nacos_share_config:
    nacos_share_host = nacos_share_config["host"]
    nacos_share_namespace = nacos_share_config["namespace"]
    nacos_share_data_id = nacos_share_config['data_id']
    nacos_share_group = nacos_share_config.get("group", "DEFAULT_GROUP")
    nacos_share_username = nacos_share_config.get("username", None)
    nacos_share_password = nacos_share_config.get("password", None)
    config_file = "share_config.json"
    if not nacos_share_host or not nacos_share_namespace or not nacos_share_data_id or not nacos_share_group:
        raise Exception("nacos配置错误")
    try:
        nacos_share_client = NacosClient(server_addresses=nacos_share_host, namespace=nacos_share_namespace, username=nacos_share_username, password=nacos_share_password)
        nacos_share_client.add_naming_instance(nacos_share_data_id, HostHelper.get_host_ip(), int(config.get_value("run_port")), heartbeat_interval=5, group_name=nacos_share_group)
        # 从Nacos获取配置，并更新到Flask应用的config对象中，以便在应用中使用这些配置
        config_content = nacos_share_client.get_config(data_id=nacos_share_data_id, group=nacos_share_group)
        share_config.init_config_from_nacos(config_file, config_content)
    except Exception as ex:
        logger_error.error(f"nacos连接失败:{ex},将使用本地配置。")
        share_config.init_config(config_file)
    # 添加配置监听器，当Nacos中的配置发生变化时，自动更新Flask应用的config对象
    try:
        nacos_share_client.add_config_watcher(data_id=nacos_share_data_id, group=nacos_share_group, cb=lambda cfg: share_config.init_config_from_nacos(config_file, cfg["content"]))
    except:
        pass
