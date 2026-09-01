from typing import overload
from enum import IntEnum
import abc
import datetime
import typing

import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.Results
import QuantConnect.Lean.Engine.TransactionHandlers
import QuantConnect.Orders
import QuantConnect.Securities
import System
import System.Collections.Concurrent
import System.Collections.Generic

QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_Callable = typing.TypeVar("QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_Callable")
QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_ReturnType")


class OrderRequestProcessingPool(System.Object, System.IDisposable):
    """
    Runs order requests on background worker threads that pull from a single shared queue. The pool grows on
    demand when the workers get saturated and keeps every request of an order processed in order.
    """

    @property
    def shutdown_deadline_reached(self) -> bool:
        """
        True once disposing has given the workers their shared deadline to drain normally: the requests
        drained after this point should be dropped by the request handler instead of processed
        """
        ...

    @property
    def is_active(self) -> bool:
        """True while the pool is processing order requests, false once it has been shut down."""
        ...

    @property
    def thread_count(self) -> int:
        """The number of worker threads currently running."""
        ...

    def __init__(self, concurrency_enabled: bool, minimum_threads: int, maximum_threads: int, process_request: typing.Callable[[QuantConnect.Orders.OrderRequest], typing.Any], on_error: typing.Callable[[System.Exception], typing.Any]) -> None:
        """
        Creates a threaded pool and starts its initial worker threads. When concurrency is enabled the pool
        starts at minimum_threads and grows on demand up to maximum_threads,
        otherwise it runs a single fixed worker thread.
        
        :param concurrency_enabled: True to grow the pool on demand, false to run a single worker thread
        :param minimum_threads: The number of worker threads the pool starts with when growing
        :param maximum_threads: The maximum number of worker threads the pool can grow to on demand
        :param process_request: Handles a single order request
        :param on_error: Invoked when processing fails unexpectedly
        """
        ...

    def dispatch(self, request: QuantConnect.Orders.OrderRequest, order: QuantConnect.Orders.Order) -> None:
        """
        Dispatches an order request to be processed. If the order already has a request in flight, the new one
        waits parked so its worker runs it next and the order stays in arrival order. Otherwise it is queued for
        any worker to pick up, growing the pool first when every worker is already busy.
        
        :param request: The order request to process
        :param order: The order the request belongs to, used to keep its requests ordered
        """
        ...

    def dispose(self) -> None:
        """
        Stops the pool. The requests still in the ready queue are drained through the normal processing loop:
        the surviving workers process them normally until the shared deadline, after which a last resort
        drainer thread drains the rest, dropped by the request handler through
        shutdown_deadline_reached. Parked follow up requests are left with their owning worker
        and are dropped with it. Workers that won't stop within the deadline are interrupted.
        """
        ...

    def process_pending(self) -> None:
        """
        Drains the pending order requests on the calling thread. Only used in synchronous mode, where there
        are no worker threads and the caller pumps the single queue itself.
        """
        ...

    @staticmethod
    def synchronous(process_request: typing.Callable[[QuantConnect.Orders.OrderRequest], typing.Any], on_error: typing.Callable[[System.Exception], typing.Any]) -> QuantConnect.Lean.Engine.TransactionHandlers.OrderRequestProcessingPool:
        """
        Creates a synchronous pool with no worker threads. Its single queue is drained on the caller thread
        via process_pending.
        
        :param process_request: Handles a single order request
        :param on_error: Invoked when processing fails unexpectedly
        """
        ...

    def wait_for_processing(self, timeout: datetime.timedelta) -> bool:
        """
        Waits until no order has requests in flight, up to the given timeout. In practice only the synchronous
        early return runs. The threaded branch below is defensive, since its callers only reach it in backtesting
        where the pool is synchronous, so it never runs in a live deployment.
        
        :param timeout: The maximum time to wait
        :returns: True if the pool was still processing when the timeout elapsed.
        """
        ...


