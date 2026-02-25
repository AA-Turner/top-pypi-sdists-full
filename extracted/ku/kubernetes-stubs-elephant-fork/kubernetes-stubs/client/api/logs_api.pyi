import typing

import kubernetes.client

class LogsApi:
    def __init__(self, api_client: typing.Optional[kubernetes.client.ApiClient] = ...) -> None:
        ...
    def log_file_list_handler(self, *, 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> None:
        ...
    def log_file_handler(self, logpath: str, *, 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> None:
        ...
