from collections import Counter
from typing import Dict, List, Tuple, Union


def reconstruct_order_book(
    raw_order_book_revisions: List[Dict[str, Union[str, int, List[Dict[str, Union[str, float]]]]]], with_best_prices: bool = True
) -> Dict[Tuple[str, str], Dict[str, Dict[str, List[Dict[str, Union[str, float]]]]]]:
    """Reconstruct order book from raw order book revisions.

        :param raw_order_book_revisions: List of raw order book revision received from the PowerBot API.
        :param with_best_prices: Whether to include the best bid and ask prices in each order book snapshot.
                                 If True, the output will contain additional dictionary statistics, that contains
                                 `best_bid`, `best_ask` and their corresponding quantities.

    :return: Reconstructed order book.

    Example:
        Data retrieval using powerbot_client
        >>> import json
        >>> from datetime import datetime

        >>> from powerbot_client import ApiClient, Configuration, HistoricDataApi
        >>> from powerbot_client.utils import reconstruct_order_book

        >>> api_key = "YOUR_API_KEY"
        >>> host_url = "YOUR_HOST_URL"
        >>> client = ApiClient(Configuration(api_key={"api_key_security": api_key}, host=host_url))
        >>> hist_api = HistoricDataApi(client)
        >>> delivery_start = datetime.fromisoformat("2024-05-01T12:00Z")
        >>> delivery_end = datetime.fromisoformat("2024-05-01T13:00Z")
        >>> product = "XBID_Hour_Power"
        >>> delivery_area = "SomeDeliveryArea"
        >>> page_size = 10_000
        >>> raw_order_book_revisions = []
        >>> token = None
        >>> while True:
        >>>     page = hist_api.get_historic_orders_with_http_info(
        >>>         delivery_area=delivery_area,
        >>>         delivery_start=delivery_start,
        >>>         delivery_end=delivery_end,
        >>>         product=product,
        >>>         page_size=page_size,
        >>>         page_token=token,
        >>>         _preload_content=False,
        >>>     )
        >>>     data = json.loads(page.data)
        >>>     raw_order_book_revisions.extend(data["revisions"])
        >>>     token = data.get("next_page_token")
        >>>     if token is None:
        >>>         break

        Data retrieval using powerbot_asyncio_client
        >>> import asyncio
        >>> import json
        >>> from datetime import datetime
        >>> from typing import Callable

        >>> from powerbot_asyncio_client import ApiClient, Configuration, HistoricDataApi
        >>> from powerbot_asyncio_client.utils import reconstruct_order_book

        >>> async def retrieve_raw_order_book_revisions(historic_request, delivery_area, delivery_start, delivery_end, product, page_size):
        >>>     raw_order_book_revisions = []
        >>>     token = None
        >>>     while True:
        >>>         page = await historic_request(
        >>>             delivery_area=delivery_area,
        >>>             delivery_start=delivery_start,
        >>>             delivery_end=delivery_end,
        >>>             product=product,
        >>>             page_size=page_size,
        >>>             page_token=token,
        >>>             _preload_content=False,
        >>>         )
        >>>         data = await page.content.read()
        >>>         data = json.loads(data)
        >>>         raw_order_book_revisions.extend(data["revisions"])
        >>>         token = data.get("next_page_token")
        >>>         if token is None:
        >>>             break
        >>>     return raw_order_book_revisions
        >>>
        >>> raw_order_book_revisions = asyncio.run(
        >>>     retrieve_raw_order_book_revisions(
        >>>         hist_api.get_historic_orders_with_http_info,
        >>>         delivery_start=delivery_start,
        >>>         delivery_end=delivery_end,
        >>>         product=product,
        >>>         page_size=page_size,
        >>>     )
        >>> )
        >>> reconstructed_order_book = reconstruct_order_book(raw_order_book_revisions)

    """
    bid_snapshot = {}
    ask_snapshot = {}

    book = {}
    # raw_order_book_revisions are already correctly sorted
    for revision in raw_order_book_revisions:
        current_bid = revision["buy_orders"]
        current_ask = revision["sell_orders"]

        # Keep all extra bids/asks and also those with quantity > 0. The latter are needed to get the best_bid/best_ask of new orders
        extra_bid = {o["order_id"]: o for o in current_bid}
        extra_bid_qty_filt = {o["order_id"]: o for o in current_bid if o["quantity"] > 0}

        extra_ask = {o["order_id"]: o for o in current_ask}
        extra_ask_qty_filt = {o["order_id"]: o for o in current_ask if o["quantity"] > 0}

        # Get best_bid and best_ask of the new orders
        new_best_bid = sorted(extra_bid_qty_filt.values(), key=lambda x: x["price"], reverse=True)[0]["price"] if extra_bid_qty_filt else -10000
        new_best_ask = sorted(extra_ask_qty_filt.values(), key=lambda x: x["price"])[0]["price"] if extra_ask_qty_filt else 10000

        # Remove every order from the last snapshot if
        # (1) its order-id is present in the new orders (extra_bid, extra_ask)
        bid_snapshot = bid_snapshot | extra_bid
        ask_snapshot = ask_snapshot | extra_ask

        # (2) If the order has a worse price than the best opposing order of the new orders. Important to note:
        # If this happens, it means that the deletion of that order has not been persisted correctly. It is not clear when the actual deletion
        # of that order did happen, but this timestamp is the latest point where the order can for sure not be available anymore and needs to
        # be removed.
        # (3) Remove orders that have quantity 0
        bid_snapshot = {o_id: o for o_id, o in bid_snapshot.items() if o["quantity"] > 0 and o["price"] < new_best_ask}
        ask_snapshot = {o_id: o for o_id, o in ask_snapshot.items() if o["quantity"] > 0 and o["price"] > new_best_bid}

        book[(revision["time"], revision["revision_number"])] = {"ask": ask_snapshot, "bid": bid_snapshot}

        if with_best_prices:
            bid_counter = Counter()

            for order in bid_snapshot.values():
                bid_counter[order["price"]] += order["quantity"]

            best_bid_price, best_bid_quantity = max(bid_counter.items(), key=lambda x: x[0], default=(None, None))

            sell_counter = Counter()

            for order in ask_snapshot.values():
                sell_counter[order["price"]] += order["quantity"]

            best_ask_price, best_ask_quantity = min(sell_counter.items(), key=lambda x: x[0], default=(None, None))

            book[(revision["time"], revision["revision_number"])].update(
                {
                    "best_bid_price": best_bid_price,
                    "best_bid_quantity": best_bid_quantity,
                    "best_ask_price": best_ask_price,
                    "best_ask_quantity": best_ask_quantity,
                }
            )

    return book
