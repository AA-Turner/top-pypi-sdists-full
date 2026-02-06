"""
ZINC tool for ToolUniverse.

ZINC is a free database of commercially available compounds for virtual
screening, containing over 750 million purchasable molecules.

Website: https://zinc.docking.org/
ZINC20: https://zinc20.docking.org/
CartBlanche22: https://cartblanche22.docking.org/
"""

import requests
from typing import Dict, Any, Optional, List
from .base_tool import BaseTool
from .tool_registry import register_tool

# ZINC base URLs
ZINC_BASE_URL = "https://zinc.docking.org"
ZINC20_BASE_URL = "https://zinc20.docking.org"
CARTBLANCHE_URL = "https://cartblanche22.docking.org"


@register_tool("ZINCTool")
class ZINCTool(BaseTool):
    """
    Tool for querying ZINC database of commercially available compounds.

    ZINC provides:
    - Purchasable compound database
    - Virtual screening libraries
    - Structure search
    - Vendor information

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout: int = tool_config.get("timeout", 30)
        self.parameter = tool_config.get("parameter", {})

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ZINC query based on operation type."""
        operation = arguments.get("operation", "")

        if operation == "get_substance":
            return self._get_substance(arguments)
        elif operation == "search_by_name":
            return self._search_by_name(arguments)
        elif operation == "search_by_smiles":
            return self._search_by_smiles(arguments)
        elif operation == "get_catalogs":
            return self._get_catalogs(arguments)
        else:
            return {
                "status": "error",
                "error": f"Unknown operation: {operation}. Supported: get_substance, search_by_name, search_by_smiles, get_catalogs",
            }

    def _get_substance(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get substance by ZINC ID.

        Args:
            arguments: Dict containing:
                - zinc_id: ZINC ID (e.g., ZINC000000000001)
        """
        zinc_id = arguments.get("zinc_id", "")
        if not zinc_id:
            return {"status": "error", "error": "Missing required parameter: zinc_id"}

        # Normalize ZINC ID format
        if not zinc_id.startswith("ZINC"):
            zinc_id = f"ZINC{zinc_id.zfill(15)}"

        try:
            # Try ZINC20 substances API
            response = requests.get(
                f"{ZINC20_BASE_URL}/substances/{zinc_id}.json",
                timeout=self.timeout,
                headers={
                    "User-Agent": "ToolUniverse/ZINC",
                    "Accept": "application/json",
                },
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": {
                        "zinc_id": data.get("zinc_id", zinc_id),
                        "smiles": data.get("smiles"),
                        "mwt": data.get("mwt"),
                        "logp": data.get("logp"),
                        "purchasability": data.get("purchasability"),
                        "catalogs": data.get("catalogs", []),
                    },
                    "metadata": {
                        "source": "ZINC20",
                        "zinc_id": zinc_id,
                        "url": f"{ZINC20_BASE_URL}/substances/{zinc_id}",
                    },
                }

            # Return reference URLs if not found via API
            return {
                "status": "success",
                "data": {
                    "zinc_id": zinc_id,
                    "note": "Substance lookup available via web interface",
                },
                "metadata": {
                    "source": "ZINC",
                    "zinc20_url": f"{ZINC20_BASE_URL}/substances/{zinc_id}",
                    "cartblanche_url": f"{CARTBLANCHE_URL}/substances.txt?zinc_ids={zinc_id}",
                    "note": "Use CartBlanche for ZINC22 substances (54B+ molecules)",
                },
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _search_by_name(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search ZINC by compound name.

        Args:
            arguments: Dict containing:
                - name: Compound name
                - max_results: Maximum results to return (default 20)
        """
        name = arguments.get("name", "")
        if not name:
            return {"status": "error", "error": "Missing required parameter: name"}

        max_results = arguments.get("max_results", 20)

        try:
            # Try ZINC20 search
            response = requests.get(
                f"{ZINC20_BASE_URL}/substances/search.json",
                params={"q": name, "count": max_results},
                timeout=self.timeout,
                headers={
                    "User-Agent": "ToolUniverse/ZINC",
                    "Accept": "application/json",
                },
            )

            results = []
            if response.status_code == 200 and "json" in response.headers.get(
                "Content-Type", ""
            ):
                data = response.json()
                results = data if isinstance(data, list) else data.get("substances", [])

            import urllib.parse

            encoded_name = urllib.parse.quote(name)

            return {
                "status": "success",
                "data": {
                    "query": name,
                    "results": results[:max_results],
                    "count": len(results),
                    "zinc20_search_url": f"{ZINC20_BASE_URL}/substances/search/?q={encoded_name}",
                    "zinc15_search_url": f"{ZINC_BASE_URL}/substances/search/?q={encoded_name}",
                },
                "metadata": {
                    "source": "ZINC",
                    "note": "ZINC20 contains 1.4B+ purchasable compounds",
                },
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _search_by_smiles(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search ZINC by SMILES structure.

        Args:
            arguments: Dict containing:
                - smiles: SMILES string
                - search_type: 'exact', 'substructure', 'similarity' (default: similarity)
                - max_results: Maximum results (default 20)
        """
        smiles = arguments.get("smiles", "")
        if not smiles:
            return {"status": "error", "error": "Missing required parameter: smiles"}

        search_type = arguments.get("search_type", "similarity")
        max_results = arguments.get("max_results", 20)

        try:
            endpoint_map = {
                "exact": "substances/search.json",
                "substructure": "substances/substructure.json",
                "similarity": "substances/similarity.json",
            }

            endpoint = endpoint_map.get(search_type, "substances/similarity.json")

            response = requests.get(
                f"{ZINC20_BASE_URL}/{endpoint}",
                params={"smiles": smiles, "count": max_results},
                timeout=self.timeout,
                headers={
                    "User-Agent": "ToolUniverse/ZINC",
                    "Accept": "application/json",
                },
            )

            if response.status_code == 200 and "json" in response.headers.get(
                "Content-Type", ""
            ):
                data = response.json()
                results = data if isinstance(data, list) else data.get("substances", [])
            else:
                results = []

            return {
                "status": "success",
                "data": {
                    "query_smiles": smiles,
                    "search_type": search_type,
                    "results": results[:max_results],
                    "count": len(results),
                },
                "metadata": {"source": "ZINC"},
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_catalogs(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get available ZINC catalogs/libraries.

        Returns list of available compound catalogs for virtual screening.
        """
        try:
            response = requests.get(
                f"{ZINC20_BASE_URL}/catalogs.json",
                timeout=self.timeout,
                headers={
                    "User-Agent": "ToolUniverse/ZINC",
                    "Accept": "application/json",
                },
            )

            if response.status_code == 200:
                data = response.json()
                catalogs = data if isinstance(data, list) else data.get("catalogs", [])
                return {
                    "status": "success",
                    "data": {
                        "catalogs": catalogs[:50],  # Limit to 50
                        "count": len(catalogs),
                    },
                    "metadata": {"source": "ZINC"},
                }

            # Return basic info if API not available
            return {
                "status": "success",
                "data": {
                    "catalogs": [
                        {
                            "name": "In-Stock",
                            "description": "Immediately purchasable compounds",
                        },
                        {
                            "name": "Make-on-demand",
                            "description": "Synthesizable compounds",
                        },
                        {
                            "name": "Drug-like",
                            "description": "Drug-like compounds (Lipinski)",
                        },
                        {"name": "Lead-like", "description": "Lead-like compounds"},
                        {"name": "Fragment-like", "description": "Fragment library"},
                    ],
                    "catalog_url": f"{ZINC20_BASE_URL}/catalogs",
                    "note": "Visit catalog_url for complete list",
                },
                "metadata": {"source": "ZINC"},
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}
