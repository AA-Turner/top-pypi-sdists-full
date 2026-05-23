from collections.abc import Iterable
from typing import Any, Dict, Literal, Optional, Set, Union

from .base import AgentTools

Method = Literal["select", "insert", "update", "delete"]
_ALL_METHODS: Set[Method] = {"select", "insert", "update", "delete"}


def to_method(m: Union[Literal["all"], Method, Iterable[Method]]) -> Set[Method]:
    if m == "all":
        return set(_ALL_METHODS)
    if isinstance(m, str):
        if m in _ALL_METHODS:
            return {m}  # type: ignore[arg-type]
        raise ValueError(f"Invalid method: {m}")
    return set(m)


def to_table(t: Optional[Union[str, Iterable[str]]]) -> Optional[Set[str]]:
    if t is None or t == "all":
        return None
    if isinstance(t, str):
        return {t}
    return set(t)


class TablesTools(AgentTools):
    """
    Toolkit that gives an agent access to your Abstra Tables. The agent gets one tool per allowed method (`select`, `insert`, `update`, `delete`, optionally `run_sql`), scoped to the tables and default WHERE clause you configure.

    The `where` default is treated as a scoping invariant: it is merged into every `select`, `update`, and `delete` call AFTER the agent's call-site `where`, so the toolkit-level keys always win. Use this for tenant scoping (e.g. `{"tenant_id": "abc"}`) — the agent cannot override or remove those keys, even by accident.
    """

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
        """
        Build a TablesTools toolkit, optionally scoped to specific methods, tables, and a default WHERE clause.

        Args:
            method (Union): Allowed table operations. Either `"all"` (full CRUD), a single method (`"select"`, `"insert"`, `"update"`, `"delete"`), or a list of methods. Defaults to `"all"`.
            table (Optional): Restrict access to one or more table names. `None` (or `"all"`) allows every table in the project. Defaults to None.
            where (Optional): Default WHERE clause merged into every `select`/`update`/`delete`. The toolkit keys always win over the agent's call-site `where`, so this is safe for scoping (e.g. `{"tenant_id": "abc"}`). Defaults to None.
            allow_sql (bool): If True, exposes an extra `run_sql` tool that accepts arbitrary read-only SQL. Use with caution. Defaults to False.
        """
        self.methods = to_method(method)
        self.table = to_table(table)
        self.where = where or {}
        self.allow_sql = allow_sql

    def _assert_method(self, method: Method) -> None:
        if method not in self.methods:
            raise PermissionError(f"{method.capitalize()} method is not allowed.")

    def _assert_table(self, table: str) -> None:
        if self.table is not None and table not in self.table:
            raise ValueError(f"Table '{table}' is not allowed.")

    def _scoped_where(self, where: Dict[str, Any]) -> Dict[str, Any]:
        # Toolkit defaults win over call-site so scoping (e.g. tenant_id) is
        # enforceable — the agent cannot override or strip those keys.
        return {**where, **self.where}

    def select(
        self, table: str, where: Dict[str, Any] = {}
    ) -> Iterable[Dict[str, Any]]:
        from abstra.tables import select

        self._assert_method("select")
        self._assert_table(table)
        return select(table, where=self._scoped_where(where))

    def insert(self, table: str, data: Dict[str, Any]) -> Any:
        from abstra.tables import insert

        self._assert_method("insert")
        self._assert_table(table)
        # Apply default-where as data tags on insert so tenant scoping is
        # symmetric with select/update/delete. Without this, an agent could
        # insert rows that the same toolkit's select() would then hide.
        data = {**data, **self.where}
        return insert(table, data)

    def update(
        self, table: str, set: Dict[str, Any], where: Dict[str, Any] = {}
    ) -> Any:
        from abstra.tables import update

        self._assert_method("update")
        self._assert_table(table)
        return update(table, set=set, where=self._scoped_where(where))

    def delete(self, table: str, where: Dict[str, Any] = {}) -> Any:
        from abstra.tables import delete

        self._assert_method("delete")
        self._assert_table(table)
        return delete(table, where=self._scoped_where(where))

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
