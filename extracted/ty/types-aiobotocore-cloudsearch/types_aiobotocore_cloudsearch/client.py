"""
Type annotations for cloudsearch service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudsearch.client import CloudSearchClient

    session = get_session()
    async with session.create_client("cloudsearch") as client:
        client: CloudSearchClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    BuildSuggestersRequestTypeDef,
    BuildSuggestersResponseTypeDef,
    CreateDomainRequestTypeDef,
    CreateDomainResponseTypeDef,
    DefineAnalysisSchemeRequestTypeDef,
    DefineAnalysisSchemeResponseTypeDef,
    DefineExpressionRequestTypeDef,
    DefineExpressionResponseTypeDef,
    DefineIndexFieldRequestTypeDef,
    DefineIndexFieldResponseTypeDef,
    DefineSuggesterRequestTypeDef,
    DefineSuggesterResponseTypeDef,
    DeleteAnalysisSchemeRequestTypeDef,
    DeleteAnalysisSchemeResponseTypeDef,
    DeleteDomainRequestTypeDef,
    DeleteDomainResponseTypeDef,
    DeleteExpressionRequestTypeDef,
    DeleteExpressionResponseTypeDef,
    DeleteIndexFieldRequestTypeDef,
    DeleteIndexFieldResponseTypeDef,
    DeleteSuggesterRequestTypeDef,
    DeleteSuggesterResponseTypeDef,
    DescribeAnalysisSchemesRequestTypeDef,
    DescribeAnalysisSchemesResponseTypeDef,
    DescribeAvailabilityOptionsRequestTypeDef,
    DescribeAvailabilityOptionsResponseTypeDef,
    DescribeDomainEndpointOptionsRequestTypeDef,
    DescribeDomainEndpointOptionsResponseTypeDef,
    DescribeDomainsRequestTypeDef,
    DescribeDomainsResponseTypeDef,
    DescribeExpressionsRequestTypeDef,
    DescribeExpressionsResponseTypeDef,
    DescribeIndexFieldsRequestTypeDef,
    DescribeIndexFieldsResponseTypeDef,
    DescribeScalingParametersRequestTypeDef,
    DescribeScalingParametersResponseTypeDef,
    DescribeServiceAccessPoliciesRequestTypeDef,
    DescribeServiceAccessPoliciesResponseTypeDef,
    DescribeSuggestersRequestTypeDef,
    DescribeSuggestersResponseTypeDef,
    IndexDocumentsRequestTypeDef,
    IndexDocumentsResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    UpdateAvailabilityOptionsRequestTypeDef,
    UpdateAvailabilityOptionsResponseTypeDef,
    UpdateDomainEndpointOptionsRequestTypeDef,
    UpdateDomainEndpointOptionsResponseTypeDef,
    UpdateScalingParametersRequestTypeDef,
    UpdateScalingParametersResponseTypeDef,
    UpdateServiceAccessPoliciesRequestTypeDef,
    UpdateServiceAccessPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("CloudSearchClient",)


class Exceptions(BaseClientExceptions):
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudSearchClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudSearchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#generate_presigned_url)
        """

    async def build_suggesters(
        self, **kwargs: Unpack[BuildSuggestersRequestTypeDef]
    ) -> BuildSuggestersResponseTypeDef:
        """
        Indexes the search suggestions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/build_suggesters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#build_suggesters)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates a new search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/create_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#create_domain)
        """

    async def define_analysis_scheme(
        self, **kwargs: Unpack[DefineAnalysisSchemeRequestTypeDef]
    ) -> DefineAnalysisSchemeResponseTypeDef:
        """
        Configures an analysis scheme that can be applied to a <code>text</code> or
        <code>text-array</code> field to define language-specific text processing
        options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_analysis_scheme.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_analysis_scheme)
        """

    async def define_expression(
        self, **kwargs: Unpack[DefineExpressionRequestTypeDef]
    ) -> DefineExpressionResponseTypeDef:
        """
        Configures an <code><a>Expression</a></code> for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_expression.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_expression)
        """

    async def define_index_field(
        self, **kwargs: Unpack[DefineIndexFieldRequestTypeDef]
    ) -> DefineIndexFieldResponseTypeDef:
        """
        Configures an <code><a>IndexField</a></code> for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_index_field.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_index_field)
        """

    async def define_suggester(
        self, **kwargs: Unpack[DefineSuggesterRequestTypeDef]
    ) -> DefineSuggesterResponseTypeDef:
        """
        Configures a suggester for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/define_suggester.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#define_suggester)
        """

    async def delete_analysis_scheme(
        self, **kwargs: Unpack[DeleteAnalysisSchemeRequestTypeDef]
    ) -> DeleteAnalysisSchemeResponseTypeDef:
        """
        Deletes an analysis scheme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_analysis_scheme.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_analysis_scheme)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestTypeDef]
    ) -> DeleteDomainResponseTypeDef:
        """
        Permanently deletes a search domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_domain)
        """

    async def delete_expression(
        self, **kwargs: Unpack[DeleteExpressionRequestTypeDef]
    ) -> DeleteExpressionResponseTypeDef:
        """
        Removes an <code><a>Expression</a></code> from the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_expression.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_expression)
        """

    async def delete_index_field(
        self, **kwargs: Unpack[DeleteIndexFieldRequestTypeDef]
    ) -> DeleteIndexFieldResponseTypeDef:
        """
        Removes an <code><a>IndexField</a></code> from the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_index_field.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_index_field)
        """

    async def delete_suggester(
        self, **kwargs: Unpack[DeleteSuggesterRequestTypeDef]
    ) -> DeleteSuggesterResponseTypeDef:
        """
        Deletes a suggester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/delete_suggester.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#delete_suggester)
        """

    async def describe_analysis_schemes(
        self, **kwargs: Unpack[DescribeAnalysisSchemesRequestTypeDef]
    ) -> DescribeAnalysisSchemesResponseTypeDef:
        """
        Gets the analysis schemes configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_analysis_schemes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_analysis_schemes)
        """

    async def describe_availability_options(
        self, **kwargs: Unpack[DescribeAvailabilityOptionsRequestTypeDef]
    ) -> DescribeAvailabilityOptionsResponseTypeDef:
        """
        Gets the availability options configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_availability_options.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_availability_options)
        """

    async def describe_domain_endpoint_options(
        self, **kwargs: Unpack[DescribeDomainEndpointOptionsRequestTypeDef]
    ) -> DescribeDomainEndpointOptionsResponseTypeDef:
        """
        Returns the domain's endpoint options, specifically whether all requests to the
        domain must arrive over HTTPS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_domain_endpoint_options.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_domain_endpoint_options)
        """

    async def describe_domains(
        self, **kwargs: Unpack[DescribeDomainsRequestTypeDef]
    ) -> DescribeDomainsResponseTypeDef:
        """
        Gets information about the search domains owned by this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_domains.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_domains)
        """

    async def describe_expressions(
        self, **kwargs: Unpack[DescribeExpressionsRequestTypeDef]
    ) -> DescribeExpressionsResponseTypeDef:
        """
        Gets the expressions configured for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_expressions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_expressions)
        """

    async def describe_index_fields(
        self, **kwargs: Unpack[DescribeIndexFieldsRequestTypeDef]
    ) -> DescribeIndexFieldsResponseTypeDef:
        """
        Gets information about the index fields configured for the search domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_index_fields.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_index_fields)
        """

    async def describe_scaling_parameters(
        self, **kwargs: Unpack[DescribeScalingParametersRequestTypeDef]
    ) -> DescribeScalingParametersResponseTypeDef:
        """
        Gets the scaling parameters configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_scaling_parameters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_scaling_parameters)
        """

    async def describe_service_access_policies(
        self, **kwargs: Unpack[DescribeServiceAccessPoliciesRequestTypeDef]
    ) -> DescribeServiceAccessPoliciesResponseTypeDef:
        """
        Gets information about the access policies that control access to the domain's
        document and search endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_service_access_policies.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_service_access_policies)
        """

    async def describe_suggesters(
        self, **kwargs: Unpack[DescribeSuggestersRequestTypeDef]
    ) -> DescribeSuggestersResponseTypeDef:
        """
        Gets the suggesters configured for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/describe_suggesters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#describe_suggesters)
        """

    async def index_documents(
        self, **kwargs: Unpack[IndexDocumentsRequestTypeDef]
    ) -> IndexDocumentsResponseTypeDef:
        """
        Tells the search domain to start indexing its documents using the latest
        indexing options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/index_documents.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#index_documents)
        """

    async def list_domain_names(self) -> ListDomainNamesResponseTypeDef:
        """
        Lists all search domains owned by an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/list_domain_names.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#list_domain_names)
        """

    async def update_availability_options(
        self, **kwargs: Unpack[UpdateAvailabilityOptionsRequestTypeDef]
    ) -> UpdateAvailabilityOptionsResponseTypeDef:
        """
        Configures the availability options for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_availability_options.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_availability_options)
        """

    async def update_domain_endpoint_options(
        self, **kwargs: Unpack[UpdateDomainEndpointOptionsRequestTypeDef]
    ) -> UpdateDomainEndpointOptionsResponseTypeDef:
        """
        Updates the domain's endpoint options, specifically whether all requests to the
        domain must arrive over HTTPS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_domain_endpoint_options.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_domain_endpoint_options)
        """

    async def update_scaling_parameters(
        self, **kwargs: Unpack[UpdateScalingParametersRequestTypeDef]
    ) -> UpdateScalingParametersResponseTypeDef:
        """
        Configures scaling parameters for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_scaling_parameters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_scaling_parameters)
        """

    async def update_service_access_policies(
        self, **kwargs: Unpack[UpdateServiceAccessPoliciesRequestTypeDef]
    ) -> UpdateServiceAccessPoliciesResponseTypeDef:
        """
        Configures the access rules that control access to the domain's document and
        search endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch/client/update_service_access_policies.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/#update_service_access_policies)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudsearch/client/)
        """
