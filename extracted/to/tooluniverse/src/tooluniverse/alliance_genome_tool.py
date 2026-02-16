# alliance_genome_tool.py
"""
Alliance of Genome Resources REST API tool for ToolUniverse.

The Alliance of Genome Resources (AGR) integrates data from 7 model organism
databases (SGD, FlyBase, WormBase, ZFIN, RGD, MGI, Xenbase) plus human data.
It provides unified access to gene information, disease associations,
phenotypes, and cross-species search across all model organisms.

API: https://www.alliancegenome.org/api
No authentication required.
"""

import requests
from typing import Dict, Any
from .base_tool import BaseTool
from .tool_registry import register_tool

ALLIANCE_BASE = "https://www.alliancegenome.org/api"


@register_tool("AllianceGenomeTool")
class AllianceGenomeTool(BaseTool):
    """
    Tool for querying the Alliance of Genome Resources API.

    Provides cross-species gene information across 7 model organisms
    (yeast, fly, worm, zebrafish, rat, mouse, frog) plus human.
    Supports gene detail, disease associations, phenotypes, and search.

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        self.endpoint_type = tool_config.get("fields", {}).get(
            "endpoint_type", "gene_detail"
        )

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Alliance of Genome Resources API call."""
        try:
            return self._query(arguments)
        except requests.exceptions.Timeout:
            return {"error": f"Alliance API request timed out after {self.timeout}s"}
        except requests.exceptions.ConnectionError:
            return {
                "error": "Failed to connect to Alliance API. Check network connectivity."
            }
        except requests.exceptions.HTTPError as e:
            return {"error": f"Alliance API HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error querying Alliance API: {str(e)}"}

    def _query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to the appropriate Alliance endpoint."""
        endpoint_type = self.endpoint_type

        if endpoint_type == "gene_detail":
            return self._get_gene_detail(arguments)
        elif endpoint_type == "search_genes":
            return self._search_genes(arguments)
        elif endpoint_type == "gene_phenotypes":
            return self._get_gene_phenotypes(arguments)
        elif endpoint_type == "disease_genes":
            return self._get_disease_genes(arguments)
        elif endpoint_type == "disease_detail":
            return self._get_disease_detail(arguments)
        else:
            return {"error": f"Unknown endpoint type: {endpoint_type}"}

    def _get_gene_detail(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed gene information from Alliance."""
        gene_id = arguments.get("gene_id", "")
        if not gene_id:
            return {
                "error": "gene_id parameter is required (e.g., 'HGNC:6081', 'MGI:98834', 'FB:FBgn0003996')"
            }

        url = f"{ALLIANCE_BASE}/gene/{gene_id}"
        response = requests.get(
            url, headers={"Accept": "application/json"}, timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()

        species = data.get("species", {})
        locations = data.get("genomeLocations", [])
        loc_info = locations[0] if locations else {}
        xrefs = data.get("crossReferenceMap", {})

        # Extract cross-references
        other_xrefs = xrefs.get("other", [])
        xref_list = [
            {"name": x.get("name"), "url": x.get("crossRefCompleteUrl")}
            for x in other_xrefs[:10]
        ]

        return {
            "data": {
                "id": data.get("id"),
                "symbol": data.get("symbol"),
                "name": data.get("name"),
                "species": {
                    "name": species.get("name"),
                    "short_name": species.get("shortName"),
                    "taxon_id": species.get("taxonId"),
                    "data_provider": species.get("dataProviderShortName"),
                },
                "gene_synopsis": data.get("geneSynopsis"),
                "automated_gene_synopsis": data.get("automatedGeneSynopsis"),
                "synonyms": data.get("synonyms", []),
                "so_term": data.get("soTerm", {}).get("name"),
                "genomic_location": {
                    "chromosome": loc_info.get("chromosome"),
                    "start": loc_info.get("start"),
                    "end": loc_info.get("end"),
                    "assembly": loc_info.get("assembly"),
                    "strand": loc_info.get("strand"),
                },
                "cross_references": xref_list,
            },
            "metadata": {
                "query_gene_id": gene_id,
                "data_provider": data.get("dataProvider"),
                "source": "Alliance of Genome Resources",
            },
        }

    def _search_genes(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for genes across all model organisms."""
        query = arguments.get("query", "")
        if not query:
            return {"error": "query parameter is required"}

        limit = arguments.get("limit", 10)
        url = f"{ALLIANCE_BASE}/search_autocomplete"
        params = {"q": query, "category": "gene", "limit": min(int(limit), 50)}

        response = requests.get(
            url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        genes = []
        for r in results:
            genes.append(
                {
                    "symbol": r.get("symbol"),
                    "name": r.get("name"),
                    "primary_key": r.get("primaryKey"),
                    "name_key": r.get("name_key"),
                    "category": r.get("category"),
                }
            )

        return {
            "data": genes,
            "metadata": {
                "total_results": len(genes),
                "query": query,
                "source": "Alliance of Genome Resources",
            },
        }

    def _get_gene_phenotypes(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get phenotype annotations for a gene."""
        gene_id = arguments.get("gene_id", "")
        if not gene_id:
            return {"error": "gene_id parameter is required"}

        limit = arguments.get("limit", 20)
        page = arguments.get("page", 1)
        url = f"{ALLIANCE_BASE}/gene/{gene_id}/phenotypes"
        params = {"limit": min(int(limit), 100), "page": int(page)}

        response = requests.get(
            url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        total = data.get("total", 0)
        results = data.get("results", [])
        phenotypes = []
        for r in results:
            subject = r.get("subject", {})
            phenotypes.append(
                {
                    "gene_symbol": subject.get("symbol"),
                    "gene_id": subject.get("primaryExternalId"),
                    "phenotype_statement": r.get("phenotypeStatement"),
                }
            )

        return {
            "data": phenotypes,
            "metadata": {
                "total_results": total,
                "returned": len(phenotypes),
                "query_gene_id": gene_id,
                "page": int(page),
                "source": "Alliance of Genome Resources",
            },
        }

    def _get_disease_genes(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get genes associated with a disease by Disease Ontology ID."""
        disease_id = arguments.get("disease_id", "")
        if not disease_id:
            return {
                "error": "disease_id parameter is required (e.g., 'DOID:162' for cancer)"
            }

        limit = arguments.get("limit", 20)
        page = arguments.get("page", 1)
        url = f"{ALLIANCE_BASE}/disease/{disease_id}/genes"
        params = {"limit": min(int(limit), 100), "page": int(page)}

        response = requests.get(
            url,
            params=params,
            headers={"Accept": "application/json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        total = data.get("total", 0)
        results = data.get("results", [])
        genes = []
        for r in results:
            subject = r.get("subject", {})
            species = subject.get("taxon", {})
            disease_obj = r.get("object", {})
            genes.append(
                {
                    "gene_symbol": subject.get("symbol")
                    or subject.get("geneSymbol", {}).get("displayText"),
                    "gene_id": subject.get("primaryExternalId") or subject.get("curie"),
                    "species": species.get("curie"),
                    "disease_name": disease_obj.get("name"),
                    "disease_id": disease_obj.get("curie"),
                    "association_type": r.get("associationType"),
                }
            )

        return {
            "data": genes,
            "metadata": {
                "total_results": total,
                "returned": len(genes),
                "query_disease_id": disease_id,
                "page": int(page),
                "source": "Alliance of Genome Resources",
            },
        }

    def _get_disease_detail(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get disease summary information by Disease Ontology ID."""
        disease_id = arguments.get("disease_id", "")
        if not disease_id:
            return {
                "error": "disease_id parameter is required (e.g., 'DOID:162' for cancer)"
            }

        url = f"{ALLIANCE_BASE}/disease/{disease_id}"
        response = requests.get(
            url, headers={"Accept": "application/json"}, timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()

        do_term = data.get("doTerm", {})
        synonyms = do_term.get("synonyms", [])
        synonym_names = [s.get("name") for s in synonyms if s.get("name")]

        return {
            "data": {
                "disease_id": do_term.get("curie"),
                "name": do_term.get("name"),
                "definition": do_term.get("definition"),
                "synonyms": synonym_names,
                "category": data.get("category"),
            },
            "metadata": {
                "query_disease_id": disease_id,
                "source": "Alliance of Genome Resources",
            },
        }
