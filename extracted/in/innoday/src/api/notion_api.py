"""
Notion API client for interacting with Notion databases and pages.

Key differences from Trello/Jira:
- Notion-Version header required (2022-06-28)
- Bearer token authentication
- Block-based content format
- Rich property type system (title, rich_text, select, multi_select, date, etc.)
- Cursor-based pagination (max 100 results per query)
- Rate limiting (3 requests/second average)
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple

import httpx

logger = logging.getLogger(__name__)


class NotionAPI:
    """API client for interacting with Notion databases and pages"""

    def __init__(
        self,
        integration_token: str,
        base_url: str = "https://api.notion.com/v1",
        notion_version: str = "2022-06-28",
    ):
        """
        Initialize Notion API client.

        Args:
            integration_token: Notion integration token (starts with secret_)
            base_url: Notion API base URL
            notion_version: API version header
        """
        self.base_url = base_url
        self.integration_token = integration_token
        self.notion_version = notion_version

        if not self.integration_token:
            raise ValueError("Notion integration token is required")

        if not self.integration_token.startswith("secret_"):
            logger.warning(
                "Integration token should start with 'secret_'. "
                "Visit https://www.notion.so/my-integrations"
            )

        self.headers = {
            "Authorization": f"Bearer {self.integration_token}",
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json",
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> httpx.Response:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method (GET, POST, PATCH)
            endpoint: API endpoint (without base URL)
            json_data: JSON body for POST/PATCH
            params: Query parameters

        Returns:
            httpx.Response object

        Raises:
            Exception: On API errors
        """
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                json=json_data,
                params=params,
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                logger.warning(f"Rate limited. Retrying after {retry_after}s")
                await asyncio.sleep(retry_after)
                return await self._make_request(method, endpoint, json_data, params)

            # Handle errors
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                error_code = error_data.get("code", "unknown")
                error_message = error_data.get("message", response.text)

                if response.status_code == 401:
                    raise Exception(
                        f"Invalid Notion token. Verify at https://www.notion.so/my-integrations. "
                        f"Error: {error_message}"
                    )
                elif response.status_code == 404:
                    raise Exception(
                        f"Notion resource not found. Database may not be shared with integration. "
                        f"Error: {error_message}"
                    )
                else:
                    raise Exception(
                        f"Notion API error ({response.status_code}): {error_code} - {error_message}"
                    )

            return response

    async def get_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        """
        Get database structure including properties.

        Args:
            database_id: Notion database ID (32-char hex string)

        Returns:
            Database object with properties schema
        """
        try:
            response = await self._make_request("GET", f"/databases/{database_id}")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get database {database_id}: {e}")
            raise

    async def query_database_pages(
        self,
        database_id: str,
        filter_dict: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query all pages (tickets) from database with automatic pagination.

        Args:
            database_id: Notion database ID
            filter_dict: Optional filter conditions
            sorts: Optional sort criteria

        Returns:
            List of page objects
        """
        all_pages = []
        has_more = True
        start_cursor = None

        try:
            while has_more:
                query_body = {"page_size": 100}

                if filter_dict:
                    query_body["filter"] = filter_dict
                if sorts:
                    query_body["sorts"] = sorts
                if start_cursor:
                    query_body["start_cursor"] = start_cursor

                response = await self._make_request(
                    "POST", f"/databases/{database_id}/query", json_data=query_body
                )

                data = response.json()
                results = data.get("results", [])
                all_pages.extend(results)

                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")

                # Rate limiting: ~3 requests/second
                if has_more:
                    await asyncio.sleep(0.35)

            logger.info(f"Retrieved {len(all_pages)} pages from database {database_id}")
            return all_pages

        except Exception as e:
            logger.error(f"Failed to query database {database_id}: {e}")
            raise

    async def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific page (ticket) by ID.

        Args:
            page_id: Notion page ID

        Returns:
            Page object with properties
        """
        try:
            response = await self._make_request("GET", f"/pages/{page_id}")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get page {page_id}: {e}")
            return None

    async def create_page(
        self,
        database_id: str,
        properties: Dict[str, Any],
        content_blocks: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new page (ticket) in database.

        Args:
            database_id: Parent database ID
            properties: Property values (title, status, etc.)
            content_blocks: Optional content blocks for page body

        Returns:
            Created page object
        """
        try:
            page_data = {
                "parent": {"database_id": database_id},
                "properties": properties,
            }

            if content_blocks:
                page_data["children"] = content_blocks

            response = await self._make_request("POST", "/pages", json_data=page_data)
            return response.json()

        except Exception as e:
            logger.error(f"Failed to create page in database {database_id}: {e}")
            raise

    async def update_page(
        self, page_id: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update page properties.

        Args:
            page_id: Page ID to update
            properties: Updated property values

        Returns:
            Updated page object
        """
        try:
            update_data = {"properties": properties}
            response = await self._make_request(
                "PATCH", f"/pages/{page_id}", json_data=update_data
            )
            return response.json()

        except Exception as e:
            logger.error(f"Failed to update page {page_id}: {e}")
            raise

    async def append_block_children(
        self, block_id: str, children: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Add content blocks to page (used for comments/descriptions).

        Args:
            block_id: Page ID (blocks are appended to page)
            children: List of block objects

        Returns:
            Response with appended blocks
        """
        try:
            response = await self._make_request(
                "PATCH",
                f"/blocks/{block_id}/children",
                json_data={"children": children},
            )
            return response.json()

        except Exception as e:
            logger.error(f"Failed to append blocks to {block_id}: {e}")
            raise

    async def get_page_content(self, page_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve page content blocks.

        Args:
            page_id: Page ID

        Returns:
            List of block objects
        """
        try:
            response = await self._make_request(
                "GET", f"/blocks/{page_id}/children", params={"page_size": 100}
            )
            data = response.json()
            return data.get("results", [])

        except Exception as e:
            logger.error(f"Failed to get page content for {page_id}: {e}")
            return []

    def _extract_property_value(
        self, property_data: Dict[str, Any], property_type: str
    ) -> Any:
        """
        Extract value from Notion property based on type.

        Args:
            property_data: Property data from API
            property_type: Property type (title, rich_text, select, etc.)

        Returns:
            Extracted value (string, number, date, etc.)
        """
        if not property_data or property_type not in property_data:
            return None

        type_data = property_data[property_type]

        if property_type == "title":
            # Title is array of rich_text objects
            if type_data and len(type_data) > 0:
                return "".join([t.get("plain_text", "") for t in type_data])
            return ""

        elif property_type == "rich_text":
            # Rich text is array of text objects
            if type_data and len(type_data) > 0:
                return "".join([t.get("plain_text", "") for t in type_data])
            return ""

        elif property_type == "select":
            # Select is single option object
            if type_data:
                return type_data.get("name", "")
            return None

        elif property_type == "multi_select":
            # Multi-select is array of option objects
            if type_data and len(type_data) > 0:
                return [opt.get("name", "") for opt in type_data]
            return []

        elif property_type == "date":
            # Date is object with start/end
            if type_data:
                return type_data.get("start")
            return None

        elif property_type == "number":
            return type_data

        elif property_type == "checkbox":
            return type_data

        else:
            # Unsupported type, return as-is
            return type_data

    def _build_property_object(self, property_type: str, value: Any) -> Dict[str, Any]:
        """
        Build Notion property object for creation/update.

        Args:
            property_type: Property type (title, select, rich_text, etc.)
            value: Value to set

        Returns:
            Property object for API
        """
        if property_type == "title":
            return {"title": [{"text": {"content": str(value)}}]}

        elif property_type == "rich_text":
            return {"rich_text": [{"text": {"content": str(value)}}]}

        elif property_type == "select":
            if value:
                return {"select": {"name": str(value)}}
            return {"select": None}

        elif property_type == "multi_select":
            if value and isinstance(value, list):
                return {"multi_select": [{"name": str(v)} for v in value]}
            return {"multi_select": []}

        elif property_type == "date":
            if value:
                return {"date": {"start": str(value)}}
            return {"date": None}

        elif property_type == "number":
            return {"number": value}

        elif property_type == "checkbox":
            return {"checkbox": bool(value)}

        else:
            raise ValueError(f"Unsupported property type: {property_type}")

    def _build_text_block(self, text: str) -> Dict[str, Any]:
        """
        Build a paragraph block for page content.

        Args:
            text: Text content

        Returns:
            Paragraph block object
        """
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
        }

    def _extract_text_from_blocks(
        self, blocks: List[Dict], max_blocks: int = 50, max_length: int = 5000
    ) -> str:
        """
        Extract plain text from Notion blocks with limits.

        Args:
            blocks: List of block objects
            max_blocks: Maximum blocks to process
            max_length: Maximum total text length

        Returns:
            Extracted text with truncation if needed
        """
        text_parts = []
        total_length = 0

        for block in blocks[:max_blocks]:
            block_type = block.get("type")

            if block_type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
                rich_text = block.get(block_type, {}).get("rich_text", [])
                block_text = "".join([t.get("plain_text", "") for t in rich_text])

                if total_length + len(block_text) > max_length:
                    remaining = max_length - total_length
                    text_parts.append(block_text[:remaining])
                    text_parts.append("\n[Description truncated...]")
                    break

                text_parts.append(block_text)
                total_length += len(block_text)

            elif block_type in ["bulleted_list_item", "numbered_list_item"]:
                rich_text = block.get(block_type, {}).get("rich_text", [])
                block_text = "".join([t.get("plain_text", "") for t in rich_text])
                text_parts.append(f"- {block_text}")
                total_length += len(block_text)

        return "\n".join(text_parts)

    async def _detect_status_property(
        self, database_properties: Dict[str, Any]
    ) -> Optional[Tuple[str, str]]:
        """
        Auto-detect status property from database schema.

        Priority:
        1. Property named exactly "Status" (case-insensitive)
        2. Property containing "status" in name
        3. Property named "State" or "Stage"
        4. First select/multi_select property

        Args:
            database_properties: Properties from database object

        Returns:
            Tuple of (property_name, property_type) or None
        """
        candidates = []

        for prop_name, prop_data in database_properties.items():
            prop_type = prop_data.get("type")

            # Only consider select/multi_select properties
            if prop_type not in ["select", "multi_select"]:
                continue

            name_lower = prop_name.lower()

            # Exact match - return immediately
            if name_lower == "status":
                return (prop_name, prop_type)

            # High priority
            elif "status" in name_lower:
                candidates.insert(0, (prop_name, prop_type))

            # Medium priority
            elif name_lower in ["state", "stage"]:
                candidates.append((prop_name, prop_type))

            # Low priority (first select found)
            elif not candidates:
                candidates.append((prop_name, prop_type))

        return candidates[0] if candidates else None
