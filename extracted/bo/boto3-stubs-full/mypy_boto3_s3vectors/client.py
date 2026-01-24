"""
Type annotations for s3vectors service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_s3vectors.client import S3VectorsClient

    session = Session()
    client: S3VectorsClient = session.client("s3vectors")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListIndexesPaginator, ListVectorBucketsPaginator, ListVectorsPaginator
from .type_defs import (
    CreateIndexInputTypeDef,
    CreateIndexOutputTypeDef,
    CreateVectorBucketInputTypeDef,
    CreateVectorBucketOutputTypeDef,
    DeleteIndexInputTypeDef,
    DeleteVectorBucketInputTypeDef,
    DeleteVectorBucketPolicyInputTypeDef,
    DeleteVectorsInputTypeDef,
    GetIndexInputTypeDef,
    GetIndexOutputTypeDef,
    GetVectorBucketInputTypeDef,
    GetVectorBucketOutputTypeDef,
    GetVectorBucketPolicyInputTypeDef,
    GetVectorBucketPolicyOutputTypeDef,
    GetVectorsInputTypeDef,
    GetVectorsOutputTypeDef,
    ListIndexesInputTypeDef,
    ListIndexesOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVectorBucketsInputTypeDef,
    ListVectorBucketsOutputTypeDef,
    ListVectorsInputTypeDef,
    ListVectorsOutputTypeDef,
    PutVectorBucketPolicyInputTypeDef,
    PutVectorsInputTypeDef,
    QueryVectorsInputTypeDef,
    QueryVectorsOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("S3VectorsClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    KmsDisabledException: type[BotocoreClientError]
    KmsInvalidKeyUsageException: type[BotocoreClientError]
    KmsInvalidStateException: type[BotocoreClientError]
    KmsNotFoundException: type[BotocoreClientError]
    NotFoundException: type[BotocoreClientError]
    RequestTimeoutException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class S3VectorsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html#S3Vectors.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3VectorsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html#S3Vectors.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#generate_presigned_url)
        """

    def create_index(self, **kwargs: Unpack[CreateIndexInputTypeDef]) -> CreateIndexOutputTypeDef:
        """
        Creates a vector index within a vector bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/create_index.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#create_index)
        """

    def create_vector_bucket(
        self, **kwargs: Unpack[CreateVectorBucketInputTypeDef]
    ) -> CreateVectorBucketOutputTypeDef:
        """
        Creates a vector bucket in the Amazon Web Services Region that you want your
        bucket to be in.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/create_vector_bucket.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#create_vector_bucket)
        """

    def delete_index(self, **kwargs: Unpack[DeleteIndexInputTypeDef]) -> dict[str, Any]:
        """
        Deletes a vector index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/delete_index.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#delete_index)
        """

    def delete_vector_bucket(
        self, **kwargs: Unpack[DeleteVectorBucketInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a vector bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/delete_vector_bucket.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#delete_vector_bucket)
        """

    def delete_vector_bucket_policy(
        self, **kwargs: Unpack[DeleteVectorBucketPolicyInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a vector bucket policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/delete_vector_bucket_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#delete_vector_bucket_policy)
        """

    def delete_vectors(self, **kwargs: Unpack[DeleteVectorsInputTypeDef]) -> dict[str, Any]:
        """
        Deletes one or more vectors in a vector index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/delete_vectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#delete_vectors)
        """

    def get_index(self, **kwargs: Unpack[GetIndexInputTypeDef]) -> GetIndexOutputTypeDef:
        """
        Returns vector index attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/get_index.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#get_index)
        """

    def get_vector_bucket(
        self, **kwargs: Unpack[GetVectorBucketInputTypeDef]
    ) -> GetVectorBucketOutputTypeDef:
        """
        Returns vector bucket attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/get_vector_bucket.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#get_vector_bucket)
        """

    def get_vector_bucket_policy(
        self, **kwargs: Unpack[GetVectorBucketPolicyInputTypeDef]
    ) -> GetVectorBucketPolicyOutputTypeDef:
        """
        Gets details about a vector bucket policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/get_vector_bucket_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#get_vector_bucket_policy)
        """

    def get_vectors(self, **kwargs: Unpack[GetVectorsInputTypeDef]) -> GetVectorsOutputTypeDef:
        """
        Returns vector attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/get_vectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#get_vectors)
        """

    def list_indexes(self, **kwargs: Unpack[ListIndexesInputTypeDef]) -> ListIndexesOutputTypeDef:
        """
        Returns a list of all the vector indexes within the specified vector bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/list_indexes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#list_indexes)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists all of the tags applied to a specified Amazon S3 Vectors resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#list_tags_for_resource)
        """

    def list_vector_buckets(
        self, **kwargs: Unpack[ListVectorBucketsInputTypeDef]
    ) -> ListVectorBucketsOutputTypeDef:
        """
        Returns a list of all the vector buckets that are owned by the authenticated
        sender of the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/list_vector_buckets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#list_vector_buckets)
        """

    def list_vectors(self, **kwargs: Unpack[ListVectorsInputTypeDef]) -> ListVectorsOutputTypeDef:
        """
        List vectors in the specified vector index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/list_vectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#list_vectors)
        """

    def put_vector_bucket_policy(
        self, **kwargs: Unpack[PutVectorBucketPolicyInputTypeDef]
    ) -> dict[str, Any]:
        """
        Creates a bucket policy for a vector bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/put_vector_bucket_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#put_vector_bucket_policy)
        """

    def put_vectors(self, **kwargs: Unpack[PutVectorsInputTypeDef]) -> dict[str, Any]:
        """
        Adds one or more vectors to a vector index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/put_vectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#put_vectors)
        """

    def query_vectors(
        self, **kwargs: Unpack[QueryVectorsInputTypeDef]
    ) -> QueryVectorsOutputTypeDef:
        """
        Performs an approximate nearest neighbor search query in a vector index using a
        query vector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/query_vectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#query_vectors)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Applies one or more user-defined tags to an Amazon S3 Vectors resource or
        updates existing tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes the specified user-defined tags from an Amazon S3 Vectors resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_indexes"]
    ) -> ListIndexesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_vector_buckets"]
    ) -> ListVectorBucketsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_vectors"]
    ) -> ListVectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3vectors/client/#get_paginator)
        """
