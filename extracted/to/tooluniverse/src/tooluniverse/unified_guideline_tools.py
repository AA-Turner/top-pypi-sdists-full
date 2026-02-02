#!/usr/bin/env python3
"""
Unified Guideline Tools
Consolidated clinical guidelines search tools from multiple sources.
"""

import requests
import time
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from markitdown import MarkItDown
from .base_tool import BaseTool
from .tool_registry import register_tool


def _extract_meaningful_terms(query):
    """Return significant query terms for relevance filtering."""
    if not isinstance(query, str):
        return []

    # Keep alphabetic tokens with length >= 3
    tokens = re.findall(r"[a-zA-Z]{3,}", query.lower())
    stop_terms = {
        "management",
        "care",
        "guideline",
        "guidelines",
        "clinical",
        "practice",
        "and",
        "with",
        "for",
        "the",
        "that",
        "from",
        "into",
        "using",
        "update",
        "introduction",
        "review",
        "overview",
        "recommendation",
        "recommendations",
    }
    meaningful = [token for token in tokens if token not in stop_terms]
    return meaningful if meaningful else tokens


@register_tool()
class NICEWebScrapingTool(BaseTool):
    """
    Real NICE guidelines search using web scraping.
    Makes actual HTTP requests to NICE website and parses HTML responses.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.nice.org.uk"
        self.search_url = f"{self.base_url}/search"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_nice_guidelines_real(query, limit)

    def _fetch_guideline_summary(self, url):
        """Fetch summary from a guideline detail page."""
        try:
            time.sleep(0.5)  # Be respectful
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Try to find overview section
            overview = soup.find("div", {"class": "chapter-overview"})
            if overview:
                paragraphs = overview.find_all("p")
                if paragraphs:
                    return " ".join([p.get_text().strip() for p in paragraphs[:2]])

            # Try meta description
            meta_desc = soup.find("meta", {"name": "description"})
            if meta_desc and meta_desc.get("content"):
                return meta_desc.get("content")

            # Try first paragraph in main content
            main_content = soup.find("div", {"class": "content"}) or soup.find("main")
            if main_content:
                first_p = main_content.find("p")
                if first_p:
                    return first_p.get_text().strip()

            return ""
        except Exception:
            return ""

    def _search_nice_guidelines_real(self, query, limit):
        """Search NICE guidelines using real web scraping."""
        try:
            # Add delay to be respectful
            time.sleep(1)

            params = {"q": query, "type": "guidance"}

            response = self.session.get(self.search_url, params=params, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find the JSON data in the script tag
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if not script_tag:
                return {
                    "error": "No search results found",
                    "suggestion": "Try different search terms or check if the NICE website is accessible",
                }

            # Parse the JSON data
            import json

            try:
                data = json.loads(script_tag.string)
                documents = (
                    data.get("props", {})
                    .get("pageProps", {})
                    .get("results", {})
                    .get("documents", [])
                )
            except (json.JSONDecodeError, KeyError) as e:
                return {
                    "error": f"Failed to parse search results: {str(e)}",
                    "source": "NICE",
                }

            if not documents:
                return {
                    "error": "No NICE guidelines found",
                    "suggestion": "Try different search terms or check if the NICE website is accessible",
                }

            # Process the documents
            results = []
            for doc in documents[:limit]:
                try:
                    title = doc.get("title", "").replace("<b>", "").replace("</b>", "")
                    url = doc.get("url", "")

                    # Make URL absolute
                    if url.startswith("/"):
                        url = self.base_url + url

                    # Extract summary - try multiple fields
                    summary = (
                        doc.get("abstract", "")
                        or doc.get("staticAbstract", "")
                        or doc.get("metaDescription", "")
                        or doc.get("teaser", "")
                        or ""
                    )

                    # If still no summary, try to fetch from the detail page
                    if not summary and url:
                        summary = self._fetch_guideline_summary(url)

                    # Extract date
                    publication_date = doc.get("publicationDate", "")
                    last_updated = doc.get("lastUpdated", "")
                    date = last_updated or publication_date

                    # Extract type/category
                    nice_result_type = doc.get("niceResultType", "")
                    nice_guidance_type = doc.get("niceGuidanceType", [])
                    guideline_type = nice_result_type or (
                        nice_guidance_type[0]
                        if nice_guidance_type
                        else "NICE Guideline"
                    )

                    # Determine if it's a guideline
                    is_guideline = any(
                        keyword in guideline_type.lower()
                        for keyword in [
                            "guideline",
                            "quality standard",
                            "technology appraisal",
                        ]
                    )

                    # Extract category
                    category = "Clinical Guidelines"
                    if "quality standard" in guideline_type.lower():
                        category = "Quality Standards"
                    elif "technology appraisal" in guideline_type.lower():
                        category = "Technology Appraisal"

                    result = {
                        "title": title,
                        "url": url,
                        "summary": summary,
                        "content": summary,  # Copy summary to content field
                        "date": date,
                        "type": guideline_type,
                        "source": "NICE",
                        "is_guideline": is_guideline,
                        "category": category,
                    }

                    results.append(result)

                except Exception:
                    # Skip items that can't be parsed
                    continue

            if not results:
                return {
                    "error": "No NICE guidelines found",
                    "suggestion": "Try different search terms or check if the NICE website is accessible",
                }

            return results

        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to search NICE guidelines: {str(e)}",
                "source": "NICE",
            }
        except Exception as e:
            return {"error": f"Error parsing NICE response: {str(e)}", "source": "NICE"}


@register_tool()
class PubMedGuidelinesTool(BaseTool):
    """
    Search PubMed for clinical practice guidelines.
    Uses NCBI E-utilities with guideline publication type filter.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.session = requests.Session()

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)
        api_key = arguments.get("api_key", "")

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_pubmed_guidelines(query, limit, api_key)

    def _search_pubmed_guidelines(self, query, limit, api_key):
        """Search PubMed for guideline publications."""
        try:
            # Add guideline publication type filter
            guideline_query = f"{query} AND (guideline[Publication Type] OR practice guideline[Publication Type])"

            # Search for PMIDs
            search_params = {
                "db": "pubmed",
                "term": guideline_query,
                "retmode": "json",
                "retmax": limit,
            }
            if api_key:
                search_params["api_key"] = api_key

            search_response = self.session.get(
                f"{self.base_url}/esearch.fcgi", params=search_params, timeout=30
            )
            search_response.raise_for_status()
            search_data = search_response.json()

            pmids = search_data.get("esearchresult", {}).get("idlist", [])
            search_data.get("esearchresult", {}).get("count", "0")

            if not pmids:
                return []

            # Get details for PMIDs
            time.sleep(0.5)  # Be respectful with API calls

            detail_params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}
            if api_key:
                detail_params["api_key"] = api_key

            detail_response = self.session.get(
                f"{self.base_url}/esummary.fcgi", params=detail_params, timeout=30
            )
            detail_response.raise_for_status()
            detail_data = detail_response.json()

            # Fetch abstracts using efetch
            time.sleep(0.5)
            abstract_params = {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "xml",
                "rettype": "abstract",
            }
            if api_key:
                abstract_params["api_key"] = api_key

            abstract_response = self.session.get(
                f"{self.base_url}/efetch.fcgi", params=abstract_params, timeout=30
            )
            abstract_response.raise_for_status()

            # Parse abstracts from XML
            import re

            abstracts = {}
            xml_text = abstract_response.text
            # Extract abstracts for each PMID
            for pmid in pmids:
                # Find abstract text for this PMID
                pmid_pattern = rf"<PMID[^>]*>{pmid}</PMID>.*?<AbstractText[^>]*>(.*?)</AbstractText>"
                abstract_match = re.search(pmid_pattern, xml_text, re.DOTALL)
                if abstract_match:
                    # Clean HTML tags from abstract
                    abstract = re.sub(r"<[^>]+>", "", abstract_match.group(1))
                    abstracts[pmid] = abstract.strip()
                else:
                    abstracts[pmid] = ""

            # Process results
            results = []
            query_terms = _extract_meaningful_terms(query)

            for pmid in pmids:
                if pmid in detail_data.get("result", {}):
                    article = detail_data["result"][pmid]

                    # Extract author information
                    authors = []
                    for author in article.get("authors", [])[:3]:
                        authors.append(author.get("name", ""))
                    author_str = ", ".join(authors)
                    if len(article.get("authors", [])) > 3:
                        author_str += ", et al."

                    # Check publication types
                    pub_types = article.get("pubtype", [])
                    is_guideline = any("guideline" in pt.lower() for pt in pub_types)

                    abstract_text = abstracts.get(pmid, "")
                    searchable_text = " ".join(
                        [
                            article.get("title", ""),
                            abstract_text or "",
                            " ".join(pub_types),
                        ]
                    ).lower()

                    if query_terms and not any(
                        term in searchable_text for term in query_terms
                    ):
                        continue

                    result = {
                        "pmid": pmid,
                        "title": article.get("title", ""),
                        "abstract": abstract_text,
                        "content": abstract_text,  # Copy abstract to content field
                        "authors": author_str,
                        "journal": article.get("source", ""),
                        "publication_date": article.get("pubdate", ""),
                        "publication_types": pub_types,
                        "is_guideline": is_guideline,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        "doi": (
                            article.get("elocationid", "").replace("doi: ", "")
                            if "doi:" in article.get("elocationid", "")
                            else ""
                        ),
                        "source": "PubMed",
                    }

                    results.append(result)

            return results

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to search PubMed: {str(e)}", "source": "PubMed"}
        except Exception as e:
            return {
                "error": f"Error processing PubMed response: {str(e)}",
                "source": "PubMed",
            }


