#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Extensions for RDM API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask_resources import RequestBodyParser
from flask_resources.responses import ResponseHandler
from invenio_records_resources.resources.records.headers import etag_headers

if TYPE_CHECKING:
    from collections.abc import Iterable

    from oarepo_runtime.api import Export, Import


def exports_to_response_handlers(
    exports: Iterable[Export],
) -> dict[str, ResponseHandler]:
    """Convert exports to a dictionary of mimetype -> response handlers."""
    return {
        export.mimetype: ResponseHandler(
            serializer=export.serializer,
            headers=etag_headers,
        )
        for export in exports
    }


def imports_to_request_body_parsers(
    imports: Iterable[Import],
) -> dict[str, RequestBodyParser]:
    """Convert imports to a dictionary of mimetype -> request body parsers."""
    return {import_option.mimetype: RequestBodyParser(import_option.deserializer) for import_option in imports}
