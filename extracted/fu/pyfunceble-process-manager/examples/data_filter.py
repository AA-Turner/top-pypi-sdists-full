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

This is a script that provides an example.

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
import sys
from typing import Any

from PyFunceble.ext.process_manager import ProcessManagerCore, WorkerCore


class DataFilterWorker(WorkerCore):
    def perform_external_poweron_checks(self) -> bool:
        # This can be used to perform checks before starting the worker.
        # If False is returned, the worker will not start.
        return super().perform_external_poweron_checks()

    def perform_external_poweroff_checks(self) -> bool:
        # This can be used to perform checks before stopping the worker.
        return super().perform_external_poweroff_checks()

    def perform_external_preflight_checks(self) -> bool:
        # This can be used to implement your own logic before the worker
        # starts processing the next data.
        return super().perform_external_preflight_checks()

    def perform_external_inflight_checks(self, consumed: Any) -> bool:
        # This can be used to filter out the consumed data by returning False.
        # For example, filter out data that is not a string.

        print("DataFilter consumed:", consumed)

        if not isinstance(consumed, str):

            print("DataFilter filtered out:", consumed)

            return False
        return super().perform_external_inflight_checks(consumed)

    def perform_external_postflight_checks(self, produced: Any) -> bool:
        # This can be used to implement your own logic after the worker
        # has processed the data.

        print("DataFilter produced:", produced)
        return super().perform_external_postflight_checks(produced)

    def target(self, consumed: Any) -> Any:
        # Here we simply convert the string to uppercase as an example of data
        # processing.
        return consumed.upper()


class DataPrinterWorker(WorkerCore):
    def target(self, consumed: Any) -> Any:
        print("DataPrinter consumed:", consumed)
        return consumed


class DataFilterManager(ProcessManagerCore):
    STD_NAME = "data-filter"
    WORKER_CLASS = DataFilterWorker


class DataPrinterManager(ProcessManagerCore):
    STD_NAME = "data-printer"
    WORKER_CLASS = DataPrinterWorker


if __name__ == "__main__":
    dynamic_scaling = len(sys.argv) > 1

    # By default, our interfaces won't log anything. If you need to see or analyze
    # what is going on under the hood, uncomment the following
    # logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger("PyFunceble.ext.process_manager").setLevel(logging.DEBUG)

    data_to_filter = [
        "hello",
        "world",
        123,  # This will be filtered out because it's not a string.
        "PyFunceble",
        None,  # This will be filtered out because it's not a string.
    ]

    if dynamic_scaling:
        # Add more data so that we can see the workers in action.
        data_to_filter += [f"Hello, {i}!" for i in range(1000 + 1)]

    # Configure the manager to generate 2 workers/processes.
    data_filter_manager = DataFilterManager(
        max_workers=10,
        generate_output_queue=True,
        output_queue_count=1,
        dynamic_up_scaling=dynamic_scaling,
        dynamic_down_scaling=dynamic_scaling,
        spread_stop_signal=True,
    )
    # Configure the manager to generate 1 worker/process.
    data_printer_manager = DataPrinterManager(
        max_workers=1,
        input_queue=data_filter_manager.output_queues[0],
        generate_output_queue=False,
    )

    if dynamic_scaling:
        # Build dependencies, so that we can use scaling at it best.
        data_filter_manager.add_dependent_manager(data_printer_manager)

    # Start the manager.
    data_filter_manager.start()
    data_printer_manager.start()

    # Push the data to the input queue for further processing.
    for data in data_to_filter:
        print("Controller pushed:", data)
        data_filter_manager.push_to_input_queue(data)

    # If terminate the manager and all the managed workers after waiting for the
    # workers to finish processing the data.
    #
    # Note: In soft mode, the manager will wait for the workers to finish processing
    # the data before terminating them. In hard mode, the manager will terminate the
    # workers immediately.
    data_filter_manager.terminate(mode="soft")

    print("Data filtered successfully.")
