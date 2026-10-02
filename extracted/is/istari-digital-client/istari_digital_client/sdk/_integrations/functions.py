"""Functions manager (IstariIntegrations surface)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._integrations.integration_types import Function as FunctionType
from istari_digital_client.sdk._generated.v2.models.user_model_inputs import UserModelInputs
from istari_digital_client.sdk._generated.v2.models.usability_status_params import UsabilityStatusParams


class Functions(_Manager):
    """Manager for functions: get / list.

    Functions are executable operations registered by modules (read-only for clients).
    """

    def get(self, function_id: str) -> FunctionType:
        """Fetch a function by UUID."""
        dto = self._call(self._engine.v2_api.get_function, function_id)
        return FunctionType._bind(dto, mgr=self)

    def list(
        self,
        *,
        name: str | None = None,
        module_version: str | None = None,
        tool: str | None = None,
        tool_version: str | None = None,
        operating_system: str | None = None,
        input_extension: str | None = None,
        input_user_models: UserModelInputs | None = None,
        status: UsabilityStatusParams | None = None,
        page: int | None = None,
        size: int | None = None,
        sort: str | None = None,
    ) -> Page[FunctionType]:
        """List functions."""

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_functions,
                name=name,
                module_version=module_version,
                tool=tool,
                tool_version=tool_version,
                operating_system=operating_system,
                input_extension=input_extension,
                input_user_models=input_user_models,
                status=status,
                page=page_num,
                size=size,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: FunctionType._bind(d, mgr=self), start_page=page or 1
        )
