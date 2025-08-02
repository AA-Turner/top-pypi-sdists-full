from abc import ABC, abstractmethod

class IWorkers(ABC):

    @abstractmethod
    def setRamPerWorker(self, ram_per_worker: float) -> None:
        """
        Set the amount of RAM to allocate for each worker process.

        Parameters
        ----------
        ram_per_worker : float
            The amount of RAM, in gigabytes (GB), to allocate for each worker process.

        Returns
        -------
        None
            This method does not return any value.

        Notes
        -----
        This method should be implemented by subclasses to configure the memory usage
        per worker, which may affect the total number of workers that can be spawned
        based on system resources.
        """

        # Implementation should assign the specified RAM per worker.
        pass

    @abstractmethod
    def calculate(self) -> int:
        """
        Compute the recommended maximum number of worker processes for the current machine.

        This method should consider both CPU and memory constraints to determine the optimal
        number of worker processes that can be safely spawned without overloading system resources.

        Returns
        -------
        int
            The maximum number of worker processes that can be supported by the current machine,
            based on available CPU cores and memory limits.

        Notes
        -----
        Subclasses should implement this method to analyze system resources and return an integer
        representing the recommended number of workers. The calculation should ensure that each
        worker receives sufficient resources as configured (e.g., RAM per worker).
        """

        # Implementation should analyze system resources and return the recommended worker count.
        pass