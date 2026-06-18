# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-License-Identifier: MIT

"""Search dumpers for the is_expired state of requests."""

from invenio_records.dumpers import SearchDumperExt


class CalculatedFieldDumperExt(SearchDumperExt):
    """Search dumper extension for calculated fields."""

    def __init__(self, field, prop=None):
        """Constructor.

        :param field: Field into which to dump the property value.
        :param prop: Property whose value to dump.
        """
        super().__init__()
        self.field = field
        self.property = prop or field

    def dump(self, record, data):
        """Dump the data."""
        data[self.field] = getattr(record, self.property)

    def load(self, data, record_cls):
        """Load the data."""
        data.pop(self.field, None)