class ITransactionHandler(QuantConnect.Securities.IOrderProcessor, QuantConnect.Securities.IOrderEventProvider, metaclass=abc.ABCMeta):
    """
    Transaction handlers define how the transactions are processed and set the order fill information.
    The pass this information back to the algorithm portfolio and ensure the cash and portfolio are synchronized.
    """

    @property
    @abc.abstractmethod
    def is_active(self) -> bool:
        """
        Boolean flag indicating the thread is busy.
        False indicates it is completely finished processing and ready to be terminated.
        """
        ...

    @property
    @abc.abstractmethod
    def orders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]:
        """Gets the permanent storage for all orders"""
        ...

    @property
    @abc.abstractmethod
    def order_events(self) -> typing.Iterable[QuantConnect.Orders.OrderEvent]:
        """Gets all order events"""
        ...

    @property
    @abc.abstractmethod
    def order_tickets(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.OrderTicket]:
        """Gets the permanent storage for all order tickets"""
        ...

    def add_open_order(self, order: QuantConnect.Orders.Order, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """Register an already open Order"""
        ...

    def exit(self) -> None:
        """Signal a end of thread request to stop montioring the transactions."""
        ...

    def initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm, brokerage: QuantConnect.Interfaces.IBrokerage, result_handler: QuantConnect.Lean.Engine.Results.IResultHandler) -> None:
        """Initializes the transaction handler for the specified algorithm using the specified brokerage implementation"""
        ...

    def process_synchronous_events(self) -> None:
        """Process any synchronous events from the primary algorithm thread."""
        ...


class CancelPendingOrders(System.Object):
    """Class used to keep track of CancelPending orders and their original or updated status"""

    @property
    def get_cancel_pending_orders_size(self) -> int:
        """Amount of CancelPending Orders"""
        ...

    def remove_and_fallback(self, order: QuantConnect.Orders.Order) -> None:
        """
        Removes an order which we failed to cancel and falls back the order Status to previous value
        
        :param order: The order that failed to be canceled
        """
        ...

    def set(self, order_id: int, status: QuantConnect.Orders.OrderStatus) -> None:
        """
        Adds an order which will be canceled and we want to keep track of it Status in case of fallback
        
        :param order_id: The order id
        :param status: The order Status, before the cancel request
        """
        ...

    def update_or_remove(self, order_id: int, new_status: QuantConnect.Orders.OrderStatus) -> None:
        """
        Updates an order that is pending to be canceled.
        
        :param new_status: The new status of the order. If its OrderStatus.Canceled or OrderStatus.Filled it will be removed
        :param order_id: The id of the order
        """
        ...