@register_tool()
class EuropePMCGuidelinesTool(BaseTool):
    """
    Search Europe PMC for clinical guidelines.
    Europe PMC provides access to life science literature including guidelines.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        self.session = requests.Session()

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_europepmc_guidelines(query, limit)

    def _search_europepmc_guidelines(self, query, limit):
        """Search Europe PMC for guideline publications."""
        try:
            # More specific guideline search query
            guideline_query = f'"{query}" AND (guideline OR "practice guideline" OR "clinical guideline" OR recommendation OR "consensus statement")'

            params = {
                "query": guideline_query,
                "format": "json",
                "pageSize": limit * 2,
            }  # Get more to filter

            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            data.get("hitCount", 0)
            results_list = data.get("resultList", {}).get("result", [])

            if not results_list:
                return []

            # Process results with stricter filtering
            results = []
            for result in results_list:
                title = result.get("title", "")
                pub_type = result.get("pubType", "")

                # Get abstract from detailed API call
                abstract = self._get_europepmc_abstract(result.get("pmid", ""))

                # If abstract is too short or just a question, try to get more content
                if len(abstract) < 200 or abstract.endswith("?"):
                    # Try to get full text or more detailed content
                    abstract = self._get_europepmc_full_content(
                        result.get("pmid", ""), result.get("pmcid", "")
                    )

                # More strict guideline detection
                title_lower = title.lower()
                abstract_lower = abstract.lower()

                # Must contain guideline-related keywords in title or abstract
                guideline_keywords = [
                    "guideline",
                    "practice guideline",
                    "clinical guideline",
                    "recommendation",
                    "consensus statement",
                    "position statement",
                    "clinical practice",
                    "best practice",
                ]

                has_guideline_keywords = any(
                    keyword in title_lower or keyword in abstract_lower
                    for keyword in guideline_keywords
                )

                # Exclude research papers and studies
                exclude_keywords = [
                    "study",
                    "trial",
                    "analysis",
                    "evaluation",
                    "assessment",
                    "effectiveness",
                    "efficacy",
                    "outcome",
                    "result",
                    "finding",
                ]

                is_research = any(
                    keyword in title_lower for keyword in exclude_keywords
                )

                # Publication type must confirm guideline nature
                pub_type_tokens = []
                if isinstance(pub_type, str):
                    pub_type_tokens.append(pub_type.lower())

                pub_type_list = result.get("pubTypeList", {}).get("pubType", [])
                if isinstance(pub_type_list, str):
                    pub_type_list = [pub_type_list]

                if isinstance(pub_type_list, list):
                    for entry in pub_type_list:
                        if isinstance(entry, str):
                            pub_type_tokens.append(entry.lower())
                        elif isinstance(entry, dict):
                            label = (
                                entry.get("text")
                                or entry.get("name")
                                or entry.get("value")
                            )
                            if label:
                                pub_type_tokens.append(str(label).lower())

                pub_type_combined = " ".join(pub_type_tokens)

                pub_type_has_guideline = any(
                    term in pub_type_combined
                    for term in [
                        "guideline",
                        "practice guideline",
                        "consensus",
                        "recommendation",
                    ]
                )

                # Determine if it's a guideline
                is_guideline = (
                    has_guideline_keywords
                    and pub_type_has_guideline
                    and not is_research
                    and len(title) > 20
                )

                # Build URL
                pmid = result.get("pmid", "")
                pmcid = result.get("pmcid", "")
                doi = result.get("doi", "")

                url = ""
                if pmid:
                    url = f"https://europepmc.org/article/MED/{pmid}"
                elif pmcid:
                    url = f"https://europepmc.org/article/{pmcid}"
                elif doi:
                    url = f"https://doi.org/{doi}"

                abstract_text = (
                    abstract[:500] + "..." if len(abstract) > 500 else abstract
                )

                # Only add if it's actually a guideline
                if is_guideline:
                    guideline_result = {
                        "title": title,
                        "pmid": pmid,
                        "pmcid": pmcid,
                        "doi": doi,
                        "authors": result.get("authorString", ""),
                        "journal": result.get("journalTitle", ""),
                        "publication_date": result.get("firstPublicationDate", ""),
                        "publication_type": pub_type,
                        "abstract": abstract_text,
                        "content": abstract_text,  # Copy abstract to content field
                        "is_guideline": is_guideline,
                        "url": url,
                        "source": "Europe PMC",
                    }

                    results.append(guideline_result)

                    # Stop when we have enough guidelines
                    if len(results) >= limit:
                        break

            return results

        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to search Europe PMC: {str(e)}",
                "source": "Europe PMC",
            }
        except Exception as e:
            return {
                "error": f"Error processing Europe PMC response: {str(e)}",
                "source": "Europe PMC",
            }

    def _get_europepmc_abstract(self, pmid):
        """Get abstract for a specific PMID using PubMed API."""
        if not pmid:
            return ""

        try:
            # Use PubMed's E-utilities API
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "xml",
                "rettype": "abstract",
            }

            response = self.session.get(base_url, params=params, timeout=15)
            response.raise_for_status()

            # Parse XML response
            import xml.etree.ElementTree as ET

            root = ET.fromstring(response.content)

            # Find abstract text
            abstract_elem = root.find(".//AbstractText")
            if abstract_elem is not None:
                return abstract_elem.text or ""

            # Try alternative path
            abstract_elem = root.find(".//abstract")
            if abstract_elem is not None:
                return abstract_elem.text or ""

            return ""

        except Exception as e:
            return f"Error fetching abstract: {str(e)}"

    def _get_europepmc_full_content(self, pmid, pmcid):
        """Get more detailed content from Europe PMC."""
        if not pmid and not pmcid:
            return ""

        try:
            # Try to get full text from Europe PMC
            if pmcid:
                full_text_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
            else:
                full_text_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/MED/{pmid}/fullTextXML"

            response = self.session.get(full_text_url, timeout=15)
            if response.status_code == 200:
                # Parse XML to extract meaningful content
                import xml.etree.ElementTree as ET

                root = ET.fromstring(response.content)

                # Extract sections that might contain clinical recommendations
                content_parts = []

                # Look for methods, results, conclusions, recommendations
                for section in root.findall(".//sec"):
                    title_elem = section.find("title")
                    if title_elem is not None:
                        title = title_elem.text or ""
                        if any(
                            keyword in title.lower()
                            for keyword in [
                                "recommendation",
                                "conclusion",
                                "method",
                                "result",
                                "guideline",
                                "clinical",
                            ]
                        ):
                            # Extract text from this section
                            text_content = ""
                            for p in section.findall(".//p"):
                                if p.text:
                                    text_content += p.text + " "

                            if text_content.strip():
                                content_parts.append(f"{title}: {text_content.strip()}")

                if content_parts:
                    return " ".join(
                        content_parts[:3]
                    )  # Limit to first 3 relevant sections

            return ""

        except Exception as e:
            return f"Error fetching full content: {str(e)}"


@register_tool()
class TRIPDatabaseTool(BaseTool):
    """
    Search TRIP Database (Turning Research into Practice).
    Specialized evidence-based medicine database with clinical guidelines filter.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.tripdatabase.com/api/search"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)
        search_type = arguments.get("search_type", "guideline")

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_trip_database(query, limit, search_type)

    def _search_trip_database(self, query, limit, search_type):
        """Search TRIP Database for clinical guidelines."""
        try:
            params = {"criteria": query, "searchType": search_type, "limit": limit}

            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)

            total = root.find("total")
            count = root.find("count")

            int(total.text) if total is not None else 0
            int(count.text) if count is not None else 0

            documents = root.findall("document")

            if not documents:
                return []

            # Process results
            results = []
            for doc in documents[:limit]:
                title_elem = doc.find("title")
                link_elem = doc.find("link")
                publication_elem = doc.find("publication")
                category_elem = doc.find("category")
                description_elem = doc.find("description")

                description_text = (
                    description_elem.text if description_elem is not None else ""
                )
                url = link_elem.text if link_elem is not None else ""

                key_recommendations = []
                evidence_strength = []

                fetched_content = None
                requires_detailed_fetch = url and any(
                    domain in url for domain in ["bmj.com/content/", "e-dmj.org"]
                )

                if (not description_text and url) or requires_detailed_fetch:
                    fetched_content = self._fetch_guideline_content(url)

                if isinstance(fetched_content, dict):
                    description_text = (
                        fetched_content.get("content", "") or description_text
                    )
                    key_recommendations = fetched_content.get("key_recommendations", [])
                    evidence_strength = fetched_content.get("evidence_strength", [])
                elif isinstance(fetched_content, str) and fetched_content:
                    description_text = fetched_content

                category_text = (
                    category_elem.text.lower()
                    if category_elem is not None and category_elem.text
                    else ""
                )

                if category_text and "guideline" not in category_text:
                    # Skip clearly non-guideline categories such as news or trials
                    continue

                description_lower = description_text.lower()
                if any(
                    phrase in description_lower
                    for phrase in [
                        "login required",
                        "temporarily unavailable",
                        "subscription required",
                        "no results",
                    ]
                ):
                    continue

                guideline_result = {
                    "title": title_elem.text if title_elem is not None else "",
                    "url": url,
                    "description": description_text,
                    "content": description_text,  # Copy description to content field
                    "publication": (
                        publication_elem.text if publication_elem is not None else ""
                    ),
                    "category": category_elem.text if category_elem is not None else "",
                    "is_guideline": True,  # TRIP returns filtered results
                    "source": "TRIP Database",
                }

                if key_recommendations:
                    guideline_result["key_recommendations"] = key_recommendations
                if evidence_strength:
                    guideline_result["evidence_strength"] = evidence_strength

                results.append(guideline_result)

            return results

        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to search TRIP Database: {str(e)}",
                "source": "TRIP Database",
            }
        except ET.ParseError as e:
            return {
                "error": f"Failed to parse TRIP Database response: {str(e)}",
                "source": "TRIP Database",
            }
        except Exception as e:
            return {
                "error": f"Error processing TRIP Database response: {str(e)}",
                "source": "TRIP Database",
            }

    def _fetch_guideline_content(self, url):
        """Extract content from a guideline URL using targeted parsers when available."""
        try:
            time.sleep(0.5)  # Be respectful

            if "bmj.com/content/" in url:
                return self._extract_bmj_guideline_content(url)

            if "e-dmj.org" in url:
                return self._extract_dmj_guideline_content(url)

            # Fallback: generic MarkItDown extraction
            md = MarkItDown()
            result = md.convert(url)

            if not result or not getattr(result, "text_content", None):
                return f"Content extraction failed. Document available at: {url}"

            content = self._clean_generic_content(result.text_content)
            return content

        except Exception as e:
            return f"Error extracting content: {str(e)}"

    def _clean_generic_content(self, raw_text):
        """Clean generic text content to emphasise clinical lines."""
        content = raw_text.strip()
        content = re.sub(r"\n\s*\n", "\n\n", content)
        content = re.sub(r" +", " ", content)

        meaningful_lines = []
        for line in content.split("\n"):
            line = line.strip()
            if len(line) < 20:
                continue
            if line.count("[") > 0 or line.count("]") > 0:
                continue
            if "http" in line or "//" in line:
                continue

            skip_keywords = [
                "copyright",
                "rights reserved",
                "notice of rights",
                "terms and conditions",
                "your responsibility",
                "local commissioners",
                "environmental impact",
                "medicines and healthcare",
                "yellow card scheme",
                "©",
                "all rights reserved",
            ]
            if any(keyword in line.lower() for keyword in skip_keywords):
                continue

            clinical_keywords = [
                "recommendation",
                "recommendations",
                "should",
                "strong recommendation",
                "conditional recommendation",
                "clinicians",
                "patients",
                "treatment",
                "management",
                "diagnosis",
                "assessment",
                "therapy",
                "intervention",
                "pharmacologic",
                "monitoring",
                "screening",
                "diabetes",
                "glycaemic",
            ]
            if any(keyword in line.lower() for keyword in clinical_keywords):
                meaningful_lines.append(line)

        if meaningful_lines:
            content = "\n".join(meaningful_lines[:8])
        else:
            content = content[:1000]

        if len(content) > 2000:
            truncated = content[:2000]
            last_period = truncated.rfind(".")
            if last_period > 1000:
                content = truncated[: last_period + 1] + "..."
            else:
                content = truncated + "..."

        return content

    def _extract_bmj_guideline_content(self, url):
        """Fetch BMJ Rapid Recommendation content with key recommendations."""
        try:
            md = MarkItDown()
            result = md.convert(url)
            if not result or not getattr(result, "text_content", None):
                return {
                    "content": f"Content extraction failed. Document available at: {url}",
                    "key_recommendations": [],
                    "evidence_strength": [],
                }

            text = result.text_content
            content = self._clean_generic_content(text)

            lines = [line.strip() for line in text.splitlines() if line.strip()]
            recommendations = []
            grading = []
            tokens = [
                "strong recommendation",
                "conditional recommendation",
                "weak recommendation",
                "good practice statement",
            ]

            for idx, line in enumerate(lines):
                lower = line.lower()
                if "recommendation" not in lower:
                    continue
                if len(line) > 180:
                    continue

                title_clean = line.lstrip("#").strip()
                if title_clean.startswith("+"):
                    continue
                if title_clean.lower().startswith("rapid recommendations"):
                    continue

                summary_lines = []
                for following in lines[idx + 1 : idx + 10]:
                    if "recommendation" in following.lower() and len(following) < 180:
                        break
                    if len(following) < 40:
                        continue
                    summary_lines.append(following)
                    if len(summary_lines) >= 3:
                        break

                summary = " ".join(summary_lines)
                if summary:
                    recommendations.append(
                        {"title": title_clean, "summary": summary[:400]}
                    )

                strength = None
                for token in tokens:
                    if token in lower or any(token in s.lower() for s in summary_lines):
                        strength = token.title()
                        break

                if not strength:
                    grade_match = re.search(r"grade\s+[A-D1-9]+", lower)
                    if grade_match:
                        strength = grade_match.group(0).title()

                if strength and not any(
                    entry.get("section") == title_clean for entry in grading
                ):
                    grading.append({"section": title_clean, "strength": strength})

            return {
                "content": content,
                "key_recommendations": recommendations[:5],
                "evidence_strength": grading,
            }

        except Exception as e:
            return {
                "content": f"Error extracting BMJ content: {str(e)}",
                "key_recommendations": [],
                "evidence_strength": [],
            }

    def _extract_dmj_guideline_content(self, url):
        """Fetch Diabetes & Metabolism Journal guideline content and GRADE statements."""
        try:
            md = MarkItDown()
            result = md.convert(url)
            if not result or not getattr(result, "text_content", None):
                return {
                    "content": f"Content extraction failed. Document available at: {url}",
                    "key_recommendations": [],
                    "evidence_strength": [],
                }

            text = result.text_content
            content = self._clean_generic_content(text)

            lines = [line.strip() for line in text.splitlines() if line.strip()]
            recommendations = []
            grading = []

            for idx, line in enumerate(lines):
                lower = line.lower()
                if not any(
                    keyword in lower
                    for keyword in ["recommendation", "statement", "guideline"]
                ):
                    continue
                if len(line) > 200:
                    continue

                title_clean = line.lstrip("#").strip()
                if title_clean.startswith("+") or title_clean.startswith("Table"):
                    continue

                summary_lines = []
                for following in lines[idx + 1 : idx + 10]:
                    if (
                        any(
                            keyword in following.lower()
                            for keyword in ["recommendation", "statement", "guideline"]
                        )
                        and len(following) < 200
                    ):
                        break
                    if len(following) < 30:
                        continue
                    summary_lines.append(following)
                    if len(summary_lines) >= 3:
                        break

                summary = " ".join(summary_lines)
                if summary:
                    recommendations.append(
                        {"title": title_clean, "summary": summary[:400]}
                    )

                strength = None
                grade_match = re.search(r"grade\s+[A-E]\b", lower)
                if grade_match:
                    strength = grade_match.group(0).title()
                level_match = re.search(r"level\s+[0-4]", lower)
                if level_match:
                    level_text = level_match.group(0).title()
                    strength = f"{strength} ({level_text})" if strength else level_text

                for line_text in summary_lines:
                    lower_line = line_text.lower()
                    if "strong" in lower_line and "recommendation" in lower_line:
                        strength = "Strong recommendation"
                        break
                    if "conditional" in lower_line and "recommendation" in lower_line:
                        strength = "Conditional recommendation"
                        break

                if strength and not any(
                    entry.get("section") == title_clean for entry in grading
                ):
                    grading.append({"section": title_clean, "strength": strength})

            return {
                "content": content,
                "key_recommendations": recommendations[:5],
                "evidence_strength": grading,
            }

        except Exception as e:
            return {
                "content": f"Error extracting DMJ content: {str(e)}",
                "key_recommendations": [],
                "evidence_strength": [],
            }


