from __future__ import annotations # Allow self-referencing 
import datetime
import json
import logging
import os

from collections import defaultdict
from pathlib import Path
from typing import Union, List, Dict, Any, Optional
from zoneinfo import ZoneInfo

import grpc
import pandas as pd
import polars as pl
import zstandard  # Required for ZSTD decompression
from dotenv import load_dotenv # Import load_dotenv

from ._proto.v3grpc import endpoints_pb2, endpoints_pb2_grpc
from ._proto.endpoints_pb2 import AuthToken, DataTable, CompressionAlgo, ContractSpec, TimeZone
from .errors import AuthenticationError, NoDataFoundError

logger = logging.getLogger(__name__)

def _fmt_time(time:Union[datetime.time|str]) -> str:
    if isinstance(time, str):
        return time
    ms = time.microsecond // 1000
    return time.strftime("%H:%M:%S") + f".{ms:03d}"

def _fmt_if_date(date:Union[datetime.date, str]) -> str:
    if isinstance(date, str):
        return date
    return date.strftime('%Y-%m-%d')

PRICE_TYPE_FACTORS = [
            0.0,
            0.000000001,
            0.00000001,
            0.0000001,
            0.000001,
            0.00001,
            0.0001,
            0.001,
            0.01,
            0.1,
            1.0,
            10.0,
            100.0,
            1000.0,
            10000.0,
            100000.0,
            1000000.0,
            10000000.0,
            100000000.0,
            1000000000.0
]

class ThetaClient:
    """The client for making requests to Theta Data.

    Note: a subscription to thetadata.net is required to use this class.

    Args:
        creds_file: A credentials file with an email on the first line, and password on the second. This can be the
                    same file used for the v3 terminal.
        email:      An email address to use for authentication, assuming a creds_file or api_key was not provided.
        password:   A password to use for authentication, assuming a creds_file or api_key was not provided.
        dotenv_path: An optional path to the .env file containing API key or credentials.
        api_key:    An API key to use for authentication. If provided, takes precedence over email/password from creds_file or email/password parameters.
        existing_authorized_client: An existing ThetaClient object whose authentication can be reused by this one - overrides all other authentication parameters.
        dataframe_type: The type of DataFrame to return from methods: Pandas or Polars; defaults to Polars.
        mdds_host:  Used to override the address of the Thetadata service.
        mdds_port:  Used to override the port of the Thetadata service.
        mdds_type:  The MDDS environment to connect to: "PROD" (default) or "STAGE". Can also be set via the THETADATA_MDDS_TYPE environment variable.
    Raises:
        AuthenticationError: If authentication fails.
    """
    @staticmethod
    def _read_creds_from_file(file_path: Path) -> Optional[dict]:
        """Reads credentials from a file path."""
        try:
            with open(file_path, "r") as f:
                email = f.readline().strip()
                password = f.readline().strip()
                if email and password:
                    return {"email": email, "password": password}
        except FileNotFoundError:
            return None
        return None

    def __init__(self, creds_file:Optional[Union[Path|str]]=None, email:Optional[str]=None, password:Optional[str]=None, api_key:Optional[str]=None, existing_authorized_client:Optional[ThetaClient]=None, dataframe_type:Union["pandas", "polars"] = "polars", mdds_host:Optional[str]=None, mdds_port:Optional[str]=None, mdds_type:Optional[str]=None, dotenv_path:Optional[Union[Path|str]]=None, auth_url:Optional[str]=None, insecure_channel:bool=False):
        if mdds_type is not None:
            self.mdds_type = mdds_type
        elif existing_authorized_client is not None:
            self.mdds_type = existing_authorized_client.mdds_type
        else:
            self.mdds_type = os.getenv("THETADATA_MDDS_TYPE", "PROD")

        if existing_authorized_client is not None:
            # Copy authentication from an existing client
            self.auth_token = existing_authorized_client.auth_token
            self.email = getattr(existing_authorized_client, 'email', "")
            self.api_key = getattr(existing_authorized_client, 'api_key', None)
            self.stock_subscription = existing_authorized_client.stock_subscription
            self.options_subscription = existing_authorized_client.options_subscription
            self.index_subscription = existing_authorized_client.index_subscription
            self.creds_file = getattr(existing_authorized_client, 'creds_file', None)
        else:
            import httpx

            auth_request = {}

            # explicit creds_file overrides API key discovery
            if creds_file:
                self.creds_file = Path(creds_file)
                creds = self._read_creds_from_file(self.creds_file)
                if creds:
                    auth_request.update(creds)
                    logger.info(f"Authenticating with explicitly provided credentials file: {self.creds_file}")
                else:
                    raise AuthenticationError(f"Specified credentials file not found at {self.creds_file}.")
            else:
                load_dotenv(dotenv_path=dotenv_path) # Load .env file
                # Try API Key first (param or env var)
                self.api_key = api_key or os.getenv("THETADATA_API_KEY")
                if self.api_key:
                    auth_request['apiKey'] = self.api_key
                    logger.info("Authenticating with API key.")
                # Then try email/password params
                elif email and password:
                    auth_request['email'] = email.strip()
                    auth_request['password'] = password
                    logger.info("Authenticating with email and password.")
                # Finally, fall back to default creds file
                else:
                    default_creds_file = Path(os.getenv("THETADATA_CREDENTIALS_FILE", "./creds.txt"))
                    self.creds_file = default_creds_file
                    creds = self._read_creds_from_file(self.creds_file)
                    if creds:
                        auth_request.update(creds)
                        logger.info(f"Authenticating with credentials from default file: {self.creds_file}")
                    # If creds is None, we just continue, and the final check will catch it.
            
            if not auth_request:
                raise AuthenticationError("No valid authentication credentials could be found.")

            auth_request['authEnv'] = {'envType': self.mdds_type}

            resolved_auth_url = auth_url or os.getenv("THETADATA_AUTH_URL", "https://nexus-api.thetadata.us/identity/terminal/auth_user")
            res = httpx.post(resolved_auth_url, json=auth_request, headers={'TD-TERMINAL-KEY': 'cf58ada4-4175-11f0-860f-1e2e95c79e64'})

            if not res.is_success:
                logger.error(f"Authentication failed: {res.text}")
                raise AuthenticationError(res.text)

            auth_response = res.json()
            logger.info(f"Successfully authenticated with Theta Data server: {json.dumps(auth_response, indent=2)}")

            # set all the fields
            self.auth_token = AuthToken(session_uuid=auth_response["sessionId"])
            self.email = auth_response['user']['email']
            self.stock_subscription = auth_response['user']['stockSubscription']
            self.options_subscription = auth_response['user']['optionsSubscription']
            self.index_subscription = auth_response['user']['indicesSubscription']

        self.dataframe_type = dataframe_type

        # create the gRPC channel and stub
        default_host = "mdds-stage.thetadata.us" if self.mdds_type == "STAGE" else "mdds-01.thetadata.us"
        if mdds_type is None and existing_authorized_client is not None:
            inherited_host = getattr(existing_authorized_client, 'mdds_host', default_host)
            inherited_port = getattr(existing_authorized_client, 'mdds_port', "443")
        else:
            inherited_host = default_host
            inherited_port = "443"
        self.mdds_host = mdds_host or os.getenv("THETADATA_MDDS_HOST", inherited_host)
        self.mdds_port = mdds_port or os.getenv("THETADATA_MDDS_PORT", inherited_port)
        grpc_target = f"{self.mdds_host}:{self.mdds_port}"

        use_insecure = insecure_channel or os.getenv("THETADATA_INSECURE_CHANNEL", "").lower() in ("1", "true")
        channel = grpc.insecure_channel(grpc_target) if use_insecure else grpc.secure_channel(grpc_target, grpc.ssl_channel_credentials())
        self.stub = endpoints_pb2_grpc.BetaThetaTerminalStub(channel)

    def _convert_response_stream(self, response_stream: List[endpoints_pb2.ResponseData]) -> Dict[str, List[Any]]:
        decompressor = zstandard.ZstdDecompressor()
        ret = defaultdict(list)
        timestamp_columns = set()

        for response in response_stream:
            response: endpoints_pb2.ResponseData = response

            if response.compression_description.algo == CompressionAlgo.ZSTD:
                decompressed_data = decompressor.decompress(response.compressed_data)
                data_table = DataTable()
                data_table.ParseFromString(decompressed_data)
            elif response.compression_description.algo == CompressionAlgo.NONE:
                data_table = DataTable()
                data_table.ParseFromString(response.compressed_data)
            else:
                raise NotImplementedError(response.compression_description.algo)

            for row in data_table.data_table:
                for i, header in enumerate(data_table.headers):
                    value_container = row.values[i]

                    value_to_append = None
                    if value_container.HasField('text'):
                        value_to_append = value_container.text
                    elif value_container.HasField('number'):
                        value_to_append = value_container.number
                    elif value_container.HasField('price'):
                        price = value_container.price
                        if price.type != 0:
                            value_to_append = price.value * PRICE_TYPE_FACTORS[price.type]
                        else:
                            value_to_append = float('nan')
                    elif value_container.HasField('timestamp'):
                        timestamp_columns.add(header)
                        timestamp = value_container.timestamp
                        dt_utc = datetime.datetime.fromtimestamp(timestamp.epoch_ms / 1000, tz=datetime.timezone.utc)
                        if timestamp.zone == TimeZone.NEW_YORK:
                            ny_tz = ZoneInfo('America/New_York')
                            value_to_append = dt_utc.astimezone(ny_tz)
                        else:
                            value_to_append = dt_utc

                    ret[header].append(value_to_append)

        if self.dataframe_type == "polars":
            df = pl.DataFrame(ret)
            for column_name in timestamp_columns:
                df = df.with_columns(pl.col(column_name).dt.cast_time_unit("ms"))
            return df
        else:
            return pd.DataFrame(ret)

