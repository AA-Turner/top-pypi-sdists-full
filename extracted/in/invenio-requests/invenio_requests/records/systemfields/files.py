# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""Files field allow for explicit setting after initialization."""

from invenio_records_resources.records.systemfields.files.field import FilesField


class RequestFilesField(FilesField):
    """Request Files system field."""

    def __init__(self, *args, **kwargs):
        """Initialize the RequestFilesField."""
        super().__init__(*args, **kwargs)

    #
    # Data descriptor methods (i.e. attribute access)
    #
    def __set__(self, record, value):
        """Set the request's files field."""
        assert record is not None

        self.set_dictkey(record, value)
