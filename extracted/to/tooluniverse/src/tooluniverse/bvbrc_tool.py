# bvbrc_tool.py
"""
BV-BRC (Bacterial and Viral Bioinformatics Resource Center) REST API tool for ToolUniverse.

BV-BRC (formerly PATRIC) is the primary NIAID-funded bioinformatics resource center
for bacterial and viral pathogen genomics. It provides access to genome assemblies,
antimicrobial resistance (AMR) data, genome features, and specialty genes across
hundreds of thousands of pathogen genomes.

API: https://www.bv-brc.org/api/
No authentication required. Free for academic/research use.
"""

import requests
from typing import Dict, Any, Optional, List
from .base_tool import BaseTool
from .tool_registry import register_tool

BVBRC_BASE_URL = "https://www.bv-brc.org/api"


@register_tool("BVBRCTool")
class BVBRCTool(BaseTool):
    """
    Tool for querying the BV-BRC pathogen genomics database.

    BV-BRC provides comprehensive pathogen genome data including genome metadata,
    antimicrobial resistance phenotypes, and annotated genome features. Covers
    bacteria and viruses with rich AMR surveillance data.

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.data_type = fields.get("data_type", "genome")
        self.action = fields.get("action", "search")

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the BV-BRC API call."""
        try:
            return self._query(arguments)
        except requests.exceptions.Timeout:
            return {
                "error": f"BV-BRC API request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Failed to connect to BV-BRC API. Check network connectivity."
            }
        except requests.exceptions.HTTPError as e:
            return {"error": f"BV-BRC API HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error querying BV-BRC: {str(e)}"}

    def _query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate query method."""
        if self.data_type == "genome" and self.action == "get":
            return self._get_genome(arguments)
        elif self.data_type == "genome" and self.action == "search":
            return self._search_genomes(arguments)
        elif self.data_type == "genome_amr":
            return self._search_amr(arguments)
        elif self.data_type == "genome_feature":
            return self._search_features(arguments)
        else:
            return {
                "error": f"Unknown data_type/action: {self.data_type}/{self.action}"
            }

    def _build_query_string(
        self,
        conditions: List[str],
        limit: int = 25,
        select_fields: Optional[List[str]] = None,
    ) -> str:
        """Build BV-BRC SOLR-like query string."""
        parts = []
        if len(conditions) == 1:
            parts.append(conditions[0])
        elif len(conditions) > 1:
            parts.append(f"and({','.join(conditions)})")

        parts.append(f"limit({limit})")

        if select_fields:
            parts.append(f"select({','.join(select_fields)})")

        return "&".join(parts)

    def _make_request(self, endpoint: str, query: str) -> Any:
        """Make a request to BV-BRC API."""
        url = f"{BVBRC_BASE_URL}/{endpoint}/?{query}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _get_genome(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get a specific genome by ID."""
        genome_id = arguments.get("genome_id", "")
        if not genome_id:
            return {"error": "genome_id parameter is required"}

        select_fields = [
            "genome_id",
            "genome_name",
            "organism_name",
            "taxon_id",
            "genome_length",
            "gc_content",
            "contigs",
            "genome_status",
            "isolation_country",
            "host_name",
            "disease",
            "collection_date",
            "completion_date",
            "chromosomes",
            "plasmids",
            "sequences",
        ]

        query = self._build_query_string(
            [f"eq(genome_id,{genome_id})"],
            limit=1,
            select_fields=select_fields,
        )

        data = self._make_request("genome", query)

        if not data:
            return {
                "data": {},
                "metadata": {"source": "BV-BRC", "query_genome_id": genome_id},
            }

        return {
            "data": data[0] if isinstance(data, list) else data,
            "metadata": {"source": "BV-BRC", "query_genome_id": genome_id},
        }

    def _search_genomes(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for genomes by keyword."""
        keyword = arguments.get("keyword", "")
        if not keyword:
            return {"error": "keyword parameter is required"}

        limit = min(arguments.get("limit") or 10, 100)

        select_fields = [
            "genome_id",
            "genome_name",
            "organism_name",
            "taxon_id",
            "genome_length",
            "gc_content",
            "genome_status",
            "host_name",
            "disease",
            "isolation_country",
        ]

        query = self._build_query_string(
            [f"keyword({keyword})"],
            limit=limit,
            select_fields=select_fields,
        )

        data = self._make_request("genome", query)

        results = data if isinstance(data, list) else [data] if data else []
        return {
            "data": results,
            "metadata": {
                "source": "BV-BRC",
                "total_results": len(results),
                "query": keyword,
            },
        }

    def _search_amr(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for antimicrobial resistance data."""
        conditions = []

        antibiotic = arguments.get("antibiotic")
        genome_id = arguments.get("genome_id")
        phenotype = arguments.get("resistant_phenotype")

        if antibiotic:
            conditions.append(f"eq(antibiotic,{antibiotic})")
        if genome_id:
            conditions.append(f"eq(genome_id,{genome_id})")
        if phenotype:
            conditions.append(f"eq(resistant_phenotype,{phenotype})")

        if not conditions:
            return {
                "error": "At least one of antibiotic, genome_id, or resistant_phenotype is required"
            }

        limit = min(arguments.get("limit") or 25, 100)

        select_fields = [
            "genome_id",
            "genome_name",
            "antibiotic",
            "resistant_phenotype",
            "measurement",
            "measurement_value",
            "measurement_unit",
            "laboratory_typing_method",
            "computational_method",
            "evidence",
            "taxon_id",
        ]

        query = self._build_query_string(
            conditions, limit=limit, select_fields=select_fields
        )
        data = self._make_request("genome_amr", query)

        results = data if isinstance(data, list) else [data] if data else []
        return {
            "data": results,
            "metadata": {
                "source": "BV-BRC",
                "total_results": len(results),
                "query_antibiotic": antibiotic,
                "query_genome_id": genome_id,
            },
        }

    def _search_features(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for genome features (genes, CDS)."""
        conditions = [
            "eq(annotation,PATRIC)",
            "eq(feature_type,CDS)",
        ]

        gene = arguments.get("gene")
        product = arguments.get("product")
        genome_id = arguments.get("genome_id")

        if gene:
            conditions.append(f"eq(gene,{gene})")
        if product:
            conditions.append(f"keyword({product})")
        if genome_id:
            conditions.append(f"eq(genome_id,{genome_id})")

        if not gene and not product and not genome_id:
            return {"error": "At least one of gene, product, or genome_id is required"}

        limit = min(arguments.get("limit") or 10, 100)

        select_fields = [
            "patric_id",
            "genome_name",
            "gene",
            "product",
            "feature_type",
            "aa_length",
            "accession",
            "start",
            "end",
            "strand",
            "genome_id",
        ]

        query = self._build_query_string(
            conditions, limit=limit, select_fields=select_fields
        )
        data = self._make_request("genome_feature", query)

        results = data if isinstance(data, list) else [data] if data else []
        return {
            "data": results,
            "metadata": {
                "source": "BV-BRC",
                "total_results": len(results),
                "query_gene": gene,
                "query_product": product,
            },
        }
