"""nx_ebay_tools.py — eBay seller tools for NX via the Nexplora BOS proxy.

eBay is connected via Nexplora BOS OAuth (server-side token).  NX calls the
backend proxy at /api/business-os/ebay/call, which resolves and refreshes the
credential automatically.  No eBay token is ever stored or logged client-side.

Available tools (9):
  ebay_list_inventory       — list active inventory items / listings
  ebay_get_inventory_item   — get one listing by SKU
  ebay_get_seller_analytics — seller standards / performance report
  ebay_list_campaigns       — list ad campaigns (Promoted Listings)
  ebay_get_campaign         — get one ad campaign
  ebay_list_promotions      — list discount/coupon promotions
  ebay_get_promotion        — get one promotion
  ebay_list_orders          — list recent seller orders
  ebay_get_order            — get one order by ID
"""

import json
import os
import urllib.request
import urllib.error

_CONFIG = os.path.join(os.path.expanduser("~"), ".nx", "config.json")

# --------------------------------------------------------------------------- #
# Tool schema registry (OpenAI function-calling format)                        #
# --------------------------------------------------------------------------- #

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ebay_list_inventory",
            "description": (
                "List your active eBay inventory items (product listings). "
                "Returns SKU, title, quantity, condition, and pricing."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "string",
                        "description": "Max results to return (default 25, max 100).",
                    },
                    "offset": {
                        "type": "string",
                        "description": "Pagination offset (default 0).",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_get_inventory_item",
            "description": "Get a specific eBay listing by its SKU.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {
                        "type": "string",
                        "description": "The seller-defined SKU of the inventory item.",
                    },
                },
                "required": ["sku"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_get_seller_analytics",
            "description": (
                "Get your eBay seller standards and performance report — "
                "transaction defect rate, late shipment rate, buyer feedback, "
                "and overall seller level (Top Rated, Above Standard, etc.)."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_list_campaigns",
            "description": (
                "List your Promoted Listings ad campaigns on eBay. "
                "Shows campaign name, status, budget, and start/end dates."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["RUNNING", "PAUSED", "ENDED", "PENDING"],
                        "description": "Filter by campaign status (default: all).",
                    },
                    "limit": {
                        "type": "string",
                        "description": "Max results to return (default 25).",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_get_campaign",
            "description": "Get details for a specific eBay ad campaign by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "campaign_id": {
                        "type": "string",
                        "description": "The eBay campaign ID.",
                    },
                },
                "required": ["campaign_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_list_promotions",
            "description": (
                "List your eBay marketing promotions — discount codes, "
                "order discounts, volume pricing, and sale events."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "marketplace_id": {
                        "type": "string",
                        "description": "eBay marketplace (default EBAY_US).",
                    },
                    "limit": {
                        "type": "string",
                        "description": "Max results to return (default 25).",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_get_promotion",
            "description": "Get details for a specific eBay promotion by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "promotion_id": {
                        "type": "string",
                        "description": "The eBay promotion ID.",
                    },
                },
                "required": ["promotion_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_list_orders",
            "description": (
                "List recent eBay orders placed by buyers. "
                "Shows order ID, buyer info, items ordered, amount, and fulfillment status."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "string",
                        "description": "Max orders to return (default 10, max 50).",
                    },
                    "filter": {
                        "type": "string",
                        "description": (
                            "eBay filter expression, e.g. "
                            "'orderfulfillmentstatus:{NOT_STARTED|IN_PROGRESS}' "
                            "or 'creationdate:[2026-01-01T00:00:00.000Z..]'"
                        ),
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ebay_get_order",
            "description": "Get details for a specific eBay order by its order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The eBay order ID.",
                    },
                },
                "required": ["order_id"],
            },
        },
    },
]

# --------------------------------------------------------------------------- #
# Client                                                                        #
# --------------------------------------------------------------------------- #

