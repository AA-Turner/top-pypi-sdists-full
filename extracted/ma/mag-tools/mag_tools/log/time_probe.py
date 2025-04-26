import time
from datetime import datetime
from typing import  Optional

from mag_tools.log.logger import Logger
from mag_tools.enums.log_type import LogType
from mag_tools.utils.common.check_node import CheckNode


class TimeProbe:
    def __init__(self, name: str):
        """
        初始化 TimeProbe 类的实例
        :param name: 探测器标题
        """
        self.__name = name
        self.__start_time = time.time_ns()  # 纳秒
        self.__previous_time = self.__start_time # 纳秒
        self.__check_nodes = [CheckNode(0, "初始节点", datetime.now(), 0, 0)]

    @classmethod
    def get_probe(cls, name: str = "性能监测"):
        """
        启动时间探测
        :param name: 探测器标题
        :return: TimeProbe 实例
        """
        return cls(name)

    def check(self, node_name: Optional[str] = None):
        """
        检测上次到当前检测点的时间差
        :param node_name: 节点名称
        :return: 当前节点信息
        """
        now_time = time.time_ns() # 当前时间，纳秒
        current_cost = now_time - self.__previous_time  # 纳秒
        total_cost = now_time - self.__start_time   # 纳秒

        node = CheckNode(len(self.__check_nodes), node_name, datetime.now(), current_cost, total_cost)
        self.__check_nodes.append(node)
        self.__previous_time = now_time
        return node

    @property
    def start_time(self):
        return datetime.fromtimestamp(self.__start_time // 1e9)

    @property
    def total_time(self) -> int:
        """
        检测开始到这次检测点的时间差
        :return: 时间差，单位：纳秒
        """
        return time.time_ns() - self.__start_time

    def print(self, *args):
        """
        打印节点信息
        :param args: 格式化参数
        :return: 当前节点信息
        """
        title = self.__name.format(*args)
        node = self.check(title)
        Logger.info(LogType.PERFORMANCE, f"[{title}]:\n  {node.log()}")
        return node

    def write_log(self):
        """
        写入日志信息
        """
        message = ''
        for node in self.__check_nodes:
            message += f"[node]:\n{node.log()}\n"

        Logger.info(LogType.PERFORMANCE, f"{self.__name}\n{message}")

    def get_check_nodes(self) -> list[CheckNode]:
        """
        获取所有检测节点
        :return: 检测节点列表
        """
        return self.__check_nodes
