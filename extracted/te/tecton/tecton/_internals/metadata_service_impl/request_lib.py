import urllib.parse
from typing import Dict

from tecton import version
from tecton_core import conf
from tecton_core import errors
from tecton_core.id_helper import IdHelper
from tecton_core.metadata_service_impl.providers import RequestProvider
from tecton_core.metadata_service_impl.trace import get_trace_id


class InternalRequestProvider(RequestProvider):
    def request_headers(self) -> Dict[str, str]:
        """
        :return: Dictionary of request metadata.
        """
        metadata = {}

        metadata["x-request-id"] = IdHelper.generate_string_id()
        trace_id = get_trace_id()
        if trace_id:
            metadata["x-trace-id"] = trace_id

        metadata["x-tecton-client-version"] = version.get_semantic_version()

        workspace = conf.get_or_none("TECTON_WORKSPACE")
        if workspace:
            metadata["x-workspace"] = workspace
            # Warning: This is a hack to make it possible to integration test both EMR and Databricks
            # in a single deployment.
            if workspace.endswith("__emr"):
                metadata["x-tecton-force-emr"] = "true"

        authorization = self.auth_provider.get_auth_header()
        if authorization:
            metadata["authorization"] = authorization

        parsed_url = urllib.parse.urlparse(self.request_url())
        metadata["host"] = parsed_url.netloc

        return metadata

    def request_url(self) -> str:
        """
        :return: A Validated API service URL.
        """
        api_service = conf.get_or_none("API_SERVICE")
        if not api_service:
            msg = "API_SERVICE not set. Please configure API_SERVICE or use tecton.login(tecton_url=<url>)"
            raise errors.TectonAPIValidationError(msg)
        conf.validate_api_service_url(api_service)
        return urllib.parse.urljoin(api_service + "/", "proxy")
