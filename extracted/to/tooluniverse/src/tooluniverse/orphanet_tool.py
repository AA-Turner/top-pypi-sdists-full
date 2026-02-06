"""
Orphanet API tool for ToolUniverse.

Orphanet is the reference portal for rare diseases and orphan drugs.
This tool uses the Orphadata API and RDcode API for programmatic access.

API Documentation:
- Orphadata: https://api.orphadata.com/
- RDcode: https://api.orphacode.org/
"""

import requests
import urllib.parse
from typing import Dict, Any, Optional, List
from .base_tool import BaseTool
from .tool_registry import register_tool

# Base URLs for Orphanet APIs
ORPHADATA_API_URL = "https://api.orphadata.com"
RDCODE_API_URL = "https://api.orphacode.org"

# RDcode API requires apiKey header (any value accepted)
RDCODE_API_KEY = "ToolUniverse"


def get_rdcode_headers():
    """Get headers for RDcode API requests."""
    return {
        "Accept": "application/json",
        "User-Agent": "ToolUniverse/Orphanet",
        "apiKey": RDCODE_API_KEY,
    }


def normalize_lang(lang: str) -> str:
    """Convert language code to uppercase as required by RDcode API."""
    return lang.upper() if lang else "EN"


@register_tool("OrphanetTool")
class OrphanetTool(BaseTool):
    """
    Tool for querying Orphanet rare disease database.

    Orphanet provides:
    - Rare disease nomenclature and classification
    - Disease-gene associations
    - Epidemiology data (prevalence, inheritance)
    - Expert centers and patient organizations

    RDcode API requires apiKey header (any value accepted).
    Orphadata API is free public access.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout: int = tool_config.get("timeout", 30)
        self.parameter = tool_config.get("parameter", {})

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Orphanet API call based on operation type."""
        operation = arguments.get("operation", "")

        if operation == "search_diseases":
            return self._search_diseases(arguments)
        elif operation == "get_disease":
            return self._get_disease(arguments)
        elif operation == "get_genes":
            return self._get_genes(arguments)
        elif operation == "get_classification":
            return self._get_classification(arguments)
        elif operation == "search_by_name":
            return self._search_by_name(arguments)
        else:
            return {
                "status": "error",
                "error": f"Unknown operation: {operation}. Supported: search_diseases, get_disease, get_genes, get_classification, search_by_name",
            }

    def _search_diseases(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search Orphanet for rare diseases by query term.

        Args:
            arguments: Dict containing:
                - query: Search query (disease name, keyword)
                - lang: Language code (en, fr, de, etc.). Default: en
        """
        query = arguments.get("query", "")
        if not query:
            return {"status": "error", "error": "Missing required parameter: query"}

        lang = normalize_lang(arguments.get("lang", "en"))

        try:
            # Use RDcode API for approximate name search
            # URL pattern: /{lang}/ClinicalEntity/ApproximateName/{label}
            encoded_query = urllib.parse.quote(query, safe="")
            response = requests.get(
                f"{RDCODE_API_URL}/{lang}/ClinicalEntity/ApproximateName/{encoded_query}",
                timeout=self.timeout,
                headers=get_rdcode_headers(),
            )
            response.raise_for_status()
            data = response.json()

            # Parse results from API response
            results = []
            if isinstance(data, list):
                results = data
            elif isinstance(data, dict):
                # API returns a dict with entities
                results = data.get("entities", data.get("results", [data]))

            return {
                "status": "success",
                "data": {
                    "results": results,
                    "query": query,
                    "language": lang,
                },
                "metadata": {
                    "source": "Orphanet RDcode API",
                    "query": query,
                },
            }

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {
                    "status": "success",
                    "data": {"results": [], "query": query, "language": lang},
                    "metadata": {"note": "No diseases found matching the query"},
                }
            return {"status": "error", "error": f"HTTP error: {e.response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_disease(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get disease details by ORPHA code.

        Args:
            arguments: Dict containing:
                - orpha_code: Orphanet disease code (e.g., 558, 166024)
                - lang: Language code (default: en)
        """
        orpha_code = arguments.get("orpha_code", "")
        if not orpha_code:
            return {
                "status": "error",
                "error": "Missing required parameter: orpha_code",
            }

        # Clean ORPHA code
        orpha_code = (
            str(orpha_code).replace("ORPHA:", "").replace("Orphanet:", "").strip()
        )
        lang = normalize_lang(arguments.get("lang", "en"))
        headers = get_rdcode_headers()

        result_data = {"ORPHAcode": orpha_code}

        try:
            # Get preferred name: /{lang}/ClinicalEntity/orphacode/{orphacode}/Name
            name_response = requests.get(
                f"{RDCODE_API_URL}/{lang}/ClinicalEntity/orphacode/{orpha_code}/Name",
                timeout=self.timeout,
                headers=headers,
            )
            name_response.raise_for_status()
            name_data = name_response.json()
            if isinstance(name_data, dict):
                result_data["Preferred term"] = name_data.get(
                    "Preferred term", name_data.get("Name", "")
                )
            else:
                result_data["Preferred term"] = str(name_data) if name_data else ""

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {
                    "status": "error",
                    "error": f"Disease not found: ORPHA:{orpha_code}",
                }
            return {"status": "error", "error": f"HTTP error: {e.response.status_code}"}

        try:
            # Get definition: /{lang}/ClinicalEntity/orphacode/{orphacode}/Definition
            def_response = requests.get(
                f"{RDCODE_API_URL}/{lang}/ClinicalEntity/orphacode/{orpha_code}/Definition",
                timeout=self.timeout,
                headers=headers,
            )
            if def_response.status_code == 200:
                def_data = def_response.json()
                if isinstance(def_data, dict):
                    result_data["Definition"] = def_data.get("Definition", "")
                else:
                    result_data["Definition"] = str(def_data) if def_data else ""
        except Exception:
            result_data["Definition"] = ""

        try:
            # Get synonyms: /{lang}/ClinicalEntity/orphacode/{orphacode}/Synonym
            syn_response = requests.get(
                f"{RDCODE_API_URL}/{lang}/ClinicalEntity/orphacode/{orpha_code}/Synonym",
                timeout=self.timeout,
                headers=headers,
            )
            if syn_response.status_code == 200:
                syn_data = syn_response.json()
                if isinstance(syn_data, list):
                    result_data["Synonyms"] = syn_data
                elif isinstance(syn_data, dict):
                    result_data["Synonyms"] = syn_data.get(
                        "Synonyms", syn_data.get("Synonym", [])
                    )
                else:
                    result_data["Synonyms"] = []
        except Exception:
            result_data["Synonyms"] = []

        return {
            "status": "success",
            "data": result_data,
            "metadata": {
                "source": "Orphanet RDcode API",
                "orpha_code": orpha_code,
            },
        }

    def _get_genes(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get genes associated with a rare disease.

        Args:
            arguments: Dict containing:
                - orpha_code: Orphanet disease code
        """
        orpha_code = arguments.get("orpha_code", "")
        if not orpha_code:
            return {
                "status": "error",
                "error": "Missing required parameter: orpha_code",
            }

        orpha_code = (
            str(orpha_code).replace("ORPHA:", "").replace("Orphanet:", "").strip()
        )

        try:
            # Use Orphadata API for gene associations (no auth required)
            response = requests.get(
                f"{ORPHADATA_API_URL}/rd-cross-referencing/orphacodes/{orpha_code}/genes",
                timeout=self.timeout,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "ToolUniverse/Orphanet",
                },
            )
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "data": {
                    "orpha_code": orpha_code,
                    "genes": data if isinstance(data, list) else data.get("genes", []),
                },
                "metadata": {
                    "source": "Orphanet Orphadata API",
                    "orpha_code": orpha_code,
                },
            }

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {
                    "status": "success",
                    "data": {"orpha_code": orpha_code, "genes": []},
                    "metadata": {"note": "No gene associations found"},
                }
            return {"status": "error", "error": f"HTTP error: {e.response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_classification(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get disease classification hierarchy.

        Args:
            arguments: Dict containing:
                - orpha_code: Orphanet disease code
                - lang: Language code (default: en)
        """
        orpha_code = arguments.get("orpha_code", "")
        if not orpha_code:
            return {
                "status": "error",
                "error": "Missing required parameter: orpha_code",
            }

        orpha_code = (
            str(orpha_code).replace("ORPHA:", "").replace("Orphanet:", "").strip()
        )
        lang = normalize_lang(arguments.get("lang", "en"))

        try:
            # Use RDcode API: /{lang}/ClinicalEntity/orphacode/{orphacode}/Classification
            response = requests.get(
                f"{RDCODE_API_URL}/{lang}/ClinicalEntity/orphacode/{orpha_code}/Classification",
                timeout=self.timeout,
                headers=get_rdcode_headers(),
            )
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "data": {
                    "orpha_code": orpha_code,
                    "classification": data,
                },
                "metadata": {
                    "source": "Orphanet RDcode API",
                    "orpha_code": orpha_code,
                },
            }

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {
                    "status": "success",
                    "data": {"orpha_code": orpha_code, "classification": []},
                    "metadata": {"note": "No classification found"},
                }
            return {"status": "error", "error": f"HTTP error: {e.response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _search_by_name(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for diseases by exact or partial name match.

        Args:
            arguments: Dict containing:
                - name: Disease name to search
                - exact: Whether to match exactly (default: False)
                - lang: Language code (default: en)
        """
        name = arguments.get("name", "")
        if not name:
            return {"status": "error", "error": "Missing required parameter: name"}

        exact = arguments.get("exact", False)
        lang = normalize_lang(arguments.get("lang", "en"))

        try:
            # URL encode the search name
            encoded_name = urllib.parse.quote(name, safe="")

            if exact:
                # For exact match, use FindbyName endpoint
                endpoint = (
                    f"{RDCODE_API_URL}/{lang}/ClinicalEntity/FindbyName/{encoded_name}"
                )
            else:
                # For partial match, use ApproximateName endpoint
                endpoint = f"{RDCODE_API_URL}/{lang}/ClinicalEntity/ApproximateName/{encoded_name}"

            response = requests.get(
                endpoint,
                timeout=self.timeout,
                headers=get_rdcode_headers(),
            )
            response.raise_for_status()
            data = response.json()

            # Parse results from response
            if isinstance(data, list):
                results = data
            elif isinstance(data, dict):
                # Single result or wrapped in dict
                results = data.get("entities", data.get("results", [data]))
            else:
                results = [data] if data else []

            return {
                "status": "success",
                "data": {
                    "results": results,
                    "count": len(results),
                    "search_name": name,
                    "exact_match": exact,
                },
                "metadata": {
                    "source": "Orphanet RDcode API",
                    "name": name,
                },
            }

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {
                    "status": "success",
                    "data": {
                        "results": [],
                        "count": 0,
                        "search_name": name,
                        "exact_match": exact,
                    },
                    "metadata": {"note": "No diseases found matching the name"},
                }
            return {"status": "error", "error": f"HTTP error: {e.response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}
