# proteomexchange_tool.py
"""
ProteomeXchange REST API tool for ToolUniverse.

ProteomeXchange (PX) is a consortium providing a single point of
submission for proteomics data, coordinating PRIDE, MassIVE,
PeptideAtlas, jPOST, and iProX. It provides standardized metadata
for proteomics datasets using controlled vocabulary (CV) terms.

API: https://proteomecentral.proteomexchange.org/cgi/GetDataset
No authentication required. Free for all use.
"""

import requests
from typing import Dict, Any
from .base_tool import BaseTool
from .tool_registry import register_tool

PX_BASE_URL = "https://proteomecentral.proteomexchange.org/cgi"


@register_tool("ProteomeXchangeTool")
class ProteomeXchangeTool(BaseTool):
    """
    Tool for querying ProteomeXchange, the proteomics data consortium.

    Provides access to metadata for proteomics datasets including
    species, instruments, publications, and data files from PRIDE,
    MassIVE, PeptideAtlas, jPOST, and iProX.

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        self.endpoint_type = tool_config.get("fields", {}).get(
            "endpoint_type", "get_dataset"
        )

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the ProteomeXchange API call."""
        try:
            return self._dispatch(arguments)
        except requests.exceptions.Timeout:
            return {
                "error": f"ProteomeXchange API request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Failed to connect to ProteomeXchange API. Check network connectivity."
            }
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"ProteomeXchange API HTTP error: {e.response.status_code}"
            }
        except Exception as e:
            return {"error": f"Unexpected error querying ProteomeXchange: {str(e)}"}

    def _dispatch(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate endpoint based on config."""
        if self.endpoint_type == "get_dataset":
            return self._get_dataset(arguments)
        elif self.endpoint_type == "search_datasets":
            return self._search_datasets(arguments)
        else:
            return {"error": f"Unknown endpoint_type: {self.endpoint_type}"}

    def _extract_cv_value(self, terms, accession_prefix=None, name_match=None):
        """Extract a value from CV terms list."""
        if not isinstance(terms, list):
            return None
        for term in terms:
            if not isinstance(term, dict):
                continue
            if accession_prefix and term.get("accession", "").startswith(
                accession_prefix
            ):
                return term.get("value", "")
            if name_match and name_match.lower() in term.get("name", "").lower():
                return term.get("value", "")
        return None

    def _get_dataset(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get a ProteomeXchange dataset by PX identifier."""
        px_id = arguments.get("px_id", "")
        if not px_id:
            return {"error": "px_id parameter is required (e.g., 'PXD000001')"}

        url = f"{PX_BASE_URL}/GetDataset"
        params = {"ID": px_id, "outputMode": "JSON"}
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        raw = response.json()

        # Extract title
        title_terms = raw.get("title", {}).get("terms", [])
        title = self._extract_cv_value(title_terms, name_match="dataset title") or ""

        # Extract species
        species_groups = raw.get("species", [])
        species_list = []
        for group in species_groups:
            if isinstance(group, dict):
                terms = group.get("terms", [])
                sp = self._extract_cv_value(terms, name_match="taxonomy")
                if sp:
                    species_list.append(sp)

        # Extract identifiers (PX ID + partners)
        identifiers = []
        for ident in raw.get("identifiers", []):
            if isinstance(ident, dict):
                val = ident.get("value", "")
                name = ident.get("name", "")
                if val:
                    identifiers.append({"name": name, "value": val})

        # Extract instruments
        instruments = []
        for inst_group in raw.get("instruments", []):
            if isinstance(inst_group, dict):
                terms = inst_group.get("terms", [])
                inst = self._extract_cv_value(terms, name_match="instrument model")
                if inst and inst != "null":
                    instruments.append(inst)

        # Extract publications
        publications = []
        for pub in raw.get("publications", []):
            if isinstance(pub, dict):
                terms = pub.get("terms", [])
                pmid = self._extract_cv_value(terms, name_match="PubMed identifier")
                doi = self._extract_cv_value(
                    terms, name_match="Dataset with its publication"
                )
                publications.append(
                    {
                        "pubmed_id": pmid,
                        "doi": doi,
                    }
                )

        # Extract file count
        data_files = raw.get("datasetFiles", [])

        result = {
            "px_id": px_id,
            "title": title,
            "species": species_list,
            "identifiers": identifiers,
            "instruments": instruments,
            "publications": publications,
            "file_count": len(data_files),
        }

        return {
            "data": result,
            "metadata": {
                "source": "ProteomeXchange",
                "query": px_id,
                "endpoint": "get_dataset",
            },
        }

    def _search_datasets(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search ProteomeXchange datasets via MassIVE PROXI."""
        query = arguments.get("query", "")
        limit = min(arguments.get("limit", 10), 50)

        # Use MassIVE PROXI API for search
        url = "https://massive.ucsd.edu/ProteoSAFe/proxi/v0.1/datasets"
        params = {"resultType": "compact"}
        if query:
            params["filter"] = query

        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        raw = response.json()

        datasets = []
        for ds in raw[:limit]:
            if not isinstance(ds, dict):
                continue

            # Extract accession
            accession_list = ds.get("accession", [])
            accession = ""
            if isinstance(accession_list, list):
                for acc in accession_list:
                    if isinstance(acc, dict):
                        accession = acc.get("value", "")
                        break

            # Extract title
            title = ds.get("title", "")

            # Extract species
            species_groups = ds.get("species", [])
            species_names = []
            for group in species_groups:
                if isinstance(group, list):
                    for term in group:
                        if isinstance(term, dict) and "common name" in term.get(
                            "name", ""
                        ):
                            val = term.get("value", "")
                            if val and val != "null":
                                species_names.append(val)

            datasets.append(
                {
                    "accession": accession,
                    "title": title,
                    "species": species_names,
                }
            )

        return {
            "data": datasets,
            "metadata": {
                "source": "ProteomeXchange/MassIVE",
                "total_returned": len(datasets),
                "query": query or "(all)",
                "endpoint": "search_datasets",
            },
        }