_OP_MAP = {
    # Hand-written TOOLS names (kept for any caller using nx_ebay_tools.TOOLS).
    "ebay_list_inventory":     "list_inventory",
    "ebay_get_inventory_item": "get_inventory_item",
    "ebay_get_seller_analytics": "get_seller_analytics",
    "ebay_list_campaigns":     "list_campaigns",
    "ebay_get_campaign":       "get_campaign",
    "ebay_list_promotions":    "list_promotions",
    "ebay_get_promotion":      "get_promotion",
    "ebay_list_orders":        "list_seller_orders",
    "ebay_get_order":          "get_order",
    # Auto-synced CHANNEL-catalog names (nx_channel_tools dispatches by THESE). Four of them
    # differed from the hand-written names above, so those catalog tools hit unknown_tool even
    # though the web proxy (/api/business-os/ebay/call) implements the operation. Alias them to
    # the SAME 9 operations the proxy supports so every catalog tool the proxy backs is reachable.
    "ebay_get_seller_standards_profile": "get_seller_analytics",
    "ebay_list_ad_campaigns":  "list_campaigns",
    "ebay_get_ad_campaign":    "get_campaign",
    "ebay_list_seller_orders": "list_seller_orders",
    # The remaining 16 catalog tools — now backed by the web proxy (nexplora-v2 PR #545).
    "ebay_browse_search_items":            "browse_search_items",
    "ebay_browse_get_item":                "browse_get_item",
    "ebay_get_offers":                     "get_offers",
    "ebay_list_inventory_locations":       "list_inventory_locations",
    "ebay_get_shipping_fulfillments":      "get_shipping_fulfillments",
    "ebay_get_traffic_report":             "get_traffic_report",
    "ebay_get_category_suggestions":       "get_category_suggestions",
    "ebay_create_or_update_inventory_item": "create_or_update_inventory_item",
    "ebay_bulk_update_price_quantity":     "bulk_update_price_quantity",
    "ebay_create_offer":                   "create_offer",
    "ebay_publish_offer":                  "publish_offer",
    "ebay_withdraw_offer":                 "withdraw_offer",
    "ebay_create_inventory_location":      "create_inventory_location",
    "ebay_create_shipping_fulfillment":    "create_shipping_fulfillment",
    "ebay_issue_refund":                   "issue_refund",
    "ebay_create_ad_campaign":             "create_ad_campaign",
}


def _cfg() -> dict:
    try:
        with open(_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _token() -> str:
    # The BOS proxy (/api/business-os/ebay/call) authenticates via getRequestActor, which
    # validates the Supabase SESSION token — so send `token`, NOT `nx_token` (the platform
    # token getRequestActor rejects → not_authenticated). Same token-field fix as #449; this
    # is why ebay 401'd while the other BOS connectors (which use `token`) worked.
    c = _cfg()
    return str((c.get("token") or c.get("nx_token") or "")).strip()


def _base() -> str:
    b = os.environ.get("NX_AUTH_BASE")
    if not b:
        try:
            import nx_obfuscate as _o
            b = (getattr(_o, "AUTH", {}) or {}).get("base")
        except Exception:
            b = None
    return (b or "").rstrip("/")


def call(tool_name: str, args: dict | None = None) -> dict:
    """Call an eBay tool via the Nexplora backend proxy.

    Returns {ok, data, error?}.
    """
    op = _OP_MAP.get(tool_name)
    if not op:
        return {"ok": False, "error": f"unknown_tool:{tool_name}"}

    tok = _token()
    if not tok:
        return {"ok": False, "error": "not_signed_in — run /login first"}

    base = _base()
    if not base:
        return {"ok": False, "error": "no_backend_base"}

    url = f"{base}/api/business-os/ebay/call"
    body = json.dumps({"operation": op, "params": args or {}}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", "replace")
            d = json.loads(raw) if raw else {}
            return d if isinstance(d, dict) else {"ok": True, "data": d}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        try:
            d = json.loads(raw)
        except Exception:
            d = {"error": raw[:300]}
        d.setdefault("ok", False)
        return d
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def is_connected() -> bool:
    """True if the user has an active eBay BOS connection."""
    tok = _token()
    base = _base()
    if not tok or not base:
        return False
    try:
        req = urllib.request.Request(
            f"{base}/api/business-os/connections",
            method="GET",
            headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read().decode("utf-8", "replace"))
            platforms = d.get("platforms", [])
            return any(p.get("platform") == "ebay" for p in platforms)
    except Exception:
        return False
