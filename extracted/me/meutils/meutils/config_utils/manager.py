#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : config_manager
# @Time         : 2024/12/4 12:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import nacos
from meutils.pipe import *


class ConfigManager(object):
    _instance = None
    _config: str = ""

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, namespace: str, data_id: str, group: str = "DEFAULT_GROUP", ):
        self.data_id = data_id
        self.group = group

        NACOS_URL = os.getenv("NACOS_URL")
        if NACOS_URL:
            server_addresses = NACOS_URL.split('@')[1]
            username, password = NACOS_URL.split('@')[0].split(":")

            # Nacos客户端配置
            self.client = nacos.NacosClient(
                server_addresses=server_addresses,  # Nacos服务器地址
                namespace=namespace,  # 命名空间
                username=username,  # 用户名
                password=password  # 密码
            )

    def init_config(self):
        """初始化配置并添加监听器"""
        # 获取初始配置
        config = self.client.get_config(self.data_id, self.group)
        logger.info(f"初始配置\n{config}")
        if config:
            self._config = config

        # 添加配置变更监听器
        self.client.add_config_watcher(self.data_id, self.group, self._config_changed_callback)

    def _config_changed_callback(self, args):
        """配置变更回调函数"""
        logger.debug(f"配置发生变更: {json.dumps(args, indent=4)}")
        # {'data_id': 'testdata', 'group': 'DEFAULT_GROUP', 'namespace': 'test', 'raw_content': 'sk-\nsk-',
        #  'content': 'sk-\nsk-'}
        self._config = args['content']

    @property
    def text(self) -> str:
        """获取当前配置: 原始内容"""
        return self._config or self.client.get_config(self.data_id, self.group)

    @property
    def json(self) -> Dict[str, Any]:
        text = self._config
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError as e:
            logger.warning(f"标准json 配置加载失败: {e}")

            logger.debug(f"尝试用json_repair解析")
            return json_repair.repair_json(text, return_objects=True)

    @property
    def yaml(self) -> Dict[str, Any]:
        text = self._config

        try:
            return yaml.safe_load(text)
        except Exception as e:
            logger.error(f"yaml 配置加载失败: {e}")

    @property
    def xml(self):
        return self._config

    @property
    def html(self):
        return self._config

    @property
    def properties(self):
        return self._config


if __name__ == '__main__':
    # 初始化配置管理器
    namespace = 'test'
    data_id = "testdata"

    namespace = 'prd'
    data_id = "siliconflow-api"

    manager = ConfigManager(namespace, data_id)
    # manager_ = Manager(namespace, data_id, group)

    print(manager.text)
