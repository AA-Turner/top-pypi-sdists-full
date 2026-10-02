"""Mermaid diagram service implementation."""

from typing import Union
import requests

from ..models.mermaid import (
    MermaidDiagramRequest,
    MermaidDiagramResponse,
    ContentType,
    ResponseType,
)
from ..utils import ApiRequestHandler, TokenSource


class MermaidService:
    """Service for generating mermaid diagrams."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the mermaid service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def generate_diagram(
        self,
        code: str,
        content_type: ContentType = "svg",
        response_type: ResponseType = "file",
    ) -> Union[MermaidDiagramResponse, bytes]:
        """Generate a mermaid diagram from mermaid code.

        Args:
            code: Mermaid diagram code (including theme directives if needed)
            content_type: Output format - "svg" or "png" (default: "svg")
            response_type: Response format - "file" (returns URL) or "raw" (returns binary data) (default: "file")

        Returns:
            MermaidDiagramResponse with file_url if response_type="file",
            or bytes with raw diagram data if response_type="raw"

        Raises:
            ApiError: If diagram generation fails or invalid mermaid code
        """
        request = MermaidDiagramRequest(code=code)

        # Build endpoint with query parameters
        endpoint = f"/v1/files/diagram/mermaid?content_type={content_type}&response_type={response_type}"

        if response_type == "file":
            return self._api.post(
                endpoint,
                response_model=MermaidDiagramResponse,
                json_data=request.model_dump(),
                wrap_response=False,
            )
        else:
            # For raw mode, return binary content
            response = self._api.post(
                endpoint,
                response_model=requests.Response,
                json_data=request.model_dump(),
            )
            return response.content
