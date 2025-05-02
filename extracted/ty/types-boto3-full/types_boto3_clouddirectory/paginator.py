"""
Type annotations for clouddirectory service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_clouddirectory.client import CloudDirectoryClient
    from types_boto3_clouddirectory.paginator import (
        ListAppliedSchemaArnsPaginator,
        ListAttachedIndicesPaginator,
        ListDevelopmentSchemaArnsPaginator,
        ListDirectoriesPaginator,
        ListFacetAttributesPaginator,
        ListFacetNamesPaginator,
        ListIncomingTypedLinksPaginator,
        ListIndexPaginator,
        ListManagedSchemaArnsPaginator,
        ListObjectAttributesPaginator,
        ListObjectParentPathsPaginator,
        ListObjectPoliciesPaginator,
        ListOutgoingTypedLinksPaginator,
        ListPolicyAttachmentsPaginator,
        ListPublishedSchemaArnsPaginator,
        ListTagsForResourcePaginator,
        ListTypedLinkFacetAttributesPaginator,
        ListTypedLinkFacetNamesPaginator,
        LookupPolicyPaginator,
    )

    session = Session()
    client: CloudDirectoryClient = session.client("clouddirectory")

    list_applied_schema_arns_paginator: ListAppliedSchemaArnsPaginator = client.get_paginator("list_applied_schema_arns")
    list_attached_indices_paginator: ListAttachedIndicesPaginator = client.get_paginator("list_attached_indices")
    list_development_schema_arns_paginator: ListDevelopmentSchemaArnsPaginator = client.get_paginator("list_development_schema_arns")
    list_directories_paginator: ListDirectoriesPaginator = client.get_paginator("list_directories")
    list_facet_attributes_paginator: ListFacetAttributesPaginator = client.get_paginator("list_facet_attributes")
    list_facet_names_paginator: ListFacetNamesPaginator = client.get_paginator("list_facet_names")
    list_incoming_typed_links_paginator: ListIncomingTypedLinksPaginator = client.get_paginator("list_incoming_typed_links")
    list_index_paginator: ListIndexPaginator = client.get_paginator("list_index")
    list_managed_schema_arns_paginator: ListManagedSchemaArnsPaginator = client.get_paginator("list_managed_schema_arns")
    list_object_attributes_paginator: ListObjectAttributesPaginator = client.get_paginator("list_object_attributes")
    list_object_parent_paths_paginator: ListObjectParentPathsPaginator = client.get_paginator("list_object_parent_paths")
    list_object_policies_paginator: ListObjectPoliciesPaginator = client.get_paginator("list_object_policies")
    list_outgoing_typed_links_paginator: ListOutgoingTypedLinksPaginator = client.get_paginator("list_outgoing_typed_links")
    list_policy_attachments_paginator: ListPolicyAttachmentsPaginator = client.get_paginator("list_policy_attachments")
    list_published_schema_arns_paginator: ListPublishedSchemaArnsPaginator = client.get_paginator("list_published_schema_arns")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_typed_link_facet_attributes_paginator: ListTypedLinkFacetAttributesPaginator = client.get_paginator("list_typed_link_facet_attributes")
    list_typed_link_facet_names_paginator: ListTypedLinkFacetNamesPaginator = client.get_paginator("list_typed_link_facet_names")
    lookup_policy_paginator: LookupPolicyPaginator = client.get_paginator("lookup_policy")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAppliedSchemaArnsRequestPaginateTypeDef,
    ListAppliedSchemaArnsResponseTypeDef,
    ListAttachedIndicesRequestPaginateTypeDef,
    ListAttachedIndicesResponseTypeDef,
    ListDevelopmentSchemaArnsRequestPaginateTypeDef,
    ListDevelopmentSchemaArnsResponseTypeDef,
    ListDirectoriesRequestPaginateTypeDef,
    ListDirectoriesResponseTypeDef,
    ListFacetAttributesRequestPaginateTypeDef,
    ListFacetAttributesResponseTypeDef,
    ListFacetNamesRequestPaginateTypeDef,
    ListFacetNamesResponseTypeDef,
    ListIncomingTypedLinksRequestPaginateTypeDef,
    ListIncomingTypedLinksResponseTypeDef,
    ListIndexRequestPaginateTypeDef,
    ListIndexResponseTypeDef,
    ListManagedSchemaArnsRequestPaginateTypeDef,
    ListManagedSchemaArnsResponseTypeDef,
    ListObjectAttributesRequestPaginateTypeDef,
    ListObjectAttributesResponseTypeDef,
    ListObjectParentPathsRequestPaginateTypeDef,
    ListObjectParentPathsResponseTypeDef,
    ListObjectPoliciesRequestPaginateTypeDef,
    ListObjectPoliciesResponseTypeDef,
    ListOutgoingTypedLinksRequestPaginateTypeDef,
    ListOutgoingTypedLinksResponseTypeDef,
    ListPolicyAttachmentsRequestPaginateTypeDef,
    ListPolicyAttachmentsResponseTypeDef,
    ListPublishedSchemaArnsRequestPaginateTypeDef,
    ListPublishedSchemaArnsResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypedLinkFacetAttributesRequestPaginateTypeDef,
    ListTypedLinkFacetAttributesResponseTypeDef,
    ListTypedLinkFacetNamesRequestPaginateTypeDef,
    ListTypedLinkFacetNamesResponseTypeDef,
    LookupPolicyRequestPaginateTypeDef,
    LookupPolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAppliedSchemaArnsPaginator",
    "ListAttachedIndicesPaginator",
    "ListDevelopmentSchemaArnsPaginator",
    "ListDirectoriesPaginator",
    "ListFacetAttributesPaginator",
    "ListFacetNamesPaginator",
    "ListIncomingTypedLinksPaginator",
    "ListIndexPaginator",
    "ListManagedSchemaArnsPaginator",
    "ListObjectAttributesPaginator",
    "ListObjectParentPathsPaginator",
    "ListObjectPoliciesPaginator",
    "ListOutgoingTypedLinksPaginator",
    "ListPolicyAttachmentsPaginator",
    "ListPublishedSchemaArnsPaginator",
    "ListTagsForResourcePaginator",
    "ListTypedLinkFacetAttributesPaginator",
    "ListTypedLinkFacetNamesPaginator",
    "LookupPolicyPaginator",
)


if TYPE_CHECKING:
    _ListAppliedSchemaArnsPaginatorBase = Paginator[ListAppliedSchemaArnsResponseTypeDef]
else:
    _ListAppliedSchemaArnsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAppliedSchemaArnsPaginator(_ListAppliedSchemaArnsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAppliedSchemaArns.html#CloudDirectory.Paginator.ListAppliedSchemaArns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listappliedschemaarnspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppliedSchemaArnsRequestPaginateTypeDef]
    ) -> PageIterator[ListAppliedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAppliedSchemaArns.html#CloudDirectory.Paginator.ListAppliedSchemaArns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listappliedschemaarnspaginator)
        """


