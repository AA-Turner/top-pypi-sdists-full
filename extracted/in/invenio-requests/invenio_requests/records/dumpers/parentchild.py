# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Search dumper for OpenSearch join relationships."""

from invenio_records.dumpers import SearchDumperExt


class ParentChildDumperExt(SearchDumperExt):
    """Search dumper extension for OpenSearch join relationships.

    This dumper sets the join relationship field for parent-child documents:
    - Parent events: {"name": "parent"}
    - Child events (replies): {"name": "child", "parent": parent_id}

    It also handles routing to ensure child documents are indexed on the
    same shard as their parent (required for join queries to work).
    """

    def dump(self, record, data):
        """Dump the join relationship data.

        Sets the parent_child field based on whether the record
        is a parent event or a child (reply).
        """
        if record.parent_id:
            # This is a child event (reply)
            data["parent_child"] = {"name": "child", "parent": str(record.parent_id)}
        else:
            # This is a parent event
            data["parent_child"] = {"name": "parent"}

    def load(self, data, record_cls):
        """Load the data.

        The join relationship is only used in the search index,
        not in the record data, so we remove it when loading.
        """
        data.pop("parent_child", None)
