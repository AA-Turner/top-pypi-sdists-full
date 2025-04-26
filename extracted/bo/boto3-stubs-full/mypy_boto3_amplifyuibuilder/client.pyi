"""
Type annotations for amplifyuibuilder service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_amplifyuibuilder.client import AmplifyUIBuilderClient

    session = Session()
    client: AmplifyUIBuilderClient = session.client("amplifyuibuilder")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ExportComponentsPaginator,
    ExportFormsPaginator,
    ExportThemesPaginator,
    ListCodegenJobsPaginator,
    ListComponentsPaginator,
    ListFormsPaginator,
    ListThemesPaginator,
)
from .type_defs import (
    CreateComponentRequestTypeDef,
    CreateComponentResponseTypeDef,
    CreateFormRequestTypeDef,
    CreateFormResponseTypeDef,
    CreateThemeRequestTypeDef,
    CreateThemeResponseTypeDef,
    DeleteComponentRequestTypeDef,
    DeleteFormRequestTypeDef,
    DeleteThemeRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExchangeCodeForTokenRequestTypeDef,
    ExchangeCodeForTokenResponseTypeDef,
    ExportComponentsRequestTypeDef,
    ExportComponentsResponseTypeDef,
    ExportFormsRequestTypeDef,
    ExportFormsResponseTypeDef,
    ExportThemesRequestTypeDef,
    ExportThemesResponseTypeDef,
    GetCodegenJobRequestTypeDef,
    GetCodegenJobResponseTypeDef,
    GetComponentRequestTypeDef,
    GetComponentResponseTypeDef,
    GetFormRequestTypeDef,
    GetFormResponseTypeDef,
    GetMetadataRequestTypeDef,
    GetMetadataResponseTypeDef,
    GetThemeRequestTypeDef,
    GetThemeResponseTypeDef,
    ListCodegenJobsRequestTypeDef,
    ListCodegenJobsResponseTypeDef,
    ListComponentsRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListFormsRequestTypeDef,
    ListFormsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThemesRequestTypeDef,
    ListThemesResponseTypeDef,
    PutMetadataFlagRequestTypeDef,
    RefreshTokenRequestTypeDef,
    RefreshTokenResponseTypeDef,
    StartCodegenJobRequestTypeDef,
    StartCodegenJobResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateComponentRequestTypeDef,
    UpdateComponentResponseTypeDef,
    UpdateFormRequestTypeDef,
    UpdateFormResponseTypeDef,
    UpdateThemeRequestTypeDef,
    UpdateThemeResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AmplifyUIBuilderClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class AmplifyUIBuilderClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyUIBuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#generate_presigned_url)
        """

    def create_component(
        self, **kwargs: Unpack[CreateComponentRequestTypeDef]
    ) -> CreateComponentResponseTypeDef:
        """
        Creates a new component for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/create_component.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#create_component)
        """

    def create_form(self, **kwargs: Unpack[CreateFormRequestTypeDef]) -> CreateFormResponseTypeDef:
        """
        Creates a new form for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/create_form.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#create_form)
        """

    def create_theme(
        self, **kwargs: Unpack[CreateThemeRequestTypeDef]
    ) -> CreateThemeResponseTypeDef:
        """
        Creates a theme to apply to the components in an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/create_theme.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#create_theme)
        """

    def delete_component(
        self, **kwargs: Unpack[DeleteComponentRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a component from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/delete_component.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#delete_component)
        """

    def delete_form(
        self, **kwargs: Unpack[DeleteFormRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a form from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/delete_form.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#delete_form)
        """

    def delete_theme(
        self, **kwargs: Unpack[DeleteThemeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a theme from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/delete_theme.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#delete_theme)
        """

    def exchange_code_for_token(
        self, **kwargs: Unpack[ExchangeCodeForTokenRequestTypeDef]
    ) -> ExchangeCodeForTokenResponseTypeDef:
        """
        This is for internal use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/exchange_code_for_token.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#exchange_code_for_token)
        """

    def export_components(
        self, **kwargs: Unpack[ExportComponentsRequestTypeDef]
    ) -> ExportComponentsResponseTypeDef:
        """
        Exports component configurations to code that is ready to integrate into an
        Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/export_components.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#export_components)
        """

    def export_forms(
        self, **kwargs: Unpack[ExportFormsRequestTypeDef]
    ) -> ExportFormsResponseTypeDef:
        """
        Exports form configurations to code that is ready to integrate into an Amplify
        app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/export_forms.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#export_forms)
        """

    def export_themes(
        self, **kwargs: Unpack[ExportThemesRequestTypeDef]
    ) -> ExportThemesResponseTypeDef:
        """
        Exports theme configurations to code that is ready to integrate into an Amplify
        app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/export_themes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#export_themes)
        """

    def get_codegen_job(
        self, **kwargs: Unpack[GetCodegenJobRequestTypeDef]
    ) -> GetCodegenJobResponseTypeDef:
        """
        Returns an existing code generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_codegen_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_codegen_job)
        """

    def get_component(
        self, **kwargs: Unpack[GetComponentRequestTypeDef]
    ) -> GetComponentResponseTypeDef:
        """
        Returns an existing component for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_component.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_component)
        """

    def get_form(self, **kwargs: Unpack[GetFormRequestTypeDef]) -> GetFormResponseTypeDef:
        """
        Returns an existing form for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_form.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_form)
        """

    def get_metadata(
        self, **kwargs: Unpack[GetMetadataRequestTypeDef]
    ) -> GetMetadataResponseTypeDef:
        """
        Returns existing metadata for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_metadata.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_metadata)
        """

    def get_theme(self, **kwargs: Unpack[GetThemeRequestTypeDef]) -> GetThemeResponseTypeDef:
        """
        Returns an existing theme for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_theme.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_theme)
        """

    def list_codegen_jobs(
        self, **kwargs: Unpack[ListCodegenJobsRequestTypeDef]
    ) -> ListCodegenJobsResponseTypeDef:
        """
        Retrieves a list of code generation jobs for a specified Amplify app and
        backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_codegen_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_codegen_jobs)
        """

    def list_components(
        self, **kwargs: Unpack[ListComponentsRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        Retrieves a list of components for a specified Amplify app and backend
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_components.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_components)
        """

    def list_forms(self, **kwargs: Unpack[ListFormsRequestTypeDef]) -> ListFormsResponseTypeDef:
        """
        Retrieves a list of forms for a specified Amplify app and backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_forms.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_forms)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_tags_for_resource)
        """

    def list_themes(self, **kwargs: Unpack[ListThemesRequestTypeDef]) -> ListThemesResponseTypeDef:
        """
        Retrieves a list of themes for a specified Amplify app and backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_themes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#list_themes)
        """

    def put_metadata_flag(
        self, **kwargs: Unpack[PutMetadataFlagRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stores the metadata information about a feature on a form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/put_metadata_flag.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#put_metadata_flag)
        """

    def refresh_token(
        self, **kwargs: Unpack[RefreshTokenRequestTypeDef]
    ) -> RefreshTokenResponseTypeDef:
        """
        This is for internal use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/refresh_token.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#refresh_token)
        """

    def start_codegen_job(
        self, **kwargs: Unpack[StartCodegenJobRequestTypeDef]
    ) -> StartCodegenJobResponseTypeDef:
        """
        Starts a code generation job for a specified Amplify app and backend
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/start_codegen_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#start_codegen_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags the resource with a tag key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Untags a resource with a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#untag_resource)
        """

    def update_component(
        self, **kwargs: Unpack[UpdateComponentRequestTypeDef]
    ) -> UpdateComponentResponseTypeDef:
        """
        Updates an existing component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/update_component.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#update_component)
        """

    def update_form(self, **kwargs: Unpack[UpdateFormRequestTypeDef]) -> UpdateFormResponseTypeDef:
        """
        Updates an existing form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/update_form.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#update_form)
        """

    def update_theme(
        self, **kwargs: Unpack[UpdateThemeRequestTypeDef]
    ) -> UpdateThemeResponseTypeDef:
        """
        Updates an existing theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/update_theme.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#update_theme)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["export_components"]
    ) -> ExportComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["export_forms"]
    ) -> ExportFormsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["export_themes"]
    ) -> ExportThemesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_codegen_jobs"]
    ) -> ListCodegenJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_components"]
    ) -> ListComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_forms"]
    ) -> ListFormsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_themes"]
    ) -> ListThemesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplifyuibuilder/client/#get_paginator)
        """
