import multiprocessing
import math
import psutil
from orionis.services.system.contracts.workers import IWorkers

class Workers(IWorkers):

    def __init__(self, ram_per_worker: float = 0.5):
        """
        Initialize the Workers system with resource constraints.

        Parameters
        ----------
        ram_per_worker : float, optional
            Amount of RAM (in GB) allocated per worker. Default is 0.5.

        Attributes
        ----------
        _cpu_count : int
            Number of CPU cores available on the system.
        _ram_total_gb : float
            Total system RAM in gigabytes.
        _ram_per_worker : float
            RAM allocated per worker in gigabytes.

        Returns
        -------
        None
            This constructor does not return a value.
        """

        # Get the number of CPU cores available
        self._cpu_count = multiprocessing.cpu_count()

        # Get the total system RAM in gigabytes
        self._ram_total_gb = psutil.virtual_memory().total / (1024 ** 3)

        # Set the RAM allocated per worker
        self._ram_per_worker = ram_per_worker

    def setRamPerWorker(self, ram_per_worker: float) -> None:
        """
        Update the RAM allocation per worker.

        Parameters
        ----------
        ram_per_worker : float
            The new amount of RAM (in GB) to allocate for each worker.

        Returns
        -------
        None
            This method does not return a value. It updates the internal RAM allocation setting.

        Notes
        -----
        Changing the RAM allocation per worker may affect the recommended number of workers
        calculated by the system. This method only updates the internal configuration and does
        not trigger any recalculation automatically.
        """

        # Update the RAM allocated per worker
        self._ram_per_worker = ram_per_worker

    def calculate(self) -> int:
        """
        Compute the recommended maximum number of worker processes for the current machine,
        considering both CPU and memory constraints.

        Parameters
        ----------
        None

        Returns
        -------
        int
            The maximum number of worker processes that can be safely run in parallel,
            determined by the lesser of available CPU cores and memory capacity.

        Notes
        -----
        The calculation is based on:
            - The total number of CPU cores available.
            - The total system RAM divided by the RAM allocated per worker.
        The method ensures that neither CPU nor memory resources are overcommitted.

        """

        # Calculate the maximum workers allowed by CPU core count
        max_workers_by_cpu = self._cpu_count

        # Calculate the maximum workers allowed by available RAM
        max_workers_by_ram = math.floor(self._ram_total_gb / self._ram_per_worker)

        # Return the minimum of the two to avoid overcommitting resources
        return min(max_workers_by_cpu, max_workers_by_ram)