#######################################
# All code below is auto-generated!!! #
#######################################

    """A symbol can be defined as a unique identifier for a stock / underlying asset. Common terms also include: root, ticker, and underlying. This endpoint returns all traded symbols for stocks. This endpoint is updated overnight.

    """
    def stock_list_symbols(self):
        try:
            query_parameters = {"client": "python"}
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockListSymbolsRequestQuery()
        request = endpoints_pb2.StockListSymbolsRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockListSymbols(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_list_symbols()")
            else:
                raise e

    """Lists all dates of data that are available for a stock with a given request type and symbol. This endpoint is updated overnight.

    """
    def stock_list_dates(self, request_type:str, symbol:Union[List[str], str]):
        try:
            query_parameters = {"client": "python"}
            query_parameters["request_type"] = str(request_type)
            query_parameters["symbol"] = str(symbol)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockListDatesRequestQuery()
        query.request_type = request_type
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        request = endpoints_pb2.StockListDatesRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockListDates(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_list_dates({ request_type },{ symbol })")
            else:
                raise e

    """
Provides a real-time Open, High, Low, Close for the current day.
* Returns a real-time session OHLC from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
* Returns a 15-minute delayed session OHLC from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs) if the account has the stocks value subscription.
* Theta Data resets its snapshot cache at midnight ET every day. This endpoint may not work on a weekend where there were no eligible messages sent over exchange feeds. We recommend using historic requests during the weekend.

    """
    def stock_snapshot_ohlc(self, symbol:Union[List[str], str], venue:Optional[str]='nqb', min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockSnapshotOhlcRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if venue:
            query.venue = venue
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.StockSnapshotOhlcRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockSnapshotOhlc(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_snapshot_ohlc({ symbol },{ venue },{ min_time })")
            else:
                raise e

    """
Returns a real-time last trade from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).

- Theta Data resets its snapshot cache at midnight ET every day. This endpoint may not work on a weekend where there were no eligible messages sent over exchange feeds. We recommend using historic requests during the weekend.

    """
    def stock_snapshot_trade(self, symbol:Union[List[str], str], venue:Optional[str]='nqb', min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockSnapshotTradeRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if venue:
            query.venue = venue
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.StockSnapshotTradeRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockSnapshotTrade(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_snapshot_trade({ symbol },{ venue },{ min_time })")
            else:
                raise e

    """* Returns a real-time last BBO quote from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
* Returns a 15-minute delayed NBBO quote from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs) account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.
- Theta Data resets its snapshot cache at midnight ET every day. This endpoint may not work on a weekend where there were no eligible messages sent over exchange feeds. We recommend using historic requests during the weekend.

    """
    def stock_snapshot_quote(self, symbol:Union[List[str], str], venue:Optional[str]='nqb', min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockSnapshotQuoteRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if venue:
            query.venue = venue
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.StockSnapshotQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockSnapshotQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_snapshot_quote({ symbol },{ venue },{ min_time })")
            else:
                raise e

    """* Returns a real-time market value derived from the last BBO quote from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
* Returns a 15-minute delayed market value derived from an NBBO quote from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs) if the account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.
- Theta Data resets its snapshot cache at midnight ET every day. This endpoint may not work on a weekend where there were no eligible messages sent over exchange feeds. We recommend using historic requests during the weekend.

    """
    def stock_snapshot_market_value(self, symbol:Union[List[str], str], venue:Optional[str]='nqb', min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockSnapshotMarketValueRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if venue:
            query.venue = venue
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.StockSnapshotMarketValueRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockSnapshotMarketValue(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_snapshot_market_value({ symbol },{ venue },{ min_time })")
            else:
                raise e

    """
Since [the equity SIPs](/Articles/Data-And-Requests/The-SIPs.html) only generate a partial EOD report, Theta Data generates a national EOD report at 17:15 ET each day. ``created`` represents the datetime the report was generated and ``last_trade`` represents the datetime of the last trade. The quote in the response represents the last NBBO reported by [CTA or UTP](/Articles/Data-And-Requests/The-SIPs.html) at the time of report generation. You can read more about EOD & OHLC data [here](/Articles/Data-And-Requests/OHLC-EOD.html). Theta Data plans to avail SIP EOD reports in the near future.

    """
    def stock_history_eod(self, symbol:str, start_date:datetime.date, end_date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockHistoryEodRequestQuery()
        query.symbol = symbol
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.StockHistoryEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockHistoryEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_history_eod({ symbol },{ start_date },{ end_date })")
            else:
                raise e

    """- Aggregated OHLC bars that use [SIP rules](/Articles/Data-And-Requests/OHLC-EOD.html) for each bar. Time timestamp of the bar represents the opening time of the bar. For a trade to be part of the bar:  ``bar time`` <= ``trade time`` < ``bar timestamp + ivl``, where ivl is the specified interval size in milliseconds. 
- Set the ``venue`` parameter to ``nqb`` to access current-day real-time historic data from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Multi-day requests are limited to 1 month of data.

    """
    def stock_history_ohlc(self, symbol:str, interval:str='1s', date:Optional[datetime.date]=None, start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), venue:Optional[str]='nqb', start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockHistoryOhlcRequestQuery()
        query.symbol = symbol
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if venue:
            query.venue = venue
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.StockHistoryOhlcRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockHistoryOhlc(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_history_ohlc({ symbol },{ interval },{ date },{ start_time },{ end_time },{ venue },{ start_date },{ end_date })")
            else:
                raise e

    """Returns every trade reported by [UTP & CTA](/Articles/Data-And-Requests/The-SIPs). Set the ``venue`` parameter to ``nqb`` to access current-day real-time historic data from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Multi-day requests are limited to 1 month of data.

    """
    def stock_history_trade(self, symbol:str, date:Optional[datetime.date]=None, start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), venue:Optional[str]='nqb', start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if date is not None:
                query_parameters["date"] = str(date)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockHistoryTradeRequestQuery()
        query.symbol = symbol
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if venue:
            query.venue = venue
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.StockHistoryTradeRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockHistoryTrade(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_history_trade({ symbol },{ date },{ start_time },{ end_time },{ venue },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns every NBBO quote reported by [UTP and CTA](/Articles/Data-And-Requests/The-SIPs). 
- If the ``interval`` parameter is specified, the quote for each interval represents the last quote prior to the interval's timestamp. 
- Set the ``venue`` parameter to ``nqb`` to access current-day real-time historic data from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Multi-day requests are limited to 1 month of data.

    """
    def stock_history_quote(self, symbol:str, interval:str='1s', date:Optional[datetime.date]=None, start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), venue:Optional[str]='nqb', start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockHistoryQuoteRequestQuery()
        query.symbol = symbol
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if venue:
            query.venue = venue
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.StockHistoryQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockHistoryQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_history_quote({ symbol },{ interval },{ date },{ start_time },{ end_time },{ venue },{ start_date },{ end_date })")
            else:
                raise e

    """Returns every trade reported by [UTP & CTA](/Articles/Data-And-Requests/The-SIPs) paired with the last BBO quote reported by [UTP or CTA](/Articles/Data-And-Requests/The-SIPs) at the time of trade. A quote is matched with a trade if its timestamp ``<=`` the trade timestamp. If you prefer to match quotes with timestamps that are ``<`` the trade timestamp, specify the ``exclusive`` parameter to ``true``. Set the ``venue`` parameter to ``nqb`` to access current-day real-time historic data from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Multi-day requests are limited to 1 month of data.

    """
    def stock_history_trade_quote(self, symbol:str, date:Optional[datetime.date]=None, start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), exclusive:Optional[bool]=True, venue:Optional[str]='nqb', start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if date is not None:
                query_parameters["date"] = str(date)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if exclusive is not None:
                query_parameters["exclusive"] = str(exclusive)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockHistoryTradeQuoteRequestQuery()
        query.symbol = symbol
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if exclusive:
            query.exclusive = exclusive
        if venue:
            query.venue = venue
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.StockHistoryTradeQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockHistoryTradeQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_history_trade_quote({ symbol },{ date },{ start_time },{ end_time },{ exclusive },{ venue },{ start_date },{ end_date })")
            else:
                raise e

    """#### Real-time request:
- Returns a real-time session from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs.html#nasdaq-basic) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Returns a 15-minute delayed session from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.

#### Historical request:
Returns the last trade reported by [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) at a specified millisecond of the day.
Trade condition mappings can be found [here](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).

    """
    def stock_at_time_trade(self, symbol:str, start_date:datetime.date, end_date:datetime.date, time_of_day:Union[datetime.time, str], venue:Optional[str]='nqb'):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            query_parameters["time_of_day"] = str(time_of_day)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockAtTimeTradeRequestQuery()
        query.symbol = symbol
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        query.time_of_day = _fmt_time(time_of_day)
        if venue:
            query.venue = venue
        request = endpoints_pb2.StockAtTimeTradeRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockAtTimeTrade(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_at_time_trade({ symbol },{ start_date },{ end_date },{ time_of_day },{ venue })")
            else:
                raise e

    """#### Real-time request:
  - Subscription tier standard or higher will default to NQB.
  - Real-time last BBO quote at-time_of_day-time from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs.html#nasdaq-basic) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
  - 15-minute delayed NBBO quote at-time_of_day-time from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.

#### Historical request:
  Returns the last NBBO quote reported by [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) at a specified millisecond of the day.

    """
    def stock_at_time_quote(self, symbol:str, start_date:datetime.date, end_date:datetime.date, time_of_day:Union[datetime.time, str], venue:Optional[str]='nqb'):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            query_parameters["time_of_day"] = str(time_of_day)
            if venue is not None:
                query_parameters["venue"] = str(venue)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockAtTimeQuoteRequestQuery()
        query.symbol = symbol
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        query.time_of_day = _fmt_time(time_of_day)
        if venue:
            query.venue = venue
        request = endpoints_pb2.StockAtTimeQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockAtTimeQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_at_time_quote({ symbol },{ start_date },{ end_date },{ time_of_day },{ venue })")
            else:
                raise e

    """A symbol can be defined as a unique identifier for a stock / underlying asset. Common terms also include: root, ticker, and underlying. This endpoint returns all traded symbols for options. This endpoint is updated overnight.

    """
    def option_list_symbols(self):
        try:
            query_parameters = {"client": "python"}
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.OptionListSymbolsRequestQuery()
        request = endpoints_pb2.OptionListSymbolsRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionListSymbols(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_list_symbols()")
            else:
                raise e

    """Lists all dates of data that are available for an option with a given symbol, request type, and expiration.
This endpoint is updated overnight.

    """
    def option_list_dates(self, request_type:str, symbol:str, expiration:datetime.date, strike:Optional[str]='*', right:Optional[str]='both'):
        try:
            query_parameters = {"client": "python"}
            query_parameters["request_type"] = str(request_type)
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionListDatesRequestQuery(contract_spec=contract_spec)
        query.request_type = request_type
        request = endpoints_pb2.OptionListDatesRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionListDates(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_list_dates({ request_type },{ symbol },{ expiration },{ strike },{ right })")
            else:
                raise e

    """Lists all dates of expirations that are available for an option with a given symbol.
This endpoint is updated overnight.

    """
    def option_list_expirations(self, symbol:Union[List[str], str]):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.OptionListExpirationsRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        request = endpoints_pb2.OptionListExpirationsRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionListExpirations(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_list_expirations({ symbol })")
            else:
                raise e

    """Lists all strikes that are available for an option with a given symbol and expiration date.
This endpoint is updated overnight.

    """
    def option_list_strikes(self, symbol:Union[List[str], str], expiration:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.OptionListStrikesRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        query.expiration = expiration.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionListStrikesRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionListStrikes(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_list_strikes({ symbol },{ expiration })")
            else:
                raise e

    """Lists all contracts that were traded or quoted on a particular date.

If the ``symbol`` parameter is specified, the returned contracts will be filtered to match the symbol.
Multiple symbols can be specified by separating them with commas such as ``symbol=AAPL,SPY,AMD``
This endpoint is updated real-time.

    """
    def option_list_contracts(self, request_type:str, date:datetime.date, symbol:Union[List[str], str]=None, max_dte:Optional[int]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["request_type"] = str(request_type)
            query_parameters["date"] = str(date)
            if symbol is not None:
                query_parameters["symbol"] = str(symbol)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.OptionListContractsRequestQuery()
        query.request_type = request_type
        query.date = date.strftime('%Y-%m-%d')
        if symbol:
            query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if max_dte:
            query.max_dte = max_dte
        request = endpoints_pb2.OptionListContractsRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionListContracts(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_list_contracts({ request_type },{ date },{ symbol },{ max_dte })")
            else:
                raise e

    """- Retrieve a real-time last ohlc of an option contract for the trading day.
- You might need to change the default expiration date to a different date if it is past the current date.

    """
    def option_snapshot_ohlc(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotOhlcRequestQuery(contract_spec=contract_spec)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.OptionSnapshotOhlcRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotOhlc(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_ohlc({ symbol },{ expiration },{ strike },{ right },{ max_dte },{ strike_range },{ min_time })")
            else:
                raise e

    """- Retrieve the real-time last trade of an option contract.
- You might need to change the default expiration date to a different date if it is past the current date.
- This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

    """
    def option_snapshot_trade(self, symbol:str, expiration:datetime.date, strike:Optional[str]='*', right:Optional[str]='both', strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotTradeRequestQuery(contract_spec=contract_spec)
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.OptionSnapshotTradeRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotTrade(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_trade({ symbol },{ expiration },{ strike },{ right },{ strike_range },{ min_time })")
            else:
                raise e

    """
- Retrieve a real-time last NBBO quote of an option contract.
- You might need to change the default expiration date to a different date if it is past the current date.
- This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

    """
    def option_snapshot_quote(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotQuoteRequestQuery(contract_spec=contract_spec)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.OptionSnapshotQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_quote({ symbol },{ expiration },{ strike },{ right },{ max_dte },{ strike_range },{ min_time })")
            else:
                raise e

    """- Retrieve the last open interest message of an option contract.
- Open interest is reported around 06:30 ET every morning by OPRA and reflects the open interest at the of the previous trading day. 
- You might need to change the default expiration date to a different date if it is past the current date.
- This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

    """
    def option_snapshot_open_interest(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotOpenInterestRequestQuery(contract_spec=contract_spec)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.OptionSnapshotOpenInterestRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotOpenInterest(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_open_interest({ symbol },{ expiration },{ strike },{ right },{ max_dte },{ strike_range },{ min_time })")
            else:
                raise e

    """* Returns a real-time market value derived from the last NBBO quote of an option contract.

    """
    def option_snapshot_market_value(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotMarketValueRequestQuery(contract_spec=contract_spec)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.OptionSnapshotMarketValueRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotMarketValue(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_market_value({ symbol },{ expiration },{ strike },{ right },{ max_dte },{ strike_range },{ min_time })")
            else:
                raise e

    """Returns implied volatilies calculated using the national best bid, mid, and ask price
of the option respectively. The underlying price represents whatever the last underlying price was at the
``underlying_timestamp`` field. You can read more about how Theta Data calculates greeks 
[here](/Articles/Data-And-Requests/Option-Greeks.html).

    """
    def option_snapshot_greeks_implied_volatility(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, stock_price:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None, use_market_value:Optional[bool]=False):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if stock_price is not None:
                query_parameters["stock_price"] = str(stock_price)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            if use_market_value is not None:
                query_parameters["use_market_value"] = str(use_market_value)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotGreeksImpliedVolatilityRequestQuery(contract_spec=contract_spec)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if stock_price:
            query.stock_price = stock_price
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        if use_market_value:
            query.use_market_value = use_market_value
        request = endpoints_pb2.OptionSnapshotGreeksImpliedVolatilityRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotGreeksImpliedVolatility(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_greeks_implied_volatility({ symbol },{ expiration },{ strike },{ right },{ annual_dividend },{ rate_type },{ rate_value },{ stock_price },{ version },{ max_dte },{ strike_range },{ min_time },{ use_market_value })")
            else:
                raise e

    """- Retrieve a real-time last greeks calculation for all option contracts that lie on a provided expiration.
- You might need to change the default expiration date to a different date if it is past the current date. Some quotes are omitted in the example to reduce the space of the sample output.
- Make `expiration` * if you want to get the snapshot for every expiration chain for the underlying.
> This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

    """
    def option_snapshot_greeks_all(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, stock_price:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None, use_market_value:Optional[bool]=False):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if stock_price is not None:
                query_parameters["stock_price"] = str(stock_price)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            if use_market_value is not None:
                query_parameters["use_market_value"] = str(use_market_value)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotGreeksAllRequestQuery(contract_spec=contract_spec)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if stock_price:
            query.stock_price = stock_price
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        if use_market_value:
            query.use_market_value = use_market_value
        request = endpoints_pb2.OptionSnapshotGreeksAllRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotGreeksAll(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_greeks_all({ symbol },{ expiration },{ strike },{ right },{ annual_dividend },{ rate_type },{ rate_value },{ stock_price },{ version },{ max_dte },{ strike_range },{ min_time },{ use_market_value })")
            else:
                raise e

    """- Retrieve a real-time last greeks calculation for all option contracts that lie on a provided expiration.
- You might need to change the default expiration date to a different date if it is past the current date. Some quotes are omitted in the example to reduce the space of the sample output.
- Make `expiration` * if you want to get the snapshot for every expiration chain for the underlying.
> This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

    """
    def option_snapshot_greeks_first_order(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, stock_price:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None, use_market_value:Optional[bool]=False):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if stock_price is not None:
                query_parameters["stock_price"] = str(stock_price)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            if use_market_value is not None:
                query_parameters["use_market_value"] = str(use_market_value)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotGreeksFirstOrderRequestQuery(contract_spec=contract_spec)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if stock_price:
            query.stock_price = stock_price
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        if use_market_value:
            query.use_market_value = use_market_value
        request = endpoints_pb2.OptionSnapshotGreeksFirstOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotGreeksFirstOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_greeks_first_order({ symbol },{ expiration },{ strike },{ right },{ annual_dividend },{ rate_type },{ rate_value },{ stock_price },{ version },{ max_dte },{ strike_range },{ min_time },{ use_market_value })")
            else:
                raise e

    """- Retrieve a real-time last second order greeks calculation for all option contracts that lie on a provided expiration.
- You might need to change the default expiration date to a different date if it is past the current date. Some quotes are omitted in the example to reduce the space of the sample output.
- Make `expiration` * if you want to get the snapshot for every expiration chain for the underlying.
> This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

    """
    def option_snapshot_greeks_second_order(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, stock_price:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None, use_market_value:Optional[bool]=False):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if stock_price is not None:
                query_parameters["stock_price"] = str(stock_price)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            if use_market_value is not None:
                query_parameters["use_market_value"] = str(use_market_value)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotGreeksSecondOrderRequestQuery(contract_spec=contract_spec)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if stock_price:
            query.stock_price = stock_price
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        if use_market_value:
            query.use_market_value = use_market_value
        request = endpoints_pb2.OptionSnapshotGreeksSecondOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotGreeksSecondOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_greeks_second_order({ symbol },{ expiration },{ strike },{ right },{ annual_dividend },{ rate_type },{ rate_value },{ stock_price },{ version },{ max_dte },{ strike_range },{ min_time },{ use_market_value })")
            else:
                raise e

    """- Retrieve a real-time last third order greeks calculation for all option contracts that lie on a provided expiration.
- You might need to change the default expiration date to a different date if it is past the current date. Some quotes are omitted in the example to reduce the space of the sample output.
- Make `expiration` * if you want to get the snapshot for every expiration chain for the underlying.
> This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

    """
    def option_snapshot_greeks_third_order(self, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, stock_price:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, min_time:Optional[Union[datetime.time, str]]=None, use_market_value:Optional[bool]=False):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if stock_price is not None:
                query_parameters["stock_price"] = str(stock_price)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            if use_market_value is not None:
                query_parameters["use_market_value"] = str(use_market_value)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionSnapshotGreeksThirdOrderRequestQuery(contract_spec=contract_spec)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if stock_price:
            query.stock_price = stock_price
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if min_time:
            query.min_time = _fmt_time(min_time)
        if use_market_value:
            query.use_market_value = use_market_value
        request = endpoints_pb2.OptionSnapshotGreeksThirdOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionSnapshotGreeksThirdOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_snapshot_greeks_third_order({ symbol },{ expiration },{ strike },{ right },{ annual_dividend },{ rate_type },{ rate_value },{ stock_price },{ version },{ max_dte },{ strike_range },{ min_time },{ use_market_value })")
            else:
                raise e

    """- Since [OPRA](/Articles/Data-And-Requests/The-SIPs.html) does not provide a national EOD report for options, Theta Data generates a national EOD report at 17:15 ET each day.
- ``created`` represents the datetime the report was generated and ``last_trade`` represents the datetime of the last trade. 
- The quote in the response represents the last NBBO reported by OPRA at the time of report generation. 
- You can read more about EOD & OHLC data [here](/Articles/Data-And-Requests/OHLC-EOD.html).

    """
    def option_history_eod(self, start_date:datetime.date, end_date:datetime.date, symbol:str, expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryEodRequestQuery(contract_spec=contract_spec)
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        request = endpoints_pb2.OptionHistoryEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_eod({ start_date },{ end_date },{ symbol },{ expiration },{ strike },{ right },{ max_dte },{ strike_range })")
            else:
                raise e

    """- Aggregated OHLC bars that use [SIP rules](/Articles/Data-And-Requests/OHLC-EOD.html) for each bar. 
- Time timestamp of the bar represents the opening time of the bar. For a trade to be part of the bar:  ``bar timestamp`` <= ``trade time`` < ``bar timestamp + interval``.
- Multi-day requests are limited to 1 month of data.

    """
    def option_history_ohlc(self, symbol:str, expiration:datetime.date, interval:str='1s', date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryOhlcRequestQuery(contract_spec=contract_spec)
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryOhlcRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryOhlc(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_ohlc({ symbol },{ expiration },{ interval },{ date },{ strike },{ right },{ start_time },{ end_time },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns every trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html). 
- Trade condition mappings can be found [here](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
- Extended trade conditions are not reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) for options, so they can be ignored.
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_trade(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryTradeRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryTradeRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryTrade(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_trade({ symbol },{ expiration },{ date },{ strike },{ right },{ start_time },{ end_time },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns every NBBO quote reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html). 
- If the ``interval`` parameter is specified, the quote for each interval represents the last quote at the interval's timestamp.
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_quote(self, symbol:str, expiration:Union[datetime.date, str], interval:str='1s', date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryQuoteRequestQuery(contract_spec=contract_spec)
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_quote({ symbol },{ expiration },{ interval },{ date },{ strike },{ right },{ start_time },{ end_time },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns every [trade](/operations/option_history_trade.html) reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) paired with the last NBBO quote reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) at the time of trade.
- A quote is matched with a trade if its timestamp ``<=`` the trade timestamp. 
- To match trades with quotes timestamps that are ``<`` the trade timestamp, specify the ``exclusive``parameter to ``true``. After thorough testing, we have determined that using ``exclusive=true`` might yield better results for various applications.
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_trade_quote(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), exclusive:Optional[bool]=True, max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if exclusive is not None:
                query_parameters["exclusive"] = str(exclusive)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryTradeQuoteRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if exclusive:
            query.exclusive = exclusive
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryTradeQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryTradeQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_trade_quote({ symbol },{ expiration },{ date },{ strike },{ right },{ start_time },{ end_time },{ exclusive },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Open Interest is normally reported once per day by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) at approximately 06:30 ET.
- A new open interest message might not be sent by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) if there is no open interest for the option contract.
- The reported open interest represents the open interest at the end of the previous trading day.

    """
    def option_history_open_interest(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryOpenInterestRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryOpenInterestRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryOpenInterest(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_open_interest({ symbol },{ expiration },{ date },{ strike },{ right },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration. 
- Uses Theta Data's EOD reports that get generated at 17:15 ET each day. The closing option price and closing underlying price are used for the greeks calculation.
- **Set `expiration` to ``*`` if you want to retrieve data for every option that shares the same ``symbol``. (note: Any ``expiration=*`` must be requested day by day)**

    """
    def option_history_greeks_eod(self, symbol:str, expiration:Union[datetime.date, str], start_date:datetime.date, end_date:datetime.date, strike:Optional[str]='*', right:Optional[str]='both', annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', underlyer_use_nbbo:Optional[bool]=False, max_dte:Optional[int]=None, strike_range:Optional[int]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if underlyer_use_nbbo is not None:
                query_parameters["underlyer_use_nbbo"] = str(underlyer_use_nbbo)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryGreeksEodRequestQuery(contract_spec=contract_spec)
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if underlyer_use_nbbo:
            query.underlyer_use_nbbo = underlyer_use_nbbo
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        request = endpoints_pb2.OptionHistoryGreeksEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryGreeksEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_greeks_eod({ symbol },{ expiration },{ start_date },{ end_date },{ strike },{ right },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ underlyer_use_nbbo },{ max_dte },{ strike_range })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration. 
- Calculated using the option and underlying midpoint price. If an interval size is specified (*highly recommended*), the option quote used in the calculation follows the same rules as the [quote](/operations/option_history_quote.html) endpoint. 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data.

    """
    def option_history_greeks_all(self, symbol:str, expiration:datetime.date, interval:str='1s', date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryGreeksAllRequestQuery(contract_spec=contract_spec)
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryGreeksAllRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryGreeksAll(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_greeks_all({ symbol },{ expiration },{ interval },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration. 
- Calculates greeks for every trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html).
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_trade_greeks_all(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryTradeGreeksAllRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryTradeGreeksAllRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryTradeGreeksAll(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_trade_greeks_all({ symbol },{ expiration },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration. 
- Calculated using the option and underlying midpoint price. If an interval size is specified (*highly recommended*), the option quote used in the calculation follows the same rules as the [quote](/operations/option_history_quote.html) endpoint. 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data.

    """
    def option_history_greeks_first_order(self, symbol:str, expiration:datetime.date, interval:str='1s', date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryGreeksFirstOrderRequestQuery(contract_spec=contract_spec)
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryGreeksFirstOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryGreeksFirstOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_greeks_first_order({ symbol },{ expiration },{ interval },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration.
- Calculates greeks for every trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html).
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_trade_greeks_first_order(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryTradeGreeksFirstOrderRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryTradeGreeksFirstOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryTradeGreeksFirstOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_trade_greeks_first_order({ symbol },{ expiration },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration. 
- Calculated using the option and underlying midpoint price. If an interval size is specified (*highly recommended*), the option quote used in the calculation follows the same rules as the [quote](/operations/option_history_quote.html) endpoint. 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data.

    """
    def option_history_greeks_second_order(self, symbol:str, expiration:datetime.date, interval:str='1s', date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryGreeksSecondOrderRequestQuery(contract_spec=contract_spec)
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryGreeksSecondOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryGreeksSecondOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_greeks_second_order({ symbol },{ expiration },{ interval },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration.
- Calculates greeks for every trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html).
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_trade_greeks_second_order(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryTradeGreeksSecondOrderRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryTradeGreeksSecondOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryTradeGreeksSecondOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_trade_greeks_second_order({ symbol },{ expiration },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration. 
- Calculated using the option and underlying midpoint price. If an interval size is specified (*highly recommended*), the option quote used in the calculation follows the same rules as the [quote](/operations/option_history_quote.html) endpoint. 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data.

    """
    def option_history_greeks_third_order(self, symbol:str, expiration:datetime.date, interval:str='1s', date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryGreeksThirdOrderRequestQuery(contract_spec=contract_spec)
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryGreeksThirdOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryGreeksThirdOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_greeks_third_order({ symbol },{ expiration },{ interval },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the data for all contracts that share the same provided symbol and expiration.
- Calculates greeks for every trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html).
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_trade_greeks_third_order(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryTradeGreeksThirdOrderRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryTradeGreeksThirdOrderRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryTradeGreeksThirdOrder(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_trade_greeks_third_order({ symbol },{ expiration },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns implied volatilies calculated using the national best bid, mid, and ask price of the option respectively. 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data.

    """
    def option_history_greeks_implied_volatility(self, symbol:str, expiration:datetime.date, interval:str='1s', date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=expiration.strftime('%Y-%m-%d'), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryGreeksImpliedVolatilityRequestQuery(contract_spec=contract_spec)
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryGreeksImpliedVolatilityRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryGreeksImpliedVolatility(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_greeks_implied_volatility({ symbol },{ expiration },{ interval },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns implied volatilies calculated using the trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html). 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

    """
    def option_history_trade_greeks_implied_volatility(self, symbol:str, expiration:Union[datetime.date, str], date:Optional[datetime.date]=None, strike:Optional[str]='*', right:Optional[str]='both', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), annual_dividend:Optional[float]=None, rate_type:Optional[str]='sofr', rate_value:Optional[float]=None, version:Optional[str]='latest', max_dte:Optional[int]=None, strike_range:Optional[int]=None, start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["expiration"] = str(expiration)
            if date is not None:
                query_parameters["date"] = str(date)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if annual_dividend is not None:
                query_parameters["annual_dividend"] = str(annual_dividend)
            if rate_type is not None:
                query_parameters["rate_type"] = str(rate_type)
            if rate_value is not None:
                query_parameters["rate_value"] = str(rate_value)
            if version is not None:
                query_parameters["version"] = str(version)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionHistoryTradeGreeksImpliedVolatilityRequestQuery(contract_spec=contract_spec)
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if annual_dividend:
            query.annual_dividend = annual_dividend
        if rate_type:
            query.rate_type = rate_type
        if rate_value:
            query.rate_value = rate_value
        if version:
            query.version = version
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionHistoryTradeGreeksImpliedVolatilityRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionHistoryTradeGreeksImpliedVolatility(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_history_trade_greeks_implied_volatility({ symbol },{ expiration },{ date },{ strike },{ right },{ start_time },{ end_time },{ annual_dividend },{ rate_type },{ rate_value },{ version },{ max_dte },{ strike_range },{ start_date },{ end_date })")
            else:
                raise e

    """- Returns the last trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) at a specified millisecond of the day.
- Trade condition mappings can be found [here](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
- Extended trade conditions are not reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) for options, so they can be ignored.
- The ``time_of_day``parameter represents the 00:00:00.000 ET that the trade should be provided for.

    """
    def option_at_time_trade(self, symbol:str, start_date:datetime.date, end_date:datetime.date, time_of_day:Union[datetime.time, str], expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            query_parameters["time_of_day"] = str(time_of_day)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionAtTimeTradeRequestQuery(contract_spec=contract_spec)
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        query.time_of_day = _fmt_time(time_of_day)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        request = endpoints_pb2.OptionAtTimeTradeRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionAtTimeTrade(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_at_time_trade({ symbol },{ start_date },{ end_date },{ time_of_day },{ expiration },{ strike },{ right },{ max_dte },{ strike_range })")
            else:
                raise e

    """- Returns the last NBBO quote reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) at a specified millisecond of the day.
- The ``time_of_day``parameter represents the 00:00:00.000 ET that the quote should be provided for.
- Using a sub-minute ``time_of_day`` (e.g. ``09:30:10.000``) will significantly slow the request and may cause it to hang, particularly when using ``expiration=*``. Use a minute-boundary time (e.g. ``09:30:00.000``) instead.

    """
    def option_at_time_quote(self, symbol:str, start_date:datetime.date, end_date:datetime.date, time_of_day:Union[datetime.time, str], expiration:Union[datetime.date, str], strike:Optional[str]='*', right:Optional[str]='both', max_dte:Optional[int]=None, strike_range:Optional[int]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            query_parameters["time_of_day"] = str(time_of_day)
            query_parameters["expiration"] = str(expiration)
            if strike is not None:
                query_parameters["strike"] = str(strike)
            if right is not None:
                query_parameters["right"] = str(right)
            if max_dte is not None:
                query_parameters["max_dte"] = str(max_dte)
            if strike_range is not None:
                query_parameters["strike_range"] = str(strike_range)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        contract_spec = ContractSpec(symbol=symbol, expiration=_fmt_if_date(expiration), strike=strike, right=right)
        query = endpoints_pb2.OptionAtTimeQuoteRequestQuery(contract_spec=contract_spec)
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        query.time_of_day = _fmt_time(time_of_day)
        if max_dte:
            query.max_dte = max_dte
        if strike_range:
            query.strike_range = strike_range
        request = endpoints_pb2.OptionAtTimeQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionAtTimeQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_at_time_quote({ symbol },{ start_date },{ end_date },{ time_of_day },{ expiration },{ strike },{ right },{ max_dte },{ strike_range })")
            else:
                raise e

    """A symbol can be defined as a unique identifier for a stock / underlying asset. Common terms also include: root, ticker, and underlying. This endpoint returns all traded symbols for options. This endpoint is updated overnight.

    """
    def index_list_symbols(self):
        try:
            query_parameters = {"client": "python"}
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexListSymbolsRequestQuery()
        request = endpoints_pb2.IndexListSymbolsRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexListSymbols(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_list_symbols()")
            else:
                raise e

    """Lists all dates of data that are available for a index with a given request type and symbol. This endpoint is updated overnight.

    """
    def index_list_dates(self, symbol:Union[List[str], str]):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexListDatesRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        request = endpoints_pb2.IndexListDatesRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexListDates(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_list_dates({ symbol })")
            else:
                raise e

    """- Retrieves the real-time current day OHLC.
- [Exchanges](/Articles/Data-And-Requests/The-SIPs.html) typically generate a price report every second for popular indices like SPX.

    """
    def index_snapshot_ohlc(self, symbol:Union[List[str], str], min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexSnapshotOhlcRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.IndexSnapshotOhlcRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexSnapshotOhlc(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_snapshot_ohlc({ symbol },{ min_time })")
            else:
                raise e

    """- Retrieves a real-time last index price.
- [Exchanges](/Articles/Data-And-Requests/The-SIPs.html) typically generate a price report every second for popular indices like SPX.

    """
    def index_snapshot_price(self, symbol:Union[List[str], str], min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexSnapshotPriceRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.IndexSnapshotPriceRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexSnapshotPrice(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_snapshot_price({ symbol },{ min_time })")
            else:
                raise e

    """- Retrieves a real-time last index market value.
- [Exchanges](/Articles/Data-And-Requests/The-SIPs.html) typically generate a price report every second for popular indices like SPX.

    """
    def index_snapshot_market_value(self, symbol:Union[List[str], str], min_time:Optional[Union[datetime.time, str]]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            if min_time is not None:
                query_parameters["min_time"] = str(min_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexSnapshotMarketValueRequestQuery()
        query.symbol.extend([symbol] if isinstance(symbol, str) else symbol)
        if min_time:
            query.min_time = _fmt_time(min_time)
        request = endpoints_pb2.IndexSnapshotMarketValueRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexSnapshotMarketValue(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_snapshot_market_value({ symbol },{ min_time })")
            else:
                raise e

    """- Since [the indices feeds](/Articles/Data-And-Requests/The-SIPs.html) do not provide a national EOD report, Theta Data generates a national EOD report at 17:15 each day.

    """
    def index_history_eod(self, symbol:str, start_date:datetime.date, end_date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexHistoryEodRequestQuery()
        query.symbol = symbol
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.IndexHistoryEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexHistoryEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_history_eod({ symbol },{ start_date },{ end_date })")
            else:
                raise e

    """- Aggregated OHLC bars that use [SIP rules](/Articles/Data-And-Requests/OHLC-EOD.html) for each bar.
- Time timestamp of the bar represents the opening time of the bar. For a trade to be part of the bar:  ``bar timestamp`` <= ``trade time`` < ``bar timestamp + interval``.
- [Exchanges](/Articles/Data-And-Requests/The-SIPs.html) typically generate a price report every second for popular indices like SPX.

    """
    def index_history_ohlc(self, symbol:str, start_date:datetime.date, end_date:datetime.date, interval:str='1s', start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00')):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            query_parameters["interval"] = str(interval)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexHistoryOhlcRequestQuery()
        query.symbol = symbol
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        query.interval = interval
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        request = endpoints_pb2.IndexHistoryOhlcRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexHistoryOhlc(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_history_ohlc({ symbol },{ start_date },{ end_date },{ interval },{ start_time },{ end_time })")
            else:
                raise e

    """- Retrieves historical indices price reports. [Exchanges](/Articles/Data-And-Requests/The-SIPs.html) typically generate a price report every second for popular indices like SPX.
- When the ``interval`` parameter is specified, the returned data represents the price at the exact time of each timestamp. If the timestamp in the response is 10:30:00, the price field represents the price at that exact time of the day.
- A price update from the exchange is omitted if the price remained the same from the previous update.
- Multi-day requests are limited to 1 month of data.

    """
    def index_history_price(self, symbol:str, interval:str='1s', date:Optional[datetime.date]=None, start_time:Optional[Union[datetime.time, str]]=_fmt_time('09:30:00'), end_time:Optional[Union[datetime.time, str]]=_fmt_time('16:00:00'), start_date:Optional[datetime.date]=None, end_date:Optional[datetime.date]=None):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["interval"] = str(interval)
            if date is not None:
                query_parameters["date"] = str(date)
            if start_time is not None:
                query_parameters["start_time"] = str(start_time)
            if end_time is not None:
                query_parameters["end_time"] = str(end_time)
            if start_date is not None:
                query_parameters["start_date"] = str(start_date)
            if end_date is not None:
                query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexHistoryPriceRequestQuery()
        query.symbol = symbol
        query.interval = interval
        if date:
            query.date = date.strftime('%Y-%m-%d')
        if start_time:
            query.start_time = _fmt_time(start_time)
        if end_time:
            query.end_time = _fmt_time(end_time)
        if start_date:
            query.start_date = start_date.strftime('%Y-%m-%d')
        if end_date:
            query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.IndexHistoryPriceRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexHistoryPrice(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_history_price({ symbol },{ interval },{ date },{ start_time },{ end_time },{ start_date },{ end_date })")
            else:
                raise e

    """- Retrieves historical indices price reports. [Exchanges](/Articles/Data-And-Requests/The-SIPs.html) typically generate a price report every second for popular indices like SPX.
- The ``time_of_day`` parameter represents the 00:00:00.000 ET that the price should be provided for.

    """
    def index_at_time_price(self, symbol:str, start_date:datetime.date, end_date:datetime.date, time_of_day:Union[datetime.time, str]):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            query_parameters["time_of_day"] = str(time_of_day)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexAtTimePriceRequestQuery()
        query.symbol = symbol
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        query.time_of_day = _fmt_time(time_of_day)
        request = endpoints_pb2.IndexAtTimePriceRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexAtTimePrice(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_at_time_price({ symbol },{ start_date },{ end_date },{ time_of_day })")
            else:
                raise e

    """- Retrieves current day equity market schedule
- *On days when the market closes early at 1:00 PM ET; eligible options will trade until 1:15 PM.
- **Some NYSE exchanges will continue late trading until 5:00 PM ET on early close days.

    """
    def calendar_open_today(self):
        try:
            query_parameters = {"client": "python"}
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.CalendarOpenTodayRequestQuery()
        request = endpoints_pb2.CalendarOpenTodayRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetCalendarOpenToday(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: calendar_open_today()")
            else:
                raise e

    """- Retrieves equity market schedule for a given date
- Note: Holiday data is available 01/01/2012 through the end of the calendar year that immediately follows the current year
- *On days when the market closes early at 1:00 PM ET; eligible options will trade until 1:15 PM.
- **Some NYSE exchanges will continue late trading until 5:00 PM ET on early close days.

    """
    def calendar_on_date(self, date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["date"] = str(date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.CalendarOnDateRequestQuery()
        query.date = date.strftime('%Y-%m-%d')
        request = endpoints_pb2.CalendarOnDateRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetCalendarOnDate(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: calendar_on_date({ date })")
            else:
                raise e

    """- Retrieves equity market holidays for a given year
- Note: Holiday data is available 01/01/2012 through the end of the calendar year that immediately follows the current year
- *On days when the market closes early at 1:00 PM ET; eligible options will trade until 1:15 PM.
- **Some NYSE exchanges will continue late trading until 5:00 PM ET on early close days.

    """
    def calendar_year(self, year:str):
        try:
            query_parameters = {"client": "python"}
            query_parameters["year"] = str(year)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.CalendarYearRequestQuery()
        query.year = year
        request = endpoints_pb2.CalendarYearRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetCalendarYear(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: calendar_year({ year })")
            else:
                raise e

    """- Returns the interest rate reported. Depending on the rate, reports can occur in the morning or the afternoon.

    """
    def interest_rate_history_eod(self, symbol:str, start_date:datetime.date, end_date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["symbol"] = str(symbol)
            query_parameters["start_date"] = str(start_date)
            query_parameters["end_date"] = str(end_date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.InterestRateHistoryEodRequestQuery()
        query.symbol = symbol
        query.start_date = start_date.strftime('%Y-%m-%d')
        query.end_date = end_date.strftime('%Y-%m-%d')
        request = endpoints_pb2.InterestRateHistoryEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetInterestRateHistoryEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: interest_rate_history_eod({ symbol },{ start_date },{ end_date })")
            else:
                raise e

    """Bulk download all option trade/quote ticks for a given date as a CSV stream. Returns one row per tick, grouped by contract. Requires a Professional options subscription.

Expected response time: ~3 minutes. Expected file size: ~1.2 GB.

Only the 7 most recent calendar days are available; data for the previous day is typically ready by 12:30-1am ET. See [Flat Files Getting Started](/Flat-Files/Getting-Started) for details, or [contact sales](mailto:sales@thetadata.net) for more history.

    """
    def option_flat_file_trade_quote(self, date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["date"] = str(date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.OptionFlatFileTradeQuoteRequestQuery()
        query.date = date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionFlatFileTradeQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionFlatFileTradeQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_flat_file_trade_quote({ date })")
            else:
                raise e

    """Bulk download all option end-of-day ticks for a given date as a CSV stream. Returns one row per tick, grouped by contract. Requires a Professional options subscription.

Expected response time: ~1 minute. Expected file size: ~150 MB.

Only the 7 most recent calendar days are available; data for the previous day is typically ready by 12:30-1am ET. See [Flat Files Getting Started](/Flat-Files/Getting-Started) for details, or [contact sales](mailto:sales@thetadata.net) for more history.

    """
    def option_flat_file_eod(self, date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["date"] = str(date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.OptionFlatFileEodRequestQuery()
        query.date = date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionFlatFileEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionFlatFileEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_flat_file_eod({ date })")
            else:
                raise e

    """Bulk download all option open interest ticks for a given date as a CSV stream. Returns one row per tick, grouped by contract. Requires a Professional options subscription.

Expected response time: ~1 minute. Expected file size: ~50 MB.

Only the 7 most recent calendar days are available; data for the previous day is typically ready by 12:30-1am ET. See [Flat Files Getting Started](/Flat-Files/Getting-Started) for details, or [contact sales](mailto:sales@thetadata.net) for more history.

    """
    def option_flat_file_open_interest(self, date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["date"] = str(date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.OptionFlatFileOpenInterestRequestQuery()
        query.date = date.strftime('%Y-%m-%d')
        request = endpoints_pb2.OptionFlatFileOpenInterestRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetOptionFlatFileOpenInterest(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: option_flat_file_open_interest({ date })")
            else:
                raise e

    """Bulk download all stock trade/quote ticks for a given date as a CSV stream. Returns one row per tick, grouped by symbol. Requires a Professional stock subscription.

Expected response time: ~30 minutes. Expected file size: ~14 GB. Make sure your client and connection can handle a long-running, multi-gigabyte download.

Only the 7 most recent calendar days are available; data for the previous day is typically ready by 12:30-1am ET. See [Flat Files Getting Started](/Flat-Files/Getting-Started) for details, or [contact sales](mailto:sales@thetadata.net) for more history.

    """
    def stock_flat_file_trade_quote(self, date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["date"] = str(date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockFlatFileTradeQuoteRequestQuery()
        query.date = date.strftime('%Y-%m-%d')
        request = endpoints_pb2.StockFlatFileTradeQuoteRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockFlatFileTradeQuote(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_flat_file_trade_quote({ date })")
            else:
                raise e

    """Bulk download all stock end-of-day ticks for a given date as a CSV stream. Returns one row per tick, grouped by symbol. Requires a Professional stock subscription.

Expected response time: ~1 second. Expected file size: ~1.5 MB.

Only the 7 most recent calendar days are available; data for the previous day is typically ready by 12:30-1am ET. See [Flat Files Getting Started](/Flat-Files/Getting-Started) for details, or [contact sales](mailto:sales@thetadata.net) for more history.

    """
    def stock_flat_file_eod(self, date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["date"] = str(date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.StockFlatFileEodRequestQuery()
        query.date = date.strftime('%Y-%m-%d')
        request = endpoints_pb2.StockFlatFileEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetStockFlatFileEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: stock_flat_file_eod({ date })")
            else:
                raise e

    """Bulk download all index end-of-day ticks for a given date as a CSV stream. Returns one row per tick, grouped by symbol. Requires a Professional indices subscription.

Expected response time: ~1 second. Expected file size: ~1 MB.

Only the 7 most recent calendar days are available; data for the previous day is typically ready by 12:30-1am ET. See [Flat Files Getting Started](/Flat-Files/Getting-Started) for details, or [contact sales](mailto:sales@thetadata.net) for more history.

    """
    def index_flat_file_eod(self, date:datetime.date):
        try:
            query_parameters = {"client": "python"}
            query_parameters["date"] = str(date)
            
        except Exception as query_parameters_error:
            logger.warning("Failed to build query_parameters for logging: %s", query_parameters_error)
            query_parameters = {"client": "python"}
        query_info = endpoints_pb2.QueryInfo(auth_token=self.auth_token, email_hint=self.email, query_parameters=query_parameters)
        query = endpoints_pb2.IndexFlatFileEodRequestQuery()
        query.date = date.strftime('%Y-%m-%d')
        request = endpoints_pb2.IndexFlatFileEodRequest(query_info=query_info, params=query)

        try:
            response_stream = self.stub.GetIndexFlatFileEod(request)
            return self._convert_response_stream(response_stream)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NoDataFoundError(f"No data found for: index_flat_file_eod({ date })")
            else:
                raise e
