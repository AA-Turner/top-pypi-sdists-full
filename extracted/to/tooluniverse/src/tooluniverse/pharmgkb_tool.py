"""
PharmGKB API tool for ToolUniverse.

PharmGKB is a comprehensive resource that curates knowledge about the impact
of genetic variation on drug response for clinicians and researchers.

API Documentation: https://api.pharmgkb.org/v1/
"""

import requests
from typing import Dict, Any, List
from .base_tool import BaseTool
from .tool_registry import register_tool
from .http_utils import request_with_retry

# Base URL for PharmGKB/ClinPGx REST API
PHARMGKB_BASE_URL = "https://api.clinpgx.org/v1"


@register_tool("PharmGKBTool")
class PharmGKBTool(BaseTool):
    """
    Tool for querying PharmGKB REST API.

    PharmGKB provides pharmacogenomics data:
    - Drug-gene-variant clinical annotations
    - CPIC dosing guidelines
    - Drug and gene details
    - Pharmacogenetic pathways

    No authentication required for most endpoints.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        self.operation = tool_config.get("fields", {}).get("operation", "search_drugs")
        self.session = requests.Session()

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the PharmGKB API call."""
        operation = self.operation

        if operation == "search_drugs":
            return self._search_entity("Chemical", arguments)
        elif operation == "drug_details":
            return self._get_entity_details("Chemical", arguments)
        elif operation == "search_genes":
            return self._search_entity("Gene", arguments)
        elif operation == "gene_details":
            return self._get_entity_details("Gene", arguments)
        elif operation == "clinical_annotations":
            return self._get_clinical_annotations(arguments)
        elif operation == "search_variants":
            return self._search_entity("Variant", arguments)
        elif operation == "dosing_guidelines":
            return self._get_dosing_guidelines(arguments)
        else:
            return self._error(f"Unknown operation: {operation}")

    def _error(self, message: str) -> Dict[str, Any]:
        return {"status": "error", "error": message, "data": {"error": message}}

    def _request_json(
        self, url: str, params: Dict[str, Any]
    ) -> tuple[int, Dict[str, Any], str]:
        try:
            response = request_with_retry(
                self.session,
                "GET",
                url,
                params=params,
                timeout=self.timeout,
                max_attempts=4,
                backoff_seconds=0.75,
            )
        except requests.RequestException as e:
            return 0, {}, f"PharmGKB API request failed: {str(e)}"

        try:
            payload = response.json()
        except ValueError:
            payload = {}

        if response.status_code >= 400:
            detail = (
                payload.get("error")
                if isinstance(payload, dict)
                else response.text[:200]
            )
            return (
                response.status_code,
                payload,
                f"PharmGKB API error {response.status_code}: {detail}",
            )

        if not payload:
            return (
                response.status_code,
                payload,
                "PharmGKB API returned non-JSON or empty response",
            )

        return response.status_code, payload, ""

    def _search_entity(
        self, entity_type: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Search for drugs, genes, or variants."""
        query = arguments.get("query", "")
        if not query:
            return self._error("query parameter is required")

        params = {"name": query, "view": "base"}

        # PharmGKB uses specific endpoints for filtered searches
        params = {"view": "base"}
        if entity_type == "Gene":
            params["symbol"] = query
        else:
            params["name"] = query

        status_code, api_response, error = self._request_json(
            f"{PHARMGKB_BASE_URL}/data/{entity_type.lower()}",
            params,
        )
        if status_code == 404:
            status_code, api_response, error = self._request_json(
                f"{PHARMGKB_BASE_URL}/data/search",
                {"query": query, "view": "base"},
            )

        if error:
            return self._error(error)

        results = api_response.get("data", api_response)
        return {"status": "success", "data": results}

    def _get_entity_details(
        self, entity_type: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get details for a specific entity by PharmGKB ID."""
        # Handle both chemical_id and drug_id interchangeably
        if entity_type == "Chemical":
            entity_id = (
                arguments.get("chemical_id")
                or arguments.get("drug_id")
                or arguments.get("id")
            )
        else:
            entity_id = arguments.get(f"{entity_type.lower()}_id") or arguments.get(
                "id"
            )

        if not entity_id:
            return self._error(f"{entity_type.lower()}_id parameter is required")

        _, api_response, error = self._request_json(
            f"{PHARMGKB_BASE_URL}/data/{entity_type.lower()}/{entity_id}",
            {"view": "base"},
        )
        if error:
            return self._error(error)

        result = api_response.get("data", api_response)
        return {"status": "success", "data": result}

    def _get_clinical_annotations(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get clinical annotations. Best retrieved by specific ID or filtered."""
        annotation_id = arguments.get("annotation_id")
        if annotation_id:
            _, api_response, error = self._request_json(
                f"{PHARMGKB_BASE_URL}/data/clinicalAnnotation/{annotation_id}",
                {"view": "base"},
            )
            if error:
                return self._error(error)
            result = api_response.get("data", api_response)
            return {"status": "success", "data": result}

        # If no ID, try to filter by gene or drug if possible via search or direct list

        try:
            # Fallback to search-like behavior if possible, but the API is restrictive
            # For now, return a helpful message if no filter works
            gene_id = arguments.get("gene_id")
            if gene_id:
                # Try to find annotations associated with this gene
                status_code, api_response, error = self._request_json(
                    f"{PHARMGKB_BASE_URL}/data/clinicalAnnotation",
                    {
                        "relatedGenes.id": gene_id,
                        "view": "base",
                    },
                )
                if status_code == 200 and not error:
                    # PharmGKB API returns {"data": {...}, "status": "success"}
                    result = api_response.get("data", api_response)
                    return {"status": "success", "data": result}

            result = {
                "message": "Please provide a specific clinical 'annotation_id'. You can find these IDs by searching for drugs or genes first."
            }
            return {"status": "success", "data": result}
        except Exception as e:
            return self._error(f"PharmGKB annotation retrieval failed: {str(e)}")

    def _get_dosing_guidelines(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get CPIC/DPWG dosing guidelines."""
        guideline_id = arguments.get("guideline_id")
        if guideline_id:
            _, api_response, error = self._request_json(
                f"{PHARMGKB_BASE_URL}/data/guideline/{guideline_id}",
                {"view": "base"},
            )
            if error:
                return self._error(error)
            result = api_response.get("data", api_response)
            return {"status": "success", "data": result}

        # Fallback to listing by gene if provided
        gene_symbol = arguments.get("gene") or arguments.get("gene_id")
        if gene_symbol:
            try:
                # Some guidelines are indexed by related genes
                status_code, api_response, error = self._request_json(
                    f"{PHARMGKB_BASE_URL}/data/guideline",
                    {"relatedGenes.symbol": gene_symbol, "view": "base"},
                )
                if status_code == 200 and not error:
                    # PharmGKB API returns {"data": {...}, "status": "success"}
                    result = api_response.get("data", api_response)
                    return {"status": "success", "data": result}
            except Exception:
                pass

        result = {
            "message": "Please provide a specific 'guideline_id'. Search for the gene first to find associated guidelines."
        }
        return {"status": "success", "data": result}
