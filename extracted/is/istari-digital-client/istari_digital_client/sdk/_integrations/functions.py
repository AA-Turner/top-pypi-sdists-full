"""Functions manager (IstariIntegrations surface)."""

from __future__ import annotations

import re
from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._exceptions import NotFoundError
from istari_digital_client.sdk._integrations.integration_types import Function as FunctionType
from istari_digital_client.sdk._generated.v2.models.function_schema import FunctionSchema
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

    def get_schema(self, function_id: str, *, version: str | None = None) -> FunctionSchema:
        """Fetch the input/output schema of one of a function's versions.

        Aliases: inputs outputs auth_info schema

        ``version`` picks the ``function_versions`` entry with that ``version``
        string; ``None`` picks the newest, which is the version ``jobs.create``
        runs when ``function_version`` is omitted. The returned schema's
        ``inputs`` have ``key``, ``type`` (``parameter`` / ``user_model`` /
        ``auth_info`` / ``user_link``), ``validation_types`` and ``optional``.
        An input of type ``auth_info`` must be bound to a stored credential when
        the job is created: ``istari.jobs.create(..., auth_bindings={key: credential_id})``.

        Raises NotFoundError if the function, the requested version, or that
        version's schema does not exist.
        """
        function = self.get(function_id)
        versions = function.function_versions or []
        if version is None:
            chosen = max(versions, key=lambda v: _version_key(v.version), default=None)
        else:
            chosen = next((v for v in versions if v.version == version), None)
        if chosen is None:
            wanted = f"version {version!r}" if version is not None else "versions"
            raise NotFoundError(f"function {function_id} has no {wanted}")
        if chosen.function_schema is None:
            raise NotFoundError(f"function {function_id} version {chosen.version} has no schema")
        return self._call(self._engine.v2_api.get_function_schema, chosen.function_schema)

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


def _version_key(version: str) -> list[tuple[int, int | str]]:
    """Order version strings numerically per dotted part, so "1.10.0" sorts above "1.9.0"."""
    return [(0, int(part)) if part.isdigit() else (1, part) for part in re.split(r"[.+-]", version)]
