import datetime
from typing import Any, cast, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.review_snapshot_status import ReviewSnapshotStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewSnapshot")


@attr.s(auto_attribs=True, repr=False)
class ReviewSnapshot:
    """  """

    _created_at: Union[Unset, datetime.datetime] = UNSET
    _download_url: Union[Unset, str] = UNSET
    _expires_at: Union[Unset, datetime.datetime] = UNSET
    _size: Union[Unset, int] = UNSET
    _status: Union[Unset, ReviewSnapshotStatus] = UNSET

    def __repr__(self):
        fields = []
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("download_url={}".format(repr(self._download_url)))
        fields.append("expires_at={}".format(repr(self._expires_at)))
        fields.append("size={}".format(repr(self._size)))
        fields.append("status={}".format(repr(self._status)))
        return "ReviewSnapshot({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        download_url = self._download_url
        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self._expires_at, Unset):
            expires_at = self._expires_at.isoformat()

        size = self._size
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if download_url is not UNSET:
            field_dict["downloadURL"] = download_url
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if size is not UNSET:
            field_dict["size"] = size
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_download_url() -> Union[Unset, str]:
            download_url = d.pop("downloadURL")
            return download_url

        try:
            download_url = get_download_url()
        except KeyError:
            if strict:
                raise
            download_url = cast(Union[Unset, str], UNSET)

        def get_expires_at() -> Union[Unset, datetime.datetime]:
            expires_at: Union[Unset, datetime.datetime] = UNSET
            _expires_at = d.pop("expiresAt")
            if _expires_at is not None and not isinstance(_expires_at, Unset):
                expires_at = isoparse(cast(str, _expires_at))

            return expires_at

        try:
            expires_at = get_expires_at()
        except KeyError:
            if strict:
                raise
            expires_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_size() -> Union[Unset, int]:
            size = d.pop("size")
            return size

        try:
            size = get_size()
        except KeyError:
            if strict:
                raise
            size = cast(Union[Unset, int], UNSET)

        def get_status() -> Union[Unset, ReviewSnapshotStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = ReviewSnapshotStatus(_status)
                except ValueError:
                    status = ReviewSnapshotStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, ReviewSnapshotStatus], UNSET)

        review_snapshot = cls(
            created_at=created_at,
            download_url=download_url,
            expires_at=expires_at,
            size=size,
            status=status,
        )

        return review_snapshot

    @property
    def created_at(self) -> datetime.datetime:
        """ DateTime the Review Snapshot was created at """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def download_url(self) -> str:
        """ A short-lived URL that can be used to download the original file. """
        if isinstance(self._download_url, Unset):
            raise NotPresentError(self, "download_url")
        return self._download_url

    @download_url.setter
    def download_url(self, value: str) -> None:
        self._download_url = value

    @download_url.deleter
    def download_url(self) -> None:
        self._download_url = UNSET

    @property
    def expires_at(self) -> datetime.datetime:
        """ DateTime the downloadURL expires. """
        if isinstance(self._expires_at, Unset):
            raise NotPresentError(self, "expires_at")
        return self._expires_at

    @expires_at.setter
    def expires_at(self, value: datetime.datetime) -> None:
        self._expires_at = value

    @expires_at.deleter
    def expires_at(self) -> None:
        self._expires_at = UNSET

    @property
    def size(self) -> int:
        """ Size, in bytes, of the snapshot file """
        if isinstance(self._size, Unset):
            raise NotPresentError(self, "size")
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        self._size = value

    @size.deleter
    def size(self) -> None:
        self._size = UNSET

    @property
    def status(self) -> ReviewSnapshotStatus:
        """ the current status of the Snapshot process """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: ReviewSnapshotStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
