from dataclasses import dataclass, field

@dataclass
class DbPage:
    """
    分页类

    @description: 提供基础的分页操作
    @version: 2.5
    @date: 2015
    """
    index: int = field(default=1, metadata={"description": "页面索引，从1开始"})
    size: int = field(default=10, metadata={"description": "单页最大纪录数，缺省为10"})
    order_column: str = field(default=None, metadata={"description": "用于排序的列名"})
    ascend: bool = field(default=True, metadata={"description": "是否升序"})
    __total_page: int = field(default=-1, metadata={"description": "总页数"})
    total_num: int = field(default=-1, metadata={"description": "总纪录数"})
    total_sql: str = field(default=None, metadata={"description": "计算总纪录数的SQL语句,缺省为空"})
    current_page: int = field(default=1, metadata={"description": "当前请求的页数"})
    uuid: str = field(default=None, metadata={"description": "分页查询id，上一次查询返回的uuid,缺省为空"})

    @property
    def first_row(self) -> int:
        """
        获取首记录行号

        :return: 首记录行号
        """
        return (self.index - 1) * self.size

    @property
    def total_page(self) -> int:
        """
        取得总页数，-1表示错误

        :return: 总页数
        """
        if self.size < 1 or self.total_num < 0:
            return -1

        quotient = self.total_num // self.size
        remainder = self.total_num % self.size
        if remainder == 0:
            self.__total_page = quotient
        else:
            self.__total_page = quotient + 1

        return self.__total_page

    @property
    def offset(self):
        return (self.index - 1) * self.size

    def get_sql(self):
        return f"LIMIT {self.size} OFFSET {self.offset}"

    def __str__(self) -> str:
        return f"DbPage{{totalNum={self.total_num},totalSql={self.total_sql},size={self.size},totalPage={self.total_page},currentPage={self.current_page}}}"
