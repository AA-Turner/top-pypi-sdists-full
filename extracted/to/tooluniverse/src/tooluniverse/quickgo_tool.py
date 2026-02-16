# quickgo_tool.py
"""
QuickGO (EBI Gene Ontology browser) REST API tool for ToolUniverse.

QuickGO provides fast access to Gene Ontology (GO) annotations and term
information. It offers annotation search by gene product or GO term,
ontology term details, and hierarchical relationships.

API: https://www.ebi.ac.uk/QuickGO/services/
No authentication required. Free for academic/research use.
"""

import requests
from typing import Dict, Any
from .base_tool import BaseTool
from .tool_registry import register_tool

QUICKGO_BASE_URL = "https://www.ebi.ac.uk/QuickGO/services"


@register_tool("QuickGOTool")
class QuickGOTool(BaseTool):
    """
    Tool for querying the EBI QuickGO Gene Ontology browser.

    QuickGO provides comprehensive GO annotation data with filtering
    by gene product, GO term, taxon, evidence code, and more. Also
    provides ontology term details and hierarchical relationships.

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.endpoint = fields.get("endpoint", "annotation_gene")

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the QuickGO API call."""
        try:
            return self._query(arguments)
        except requests.exceptions.Timeout:
            return {
                "error": f"QuickGO API request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Failed to connect to QuickGO API. Check network connectivity."
            }
        except requests.exceptions.HTTPError as e:
            return {"error": f"QuickGO API HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error querying QuickGO: {str(e)}"}

    def _query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate QuickGO endpoint."""
        if self.endpoint == "annotation_gene":
            return self._annotation_by_gene(arguments)
        elif self.endpoint == "annotation_goterm":
            return self._annotation_by_goterm(arguments)
        elif self.endpoint == "term_detail":
            return self._term_detail(arguments)
        elif self.endpoint == "term_children":
            return self._term_children(arguments)
        else:
            return {"error": f"Unknown endpoint: {self.endpoint}"}

    def _annotation_by_gene(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search GO annotations for a specific gene product."""
        gene_product_id = arguments.get("gene_product_id", "")
        if not gene_product_id:
            return {"error": "gene_product_id parameter is required"}

        url = f"{QUICKGO_BASE_URL}/annotation/search"
        params = {
            "geneProductId": gene_product_id,
            "limit": arguments.get("limit", 25),
        }

        # Optional filters
        aspect = arguments.get("aspect")
        if aspect:
            params["aspect"] = aspect

        taxon_id = arguments.get("taxon_id")
        if taxon_id:
            params["taxonId"] = taxon_id

        evidence_code = arguments.get("evidence_code")
        if evidence_code:
            params["goUsage"] = "exact"

        headers = {"Accept": "application/json"}
        response = requests.get(
            url, params=params, headers=headers, timeout=self.timeout
        )
        response.raise_for_status()

        data = response.json()
        annotations = []
        for r in data.get("results", []):
            annotations.append(
                {
                    "go_id": r.get("goId"),
                    "go_name": r.get("goName"),
                    "go_aspect": r.get("goAspect"),
                    "gene_product_id": r.get("geneProductId"),
                    "symbol": r.get("symbol"),
                    "qualifier": r.get("qualifier"),
                    "go_evidence": r.get("goEvidence"),
                    "assigned_by": r.get("assignedBy"),
                    "reference": r.get("reference"),
                }
            )

        return {
            "data": annotations,
            "metadata": {
                "source": "QuickGO",
                "query": gene_product_id,
                "total_annotations": data.get("numberOfHits", len(annotations)),
                "page_size": len(annotations),
            },
        }

    def _annotation_by_goterm(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search GO annotations for a specific GO term."""
        go_id = arguments.get("go_id", "")
        if not go_id:
            return {"error": "go_id parameter is required"}

        url = f"{QUICKGO_BASE_URL}/annotation/search"
        params = {
            "goId": go_id,
            "limit": arguments.get("limit", 25),
        }

        # Optional filters
        taxon_id = arguments.get("taxon_id")
        if taxon_id:
            params["taxonId"] = taxon_id

        headers = {"Accept": "application/json"}
        response = requests.get(
            url, params=params, headers=headers, timeout=self.timeout
        )
        response.raise_for_status()

        data = response.json()
        annotations = []
        for r in data.get("results", []):
            annotations.append(
                {
                    "gene_product_id": r.get("geneProductId"),
                    "symbol": r.get("symbol"),
                    "go_id": r.get("goId"),
                    "go_name": r.get("goName"),
                    "go_aspect": r.get("goAspect"),
                    "qualifier": r.get("qualifier"),
                    "go_evidence": r.get("goEvidence"),
                    "taxon_id": r.get("taxonId"),
                    "assigned_by": r.get("assignedBy"),
                }
            )

        return {
            "data": annotations,
            "metadata": {
                "source": "QuickGO",
                "query_go_id": go_id,
                "total_annotations": data.get("numberOfHits", len(annotations)),
                "page_size": len(annotations),
            },
        }

    def _term_detail(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed information about a GO term."""
        go_id = arguments.get("go_id", "")
        if not go_id:
            return {"error": "go_id parameter is required"}

        url = f"{QUICKGO_BASE_URL}/ontology/go/terms/{go_id}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            return {
                "data": {},
                "metadata": {
                    "source": "QuickGO",
                    "query": go_id,
                    "found": False,
                },
            }

        term = results[0]
        definition = term.get("definition", {})

        # Extract synonyms
        synonyms = []
        for syn in term.get("synonyms", []):
            if isinstance(syn, dict):
                synonyms.append(
                    {
                        "name": syn.get("name"),
                        "type": syn.get("type"),
                    }
                )
            elif isinstance(syn, str):
                synonyms.append({"name": syn, "type": "unknown"})

        # Extract cross-references
        xrefs = []
        for xref in term.get("xRefs", []) or []:
            if isinstance(xref, dict):
                xrefs.append(
                    {
                        "db_code": xref.get("dbCode"),
                        "db_id": xref.get("dbId"),
                    }
                )

        result = {
            "id": term.get("id"),
            "name": term.get("name"),
            "definition": definition.get("text")
            if isinstance(definition, dict)
            else definition,
            "aspect": term.get("aspect"),
            "is_obsolete": term.get("isObsolete", False),
            "synonyms": synonyms,
            "xrefs": xrefs,
            "usage": term.get("usage"),
            "num_children": len(term.get("children", [])),
        }

        return {
            "data": result,
            "metadata": {
                "source": "QuickGO",
                "query": go_id,
                "found": True,
            },
        }

    def _term_children(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get child terms of a GO term."""
        go_id = arguments.get("go_id", "")
        if not go_id:
            return {"error": "go_id parameter is required"}

        url = f"{QUICKGO_BASE_URL}/ontology/go/terms/{go_id}/children"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        children = []
        if results:
            for child in results[0].get("children", []):
                children.append(
                    {
                        "id": child.get("id"),
                        "name": child.get("name"),
                        "relation": child.get("relation"),
                        "has_children": child.get("hasChildren", False),
                    }
                )

        return {
            "data": children,
            "metadata": {
                "source": "QuickGO",
                "parent_go_id": go_id,
                "num_children": len(children),
            },
        }