@register_tool()
class WHOGuidelinesTool(BaseTool):
    """
    WHO (World Health Organization) Guidelines Search Tool.
    Searches WHO official guidelines from their publications website.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.who.int"
        self.guidelines_url = f"{self.base_url}/publications/who-guidelines"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_who_guidelines(query, limit)

    def _fetch_guideline_description(self, url):
        """Fetch description from a WHO guideline detail page."""
        try:
            time.sleep(0.5)  # Be respectful
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Try to find overview or description
            overview = soup.find("div", {"class": "overview"}) or soup.find(
                "div", {"class": "description"}
            )
            if overview:
                paragraphs = overview.find_all("p")
                if paragraphs:
                    return " ".join([p.get_text().strip() for p in paragraphs[:2]])

            # Try meta description
            meta_desc = soup.find("meta", {"name": "description"}) or soup.find(
                "meta", {"property": "og:description"}
            )
            if meta_desc and meta_desc.get("content"):
                return meta_desc.get("content")

            # Try first few paragraphs in main content
            main_content = (
                soup.find("div", {"class": "content"})
                or soup.find("main")
                or soup.find("article")
            )
            if main_content:
                paragraphs = main_content.find_all("p", recursive=True)
                if paragraphs:
                    text_parts = []
                    for p in paragraphs[:3]:
                        text = p.get_text().strip()
                        if len(text) > 30:  # Skip very short paragraphs
                            text_parts.append(text)
                        if len(" ".join(text_parts)) > 300:  # Limit total length
                            break
                    if text_parts:
                        return " ".join(text_parts)

            return ""
        except Exception:
            return ""

    def _search_who_guidelines(self, query, limit):
        """Search WHO guidelines by scraping their official website."""
        try:
            # Add delay to be respectful
            time.sleep(1)

            # First, get the guidelines page
            response = self.session.get(self.guidelines_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find all publication links
            all_links = soup.find_all("a", href=True)
            guidelines = []

            query_lower = query.lower()
            query_terms = _extract_meaningful_terms(query)

            for link in all_links:
                href = link["href"]
                text = link.get_text().strip()

                # Filter for actual guideline publications
                if (
                    ("/publications/i/item/" in href or "/publications/m/item/" in href)
                    and text
                    and len(text) > 10
                ):
                    # Check if query matches the title
                    if query_lower in text.lower():
                        full_url = (
                            href if href.startswith("http") else self.base_url + href
                        )

                        # Avoid duplicates
                        if not any(g["url"] == full_url for g in guidelines):
                            # Fetch description from detail page
                            description = self._fetch_guideline_description(full_url)

                            searchable_text = (text + " " + (description or "")).lower()
                            if query_terms and not any(
                                term in searchable_text for term in query_terms
                            ):
                                continue

                            guidelines.append(
                                {
                                    "title": text,
                                    "url": full_url,
                                    "description": description,
                                    "content": description,  # Copy description to content field
                                    "source": "WHO",
                                    "organization": "World Health Organization",
                                    "is_guideline": True,
                                    "official": True,
                                }
                            )

                            if len(guidelines) >= limit:
                                break

            # If no results with strict matching, get all WHO guidelines from page
            if len(guidelines) == 0:
                print(
                    f"No exact matches for '{query}', retrieving latest WHO guidelines..."
                )

                all_guidelines = []
                for link in all_links:
                    href = link["href"]
                    text = link.get_text().strip()

                    if (
                        (
                            "/publications/i/item/" in href
                            or "/publications/m/item/" in href
                        )
                        and text
                        and len(text) > 10
                    ):
                        full_url = (
                            href if href.startswith("http") else self.base_url + href
                        )

                        if not any(g["url"] == full_url for g in all_guidelines):
                            # Fetch description from detail page
                            description = self._fetch_guideline_description(full_url)

                            searchable_text = (text + " " + (description or "")).lower()
                            if query_terms and not any(
                                term in searchable_text for term in query_terms
                            ):
                                continue

                            all_guidelines.append(
                                {
                                    "title": text,
                                    "url": full_url,
                                    "description": description,
                                    "content": description,  # Copy description to content field
                                    "source": "WHO",
                                    "organization": "World Health Organization",
                                    "is_guideline": True,
                                    "official": True,
                                }
                            )

                guidelines = all_guidelines[:limit]

            return guidelines

        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to access WHO guidelines: {str(e)}",
                "source": "WHO",
            }
        except Exception as e:
            return {
                "error": f"Error processing WHO guidelines: {str(e)}",
                "source": "WHO",
            }


@register_tool()
class OpenAlexGuidelinesTool(BaseTool):
    """
    OpenAlex Guidelines Search Tool.
    Specialized tool for searching clinical practice guidelines using OpenAlex API.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://api.openalex.org/works"

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)
        year_from = arguments.get("year_from", None)
        year_to = arguments.get("year_to", None)

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_openalex_guidelines(query, limit, year_from, year_to)

    def _search_openalex_guidelines(self, query, limit, year_from=None, year_to=None):
        """Search for clinical guidelines using OpenAlex API."""
        try:
            # Build search query to focus on guidelines
            search_query = (
                f'"{query}" AND (guideline OR "clinical practice" OR recommendation)'
            )

            # Build parameters
            params = {
                "search": search_query,
                "per_page": min(limit, 50),
                "sort": "cited_by_count:desc",  # Sort by citations
            }

            # Add year filters
            filters = []
            if year_from and year_to:
                filters.append(f"publication_year:{year_from}-{year_to}")
            elif year_from:
                filters.append(f"from_publication_date:{year_from}-01-01")
            elif year_to:
                filters.append(f"to_publication_date:{year_to}-12-31")

            # Filter for articles
            filters.append("type:article")

            if filters:
                params["filter"] = ",".join(filters)

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])
            data.get("meta", {})

            guidelines = []
            for work in results:
                # Extract information
                title = work.get("title", "N/A")
                year = work.get("publication_year", "N/A")
                doi = work.get("doi", "")
                openalex_id = work.get("id", "")
                cited_by = work.get("cited_by_count", 0)

                # Extract authors
                authors = []
                authorships = work.get("authorships", [])
                for authorship in authorships[:5]:
                    author = authorship.get("author", {})
                    author_name = author.get("display_name", "")
                    if author_name:
                        authors.append(author_name)

                # Extract institutions
                institutions = []
                for authorship in authorships[:3]:
                    for inst in authorship.get("institutions", []):
                        inst_name = inst.get("display_name", "")
                        if inst_name and inst_name not in institutions:
                            institutions.append(inst_name)

                # Extract abstract
                abstract_inverted = work.get("abstract_inverted_index", {})
                abstract = (
                    self._reconstruct_abstract(abstract_inverted)
                    if abstract_inverted
                    else None
                )

                # More strict guideline detection
                title_lower = title.lower()
                abstract_lower = abstract.lower() if abstract else ""

                # Must contain specific guideline keywords
                guideline_keywords = [
                    "guideline",
                    "practice guideline",
                    "clinical guideline",
                    "recommendation",
                    "consensus statement",
                    "position statement",
                    "clinical practice",
                    "best practice",
                ]

                has_guideline_keywords = any(
                    keyword in title_lower or keyword in abstract_lower
                    for keyword in guideline_keywords
                )

                # Check structured concepts from OpenAlex for guideline markers
                concepts = work.get("concepts", []) or []
                has_guideline_concept = False
                for concept in concepts:
                    display_name = concept.get("display_name", "").lower()
                    if any(
                        term in display_name
                        for term in [
                            "guideline",
                            "clinical practice",
                            "recommendation",
                            "consensus",
                        ]
                    ):
                        has_guideline_concept = True
                        break

                primary_topic = work.get("primary_topic", {}) or {}
                primary_topic_name = primary_topic.get("display_name", "").lower()
                if any(
                    term in primary_topic_name
                    for term in ["guideline", "clinical practice", "recommendation"]
                ):
                    has_guideline_concept = True

                # Exclude research papers and studies (but be less strict)
                exclude_keywords = [
                    "statistics",
                    "data",
                    "survey",
                    "meta-analysis",
                    "systematic review",
                ]

                is_research = any(
                    keyword in title_lower for keyword in exclude_keywords
                )

                # Determine if it's a guideline
                is_guideline = (
                    has_guideline_keywords
                    and has_guideline_concept
                    and not is_research
                    and len(title) > 20
                )

                # Build URL
                url = (
                    doi
                    if doi and doi.startswith("http")
                    else (
                        f"https://doi.org/{doi.replace('https://doi.org/', '')}"
                        if doi
                        else openalex_id
                    )
                )

                # Only add if it's actually a guideline
                if is_guideline:
                    abstract_text = abstract[:500] if abstract else None
                    guideline = {
                        "title": title,
                        "authors": authors,
                        "institutions": institutions[:3],
                        "year": year,
                        "doi": doi,
                        "url": url,
                        "openalex_id": openalex_id,
                        "cited_by_count": cited_by,
                        "is_guideline": is_guideline,
                        "source": "OpenAlex",
                        "abstract": abstract_text,
                        "content": abstract_text,  # Copy abstract to content field
                    }

                    guidelines.append(guideline)

                    # Stop when we have enough guidelines
                    if len(guidelines) >= limit:
                        break

            return guidelines

        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to search OpenAlex: {str(e)}",
                "source": "OpenAlex",
            }
        except Exception as e:
            return {
                "error": f"Error processing OpenAlex response: {str(e)}",
                "source": "OpenAlex",
            }

    def _reconstruct_abstract(self, abstract_inverted_index):
        """Reconstruct abstract from inverted index."""
        if not abstract_inverted_index:
            return None

        try:
            # Create a list to hold words at their positions
            max_position = max(
                max(positions) for positions in abstract_inverted_index.values()
            )
            words = [""] * (max_position + 1)

            # Place each word at its positions
            for word, positions in abstract_inverted_index.items():
                for pos in positions:
                    words[pos] = word

            # Join words to form abstract
            abstract = " ".join(words).strip()
            return abstract

        except Exception:
            return None


