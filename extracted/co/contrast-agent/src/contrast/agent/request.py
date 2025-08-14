# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re
from typing import Any

import contrast_fireball
from contrast_vendor import webob

from contrast.api.user_input import InputType, DocumentType
from contrast.utils.string_utils import ensure_string, truncate
from contrast.utils.timer import now_ms
from contrast.agent.middlewares.route_coverage.common import (
    get_normalized_uri as strip_uri,
    get_url_parameters as find_parameters,
)

from contrast_vendor import structlog as logging
from contrast_vendor.webob.compat import cgi_FieldStorage
from contrast_vendor.webob.multidict import NestedMultiDict

logger = logging.getLogger("contrast")

Environ = dict[str, Any]


class Request(webob.BaseRequest):
    environ: Environ

    def __init__(self, environ: Environ):
        super().__init__(environ)

        self._document_type = None
        self._normalized_uri = None
        self._url_parameters = None
        self._multipart_headers = None

        # These fields are set by an ActivityMasker and will be used for reporting.
        self._masked = False
        self._masked_body: str | None = None
        self._masked_cookies = None
        self._masked_headers = None
        self._masked_params = None
        self._masked_query_string = None
        self._parsed_http = None

        self.timestamp_ms = now_ms()

    def to_fireball_assess_request(self) -> contrast_fireball.AssessRequest:
        return contrast_fireball.AssessRequest(
            body=truncate(self._reportable_body, length=4096),
            headers={
                k: ([v for v in (vs if isinstance(vs, list) else [vs])])
                for k, vs in self._reportable_headers.items()
            },
            method=ensure_string(self.method),
            parameters={
                k: ([v for v in (vs if isinstance(vs, list) else [vs])])
                for k, vs in self._reportable_params.items()
            },
            port=int(self.host_port),
            protocol=ensure_string(self.scheme),
            query_string=self._reportable_query_string,
            uri=ensure_string(self.path),
            standard_normalized_uri=ensure_string(self.get_normalized_uri()),
            version=self._get_http_version(),
        )

    @property
    def reportable_format(self):
        assert self._masked, "Request must be masked before reporting"

        r = self.to_fireball_assess_request()
        return {
            "body": r.body,
            # the WSGI environ supports only one value per request header. However
            # the server decides to handle multiple headers, we're guaranteed to
            # have only unique keys in request.request_headers (since we iterate
            # over webob's EnvironHeaders). Thus, each value list here is length-1.
            "headers": r.headers,
            "method": r.method,
            "parameters": r.parameters,
            "port": r.port,
            "protocol": r.protocol,
            "queryString": r.query_string,
            "uri": r.uri,
            "version": r.version,
        }

    @property
    def POST(self):
        """
        Return a MultiDict containing all the variables from a form
        request. Returns an empty dict-like object for non-form requests.

        Form requests are typically POST requests, however any other
        requests with an appropriate Content-Type are also supported.

        Swallows ValueErrors with "Invalid boundary in multipart form" message.
        """
        try:
            return super().POST
        except ValueError as e:
            if str(e).startswith("Invalid boundary in multipart form"):
                # This likely came form a malformed multipart/form-data request,
                # which is out of our control. Still log the error in case
                # there's another case we haven't considered.
                logger.debug("WARNING: failed to parse params", error=e)
                return {}
            raise

    @property
    def params(self):
        """
        Returns a NestedMultiDict of the query string and POST form parameters.

        Multipart form data is not included in this dict.
        """
        post_params = self.POST
        for key, values in post_params.items():
            if isinstance(values, cgi_FieldStorage):
                del post_params[key]
        return NestedMultiDict(self.GET, post_params)

    @property
    def _reportable_body(self):
        if self._masked_body is not None:
            return self._masked_body

        return ensure_string(self.body)

    @property
    def _reportable_cookies(self):
        if self._masked_cookies is not None:
            return self._masked_cookies

        return {ensure_string(k): ensure_string(v) for k, v in self.cookies.items()}

    @property
    def _reportable_headers(self):
        if self._masked_headers is not None:
            return self._masked_headers

        return {ensure_string(k): ensure_string(v) for k, v in self.headers.items()}

    @property
    def _reportable_params(self):
        if self._masked_params is not None:
            return self._masked_params

        return {ensure_string(k): ensure_string(v) for k, v in self.params.items()}

    @property
    def _reportable_query_string(self):
        if self._masked_query_string is not None:
            return self._masked_query_string

        return ensure_string(self.query_string)

    def get_multipart_headers(self):
        if self._multipart_headers is not None:
            return self._multipart_headers

        self._multipart_headers = {}
        for field_name, filename in self._get_file_info():
            self._multipart_headers[field_name] = filename
        return self._multipart_headers

    def get_normalized_uri(self) -> str:
        """
        A best-effort to remove client-specific information from the path.
        Example:
        /user/123456/page/12 -> /user/{n}/page/{n}
        """
        if self._normalized_uri is not None:
            return self._normalized_uri

        self._normalized_uri = strip_uri(self.path)
        return self._normalized_uri

    def get_url_parameters(self):
        """
        Returns the url parameters in a list.
        Example
        /user/123456/page/12 -> ["123456", "12"]
        """
        if self._url_parameters is not None:
            return self._url_parameters

        self._url_parameters = find_parameters(self.path)
        return self._url_parameters

    def get_body(self, as_text=False, errors="ignore"):
        """
        Get the raw request body in either bytes or as a decoded string.
        Note that we do not use webob's Request.text here, because we do not want this
        to fail in the event of a decoding error.

        :param as_text: Boolean indicating if we should attempt to return a decoded
            string
        :param errors: String indicating the unicode error handling strategy, passed to
            decode()
        :return: The request body as either bytes or a decoded string
        """
        if not as_text:
            return self.body

        return ensure_string(self.body, encoding=self.charset, errors=errors)

    def _get_http_version(self):
        """
        teamserver expects this field to be a string representing the HTTP version only.
        Using 'HTTP/1.1' is not acceptable and will cause vulnerabilities to be omitted
        from TS.
        """
        return self.http_version.split("/")[-1]

    def _get_document_type_from_header(self):
        """
        Returns the document type based on the content type header if present
        """
        content_type = self.content_type.lower()

        if not content_type:
            return None
        if "json" in content_type:
            return DocumentType.JSON
        if "xml" in content_type:
            return DocumentType.XML
        if "x-www-form-urlencoded" in content_type or "form-data" in content_type:
            return InputType.PARAMETER_VALUE

        return DocumentType.NORMAL

    def _get_document_type_from_body(self):
        str_body = self.get_body(as_text=True)

        if str_body.startswith("<?xml"):
            return DocumentType.XML
        if re.search(r"^\s*[{[]", str_body):
            return DocumentType.JSON

        return DocumentType.NORMAL

    def _get_document_type(self):
        if self._document_type is not None:
            return self._document_type

        self._document_type = self._get_document_type_from_header()
        if self._document_type is None:
            self._document_type = self._get_document_type_from_body()

        return self._document_type

    def _get_file_info(self):
        """
        Get the field names and filenames of uploaded files
        :return: list of tuples of (field_name, filename)
        """
        file_info = []
        for f in self.POST.values():
            if hasattr(f, "filename") and hasattr(f, "name"):
                file_info.append((f.name, f.filename))
                logger.debug("Found uploaded file: %s", f.filename)

        return file_info

    # from https://github.com/Contrast-Security-Inc/secobs-semantic-conventions/blob/main/docs/http/http-spans.md?plain=1#L121
    _OTEL_KNOWN_METHODS = {
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "CONNECT",
        "OPTIONS",
        "TRACE",
        "PATCH",
    }

    def get_otel_attributes(self) -> contrast_fireball.OtelAttributes:
        """
        Returns attributes following OpenTelemetry semantic conventions for HTTP spans.
        """
        attributes = {
            "url.path": self.path,
            "url.scheme": self.scheme,
        }

        # url.query is conditionally required if a query string is present
        if self.query_string:
            attributes["url.query"] = self._reportable_query_string

        # http.request.method_original is conditionally required if the method is not one of the known methods
        if self.method not in self._OTEL_KNOWN_METHODS:
            attributes["http.request.method"] = "_OTHER"
            attributes["http.request.method_original"] = self.method
        else:
            attributes["http.request.method"] = self.method

        return attributes
