from collections.abc import Iterable
from datetime import datetime
from enum import StrEnum
from typing import IO, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ContentRangePattern = str
ContentType = str
ETag = str
ErrorMessage = str
ItemName = str
ListLimit = int
ListPathNaming = str
PaginationToken = str
PathNaming = str
RangePattern = str
SHA256Hash = str
StringPrimitive = str
statusCode = int


class ItemType(StrEnum):
    OBJECT = "OBJECT"
    FOLDER = "FOLDER"


class StorageClass(StrEnum):
    TEMPORAL = "TEMPORAL"


class UploadAvailability(StrEnum):
    STANDARD = "STANDARD"
    STREAMING = "STREAMING"


class ContainerNotFoundException(ServiceException):
    """The specified container was not found for the specified account."""

    code: str = "ContainerNotFoundException"
    sender_fault: bool = False
    status_code: int = 404


class InternalServerError(ServiceException):
    """The service is temporarily unavailable."""

    code: str = "InternalServerError"
    sender_fault: bool = False
    status_code: int = 400


class ObjectNotFoundException(ServiceException):
    """Could not perform an operation on an object that does not exist."""

    code: str = "ObjectNotFoundException"
    sender_fault: bool = False
    status_code: int = 404


class RequestedRangeNotSatisfiableException(ServiceException):
    """The requested content range is not valid."""

    code: str = "RequestedRangeNotSatisfiableException"
    sender_fault: bool = False
    status_code: int = 416


class DeleteObjectRequest(ServiceRequest):
    Path: PathNaming


class DeleteObjectResponse(TypedDict, total=False):
    pass


class DescribeObjectRequest(ServiceRequest):
    Path: PathNaming


TimeStamp = datetime
NonNegativeLong = int


class DescribeObjectResponse(TypedDict, total=False):
    ETag: ETag | None
    ContentType: ContentType | None
    ContentLength: NonNegativeLong | None
    CacheControl: StringPrimitive | None
    LastModified: TimeStamp | None


class GetObjectRequest(ServiceRequest):
    Path: PathNaming
    Range: RangePattern | None


PayloadBlob = bytes


class GetObjectResponse(TypedDict, total=False):
    Body: PayloadBlob | IO[PayloadBlob] | Iterable[PayloadBlob] | None
    CacheControl: StringPrimitive | None
    ContentRange: ContentRangePattern | None
    ContentLength: NonNegativeLong | None
    ContentType: ContentType | None
    ETag: ETag | None
    LastModified: TimeStamp | None
    StatusCode: statusCode


class Item(TypedDict, total=False):
    """A metadata entry for a folder or object."""

    Name: ItemName | None
    Type: ItemType | None
    ETag: ETag | None
    LastModified: TimeStamp | None
    ContentType: ContentType | None
    ContentLength: NonNegativeLong | None


ItemList = list[Item]


class ListItemsRequest(ServiceRequest):
    Path: ListPathNaming | None
    MaxResults: ListLimit | None
    NextToken: PaginationToken | None


class ListItemsResponse(TypedDict, total=False):
    Items: ItemList | None
    NextToken: PaginationToken | None


class PutObjectRequest(ServiceRequest):
    Body: IO[PayloadBlob]
    Path: PathNaming
    ContentType: ContentType | None
    CacheControl: StringPrimitive | None
    StorageClass: StorageClass | None
    UploadAvailability: UploadAvailability | None


class PutObjectResponse(TypedDict, total=False):
    ContentSHA256: SHA256Hash | None
    ETag: ETag | None
    StorageClass: StorageClass | None


class MediastoreDataApi:
    service: str = "mediastore-data"
    version: str = "2017-09-01"

    @handler("DeleteObject")
    def delete_object(
        self, context: RequestContext, path: PathNaming, **kwargs
    ) -> DeleteObjectResponse:
        """Deletes an object at the specified path.

        :param path: The path (including the file name) where the object is stored in the
        container.
        :returns: DeleteObjectResponse
        :raises ContainerNotFoundException:
        :raises ObjectNotFoundException:
        :raises InternalServerError:
        """
        raise NotImplementedError

    @handler("DescribeObject")
    def describe_object(
        self, context: RequestContext, path: PathNaming, **kwargs
    ) -> DescribeObjectResponse:
        """Gets the headers for an object at the specified path.

        :param path: The path (including the file name) where the object is stored in the
        container.
        :returns: DescribeObjectResponse
        :raises ContainerNotFoundException:
        :raises ObjectNotFoundException:
        :raises InternalServerError:
        """
        raise NotImplementedError

    @handler("GetObject")
    def get_object(
        self, context: RequestContext, path: PathNaming, range: RangePattern | None = None, **kwargs
    ) -> GetObjectResponse:
        """Downloads the object at the specified path. If the object’s upload
        availability is set to ``streaming``, AWS Elemental MediaStore downloads
        the object even if it’s still uploading the object.

        :param path: The path (including the file name) where the object is stored in the
        container.
        :param range: The range bytes of an object to retrieve.
        :returns: GetObjectResponse
        :raises ContainerNotFoundException:
        :raises ObjectNotFoundException:
        :raises RequestedRangeNotSatisfiableException:
        :raises InternalServerError:
        """
        raise NotImplementedError

    @handler("ListItems")
    def list_items(
        self,
        context: RequestContext,
        path: ListPathNaming | None = None,
        max_results: ListLimit | None = None,
        next_token: PaginationToken | None = None,
        **kwargs,
    ) -> ListItemsResponse:
        """Provides a list of metadata entries about folders and objects in the
        specified folder.

        :param path: The path in the container from which to retrieve items.
        :param max_results: The maximum number of results to return per API request.
        :param next_token: The token that identifies which batch of results that you want to see.
        :returns: ListItemsResponse
        :raises ContainerNotFoundException:
        :raises InternalServerError:
        """
        raise NotImplementedError

    @handler("PutObject")
    def put_object(
        self,
        context: RequestContext,
        body: IO[PayloadBlob],
        path: PathNaming,
        content_type: ContentType | None = None,
        cache_control: StringPrimitive | None = None,
        storage_class: StorageClass | None = None,
        upload_availability: UploadAvailability | None = None,
        **kwargs,
    ) -> PutObjectResponse:
        """Uploads an object to the specified path. Object sizes are limited to 25
        MB for standard upload availability and 10 MB for streaming upload
        availability.

        :param body: The bytes to be stored.
        :param path: The path (including the file name) where the object is stored in the
        container.
        :param content_type: The content type of the object.
        :param cache_control: An optional ``CacheControl`` header that allows the caller to control
        the object's cache behavior.
        :param storage_class: Indicates the storage class of a ``Put`` request.
        :param upload_availability: Indicates the availability of an object while it is still uploading.
        :returns: PutObjectResponse
        :raises ContainerNotFoundException:
        :raises InternalServerError:
        """
        raise NotImplementedError
