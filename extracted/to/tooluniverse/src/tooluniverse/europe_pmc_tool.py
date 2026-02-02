import requests
from .base_tool import BaseTool
from .tool_registry import register_tool
from .http_utils import request_with_retry


@register_tool("EuropePMCTool")
class EuropePMCTool(BaseTool):
    """
    Tool to search for articles on Europe PMC including abstracts.
    """

    def __init__(
        self,
        tool_config,
        base_url="https://www.ebi.ac.uk/europepmc/webservices/rest/search",
    ):
        super().__init__(tool_config)
        self.base_url = base_url

    def run(self, arguments):
        query = arguments.get("query")
        limit = arguments.get("limit", 5)
        if not query:
            return {"error": "`query` parameter is required."}
        return self._search(query, limit)

    def _search(self, query, limit):
        # First try core mode to get abstracts
        core_params = {
            "query": query,
            "resultType": "core",
            "pageSize": limit,
            "format": "json",
        }
        core_response = requests.get(self.base_url, params=core_params, timeout=20)

        # Then try lite mode to get journal information
        lite_params = {
            "query": query,
            "resultType": "lite",
            "pageSize": limit,
            "format": "json",
        }
        lite_response = requests.get(self.base_url, params=lite_params, timeout=20)

        if core_response.status_code != 200:
            return {
                "error": f"Europe PMC API error {core_response.status_code}",
                "reason": core_response.reason,
            }

        # Get core mode results
        core_results = core_response.json().get("resultList", {}).get("result", [])
        lite_results = []

        # If lite mode also succeeds, get journal information
        if lite_response.status_code == 200:
            lite_results = lite_response.json().get("resultList", {}).get("result", [])

        # Create ID to record mapping
        lite_map = {rec.get("id"): rec for rec in lite_results}

        articles = []
        for rec in core_results:
            # Extract basic information
            title = rec.get("title")
            abstract = rec.get("abstractText")
            year = rec.get("pubYear")

            # Extract author information
            authors = []
            author_list = rec.get("authorList", {}).get("author", [])
            if isinstance(author_list, list):
                for author in author_list:
                    if isinstance(author, dict):
                        full_name = author.get("fullName", "")
                        if full_name:
                            authors.append(full_name)
            elif isinstance(author_list, dict):
                full_name = author_list.get("fullName", "")
                if full_name:
                    authors.append(full_name)

            # Get journal information from lite mode
            journal = None
            if rec.get("id") in lite_map:
                lite_rec = lite_map[rec["id"]]
                journal = lite_rec.get("journalTitle")

            # If still no journal information, use source field
            if not journal:
                journal = rec.get("source")

            # Extract DOI
            doi = rec.get("doi", "")

            # Extract citation count
            citations = rec.get("citedByCount", 0)
            if citations:
                try:
                    citations = int(citations)
                except (ValueError, TypeError):
                    citations = 0

            # Extract open access status
            open_access_raw = rec.get("isOpenAccess", False)
            # Normalize to boolean (API can return 'Y'/'N' or True/False)
            if isinstance(open_access_raw, str):
                open_access = open_access_raw.upper() == "Y"
            else:
                open_access = bool(open_access_raw)

            # Extract keywords
            keywords = []
            text_mined_terms = rec.get("hasTextMinedTerms", {})
            if text_mined_terms and isinstance(text_mined_terms, dict):
                # Try to extract keywords
                for _key, value in text_mined_terms.items():
                    if isinstance(value, list):
                        keywords.extend(value)
                    elif isinstance(value, str):
                        keywords.append(value)

            # Handle missing abstract
            if not abstract:
                abstract = "Abstract not available"

            # Handle missing journal information
            if not journal:
                journal = "Journal information not available"

            # Build URL
            source = rec.get("source", "")
            article_id = rec.get("id", "")
            url = (
                f"https://europepmc.org/article/{source}/{article_id}"
                if source and article_id
                else "URL not available"
            )

            articles.append(
                {
                    "title": title or "Title not available",
                    "abstract": abstract,
                    "authors": (
                        authors if authors else "Author information not available"
                    ),
                    "journal": journal,
                    "year": year,
                    "doi": doi or "DOI not available",
                    "url": url,
                    "citations": citations,
                    "open_access": open_access,
                    "keywords": keywords if keywords else "Keywords not available",
                    "source": "Europe PMC",
                    "data_quality": {
                        "has_abstract": bool(
                            abstract and abstract != "Abstract not available"
                        ),
                        "has_authors": bool(authors),
                        "has_journal": bool(
                            journal and journal != "Journal information not available"
                        ),
                        "has_year": bool(year),
                        "has_doi": bool(doi),
                        "has_citations": bool(citations and citations > 0),
                        "has_keywords": bool(keywords),
                        "has_url": bool(url and url != "URL not available"),
                    },
                }
            )
        return articles


@register_tool("EuropePMCRESTTool")
class EuropePMCRESTTool(BaseTool):
    """
    Generic REST tool for Europe PMC API endpoints.
    Supports citations, references, and other article-related endpoints.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest"
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = 30

    def _build_url(self, arguments):
        """Build URL from endpoint template and arguments."""
        endpoint = self.tool_config["fields"]["endpoint"]
        url = endpoint
        for key, value in arguments.items():
            placeholder = f"{{{key}}}"
            if placeholder in url:
                url = url.replace(placeholder, str(value))
        return url

    def run(self, arguments):
        """Execute the Europe PMC REST API request."""
        try:
            url = self._build_url(arguments)

            # Extract query parameters (those not in URL path)
            params = {"format": "json"}
            endpoint_template = self.tool_config["fields"]["endpoint"]

            # Add parameters that are not path parameters
            for key, value in arguments.items():
                placeholder = f"{{{key}}}"
                if placeholder not in endpoint_template and value is not None:
                    params[key] = value

            response = request_with_retry(
                self.session,
                "GET",
                url,
                params=params,
                timeout=self.timeout,
                max_attempts=3,
            )

            if response.status_code == 200:
                data = response.json()
                return {"status": "success", "data": data, "url": response.url}
            else:
                return {
                    "status": "error",
                    "error": f"Europe PMC API returned status {response.status_code}",
                    "url": response.url,
                    "status_code": response.status_code,
                    "detail": response.text[:200] if response.text else None,
                }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Europe PMC API request failed: {str(e)}",
                "url": url if "url" in locals() else None,
            }