@register_tool()
class NICEGuidelineFullTextTool(BaseTool):
    """
    Fetch full text content from NICE guideline pages.
    Takes a NICE guideline URL and extracts the complete guideline content.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.nice.org.uk"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def run(self, arguments):
        url = arguments.get("url", "")

        if not url:
            return {"error": "URL parameter is required"}

        # Ensure it's a NICE URL
        if "nice.org.uk" not in url:
            return {"error": "URL must be a NICE guideline URL (nice.org.uk)"}

        return self._fetch_full_guideline(url)

    def _fetch_full_guideline(self, url):
        """Fetch complete guideline content from NICE page."""
        try:
            time.sleep(1)  # Be respectful
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title_elem = soup.find("h1") or soup.find("title")
            title = title_elem.get_text().strip() if title_elem else "Unknown Title"

            # Extract guideline metadata
            metadata = {}

            # Published date
            date_elem = soup.find("time") or soup.find(
                "span", {"class": "published-date"}
            )
            if date_elem:
                metadata["published_date"] = date_elem.get_text().strip()

            # Guideline code (e.g., NG28)
            code_match = re.search(r"\(([A-Z]{2,3}\d+)\)", title)
            if code_match:
                metadata["guideline_code"] = code_match.group(1)

            # Extract main content sections
            content_sections = []

            # Find main content div - NICE uses specific structure
            main_content = (
                soup.find("div", {"class": "content"})
                or soup.find("main")
                or soup.find("article")
            )

            if main_content:
                # Extract all headings and their content
                all_headings = main_content.find_all(["h1", "h2", "h3", "h4", "h5"])

                for heading in all_headings:
                    heading_text = heading.get_text().strip()

                    # Find content between this heading and the next
                    content_parts = []
                    current = heading.find_next_sibling()

                    while current and current.name not in [
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "h5",
                    ]:
                        if current.name == "p":
                            text = current.get_text().strip()
                            if text:
                                content_parts.append(text)
                        elif current.name in ["ul", "ol"]:
                            items = current.find_all("li")
                            for li in items:
                                content_parts.append(f"  • {li.get_text().strip()}")
                        elif current.name == "div":
                            # Check if div has paragraphs
                            paras = current.find_all("p", recursive=False)
                            for p in paras:
                                text = p.get_text().strip()
                                if text:
                                    content_parts.append(text)

                        current = current.find_next_sibling()

                    if content_parts:
                        content_sections.append(
                            {
                                "heading": heading_text,
                                "content": "\n\n".join(content_parts),
                            }
                        )

                # If no sections found with headings, extract all paragraphs
                if not content_sections:
                    all_paragraphs = main_content.find_all("p")
                    all_text = "\n\n".join(
                        [
                            p.get_text().strip()
                            for p in all_paragraphs
                            if p.get_text().strip()
                        ]
                    )
                    if all_text:
                        content_sections.append(
                            {"heading": "Content", "content": all_text}
                        )

            # Compile full text
            full_text_parts = []
            for section in content_sections:
                if section["heading"]:
                    full_text_parts.append(f"## {section['heading']}")
                full_text_parts.append(section["content"])

            full_text = "\n\n".join(full_text_parts)

            # Extract recommendations specifically
            recommendations = []
            rec_sections = soup.find_all(
                ["div", "section"], class_=re.compile(r"recommendation")
            )
            for rec in rec_sections[:20]:  # Limit to first 20 recommendations
                rec_text = rec.get_text().strip()
                if rec_text and len(rec_text) > 20:
                    recommendations.append(rec_text)

            return {
                "url": url,
                "title": title,
                "metadata": metadata,
                "full_text": full_text,
                "full_text_length": len(full_text),
                "sections_count": len(content_sections),
                "recommendations": recommendations[:20] if recommendations else None,
                "recommendations_count": len(recommendations) if recommendations else 0,
                "source": "NICE",
                "content_type": "full_guideline",
                "success": len(full_text) > 500,
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch NICE guideline: {str(e)}", "url": url}
        except Exception as e:
            return {"error": f"Error parsing NICE guideline: {str(e)}", "url": url}


@register_tool()
class WHOGuidelineFullTextTool(BaseTool):
    """
    Fetch full text content from WHO guideline pages.
    Takes a WHO publication URL and extracts content or PDF download link.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.who.int"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def run(self, arguments):
        url = arguments.get("url", "")

        if not url:
            return {"error": "URL parameter is required"}

        # Ensure it's a WHO URL
        if "who.int" not in url:
            return {"error": "URL must be a WHO publication URL (who.int)"}

        return self._fetch_who_guideline(url)

    def _fetch_who_guideline(self, url):
        """Fetch WHO guideline content and PDF link."""
        try:
            time.sleep(1)  # Be respectful
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title_elem = soup.find("h1") or soup.find("title")
            title = title_elem.get_text().strip() if title_elem else "Unknown Title"

            # Extract metadata
            metadata = {}

            # Publication date
            date_elem = soup.find("time") or soup.find(
                "span", class_=re.compile(r"date")
            )
            if date_elem:
                metadata["published_date"] = date_elem.get_text().strip()

            # ISBN
            isbn_elem = soup.find(text=re.compile(r"ISBN"))
            if isbn_elem:
                isbn_match = re.search(r"ISBN[:\s]*([\d\-]+)", isbn_elem)
                if isbn_match:
                    metadata["isbn"] = isbn_match.group(1)

            # Find PDF download link
            pdf_link = None
            pdf_links = soup.find_all("a", href=re.compile(r"\.pdf$", re.I))

            for link in pdf_links:
                href = link.get("href", "")
                if href:
                    # Make absolute URL
                    if href.startswith("http"):
                        pdf_link = href
                    elif href.startswith("//"):
                        pdf_link = "https:" + href
                    elif href.startswith("/"):
                        pdf_link = self.base_url + href
                    else:
                        pdf_link = self.base_url + "/" + href

                    # Prefer full document over excerpts
                    link_text = link.get_text().lower()
                    if "full" in link_text or "complete" in link_text:
                        break

            # Extract overview/description
            overview = ""
            overview_section = soup.find(
                "div", class_=re.compile(r"overview|description|summary")
            ) or soup.find(
                "section", class_=re.compile(r"overview|description|summary")
            )

            if overview_section:
                paragraphs = overview_section.find_all("p")
                overview = "\n\n".join(
                    [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
                )

            # Extract key facts/highlights
            key_facts = []
            facts_section = soup.find(
                ["div", "section"], class_=re.compile(r"key.*facts|highlights")
            )
            if facts_section:
                items = facts_section.find_all("li")
                key_facts = [
                    li.get_text().strip() for li in items if li.get_text().strip()
                ]

            # Try to extract main content
            main_content = ""
            content_div = (
                soup.find("div", {"class": "content"})
                or soup.find("main")
                or soup.find("article")
            )

            if content_div:
                # Get all paragraphs
                paragraphs = content_div.find_all("p")
                content_parts = []
                for p in paragraphs[:50]:  # Limit to avoid too much content
                    text = p.get_text().strip()
                    if len(text) > 30:  # Skip very short paragraphs
                        content_parts.append(text)

                main_content = "\n\n".join(content_parts)

            return {
                "url": url,
                "title": title,
                "metadata": metadata,
                "overview": overview,
                "main_content": main_content,
                "content_length": len(main_content),
                "key_facts": key_facts if key_facts else None,
                "pdf_download_url": pdf_link,
                "has_pdf": pdf_link is not None,
                "source": "WHO",
                "content_type": "guideline_page",
                "success": len(overview) > 100 or pdf_link is not None,
                "note": (
                    "Full text available as PDF download"
                    if pdf_link
                    else "Limited web content available"
                ),
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch WHO guideline: {str(e)}", "url": url}
        except Exception as e:
            return {"error": f"Error parsing WHO guideline: {str(e)}", "url": url}


@register_tool()
class GINGuidelinesTool(BaseTool):
    """
    Guidelines International Network (GIN) Guidelines Search Tool.
    Searches the global guidelines database with 6400+ guidelines from various organizations.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.g-i-n.net"
        self.search_url = f"{self.base_url}/library/international-guidelines-library"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_gin_guidelines(query, limit)

    def _search_gin_guidelines(self, query, limit):
        """Search GIN guidelines using web scraping."""
        try:
            time.sleep(1)  # Be respectful

            # Try to search GIN guidelines
            try:
                # GIN search typically uses form parameters
                search_params = {"search": query, "type": "guideline", "limit": limit}

                response = self.session.get(
                    self.search_url, params=search_params, timeout=30
                )
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")

                # Find guideline results - common selectors for guideline databases
                guidelines = []

                # Try different selectors for guideline results
                result_selectors = [
                    "div.guideline-item",
                    "div.search-result",
                    "div.result-item",
                    "article.guideline",
                    "div.item",
                    "li.guideline",
                ]

                results = []
                for selector in result_selectors:
                    results = soup.select(selector)
                    if results:
                        break

                if not results:
                    # Fallback: look for any div with guideline-related content
                    results = soup.find_all(
                        "div",
                        class_=lambda x: x
                        and any(
                            keyword in x.lower()
                            for keyword in ["guideline", "result", "item", "card"]
                        ),
                    )

                for result in results[:limit]:
                    try:
                        # Extract title
                        title_elem = (
                            result.find("h3")
                            or result.find("h2")
                            or result.find("a", class_="title")
                            or result.find("a")
                        )
                        if not title_elem:
                            continue

                        title = title_elem.get_text().strip()
                        if not title or len(title) < 10:
                            continue

                        # Extract URL
                        link_elem = result.find("a", href=True)
                        if not link_elem:
                            continue

                        url = link_elem.get("href", "")
                        if url.startswith("/"):
                            url = self.base_url + url
                        elif not url.startswith("http"):
                            continue

                        # Extract description/summary
                        desc_elem = (
                            result.find("p")
                            or result.find("div", class_="description")
                            or result.find("div", class_="summary")
                        )
                        description = desc_elem.get_text().strip() if desc_elem else ""

                        # Extract organization
                        org_elem = (
                            result.find("span", class_="organization")
                            or result.find("div", class_="org")
                            or result.find("cite")
                        )
                        organization = (
                            org_elem.get_text().strip()
                            if org_elem
                            else "GIN Member Organization"
                        )

                        # Extract date
                        date_elem = (
                            result.find("time")
                            or result.find("span", class_="date")
                            or result.find("div", class_="date")
                        )
                        date = date_elem.get_text().strip() if date_elem else ""

                        # Extract content from the guideline page
                        content = self._extract_guideline_content(url)

                        guidelines.append(
                            {
                                "title": title,
                                "url": url,
                                "description": description,
                                "content": content,
                                "date": date,
                                "source": "GIN",
                                "organization": organization,
                                "is_guideline": True,
                                "official": True,
                            }
                        )

                    except Exception:
                        continue

                if guidelines:
                    return guidelines

            except requests.exceptions.RequestException as e:
                print(f"GIN website access failed: {e}, trying fallback search...")

            # Fallback: Return sample guidelines based on query
            return self._get_fallback_gin_guidelines(query, limit)

        except Exception as e:
            return {
                "error": f"Error processing GIN guidelines: {str(e)}",
                "source": "GIN",
            }

    def _get_fallback_gin_guidelines(self, query, limit):
        """Provide fallback guidelines when direct access fails."""
        # This would contain sample guidelines based on common queries
        # For now, return a message indicating the issue
        return [
            {
                "title": f"GIN Guidelines Search for '{query}'",
                "url": self.search_url,
                "description": "GIN guidelines database access temporarily unavailable. Please try again later or visit the GIN website directly.",
                "content": "The Guidelines International Network (GIN) maintains the world's largest database of clinical guidelines with over 6400 guidelines from various organizations worldwide.",
                "date": "",
                "source": "GIN",
                "organization": "Guidelines International Network",
                "is_guideline": False,
                "official": True,
                "is_placeholder": True,
                "note": "Direct access to GIN database failed. Please visit g-i-n.net for full access.",
            }
        ]

    def _extract_guideline_content(self, url):
        """Extract actual content from a guideline URL."""
        try:
            time.sleep(0.5)  # Be respectful
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract main content
            content_selectors = [
                "main",
                ".content",
                ".article-content",
                ".guideline-content",
                "article",
                ".main-content",
            ]

            content_text = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Get all text content
                    paragraphs = content_elem.find_all("p")
                    content_parts = []
                    for p in paragraphs:
                        text = p.get_text().strip()
                        if len(text) > 20:  # Skip very short paragraphs
                            content_parts.append(text)

                    if content_parts:
                        content_text = "\n\n".join(
                            content_parts[:10]
                        )  # Limit to first 10 paragraphs
                        break

            # If no main content found, try to get any meaningful text
            if not content_text:
                all_text = soup.get_text()
                # Clean up the text
                lines = [line.strip() for line in all_text.split("\n") if line.strip()]
                content_text = "\n".join(lines[:20])  # First 20 meaningful lines

            return content_text[:2000]  # Limit content length

        except Exception as e:
            return f"Error extracting content: {str(e)}"


@register_tool()
class CMAGuidelinesTool(BaseTool):
    """
    Canadian Medical Association (CMA) Infobase Guidelines Search Tool.
    Searches the CMA Infobase with 1200+ Canadian clinical practice guidelines.
    """

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://joulecma.ca"
        self.search_url = f"{self.base_url}/infobase"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def run(self, arguments):
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)

        if not query:
            return {"error": "Query parameter is required"}

        return self._search_cma_guidelines(query, limit)

    def _search_cma_guidelines(self, query, limit):
        """Search CMA Infobase guidelines using web scraping."""
        try:
            time.sleep(1)  # Be respectful

            # Try to search CMA Infobase
            try:
                # CMA search typically uses form parameters
                search_params = {"search": query, "type": "guideline", "limit": limit}

                response = self.session.get(
                    self.search_url, params=search_params, timeout=30
                )
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")

                # Find guideline results
                guidelines = []

                # Try different selectors for guideline results
                result_selectors = [
                    "div.guideline-item",
                    "div.search-result",
                    "div.result-item",
                    "article.guideline",
                    "div.item",
                    "li.guideline",
                ]

                results = []
                for selector in result_selectors:
                    results = soup.select(selector)
                    if results:
                        break

                if not results:
                    # Fallback: look for any div with guideline-related content
                    results = soup.find_all(
                        "div",
                        class_=lambda x: x
                        and any(
                            keyword in x.lower()
                            for keyword in ["guideline", "result", "item", "card"]
                        ),
                    )

                for result in results[:limit]:
                    try:
                        # Extract title
                        title_elem = (
                            result.find("h3")
                            or result.find("h2")
                            or result.find("a", class_="title")
                            or result.find("a")
                        )
                        if not title_elem:
                            continue

                        title = title_elem.get_text().strip()
                        if not title or len(title) < 10:
                            continue

                        # Extract URL
                        link_elem = result.find("a", href=True)
                        if not link_elem:
                            continue

                        url = link_elem.get("href", "")
                        if url.startswith("/"):
                            url = self.base_url + url
                        elif not url.startswith("http"):
                            continue

                        # Extract description/summary
                        desc_elem = (
                            result.find("p")
                            or result.find("div", class_="description")
                            or result.find("div", class_="summary")
                        )
                        description = desc_elem.get_text().strip() if desc_elem else ""

                        # Extract organization
                        org_elem = (
                            result.find("span", class_="organization")
                            or result.find("div", class_="org")
                            or result.find("cite")
                        )
                        organization = (
                            org_elem.get_text().strip()
                            if org_elem
                            else "Canadian Medical Association"
                        )

                        # Extract date
                        date_elem = (
                            result.find("time")
                            or result.find("span", class_="date")
                            or result.find("div", class_="date")
                        )
                        date = date_elem.get_text().strip() if date_elem else ""

                        # Extract content from the guideline page
                        content = self._extract_guideline_content(url)

                        guidelines.append(
                            {
                                "title": title,
                                "url": url,
                                "description": description,
                                "content": content,
                                "date": date,
                                "source": "CMA",
                                "organization": organization,
                                "is_guideline": True,
                                "official": True,
                            }
                        )

                    except Exception:
                        continue

                if guidelines:
                    return guidelines

            except requests.exceptions.RequestException as e:
                print(f"CMA Infobase access failed: {e}, trying fallback search...")

            # Fallback: Return sample guidelines based on query
            return self._get_fallback_cma_guidelines(query, limit)

        except Exception as e:
            return {
                "error": f"Error processing CMA guidelines: {str(e)}",
                "source": "CMA",
            }

    def _get_fallback_cma_guidelines(self, query, limit):
        """Provide fallback guidelines when direct access fails."""
        # This would contain sample guidelines based on common queries
        # For now, return a message indicating the issue
        return [
            {
                "title": f"CMA Infobase Guidelines Search for '{query}'",
                "url": self.search_url,
                "description": "CMA Infobase access temporarily unavailable. Please try again later or visit the CMA website directly.",
                "content": "The Canadian Medical Association Infobase contains over 1200 evidence-based clinical practice guidelines developed or endorsed by Canadian healthcare organizations.",
                "date": "",
                "source": "CMA",
                "organization": "Canadian Medical Association",
                "is_guideline": False,
                "official": True,
                "is_placeholder": True,
                "note": "Direct access to CMA Infobase failed. Please visit joulecma.ca/infobase for full access.",
            }
        ]

    def _extract_guideline_content(self, url):
        """Extract actual content from a guideline URL."""
        try:
            time.sleep(0.5)  # Be respectful
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract main content
            content_selectors = [
                "main",
                ".content",
                ".article-content",
                ".guideline-content",
                "article",
                ".main-content",
            ]

            content_text = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Get all text content
                    paragraphs = content_elem.find_all("p")
                    content_parts = []
                    for p in paragraphs:
                        text = p.get_text().strip()
                        if len(text) > 20:  # Skip very short paragraphs
                            content_parts.append(text)

                    if content_parts:
                        content_text = "\n\n".join(
                            content_parts[:10]
                        )  # Limit to first 10 paragraphs
                        break

            # If no main content found, try to get any meaningful text
            if not content_text:
                all_text = soup.get_text()
                # Clean up the text
                lines = [line.strip() for line in all_text.split("\n") if line.strip()]
                content_text = "\n".join(lines[:20])  # First 20 meaningful lines

            return content_text[:2000]  # Limit content length

        except Exception as e:
            return f"Error extracting content: {str(e)}"
