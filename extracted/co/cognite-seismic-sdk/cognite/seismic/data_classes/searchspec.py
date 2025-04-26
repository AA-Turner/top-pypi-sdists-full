import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import LastModifiedFilter, SearchSpec
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        SearchFilesRequest,
        SearchSeismicsRequest,
        SearchSeismicStoresRequest,
    )


class SearchSpecBase(ABC):
    """Base class for search specs. The concrete implementations are
    :py:class:`~cognite.seismic.data_classes.searchspec.SearchSpecGetAll`,
    :py:class:`~cognite.seismic.data_classes.searchspec.SearchSpecLastModified`,
    :py:class:`~cognite.seismic.data_classes.searchspec.SearchSpecSurvey`,
    :py:class:`~cognite.seismic.data_classes.searchspec.SearchSpecSeismicStore`,
    :py:class:`~cognite.seismic.data_classes.searchspec.SearchSpecFile`.
    """

    @abstractmethod
    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        pass

    @abstractmethod
    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        pass

    @abstractmethod
    def _to_search_files_request(self) -> "SearchFilesRequest":
        pass


@dataclass(eq=True, frozen=True)
class SearchSpecUnion:
    id: Optional[int] = None
    external_id: Optional[str] = None
    external_id_substring: Optional[str] = None
    name: Optional[str] = None
    name_substring: Optional[str] = None
    uuid: Optional[str] = None

    def __init__(
        self,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        external_id_substring: Optional[str] = None,
        name: Optional[str] = None,
        name_substring: Optional[str] = None,
        uuid: Optional[str] = None,
    ):
        spec_count = sum(x is not None for x in [id, external_id, external_id_substring, name, name_substring, uuid])
        if spec_count > 1:
            raise ValueError(
                "You should specify only one of id, external_id, external_id_substring, name, \
                        name_substring, uuid when searching for objects"
            )
        # We can't do self.id = id, since the class is declared as frozen.
        # This workaround is the same as the generated __init__ method would have.
        object.__setattr__(self, "id", id)
        object.__setattr__(self, "external_id", external_id)
        object.__setattr__(self, "external_id_substring", external_id_substring)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "name_substring", name_substring)
        object.__setattr__(self, "uuid", uuid)

    def _to_search_spec(self) -> "SearchSpec":
        spec = SearchSpec()
        if self.id is not None:
            spec.id = self.id
        if self.uuid is not None:
            spec.id_string = self.uuid
        if self.external_id is not None:
            spec.external_id = self.external_id
        if self.external_id_substring is not None:
            spec.external_id_substring = self.external_id_substring
        if self.name is not None:
            spec.name = self.name
        if self.name_substring is not None:
            spec.name_substring = self.name_substring
        return spec


@dataclass(eq=True, frozen=True)
class SearchSpecGetAll(SearchSpecBase):
    """Defines a spec to search for all objects."""

    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        """Create a SearchSeismicStoreReqeust that will fetch all seismic stores"""
        return SearchSeismicStoresRequest()

    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        return SearchSeismicsRequest()

    def _to_search_files_request(self) -> "SearchFilesRequest":
        return SearchFilesRequest()


@dataclass(eq=True, frozen=True)
class SearchSpecLastModified(SearchSpecBase):
    from datetime import datetime

    """Defines a spec to search for objects that were last modified between certain times.

    Attributes:
        before (Optional[:py:class:`~datetime.datetime`]): Only return objects that were last modified before this time.
        after (Optional[:py:class:`~datetime.datetime`]): Only return objects that were last modified after this time.
    """

    before: Optional[datetime] = None
    after: Optional[datetime] = None

    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        return SearchSeismicStoresRequest(last_modified=self.to_last_modified_filter())

    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        return SearchSeismicsRequest(last_modified=self.to_last_modified_filter())

    def _to_search_files_request(self) -> "SearchFilesRequest":
        return SearchFilesRequest(last_modified=self.to_last_modified_filter())

    def to_last_modified_filter(self) -> Optional["LastModifiedFilter"]:
        if self.before is None and self.after is None:
            return None
        before, after = None, None
        if self.before is not None:
            before = Timestamp()
            before.FromDatetime(self.before)
        if self.after is not None:
            after = Timestamp()
            after.FromDatetime(self.after)
        return LastModifiedFilter(before=before, after=after)


class SearchSpecSurvey(SearchSpecBase, SearchSpecUnion):
    """Defines a spec to search for objects by survey identifiers. Only one such identifier be specified."""

    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        """Convert this search spec into a SearchSeismicStoreRequest."""
        return SearchSeismicStoresRequest(survey=self._to_search_spec())

    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        return SearchSeismicsRequest(survey=self._to_search_spec())

    def _to_search_files_request(self) -> "SearchFilesRequest":
        return SearchFilesRequest(survey=self._to_search_spec())


class SearchSpecSeismicStore(SearchSpecBase, SearchSpecUnion):
    """Defines a spec to search for seismics, files, and seismic stores by seismic store identifiers.
    Only one such identifier should be specified."""

    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        """Convert this search spec into a SearchSeismicStoreRequest."""
        return SearchSeismicStoresRequest(seismic_store=self._to_search_spec())

    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        """Convert this search spec into a SearchSeismicsRequest."""
        return SearchSeismicsRequest(seismic_store=self._to_search_spec())

    def _to_search_files_request(self) -> "SearchFilesRequest":
        """Convert this search spec into a SearchFilesRequest."""
        return SearchFilesRequest(seismic_store=self._to_search_spec())


class SearchSpecFile(SearchSpecBase, SearchSpecUnion):
    """Defines a spec to search for seismic stores by file identifiers.
    Only one such identifier should be specified."""

    uuid: Optional[str] = None

    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        """Convert this search spec into a SearchSeismicStoreRequest."""
        return SearchSeismicStoresRequest(file=self._to_search_spec())

    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        raise TypeError("Cannot search for seismics by file")

    def _to_search_files_request(self) -> "SearchFilesRequest":
        return SearchFilesRequest(spec=self._to_search_spec())


class SearchSpecPartition(SearchSpecBase, SearchSpecUnion):
    """Defines a spec to search for seismics by partition.
    Only one such identifier should be specified."""

    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        raise TypeError("Cannot search for seismic stores by partition")

    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        """Converts search spec into SearchSeismicsRequest"""
        return SearchSeismicsRequest(partition=self._to_search_spec())

    def _to_search_files_request(self) -> "SearchFilesRequest":
        raise TypeError("Cannot search for files by partition")


class SearchSpecSeismic(SearchSpecBase, SearchSpecUnion):
    """Defines a spec to search for seismics by seismic identifiers.
    Only one such identifier should be specified."""

    def _to_search_seismicstores_request(self) -> "SearchSeismicStoresRequest":
        raise TypeError("Cannot search for seismic stores by seismic")

    def _to_search_seismics_request(self) -> "SearchSeismicsRequest":
        """Converts search spec into SearchSeismicsRequest"""
        return SearchSeismicsRequest(seismic=self._to_search_spec())

    def _to_search_files_request(self) -> "SearchFilesRequest":
        raise TypeError("Cannot search for files by seismic")
