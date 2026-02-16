# digikey_tool.py
"""
Digi-Key Electronics REST API tool for ToolUniverse.

Digi-Key is one of the world's largest electronic component distributors,
offering millions of products. The Product Information API v4 provides
keyword search, part detail lookup, categories, and manufacturer data.

API Documentation: https://developer.digikey.com/documentation
Registration: https://developer.digikey.com/ (free developer account)

Authentication: OAuth 2.0 (2-legged client credentials flow).
- Register at https://developer.digikey.com/
- Create an application to get Client ID and Client Secret
- Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET environment variables
Rate limits: 120 requests/minute, 1000 requests/day
Token lifetime: 10 minutes (auto-refreshed)
"""

import os
import time
import requests
from typing import Dict, Any, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool

# Digi-Key API endpoints
DIGIKEY_TOKEN_URL = "https://api.digikey.com/v1/oauth2/token"
DIGIKEY_API_BASE = "https://api.digikey.com/products/v4"

# Token cache (shared across instances for efficiency)
_token_cache: Dict[str, Any] = {
    "access_token": None,
    "expires_at": 0,
}


@register_tool("DigiKeyTool")
class DigiKeyTool(BaseTool):
    """
    Tool for searching electronic components via the Digi-Key Electronics API.

    Digi-Key provides comprehensive electronic component data including:
    - Product search by keyword or Digi-Key part number
    - Detailed product specifications and parameters
    - Real-time pricing with volume breaks
    - Stock availability and packaging options
    - Manufacturer and category information

    Authentication: OAuth 2.0 client credentials (free registration).
    Register at: https://developer.digikey.com/
    Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET environment variables.
    Rate limits: 120 req/min, 1000 req/day.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.operation = fields.get("operation", "keyword_search")
        # OAuth2 credentials from environment
        self.client_id = os.environ.get("DIGIKEY_CLIENT_ID", "")
        self.client_secret = os.environ.get("DIGIKEY_CLIENT_SECRET", "")

    def _get_credentials(self, arguments: Dict[str, Any]) -> tuple:
        """Get OAuth2 credentials from arguments or environment."""
        client_id = arguments.get("client_id") or self.client_id
        client_secret = arguments.get("client_secret") or self.client_secret

        if not client_id or not client_secret:
            raise ValueError(
                "Digi-Key API credentials required. Set DIGIKEY_CLIENT_ID and "
                "DIGIKEY_CLIENT_SECRET environment variables. Register for free at: "
                "https://developer.digikey.com/"
            )
        return client_id, client_secret

    def _get_access_token(self, client_id: str, client_secret: str) -> str:
        """Get OAuth2 access token, using cache if still valid."""
        global _token_cache

        # Check if cached token is still valid (with 30s buffer)
        if (
            _token_cache["access_token"]
            and time.time() < _token_cache["expires_at"] - 30
        ):
            return _token_cache["access_token"]

        # Request new token
        response = requests.post(
            DIGIKEY_TOKEN_URL,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=self.timeout,
        )

        if response.status_code == 401:
            raise ValueError(
                "Invalid Digi-Key API credentials. Verify your DIGIKEY_CLIENT_ID "
                "and DIGIKEY_CLIENT_SECRET. Register at: https://developer.digikey.com/"
            )

        response.raise_for_status()
        token_data = response.json()

        # Cache the token
        _token_cache["access_token"] = token_data["access_token"]
        _token_cache["expires_at"] = time.time() + token_data.get("expires_in", 600)

        return token_data["access_token"]

    def _make_api_request(
        self,
        method: str,
        endpoint: str,
        client_id: str,
        access_token: str,
        json_body: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict:
        """Make an authenticated request to Digi-Key API."""
        url = f"{DIGIKEY_API_BASE}/{endpoint}"
        headers = {
            "X-DIGIKEY-Client-Id": client_id,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if method.upper() == "POST":
            response = requests.post(
                url,
                json=json_body,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
        else:
            response = requests.get(
                url, headers=headers, params=params, timeout=self.timeout
            )

        response.raise_for_status()
        return response.json()

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Digi-Key API call based on the configured operation."""
        try:
            client_id, client_secret = self._get_credentials(arguments)
        except ValueError as e:
            return {"error": str(e)}

        try:
            access_token = self._get_access_token(client_id, client_secret)
        except ValueError as e:
            return {"error": str(e)}
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to obtain Digi-Key access token: {str(e)}"}

        try:
            if self.operation == "keyword_search":
                return self._keyword_search(arguments, client_id, access_token)
            elif self.operation == "product_details":
                return self._product_details(arguments, client_id, access_token)
            elif self.operation == "categories":
                return self._get_categories(arguments, client_id, access_token)
            elif self.operation == "manufacturers":
                return self._get_manufacturers(arguments, client_id, access_token)
            else:
                return {"error": f"Unknown operation: {self.operation}"}
        except requests.exceptions.Timeout:
            return {
                "error": f"Digi-Key API request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Failed to connect to Digi-Key API. Check network connectivity."
            }
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "unknown"
            detail = ""
            if e.response is not None:
                try:
                    err_json = e.response.json()
                    detail = err_json.get("detail", err_json.get("ErrorMessage", ""))
                except Exception:
                    detail = e.response.text[:200]
            if status_code == 401:
                # Clear token cache on auth failure
                _token_cache["access_token"] = None
                _token_cache["expires_at"] = 0
                return {
                    "error": "Digi-Key authentication failed. Token may have expired. Try again."
                }
            elif status_code == 429:
                return {
                    "error": "Digi-Key API rate limit exceeded (120 req/min or 1000 req/day). Try again later."
                }
            return {"error": f"Digi-Key API HTTP error {status_code}: {detail}"}
        except Exception as e:
            return {"error": f"Unexpected error querying Digi-Key: {str(e)}"}

    def _parse_product(self, p: Dict) -> Dict[str, Any]:
        """Parse a single product from Digi-Key API response."""
        product = {
            "digikey_part_number": p.get("DigiKeyPartNumber", ""),
            "manufacturer_part_number": p.get("ManufacturerPartNumber", ""),
            "manufacturer": p.get("Manufacturer", {}).get("Name", ""),
            "description": p.get("Description", {}).get("ProductDescription", "")
            if isinstance(p.get("Description"), dict)
            else p.get("ProductDescription", p.get("Description", "")),
            "detailed_description": p.get("Description", {}).get(
                "DetailedDescription", ""
            )
            if isinstance(p.get("Description"), dict)
            else "",
            "quantity_available": p.get("QuantityAvailable", 0),
            "unit_price": p.get("UnitPrice", 0),
            "product_url": p.get("ProductUrl", ""),
            "datasheet_url": p.get("DatasheetUrl", p.get("PrimaryDatasheet", "")),
            "photo_url": p.get("PhotoUrl", p.get("PrimaryPhoto", "")),
            "category": p.get("Category", {}).get("Name", "")
            if isinstance(p.get("Category"), dict)
            else "",
            "family": p.get("Family", {}).get("Name", "")
            if isinstance(p.get("Family"), dict)
            else "",
            "series": p.get("Series", {}).get("Name", "")
            if isinstance(p.get("Series"), dict)
            else "",
            "packaging": p.get("Packaging", {}).get("Name", "")
            if isinstance(p.get("Packaging"), dict)
            else "",
            "product_status": p.get("ProductStatus", {}).get("Status", "")
            if isinstance(p.get("ProductStatus"), dict)
            else p.get("ProductStatus", ""),
            "min_order_quantity": p.get("MinimumOrderQuantity", 0),
        }

        # Parse standard pricing
        pricing = []
        for pb in p.get("StandardPricing", p.get("PriceBreaks", [])) or []:
            pricing.append(
                {
                    "break_quantity": pb.get("BreakQuantity", 0),
                    "unit_price": pb.get("UnitPrice", 0),
                    "total_price": pb.get("TotalPrice", 0),
                }
            )
        product["pricing"] = pricing

        # Parse parameters/specifications
        parameters = []
        for param in p.get("Parameters", []) or []:
            parameters.append(
                {
                    "name": param.get("ParameterText", param.get("Parameter", "")),
                    "value": param.get("ValueText", param.get("Value", "")),
                }
            )
        product["parameters"] = parameters

        return product

    def _keyword_search(
        self, arguments: Dict[str, Any], client_id: str, access_token: str
    ) -> Dict[str, Any]:
        """Search products by keyword."""
        keywords = arguments.get("keywords", "")
        if not keywords:
            return {"error": "keywords parameter is required"}

        body = {
            "Keywords": keywords,
        }

        # Optional filters
        limit = arguments.get("limit")
        if limit:
            body["RecordCount"] = min(int(limit), 50)

        offset = arguments.get("offset")
        if offset:
            body["RecordStartPosition"] = int(offset)

        # Sort
        sort_by = arguments.get("sort_by")
        if sort_by:
            body["SortOptions"] = {
                "Field": sort_by,
                "SortOrder": arguments.get("sort_order", "Ascending"),
            }

        raw_data = self._make_api_request(
            "POST", "search/keyword", client_id, access_token, json_body=body
        )

        # Parse products
        products = []
        for p in raw_data.get("Products", raw_data.get("ExactMatches", [])) or []:
            products.append(self._parse_product(p))

        return {
            "data": products,
            "metadata": {
                "source": "Digi-Key Electronics",
                "endpoint": "keyword_search",
                "query": keywords,
                "total_results": raw_data.get(
                    "ProductsCount",
                    raw_data.get("ExactManufacturerProductsCount", len(products)),
                ),
                "results_returned": len(products),
            },
        }

    def _product_details(
        self, arguments: Dict[str, Any], client_id: str, access_token: str
    ) -> Dict[str, Any]:
        """Get detailed product information by part number."""
        product_number = arguments.get("product_number", "")
        if not product_number:
            return {"error": "product_number parameter is required"}

        raw_data = self._make_api_request(
            "GET", f"search/{product_number}/productdetails", client_id, access_token
        )

        product_data = raw_data.get("Product", raw_data)
        product = self._parse_product(product_data)

        return {
            "data": product,
            "metadata": {
                "source": "Digi-Key Electronics",
                "endpoint": "product_details",
                "query": product_number,
            },
        }

    def _get_categories(
        self, arguments: Dict[str, Any], client_id: str, access_token: str
    ) -> Dict[str, Any]:
        """Get product categories or category details."""
        category_id = arguments.get("category_id")

        if category_id:
            endpoint = f"categories/{category_id}"
        else:
            endpoint = "categories"

        raw_data = self._make_api_request("GET", endpoint, client_id, access_token)

        categories = raw_data.get("Categories", raw_data.get("Children", [raw_data]))
        if isinstance(categories, dict):
            categories = [categories]

        parsed_categories = []
        for cat in categories if isinstance(categories, list) else [categories]:
            parsed_categories.append(
                {
                    "category_id": cat.get("CategoryId", cat.get("Id", "")),
                    "name": cat.get("Name", ""),
                    "product_count": cat.get("ProductCount", 0),
                    "parent_id": cat.get("ParentId", ""),
                    "children_count": len(
                        cat.get("Children", cat.get("ChildCategories", []))
                    ),
                }
            )

        return {
            "data": parsed_categories,
            "metadata": {
                "source": "Digi-Key Electronics",
                "endpoint": "categories",
                "total_results": len(parsed_categories),
            },
        }

    def _get_manufacturers(
        self, arguments: Dict[str, Any], client_id: str, access_token: str
    ) -> Dict[str, Any]:
        """Get manufacturer list or details."""
        raw_data = self._make_api_request(
            "GET", "manufacturers", client_id, access_token
        )

        manufacturers = raw_data.get("Manufacturers", [raw_data])
        if isinstance(manufacturers, dict):
            manufacturers = [manufacturers]

        parsed_mfrs = []
        for mfr in (
            manufacturers if isinstance(manufacturers, list) else [manufacturers]
        ):
            parsed_mfrs.append(
                {
                    "manufacturer_id": mfr.get("ManufacturerId", mfr.get("Id", "")),
                    "name": mfr.get("Name", ""),
                }
            )

        return {
            "data": parsed_mfrs,
            "metadata": {
                "source": "Digi-Key Electronics",
                "endpoint": "manufacturers",
                "total_results": len(parsed_mfrs),
            },
        }
