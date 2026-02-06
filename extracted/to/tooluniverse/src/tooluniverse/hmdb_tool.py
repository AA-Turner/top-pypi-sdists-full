"""
HMDB (Human Metabolome Database) tool for ToolUniverse.

HMDB is the most comprehensive database of human metabolites containing
chemical, clinical, and molecular biology data.

Website: https://hmdb.ca/

Note: HMDB does not provide an open API. This tool uses PubChem as a cross-reference
source for metabolite data, with HMDB IDs for reference.
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List
from .base_tool import BaseTool
from .tool_registry import register_tool

# HMDB base URL
HMDB_BASE_URL = "https://hmdb.ca"
# PubChem API for cross-referencing
PUBCHEM_API_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"


@register_tool("HMDBTool")
class HMDBTool(BaseTool):
    """
    Tool for querying HMDB (Human Metabolome Database).

    HMDB provides:
    - Metabolite identification
    - Chemical properties
    - Biological functions
    - Disease associations
    - Spectral data (MS, NMR)

    Uses PubChem for data retrieval with HMDB cross-references.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout: int = tool_config.get("timeout", 30)
        self.parameter = tool_config.get("parameter", {})

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute HMDB query based on operation type."""
        operation = arguments.get("operation", "")

        if operation == "get_metabolite":
            return self._get_metabolite(arguments)
        elif operation == "search":
            return self._search(arguments)
        elif operation == "get_diseases":
            return self._get_diseases(arguments)
        else:
            return {
                "status": "error",
                "error": f"Unknown operation: {operation}. Supported: get_metabolite, search, get_diseases",
            }

    def _get_metabolite(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get metabolite by HMDB ID.

        Uses PubChem to retrieve metabolite data via HMDB ID cross-reference.

        Args:
            arguments: Dict containing:
                - hmdb_id: HMDB ID (e.g., HMDB0000001)
        """
        hmdb_id = arguments.get("hmdb_id", "")
        if not hmdb_id:
            return {"status": "error", "error": "Missing required parameter: hmdb_id"}

        # Normalize HMDB ID format
        if not hmdb_id.startswith("HMDB"):
            hmdb_id = f"HMDB{hmdb_id.zfill(7)}"

        try:
            # Use PubChem to find compound by HMDB ID
            response = requests.get(
                f"{PUBCHEM_API_URL}/compound/xref/RegistryID/{hmdb_id}/JSON",
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/HMDB"},
            )

            if response.status_code == 200:
                data = response.json()
                compounds = data.get("PC_Compounds", [])
                if compounds:
                    cid = compounds[0].get("id", {}).get("id", {}).get("cid")
                    # Get full compound properties
                    props_response = requests.get(
                        f"{PUBCHEM_API_URL}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,InChIKey,IUPACName/JSON",
                        timeout=self.timeout,
                    )
                    if props_response.status_code == 200:
                        props = (
                            props_response.json()
                            .get("PropertyTable", {})
                            .get("Properties", [{}])[0]
                        )
                        return {
                            "status": "success",
                            "data": {
                                "hmdb_id": hmdb_id,
                                "pubchem_cid": cid,
                                "name": props.get("IUPACName"),
                                "chemical_formula": props.get("MolecularFormula"),
                                "molecular_weight": props.get("MolecularWeight"),
                                "smiles": props.get("CanonicalSMILES"),
                                "inchikey": props.get("InChIKey"),
                            },
                            "metadata": {
                                "source": "PubChem (HMDB cross-reference)",
                                "hmdb_id": hmdb_id,
                                "hmdb_url": f"{HMDB_BASE_URL}/metabolites/{hmdb_id}",
                                "pubchem_url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
                            },
                        }

            # Return HMDB reference if PubChem doesn't have it
            return {
                "status": "success",
                "data": {
                    "hmdb_id": hmdb_id,
                    "note": "Metabolite data available at HMDB website",
                },
                "metadata": {
                    "source": "HMDB",
                    "hmdb_url": f"{HMDB_BASE_URL}/metabolites/{hmdb_id}",
                    "note": "HMDB does not provide open API access. Visit hmdb_url for full data.",
                },
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _search(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for metabolites by name using PubChem.

        Args:
            arguments: Dict containing:
                - query: Search query (metabolite name)
                - search_type: Type of search (name, formula, mass)
        """
        query = arguments.get("query", "")
        if not query:
            return {"status": "error", "error": "Missing required parameter: query"}

        search_type = arguments.get("search_type", "name")

        try:
            # Use PubChem to search for compounds
            response = requests.get(
                f"{PUBCHEM_API_URL}/compound/name/{query}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,IUPACName/JSON",
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/HMDB"},
            )

            results = []
            if response.status_code == 200:
                data = response.json()
                props_list = data.get("PropertyTable", {}).get("Properties", [])
                for props in props_list[:10]:
                    results.append(
                        {
                            "cid": props.get("CID"),
                            "name": props.get("IUPACName"),
                            "formula": props.get("MolecularFormula"),
                            "mw": props.get("MolecularWeight"),
                            "smiles": props.get("CanonicalSMILES"),
                        }
                    )

            import urllib.parse

            encoded_query = urllib.parse.quote(query)

            return {
                "status": "success",
                "data": {
                    "query": query,
                    "search_type": search_type,
                    "results": results,
                    "count": len(results),
                    "hmdb_search_url": f"{HMDB_BASE_URL}/unearth/q?query={encoded_query}&searcher=metabolites",
                    "pubchem_search_url": f"https://pubchem.ncbi.nlm.nih.gov/#query={encoded_query}",
                },
                "metadata": {
                    "source": "PubChem",
                    "note": "Use hmdb_search_url for HMDB-specific metabolite search",
                },
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_diseases(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get disease associations for a metabolite.

        Note: Disease associations are best accessed directly from HMDB website.

        Args:
            arguments: Dict containing:
                - hmdb_id: HMDB ID
        """
        hmdb_id = arguments.get("hmdb_id", "")
        if not hmdb_id:
            return {"status": "error", "error": "Missing required parameter: hmdb_id"}

        if not hmdb_id.startswith("HMDB"):
            hmdb_id = f"HMDB{hmdb_id.zfill(7)}"

        try:
            # Get basic compound info from PubChem
            response = requests.get(
                f"{PUBCHEM_API_URL}/compound/xref/RegistryID/{hmdb_id}/property/IUPACName/JSON",
                timeout=self.timeout,
                headers={"User-Agent": "ToolUniverse/HMDB"},
            )

            name = None
            if response.status_code == 200:
                props = response.json().get("PropertyTable", {}).get("Properties", [{}])
                if props:
                    name = props[0].get("IUPACName")

            return {
                "status": "success",
                "data": {
                    "hmdb_id": hmdb_id,
                    "metabolite_name": name,
                    "note": "Disease associations are available at HMDB website",
                    "hmdb_url": f"{HMDB_BASE_URL}/metabolites/{hmdb_id}",
                },
                "metadata": {
                    "source": "HMDB",
                    "hmdb_id": hmdb_id,
                    "note": "HMDB does not provide open API. Visit hmdb_url for disease associations.",
                },
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _parse_xml(self, xml_text: str) -> Dict[str, Any]:
        """Parse HMDB XML response."""
        try:
            root = ET.fromstring(xml_text)
            ns = {"hmdb": "http://www.hmdb.ca"}

            def get_text(elem, path):
                el = root.find(path, ns)
                return el.text if el is not None else None

            return {
                "hmdb_id": get_text(root, ".//hmdb:accession")
                or get_text(root, ".//accession"),
                "name": get_text(root, ".//hmdb:name") or get_text(root, ".//name"),
                "description": get_text(root, ".//hmdb:description")
                or get_text(root, ".//description"),
                "chemical_formula": get_text(root, ".//hmdb:chemical_formula")
                or get_text(root, ".//chemical_formula"),
                "smiles": get_text(root, ".//hmdb:smiles")
                or get_text(root, ".//smiles"),
            }
        except Exception:
            return {"raw_xml": xml_text[:500]}
