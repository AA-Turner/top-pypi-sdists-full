import datetime
from typing import Optional


class CheckNode:
    def __init__(self, sn: int, name: Optional[str], time: datetime, last_cost: int, total_cost: int):
        """
        初始化 CheckNode 类的实例
        :param sn: 节点序号
        :param name: 节点名称
        :param time: 节点时间
        :param last_cost: 上次到当前节点的时间差，单位：毫秒
        :param total_cost: 从开始到当前节点的总时间差，单位：毫秒
        """
        self.__sn = sn
        self.name = name if name else f"节点{sn}"
        self.__time = time
        self.__last_cost = last_cost
        self.__total_cost = total_cost

    def __str__(self):
        """
        返回节点的字符串表示
        :return: 节点的字符串表示
        """
        return f"sn={self.__sn};\nname={self.name};\ntime={self.__time};\nlast_cost={self.__last_cost};\ntotal_cost={self.__total_cost};\n"

    def log(self):
        """
        返回节点的日志信息
        :return: 节点的日志信息
        """
        total = f"{self.__total_cost / 1000}毫秒" if self.__total_cost > 1000 else f"{self.__total_cost}纳秒"
        last = f"{self.__last_cost / 1000}毫秒" if self.__last_cost > 1000 else f"{self.__last_cost}纳秒"

        return f"  节点号：{self.__sn};\n  节点名：{self.name};\n  执行时间：{self.__time};\n  本节点花费时间：{last};\n  总花费时间：{total};\n"