class BrokerageTransactionHandler(System.Object, QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler):
    """Transaction handler for all brokerages"""

    LIQUIDATE_FROM_DELISTING_TAG: str = "Liquidate from delisting"
    """The tag used for order events of liquidations triggered by a delisting"""

    @property
    def _cancel_pending_orders(self) -> QuantConnect.Lean.Engine.TransactionHandlers.CancelPendingOrders:
        """
        The _cancelPendingOrders instance will help to keep track of CancelPending orders and their Status
        
        
        This Property is protected.
        """
        ...

    @property
    def new_order_event(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Orders.OrderEvent], typing.Any], typing.Any]:
        """Event fired when there is a new OrderEvent"""
        ...

    @new_order_event.setter
    def new_order_event(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Orders.OrderEvent], typing.Any], typing.Any]) -> None:
        ...

    @property
    def orders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]:
        """Gets the permanent storage for all orders"""
        ...

    @property
    def order_events(self) -> typing.Iterable[QuantConnect.Orders.OrderEvent]:
        """Gets all order events"""
        ...

    @property
    def order_tickets(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.OrderTicket]:
        """Gets the permanent storage for all order tickets"""
        ...

    @property
    def orders_count(self) -> int:
        """Gets the current number of orders that have been processed"""
        ...

    @property
    def concurrency_enabled(self) -> bool:
        """
        Whether the transaction thread pool can grow on demand to process order requests concurrently.
        When false a single worker thread is used.
        
        
        This Property is protected.
        """
        ...

    @property
    def synchronous_processing(self) -> bool:
        """
        Whether order requests are drained synchronously by the algorithm thread instead of by background
        worker threads. Used by backtesting deployments.
        
        
        This Property is protected.
        """
        ...

    @property
    def maximum_transaction_threads(self) -> int:
        """
        The maximum number of transaction threads the pool can grow to
        
        
        This Property is protected.
        """
        ...

    @property
    def minimum_transaction_threads(self) -> int:
        """
        The number of transaction threads the pool starts with
        
        
        This Property is protected.
        """
        ...

    @property
    def processing_threads_count(self) -> int:
        """
        The number of transaction threads currently running
        
        
        This Property is protected.
        """
        ...

    @property
    def is_active(self) -> bool:
        """
        Boolean flag indicating the transaction threads are busy.
        False indicates they are completely finished processing and ready to be terminated.
        """
        ...

    @property
    def time_since_last_fill(self) -> datetime.timedelta:
        """
        Gets the amount of time since the last call to algorithm.Portfolio.ProcessFill(fill)
        
        
        This Property is protected.
        """
        ...

    @property
    def current_time_utc(self) -> datetime.datetime:
        """
        Gets current time UTC. This is here to facilitate testing
        
        
        This Property is protected.
        """
        ...

    def add_open_order(self, order: QuantConnect.Orders.Order, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """Register an already open Order"""
        ...

    def add_order(self, request: QuantConnect.Orders.SubmitOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """
        Add an order to collection and return the unique order id or negative if an error.
        
        :param request: A request detailing the order to be submitted
        :returns: New unique, increasing orderid.
        """
        ...

    def cancel_order(self, request: QuantConnect.Orders.CancelOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """
        Remove this order from outstanding queue: user is requesting a cancel.
        
        :param request: Request containing the specific order id to remove
        """
        ...

    def exit(self) -> None:
        """Signal a end of thread request to stop monitoring the transactions."""
        ...

    def get_open_orders(self, filter: typing.Callable[[QuantConnect.Orders.Order], bool] = None) -> typing.List[QuantConnect.Orders.Order]:
        """
        Gets open orders matching the specified filter
        
        :param filter: Delegate used to filter the orders
        :returns: All open orders this order provider currently holds.
        """
        ...

    def get_open_order_tickets(self, filter: typing.Callable[[QuantConnect.Orders.OrderTicket], bool] = None) -> typing.Sequence[QuantConnect.Orders.OrderTicket]:
        """
        Gets and enumerable of opened OrderTicket matching the specified filter
        
        :param filter: The filter predicate used to find the required order tickets
        :returns: An enumerable of opened OrderTicket matching the specified filter.
        """
        ...

    def get_order_by_id(self, order_id: int) -> QuantConnect.Orders.Order:
        """
        Get the order by its id
        
        :param order_id: Order id to fetch
        :returns: A clone of the order with the specified id, or null if no match is found.
        """
        ...

    def get_orders(self, filter: typing.Callable[[QuantConnect.Orders.Order], bool] = None) -> typing.Sequence[QuantConnect.Orders.Order]:
        """
        Gets all orders matching the specified filter. Specifying null will return an enumerable
        of all orders.
        
        :param filter: Delegate used to filter the orders
        :returns: All orders this order provider currently holds by the specified filter.
        """
        ...

    def get_orders_by_brokerage_id(self, brokerage_id: str) -> typing.List[QuantConnect.Orders.Order]:
        """
        Gets the order by its brokerage id
        
        :param brokerage_id: The brokerage id to fetch
        :returns: The first order matching the brokerage id, or null if no match is found.
        """
        ...

    def get_order_ticket(self, order_id: int) -> QuantConnect.Orders.OrderTicket:
        """
        Gets the order ticket for the specified order id. Returns null if not found
        
        :param order_id: The order's id
        :returns: The order ticket with the specified id, or null if not found.
        """
        ...

    def get_order_tickets(self, filter: typing.Callable[[QuantConnect.Orders.OrderTicket], bool] = None) -> typing.Sequence[QuantConnect.Orders.OrderTicket]:
        """
        Gets and enumerable of OrderTicket matching the specified filter
        
        :param filter: The filter predicate used to find the required order tickets
        :returns: An enumerable of OrderTicket matching the specified filter.
        """
        ...

    def get_projected_holdings(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.ProjectedHoldings:
        """
        Calculates the projected holdings for the specified security based on the current open orders.
        
        :param security: The security
        :returns: The projected holdings for the specified security, which is the sum of the current holdings
        plus the sum of the open orders quantity.
        """
        ...

    def handle_order_request(self, request: QuantConnect.Orders.OrderRequest) -> None:
        """
        Handles a generic order request
        
        :param request: OrderRequest to be handled
        :returns: OrderResponse for request.
        """
        ...

    def initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm, brokerage: QuantConnect.Interfaces.IBrokerage, result_handler: QuantConnect.Lean.Engine.Results.IResultHandler) -> None:
        """
        Creates a new BrokerageTransactionHandler to process orders using the specified brokerage implementation
        
        :param algorithm: The algorithm instance
        :param brokerage: The brokerage implementation to process orders and fire fill events
        :param result_handler: 
        """
        ...

    def initialize_transaction_thread(self) -> None:
        """
        Create and start the transaction thread, who will be in charge of processing
        the order requests
        
        
        This Class is protected.
        """
        ...

    def process(self, request: QuantConnect.Orders.OrderRequest) -> QuantConnect.Orders.OrderTicket:
        """
        Adds the specified order to be processed
        
        :param request: The order to be processed
        """
        ...

    def process_asynchronous_events(self) -> None:
        """Processes asynchronous events on the transaction handler's thread"""
        ...

    def process_pending_requests(self) -> None:
        """
        Drains the pending order requests on the calling thread. Used by synchronous (non concurrent)
        deployments, where the algorithm thread pumps the request queue itself.
        
        
        This Class is protected.
        """
        ...

    def process_synchronous_events(self) -> None:
        """Processes all synchronous events that must take place before the next time loop for the algorithm"""
        ...

    def round_off_order(self, order: QuantConnect.Orders.Order, security: QuantConnect.Securities.Security) -> float:
        """Rounds off the order towards 0 to the nearest multiple of Lot Size"""
        ...

    @overload
    def round_order_prices(self, order: QuantConnect.Orders.Order, security: QuantConnect.Securities.Security) -> None:
        """
        Rounds the order prices to its security minimum price variation.
        
        This procedure is needed to meet brokerage precision requirements.
        
        
        This Class is protected.
        """
        ...

    @overload
    def round_order_prices(self, order: QuantConnect.Orders.Order, security: QuantConnect.Securities.Security, combo_is_ready: bool, orders: System.Collections.Generic.Dictionary[QuantConnect.Orders.Order, QuantConnect.Securities.Security]) -> None:
        """
        Rounds the order prices to its security minimum price variation.
        
        This procedure is needed to meet brokerage precision requirements.
        
        
        This Class is protected.
        """
        ...

    def update_order(self, request: QuantConnect.Orders.UpdateOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """
        Update an order yet to be filled such as stop or limit orders.
        
        :param request: Request detailing how the order should be updated
        """
        ...

    def wait_for_order_submission(self, ticket: QuantConnect.Orders.OrderTicket) -> None:
        """
        Wait for the order to be handled by the _threadPool
        
        This Class is protected.
        
        :param ticket: The OrderTicket expecting to be submitted
        """
        ...


class BacktestingTransactionHandler(QuantConnect.Lean.Engine.TransactionHandlers.BrokerageTransactionHandler):
    """This transaction handler is used for processing transactions during backtests"""

    @property
    def current_time_utc(self) -> datetime.datetime:
        """
        Gets current time UTC. This is here to facilitate testing
        
        
        This Property is protected.
        """
        ...

    @property
    def synchronous_processing(self) -> bool:
        """
        For backtesting order requests are processed synchronously by the algorithm thread, only live
        deployments with a concurrency enabled brokerage use background transaction threads
        
        
        This Property is protected.
        """
        ...

    def initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm, brokerage: QuantConnect.Interfaces.IBrokerage, result_handler: QuantConnect.Lean.Engine.Results.IResultHandler) -> None:
        """
        Creates a new BacktestingTransactionHandler using the BacktestingBrokerage
        
        :param algorithm: The algorithm instance
        :param brokerage: The BacktestingBrokerage
        :param result_handler: 
        """
        ...

    def process_asynchronous_events(self) -> None:
        """Processes asynchronous events on the transaction handler's thread"""
        ...

    def process_synchronous_events(self) -> None:
        """Processes all synchronous events that must take place before the next time loop for the algorithm"""
        ...

    def wait_for_order_submission(self, ticket: QuantConnect.Orders.OrderTicket) -> None:
        """
        For backtesting we will submit the order ourselves
        
        
        This Class is protected.
        
        :param ticket: The OrderTicket expecting to be submitted
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_Callable, QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Lean_Engine_TransactionHandlers__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


