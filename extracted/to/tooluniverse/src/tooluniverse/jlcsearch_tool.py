# jlcsearch_tool.py
"""
JLCSearch (tscircuit) REST API tool for ToolUniverse.

JLCSearch provides a free, public search engine for in-stock electronic
components from JLCPCB/LCSC. It offers parametric search for resistors,
capacitors, microcontrollers, voltage regulators, LEDs, diodes, and
general component full-text search.

API: https://jlcsearch.tscircuit.com/
Documentation: https://docs.tscircuit.com/web-apis/jlcsearch-api
No authentication required. Free for all use.
"""

import requests
from typing import Dict, Any, List
from .base_tool import BaseTool
from .tool_registry import register_tool

JLCSEARCH_BASE_URL = "https://jlcsearch.tscircuit.com"


@register_tool("JLCSearchTool")
class JLCSearchTool(BaseTool):
    """
    Tool for searching electronic components via the JLCSearch API (tscircuit).

    JLCSearch indexes in-stock electronic components from JLCPCB/LCSC,
    providing parametric search for passive components, semiconductors,
    microcontrollers, and more. Data includes manufacturer part numbers,
    packages, electrical specifications, stock levels, and pricing.

    No authentication required.
    """

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.endpoint_type = fields.get("endpoint", "search")

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the JLCSearch API call."""
        try:
            return self._query(arguments)
        except requests.exceptions.Timeout:
            return {
                "error": f"JLCSearch API request timed out after {self.timeout} seconds"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Failed to connect to JLCSearch API. The service may be temporarily unavailable."
            }
        except requests.exceptions.HTTPError as e:
            return {"error": f"JLCSearch API HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Unexpected error querying JLCSearch: {str(e)}"}

    def _query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to the appropriate endpoint handler."""
        handler_map = {
            "search": self._full_text_search,
            "resistors": self._parametric_search,
            "capacitors": self._parametric_search,
            "microcontrollers": self._parametric_search,
            "voltage_regulators": self._parametric_search,
            "leds": self._parametric_search,
            "diodes": self._parametric_search,
            "categories": self._list_categories,
        }
        handler = handler_map.get(self.endpoint_type)
        if handler is None:
            return {"error": f"Unknown endpoint type: {self.endpoint_type}"}
        return handler(arguments)

    def _full_text_search(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Full-text search across all electronic components."""
        query = arguments.get("query", "")
        if not query:
            return {"error": "query parameter is required"}

        params = {"q": query}
        limit = arguments.get("limit")
        if limit is not None:
            params["limit"] = int(limit)
        package = arguments.get("package")
        if package:
            params["package"] = package

        url = f"{JLCSEARCH_BASE_URL}/api/search"
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        components = data.get("components", [])

        return {
            "data": components,
            "metadata": {
                "source": "JLCSearch (tscircuit/JLCPCB)",
                "endpoint": "search",
                "query": query,
                "total_results": len(components),
            },
        }

    def _parametric_search(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Parametric search for a specific component type."""
        # Build query parameters from arguments, excluding None values
        params = {}
        limit = arguments.get("limit")
        if limit is not None:
            params["limit"] = int(limit)

        package = arguments.get("package")
        if package:
            params["package"] = package

        # Component-type-specific parameters
        # Resistors
        resistance = arguments.get("resistance")
        if resistance is not None:
            params["resistance"] = resistance

        # Capacitors
        capacitance = arguments.get("capacitance")
        if capacitance is not None:
            params["capacitance"] = capacitance
        voltage = arguments.get("voltage")
        if voltage is not None:
            params["voltage"] = voltage

        # Microcontrollers
        cpu_core = arguments.get("cpu_core")
        if cpu_core:
            params["cpu_core"] = cpu_core

        # Voltage regulators
        output_voltage = arguments.get("output_voltage")
        if output_voltage is not None:
            params["output_voltage"] = output_voltage
        output_current = arguments.get("output_current")
        if output_current is not None:
            params["output_current"] = output_current

        # LEDs
        color = arguments.get("color")
        if color:
            params["color"] = color

        url = f"{JLCSEARCH_BASE_URL}/{self.endpoint_type}/list.json"
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()

        # The response key varies by endpoint type
        # e.g., "resistors" -> "resistors", "voltage_regulators" -> "regulators",
        # "leds" -> "leds", "diodes" -> "diodes", etc.
        result_key = None
        for key in data:
            if key != "error":
                result_key = key
                break

        if result_key is None:
            return {
                "data": [],
                "metadata": {
                    "source": "JLCSearch (tscircuit/JLCPCB)",
                    "endpoint": self.endpoint_type,
                    "total_results": 0,
                },
            }

        components = data[result_key]

        return {
            "data": components,
            "metadata": {
                "source": "JLCSearch (tscircuit/JLCPCB)",
                "endpoint": self.endpoint_type,
                "total_results": len(components),
                "params": {k: v for k, v in params.items() if k != "limit"},
            },
        }

    def _list_categories(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """List all available component categories and subcategories."""
        url = f"{JLCSEARCH_BASE_URL}/categories/list.json"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        categories = data.get("categories", [])

        return {
            "data": categories,
            "metadata": {
                "source": "JLCSearch (tscircuit/JLCPCB)",
                "endpoint": "categories",
                "total_categories": len(categories),
            },
        }
