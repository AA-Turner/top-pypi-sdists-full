import os
import requests
import time
import threading
from typing import Any, Dict, Optional
from .base_tool import BaseTool
from .base_rest_tool import BaseRESTTool
from .http_utils import request_with_retry
from .tool_registry import register_tool


@register_tool("PubMedRESTTool")
class PubMedRESTTool(BaseRESTTool):
    """Generic REST tool for PubMed E-utilities (efetch, elink).

    Implements rate limiting per NCBI guidelines:
    - Without API key: 3 requests/second
    - With API key: 10 requests/second

    API key is read from environment variable NCBI_API_KEY.
    Get your free key at: https://www.ncbi.nlm.nih.gov/account/
    """

    # Class-level rate limiting (shared across all instances)
    _last_request_time = 0.0
    _rate_limit_lock = threading.Lock()

    def __init__(self, tool_config):
        super().__init__(tool_config)
        # Get API key from environment as fallback
        self.default_api_key = os.environ.get("NCBI_API_KEY", "")

    def _get_param_mapping(self) -> Dict[str, str]:
        """Map PubMed E-utilities parameter names."""
        return {
            "limit": "retmax",  # limit -> retmax for E-utilities
        }

    def _enforce_rate_limit(self, has_api_key: bool) -> None:
        """Enforce NCBI E-utilities rate limits.

        Args:
            has_api_key: Whether an API key is provided
        """
        # Rate limits per NCBI guidelines
        # https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen
        # Using conservative intervals to avoid rate limit errors:
        # - Without API key: 3 req/sec -> 0.4s interval (more conservative than 0.33s)
        # - With API key: 10 req/sec -> 0.15s interval (more conservative than 0.1s)
        min_interval = 0.15 if has_api_key else 0.4

        with self._rate_limit_lock:
            current_time = time.time()
            time_since_last = current_time - PubMedRESTTool._last_request_time

            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)

            PubMedRESTTool._last_request_time = time.time()

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

        # Add API key from environment variable
        if self.default_api_key:
            params["api_key"] = self.default_api_key

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
        Enforces NCBI rate limits to prevent API errors.
        """
        url = None
        try:
            # Enforce rate limiting before making request
            has_api_key = bool(self.default_api_key)
            self._enforce_rate_limit(has_api_key)

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

                # Check for API errors in response
                if "ERROR" in data:
                    error_msg = data.get("ERROR", "Unknown API error")
                    return {
                        "status": "error",
                        "data": f"NCBI API error: {error_msg[:200]}",
                        "url": response.url,
                    }

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

                # For elink responses with LinkOut URLs (llinks command)
                if "linksets" in data:
                    linksets = data.get("linksets", [])
                    # Check for empty linksets with errors
                    if not linksets or (linksets and len(linksets) == 0):
                        return {
                            "status": "success",
                            "data": [],
                            "count": 0,
                            "url": response.url,
                        }

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
                        # Extract LinkOut URLs (idurllist)
                        elif "idurllist" in linkset:
                            return {
                                "status": "success",
                                "data": linkset.get("idurllist", {}),
                                "url": response.url,
                            }

                # For elink responses with LinkOut URLs (llinks returns direct idurllist)
                if "idurllist" in data:
                    return {
                        "status": "success",
                        "data": data.get("idurllist", []),
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
