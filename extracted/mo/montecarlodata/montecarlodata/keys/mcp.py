from typing import Any, Callable, Optional, cast

import click
from pycarlo.core import Client, Mutation, Query, Session

from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort, manage_errors


class McpKeyService:
    _table_headers = ["Id", "Description", "Created"]

    def __init__(
        self,
        config: Config,
        command_name: str,
        pycarlo_client: Optional[Client] = None,
        print_func: Optional[Callable] = None,
    ):
        self._command_name = command_name
        self._client = pycarlo_client or Client(
            Session(
                endpoint=config.mcd_api_endpoint, mcd_id=config.mcd_id, mcd_token=config.mcd_token
            )
        )
        self._print_func = print_func or click.echo
        self._abort_on_error = True

    @manage_errors
    def create(self, description: str):
        m = Mutation()
        create_sel = m.create_mcp_integration_key(description=description)
        key_sel = cast(Any, getattr(create_sel, "key", None))
        key_sel.__fields__("id", "secret")
        response = self._client(m)
        create_result = getattr(response, "create_mcp_integration_key", None)
        key = getattr(create_result, "key", None) if create_result else None
        if not key:
            complain_and_abort("Create MCP key failed: empty response from server")
        key_obj = cast(Any, key)
        self._print_func(f"Key id: {key_obj.id}")
        self._print_func(f"Key secret: {key_obj.secret}")

    @manage_errors
    def delete(self, key_id: str):
        m = Mutation()
        m.delete_mcp_integration_key(key_id=key_id).deleted
        response = self._client(m)
        delete_result = getattr(response, "delete_mcp_integration_key", None)
        deleted = bool(getattr(delete_result, "deleted", False))
        if deleted:
            self._print_func("Key has been deleted.")
        else:
            complain_and_abort(f"Failed to delete MCP key: {key_id}")

    @manage_errors
    def get_all(self):
        q = Query()
        list_sel = q.get_my_mcp_integration_keys
        cast(Any, list_sel).__fields__("id", "description", "created_time")
        response = self._client(q)
        keys = getattr(response, "get_my_mcp_integration_keys", []) or []
        if not keys:
            self._print_func("No MCP keys found.")
            return

        from tabulate import tabulate

        data = [[k.id, k.description, k.created_time] for k in keys]
        table = tabulate(data, headers=self._table_headers, tablefmt="fancy_grid")
        self._print_func(table)
