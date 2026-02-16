# monarch_v3_tool.py
"""
Monarch Initiative V3 API tool for ToolUniverse.

The Monarch Initiative integrates gene, disease, and phenotype data
from multiple organisms to support biomedical discovery. The V3 API
provides access to a knowledge graph linking genes, diseases, phenotypes,
and variants across species.

API: https://api.monarchinitiative.org/v3/api/
No authentication required. Free public access.
"""

import requests
from typing import Dict, Any
from .base_tool import BaseTool
from .tool_registry import register_tool

MONARCH_BASE_URL = "https://api.monarchinitiative.org/v3/api"


@register_tool("MonarchV3Tool")
class MonarchV3Tool(BaseTool):
    """
    Tool for querying the Monarch Initiative V3 knowledge graph.

    Monarch provides integrated data linking genes, diseases, phenotypes,
    and model organisms. The V3 API supports entity lookup, association
    queries, and cross-species phenotype comparisons. Data sources include
    OMIM, ClinVar, HPO, MGI, ZFIN, FlyBase, WormBase, and others.

    Supports: entity lookup, phenotype associations, disease-gene associations.

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.endpoint = fields.get("endpoint", "entity")

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Monarch V3 API call."""
        try:
            return self._query(arguments)
        except requests.exceptions.Timeout:
            return {"error": f"Monarch API timed out after {self.timeout}s"}
        except requests.exceptions.ConnectionError:
            return {"error": "Failed to connect to Monarch Initiative API"}
        except requests.exceptions.HTTPError as e:
            return {"error": f"Monarch API HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error querying Monarch: {str(e)}"}

    def _query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate Monarch V3 endpoint."""
        if self.endpoint == "entity":
            return self._get_entity(arguments)
        elif self.endpoint == "associations":
            return self._get_associations(arguments)
        elif self.endpoint == "search":
            return self._search(arguments)
        else:
            return {"error": f"Unknown endpoint: {self.endpoint}"}

    def _get_entity(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed entity information by CURIE identifier."""
        entity_id = arguments.get("entity_id", "")
        if not entity_id:
            return {
                "error": "entity_id parameter is required (e.g., HGNC:11998, MONDO:0005148, HP:0001250)"
            }

        url = f"{MONARCH_BASE_URL}/entity/{entity_id}"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        return {
            "data": {
                "id": data.get("id"),
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "category": data.get("category"),
                "description": data.get("description"),
                "symbol": data.get("symbol"),
                "synonyms": data.get("synonym", []),
                "xrefs": data.get("xref", []),
                "taxon": data.get("in_taxon"),
                "taxon_label": data.get("in_taxon_label"),
                "provided_by": data.get("provided_by"),
            },
            "metadata": {
                "source": "Monarch Initiative V3",
            },
        }

    def _get_associations(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get associations for an entity with filtering by category."""
        subject = arguments.get("subject", "")
        if not subject:
            return {
                "error": "subject parameter is required (e.g., HGNC:11998 or MONDO:0005148)"
            }

        category = arguments.get("category", "")
        if not category:
            return {
                "error": "category parameter is required. Options: biolink:GeneToPhenotypicFeatureAssociation, biolink:DiseaseToPhenotypicFeatureAssociation, biolink:CorrelatedGeneToDiseaseAssociation, biolink:CausalGeneToDiseaseAssociation, biolink:VariantToDiseaseAssociation, biolink:GeneToPathwayAssociation"
            }

        limit = arguments.get("limit") or 20

        url = f"{MONARCH_BASE_URL}/association"
        params = {
            "subject": subject,
            "category": category,
            "limit": min(limit, 200),
        }

        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        associations = []
        for item in data.get("items", []):
            associations.append(
                {
                    "subject": item.get("subject"),
                    "subject_label": item.get("subject_label"),
                    "object": item.get("object"),
                    "object_label": item.get("object_label"),
                    "category": item.get("category"),
                    "predicate": item.get("predicate"),
                    "negated": item.get("negated"),
                    "provided_by": item.get("provided_by"),
                    "primary_knowledge_source": item.get("primary_knowledge_source"),
                }
            )

        return {
            "data": associations,
            "metadata": {
                "source": "Monarch Initiative V3",
                "subject": subject,
                "category": category,
                "total_results": data.get("total", len(associations)),
            },
        }

    def _search(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search Monarch knowledge graph for entities by name/keyword."""
        query = arguments.get("query", "")
        if not query:
            return {"error": "query parameter is required"}

        limit = arguments.get("limit") or 10
        category = arguments.get("category")  # e.g., biolink:Gene, biolink:Disease

        url = f"{MONARCH_BASE_URL}/search"
        params = {
            "q": query,
            "limit": min(limit, 50),
        }
        if category:
            params["category"] = category

        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            results.append(
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "category": item.get("category"),
                    "symbol": item.get("symbol"),
                    "description": item.get("description"),
                    "taxon": item.get("in_taxon"),
                    "taxon_label": item.get("in_taxon_label"),
                }
            )

        return {
            "data": results,
            "metadata": {
                "source": "Monarch Initiative V3",
                "query": query,
                "total_results": data.get("total", len(results)),
            },
        }
