from collections.abc import Iterable
from typing import Any, Dict, Literal, Optional, Set, Union

from .base import AgentTools

Method = Literal["select", "insert", "update", "delete"]


def to_method(m: Union[Literal["all"], Method, Iterable[Method]]) -> Set[Method]:
    if isinstance(m, list):
        return set(m)
    elif m == "all":
        return set(*["select", "insert", "update", "delete"])
    elif m in ["select", "insert", "update", "delete"]:
        return set(*[m])
    raise ValueError(f"Invalid method: {m}")


def to_table(t: Optional[Union[str, Iterable[str]]]) -> Set[str]:
    if isinstance(t, list):
        return set(t)
    elif t == "all":
        return set(["all"])
    elif isinstance(t, str):
        return set([t])
    raise ValueError(f"Invalid table: {t}")


class TablesTools(AgentTools):
    methods: Set[Method]
    table: Optional[Set[str]]
    where: Dict[str, Any]
    allow_sql: bool

    def __init__(
        self,
        method: Union[Literal["all"], Method, Iterable[Method]] = "all",
        table: Optional[Union[str, Iterable[str]]] = None,
        where: Optional[Dict[str, Any]] = None,
        allow_sql: bool = False,
    ):
        self.methods = to_method(method)
        self.table = to_table(table)
        self.where = where or {}
        self.allow_sql = allow_sql

    def select(
        self, table: str, where: Dict[str, Any] = {}
    ) -> Iterable[Dict[str, Any]]:
        from abstra.tables import select

        if "select" not in self.methods and "all" not in self.methods:
            raise PermissionError("Select method is not allowed.")
        if self.table is not None and table not in self.table:
            raise ValueError(f"Table '{table}' is not allowed.")
        where = {**where, **self.where}
        return select(table, where=where)

    def insert(self, table: str, data: Dict[str, Any]) -> Any:
        from abstra.tables import insert

        if "insert" not in self.methods and "all" not in self.methods:
            raise PermissionError("Insert method is not allowed.")
        if self.table is not None and table not in self.table:
            raise ValueError(f"Table '{table}' is not allowed.")
        return insert(table, data)

    def update(
        self, table: str, set: Dict[str, Any], where: Dict[str, Any] = {}
    ) -> Any:
        from abstra.tables import update

        if "update" not in self.methods and "all" not in self.methods:
            raise PermissionError("Update method is not allowed.")
        if self.table is not None and table not in self.table:
            raise ValueError(f"Table '{table}' is not allowed.")
        where = where or self.where
        return update(table, set=set, where=where)

    def delete(self, table: str, where: Dict[str, Any] = {}) -> Any:
        from abstra.tables import delete

        if "delete" not in self.methods and "all" not in self.methods:
            raise PermissionError("Delete method is not allowed.")
        if self.table is not None and table not in self.table:
            raise ValueError(f"Table '{table}' is not allowed.")

        return delete(table, values=where)

    def run_sql(self, query: str) -> Any:
        from abstra.tables import run_sql

        if not self.allow_sql:
            raise PermissionError("Running raw SQL is not allowed.")
        return run_sql(query)

    def __tools__(self):
        tools = [
            self.select.__name__,
            self.insert.__name__,
            self.update.__name__,
            self.delete.__name__,
        ]
        if self.allow_sql:
            tools.append(self.run_sql.__name__)
        return tools
