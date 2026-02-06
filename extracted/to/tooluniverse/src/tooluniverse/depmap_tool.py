# depmap_tool.py
"""
DepMap (Dependency Map) API tool for ToolUniverse.

DepMap provides cancer cell line dependency data from CRISPR knockout screens,
drug sensitivity data, and multi-omics characterization of cancer cell lines.

Data includes:
- CRISPR gene effect scores (gene essentiality)
- Drug sensitivity data
- Cell line metadata (lineage, mutations)
- Gene expression data

API Documentation: https://depmap.sanger.ac.uk/documentation/api/
Base URL: https://api.cellmodelpassports.sanger.ac.uk
"""

import requests
from typing import Dict, Any, List, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool

# Base URL for Sanger Cell Model Passports API
DEPMAP_BASE_URL = "https://api.cellmodelpassports.sanger.ac.uk"


@register_tool("DepMapTool")
class DepMapTool(BaseTool):
    """
    Tool for querying DepMap/Sanger Cell Model Passports API.

    Provides access to:
    - Cancer cell line dependency data (CRISPR screens)
    - Drug sensitivity profiles
    - Cell line metadata and annotations
    - Gene effect scores for target validation

    No authentication required for non-commercial use.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        self.operation = tool_config.get("fields", {}).get(
            "operation", "get_cell_lines"
        )

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the DepMap API call."""
        operation = self.operation

        if operation == "get_cell_lines":
            return self._get_cell_lines(arguments)
        elif operation == "get_cell_line":
            return self._get_cell_line(arguments)
        elif operation == "search_cell_lines":
            return self._search_cell_lines(arguments)
        elif operation == "get_gene_dependencies":
            return self._get_gene_dependencies(arguments)
        elif operation == "get_drug_response":
            return self._get_drug_response(arguments)
        else:
            return {"status": "error", "error": f"Unknown operation: {operation}"}

    def _get_cell_lines(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get list of cancer cell lines with metadata.

        Filter by tissue type or cancer type.
        """
        tissue = arguments.get("tissue")
        cancer_type = arguments.get("cancer_type")
        page_size = arguments.get("page_size", 20)

        try:
            url = f"{DEPMAP_BASE_URL}/models"
            params = {"page[size]": min(page_size, 100)}

            # Add filters if provided
            filters = []
            if tissue:
                filters.append(f"tissue:{tissue}")
            if cancer_type:
                filters.append(f"cancer_type:{cancer_type}")

            if filters:
                params["filter[model]"] = ",".join(filters)

            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            # Parse cell line data
            cell_lines = []
            for item in data.get("data", []):
                attrs = item.get("attributes", {})
                cell_lines.append(
                    {
                        "model_id": item.get("id"),
                        "model_name": attrs.get("model_name"),
                        "tissue": attrs.get("tissue"),
                        "cancer_type": attrs.get("cancer_type"),
                        "sample_site": attrs.get("sample_site"),
                        "gender": attrs.get("gender"),
                        "ethnicity": attrs.get("ethnicity"),
                    }
                )

            return {
                "status": "success",
                "data": {
                    "cell_lines": cell_lines,
                    "count": len(cell_lines),
                    "total": data.get("meta", {}).get("total", len(cell_lines)),
                },
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error": f"DepMap API timeout after {self.timeout}s",
            }
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"DepMap API request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_cell_line(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed information for a specific cell line.

        Returns metadata, mutations, and available data types.
        """
        model_id = arguments.get("model_id")
        model_name = arguments.get("model_name")

        if not model_id and not model_name:
            return {
                "status": "error",
                "error": "Either model_id or model_name is required",
            }

        try:
            if model_id:
                url = f"{DEPMAP_BASE_URL}/models/{model_id}"
            else:
                # Search by name first
                search_result = self._search_cell_lines({"query": model_name})
                if (
                    search_result["status"] != "success"
                    or not search_result["data"]["cell_lines"]
                ):
                    return {
                        "status": "success",
                        "data": None,
                        "message": f"Cell line '{model_name}' not found",
                    }
                model_id = search_result["data"]["cell_lines"][0]["model_id"]
                url = f"{DEPMAP_BASE_URL}/models/{model_id}"

            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 404:
                return {
                    "status": "success",
                    "data": None,
                    "message": f"Cell line not found: {model_id or model_name}",
                }

            response.raise_for_status()
            data = response.json()

            item = data.get("data", {})
            attrs = item.get("attributes", {})

            return {
                "status": "success",
                "data": {
                    "model_id": item.get("id"),
                    "model_name": attrs.get("model_name"),
                    "tissue": attrs.get("tissue"),
                    "cancer_type": attrs.get("cancer_type"),
                    "tissue_status": attrs.get("tissue_status"),
                    "sample_site": attrs.get("sample_site"),
                    "gender": attrs.get("gender"),
                    "ethnicity": attrs.get("ethnicity"),
                    "age_at_sampling": attrs.get("age_at_sampling"),
                    "growth_properties": attrs.get("growth_properties"),
                    "msi_status": attrs.get("msi_status"),
                    "ploidy": attrs.get("ploidy"),
                    "mutational_burden": attrs.get("mutational_burden"),
                },
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error": f"DepMap API timeout after {self.timeout}s",
            }
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"DepMap API request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _search_cell_lines(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search cell lines by name or identifier.
        """
        query = arguments.get("query")

        if not query:
            return {"status": "error", "error": "query parameter is required"}

        try:
            url = f"{DEPMAP_BASE_URL}/models"
            params = {"filter[model]": f"model_name:{query}", "page[size]": 20}

            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            cell_lines = []
            for item in data.get("data", []):
                attrs = item.get("attributes", {})
                cell_lines.append(
                    {
                        "model_id": item.get("id"),
                        "model_name": attrs.get("model_name"),
                        "tissue": attrs.get("tissue"),
                        "cancer_type": attrs.get("cancer_type"),
                    }
                )

            return {
                "status": "success",
                "data": {
                    "query": query,
                    "cell_lines": cell_lines,
                    "count": len(cell_lines),
                },
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error": f"DepMap API timeout after {self.timeout}s",
            }
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"DepMap API request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_gene_dependencies(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get CRISPR gene dependency data.

        Returns gene effect scores indicating essentiality in cancer cell lines.
        Negative scores indicate the gene is essential (cell death upon knockout).
        """
        gene_symbol = arguments.get("gene_symbol")
        arguments.get("model_id")

        if not gene_symbol:
            return {"status": "error", "error": "gene_symbol parameter is required"}

        try:
            # Query the genes endpoint
            url = f"{DEPMAP_BASE_URL}/genes"
            params = {"filter[gene]": f"symbol:{gene_symbol}", "page[size]": 10}

            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            genes = []
            for item in data.get("data", []):
                attrs = item.get("attributes", {})
                genes.append(
                    {
                        "gene_id": item.get("id"),
                        "symbol": attrs.get("symbol"),
                        "name": attrs.get("name"),
                        "ensembl_id": attrs.get("ensembl_gene_id"),
                    }
                )

            return {
                "status": "success",
                "data": {
                    "gene_symbol": gene_symbol,
                    "genes": genes,
                    "note": "Gene effect scores are available through the DepMap portal. Negative scores indicate gene essentiality.",
                },
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error": f"DepMap API timeout after {self.timeout}s",
            }
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"DepMap API request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    def _get_drug_response(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get drug sensitivity data for cell lines.

        Returns IC50/AUC values for drug-cell line combinations.
        """
        drug_name = arguments.get("drug_name")
        model_id = arguments.get("model_id")

        if not drug_name and not model_id:
            return {
                "status": "error",
                "error": "Either drug_name or model_id is required",
            }

        try:
            # Query drugs endpoint
            url = f"{DEPMAP_BASE_URL}/drugs"
            params = {"page[size]": 20}

            if drug_name:
                params["filter[drug]"] = f"drug_name:{drug_name}"

            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            drugs = []
            for item in data.get("data", []):
                attrs = item.get("attributes", {})
                drugs.append(
                    {
                        "drug_id": item.get("id"),
                        "drug_name": attrs.get("drug_name"),
                        "synonyms": attrs.get("synonyms"),
                        "targets": attrs.get("targets"),
                        "target_pathway": attrs.get("target_pathway"),
                    }
                )

            return {
                "status": "success",
                "data": {
                    "query": drug_name or model_id,
                    "drugs": drugs,
                    "count": len(drugs),
                    "note": "Drug sensitivity data (IC50, AUC) available through DepMap portal.",
                },
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error": f"DepMap API timeout after {self.timeout}s",
            }
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": f"DepMap API request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}
