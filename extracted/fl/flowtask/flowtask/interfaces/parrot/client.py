"""
ParrotClient Interface.

Direct interface for invoking ai-parrot LLM clients methods without wrapping an Agent.
"""
from typing import Any
from navconfig.logging import logging
from parrot.clients.factory import SUPPORTED_CLIENTS


class ParrotClient:
    """
    Interface for invoking parrot/clients LLMs methods directly.
    
    Example:
        ```python
        client = ParrotClient(client='google')
        result = await client.call_method(
            method='video_understanding', 
            prompt=prompt, 
            video=video_file, 
            as_image=True
        )
        ```
    """

    def __init__(self, client: str = 'google', **kwargs):
        self.client_name = client
        self.client_params = kwargs
        self._logger = logging.getLogger(f'ParrotClient.{self.client_name}')

    def create_client(self, client_name: str = None, **kwargs) -> Any:
        """
        Creates the instance of parrot.clients based on the client name.
        """
        name = client_name or self.client_name
        if name not in SUPPORTED_CLIENTS:
            available = ', '.join(SUPPORTED_CLIENTS.keys())
            raise ValueError(
                f"Unsupported client '{name}'. "
                f"Available clients: {available}"
            )
        
        client_class = SUPPORTED_CLIENTS[name]
        params = {**self.client_params, **kwargs}
        return client_class(**params)

    async def call_method(self, method: str = 'ask', **kwargs) -> Any:
        """
        Invokes a specific method on the created client instance.
        """
        client = self.create_client()
        
        if not hasattr(client, method):
            raise AttributeError(
                f"Method '{method}' not found on client '{self.client_name}'"
            )
            
        try:
            # Use async context manager if the client supports it
            if hasattr(client, "__aenter__"):
                async with client as active_client:
                    target_method = getattr(active_client, method)
                    response = await target_method(**kwargs)
                    return response
            else:
                target_method = getattr(client, method)
                response = await target_method(**kwargs)
                return response
        except Exception as err:
            self._logger.error(
                f"Error calling method '{method}' on client '{self.client_name}': {err}"
            )
            raise
