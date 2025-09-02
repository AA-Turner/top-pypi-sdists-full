# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-07-15 14:09:43
@LastEditTime: 2024-11-06 10:48:04
@LastEditors: HuangJianYi
:description: 通用Handler
"""
import tornado.websocket
from seven_framework.config import *
from seven_framework.redis import *
from seven_framework.web_tornado.base_handler.base_api_handler import *

from seven_cloudapp_frame.handlers.frame_base import *


class IndexHandler(FrameBaseHandler):
    """
    :description: 默认页
    """
    def get_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: HuangJianYi
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")

    def post_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: HuangJianYi
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")
    
    def head_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: HuangJianYi
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")



web_socket_clients = set()

class WebSocketBaseHandler(tornado.websocket.WebSocketHandler):
    """
    :description: WebSocket基类，http的话，使用ws的方式连接，https的话，使用wss的方式连接
    :last_editors: HuangJianYi
    """
    def check_origin(self, origin):
        return True

    def open(self):
        """
        :description: 建立连接
        :return: 
        :last_editors: HuangJianYi
        """
        print("已连接")
        web_socket_clients.add(self)
        # 启动定时任务
        self.periodic_callback = tornado.ioloop.PeriodicCallback(self.send_periodic_message, 100)
        self.periodic_callback.start()

    def send_periodic_message(self):
        """
        :description: 定时任务推送消息
        :return: 
        :last_editors: HuangJianYi
        """
        self.write_message("定时任务推送消息")

    def on_message(self, message):
        """
        :description: 接收当前客户端消息
        :param message: 消息
        :return: InvokeResultData   
        :last_editors: HuangJianYi
        """
        print(f"接收消息: {message}")
        self.write_message("测试：" + message)

    def on_close(self):
        """
        :description: 断开连接
        :return: 
        :last_editors: HuangJianYi
        """
        print("已关闭")
        # 关闭定期回调
        if hasattr(self, 'periodic_callback'):
            self.periodic_callback.stop()
        web_socket_clients.remove(self)