if TYPE_CHECKING:
    _ListAttachedIndicesPaginatorBase = Paginator[ListAttachedIndicesResponseTypeDef]
else:
    _ListAttachedIndicesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAttachedIndicesPaginator(_ListAttachedIndicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAttachedIndices.html#CloudDirectory.Paginator.ListAttachedIndices)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listattachedindicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachedIndicesRequestPaginateTypeDef]
    ) -> PageIterator[ListAttachedIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListAttachedIndices.html#CloudDirectory.Paginator.ListAttachedIndices.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listattachedindicespaginator)
        """


if TYPE_CHECKING:
    _ListDevelopmentSchemaArnsPaginatorBase = Paginator[ListDevelopmentSchemaArnsResponseTypeDef]
else:
    _ListDevelopmentSchemaArnsPaginatorBase = Paginator  # type: ignore[assignment]


class ListDevelopmentSchemaArnsPaginator(_ListDevelopmentSchemaArnsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDevelopmentSchemaArns.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listdevelopmentschemaarnspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevelopmentSchemaArnsRequestPaginateTypeDef]
    ) -> PageIterator[ListDevelopmentSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDevelopmentSchemaArns.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listdevelopmentschemaarnspaginator)
        """


if TYPE_CHECKING:
    _ListDirectoriesPaginatorBase = Paginator[ListDirectoriesResponseTypeDef]
else:
    _ListDirectoriesPaginatorBase = Paginator  # type: ignore[assignment]


class ListDirectoriesPaginator(_ListDirectoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDirectories.html#CloudDirectory.Paginator.ListDirectories)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listdirectoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDirectoriesRequestPaginateTypeDef]
    ) -> PageIterator[ListDirectoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListDirectories.html#CloudDirectory.Paginator.ListDirectories.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listdirectoriespaginator)
        """


if TYPE_CHECKING:
    _ListFacetAttributesPaginatorBase = Paginator[ListFacetAttributesResponseTypeDef]
else:
    _ListFacetAttributesPaginatorBase = Paginator  # type: ignore[assignment]


class ListFacetAttributesPaginator(_ListFacetAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetAttributes.html#CloudDirectory.Paginator.ListFacetAttributes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listfacetattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFacetAttributesRequestPaginateTypeDef]
    ) -> PageIterator[ListFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetAttributes.html#CloudDirectory.Paginator.ListFacetAttributes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listfacetattributespaginator)
        """


if TYPE_CHECKING:
    _ListFacetNamesPaginatorBase = Paginator[ListFacetNamesResponseTypeDef]
else:
    _ListFacetNamesPaginatorBase = Paginator  # type: ignore[assignment]


class ListFacetNamesPaginator(_ListFacetNamesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetNames.html#CloudDirectory.Paginator.ListFacetNames)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listfacetnamespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFacetNamesRequestPaginateTypeDef]
    ) -> PageIterator[ListFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListFacetNames.html#CloudDirectory.Paginator.ListFacetNames.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listfacetnamespaginator)
        """


if TYPE_CHECKING:
    _ListIncomingTypedLinksPaginatorBase = Paginator[ListIncomingTypedLinksResponseTypeDef]
else:
    _ListIncomingTypedLinksPaginatorBase = Paginator  # type: ignore[assignment]


class ListIncomingTypedLinksPaginator(_ListIncomingTypedLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIncomingTypedLinks.html#CloudDirectory.Paginator.ListIncomingTypedLinks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listincomingtypedlinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIncomingTypedLinksRequestPaginateTypeDef]
    ) -> PageIterator[ListIncomingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIncomingTypedLinks.html#CloudDirectory.Paginator.ListIncomingTypedLinks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listincomingtypedlinkspaginator)
        """


if TYPE_CHECKING:
    _ListIndexPaginatorBase = Paginator[ListIndexResponseTypeDef]
else:
    _ListIndexPaginatorBase = Paginator  # type: ignore[assignment]


class ListIndexPaginator(_ListIndexPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIndex.html#CloudDirectory.Paginator.ListIndex)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listindexpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIndexRequestPaginateTypeDef]
    ) -> PageIterator[ListIndexResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListIndex.html#CloudDirectory.Paginator.ListIndex.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listindexpaginator)
        """


if TYPE_CHECKING:
    _ListManagedSchemaArnsPaginatorBase = Paginator[ListManagedSchemaArnsResponseTypeDef]
else:
    _ListManagedSchemaArnsPaginatorBase = Paginator  # type: ignore[assignment]


class ListManagedSchemaArnsPaginator(_ListManagedSchemaArnsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListManagedSchemaArns.html#CloudDirectory.Paginator.ListManagedSchemaArns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listmanagedschemaarnspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedSchemaArnsRequestPaginateTypeDef]
    ) -> PageIterator[ListManagedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListManagedSchemaArns.html#CloudDirectory.Paginator.ListManagedSchemaArns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listmanagedschemaarnspaginator)
        """


if TYPE_CHECKING:
    _ListObjectAttributesPaginatorBase = Paginator[ListObjectAttributesResponseTypeDef]
else:
    _ListObjectAttributesPaginatorBase = Paginator  # type: ignore[assignment]


class ListObjectAttributesPaginator(_ListObjectAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectAttributes.html#CloudDirectory.Paginator.ListObjectAttributes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listobjectattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListObjectAttributesRequestPaginateTypeDef]
    ) -> PageIterator[ListObjectAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectAttributes.html#CloudDirectory.Paginator.ListObjectAttributes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listobjectattributespaginator)
        """


if TYPE_CHECKING:
    _ListObjectParentPathsPaginatorBase = Paginator[ListObjectParentPathsResponseTypeDef]
else:
    _ListObjectParentPathsPaginatorBase = Paginator  # type: ignore[assignment]


class ListObjectParentPathsPaginator(_ListObjectParentPathsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectParentPaths.html#CloudDirectory.Paginator.ListObjectParentPaths)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listobjectparentpathspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListObjectParentPathsRequestPaginateTypeDef]
    ) -> PageIterator[ListObjectParentPathsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectParentPaths.html#CloudDirectory.Paginator.ListObjectParentPaths.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listobjectparentpathspaginator)
        """


if TYPE_CHECKING:
    _ListObjectPoliciesPaginatorBase = Paginator[ListObjectPoliciesResponseTypeDef]
else:
    _ListObjectPoliciesPaginatorBase = Paginator  # type: ignore[assignment]


class ListObjectPoliciesPaginator(_ListObjectPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectPolicies.html#CloudDirectory.Paginator.ListObjectPolicies)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listobjectpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListObjectPoliciesRequestPaginateTypeDef]
    ) -> PageIterator[ListObjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListObjectPolicies.html#CloudDirectory.Paginator.ListObjectPolicies.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listobjectpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListOutgoingTypedLinksPaginatorBase = Paginator[ListOutgoingTypedLinksResponseTypeDef]
else:
    _ListOutgoingTypedLinksPaginatorBase = Paginator  # type: ignore[assignment]


class ListOutgoingTypedLinksPaginator(_ListOutgoingTypedLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListOutgoingTypedLinks.html#CloudDirectory.Paginator.ListOutgoingTypedLinks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listoutgoingtypedlinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOutgoingTypedLinksRequestPaginateTypeDef]
    ) -> PageIterator[ListOutgoingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListOutgoingTypedLinks.html#CloudDirectory.Paginator.ListOutgoingTypedLinks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listoutgoingtypedlinkspaginator)
        """


if TYPE_CHECKING:
    _ListPolicyAttachmentsPaginatorBase = Paginator[ListPolicyAttachmentsResponseTypeDef]
else:
    _ListPolicyAttachmentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPolicyAttachmentsPaginator(_ListPolicyAttachmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPolicyAttachments.html#CloudDirectory.Paginator.ListPolicyAttachments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listpolicyattachmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyAttachmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListPolicyAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPolicyAttachments.html#CloudDirectory.Paginator.ListPolicyAttachments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listpolicyattachmentspaginator)
        """


if TYPE_CHECKING:
    _ListPublishedSchemaArnsPaginatorBase = Paginator[ListPublishedSchemaArnsResponseTypeDef]
else:
    _ListPublishedSchemaArnsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPublishedSchemaArnsPaginator(_ListPublishedSchemaArnsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPublishedSchemaArns.html#CloudDirectory.Paginator.ListPublishedSchemaArns)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listpublishedschemaarnspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPublishedSchemaArnsRequestPaginateTypeDef]
    ) -> PageIterator[ListPublishedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListPublishedSchemaArns.html#CloudDirectory.Paginator.ListPublishedSchemaArns.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listpublishedschemaarnspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = Paginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = Paginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTagsForResource.html#CloudDirectory.Paginator.ListTagsForResource)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTagsForResource.html#CloudDirectory.Paginator.ListTagsForResource.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListTypedLinkFacetAttributesPaginatorBase = Paginator[
        ListTypedLinkFacetAttributesResponseTypeDef
    ]
else:
    _ListTypedLinkFacetAttributesPaginatorBase = Paginator  # type: ignore[assignment]


class ListTypedLinkFacetAttributesPaginator(_ListTypedLinkFacetAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetAttributes.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listtypedlinkfacetattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTypedLinkFacetAttributesRequestPaginateTypeDef]
    ) -> PageIterator[ListTypedLinkFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetAttributes.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listtypedlinkfacetattributespaginator)
        """


if TYPE_CHECKING:
    _ListTypedLinkFacetNamesPaginatorBase = Paginator[ListTypedLinkFacetNamesResponseTypeDef]
else:
    _ListTypedLinkFacetNamesPaginatorBase = Paginator  # type: ignore[assignment]


class ListTypedLinkFacetNamesPaginator(_ListTypedLinkFacetNamesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetNames.html#CloudDirectory.Paginator.ListTypedLinkFacetNames)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listtypedlinkfacetnamespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTypedLinkFacetNamesRequestPaginateTypeDef]
    ) -> PageIterator[ListTypedLinkFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/ListTypedLinkFacetNames.html#CloudDirectory.Paginator.ListTypedLinkFacetNames.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#listtypedlinkfacetnamespaginator)
        """


if TYPE_CHECKING:
    _LookupPolicyPaginatorBase = Paginator[LookupPolicyResponseTypeDef]
else:
    _LookupPolicyPaginatorBase = Paginator  # type: ignore[assignment]


class LookupPolicyPaginator(_LookupPolicyPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/LookupPolicy.html#CloudDirectory.Paginator.LookupPolicy)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#lookuppolicypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[LookupPolicyRequestPaginateTypeDef]
    ) -> PageIterator[LookupPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory/paginator/LookupPolicy.html#CloudDirectory.Paginator.LookupPolicy.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/paginators/#lookuppolicypaginator)
        """
