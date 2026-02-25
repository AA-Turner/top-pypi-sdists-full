import typing

import kubernetes.client

class AuthenticationV1Api:
    def __init__(self, api_client: typing.Optional[kubernetes.client.ApiClient] = ...) -> None:
        ...
    def get_api_resources(self, *, 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1APIResourceList:
        ...
    def create_self_subject_review(self, body: kubernetes.client.V1SelfSubjectReview, *, dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1SelfSubjectReview:
        ...
    def create_token_review(self, body: kubernetes.client.V1TokenReview, *, dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1TokenReview:
        ...
