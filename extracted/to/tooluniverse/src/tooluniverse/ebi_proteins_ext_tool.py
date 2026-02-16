# ebi_proteins_ext_tool.py
"""
EBI Proteins API Extended tool for ToolUniverse.

Extended endpoints for the EBI Proteins API covering mutagenesis data
and post-translational modification (PTM) proteomics evidence.

API: https://www.ebi.ac.uk/proteins/api/
No authentication required. Free public access.
"""

import requests
from typing import Dict, Any
from .base_tool import BaseTool
from .tool_registry import register_tool

PROTEINS_API_BASE_URL = "https://www.ebi.ac.uk/proteins/api"


@register_tool("EBIProteinsExtTool")
class EBIProteinsExtTool(BaseTool):
    """
    Extended tool for EBI Proteins API covering mutagenesis and PTM data.

    These endpoints provide detailed mutagenesis experiment results and
    mass spectrometry-based post-translational modification evidence
    mapped to UniProt protein sequences.

    Supports: mutagenesis data, proteomics PTM evidence.

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.endpoint = fields.get("endpoint", "mutagenesis")

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the EBI Proteins API call."""
        try:
            return self._query(arguments)
        except requests.exceptions.Timeout:
            return {"error": f"EBI Proteins API timed out after {self.timeout}s"}
        except requests.exceptions.ConnectionError:
            return {"error": "Failed to connect to EBI Proteins API"}
        except requests.exceptions.HTTPError as e:
            return {"error": f"EBI Proteins API HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error querying EBI Proteins API: {str(e)}"}

    def _query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate endpoint."""
        if self.endpoint == "mutagenesis":
            return self._get_mutagenesis(arguments)
        elif self.endpoint == "proteomics_ptm":
            return self._get_proteomics_ptm(arguments)
        else:
            return {"error": f"Unknown endpoint: {self.endpoint}"}

    def _get_mutagenesis(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get mutagenesis experiment data for a protein."""
        accession = arguments.get("accession", "")
        if not accession:
            return {
                "error": "accession parameter is required (UniProt accession, e.g., P04637)"
            }

        url = f"{PROTEINS_API_BASE_URL}/mutagenesis/{accession}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        features = []
        for f in data.get("features", []):
            # Extract evidence details
            evidences = []
            for ev in f.get("evidences", []):
                src = ev.get("source", {})
                evidences.append(
                    {
                        "code": ev.get("code"),
                        "source_name": src.get("name"),
                        "source_id": src.get("id"),
                        "source_url": src.get("url"),
                    }
                )

            features.append(
                {
                    "type": f.get("type"),
                    "position_start": f.get("begin"),
                    "position_end": f.get("end"),
                    "original_sequence": f.get("alternativeSequence"),
                    "description": f.get("description"),
                    "evidences": evidences[:5],
                }
            )

        return {
            "data": {
                "accession": data.get("accession"),
                "entry_name": data.get("entryName"),
                "gene_name": None,
                "features": features[:100],
                "total_features": len(data.get("features", [])),
            },
            "metadata": {
                "source": "EBI Proteins API - Mutagenesis",
                "accession": accession,
            },
        }

    def _get_proteomics_ptm(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get post-translational modification evidence from mass spec proteomics."""
        accession = arguments.get("accession", "")
        if not accession:
            return {
                "error": "accession parameter is required (UniProt accession, e.g., P04637)"
            }

        url = f"{PROTEINS_API_BASE_URL}/proteomics-ptm/{accession}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        features = []
        for f in data.get("features", []):
            # Extract source databases
            evidences = []
            for ev in f.get("evidences", []):
                src = ev.get("source", {})
                props = src.get("properties", {})
                evidences.append(
                    {
                        "source": src.get("name"),
                        "id": src.get("id"),
                        "url": src.get("url"),
                        "properties": props,
                    }
                )

            features.append(
                {
                    "type": f.get("type"),
                    "position_start": f.get("begin"),
                    "position_end": f.get("end"),
                    "description": f.get("description"),
                    "evidences": evidences[:5],
                }
            )

        return {
            "data": {
                "accession": data.get("accession"),
                "entry_name": data.get("entryName"),
                "features": features[:100],
                "total_features": len(data.get("features", [])),
            },
            "metadata": {
                "source": "EBI Proteins API - Proteomics PTM",
                "accession": accession,
            },
        }
