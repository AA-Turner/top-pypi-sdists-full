from typing import Any, Dict, List, Optional, Union

from anyscale._private.models.model_base import ResultIterator
from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models.apply_scheduler_config_request import (
    ApplySchedulerConfigRequest,
)
from anyscale.client.openapi_client.models.scheduler_config import (
    SchedulerConfig as APISchedulerConfig,
)
from anyscale.client.openapi_client.models.scheduler_config_response import (
    SchedulerConfigResponse,
)
from anyscale.client.openapi_client.models.scheduler_config_version_summary import (
    SchedulerConfigVersionSummary as APISchedulerConfigVersionSummary,
)
from anyscale.scheduler.models import (
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
)


# Backend per-page cap; the API rejects count > 50.
_PAGE_SIZE_CAP = 50


class PrivateSchedulerSDK(BaseSDK):
    def apply_config(self, config: Union[SchedulerConfig, Dict[str, Any]],) -> int:
        request = ApplySchedulerConfigRequest(config=_to_api_config(config),)
        response = self.client.apply_scheduler_config(request)
        return response.version

    def get_config(self, version: Optional[int] = None,) -> SchedulerConfigVersion:
        if version is None:
            response = self.client.get_active_scheduler_config()
        else:
            response = self.client.get_scheduler_config_version(version)
        return _from_api_response(response)

    def list_config_versions(
        self, max_items: int = 10,
    ) -> List[SchedulerConfigVersionSummary]:
        page_size = min(max_items, _PAGE_SIZE_CAP) if max_items > 0 else 0

        def _fetch_page(token: Optional[str]):
            return self.client.list_scheduler_config_versions(
                count=page_size, paging_token=token,
            )

        return list(
            ResultIterator(
                page_token=None,
                max_items=max_items,
                fetch_page=_fetch_page,
                parse_fn=_from_api_summary,
            )
        )


def _to_api_config(
    config: Union[SchedulerConfig, Dict[str, Any]],
) -> APISchedulerConfig:
    if isinstance(config, SchedulerConfig):
        return APISchedulerConfig(**config.to_dict(exclude_none=True))
    if isinstance(config, dict):
        # Validate locally before sending; raises on schema errors with field path.
        return APISchedulerConfig(
            **SchedulerConfig.from_dict(config).to_dict(exclude_none=True)
        )
    raise TypeError(
        f"config must be SchedulerConfig or dict, got {type(config).__name__}."
    )


def _from_api_response(response: SchedulerConfigResponse) -> SchedulerConfigVersion:
    config_dict = (
        response.config.to_dict()
        if hasattr(response.config, "to_dict")
        else response.config
    )
    return SchedulerConfigVersion(
        version=response.version,
        is_active=response.is_active,
        created_at=response.created_at,
        creator_id=response.creator_id,
        config=SchedulerConfig.from_api_dict(config_dict),
    )


def _from_api_summary(
    summary: APISchedulerConfigVersionSummary,
) -> SchedulerConfigVersionSummary:
    return SchedulerConfigVersionSummary(
        version=summary.version,
        created_at=summary.created_at,
        creator_id=summary.creator_id,
    )
