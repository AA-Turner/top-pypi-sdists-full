from contextvars import ContextVar
from typing import TYPE_CHECKING

# Avoid circular import error
if TYPE_CHECKING:
    from hfi.hfi_workspace_data import HfiWorkspaceData


workspace_id: ContextVar[str] = ContextVar("workspace_id")
hfi_workspace_data: ContextVar["HfiWorkspaceData"] = ContextVar("hfi_workspace_data")
table_id: ContextVar[str] = ContextVar("table_id")
hfi_frequency: ContextVar[float] = ContextVar("hfi_frequency")
hfi_frequency_gatherer: ContextVar[float] = ContextVar("hfi_frequency_gatherer")
gatherer_allow_s3_backup_on_user_errors: ContextVar[bool] = ContextVar("gatherer_allow_s3_backup_on_user_errors")
disable_template_security_validation: ContextVar[bool] = ContextVar("disable_template_security_validation")
origin: ContextVar[str] = ContextVar("origin")
request_id: ContextVar[str] = ContextVar("request_id")
engine: ContextVar[str] = ContextVar("engine")
wait_parameter: ContextVar[bool] = ContextVar("wait_parameter")
api_host: ContextVar[str] = ContextVar("api_host")
ff_split_to_array_escape: ContextVar[bool] = ContextVar("ff_split_to_array_escape")
ff_column_json_backticks_circuit_breaker: ContextVar[bool] = ContextVar("ff_column_json_backticks_circuit_breaker")
