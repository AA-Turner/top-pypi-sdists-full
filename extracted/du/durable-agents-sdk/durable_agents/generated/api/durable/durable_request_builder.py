from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .accounts.accounts_request_builder import AccountsRequestBuilder
    from .agents.agents_request_builder import AgentsRequestBuilder
    from .audit.audit_request_builder import AuditRequestBuilder
    from .billing.billing_request_builder import BillingRequestBuilder
    from .channels.channels_request_builder import ChannelsRequestBuilder
    from .connectors.connectors_request_builder import ConnectorsRequestBuilder
    from .content.content_request_builder import ContentRequestBuilder
    from .data_sources.data_sources_request_builder import DataSourcesRequestBuilder
    from .keys.keys_request_builder import KeysRequestBuilder
    from .models_requests.models_request_builder import ModelsRequestBuilder
    from .personas.personas_request_builder import PersonasRequestBuilder
    from .runs.runs_request_builder import RunsRequestBuilder
    from .skills.skills_request_builder import SkillsRequestBuilder
    from .vfs.vfs_request_builder import VfsRequestBuilder

class DurableRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new DurableRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable", path_parameters)
    
    @property
    def accounts(self) -> AccountsRequestBuilder:
        """
        The accounts property
        """
        from .accounts.accounts_request_builder import AccountsRequestBuilder

        return AccountsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def agents(self) -> AgentsRequestBuilder:
        """
        The agents property
        """
        from .agents.agents_request_builder import AgentsRequestBuilder

        return AgentsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def audit(self) -> AuditRequestBuilder:
        """
        The audit property
        """
        from .audit.audit_request_builder import AuditRequestBuilder

        return AuditRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def billing(self) -> BillingRequestBuilder:
        """
        The billing property
        """
        from .billing.billing_request_builder import BillingRequestBuilder

        return BillingRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def channels(self) -> ChannelsRequestBuilder:
        """
        The channels property
        """
        from .channels.channels_request_builder import ChannelsRequestBuilder

        return ChannelsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def connectors(self) -> ConnectorsRequestBuilder:
        """
        The connectors property
        """
        from .connectors.connectors_request_builder import ConnectorsRequestBuilder

        return ConnectorsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def content(self) -> ContentRequestBuilder:
        """
        The content property
        """
        from .content.content_request_builder import ContentRequestBuilder

        return ContentRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def data_sources(self) -> DataSourcesRequestBuilder:
        """
        The dataSources property
        """
        from .data_sources.data_sources_request_builder import DataSourcesRequestBuilder

        return DataSourcesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def keys(self) -> KeysRequestBuilder:
        """
        The keys property
        """
        from .keys.keys_request_builder import KeysRequestBuilder

        return KeysRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def models(self) -> ModelsRequestBuilder:
        """
        The models property
        """
        from .models_requests.models_request_builder import ModelsRequestBuilder

        return ModelsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def personas(self) -> PersonasRequestBuilder:
        """
        The personas property
        """
        from .personas.personas_request_builder import PersonasRequestBuilder

        return PersonasRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def runs(self) -> RunsRequestBuilder:
        """
        The runs property
        """
        from .runs.runs_request_builder import RunsRequestBuilder

        return RunsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def skills(self) -> SkillsRequestBuilder:
        """
        The skills property
        """
        from .skills.skills_request_builder import SkillsRequestBuilder

        return SkillsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def vfs(self) -> VfsRequestBuilder:
        """
        The vfs property
        """
        from .vfs.vfs_request_builder import VfsRequestBuilder

        return VfsRequestBuilder(self.request_adapter, self.path_parameters)
    

