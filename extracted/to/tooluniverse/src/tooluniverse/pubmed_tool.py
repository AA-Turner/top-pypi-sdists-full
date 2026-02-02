import requests
from typing import Any, Dict, Optional
from .base_tool import BaseTool
from .base_rest_tool import BaseRESTTool
from .http_utils import request_with_retry
from .tool_registry import register_tool


@register_tool("PubMedRESTTool")
class PubMedRESTTool(BaseRESTTool):
    """Generic REST tool for PubMed E-utilities (efetch, elink)."""

    def _get_param_mapping(self) -> Dict[str, str]:
        """Map PubMed E-utilities parameter names."""
        return {
            "limit": "retmax",  # limit -> retmax for E-utilities
        }

    def _build_params(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Build E-utilities parameters with special handling."""
        params = {}

        # Start with default params from config (db, dbfrom, cmd, linkname, retmode, rettype)
        for key in ["db", "dbfrom", "cmd", "linkname", "retmode", "rettype"]:
            if key in self.tool_config["fields"]:
                params[key] = self.tool_config["fields"][key]

        # Handle PMID as 'id' parameter (for efetch, elink)
        if "pmid" in args:
            params["id"] = args["pmid"]

        # Handle query as 'term' parameter (for esearch)
        if "query" in args:
            params["term"] = args["query"]

        # Add API key if provided
        if "api_key" in args and args["api_key"]:
            params["api_key"] = args["api_key"]

        # Handle limit
        if "limit" in args and args["limit"]:
            params["retmax"] = args["limit"]

        # Set retmode to json for elink and esearch (easier parsing)
        endpoint = self.tool_config["fields"]["endpoint"]
        if "retmode" not in params and ("elink" in endpoint or "esearch" in endpoint):
            params["retmode"] = "json"

        return params

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        PubMed E-utilities need special handling for direct endpoint URLs.
        """
        url = None
        try:
            endpoint = self.tool_config["fields"]["endpoint"]
            params = self._build_params(arguments)

            response = request_with_retry(
                self.session,
                "GET",
                endpoint,
                params=params,
                timeout=self.timeout,
                max_attempts=3,
            )

            if response.status_code != 200:
                return {
                    "status": "error",
                    "error": "PubMed API error",
                    "url": response.url,
                    "status_code": response.status_code,
                    "detail": (response.text or "")[:500],
                }

            # Try JSON first (elink, esearch)
            try:
                data = response.json()

                # For esearch responses, extract ID list
                if "esearchresult" in data:
                    esearch_result = data.get("esearchresult", {})
                    id_list = esearch_result.get("idlist", [])
                    return {
                        "status": "success",
                        "data": id_list,
                        "count": len(id_list),
                        "total_count": int(esearch_result.get("count", 0)),
                        "url": response.url,
                    }

                # For elink responses, extract linksets
                if "linksets" in data:
                    linksets = data.get("linksets", [])
                    if linksets and len(linksets) > 0:
                        linkset = linksets[0]
                        # Extract linked IDs
                        if "linksetdbs" in linkset:
                            linksetdbs = linkset.get("linksetdbs", [])
                            if linksetdbs and len(linksetdbs) > 0:
                                links = linksetdbs[0].get("links", [])
                                return {
                                    "status": "success",
                                    "data": links,
                                    "count": len(links),
                                    "url": response.url,
                                }
                        # Extract LinkOut URLs
                        elif "idurllist" in linkset:
                            return {
                                "status": "success",
                                "data": linkset.get("idurllist", {}),
                                "url": response.url,
                            }

                return {
                    "status": "success",
                    "data": data,
                    "url": response.url,
                }
            except Exception:
                # For XML responses (efetch), return as text
                return {
                    "status": "success",
                    "data": response.text,
                    "url": response.url,
                }

        except Exception as e:
            return {
                "status": "error",
                "error": f"PubMed API error: {str(e)}",
                "url": url,
            }
