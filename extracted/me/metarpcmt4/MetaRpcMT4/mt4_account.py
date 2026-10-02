import asyncio
import grpc
import uuid
from datetime import datetime
from typing import Optional, Callable, Awaitable, AsyncGenerator, Any
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.empty_pb2 import Empty

# import your generated stubs
import MetaRpcMT4.mt4_term_api_connection_pb2 as connection_pb2
import MetaRpcMT4.mt4_term_api_connection_pb2_grpc as connection_pb2_grpc
import MetaRpcMT4.mt4_term_api_account_helper_pb2 as account_helper_pb2
import MetaRpcMT4.mt4_term_api_account_helper_pb2_grpc as account_helper_pb2_grpc
import MetaRpcMT4.mt4_term_api_trading_helper_pb2 as trading_helper_pb2
import MetaRpcMT4.mt4_term_api_trading_helper_pb2_grpc as trading_helper_pb2_grpc
import MetaRpcMT4.mt4_term_api_market_info_pb2 as market_info_pb2
import MetaRpcMT4.mt4_term_api_market_info_pb2_grpc as market_info_pb2_grpc
import MetaRpcMT4.mt4_term_api_subscriptions_pb2 as subscriptions_pb2
import MetaRpcMT4.mt4_term_api_subscriptions_pb2_grpc as subscriptions_pb2_grpc
import MetaRpcMT4.mt4_term_api_market_info_pb2 as market_info_pb2
import MetaRpcMT4.mt4_term_api_market_info_pb2_grpc as market_info_pb2_grpc



# === Custom exceptions (like in your C# code) ===
class ConnectExceptionMT4(Exception):
    pass


class ApiExceptionMT4(Exception):
    def __init__(self, error):
        super().__init__(str(error))
        self.error = error


