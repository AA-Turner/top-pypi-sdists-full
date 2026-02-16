# mouser_tool.py
"""
Mouser Electronics REST API tool for ToolUniverse.

Mouser is one of the world's largest distributors of electronic components,
offering over 1 million products from 1,200+ manufacturers. The API provides
part search, pricing, availability, and technical specifications.

API Documentation: https://api.mouser.com/api/docs/ui/index
Registration: https://www.mouser.com/api-search/ (free API key)

Authentication: Requires a free Search API key from Mouser.
- Register at https://www.mouser.com/api-search/
- Set the MOUSER_API_KEY environment variable with your Search API key
Rate limits: 30 requests/minute, 1000 requests/day
"""

import os
import requests
from typing import Dict, Any, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool

# Mouser API base URLs - v1 for basic search, v2 for enhanced search
MOUSER_API_V1 = "https://api.mouser.com/api/v1"
MOUSER_API_V2 = "https://api.mouser.com/api/v2"


@register_tool("MouserTool")
class MouserTool(BaseTool):
    """
    Tool for searching electronic components via the Mouser Electronics API.

    Mouser provides comprehensive electronic component data including:
    - Part search by keyword or manufacturer part number
    - Real-time pricing with volume breaks
    - Stock availability and lead times
    - Technical specifications and datasheets
    - Manufacturer information

    Authentication: Requires a free API key from Mouser.
    Register at: https://www.mouser.com/api-search/
    Set MOUSER_API_KEY environment variable with your key.
    Rate limits: 30 req/min, 1000 req/day.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.operation = fields.get("operation", "keyword_search")
        self.api_version = fields.get("api_version", "v1")
        # API key from environment variable
        self.api_key = os.environ.get("MOUSER_API_KEY", "")

    def _get_api_key(self, arguments: Dict[str, Any]) -> str:
        """Get API key from arguments or environment."""
        key = arguments.get("api_key") or self.api_key
        if not key:
            raise ValueError(
                "Mouser API key is required. Set MOUSER_API_KEY environment variable "
                "or pass 'api_key' parameter. Register for a free key at: "
                "https://www.mouser.com/api-search/"
            )
        return key

    def _get_base_url(self) -> str:
        """Get the base URL for the configured API version."""
        if self.api_version == "v2":
            return MOUSER_API_V2
        return MOUSER_API_V1

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Mouser API call based on the configured operation."""
        try:
            api_key = self._get_api_key(arguments)
        except ValueError as e:
            return {"error": str(e)}

        try:
            if self.operation == "keyword_search":
                return self._keyword_search(arguments, api_key)
            elif self.operation == "partnumber_search":
                return self._partnumber_search(arguments, api_key)
            elif self.operation == "keyword_manufacturer_search":
                return self._keyword_manufacturer_search(arguments, api_key)
            elif self.operation == "partnumber_manufacturer_search":
                return self._partnumber_manufacturer_search(arguments, api_key)
            else:
                return {"error": f"Unknown operation: {self.operation}"}
        except requests.exceptions.Timeout:
            return {
                "error": f"Mouser API request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Failed to connect to Mouser API. Check network connectivity."
            }
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "unknown"
            if status_code == 429:
                return {
                    "error": "Mouser API rate limit exceeded (30 req/min or 1000 req/day). Try again later."
                }
            return {"error": f"Mouser API HTTP error {status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error querying Mouser: {str(e)}"}

    def _make_post_request(self, endpoint: str, body: Dict, api_key: str) -> Dict:
        """Make a POST request to Mouser API."""
        base_url = self._get_base_url()
        url = f"{base_url}/{endpoint}?apiKey={api_key}"
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        response = requests.post(url, json=body, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _parse_parts(self, raw_data: Dict) -> Dict[str, Any]:
        """Parse Mouser API response into standardized format."""
        errors = raw_data.get("Errors", [])
        if errors:
            error_msgs = [e.get("Message", "Unknown error") for e in errors]
            # Check for auth errors specifically
            for e in errors:
                code = e.get("Code", "")
                prop = e.get("PropertyName", "")
                # v1 returns "Invalid" for "API Key", v2 returns "Required" for "Request"
                if (code == "Invalid" and "API Key" in prop) or (
                    code == "Required" and prop == "Request"
                ):
                    return {
                        "error": "Invalid Mouser API key. Register for a free key at: https://www.mouser.com/api-search/"
                    }
            return {"error": "; ".join(error_msgs)}

        search_results = raw_data.get("SearchResults", {})
        if search_results is None:
            return {
                "data": [],
                "metadata": {
                    "source": "Mouser Electronics",
                    "total_results": 0,
                },
            }

        raw_parts = search_results.get("Parts", [])
        parts = []
        for p in raw_parts:
            part = {
                "mouser_part_number": p.get("MouserPartNumber", ""),
                "manufacturer_part_number": p.get("ManufacturerPartNumber", ""),
                "manufacturer": p.get("Manufacturer", ""),
                "description": p.get("Description", ""),
                "availability": p.get("Availability", ""),
                "lifecycle": p.get("LifecycleStatus", ""),
                "datasheet_url": p.get("DataSheetUrl", ""),
                "product_detail_url": p.get("ProductDetailUrl", ""),
                "category": p.get("Category", ""),
                "image_path": p.get("ImagePath", ""),
                "min_order_qty": p.get("Min", ""),
                "mult_order_qty": p.get("Mult", ""),
                "lead_time": p.get("LeadTime", ""),
                "roi_status": p.get("ROHSStatus", ""),
            }

            # Parse price breaks
            price_breaks = []
            for pb in p.get("PriceBreaks", []):
                price_breaks.append(
                    {
                        "quantity": pb.get("Quantity", 0),
                        "price": pb.get("Price", ""),
                        "currency": pb.get("Currency", "USD"),
                    }
                )
            part["price_breaks"] = price_breaks

            # Parse product attributes (specs)
            attributes = []
            for attr in p.get("ProductAttributes", []):
                attributes.append(
                    {
                        "name": attr.get("AttributeName", ""),
                        "value": attr.get("AttributeValue", ""),
                    }
                )
            part["attributes"] = attributes

            parts.append(part)

        return {
            "data": parts,
            "metadata": {
                "source": "Mouser Electronics",
                "total_results": search_results.get("NumberOfResult", len(parts)),
            },
        }

    def _keyword_search(
        self, arguments: Dict[str, Any], api_key: str
    ) -> Dict[str, Any]:
        """Search components by keyword."""
        keyword = arguments.get("keyword", "")
        if not keyword:
            return {"error": "keyword parameter is required"}

        records = arguments.get("records", 10)
        starting_record = arguments.get("starting_record", 0)
        search_options = arguments.get("search_options", "")

        body = {
            "SearchByKeywordRequest": {
                "keyword": keyword,
                "records": min(int(records), 50),
                "startingRecord": int(starting_record),
                "searchOptions": search_options,
                "searchWithYourSignUpLanguage": "",
            }
        }

        raw_data = self._make_post_request("search/keyword", body, api_key)
        result = self._parse_parts(raw_data)
        if "metadata" in result:
            result["metadata"]["query"] = keyword
            result["metadata"]["endpoint"] = "keyword_search"
        return result

    def _partnumber_search(
        self, arguments: Dict[str, Any], api_key: str
    ) -> Dict[str, Any]:
        """Search components by part number."""
        part_number = arguments.get("part_number", "")
        if not part_number:
            return {"error": "part_number parameter is required"}

        search_option = arguments.get("search_option", "")

        body = {
            "SearchByPartRequest": {
                "mouserPartNumber": part_number,
                "partSearchOptions": search_option,
            }
        }

        raw_data = self._make_post_request("search/partnumber", body, api_key)
        result = self._parse_parts(raw_data)
        if "metadata" in result:
            result["metadata"]["query"] = part_number
            result["metadata"]["endpoint"] = "partnumber_search"
        return result

    def _keyword_manufacturer_search(
        self, arguments: Dict[str, Any], api_key: str
    ) -> Dict[str, Any]:
        """Search by keyword filtered to a specific manufacturer."""
        keyword = arguments.get("keyword", "")
        manufacturer = arguments.get("manufacturer", "")
        if not keyword:
            return {"error": "keyword parameter is required"}
        if not manufacturer:
            return {"error": "manufacturer parameter is required"}

        records = arguments.get("records", 10)
        starting_record = arguments.get("starting_record", 0)
        search_options = arguments.get("search_options", "")

        body = {
            "SearchByKeywordMfrRequest": {
                "keyword": keyword,
                "manufacturerName": manufacturer,
                "records": min(int(records), 50),
                "startingRecord": int(starting_record),
                "searchOptions": search_options,
                "searchWithYourSignUpLanguage": "",
            }
        }

        raw_data = self._make_post_request(
            "search/keywordandmanufacturer", body, api_key
        )
        result = self._parse_parts(raw_data)
        if "metadata" in result:
            result["metadata"]["query"] = keyword
            result["metadata"]["manufacturer_filter"] = manufacturer
            result["metadata"]["endpoint"] = "keyword_manufacturer_search"
        return result

    def _partnumber_manufacturer_search(
        self, arguments: Dict[str, Any], api_key: str
    ) -> Dict[str, Any]:
        """Search by part number filtered to a specific manufacturer."""
        part_number = arguments.get("part_number", "")
        manufacturer = arguments.get("manufacturer", "")
        if not part_number:
            return {"error": "part_number parameter is required"}
        if not manufacturer:
            return {"error": "manufacturer parameter is required"}

        records = arguments.get("records", 10)
        starting_record = arguments.get("starting_record", 0)
        search_option = arguments.get("search_option", "")

        body = {
            "SearchByPartMfrRequest": {
                "mouserPartNumber": part_number,
                "manufacturerName": manufacturer,
                "records": min(int(records), 50),
                "startingRecord": int(starting_record),
                "partSearchOptions": search_option,
            }
        }

        raw_data = self._make_post_request(
            "search/partnumberandmanufacturer", body, api_key
        )
        result = self._parse_parts(raw_data)
        if "metadata" in result:
            result["metadata"]["query"] = part_number
            result["metadata"]["manufacturer_filter"] = manufacturer
            result["metadata"]["endpoint"] = "partnumber_manufacturer_search"
        return result
