"""
MetaCyc tool for ToolUniverse.

MetaCyc is a curated database of experimentally elucidated metabolic
pathways from all domains of life.

Website: https://metacyc.org/
BioCyc: https://biocyc.org/
"""

import requests
from typing import Dict, Any, Optional, List
from .base_tool import BaseTool
from .tool_registry import register_tool

# BioCyc API base URL (MetaCyc is part of BioCyc collection)
BIOCYC_BASE_URL = "https://biocyc.org"


@register_tool("MetaCycTool")
class MetaCycTool(BaseTool):
    """
    Tool for querying MetaCyc metabolic pathway database.

    MetaCyc provides:
    - Experimentally elucidated metabolic pathways
    - Enzymes and reactions
    - Metabolites and compounds
    - Pathway diagrams

    Uses BioCyc web services API.
    No authentication required for basic access.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout: int = tool_config.get("timeout", 30)
        self.parameter = tool_config.get("parameter", {})

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute MetaCyc query based on operation type."""
        operation = arguments.get("operation", "")
        # Auto-fill operation from tool config const if not provided by user
        if not operation:
            operation = self.get_schema_const_operation()

        if operation == "search_pathways":
            return self._search_pathways(arguments)
        elif operation == "get_pathway":
            return self._get_pathway(arguments)
        elif operation == "get_compound":
            return self._get_compound(arguments)
        elif operation == "get_reaction":
            return self._get_reaction(arguments)
        else:
            return {
                "status": "error",
                "error": f"Unknown operation: {operation}. Supported: search_pathways, get_pathway, get_compound, get_reaction",
            }

    def _search_pathways(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search MetaCyc for pathways.

        Args:
            arguments: Dict containing:
                - query: Search query (pathway name or keyword)
        """
        query = arguments.get("query", "")
        if not query:
            return {"status": "error", "error": "Missing required parameter: query"}

        try:
            # Use BioCyc quick search API
            response = requests.get(
                f"{BIOCYC_BASE_URL}/META/search-query",
                params={"type": "PATHWAY", "query": query},
                timeout=self.timeout,
                headers={
                    "User-Agent": "ToolUniverse/MetaCyc",
                    "Accept": "application/json",
                },
            )

            # If JSON response works
            if "json" in response.headers.get("Content-Type", ""):
                data = response.json()
                return {
                    "status": "success",
                    "data": {
                        "query": query,
                        "results": data
                        if isinstance(data, list)
                        else data.get("results", []),
                    },
                    "metadata": {"source": "MetaCyc"},
                }

            # Return search guidance with web URL
            return {
                "status": "success",
                "data": {
                    "query": query,
                    "results": [],
                    "search_url": f"{BIOCYC_BASE_URL}/META/substring-search?type=PATHWAY&object={query}",
                    "note": "Visit search_url for full results. Use get_pathway with pathway ID once found.",
                },
                "metadata": {"source": "MetaCyc"},
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_pathway(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get pathway details by MetaCyc pathway ID.

        Args:
            arguments: Dict containing:
                - pathway_id: MetaCyc pathway ID (e.g., PWY-5177)
        """
        pathway_id = arguments.get("pathway_id", "")
        if not pathway_id:
            return {
                "status": "error",
                "error": "Missing required parameter: pathway_id",
            }

        try:
            # Try to get pathway data via getxml API
            response = requests.get(
                f"{BIOCYC_BASE_URL}/getxml",
                params={"META": pathway_id},
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/MetaCyc"},
            )

            if response.status_code == 200:
                # Parse basic info from response
                return {
                    "status": "success",
                    "data": {
                        "pathway_id": pathway_id,
                        "has_data": True,
                        "url": f"{BIOCYC_BASE_URL}/META/NEW-IMAGE?type=PATHWAY&object={pathway_id}",
                        "diagram_url": f"{BIOCYC_BASE_URL}/META/NEW-IMAGE?type=PATHWAY&object={pathway_id}&detail-level=2",
                    },
                    "metadata": {
                        "source": "MetaCyc",
                        "pathway_id": pathway_id,
                    },
                }

            return {
                "status": "error",
                "error": f"Pathway not found: {pathway_id}",
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_compound(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get compound details from MetaCyc.

        Args:
            arguments: Dict containing:
                - compound_id: MetaCyc compound ID (e.g., CPD-1)
        """
        compound_id = arguments.get("compound_id", "")
        if not compound_id:
            return {
                "status": "error",
                "error": "Missing required parameter: compound_id",
            }

        try:
            response = requests.get(
                f"{BIOCYC_BASE_URL}/getxml",
                params={"META": compound_id},
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/MetaCyc"},
            )

            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": {
                        "compound_id": compound_id,
                        "has_data": True,
                        "url": f"{BIOCYC_BASE_URL}/compound?orgid=META&id={compound_id}",
                    },
                    "metadata": {
                        "source": "MetaCyc",
                        "compound_id": compound_id,
                    },
                }

            return {
                "status": "error",
                "error": f"Compound not found: {compound_id}",
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_reaction(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get reaction details from MetaCyc.

        Args:
            arguments: Dict containing:
                - reaction_id: MetaCyc reaction ID (e.g., RXN-14500)
        """
        reaction_id = arguments.get("reaction_id", "")
        if not reaction_id:
            return {
                "status": "error",
                "error": "Missing required parameter: reaction_id",
            }

        try:
            response = requests.get(
                f"{BIOCYC_BASE_URL}/getxml",
                params={"META": reaction_id},
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/MetaCyc"},
            )

            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": {
                        "reaction_id": reaction_id,
                        "has_data": True,
                        "url": f"{BIOCYC_BASE_URL}/META/NEW-IMAGE?type=REACTION&object={reaction_id}",
                    },
                    "metadata": {
                        "source": "MetaCyc",
                        "reaction_id": reaction_id,
                    },
                }

            return {
                "status": "error",
                "error": f"Reaction not found: {reaction_id}",
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}
