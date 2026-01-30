"""
The tool to check the availability or syntax of domain, IP or URL.

-- The process manager library for and from the PyFunceble project.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This is the module that provides the core components of our worker manager.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025, 2026 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import logging
import multiprocessing
import multiprocessing.connection
import multiprocessing.queues
import multiprocessing.synchronize
import queue
import time
import traceback
from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional

logger = logging.getLogger("PyFunceble.ext.process_manager")


class WorkerCore(multiprocessing.Process):
    """
    Provides the core of the worker manager.
    """

    RESERVED_MESSAGES: List[str] = ["__wait__", "__stop__", "__immediate_shutdown__"]
    """
    This is the list of reserved messages that are used by the worker manager.

    .. warning::
        Messages listed above are reserved. They are used by the worker manager
        and should not be used as part of your own downstream workers and logic.
    """

    SHARING_DELAY_SECONDS: float = 2.0
    """
    This is the number of seconds to wait before sharing a message.

    .. note::
        This is the default value when :prop:`sharing_delay` is not set.
    """

    SHUTDOWN_DELAY_SECONDS: float = 2.0
    """
    This is the number of seconds to wait before shutting down the worker after
    receiving a stop signal.

    .. note::
        This is the default value when :prop:`shutdown_delay` is not set.
    """

    FETCH_DELAY_SECONDS: float = 0.0
    """
    This is the number of seconds to wait before fetching the next dataset.

    .. note::
        This is the default value when :prop:`fetch_delay` is not set.
    """

    input_queue: Optional[multiprocessing.queues.Queue] = None
    """
    Stores and exposes the input queue of the worker.
    """

    output_queues: Optional[List[multiprocessing.queues.Queue]] = None
    """
    Stores and exposes the output queue of the worker.
    """

    configuration_queue: Optional[multiprocessing.queues.Queue] = None
    """
    Stores and exposes the configuration queue of the worker.
    """

    global_exit_event: Optional[multiprocessing.synchronize.Event] = None
    """
    Stores and exposes the global exit event of the worker.

    The global exit event is used to tell the worker to stop its work.

    When initialized, it will be a :code:`multiprocessing.Event()` object.
    """

    exit_event: Optional[multiprocessing.synchronize.Event] = None
    """
    Stores and exposes the (local) exit event of the worker.

    The local exit event is used to tell the worker to stop its work.

    When initialized, it will be a :code:`multiprocessing.Event()` object.
    """

    daemon: Optional[bool] = None
    """
    Stores and exposes the daemon status of the worker.

    When set to :code:`True`, the worker will be a daemon.
    """

    spread_stop_signal: Optional[bool] = None
    """
    Whether we have to spread the stop signal to the output queue(s) of the
    worker(s).
    """

    spread_wait_signal: Optional[bool] = None
    """
    Whether we have to spread the wait signal to the output queue(s) of the
    worker(s).
    """

    concurrent_workers_names: Optional[List[str]] = None
    """
    Stores and exposes the names of the concurrent workers.
    """

    dependent_workers_names: Optional[List[str]] = None
    """
    Stores and exposes the names of the dependent workers.
    This should be the name of the workers that reads from our output queues -
    which is the input queue for them.

    .. note::
        Defining this attribute unlocks some of the dependencies features.
    """

    controlling_workers_name: Optional[str] = None
    """
    Stores and exposes the name of the controlling worker.

    This should be the name of the workers that sends to our input queue -
    which is one of the output queues for them.

    .. note::
        Not implemented yet.
    """

    targeted_processing: Optional[bool] = None
    """
    Whether the worker should strictly process data that are intended for it.

    .. note::
        When set to :code:`True`, the worker will only process data that are
        intended for it. If the data are not intended for it, the worker will
        push the data back to the input queue.

        When set to :code:`False`, the worker will process all data that are
        pushed to the input queue.
    """

    delay_message_sharing: Optional[bool] = None
    """
    Whether we have to delay the sharing of the message to queue(s).
    """

    delay_shutdown: Optional[bool] = None
    """
    Whether we have to delay the shutdown of the worker.

    .. note::
        This is useful when you just want to be able to stop the worker but
        not immediately.

    .. warning::
        When set to :code:`True`, the worker will wait for :prop:`shutdown_delay`
        seconds before shutting down.
    """

    raise_exception: Optional[bool] = None
    """
    Whether we have to raise any exception or just store/share it.
    """

    _name: str = None
    """
    The name of the worker.
    """

    _sharing_delay: Optional[float] = None
    """
    The number of seconds to wait before sharing the message.
    """

    _shutdown_delay: Optional[float] = None
    """
    The number of seconds to wait before shutting down the worker.
    """

    _fetch_delay: Optional[float] = None
    """
    The number of seconds to wait before fetching the next dataset.
    """

    _parent_connection: Optional[multiprocessing.connection.Connection] = None
    """
    The parent connection that is used to receive exceptions from the child
    process.
    """

    _child_connection: Optional[multiprocessing.connection.Connection] = None
    """
    The child connection that is used to send exceptions to the parent process.
    """

    _exception: Optional[multiprocessing.connection.Pipe] = None
    """
    The exception pipe that is used to store the exception.
    """

    _extra_args: Optional[dict] = None
    """
    The extra arguments that were passed to the worker through the
    :code:`kwargs` parameter.
    """

    _all_args: Optional[dict] = None
    """
    Exposes all arguments that were passed to the worker.

    This instance exists to allow child classes to access the arguments that were
    passed to the worker.
    """

    def __init__(
        self,
        name: str,
        *,
        global_exit_event: multiprocessing.synchronize.Event,
        input_queue: Optional[multiprocessing.queues.Queue] = None,
        output_queues: Optional[multiprocessing.queues.Queue] = None,
        configuration_queue: Optional[multiprocessing.queues.Queue] = None,
        daemon: bool = False,
        spread_stop_signal: bool = True,
        spread_wait_signal: bool = True,
        delay_message_sharing: bool = False,
        delay_shutdown: bool = False,
        raise_exception: bool = False,
        targeted_processing: bool = True,
        sharing_delay: Optional[float] = None,
        shutdown_delay: Optional[float] = None,
        fetch_delay: Optional[float] = None,
        concurrent_workers_names: Optional[List[str]] = None,
        dependent_workers_names: Optional[List[str]] = None,
        controlling_workers_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.name = name
        self.input_queue = input_queue
        self.output_queues = output_queues
        self.configuration_queue = configuration_queue

        self.spread_stop_signal = spread_stop_signal
        self.spread_wait_signal = spread_wait_signal

        self.delay_message_sharing = delay_message_sharing
        self.delay_shutdown = delay_shutdown
        self.raise_exception = raise_exception
        self.targeted_processing = targeted_processing

        self.daemon = daemon

        self.global_exit_event = global_exit_event
        self.exit_event = multiprocessing.Event()

        self._parent_connection, self._child_connection = multiprocessing.Pipe()

        self.concurrent_workers_names = []
        self.dependent_workers_names = []

        if concurrent_workers_names is not None:
            self.concurrent_workers_names = concurrent_workers_names

        if dependent_workers_names is not None:
            self.dependent_workers_names = dependent_workers_names

        if controlling_workers_name is not None:
            self.controlling_workers_name = controlling_workers_name

        if sharing_delay is not None:
            self.sharing_delay = sharing_delay

        if shutdown_delay is not None:
            self.shutdown_delay = shutdown_delay

        if fetch_delay is not None:
            self.fetch_delay = fetch_delay

        self._extra_args = kwargs

        self._all_args = {
            "name": name,
            "global_exit_event": global_exit_event,
            "input_queue": input_queue,
            "output_queues": output_queues,
            "configuration_queue": configuration_queue,
            "daemon": daemon,
            "spread_stop_signal": spread_stop_signal,
            "spread_wait_signal": spread_wait_signal,
            "delay_message_sharing": delay_message_sharing,
            "delay_shutdown": delay_shutdown,
            "raise_exception": raise_exception,
            "targeted_processing": targeted_processing,
            "sharing_delay": sharing_delay,
            "shutdown_delay": shutdown_delay,
            "fetch_delay": fetch_delay,
            "concurrent_workers_names": concurrent_workers_names,
            "dependent_workers_names": dependent_workers_names,
            **kwargs,
        }

        super().__init__(name=name, daemon=daemon)

        self.__post_init__()

    def __post_init__(self) -> None:
        """
        Called after the initialization of the worker, this method can be used
        by the child class to initialize their own workflows.
        """

    def __del__(self) -> None:
        """
        Destroys the worker.
        """

        if self._parent_connection:
            self._parent_connection.close()

        if self._child_connection:
            self._child_connection.close()

    def __getattr__(self, attribute: str) -> Any:
        """
        Provides the value of the given attribute.

        :param str attribute:
            The attribute to get the value of.
        """

        if self._extra_args and attribute in self._extra_args:
            return self._extra_args[attribute]

        raise AttributeError(f"{self.__class__.__name__} has no attribute {attribute}")

    @property
    def name(self) -> str:
        """
        Provides the name of the worker.
        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets the name of the worker.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._name = value

    @property
    def sharing_delay(self) -> Optional[float]:
        """
        Provides the value of the :py:attr:`_sharing_delay` attribute.
        """

        return self._sharing_delay or self.SHARING_DELAY_SECONDS

    @sharing_delay.setter
    def sharing_delay(self, value: float) -> None:
        """
        Sets the value of the :py:attr:`_sharing_delay` attribute.

        :param float value:
            The value to set.

        :raise TypeError:
            When the given value is not a :py:class:`int` or a :py:class:`float`.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"<value> should be {int} or {float}, {type(value)} given.")

        self._sharing_delay = float(value)

    @property
    def shutdown_delay(self) -> Optional[float]:
        """
        Provides the value of the :py:attr:`_shutdown_delay` attribute.
        """

        if (
            self._shutdown_delay is None
            or self._shutdown_delay < self.SHUTDOWN_DELAY_SECONDS
        ):
            return self.SHUTDOWN_DELAY_SECONDS

        return self._shutdown_delay

    @shutdown_delay.setter
    def shutdown_delay(self, value: float) -> None:
        """
        Sets the value of the :py:attr:`_shutdown_delay` attribute.

        :param float value:
            The value to set.

        :raise TypeError:
            When the given value is not a :py:class:`int` or a :py:class:`float`.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"<value> should be {int} or {float}, {type(value)} given.")

        self._shutdown_delay = float(value)

    @property
    def fetch_delay(self) -> Optional[float]:
        """
        Provides the value of the :py:attr:`_fetch_delay` attribute.
        """

        if self._fetch_delay is None or self._fetch_delay < self.FETCH_DELAY_SECONDS:
            return self.FETCH_DELAY_SECONDS

        return self._fetch_delay

    @fetch_delay.setter
    def fetch_delay(self, value: float) -> None:
        """
        Sets the value of the :py:attr:`_fetch_delay` attribute.

        :param float value:
            The value to set.

        :raise TypeError:
            When the given value is not a :py:class:`int` or a :py:class:`float`.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"<value> should be {int} or {float}, {type(value)} given.")

        self._fetch_delay = float(value)

    @property
    def exception(self) -> Optional[multiprocessing.connection.Pipe]:
        """
        Provides the exception pipe.
        """

        if self._parent_connection.poll():
            self._exception = self._parent_connection.recv()

        return self._exception

    def push_to_input_queue(
        self,
        data: Any,
        *,
        source_worker: Optional[str] = None,
        destination_worker: Optional[str] = None,
    ) -> "WorkerCore":
        """
        Pushes the given data to the input queue of the worker.

        :param data:
            The data to push to the input queue.
        :param source_worker:
            The name of the worker which pushed the data.

            .. note::
                When not given, we assume that that we are the source worker.
        :param destination_worker:
            The name of the worker which is supposed to receive the data.
        """

        if source_worker:
            to_send = (source_worker, destination_worker, data)
        else:
            to_send = (self.name, destination_worker, data)

        if self.input_queue:
            self.input_queue.put(to_send)

            logger.debug("%s | Pushed to (input) queue: %r", self.name, to_send)
        else:  # pragma: no cover
            logger.debug(
                "%s | No input queue to push to. Discarding the following data: %r",
                self.name,
                to_send,
            )

        return self

    def push_to_output_queues(
        self,
        data: Any,
        *,
        source_worker: Optional[str] = None,
        destination_worker: Optional[str] = None,
    ) -> "WorkerCore":
        """
        Pushes the given data to the output queue of the worker.

        :param data:
            The data to push to the output queue.
        :param source_worker:
            The name of the worker which pushed the data.

            .. note::
                When not given, we assume that that we are the source worker.
        :param destination_worker:
            The name of the worker which is supposed to receive the data.
        """

        if source_worker:
            to_send = (source_worker, destination_worker, data)
        else:
            to_send = (self.name, destination_worker, data)

        if self.output_queues:
            for output_queue in self.output_queues:
                output_queue.put(to_send)

            logger.debug("%s | Pushed to (input) queues: %r", self.name, to_send)
        else:  # pragma: no cover
            logger.debug(
                "%s | No output queue to push to. Discarding the following data: %r",
                self.name,
                to_send,
            )

        return self

    def push_to_configuration_queue(
        self,
        data: Any,
        *,
        source_worker: Optional[str] = None,
        destination_worker: Optional[str] = None,
    ) -> "WorkerCore":
        """
        Pushes the given data to the configuration queue of the worker.

        :param data:
            The data to push to the configuration queue.
        :param source_worker:
            The name of the worker which pushed the data.

            .. note::
                When not given, we assume that that we are the source worker.
        :param destination_worker:
            The name of the worker which is supposed to receive the data.
        """

        if source_worker:
            to_send = (source_worker, destination_worker, data)
        else:
            to_send = (self.name, destination_worker, data)

        if self.configuration_queue:
            self.configuration_queue.put(to_send)

            logger.debug("%s | Pushed to (configuration) queue: %r", self.name, to_send)
        else:  # pragma: no cover
            logger.debug(
                "%s | No configuration queue to push to. Discarding the "
                "following data: %r",
                self.name,
                to_send,
            )

        return self

    def target(self, consumed: Any) -> Any:
        """
        This is the target what is executed by the worker.

        This method should be overwritten by the child class and it should return
        the data to push to the output queue.
        """

        return consumed

    def share_message(
        self,
        message: Any,
        *,
        overall: bool = False,
        input_queue_only: bool = False,
        output_queue_only: bool = False,
        apply_delay: bool = False,
    ) -> "WorkerCore":
        """
        Shares a message to all output queues.

        :param message:
            The message to share.
        :param overall:
            Share the message back to ourself, our concurrent workers and the
            dependent workers.
        :param input_queue_only:
            Whether we should share the message to the input queue only.
        :param output_queue_only:
            Whether we should share the message to the output queues only.
        :param apply_delay:
            Whether we should apply a delay before sharing the message.

            .. note::
                If :ivar:`delay_message_sharing` is set to :code:`True`, the delay
                will be applied regardless of the value of this parameter.
        """

        if self.delay_message_sharing or apply_delay:
            time.sleep(self.sharing_delay)

        if overall:
            if input_queue_only or not output_queue_only:
                # send to ourself - to make sure that we are not stuck.
                self.push_to_input_queue(message, destination_worker=self.name)

            if input_queue_only or not output_queue_only:
                # send to our concurrent workers.
                for worker_name in self.concurrent_workers_names:
                    if self.delay_message_sharing or apply_delay:
                        time.sleep(self.sharing_delay)

                    self.push_to_input_queue(message, destination_worker=worker_name)

            if output_queue_only or not input_queue_only:
                if self.dependent_workers_names:
                    for worker_name in self.dependent_workers_names:
                        if self.delay_message_sharing or apply_delay:
                            time.sleep(self.sharing_delay)

                        self.push_to_output_queues(
                            message, destination_worker=worker_name
                        )
                elif self.output_queues:
                    for _ in range(len(self.output_queues)):
                        self.push_to_output_queues(message)
        else:
            if input_queue_only or not output_queue_only:
                self.push_to_input_queue(message)

            if output_queue_only or not input_queue_only:
                self.push_to_output_queues(message)

        return self

    def share_wait_signal(
        self,
        *,
        overall: bool = False,
        output_queue_only: bool = False,
        input_queue_only: bool = False,
        apply_delay: bool = False,
    ) -> "WorkerCore":
        """
        Shares a message to all output queues.

        The message is a wait message.

        :param overall:
            Share the message to all output queues.
        :param output_queue_only:
            Whether we should share the message to the output queues only.
        :param input_queue_only:
            Whether we should share the message to the input queue only.
        :param apply_delay:
            Whether we should apply a delay before sharing the message.
        """

        return self.share_message(
            "__wait__",
            overall=overall,
            output_queue_only=output_queue_only,
            input_queue_only=input_queue_only,
            apply_delay=apply_delay,
        )

    def share_stop_signal(
        self,
        *,
        overall: bool = False,
        output_queue_only: bool = False,
        input_queue_only: bool = False,
        apply_delay: bool = False,
    ) -> "WorkerCore":
        """
        Shares a message to all input or output queues.

        The message is a stop message.

        :param overall:
            Share the message to all output queues.
        :param output_queue_only:
            Whether we should share the message to the output queues only.
        :param input_queue_only:
            Whether we should share the message to the input queue only.
        :param apply_delay:
            Whether we should apply a delay before sharing the message.
        """

        return self.share_message(
            "__stop__",
            overall=overall,
            output_queue_only=output_queue_only,
            input_queue_only=input_queue_only,
            apply_delay=apply_delay,
        )

    def take_a_break(self, *, mode: str = "standard") -> "WorkerCore":
        """
        Proceed to take a break - when necessary.

        :param str mode:
            The mode of the break. It can be one of the following:

            - :code:`standard` - Take a break before further processing.
              In this mode we will sleep for :ivar:`fetch_delay` seconds.

            - :code:`shutdown` - Take a break before shutting down the worker.
              In this mode we will sleep for :ivar:`shutdown_delay` seconds.
        """

        if mode == "shutdown":
            if self.delay_shutdown:
                logger.debug(
                    "%s | Delaying shutdown. Sleeping for %s seconds.",
                    self.name,
                    self.shutdown_delay,
                )

                time.sleep(self.shutdown_delay)
            return self

        if mode == "standard":
            logger.debug(
                "%s | Taking a break. Sleeping for %s seconds.",
                self.name,
                self.fetch_delay,
            )

            time.sleep(self.fetch_delay)

            return self

        return self

    def perform_external_preflight_checks(self) -> bool:
        """
        An external preflight check that can be used to provides some checks or
        controls before we start ingesting the next dataset - in the loop.

        .. note::
            This method should be overwritten by the child class.

        :return:
            The result of the preflight checks.

            When set to :py:class:`False`, the worker will consider that the
            preflight checks failed and will reiterate the ingestion process from the
            beginning.

            When set to :py:class:`True`, the worker will consider that the preflight
            checks passed and will start the ingestion of the next dataset.
        """

        logger.debug("%s | Predefined preflight checks passed.", self.name)

        return True

    def perform_external_poweron_checks(self) -> bool:
        """
        An external poweron check that can be used to provides some checks or
        controls before we poweron the worker.

        .. note::
            This method should be overwritten by the child class.

        :return:
            The result of the poweron checks.

            When set to :py:class:`False`, the worker will consider that the
            poweron checks failed and will stop the worker.

            When set to :py:class:`True`, the worker will consider that the poweron
            checks passed and will start the ingestion of the first dataset.
        """

        logger.debug("%s | Predefined poweron checks passed.", self.name)

        return True

    def perform_external_poweroff_checks(self) -> bool:
        """
        An external poweroff check that can be used to provides some checks or
        controls before we poweroff the worker.

        .. note::
            This method should be overwritten by the child class.

        :return:
            The result of the poweroff checks.

            It is expected to be a :py:class`bool` value; but it won't be used be
            evaluated - yet.
        """

        logger.debug("%s | Predefined poweroff checks passed.", self.name)

        return True

    def perform_external_inflight_checks(self, consumed: Any) -> bool:
        """
        An external inflight check that can be used to provides some checks or
        controls after we ingested the dataset but before we process it.

        .. note::
            This method should be overwritten by the child class.

        :param consumed:
            The dataset that was consumed.

        :return:
            The result of the inflight checks.

            When set to :py:class:`False`, the worker will consider that the
            inflight checks failed and will drop the consumed dataset and reiterate
            the ingestion process from the beginning.

            When set to :py:class:`True`, the worker will consider that the inflight
            checks passed and will start the processing of the dataset.
        """

        logger.debug(
            "%s | Predefined inflight checks passed for:\n%r", self.name, consumed
        )

        return True

    def perform_external_postflight_checks(self, produced: Any) -> bool:
        """
        An external postflight check that can be used to provides some checks or
        controls after we ingested and processed the dataset - in the loop.

        .. note::
            This method should be overwritten by the child class.

        :param produced:
            The dataset that was produced by :meth:`target`.

        :return:
            The result of the postflight checks.

            When set to :py:class:`False`, the worker will consider that the
            postflight checks failed and will reiterate the ingestion process from the
            beginning.

            When set to :py:class:`True`, the worker will consider that the postflight
            checks passed and will start the ingestion of the next dataset.
        """

        logger.debug(
            "%s | Predefined postflight checks passed for:\n%r.", self.name, produced
        )

        return True

    def run(self) -> "WorkerCore":  # pylint: disable=too-many-branches
        """
        This is the brain of the worker. It coordinates how the worker should
        behave and interact with the other workers.
        """

        def shutdown_time_reached():  # pragma: no cover
            return datetime.now(timezone.utc) > shutdown_time

        if not self.perform_external_poweron_checks():  # pragma: no cover
            logger.debug("%s | Poweron checks failed. Stopping worker.", self.name)

            self.exit_event.set()
            return self

        if self.delay_shutdown:  # pragma: no cover
            shutdown_time = datetime.now(timezone.utc) + timedelta(
                seconds=self.shutdown_delay
            )
        else:
            shutdown_time = datetime.now(timezone.utc) + timedelta(days=365)

        try:
            while True:
                if self.global_exit_event.is_set():
                    logger.debug(
                        "%s | Global exit event set. Stopping worker.", self.name
                    )

                    self.exit_event.set()
                    self.take_a_break(mode="shutdown")
                    break

                if self.exit_event.is_set():
                    logger.debug(
                        "%s | Local exit event set. Stopping worker.", self.name
                    )

                    self.take_a_break(mode="shutdown")
                    break

                if shutdown_time_reached():  # pragma: no cover
                    logger.debug(
                        "%s | Shutdown time reached. Stopping worker.", self.name
                    )

                    self.exit_event.set()
                    continue

                if not self.perform_external_preflight_checks():  # pragma: no cover
                    logger.debug(
                        "%s | Preflight checks failed. Reiterating the "
                        "ingestion process.",
                        self.name,
                    )
                    self.take_a_break()
                    continue

                # We are now ready to process the data.
                # but before we do that, we have to check if we have to
                # take a break.
                self.take_a_break()

                try:
                    logger.debug("%s | Waiting for message.", self.name)
                    worker_name, destination_worker, consumed = self.input_queue.get()
                except queue.Empty:  # pragma: no cover
                    logger.debug("%s | No message to consume.", self.name)
                    continue
                except (EOFError, KeyboardInterrupt):  # pragma: no cover
                    logger.debug(
                        "%s | EOFError or KeyboardInterrupt while waiting. "
                        "Stopping worker.",
                        self.name,
                    )

                    try:
                        self.global_exit_event.set()
                        continue
                    except ConnectionResetError:
                        logger.debug(
                            "%s | ConnectionResetError. Stopping worker.", self.name
                        )

                        break
                except TypeError:  # pragma: no cover
                    logger.debug("%s | No valid message to consume.", self.name)
                    continue

                if (
                    self.targeted_processing
                    and destination_worker
                    and destination_worker != self.name
                ):  # pragma: no cover
                    logger.debug(
                        "%s | Message not for us. Pushing the following message "
                        "back to the input queue: %r",
                        self.name,
                        consumed,
                    )

                    # Message is not for us.
                    self.push_to_input_queue(
                        consumed,
                        source_worker=worker_name,
                        destination_worker=destination_worker,
                    )
                    continue

                logger.debug(
                    "%s | Consumed from %s: %r", self.name, worker_name, consumed
                )

                if consumed == "__immediate_shutdown__":  # pragma: no cover
                    # A shutdown signal was received.
                    # A shutdown signal comes from scaling. Therefore, we don't
                    # handle it as a soft signal with a possible delay or spreading.

                    logger.debug(
                        "%s | Shutdown signal received from %s. Stopping worker.",
                        self.name,
                        worker_name,
                    )

                    # If a shutdown came, we have to stop the worker silently,
                    # without spreading the stop signal.
                    self.exit_event.set()

                    continue

                if consumed == "__stop__":
                    # A stop signal was received.

                    # We have to delay the shutdown of the worker.
                    # So we will silently continue the loop.
                    # Meaning that we will still be able to process data
                    # but we will stop the worker when the
                    # shutdown_time_reached is True.

                    if self.delay_shutdown:  # pragma: no cover
                        # We have to delay the shutdown of the worker. Therefore,
                        # we will silently continue and keeping any processing
                        # pipeline alive by sending a wait signal to every worker.
                        self.share_wait_signal(overall=self.spread_wait_signal)

                        logger.debug(
                            "%s | Stop signal received. Delaying shutdown.",
                            self.name,
                        )
                        logger.debug(
                            "%s | Expected shutdown time: %s", self.name, shutdown_time
                        )
                        continue

                    logger.debug(
                        "%s | Stop signal received. Scheduling shutdown.", self.name
                    )
                    self.exit_event.set()
                    # Make sure that none of the concurrent workers are stuck or
                    # left behind.
                    self.share_stop_signal(overall=True, input_queue_only=True)

                    continue

                if consumed == "__wait__":
                    self.share_wait_signal(overall=self.spread_wait_signal)

                    logger.debug(
                        "%s | Wait signal received. Spreading the wait signal.",
                        self.name,
                    )

                    continue

                if not self.perform_external_inflight_checks(
                    consumed
                ):  # pragma: no cover
                    logger.debug(
                        "%s | Inflight checks failed. Dropping the following "
                        "message: %r",
                        self.name,
                        consumed,
                    )

                    continue

                try:
                    result = self.target(consumed)
                except (EOFError, KeyboardInterrupt):
                    logger.debug(
                        "%s | EOFError or KeyboardInterrupt while producing. "
                        "Stopping worker.",
                        self.name,
                    )

                    self.global_exit_event.set()
                    continue

                if result is not None:
                    logger.debug(
                        "%s | Produced the following result: %r", self.name, result
                    )

                    self.push_to_output_queues(result)

                if self.delay_shutdown:  # pragma: no cover
                    shutdown_time = datetime.now(timezone.utc) + timedelta(
                        seconds=self.shutdown_delay
                    )
                else:
                    shutdown_time = datetime.now(timezone.utc) + timedelta(days=365)

                if not self.perform_external_postflight_checks(
                    result
                ):  # pragma: no cover
                    logger.debug(
                        "%s | Postflight checks failed. Reiterating the "
                        "ingestion process.",
                        self.name,
                    )
                    continue
        except (ConnectionResetError, BrokenPipeError):  # pragma: no cover
            # This happens when the communication channels are broken or closed.
            # Which is OK.

            logger.debug(
                "%s | ConnectionResetError or BrokenPipeError. Stopping worker.",
                self.name,
            )
        except Exception as exception:  # pylint: disable=broad-exception-caught
            logger.critical(
                "%s | An exception was raised. Stopping worker.",
                self.name,
                exc_info=True,
            )

            trace = traceback.format_exc()
            self._child_connection.send((exception, trace))

            self.exit_event.set()

            if self.raise_exception:  # pragma: no cover
                raise exception

        self.perform_external_poweroff_checks()

        return self

    def terminate(self) -> None:
        """
        Terminates the worker.
        """

        self.exit_event.set()

        try:
            super().terminate()
        except AttributeError:  # pragma: no cover
            pass
