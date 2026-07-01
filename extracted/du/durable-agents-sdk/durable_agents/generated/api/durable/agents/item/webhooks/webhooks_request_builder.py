from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_webhook_token_item_request_builder import WithWebhook_tokenItemRequestBuilder

class WebhooksRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/durable/agents/{agent}/webhooks
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WebhooksRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/durable/agents/{agent}/webhooks", path_parameters)
    
    def by_webhook_token(self,webhook_token: str) -> WithWebhook_tokenItemRequestBuilder:
        """
        Gets an item from the durable_agents.generated.api.durable.agents.item.webhooks.item collection
        param webhook_token: Unique identifier of the item
        Returns: WithWebhook_tokenItemRequestBuilder
        """
        if webhook_token is None:
            raise TypeError("webhook_token cannot be null.")
        from .item.with_webhook_token_item_request_builder import WithWebhook_tokenItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["webhook_token"] = webhook_token
        return WithWebhook_tokenItemRequestBuilder(self.request_adapter, url_tpl_params)
    

