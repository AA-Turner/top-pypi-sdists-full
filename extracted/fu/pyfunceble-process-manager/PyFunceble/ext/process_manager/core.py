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

This is the module that provides the core components of our process manager.

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

import functools
import logging
import multiprocessing
import multiprocessing.context
import multiprocessing.managers
import multiprocessing.queues
import multiprocessing.synchronize
import os
import queue
import random
from typing import Any, Callable, List, Optional

from PyFunceble.ext.process_manager.worker.core import WorkerCore

logger = logging.getLogger("PyFunceble.ext.process_manager")


class ProcessManagerCore:
    """
    This is the core of the process manager. It provides the basic methods
    to work with.

    It has been designed to be used as a parent class.
    """

    STD_NAME: str = "pyfunceble-process-manager"
    """
    The standard name of the process manager.

    .. note::
        The name of the worker will be in the format:

        ppm-{STD_NAME}-{worker_number}

    """

    WORKER_CLASS: WorkerCore
    """
    The class which is going to be used as worker. This is a mandatory attribute
    and its value should be a class that inherits from our :code:`WorkerCore`.

    .. note::

        This is a mandatory attribute and its value should be a class that
        inherits from :code:`multiprocessing.Process`. It is although recommended
        to inherit from :code:`PyFunceble.ext.process_manager.worker.WorkerCore`.
    """

    AVAILABLE_CPU_COUNT = os.cpu_count()
    """
    Represents the number of CPU available on the current machine.
    """

    input_datasets: Optional[List] = []
    """
    Stores and exposes the input datasets. This is a list of data that we
    have to send to the input queue of the worker(s) before we start them.

    It should be a list of data. The data is up to you, but it must be a list.
    """

    output_datasets: Optional[List] = []
    """
    Stores and exposes the output datasets. This is a list of data that we
    have to send to the output queue(s) of the worker(s) before we start them.

    It should be a list of data. The data is up to you, but it must be a list.
    """

    configuration_datasets: Optional[List] = []
    """
    Stores and exposes the configuration datasets. This is a list of data that we
    have to send to the configuration queue of the worker(s) before we start them.

    It should be a list of data. The data is up to you, but it must be a list.
    """

    manager: Optional[multiprocessing.managers.SyncManager] = None
    """
    Stores and exposes the manager of the worker.

    The manager is used to initialize the worker's queue(s) - when not explicitly
    provided by the end-user.

    When initialized, it will be a :code:`multiprocessing.Manager()` object.
    """

    global_exit_event: Optional[multiprocessing.synchronize.Event] = None
    """
    Stores and exposes the global exit event of the worker.

    The global exit event is used to tell the worker to stop its work.

    When initialized, it will be a :code:`multiprocessing.Event()` object.
    """

    terminating_event: Optional[multiprocessing.synchronize.Event] = None
    """
    Stores and exposes the terminating event of the process manager - itself.

    The terminating event is used to keep track of the termination status of the
    process manager.

    When initialized, it will be a :code:`multiprocessing.Event()` object.
    """

    configuration_queue: Optional[multiprocessing.queues.Queue] = None
    """
    Stores and exposes the configuration queue of the worker.

    The configuration queue is used to send or share configuration data between
    the process manager and the managed worker.
    """

    input_queue: Optional[multiprocessing.queues.Queue] = None
    """
    Stores and exposes the input queue of the worker.
    """

    output_queues: Optional[List[multiprocessing.queues.Queue]] = None
    """
    Store and expose the output queue(s) of the worker.
    """

    daemon: Optional[bool] = None
    """
    Store and expose the daemon status of the worker.

    When set to :code:`True`, the worker will be a daemon.
    """

    spread_stop_signal: bool = False
    """
    Whether we have to spread the stop signal to the output queue(s) of the
    worker(s).
    """

    spread_wait_signal: bool = False
    """
    Whether we have to spread the wait signal to the output queue(s) of the
    worker(s).
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

    shutdown_on_exception: Optional[bool] = None
    """
    Whether we have to shutdown every worker as soon as one of the workers
    raised an exception.
    """

    dynamic_up_scaling: Optional[bool] = None
    """
    Whether we have to dynamically scale-up the number of workers based on the
    number of data in the input queue.

    When set to :code:`True`, the system will try to scale the number of workers
    up based on the number of data in the input queue. This won't however
    scale down the number of workers once the maximum number of workers is reached
    because scaling down can be expensive.

    .. warning::
        This is experimental and should be used with caution.
    """

    dynamic_down_scaling: Optional[bool] = None
    """
    Whether we have to dynamically scale-down the number of workers based on the
    number of data in the input queue.

    When set to :code:`True`, the system will try to scale the number of workers
    down based on the number of data in the input queue.

    Please note that scaling down can be expensive and that's why we don't
    recommend using this feature.

    .. warning::
        This is experimental and should be used with caution.
    """

    sharing_delay: Optional[float] = None
    """
    The number of seconds to wait before sharing the message.
    """

    shutdown_delay: Optional[float] = None
    """
    The number of seconds to wait before shutting down the worker.
    """

    fetch_delay: Optional[float] = None
    """
    The number of seconds to wait before fetching the next dataset.
    """

    dependent_managers: Optional[List["ProcessManagerCore"]] = None
    """
    The process manager that depends on the currently managed process manager.

    When given, the system will interact with the dependent process manager
    instead of directly interacting with the queue(s).

    .. note::
        This is optional but when used, it allow us to not only scale the very
        first process manager but also the dependent ones.

        If you are playing with :ivar:`dynamic_up_scaling` and
        :ivar:`dynamic_down_scaling`, this is a must to have.
    """

    controlling_manager: Optional["ProcessManagerCore"] = None
    """
    The process manager that controls the currently managed process manager.

    When given, the system will interact with the controlling process manager
    instead of directly interacting with the queue(s).

    .. note::
        This is optional but when used, it allow us to not only scale the very
        first process manager but also the controlled ones.

        If you are playing with :ivar:`dynamic_up_scaling` and
        :ivar:`dynamic_down_scaling`, this is a must to have.

    .. warning::
        You are not expected to set this manually. This is set automatically
        when you use the :meth:`add_dependent_manager` method.
    """

    _extra_args: Optional[dict] = None
    """
    The extra arguments that were passed to the worker through the
    :code:`kwargs` parameter.
    """

    created_workers: Optional[List[WorkerCore]] = None
    running_workers: Optional[List[WorkerCore]] = None

    _max_workers: Optional[int] = 1

    def __init__(
        self,
        max_workers: Optional[int] = None,
        *,
        manager: Optional[multiprocessing.managers.SyncManager] = None,
        input_queue: Optional[queue.Queue] = None,
        generate_input_queue: bool = True,
        output_queue: Optional[queue.Queue] = None,
        output_queue_count: int = 1,
        generate_output_queue: bool = True,
        configuration_queue: Optional[queue.Queue] = None,
        generate_configuration_queue: bool = True,
        daemon: Optional[bool] = None,
        spread_stop_signal: bool = None,
        spread_wait_signal: bool = None,
        delay_message_sharing: bool = None,
        delay_shutdown: bool = None,
        raise_exception: bool = None,
        shutdown_on_exception: bool = None,
        targeted_processing: bool = None,
        sharing_delay: Optional[float] = None,
        shutdown_delay: Optional[float] = None,
        fetch_delay: Optional[float] = None,
        dynamic_up_scaling: Optional[bool] = None,
        dynamic_down_scaling: Optional[bool] = None,
        dependent_managers: Optional[List["ProcessManagerCore"]] = None,
        **kwargs,
    ):
        self.created_workers = []
        self.running_workers = []

        self._max_workers = max_workers or self.cpu_count

        self.daemon = daemon or False
        self.targeted_processing = targeted_processing or True
        self.delay_message_sharing = delay_message_sharing or False
        self.delay_shutdown = delay_shutdown or False
        self.raise_exception = raise_exception or False
        self.shutdown_on_exception = shutdown_on_exception or False
        self.dynamic_up_scaling = dynamic_up_scaling or False
        self.dynamic_down_scaling = dynamic_down_scaling or False

        if manager is None:
            self.manager = multiprocessing.Manager()
        else:
            self.manager = manager

        self.global_exit_event = self.manager.Event()
        self.terminating_event = self.manager.Event()

        if dependent_managers is None:
            self.dependent_managers = []
        else:
            self.dependent_managers = dependent_managers

        if spread_stop_signal is not None:
            self.spread_stop_signal = spread_stop_signal

        if spread_wait_signal is not None:
            self.spread_wait_signal = spread_wait_signal

        if sharing_delay is not None:
            self.sharing_delay = sharing_delay

        if shutdown_delay is not None:
            self.shutdown_delay = shutdown_delay

        if fetch_delay is not None:
            self.fetch_delay = fetch_delay

        if not input_queue and generate_input_queue:
            self.input_queue = self.manager.Queue()
        else:
            self.input_queue = input_queue

        if not output_queue and generate_output_queue:
            self.output_queues = [
                self.manager.Queue() for _ in range(max(1, output_queue_count))
            ]
        elif output_queue:
            self.output_queues = (
                [output_queue] if not isinstance(output_queue, list) else output_queue
            )

        if not configuration_queue and generate_configuration_queue:
            self.configuration_queue = self.manager.Queue()

        self._extra_args = kwargs

        self.__post_init__()

    def __post_init__(self) -> None:
        """
        Called after the initialization of the worker, this method can be used
        by the child class to initialize their own workflows.
        """

    def __getattr__(self, attribute: str) -> Any:
        """
        Provides the value of the given attribute.

        :param str attribute:
            The attribute to get the value of.
        """

        if self._extra_args and attribute in self._extra_args:
            return self._extra_args[attribute]

        raise AttributeError(f"{self.__class__.__name__} has no attribute {attribute}")

    def ensure_worker_class_is_set(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator which ensures that the worker class is set before launching
        the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.WORKER_CLASS:
                raise TypeError(f"<{self.__class__.__name__}.WORKER_CLASS> is not set.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ensure_worker_spawned(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator which ensures that at least one has been spawned before
        launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # We will skip the spawning of the worker if the first argument
            # is in the list of reserved messages.
            skip_spawn_based_on_arg = (
                False if not args else args[0] in WorkerCore.RESERVED_MESSAGES
            )

            if (
                not skip_spawn_based_on_arg
                and not self.is_terminating()
                and (
                    not self.created_workers
                    or self.dynamic_up_scaling
                    or self.dynamic_down_scaling
                )
            ):
                self.spawn_workers(start=False)

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ignore_if_running(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator which ensures that the decorated method is ignored if at least
        one worker is running.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.is_running():
                return self

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ignore_if_terminating(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator which ensures that the decorated method is ignored if we are
        exiting/terminating. (cf: self.global_exit_event is set)
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.is_terminating():  # pragma: no cover # impossible to test - yet.
                return self

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def relink_queues_after(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator which ensures that the input queue of the dependent manager is
        the output queue of the current manager.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if self.output_queues and self.dependent_managers:
                for index, manager in enumerate(self.dependent_managers):
                    try:
                        manager.input_queue = self.output_queues[index]
                    except IndexError:
                        manager.input_queue = self.output_queues[-1]

            return result

        return wrapper

    @property
    def name(self) -> str:
        """
        Provides the sanitized name of the process manager.
        """

        return f"ppm-{self.STD_NAME}"

    @property
    def cpu_count(self) -> int:
        """
        Provides the number of CPU that the process has to use.

        This method assumes that we we should always leave 2 CPUs available.
        Meaning that if you have more than 2 CPUs, we will return the number
        of CPUs minus 2. Otherwise, we return the number of CPUs.
        """

        if self.AVAILABLE_CPU_COUNT > 2:
            return self.AVAILABLE_CPU_COUNT - 2

        return self.AVAILABLE_CPU_COUNT

    @property
    def queue_size(self) -> int:
        """
        Provides the size of the queue to use.
        """

        if not self.input_queue:
            return 0
        return self.input_queue.qsize()

    @property
    def queue_full(self) -> bool:
        """
        Provides the status of the queue.
        """

        return self.queue_size >= self.max_workers

    @property
    def running(self) -> bool:
        """
        Provides the status of the worker(s).
        """

        if not self.running_workers:
            return False

        return any(x.is_alive() for x in self.running_workers)

    @property
    def terminating(self) -> bool:
        """
        Provides the termination status of the worker(s).
        """

        return self.terminating_event.is_set()

    @property
    def max_workers(self) -> int:
        """
        Provides the maximum number of workers that we are allowed to create.
        """

        return self._max_workers

    @max_workers.setter
    def max_workers(self, value: int) -> None:
        """
        Sets the maximum number of workers that we are allowed to create.

        :param int value:
            The value to set.

        :raise TypeError:
            When the given value is not an integer.
        """

        if not isinstance(value, int):
            raise TypeError(f"<value> should be {int}, {type(value)} given.")

        self._max_workers = max(1, value)

    @property
    def running_workers_full(self) -> bool:
        """
        Provides the status of the workers.
        """

        return len(self.running_workers) >= self.max_workers

    @property
    def created_workers_full(self) -> bool:
        """
        Provides the status of the workers.
        """

        return len(self.created_workers) >= self.max_workers

    def adjust_workers_to_reality(self) -> "ProcessManagerCore":
        """
        Adjust the number of running workers to the reality of the situation.
        """

        # Adjust to make sure to remove the workers that are not running anymore.
        self.running_workers = [x for x in self.running_workers if x.exitcode is None]
        self.created_workers = [x for x in self.created_workers if x.exitcode is None]

        return self

    def is_running(self) -> bool:
        """
        Checks if at least one worker is running.
        """

        return self.running

    def is_terminating(self) -> bool:
        """
        Checks if the worker is terminating.
        """

        return self.terminating

    def is_queue_full(self) -> bool:
        """
        Checks if the queue is full.
        """

        return self.queue_full

    @relink_queues_after
    def add_dependent_manager(
        self, manager: "ProcessManagerCore"
    ) -> "ProcessManagerCore":
        """
        Adds a dependent manager to the currently managed process manager.

        :param ProcessManagerCore manager:
            The dependent manager to add.
        """

        manager.controlling_manager = self
        self.dependent_managers.append(manager)

        return self

    @relink_queues_after
    def remove_dependent_manager(
        self, manager: "ProcessManagerCore"
    ) -> "ProcessManagerCore":
        """
        Removes a dependent manager from the currently managed process manager.

        :param ProcessManagerCore manager:
            The dependent manager to remove.
        """

        if manager in self.dependent_managers:
            self.dependent_managers.remove(manager)

        return self

    @ensure_worker_spawned
    def push_to_input_queue(
        self,
        data: Any,
        *,
        source_worker: Optional[str] = None,
        all_queues: bool = False,
    ) -> "ProcessManagerCore":
        """
        Pushes the given data to the currently managed input queue.

        :param any data:
            The data to spread.
        :param str source_worker:
            The name to use to identify the worker or process that is sending
            the data.

            If this is not set, we will use the name of the process manager.
        :param bool all_queues:
            Whether we have to spread the data to the queues of all workers instead
            of just the first one reached.

            .. warning::

                When this is set to :code:`True`, the system will spread the data
                to all workers. This means that it might be possible that the data
                is sent to the same worker multiple times.
        """

        if self.is_running():
            workers = self.running_workers
        else:
            workers = self.created_workers

        source_worker = source_worker or self.name

        if all_queues:
            for worker in workers:
                worker.push_to_input_queue(
                    data, source_worker=source_worker, destination_worker=worker.name
                )
        elif workers:
            random.choice(  # nosec: B311 # We aren't doing encryption here.
                workers
            ).push_to_input_queue(data, source_worker=source_worker)

        logger.debug("%s-manager | Pushed to input queue: %r", self.STD_NAME, data)

        return self

    @ensure_worker_spawned
    def push_to_output_queues(
        self,
        data: Any,
        *,
        source_worker: Optional[str] = None,
        all_queues: bool = False,
    ) -> "ProcessManagerCore":
        """
        Pushes the given data to the currently managed output queue.

        :param any data:
            The data to spread.
        :param str source_worker:
            The name to use to identify the worker or process that is sending
            the data.

            If this is not set, we will use the name of the process manager.
        :param bool all_queues:
            Whether we have to spread the data to the queues of all workers instead
            of just the first one reached.

            .. warning::

                When this is set to :code:`True`, the system will spread the data
                to all workers. This means that it might be possible that the data
                is sent to the same worker multiple times.
        """

        source_worker = source_worker or f"ppm-{self.STD_NAME}-manager"

        if not self.dependent_managers:
            if self.is_running():
                workers = self.running_workers
            else:
                workers = self.created_workers

            if all_queues:
                for worker in workers:
                    worker.push_to_output_queues(
                        data,
                        source_worker=source_worker,
                        destination_worker=worker.name,
                    )
            elif workers:
                random.choice(  # nosec: B311 # We aren't doing encryption here.
                    workers
                ).push_to_output_queues(data, source_worker=source_worker)
        else:
            for manager in self.dependent_managers:
                # Their input queue is our output queue.
                manager.push_to_input_queue(data, source_worker=source_worker)

        logger.debug("%s-manager | Pushed to output queues: %r", self.STD_NAME, data)

        return self

    @ensure_worker_spawned
    def push_to_configuration_queue(
        self, data: Any, *, source_worker: Optional[str] = None, all_queues: bool = True
    ) -> "ProcessManagerCore":
        """
        Pushes the given data to the currently managed configuration queue.

        :param any data:
            The data to spread.

        :param str source_worker:
            The name to use to identify the worker or process that is sending
            the data.
        :param bool all_queues:
            Whether we have to spread the data to the queues of all workers instead
            of just the first one reached.

            .. warning::

                When this is set to :code:`True`, the system will spread the data
                to all workers. This means that it might be possible that the data
                is sent to the same worker multiple times.
        """

        if self.is_running():
            workers = self.running_workers
        else:
            workers = self.created_workers

        source_worker = source_worker or f"ppm-{self.STD_NAME}-manager"

        if all_queues:
            for worker in workers:
                worker.push_to_configuration_queue(
                    data, source_worker=source_worker, destination_worker=worker.name
                )
        elif workers:
            random.choice(  # nosec: B311 # We aren't doing encryption here.
                workers
            ).push_to_configuration_queue(data, source_worker=source_worker)

        logger.debug(
            "%s-manager | Pushed to configuration queue: %r", self.STD_NAME, data
        )

        return self

    def spawn_worker(
        self, *, start: bool = False, daemon: bool = None, force: bool = False
    ) -> Optional[WorkerCore]:
        """
        Spawns and configures a (single) new worker.

        :param bool start:
            Tell us if we have to start the worker after its creation.
        :param bool daemon:
            Tell us if the worker should be a daemon.

            .. note::
                If this is not set, we will use the value of the
                :code:`daemon` attribute.
        :param bool force:
            Tell us if we have to force the spawning of the worker.

            .. note::
                This is useful when we want to spawn a worker even if the
                maximum number of workers is reached.
        """

        if start and self.running_workers_full and not force:
            return None

        if not start and self.created_workers_full and not force:
            return None

        worker = self.WORKER_CLASS(
            name=f"ppm-{self.STD_NAME}-{len(self.created_workers) + 1}",
            input_queue=self.input_queue,
            output_queues=self.output_queues,
            global_exit_event=self.global_exit_event,
            configuration_queue=self.configuration_queue,
            daemon=daemon or self.daemon,
            spread_stop_signal=self.spread_stop_signal,
            spread_wait_signal=self.spread_wait_signal,
            targeted_processing=self.targeted_processing,
            delay_message_sharing=self.delay_message_sharing,
            delay_shutdown=self.delay_shutdown,
            raise_exception=self.raise_exception,
            sharing_delay=self.sharing_delay,
            shutdown_delay=self.shutdown_delay,
            fetch_delay=self.fetch_delay,
            dependent_workers_names=[x.name for x in self.dependent_managers],
            controlling_workers_name=(
                self.controlling_manager.name if self.controlling_manager else None
            ),
            **self._extra_args,
        )

        if not self.is_running():
            # Just to make sure that the worker is aware that it might not not alone.
            worker.concurrent_workers_names = [x.name for x in self.created_workers]
        else:
            worker.concurrent_workers_names = [x.name for x in self.running_workers]

        self.created_workers.append(worker)

        if start:
            worker.start()
            self.running_workers.append(worker)

        logger.debug("%s-manager | Worker spawned: %r", self.STD_NAME, worker.name)

        return worker

    def spawn_workers(
        self, *, start: bool = False
    ) -> (
        "ProcessManagerCore"
    ):  # pragma: no cover # Scaling tested through human analysis.
        """
        Spawns and scales the number of workers.

        :param bool start:
            Tell us if we have to start the worker after its creation.
        :param any last_message:
            The last message that was pushed to the input queue.
        """

        self.adjust_workers_to_reality()

        if not self.dynamic_up_scaling:
            while not self.running_workers_full and not self.created_workers_full:
                self.spawn_worker(start=start)
            return self

        logger.debug("%s-manager | SCALING | Entering dynamic scaling.", self.STD_NAME)

        logger.debug(
            "%s-manager | SCALING | Queue size: %r, Running workers: %r, "
            "Created workers: %r",
            self.STD_NAME,
            self.queue_size,
            len(self.running_workers),
            len(self.created_workers),
        )

        if self.is_running():
            logger.debug(
                "%s-manager | SCALING | Entering dynamic scaling for running workers.",
                self.STD_NAME,
            )

            logger.debug(
                "%s-manager | SCALING | (NEW) Running workers: %r",
                self.STD_NAME,
                len(self.running_workers),
            )

            if self.queue_size > len(self.running_workers):
                if not self.running_workers_full:
                    # This will be the maximum number of workers that we can create.
                    available_workers_to_create = self.max_workers - len(
                        self.running_workers
                    )

                    # This will be the number of workers that we can create based
                    # on the number of data in the queue. We try to never exceed
                    # the maximum number of workers we are allowed to create.
                    to_create = min(
                        available_workers_to_create,
                        self.queue_size - len(self.running_workers) or 1,
                    )

                    logger.debug(
                        "%s-manager | SCALING | Spawning %r new workers.",
                        self.STD_NAME,
                        to_create,
                    )

                    while not self.running_workers_full and to_create > 0:
                        # Note: we start immediately because we are scaling up.
                        self.spawn_worker(start=True)
                        to_create -= 1

                return self

            if self.dynamic_down_scaling and len(self.running_workers) > 1:
                logger.debug(
                    "%s-manager | SCALING | Scaling down the number of workers by 1.",
                    self.STD_NAME,
                )

                worker_to_kill = self.running_workers[0]

                # We shutdown the first worker that we can find.
                worker_to_kill.push_to_input_queue(
                    "__immediate_shutdown__", destination_worker=worker_to_kill.name
                )

                if worker_to_kill in self.running_workers:
                    self.running_workers.remove(worker_to_kill)

                if worker_to_kill in self.created_workers:
                    self.created_workers.remove(worker_to_kill)

                return self
            return self

        logger.debug(
            "%s-manager | SCALING | Entering dynamic scaling for created workers.",
            self.STD_NAME,
        )

        if not self.created_workers or (
            not self.created_workers_full
            and self.queue_size > len(self.created_workers)
        ):
            # This will be the maximum number of workers that we can create.
            available_workers_to_create = self.max_workers - len(self.created_workers)

            # This will be the number of workers that we can create based
            # on the number of data in the queue. We try to never exceed
            # the maximum number of workers we are allowed to create.
            to_create = min(
                available_workers_to_create,
                self.queue_size - len(self.created_workers) or 1,
            )

            logger.debug(
                "%s-manager | SCALING | Spawning %r new workers.",
                self.STD_NAME,
                to_create,
            )

            while (
                not self.created_workers or not self.created_workers_full
            ) and to_create > 0:
                self.spawn_worker(start=start)
                to_create -= 1

        return self

    def push_stop_signal(
        self, *, source_worker: Optional[str] = None, all_workers: bool = True
    ) -> "ProcessManagerCore":
        """
        Sends the stop signal to the worker(s).

        :param str source_worker:
            The name to use to identify the worker or process that is sending
            the data.
        :param bool all_workers:
            Whether we have to spread the stop signal to all workers.
        """

        self.push_to_input_queue(
            "__stop__", source_worker=source_worker, all_queues=all_workers
        )

        return self

    def share_stop_signal(
        self, *, source_worker: Optional[str] = None, all_workers: bool = False
    ) -> "ProcessManagerCore":
        """
        Shares the stop signal to the worker(s).

        :param str source_worker:
            The name to use to identify the worker or process that is sending
            the data.
        :param bool all_workers:
            Whether we have to spread the stop signal to all workers.
        """

        self.push_to_output_queues(
            "__stop__", source_worker=source_worker, all_queues=all_workers
        )

        return self

    def push_wait_signal(
        self, *, source_worker: Optional[str] = None
    ) -> "ProcessManagerCore":
        """
        Sends the wait signal to the worker(s).

        :param str source_worker:
            The name to use to identify the worker or process that is sending
            the data.
        """

        self.push_to_input_queue(
            "__wait__", source_worker=source_worker, all_queues=True
        )

        return self

    def terminate_worker(self, worker: WorkerCore) -> "ProcessManagerCore":
        """
        Terminates the given worker.

        :param WorkerCore worker:
            The worker to terminate.
        """

        logger.debug("%s-manager | Terminating worker: %r", self.STD_NAME, worker.name)

        worker.terminate()
        worker.join()

        if worker in self.running_workers:
            self.running_workers.remove(worker)

        if worker in self.created_workers:
            self.created_workers.remove(worker)

        del worker

        logger.debug("%s-manager | Worker terminated.", self.STD_NAME)

        return self

    @ignore_if_terminating
    def terminate(self, *, mode: str = "soft") -> "ProcessManagerCore":
        """
        Terminates the worker(s).

        :param str mode:
            The mode to use to terminate the worker(s).

            .. note::
                - If set to :code:`soft`, we will send a stop signal to
                  the worker(s) and wait for them to terminate.

                - If set to :code:`hard`, we will terminate the worker(s)
                  directly without waiting for them to terminate.
        """

        logger.debug("%s-manager | Terminating all workers.", self.STD_NAME)

        if mode not in ("soft", "hard"):
            raise ValueError(f"<mode> should be 'soft' or 'hard', {mode} given.")

        if not self.is_terminating():
            # Set the terminating event to tell the controller that we are
            # terminating.
            self.terminating_event.set()

        if mode == "hard":
            logging.debug(
                "%s-manager | Forcefully terminating all workers.", self.STD_NAME
            )

            # Instruct the workers to terminate themselves.
            self.global_exit_event.set()

            for worker in set(self.running_workers + self.created_workers):
                self.terminate_worker(worker)

            return self

        if len(set(self.running_workers + self.created_workers)) != 0:
            self.push_stop_signal(all_workers=True)
            # We now wait for the workers to terminate by themselves.
            self.wait()

        if self.spread_stop_signal:
            # When all workers are terminated, we send a stop message to the workers
            # that depends on the currently managed workers.
            self.share_stop_signal(all_workers=self.spread_stop_signal)

        logger.debug("%s-manager | All workers terminated.", self.STD_NAME)

        return self

    def wait(self) -> "ProcessManagerCore":
        """
        Waits for all workers to finish their work.
        """

        for worker in set(self.running_workers + self.created_workers):
            logger.debug(
                "%s-manager | Waiting for worker: %r", self.STD_NAME, worker.name
            )

            if worker.is_alive():
                worker.join()

            if worker in self.running_workers:
                self.running_workers.remove(worker)

            if worker in self.created_workers:
                self.created_workers.remove(worker)

            if worker.exception:
                try:
                    worker_error, trace = worker.exception
                except ValueError:  # pragma: no cover  # safety
                    # No exception - actually
                    continue

                if self.shutdown_on_exception:
                    # We terminate everything that we are controlling as soon as
                    # possible.
                    self.terminate()

                logger.critical(
                    "%s-manager | Worker %r raised an exception:\n%s",
                    self.STD_NAME,
                    worker.name,
                    trace,
                )

                raise worker_error

            logger.debug(
                "%s-manager | Still running workers: %r",
                self.STD_NAME,
                self.running_workers,
            )

            logger.debug(
                "%s-manager | Still running workers: %r",
                self.STD_NAME,
                self.running_workers,
            )

        return self

    @ensure_worker_class_is_set
    @ignore_if_running
    @ensure_worker_spawned
    def start(self) -> "ProcessManagerCore":
        """
        Starts the worker(s).
        """

        for worker in self.created_workers:
            worker.start()
            self.running_workers.append(worker)

        for data in self.input_datasets:
            self.push_to_input_queue(data, source_worker="ppm")

        for data in self.output_datasets:
            self.push_to_output_queues(data, source_worker="ppm")

        for data in self.configuration_datasets:
            self.push_to_configuration_queue(data, source_worker="ppm")

        return self
