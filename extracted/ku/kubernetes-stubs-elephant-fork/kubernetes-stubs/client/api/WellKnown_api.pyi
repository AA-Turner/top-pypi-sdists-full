import typing

import kubernetes.client

class WellKnownApi:
    def __init__(self, api_client: typing.Optional[kubernetes.client.ApiClient] = ...) -> None:
        ...
    def get_service_account_issuer_open_id_configuration(self, *, 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> str:
        ...
