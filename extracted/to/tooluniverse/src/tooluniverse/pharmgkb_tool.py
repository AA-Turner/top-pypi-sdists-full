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
            return {"error": f"Unknown operation: {operation}"}

    def _search_entity(
        self, entity_type: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Search for drugs, genes, or variants."""
        query = arguments.get("query", "")
        if not query:
            return {"error": "query parameter is required"}

        params = {"name": query, "view": "base"}

        try:
            # PharmGKB uses specific endpoints for filtered searches
            params = {"view": "base"}
            if entity_type == "Gene":
                params["symbol"] = query
            else:
                params["name"] = query

            response = requests.get(
                f"{PHARMGKB_BASE_URL}/data/{entity_type.lower()}",
                params=params,
                timeout=self.timeout,
            )
            if response.status_code == 404:
                # Try generic search if name search fails
                response = requests.get(
                    f"{PHARMGKB_BASE_URL}/data/search",
                    params={"query": query, "view": "base"},
                    timeout=self.timeout,
                )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"PharmGKB API request failed: {str(e)}"}

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
            return {"error": f"{entity_type.lower()}_id parameter is required"}

        try:
            response = requests.get(
                f"{PHARMGKB_BASE_URL}/data/{entity_type.lower()}/{entity_id}",
                params={"view": "base"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"PharmGKB API request failed: {str(e)}"}

    def _get_clinical_annotations(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get clinical annotations. Best retrieved by specific ID or filtered."""
        annotation_id = arguments.get("annotation_id")
        if annotation_id:
            try:
                response = requests.get(
                    f"{PHARMGKB_BASE_URL}/data/clinicalAnnotation/{annotation_id}",
                    params={"view": "base"},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                return {"error": f"PharmGKB API request failed: {str(e)}"}

        # If no ID, try to filter by gene or drug if possible via search or direct list

        try:
            # Fallback to search-like behavior if possible, but the API is restrictive
            # For now, return a helpful message if no filter works
            gene_id = arguments.get("gene_id")
            if gene_id:
                # Try to find annotations associated with this gene
                response = requests.get(
                    f"{PHARMGKB_BASE_URL}/data/clinicalAnnotation",
                    params={
                        "relatedGenes.id": gene_id,
                        "view": "base",
                    },  # Try one more time with different param
                    timeout=self.timeout,
                )
                if response.status_code == 200:
                    return response.json()

            return {
                "message": "Please provide a specific clinical 'annotation_id'. You can find these IDs by searching for drugs or genes first."
            }
        except Exception as e:
            return {"error": f"PharmGKB annotation retrieval failed: {str(e)}"}

    def _get_dosing_guidelines(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get CPIC/DPWG dosing guidelines."""
        guideline_id = arguments.get("guideline_id")
        if guideline_id:
            try:
                response = requests.get(
                    f"{PHARMGKB_BASE_URL}/data/guideline/{guideline_id}",
                    params={"view": "base"},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                return {"error": f"PharmGKB API request failed: {str(e)}"}

        # Fallback to listing by gene if provided
        gene_symbol = arguments.get("gene") or arguments.get("gene_id")
        if gene_symbol:
            try:
                # Some guidelines are indexed by related genes
                response = requests.get(
                    f"{PHARMGKB_BASE_URL}/data/guideline",
                    params={"relatedGenes.symbol": gene_symbol, "view": "base"},
                    timeout=self.timeout,
                )
                if response.status_code == 200:
                    return response.json()
            except Exception:
                pass

        return {
            "message": "Please provide a specific 'guideline_id'. Search for the gene first to find associated guidelines."
        }
