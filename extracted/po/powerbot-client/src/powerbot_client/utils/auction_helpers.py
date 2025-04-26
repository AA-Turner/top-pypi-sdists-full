try:
    import pandas as pd
except ImportError as e:
    raise ImportError(
        "Missing required module 'pandas'. Please install it using `pip install pandas`."
    ) from e

from ..models import Auction, Curve, CurvePoint, AuctionOrderEntry, Curve, CurvePoint, AuctionOrderData


def generate_curve_orders(price_matrix: pd.DataFrame, auction: Auction, delivery_area: str, portfolio_id: str) -> AuctionOrderEntry:
    """Generate auction order entry from the provided price matrix in the pandas DataFrame format.

        :param price_matrix: Price matrix in pandas DataFrame format.
        :param auction: Auction object received from PowerBot API.
        :param delivery_area: EIC.
        :param portfolio_id: Unique portfolio ID.


    :return: AuctionOrderEntry object, that can be used to post curve orders on the exchange.

    Example:
        Data retrieval using powerbot_client
        >>> from powerbot_client import Configuration, ApiClient, AuctionsApi

        >>> api_key = "YOUR_API_KEY"
        >>> host_url = "YOUR_HOST_URL"
        >>> EXCHANGE = "XXX"
        >>> DELIVERY_AREA = "XXX"
        >>> PORTFOLIO_ID = "XXX"
        >>> gate_closure_from = "XXX"
        >>> gate_closure_to = "XXX"

        >>> client = ApiClient(Configuration(api_key={"api_key_security": api_key}, host=host_url))
        >>> auctions_api = AuctionsApi(client)

        >>> # retrieve relevant auction from the API
        >>> list_auctions = auctions_api.list_auctions(exchange_id=EXCHANGE, delivery_areas=[DELIVERY_AREA],  gate_closure_from=gate_closure_from,  gate_closure_to=gate_closure_to)

        >>> # instead of taking the first element, select according to some criteria
        >>> relevant_auction = list_auctions[0]

        >>> # dataframe containing: delivery_start & delivery_end which are timezone aware datetime objects
        >>> # ALL other column names should be string representations of prices that correspond to the quantities
        >>> orders_to_place = generate_curve_orders(price_matrix, relevant_auction, DELIVERY_AREA, PORTFOLIO_ID)

    """
    assert isinstance(price_matrix, pd.DataFrame), "Price matrix must be a pandas DataFrame!"
    assert "delivery_start" in price_matrix.columns, "delivery start column is missing in the DataFrame!"
    assert "delivery_end" in price_matrix.columns, "delivery end column is missing in the DataFrame!"

    assert isinstance(auction, Auction), "Auction must be an Auction object!"

    # check for duplicates in the delivery start column
    duplicates = price_matrix[price_matrix["delivery_start"].duplicated()]["delivery_start"]
    assert duplicates.empty, "Duplicate rows detected in delivery_start column!"

    # check for duplicates in the delivery end column
    duplicates = price_matrix[price_matrix["delivery_end"].duplicated()]["delivery_end"]
    assert duplicates.empty, "Duplicate rows detected in delivery_end column!"

    # try convert to datetime
    price_matrix["delivery_start"] = pd.to_datetime(price_matrix["delivery_start"])
    price_matrix["delivery_end"] = pd.to_datetime(price_matrix["delivery_end"])

    # datetime MUST be tz-aware
    assert price_matrix["delivery_start"].dt.tz is not None, "delivery start MUST be tz aware!"
    assert price_matrix["delivery_end"].dt.tz is not None, "delivery end MUST be tz aware!"

    contract_mapping = {(c.delivery_start, c.delivery_end): c for c in auction.contracts}

    price_matrix["contract_id"] = price_matrix.apply(lambda x: contract_mapping.get((x.delivery_start, x.delivery_end)).contract_id, axis=1)

    # drop delivery period, since we have contract ID already
    price_matrix = price_matrix.drop(columns=["delivery_start", "delivery_end"])

    curves = []
    for row in price_matrix.iterrows():
        curve_information = row[1].to_dict()

        contract_id = curve_information.pop("contract_id")

        curves.append(Curve(contract_id=contract_id, curve_points=[CurvePoint(price=float(k), quantity=float(v)) for k, v in curve_information.items()]))

    return AuctionOrderEntry(
        auction_id=auction.auction_id,
        delivery_area=delivery_area,
        portfolio_id=portfolio_id,
        order_data=AuctionOrderData(curves=curves))

