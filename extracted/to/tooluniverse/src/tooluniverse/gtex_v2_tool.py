"""
GTEx Portal API V2 Tool

This tool provides access to the GTEx Portal API V2 for querying tissue-specific
gene expression and eQTL data. GTEx provides comprehensive gene expression and regulation
data from 54 non-diseased tissue sites across nearly 1,000 individuals.

Latest release: Adult GTEx V11 (January 2026)
"""

import requests
from typing import Dict, Any, List
from .base_tool import BaseTool
from .tool_registry import register_tool

GTEX_BASE_URL = "https://gtexportal.org/api/v2"


@register_tool("GTExV2Tool")
class GTExV2Tool(BaseTool):
    """
    GTEx Portal API V2 tool for gene expression and eQTL analysis.

    Provides access to:
    - Gene expression data (median, per-sample)
    - eQTL associations (single-tissue, multi-tissue)
    - Tissue and sample metadata
    - Dataset information
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.parameter = tool_config.get("parameter", {})
        self.required = self.parameter.get("required", [])

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the GTEx API tool with given arguments."""
        # Validate required parameters
        for param in self.required:
            if param not in arguments or arguments[param] is None:
                return {
                    "status": "error",
                    "error": f"Missing required parameter: {param}",
                }

        operation = arguments.get("operation")
        if not operation:
            return {"status": "error", "error": "Missing required parameter: operation"}

        # Route to appropriate operation handler
        operation_handlers = {
            "get_median_gene_expression": self._get_median_gene_expression,
            "get_gene_expression": self._get_gene_expression,
            "get_tissue_sites": self._get_tissue_sites,
            "get_dataset_info": self._get_dataset_info,
            "get_eqtl_genes": self._get_eqtl_genes,
            "get_single_tissue_eqtls": self._get_single_tissue_eqtls,
            "get_multi_tissue_eqtls": self._get_multi_tissue_eqtls,
            "calculate_eqtl": self._calculate_eqtl,
            "get_sample_info": self._get_sample_info,
            "get_top_expressed_genes": self._get_top_expressed_genes,
        }

        handler = operation_handlers.get(operation)
        if not handler:
            return {
                "status": "error",
                "error": f"Unknown operation: {operation}",
                "available_operations": list(operation_handlers.keys()),
            }

        try:
            return handler(arguments)
        except Exception as e:
            return {
                "status": "error",
                "error": f"Operation failed: {str(e)}",
                "operation": operation,
            }

    def _get_median_gene_expression(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get median gene expression across tissues."""
        gencode_ids = arguments.get("gencode_id")
        if isinstance(gencode_ids, str):
            gencode_ids = [gencode_ids]

        # Feature-69A-002: gtex_v10 returns empty results for medianGeneExpression.
        # Default to gtex_v8 which is stable and returns correct tissue expression.
        dataset_id = arguments.get("dataset_id", "gtex_v8")
        tissue_ids = arguments.get("tissue_site_detail_id", [])

        if isinstance(tissue_ids, str):
            tissue_ids = [tissue_ids]

        params = {
            "gencodeId": gencode_ids,
            "datasetId": dataset_id,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        if tissue_ids:
            params["tissueSiteDetailId"] = tissue_ids

        url = f"{GTEX_BASE_URL}/expression/medianGeneExpression"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_results": len(data.get("data", [])),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_gene_expression(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get gene expression data at sample level."""
        gencode_ids = arguments.get("gencode_id")
        if isinstance(gencode_ids, str):
            gencode_ids = [gencode_ids]

        dataset_id = arguments.get("dataset_id", "gtex_v10")
        tissue_ids = arguments.get("tissue_site_detail_id", [])
        attribute_subset = arguments.get("attribute_subset")

        if isinstance(tissue_ids, str):
            tissue_ids = [tissue_ids]

        params = {
            "gencodeId": gencode_ids,
            "datasetId": dataset_id,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        if tissue_ids:
            params["tissueSiteDetailId"] = tissue_ids
        if attribute_subset:
            params["attributeSubset"] = attribute_subset

        url = f"{GTEX_BASE_URL}/expression/geneExpression"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_results": len(data.get("data", [])),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_tissue_sites(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get tissue site information."""
        dataset_id = arguments.get("dataset_id", "gtex_v8")

        params = {
            "datasetId": dataset_id,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        url = f"{GTEX_BASE_URL}/dataset/tissueSiteDetail"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_tissues": len(data.get("data", [])),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_dataset_info(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get GTEx dataset information."""
        dataset_id = arguments.get("dataset_id")

        params = {}
        if dataset_id:
            params["datasetId"] = dataset_id

        url = f"{GTEX_BASE_URL}/metadata/dataset"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            api_data = response.json()
            datasets = api_data if isinstance(api_data, list) else [api_data]
            return {
                "status": "success",
                "data": datasets,
                "num_datasets": len(datasets),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_eqtl_genes(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get eQTL genes (eGenes) with significant cis-eQTLs."""
        tissue_ids = arguments.get("tissue_site_detail_id", [])
        dataset_id = arguments.get("dataset_id", "gtex_v10")

        if isinstance(tissue_ids, str):
            tissue_ids = [tissue_ids]

        params = {
            "datasetId": dataset_id,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        if tissue_ids:
            params["tissueSiteDetailId"] = tissue_ids

        url = f"{GTEX_BASE_URL}/association/egene"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_egenes": len(data.get("data", [])),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_single_tissue_eqtls(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get significant single-tissue eQTLs."""
        gencode_ids = arguments.get("gencode_id", [])
        variant_ids = arguments.get("variant_id", [])
        tissue_ids = arguments.get("tissue_site_detail_id", [])
        dataset_id = arguments.get("dataset_id", "gtex_v10")

        if isinstance(gencode_ids, str):
            gencode_ids = [gencode_ids]
        if isinstance(variant_ids, str):
            variant_ids = [variant_ids]
        if isinstance(tissue_ids, str):
            tissue_ids = [tissue_ids]

        params = {
            "datasetId": dataset_id,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        if gencode_ids:
            params["gencodeId"] = gencode_ids
        if variant_ids:
            params["variantId"] = variant_ids
        if tissue_ids:
            params["tissueSiteDetailId"] = tissue_ids

        url = f"{GTEX_BASE_URL}/association/singleTissueEqtl"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_eqtls": len(data.get("data", [])),
            }
        elif response.status_code == 400:
            return {
                "status": "error",
                "error": "Invalid query parameters",
                "detail": response.text[:500],
                "message": "At least one of gencode_id, variant_id, or tissue_site_detail_id must be provided",
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_multi_tissue_eqtls(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get multi-tissue eQTL Metasoft results."""
        gencode_id = arguments.get("gencode_id")
        variant_id = arguments.get("variant_id")
        dataset_id = arguments.get("dataset_id", "gtex_v8")

        if not gencode_id:
            return {
                "status": "error",
                "error": "gencode_id is required for multi-tissue eQTL query",
            }

        params = {
            "gencodeId": gencode_id,
            "datasetId": dataset_id,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        if variant_id:
            params["variantId"] = variant_id

        url = f"{GTEX_BASE_URL}/association/metasoft"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_results": len(data.get("data", [])),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _calculate_eqtl(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate dynamic eQTL for gene-variant pair."""
        gencode_id = arguments.get("gencode_id")
        variant_id = arguments.get("variant_id")
        tissue_id = arguments.get("tissue_site_detail_id")
        dataset_id = arguments.get("dataset_id", "gtex_v8")

        if not all([gencode_id, variant_id, tissue_id]):
            return {
                "status": "error",
                "error": "gencode_id, variant_id, and tissue_site_detail_id are all required",
            }

        params = {
            "gencodeId": gencode_id,
            "variantId": variant_id,
            "tissueSiteDetailId": tissue_id,
            "datasetId": dataset_id,
        }

        url = f"{GTEX_BASE_URL}/association/dyneqtl"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            api_data = response.json()
            return {"status": "success", "data": api_data}
        elif response.status_code == 400:
            return {
                "status": "error",
                "error": "Unable to calculate eQTL",
                "detail": response.text[:500],
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_sample_info(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get sample information and metadata."""
        dataset_id = arguments.get("dataset_id", "gtex_v10")
        sample_ids = arguments.get("sample_id", [])
        subject_ids = arguments.get("subject_id", [])
        tissue_ids = arguments.get("tissue_site_detail_id", [])
        sex = arguments.get("sex")
        age_bracket = arguments.get("age_bracket", [])

        if isinstance(sample_ids, str):
            sample_ids = [sample_ids]
        if isinstance(subject_ids, str):
            subject_ids = [subject_ids]
        if isinstance(tissue_ids, str):
            tissue_ids = [tissue_ids]
        if isinstance(age_bracket, str):
            age_bracket = [age_bracket]

        params = {
            "datasetId": dataset_id,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        if sample_ids:
            params["sampleId"] = sample_ids
        if subject_ids:
            params["subjectId"] = subject_ids
        if tissue_ids:
            params["tissueSiteDetailId"] = tissue_ids
        if sex:
            params["sex"] = sex
        if age_bracket:
            params["ageBracket"] = age_bracket

        url = f"{GTEX_BASE_URL}/dataset/sample"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_samples": len(data.get("data", [])),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }

    def _get_top_expressed_genes(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get top expressed genes for a tissue."""
        tissue_id = arguments.get("tissue_site_detail_id")
        dataset_id = arguments.get("dataset_id", "gtex_v10")
        filter_mt = arguments.get("filter_mt_genes", True)

        if not tissue_id:
            return {"status": "error", "error": "tissue_site_detail_id is required"}

        params = {
            "tissueSiteDetailId": tissue_id,
            "datasetId": dataset_id,
            "filterMtGene": filter_mt,
            "page": arguments.get("page", 0),
            "itemsPerPage": arguments.get("items_per_page", 250),
        }

        url = f"{GTEX_BASE_URL}/expression/topExpressedGene"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", []),
                "paging_info": data.get("paging_info", {}),
                "num_genes": len(data.get("data", [])),
            }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status {response.status_code}",
                "detail": response.text[:500],
            }
