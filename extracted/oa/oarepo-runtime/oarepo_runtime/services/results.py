#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Service results."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from invenio_access.permissions import Identity
from invenio_records_resources.errors import _iter_errors_dict
from invenio_records_resources.services.records.results import (
    RecordItem as BaseRecordItem,
)
from invenio_records_resources.services.records.results import (
    RecordList as BaseRecordList,
)

if TYPE_CHECKING:
    from invenio_access.permissions import Identity
    from invenio_drafts_resources.records.api import Draft
    from invenio_records_resources.records.api import Record


log = logging.getLogger(__name__)


class ResultComponent:
    """Base class for result components that can modify the serialized record data."""

    def __init__(
        self,
        record_item: BaseRecordItem | None = None,
        record_list: BaseRecordList | None = None,
    ):
        """Initialize the result component."""
        self._record_item = record_item
        self._record_list = record_list

    def update_data(self, identity: Identity, record: Record, projection: dict, expand: bool) -> None:
        """Update the projection data with additional information.

        :param identity: The identity of the user making the request.
        :param record: The record being processed.
        :param projection: The current projection of the record.
        :param expand: Whether to expand the record data.
        """
        raise NotImplementedError  # pragma: no cover


class RecordItem(BaseRecordItem):
    """Single record result."""

    components: tuple[type[ResultComponent], ...] | property = ()
    """A list of components that can modify the serialized record data."""

    @property
    def data(self) -> Any:
        """Property to get the record."""
        if self._data:
            return self._data
        _data = super().data
        for c in self.components:
            c(record_item=self).update_data(
                identity=self._identity,
                record=self._record,
                projection=_data,
                expand=self._expand,
            )
        return _data

    @property
    def errors(self) -> list[dict]:
        """Get the processed errors."""
        return self.postprocess_errors(self._errors or [])

    def to_dict(self) -> Any:
        """Get a dictionary for the record."""
        res = self.data
        if self._errors:
            res["errors"] = self.errors
        return res

    def postprocess_error_messages(self, field_path: str, messages: Any) -> Any:
        """Postprocess error messages, looking for those that were not correctly processed by marshmallow/invenio."""
        if not isinstance(messages, list):
            yield {"field": field_path, "messages": messages}
        else:
            str_messages = [msg for msg in messages if isinstance(msg, str)]
            non_str_messages = [msg for msg in messages if not isinstance(msg, str)]

            if str_messages:
                yield {"field": field_path, "messages": str_messages}
            else:
                for non_str_msg in non_str_messages:
                    yield from _iter_errors_dict(non_str_msg, field_path)

    def postprocess_errors(self, errors: list[dict]) -> list[dict]:
        """Postprocess errors."""
        converted_errors = []
        for error in errors:
            if error.get("messages"):
                converted_errors.extend(self.postprocess_error_messages(error["field"], error["messages"]))
            else:
                converted_errors.append(error)
        return converted_errors


class RecordList(BaseRecordList):
    """List of records result."""

    components: tuple[type[ResultComponent], ...] | property = ()

    @property
    def aggregations(self) -> Any:
        """Get the search result aggregations."""
        try:
            result = super().aggregations
            if result is None:
                return result  # pragma: no cover
            for key in result:
                if "buckets" in result[key]:
                    for bucket in result[key]["buckets"]:
                        val = bucket["key"]
                        label = bucket.get("label", "")

                        if not isinstance(val, str):
                            bucket["key"] = str(val)
                        if not isinstance(label, str):
                            bucket["label"] = str(label)
        except AttributeError:  # pragma: no cover
            return None  # pragma: no cover
        return result

    @property
    def hits(self) -> Any:
        """Iterator over the hits."""
        for hit in self._results:
            # Load dump
            hit_dict = hit.to_dict()

            try:
                # Project the record
                # TODO: check if this logic is correct
                versions = hit_dict.get("versions", {})
                if (versions.get("is_latest_draft") and not versions.get("is_latest")) or (
                    "publication_status" in hit_dict and hit_dict["publication_status"] == "draft"
                ):
                    draft_class: type[Draft] | None = getattr(self._service, "draft_cls", None)
                    if draft_class is None:
                        raise RuntimeError("Draft class is not defined in the service")  # pragma: no cover
                    record = draft_class.loads(hit_dict)
                else:
                    record = self._service.record_cls.loads(hit_dict)

                projection = self._schema.dump(
                    record,
                    context={
                        "identity": self._identity,
                        "record": record,
                    },
                )
                links_search_item = getattr(self._service.config, "links_search_item", None)
                links_search_item_tpl = getattr(self._service.config, "search_item_links_template", None)
                if links_search_item and links_search_item_tpl:
                    links_tpl = links_search_item_tpl(links_search_item)
                else:
                    links_tpl = self._links_item_tpl

                if links_tpl:
                    projection["links"] = links_tpl.expand(self._identity, record)

                # TODO: optimization viz FieldsResolver
                for c in self.components:
                    c(record_list=self).update_data(
                        identity=self._identity,
                        record=record,
                        projection=projection,
                        expand=self._expand,
                    )
                yield projection
            except Exception:  # pragma: no cover
                # ignore record with error, put it to log so that it gets to glitchtip
                # but don't break the whole search
                log.exception("Error while dumping record %s", hit_dict)
