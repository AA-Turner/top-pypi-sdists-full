"""
COSMIC (Catalogue of Somatic Mutations in Cancer) API tool for ToolUniverse.

COSMIC is a comprehensive database of somatic mutations in human cancer.
This tool uses the NLM Clinical Tables Search Service API for COSMIC data.

API Documentation: https://clinicaltables.nlm.nih.gov/apidoc/cosmic/v4/doc.html
"""

import requests
from typing import Dict, Any, Optional, List
from .base_tool import BaseTool
from .tool_registry import register_tool

# Base URL for COSMIC via NLM Clinical Tables API
COSMIC_API_URL = "https://clinicaltables.nlm.nih.gov/api/cosmic/v4/search"


@register_tool("COSMICTool")
class COSMICTool(BaseTool):
    """
    Tool for querying COSMIC (Catalogue of Somatic Mutations in Cancer).

    COSMIC provides:
    - Somatic mutation data in human cancers
    - Gene-level mutation information
    - Mutation coordinates and amino acid changes
    - Associated cancer types

    Uses NLM Clinical Tables API. No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout: int = tool_config.get("timeout", 30)
        self.parameter = tool_config.get("parameter", {})

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the COSMIC API call based on operation type."""
        operation = arguments.get("operation", "search")

        if operation == "search":
            return self._search_mutations(arguments)
        elif operation == "get_by_gene":
            return self._get_mutations_by_gene(arguments)
        else:
            return {
                "status": "error",
                "error": f"Unknown operation: {operation}. Supported: search, get_by_gene",
            }

    def _search_mutations(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search COSMIC for mutations by term.

        Args:
            arguments: Dict containing:
                - terms: Search query (gene name, mutation, etc.)
                - max_results: Maximum results to return (default 20, max 500)
                - genome_build: Genome build version (37 or 38, default 37)
        """
        terms = arguments.get("terms", "")
        if not terms:
            return {"status": "error", "error": "Missing required parameter: terms"}

        max_results = min(arguments.get("max_results", 20), 500)
        genome_build = arguments.get("genome_build", 37)

        # Display fields: MutationID, GeneName, MutationCDS, MutationAA
        # Extra fields for more details
        params = {
            "terms": terms,
            "maxList": max_results,
            "grchv": genome_build,
            "df": "MutationID,GeneName,MutationCDS,MutationAA",
            "ef": "MutationID,GeneName,MutationCDS,MutationAA,PrimarySite,PrimaryHistology,MutationGenomePosition,MutationStrand",
        }

        try:
            response = requests.get(
                COSMIC_API_URL,
                params=params,
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/COSMIC"},
            )
            response.raise_for_status()
            data = response.json()

            # NLM API returns [total_count, code_list, extra_data, display_strings]
            if isinstance(data, list) and len(data) >= 4:
                total_count = data[0]
                codes = data[1] if data[1] else []
                extra_data = data[2] if data[2] else {}
                display_strings = data[3] if data[3] else []

                # Parse results
                results = []
                for i, code in enumerate(codes):
                    result = {
                        "mutation_id": code,
                        "display": display_strings[i]
                        if i < len(display_strings)
                        else None,
                    }
                    # Add extra fields if available
                    if extra_data and code in extra_data:
                        result.update(extra_data[code])
                    results.append(result)

                return {
                    "status": "success",
                    "data": {
                        "total_count": total_count,
                        "results": results,
                        "genome_build": f"GRCh{genome_build}",
                    },
                    "metadata": {
                        "source": "COSMIC via NLM Clinical Tables API",
                        "query": terms,
                    },
                }
            else:
                return {
                    "status": "success",
                    "data": {"total_count": 0, "results": []},
                    "metadata": {"source": "COSMIC via NLM Clinical Tables API"},
                }

        except requests.exceptions.Timeout:
            return {"status": "error", "error": "Request timeout after 30 seconds"}
        except requests.exceptions.HTTPError as e:
            return {"status": "error", "error": f"HTTP error: {e.response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_mutations_by_gene(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get all mutations for a specific gene.

        Args:
            arguments: Dict containing:
                - gene: Gene symbol (e.g., BRAF, TP53)
                - max_results: Maximum results (default 100, max 500)
                - genome_build: Genome build version (37 or 38)
        """
        gene = arguments.get("gene", "")
        if not gene:
            return {"status": "error", "error": "Missing required parameter: gene"}

        max_results = min(arguments.get("max_results", 100), 500)
        genome_build = arguments.get("genome_build", 37)

        params = {
            "terms": gene,
            "maxList": max_results,
            "grchv": genome_build,
            "q": f"GeneName:{gene}",
            "df": "MutationID,GeneName,MutationCDS,MutationAA",
            "ef": "MutationID,GeneName,MutationCDS,MutationAA,PrimarySite,PrimaryHistology,MutationGenomePosition,MutationStrand,Fathmm",
        }

        try:
            response = requests.get(
                COSMIC_API_URL,
                params=params,
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/COSMIC"},
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and len(data) >= 4:
                total_count = data[0]
                codes = data[1] if data[1] else []
                extra_data = data[2] if data[2] else {}
                display_strings = data[3] if data[3] else []

                results = []
                for i, code in enumerate(codes):
                    result = {
                        "mutation_id": code,
                        "display": display_strings[i]
                        if i < len(display_strings)
                        else None,
                    }
                    if extra_data and code in extra_data:
                        result.update(extra_data[code])
                    results.append(result)

                return {
                    "status": "success",
                    "data": {
                        "gene": gene,
                        "total_count": total_count,
                        "results": results,
                        "genome_build": f"GRCh{genome_build}",
                    },
                    "metadata": {
                        "source": "COSMIC via NLM Clinical Tables API",
                        "gene": gene,
                    },
                }
            else:
                return {
                    "status": "success",
                    "data": {"gene": gene, "total_count": 0, "results": []},
                    "metadata": {"source": "COSMIC via NLM Clinical Tables API"},
                }

        except requests.exceptions.Timeout:
            return {"status": "error", "error": "Request timeout"}
        except requests.exceptions.HTTPError as e:
            return {"status": "error", "error": f"HTTP error: {e.response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}
