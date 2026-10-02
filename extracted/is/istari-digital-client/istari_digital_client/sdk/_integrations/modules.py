"""Modules manager (IstariIntegrations surface)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._integrations.integration_types import Module as ModuleType, ModuleVersion


class Modules(_Manager):
    """Manager for modules: get / list."""

    def get(self, module_id: str) -> ModuleType:
        """Fetch a module by UUID."""
        dto = self._call(self._engine.v2_api.get_module, module_id)
        return ModuleType._bind(dto, mgr=self)

    def list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        name: str | None = None,
        sort: str | None = None,
    ) -> Page[ModuleType]:
        """List modules."""

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_modules,
                page=page_num,
                size=size,
                name=name,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: ModuleType._bind(d, mgr=self), start_page=page or 1
        )

    def get_version(self, version_id: str) -> ModuleVersion:
        """Fetch a module version by its ID.

        Note: Module version IDs are globally unique, so no module_id is needed.
        """
        dto = self._call(self._engine.v2_api.get_module_version, version_id)
        return ModuleVersion._bind(dto, mgr=self)

    def list_versions(
        self, module_id: str, *, page: int | None = None, size: int | None = None
    ) -> Page[ModuleVersion]:
        """List versions of a module.

        Note: The underlying API lists all module versions globally, so this method
        fetches and filters client-side. For better performance with many modules,
        consider using get() which includes module_versions in the response.
        """

        def fetch(page_num: int) -> Any:
            # API doesn't support filtering by module_id, so we fetch all and filter
            raw_page = self._call(
                self._engine.v2_api.list_module_versions,
                page=page_num,
                size=size,
            )
            # Filter items to only this module's versions
            filtered_items = [
                v for v in (raw_page.items or []) if v.module_id == module_id
            ]
            # Rebuild page with filtered items
            raw_page.items = filtered_items
            return raw_page

        return self._paginate_offset(
            fetch, lambda d: ModuleVersion._bind(d, mgr=self), start_page=page or 1
        )