# === MT5Account Class ===
class MT4Account:
    def __init__(self, user: int, password: str, grpc_server: Optional[str] = None, id_: Optional[str] = None, api_key: Optional[str] = None):
        self.user = user
        self.password = password
        self.grpc_server = grpc_server or "mt4.mrpc.pro:443"   # default server
        self.id = id_
        self.api_key = api_key or "TRIAL"

        # Async gRPC secure channel (TLS)
        self.channel = grpc.aio.secure_channel(
            self.grpc_server,
            grpc.ssl_channel_credentials()
        )

        # Init stubs directly (like in C#)
        self.connection_client = connection_pb2_grpc.ConnectionStub(self.channel)
        self.subscription_client = subscriptions_pb2_grpc.SubscriptionServiceStub(self.channel)
        self.account_client = account_helper_pb2_grpc.AccountHelperStub(self.channel)
        self.trade_client = trading_helper_pb2_grpc.TradingHelperStub(self.channel)
        self.market_info_client = market_info_pb2_grpc.MarketInfoStub(self.channel)

        # Connection state
        self.host = None
        self.port = None
        self.server_name = None
        self.connect_timeout_seconds = 30


    # === Utility: headers ===
    def get_headers(self):
        headers = []
        if self.id:
            headers.append(("id", str(self.id)))
        headers.append(("apikey", str(getattr(self, "api_key", None) or "TRIAL")))
        return headers

    async def disconnect(self):
        """
        Disconnect from MT4 server by sending Disconnect request, then close the gRPC channel.
        """
        try:
            if hasattr(self, 'connection_client') and self.connection_client:
                request = connection_pb2.DisconnectRequest()
                await self.connection_client.Disconnect(request, metadata=self.get_headers(), timeout=10)
        except Exception:
            pass
        finally:
            if hasattr(self, 'channel') and self.channel is not None:
                try:
                    await self.channel.close()
                except Exception:
                    pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    # === Utility: reconnect ===
    async def reconnect(self, deadline: Optional[datetime] = None):
        if self.server_name:
            await self.connect_by_server_name(self.server_name, True, self.connect_timeout_seconds, deadline)
        elif self.host:
            await self.connect_by_host_port(self.host, self.port or 443, True, self.connect_timeout_seconds, deadline)

    # === Core retry wrapper ===
    async def execute_with_reconnect(
        self,
        grpc_call: Callable[[list[tuple[str, str]]], Awaitable[Any]],
        error_selector: Callable[[Any], Optional[Any]],
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        while cancellation_event is None or not cancellation_event.is_set():
            headers = self.get_headers()
            try:
                res = await grpc_call(headers)
            except grpc.aio.AioRpcError as ex:
                if ex.code() == grpc.StatusCode.UNAVAILABLE:
                    await asyncio.sleep(0.5)
                    await self.reconnect(deadline)
                    continue
                raise

            error = error_selector(res)
            if error and error.error_code in ("TERMINAL_INSTANCE_NOT_FOUND", "TERMINAL_REGISTRY_TERMINAL_NOT_FOUND"):
                await asyncio.sleep(0.5)
                await self.reconnect(deadline)
                continue

            if res.HasField("error") and res.error.error_message:
                raise ApiExceptionMT4(res.error)

            return res

        raise asyncio.CancelledError("The operation was canceled by the caller.")

    # === Connect methods ===
    async def connect_by_host_port(
        self,
        host: str,
        port: int = 443,
        wait_for_terminal_is_alive: bool = True,
        timeout_seconds: int = 30,
        deadline: Optional[datetime] = None,
        base_chart_symbol: Optional[str] = None,
        *args,
        **kwargs,
    ):
        if isinstance(wait_for_terminal_is_alive, str):
            wait_for_terminal_is_alive = True

        # Build connect request (from your proto)
        request = connection_pb2.ConnectRequest(
            user=self.user,
            password=self.password,
            host=host,
            port=port,
            timeout_seconds=timeout_seconds,
        )

        headers = []
        if self.id:
            headers.append(("id", str(self.id)))
        
        res = await self.connection_client.Connect(
            request,
            metadata=headers,
            timeout=30.0 if deadline is None else (deadline - datetime.utcnow()).total_seconds(),
        )
        
        if res.HasField("error") and res.error.error_message:
            raise ApiExceptionMT4(res.error)

        # Save state
        self.host = host
        self.port = port
        self.connect_timeout_seconds = timeout_seconds
        self.id = getattr(res.data, "terminal_instance_guid", getattr(res.data, "terminalInstanceGuid", None))

    async def connect_by_server_name(
        self,
        server_name: str,
        wait_for_terminal_is_alive: bool = True,
        timeout_seconds: int = 30,
        deadline: Optional[datetime] = None,
        base_chart_symbol: Optional[str] = None,
        *args,
        **kwargs,
    ):
        if isinstance(wait_for_terminal_is_alive, str):
            wait_for_terminal_is_alive = True

        # Build connect request (from your proto)
        request = connection_pb2.ConnectExRequest(
            user=self.user,
            password=self.password,
            mt_cluster_name=server_name,
            timeout_seconds=timeout_seconds,
        )

        headers = []
        if self.id:
            headers.append(("id", str(self.id)))
        res = await self.connection_client.ConnectEx(
            request,
            metadata=headers,
            timeout=30.0 if deadline is None else (deadline - datetime.utcnow()).total_seconds(),
        )

        if res.HasField("error") and res.error.error_message:
            raise ApiExceptionMT4(res.error)

        # Save state
        self.server_name = server_name
        self.connect_timeout_seconds = timeout_seconds
        self.id = res.data.terminal_instance_guid


#
#    Account helper --------------------------------------------------------------------------------------------------------
#    

    async def account_summary(
        self,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Gets the summary information for a trading account asynchronously.

        Args:
            deadline (datetime, optional): Deadline after which the request will be canceled
                if not completed.
            cancellation_event (asyncio.Event, optional): Event to cancel the request.

        Returns:
            AccountSummaryData: The server's response containing account summary data.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an error in the response.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
        """
        if not (self.host or self.server_name):
            raise ConnectExceptionMT4("Please call connect method first")

        request = account_helper_pb2.AccountSummaryRequest()

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = (deadline - datetime.utcnow()).total_seconds()
                if timeout < 0:
                    timeout = 0
            return await self.account_client.AccountSummary(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )

        return res.data

    async def opened_orders(
        self,
        sort_mode: account_helper_pb2.EnumOpenedOrderSortType = account_helper_pb2.EnumOpenedOrderSortType.SORT_BY_OPEN_TIME_ASC,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Gets the currently opened orders and positions for the connected account asynchronously.

        Args:
            sort_mode (EnumOpenedOrderSortType): The sort mode for the opened orders
                (e.g. SORT_BY_OPEN_TIME_ASC, SORT_BY_ORDER_TICKET_ID_DESC).
            deadline (datetime, optional): Deadline after which the request will be canceled
                if not completed.
            cancellation_event (asyncio.Event, optional): Event to cancel the request.

        Returns:
            OpenedOrdersData: The result containing opened orders and positions.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an error in the response.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        # Build request
        request = account_helper_pb2.OpenedOrdersRequest(sort_type=sort_mode)

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = (deadline - datetime.utcnow()).total_seconds()
                if timeout < 0:
                    timeout = 0
            return await self.account_client.OpenedOrders(
                request,
                metadata=headers,
                timeout=timeout,
            )

        # Execute with automatic reconnect logic
        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )

        return res.data


    async def opened_orders_tickets(
        self,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Gets the list of tickets for all currently opened orders.

        Returns:
            OpenedOrdersTicketsData: The result containing the list of tickets.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an error in the response.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        request = account_helper_pb2.OpenedOrdersTicketsRequest()

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = (deadline - datetime.utcnow()).total_seconds()
                if timeout < 0:
                    timeout = 0
            return await self.account_client.OpenedOrdersTickets(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )

        return res.data


    async def orders_history(
        self,
        sort_mode: account_helper_pb2.EnumOrderHistorySortType = account_helper_pb2.EnumOrderHistorySortType.HISTORY_SORT_BY_CLOSE_TIME_DESC,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        page_number: Optional[int] = None,
        items_per_page: Optional[int] = None,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Gets the order history for the connected account.

        Args:
            sort_mode (EnumOrderHistorySortType): Sorting mode for orders.
            from_time (datetime, optional): Start of the history period.
            to_time (datetime, optional): End of the history period.
            page_number (int, optional): Page number for pagination.
            items_per_page (int, optional): Items per page.

        Returns:
            OrdersHistoryData: The result containing historical orders.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an error in the response.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        # Convert datetime → Timestamp (protobuf)
        ts_from = None
        ts_to = None
        if from_time:
            ts_from = Timestamp()
            ts_from.FromDatetime(from_time)
        if to_time:
            ts_to = Timestamp()
            ts_to.FromDatetime(to_time)

        request = account_helper_pb2.OrdersHistoryRequest(
            input_sort_mode=sort_mode,
            input_from=ts_from,
            input_to=ts_to,
            page_number=page_number,
            items_per_page=items_per_page,
        )

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = (deadline - datetime.utcnow()).total_seconds()
                if timeout < 0:
                    timeout = 0
            return await self.account_client.OrdersHistory(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )

        return res.data


    async def symbol_params_many(
        self,
        symbol_name: Optional[str] = None,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Retrieves symbol parameters (for one or all symbols).

        Args:
            symbol_name (str, optional): Symbol name. If None, returns all.

        Returns:
            SymbolParamsManyData: The result containing symbol parameters.
        
        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an error in the response.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        request = account_helper_pb2.SymbolParamsManyRequest(symbol_name=symbol_name or "")

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = (deadline - datetime.utcnow()).total_seconds()
                if timeout < 0:
                    timeout = 0
            return await self.account_client.SymbolParamsMany(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )

        return res.data


    async def tick_value_with_size(
        self,
        symbol_names: list[str],
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Gets tick value, tick size, and contract size for multiple symbols.

        Args:
            symbol_names (list[str]): List of symbol names.

        Returns: 
            TickValueWithSizeData: The result containing tick values and sizes.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an error in the response.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        request = account_helper_pb2.TickValueWithSizeRequest(symbol_names=symbol_names)

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = (deadline - datetime.utcnow()).total_seconds()
                if timeout < 0:
                    timeout = 0
            return await self.account_client.TickValueWithSize(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )

        return res.data

#
#    Streams --------------------------------------------------------------------------------------------------------
#    

    async def execute_stream_with_reconnect(
        self,
        request: Any,
        stream_invoker: Callable[[Any, list[tuple[str, str]]], grpc.aio.StreamStreamCall],
        get_error: Callable[[Any], Optional[Any]],
        get_data: Callable[[Any], Any],
        cancellation_event: Optional[asyncio.Event] = None,
    ) -> AsyncGenerator[Any, None]:
        """
        Executes a gRPC server-streaming call with automatic reconnection logic on recoverable errors.

        Args:
            request: The request object to initiate the stream with.
            stream_invoker (Callable): A function that opens the stream. It receives the request and metadata headers,
                and returns an async streaming call.
            get_error (Callable): A function that extracts the error object (if any) from a reply.
                Return an object with .error_code == "TERMINAL_INSTANCE_NOT_FOUND" to trigger reconnect,
                or any non-null error to raise ApiExceptionMT5.
            get_data (Callable): A function that extracts the data object from a reply. If it returns None, the
                message is skipped.
            cancellation_event (asyncio.Event, optional): Event to cancel streaming and reconnection attempts.

        Yields:
            Extracted data items streamed from the server.

        Raises:
            ConnectExceptionMT4: If reconnection logic fails due to missing account context.
            ApiExceptionMT4: When the stream response contains a known API error.
            grpc.aio.AioRpcError: If a non-recoverable gRPC error occurs.
        """
        while cancellation_event is None or not cancellation_event.is_set():
            reconnect_required = False
            stream = None
            try:
                stream = stream_invoker(request, self.get_headers())
                async for reply in stream:
                    error = get_error(reply)

                    if error and error.error_code in (
                        "TERMINAL_INSTANCE_NOT_FOUND",
                        "TERMINAL_REGISTRY_TERMINAL_NOT_FOUND",
                    ):
                        reconnect_required = True
                        break

                    if error and getattr(error, "message", None):
                        raise ApiExceptionMT4(error)

                    data = get_data(reply)
                    if data is not None:
                        yield data

            except grpc.aio.AioRpcError as ex:
                if ex.code() == grpc.StatusCode.UNAVAILABLE:
                    reconnect_required = True
                else:
                    raise

            finally:
                if stream:
                    stream.cancel()  # close stream properly

            if reconnect_required:
                await asyncio.sleep(0.5)
                await self.reconnect()
            else:
                break


    async def on_symbol_tick(
        self,
        symbols: list[str],
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Subscribes to real-time tick data for specified symbols.

        Args:
            symbols (list[str]): The symbol names to subscribe to.
            cancellation_event (asyncio.Event, optional): Event to cancel streaming.

        Yields:
            OnSymbolTickData: Async stream of tick data responses.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an error in the stream.
            grpc.aio.AioRpcError: If the stream fails due to communication or protocol errors.
        """
        if not self.id:
            raise ConnectExceptionMT4("Please call connect method first")

        request = subscriptions_pb2.OnSymbolTickRequest()
        request.symbol_names.extend(symbols)

        async for data in self.execute_stream_with_reconnect(
            request=request,
            stream_invoker=lambda req, headers: self.subscription_client.OnSymbolTick(req, metadata=headers),
            get_error=lambda reply: reply.error,
            get_data=lambda reply: reply.data,
            cancellation_event=cancellation_event,
        ):
            yield data

    async def on_trade(
        self,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Subscribes to all trade-related events: orders, deals, positions.

        Args:
            cancellation_event (asyncio.Event, optional): Event to cancel streaming.

        Yields:
            OnTradeData: Trade event data.

        Raises:
            ConnectExceptionMT4: If the account is not connected.
            ApiExceptionMT4: If the server returns a known API error.
            grpc.aio.AioRpcError: If the stream fails due to communication or protocol errors.
        """
        if not self.id:
            raise ConnectExceptionMT4("Please call connect method first")

        request = subscriptions_pb2.OnTradeRequest()

        async for data in self.execute_stream_with_reconnect(
            request=request,
            stream_invoker=lambda req, headers: self.subscription_client.OnTrade(req, metadata=headers),
            get_error=lambda reply: reply.error,
            get_data=lambda reply: reply.data,
            cancellation_event=cancellation_event,
        ):
            yield data


    async def on_opened_orders_tickets(
        self,
        pull_interval_milliseconds: int = 500,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Subscribes to live lists of opened order tickets (positions & pending orders).

        Args:
            pull_interval_milliseconds (int): Server-side polling interval.
            cancellation_event (asyncio.Event, optional): Event to cancel streaming.

        Yields:
            OnOpenedOrdersTicketsData

        Raises:
            ConnectExceptionMT4: If the account is not connected.
            ApiExceptionMT4: If the server returns a known API error.
            grpc.aio.AioRpcError: If the stream fails due to communication or protocol errors.
        """
        if not self.id:
            raise ConnectExceptionMT4("Please call connect method first")

        request = subscriptions_pb2.OnOpenedOrdersTicketsRequest(
            pull_interval_milliseconds=pull_interval_milliseconds
        )

        async for data in self.execute_stream_with_reconnect(
            request=request,
            stream_invoker=lambda req, headers: self.subscription_client.OnOpenedOrdersTickets(
                req, metadata=headers
            ),
            get_error=lambda reply: reply.error,
            get_data=lambda reply: reply.data,
            cancellation_event=cancellation_event,
        ):
            yield data


    async def on_opened_orders_profit(
        self,
        timer_period_milliseconds: int = 1000,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Subscribes to real-time profit updates for opened orders (plus account snapshot).

        Args:
            timer_period_milliseconds (int): Server timer period for updates.
            cancellation_event (asyncio.Event, optional): Event to cancel streaming.

        Yields:
            OnOpenedOrdersProfitData

        Raises:
            ConnectExceptionMT4: If the account is not connected.
            ApiExceptionMT4: If the server returns a known API error.
            grpc.aio.AioRpcError: If the stream fails due to communication or protocol errors.
        """
        if not self.id:
            raise ConnectExceptionMT4("Please call connect method first")

        request = subscriptions_pb2.OnOpenedOrdersProfitRequest(
            timer_period_milliseconds=timer_period_milliseconds
        )

        async for data in self.execute_stream_with_reconnect(
            request=request,
            stream_invoker=lambda req, headers: self.subscription_client.OnOpenedOrdersProfit(
                req, metadata=headers
            ),
            get_error=lambda reply: reply.error,
            get_data=lambda reply: reply.data,
            cancellation_event=cancellation_event,
        ):
            yield data


#
# Trade functions --------------------------------------------------------------------------------------------------------
#
    async def order_send(
        self,
        symbol: str,
        operation_type: trading_helper_pb2.OrderSendOperationType,
        volume: float,
        price: Optional[float] = None,
        slippage: Optional[int] = None,
        stoploss: Optional[float] = None,
        takeprofit: Optional[float] = None,
        comment: Optional[str] = None,
        magic_number: Optional[int] = None,
        expiration: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Opens a new trade order (market or pending).

        Args:
            symbol (str): Symbol to trade, e.g. "EURUSD".
            operation_type (OrderSendOperationType): Operation type (BUY, SELL, BUYLIMIT, etc.).
            volume (float): Trade volume in lots.
            price (float, optional): Open price for pending orders.
            slippage (int, optional): Allowed price deviation in points.
            stoploss (float, optional): Stop loss price.
            takeprofit (float, optional): Take profit price.
            comment (str, optional): Comment for the order.
            magic_number (int, optional): Custom magic number to identify the order.
            expiration (datetime, optional): Expiration time for pending orders.
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the operation.

        Returns:
            OrderSendData: The server's response containing new order details.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        req = trading_helper_pb2.OrderSendRequest(
            symbol=symbol,
            operation_type=operation_type,
            volume=volume,
        )
        if price is not None:
            req.price = price
        if slippage is not None:
            req.slippage = slippage
        if stoploss is not None:
            req.stoploss = stoploss
        if takeprofit is not None:
            req.takeprofit = takeprofit
        if comment:
            req.comment = comment
        if magic_number is not None:
            req.magic_number = magic_number
        if expiration:
            ts = Timestamp()
            ts.FromDatetime(expiration)
            req.expiration.CopyFrom(ts)

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.trade_client.OrderSend(req, metadata=headers, timeout=timeout)

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data


    async def order_modify(
        self,
        order_ticket: int,
        new_price: Optional[float] = None,
        new_stop_loss: Optional[float] = None,
        new_take_profit: Optional[float] = None,
        new_expiration: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Modifies an existing order (price, SL/TP, expiration).

        Args:
            order_ticket (int): Ticket number of the order to modify.
            new_price (float, optional): New open price.
            new_stop_loss (float, optional): New stop loss.
            new_take_profit (float, optional): New take profit.
            new_expiration (datetime, optional): New expiration time.
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the operation.

        Returns:
            OrderModifyData: The server's response containing modification result.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        req = trading_helper_pb2.OrderModifyRequest(order_ticket=order_ticket)
        if new_price is not None:
            req.new_price = new_price
        if new_stop_loss is not None:
            req.new_stop_loss = new_stop_loss
        if new_take_profit is not None:
            req.new_take_profit = new_take_profit
        if new_expiration:
            ts = Timestamp()
            ts.FromDatetime(new_expiration)
            req.new_expiration.CopyFrom(ts)

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.trade_client.OrderModify(req, metadata=headers, timeout=timeout)

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data


    async def order_close_delete(
        self,
        order_ticket: int,
        lots: Optional[float] = None,
        closing_price: Optional[float] = None,
        slippage: Optional[int] = None,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Closes or deletes an order (market or pending).

        Args:
            order_ticket (int): Ticket of the order to close or delete.
            lots (float, optional): Volume to close (for partial close).
            closing_price (float, optional): Desired closing price.
            slippage (int, optional): Allowed price deviation in points.
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the operation.

        Returns:
            OrderCloseDeleteData: The server's response indicating close/delete status.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        req = trading_helper_pb2.OrderCloseDeleteRequest(order_ticket=order_ticket)
        if lots is not None:
            req.lots = lots
        if closing_price is not None:
            req.closing_price = closing_price
        if slippage is not None:
            req.slippage = slippage

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.trade_client.OrderCloseDelete(req, metadata=headers, timeout=timeout)

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data


    async def order_close_by(
        self,
        ticket_to_close: int,
        opposite_ticket_closing_by: int,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Closes one position by another (close-by operation).

        Args:
            ticket_to_close (int): Ticket of the order being closed.
            opposite_ticket_closing_by (int): Opposite ticket to close by.
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the operation.

        Returns:
            OrderCloseByData: The server's response containing close-by result.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        req = trading_helper_pb2.OrderCloseByRequest(
            ticket_to_close=ticket_to_close,
            opposite_ticket_closing_by=opposite_ticket_closing_by,
        )

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.trade_client.OrderCloseBy(req, metadata=headers, timeout=timeout)

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data

#
# Market info --------------------------------------------------------------------------------------------------------
#

    async def quote(
        self,
        symbol: str,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Retrieves the latest quote for a single symbol.

        Args:
            symbol (str): The symbol name (e.g., "EURUSD").
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the request.

        Returns:
            QuoteData: The latest bid/ask/high/low prices with timestamp.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        request = market_info_pb2.QuoteRequest(symbol=symbol)

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.market_info_client.Quote(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data


    async def quote_many(
        self,
        symbols: list[str],
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Retrieves quotes for multiple symbols.

        Args:
            symbols (list[str]): List of symbol names (e.g., ["EURUSD", "GBPUSD"]).
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the request.

        Returns:
            QuoteManyData: The response containing quotes for all requested symbols.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        request = market_info_pb2.QuoteManyRequest(symbols=symbols)

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.market_info_client.QuoteMany(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data


    async def symbols(
        self,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Retrieves the full list of tradable symbols from the connected terminal.

        Args:
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the request.

        Returns:
            SymbolsData: The response containing all available symbol names and indices.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        request = market_info_pb2.SymbolsRequest()

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.market_info_client.Symbols(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data


    async def quote_history(
        self,
        symbol: str,
        timeframe: market_info_pb2.ENUM_QUOTE_HISTORY_TIMEFRAME,
        from_time: datetime,
        to_time: datetime,
        deadline: Optional[datetime] = None,
        cancellation_event: Optional[asyncio.Event] = None,
    ):
        """
        Retrieves historical OHLC quotes for a symbol within a specified time range.

        Args:
            symbol (str): The symbol name (e.g., "EURUSD").
            timeframe (ENUM_QUOTE_HISTORY_TIMEFRAME): The timeframe (e.g., QH_PERIOD_H1).
            from_time (datetime): Start of the requested historical period.
            to_time (datetime): End of the requested historical period.
            deadline (datetime, optional): Deadline for the gRPC request.
            cancellation_event (asyncio.Event, optional): Event to cancel the request.

        Returns:
            QuoteHistoryData: The server's response containing OHLC and volume data.

        Raises:
            ConnectExceptionMT4: If the account is not connected before calling this method.
            ApiExceptionMT4: If the server returns an API error.
            grpc.aio.AioRpcError: If the gRPC call fails due to communication or protocol errors.
            asyncio.CancelledError: If cancelled via `cancellation_event`.
        """
        if not (self.host or self.server_name or self.id):
            raise ConnectExceptionMT4("Please call connect method first")

        ts_from = Timestamp()
        ts_from.FromDatetime(from_time)
        ts_to = Timestamp()
        ts_to.FromDatetime(to_time)

        request = market_info_pb2.QuoteHistoryRequest(
            symbol=symbol,
            timeframe=timeframe,
            fromTime=ts_from,
            toTime=ts_to,
        )

        async def grpc_call(headers):
            timeout = None
            if deadline:
                timeout = max((deadline - datetime.utcnow()).total_seconds(), 0)
            return await self.market_info_client.QuoteHistory(
                request,
                metadata=headers,
                timeout=timeout,
            )

        res = await self.execute_with_reconnect(
            grpc_call=grpc_call,
            error_selector=lambda r: getattr(r, "error", None),
            deadline=deadline,
            cancellation_event=cancellation_event,
        )
        return res.data
