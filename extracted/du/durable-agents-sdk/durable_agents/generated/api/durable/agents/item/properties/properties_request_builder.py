from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from ......models.agent import Agent
    from ......models.agent_property_patch import AgentPropertyPatch
    from ......models.error_envelope import ErrorEnvelope

class PropertiesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/agents/{agent}/properties
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new PropertiesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/agents/{agent}/properties", path_parameters)
    
    async def patch(self,body: AgentPropertyPatch, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Agent]:
        """
        Canonical property-oriented mutation endpoint for agent-friendly clients.Send a `properties` map whose keys are supported property paths such as`prompt`, `focus`, `mode`, `schedule.cron`, `schedule.timezone`,`trigger.kinds`, `trigger.sources`, or `heartbeat.frequency_minutes`.A `null` value clears the property when clearing is supported. Parent andchild paths cannot be patched in the same request; for example, do notsend both `schedule` and `schedule.cron`.The low-level `PATCH /api/durable/agents/{agent}` object patch endpointremains available, but this property endpoint is the canonical surfacefor LLM and CLI mutation workflows.
        param body: Property-oriented agent patch. Keys are typed property paths and valuesare the replacement value, or `null` for clearable properties.Supported property paths:- `name`: string, not clearable- `description`: string or null- `state`: `enabled` or `disabled`, not clearable- `mode`: `interactive`, `heartbeat`, `scheduled`, `triggered`, or `webhook`, not clearable- `model`: model preset/specification ID or null- `effort`: `quick`, `standard`, `deep`, `exhaustive`, or null- `persona`: ref ID/object or null- `prompt`: string or null; automation creates receive a default prompt when omitted, and automation updates cannot clear it- `focus`: string or null- `trigger`: full trigger object or null- `trigger.kinds`: string array or null- `trigger.sources`: source ref array or null- `schedule`: full schedule object or null- `schedule.cron`: string or null- `schedule.timezone`: string or null- `schedule.recurrence_type`: `monitor`, `once`, `repeat`, or null- `schedule.repeat_interval`: string or null- `heartbeat`: full heartbeat object, not clearable; use `mode: interactive` to disable heartbeat automation- `heartbeat.frequency_minutes`: number, not clearable- `heartbeat.off_hours_frequency_minutes`: number or null- `heartbeat.active_hours_start`: string, not clearable- `heartbeat.active_hours_end`: string, not clearable- `heartbeat.active_days`: number array, not clearable- `heartbeat.timezone`: string, not clearable- `heartbeat.probe_thresholds`: object or null- `heartbeat.probe_thresholds.new_content_min`: number or null- `heartbeat.probe_thresholds.volume_spike_multiplier`: number or nullParent/child path conflicts are rejected. For example, do not patchboth `schedule` and `schedule.cron` in one request.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Agent]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_patch_request_information(
            body, request_configuration
        )
        from ......models.error_envelope import ErrorEnvelope

        error_mapping: dict[str, type[ParsableFactory]] = {
            "XXX": ErrorEnvelope,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.agent import Agent

        return await self.request_adapter.send_async(request_info, Agent, error_mapping)
    
    def to_patch_request_information(self,body: AgentPropertyPatch, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Canonical property-oriented mutation endpoint for agent-friendly clients.Send a `properties` map whose keys are supported property paths such as`prompt`, `focus`, `mode`, `schedule.cron`, `schedule.timezone`,`trigger.kinds`, `trigger.sources`, or `heartbeat.frequency_minutes`.A `null` value clears the property when clearing is supported. Parent andchild paths cannot be patched in the same request; for example, do notsend both `schedule` and `schedule.cron`.The low-level `PATCH /api/durable/agents/{agent}` object patch endpointremains available, but this property endpoint is the canonical surfacefor LLM and CLI mutation workflows.
        param body: Property-oriented agent patch. Keys are typed property paths and valuesare the replacement value, or `null` for clearable properties.Supported property paths:- `name`: string, not clearable- `description`: string or null- `state`: `enabled` or `disabled`, not clearable- `mode`: `interactive`, `heartbeat`, `scheduled`, `triggered`, or `webhook`, not clearable- `model`: model preset/specification ID or null- `effort`: `quick`, `standard`, `deep`, `exhaustive`, or null- `persona`: ref ID/object or null- `prompt`: string or null; automation creates receive a default prompt when omitted, and automation updates cannot clear it- `focus`: string or null- `trigger`: full trigger object or null- `trigger.kinds`: string array or null- `trigger.sources`: source ref array or null- `schedule`: full schedule object or null- `schedule.cron`: string or null- `schedule.timezone`: string or null- `schedule.recurrence_type`: `monitor`, `once`, `repeat`, or null- `schedule.repeat_interval`: string or null- `heartbeat`: full heartbeat object, not clearable; use `mode: interactive` to disable heartbeat automation- `heartbeat.frequency_minutes`: number, not clearable- `heartbeat.off_hours_frequency_minutes`: number or null- `heartbeat.active_hours_start`: string, not clearable- `heartbeat.active_hours_end`: string, not clearable- `heartbeat.active_days`: number array, not clearable- `heartbeat.timezone`: string, not clearable- `heartbeat.probe_thresholds`: object or null- `heartbeat.probe_thresholds.new_content_min`: number or null- `heartbeat.probe_thresholds.volume_spike_multiplier`: number or nullParent/child path conflicts are rejected. For example, do not patchboth `schedule` and `schedule.cron` in one request.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.PATCH, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> PropertiesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: PropertiesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return PropertiesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class PropertiesRequestBuilderPatchRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

