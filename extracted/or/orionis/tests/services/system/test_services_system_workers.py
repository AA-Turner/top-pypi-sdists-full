from unittest.mock import patch
from orionis.services.system.workers import Workers
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServicesSystemWorkers(AsyncTestCase):

    @patch('multiprocessing.cpu_count', return_value=8)
    @patch('psutil.virtual_memory')
    def testCalculateCpuLimited(self, mockVm, mockCpuCount):
        """
        Tests worker calculation when CPU count is the limiting factor.

        Simulates a system with 8 CPUs and 16 GB RAM, where each worker requires 1 GB of RAM.
        Although the available RAM could support up to 16 workers, the CPU count restricts the number
        of workers to 8.

        Parameters
        ----------
        mockVm : unittest.mock.Mock
            Mock object for `psutil.virtual_memory`.
        mockCpuCount : unittest.mock.Mock
            Mock object for `multiprocessing.cpu_count`.

        Returns
        -------
        None
            Asserts that the calculated number of workers is limited by CPU count.
        """

        # Set the mocked total RAM to 16 GB
        mockVm.return_value.total = 16 * 1024 ** 3

        # Create Workers instance with 1 GB RAM required per worker
        workers = Workers(ram_per_worker=1)

        # Assert that the number of workers is limited to 8 by CPU count
        self.assertEqual(workers.calculate(), 8)

    @patch('multiprocessing.cpu_count', return_value=32)
    @patch('psutil.virtual_memory')
    def testCalculateRamLimited(self, mockVm, mockCpuCount):
        """
        Tests worker calculation when RAM is the limiting factor.

        Simulates a system with 32 CPUs and 4 GB RAM, where each worker requires 1 GB of RAM.
        Although the CPU count could support up to 32 workers, the available RAM restricts the number
        of workers to 4.

        Parameters
        ----------
        mockVm : unittest.mock.Mock
            Mock object for `psutil.virtual_memory`.
        mockCpuCount : unittest.mock.Mock
            Mock object for `multiprocessing.cpu_count`.

        Returns
        -------
        None
            Asserts that the calculated number of workers is limited by available RAM.
        """

        # Set the mocked total RAM to 4 GB
        mockVm.return_value.total = 4 * 1024 ** 3

        # Create Workers instance with 1 GB RAM required per worker
        workers = Workers(ram_per_worker=1)

        # Assert that the number of workers is limited to 4 by available RAM
        self.assertEqual(workers.calculate(), 4)

    @patch('multiprocessing.cpu_count', return_value=4)
    @patch('psutil.virtual_memory')
    def testCalculateExactFit(self, mockVm, mockCpuCount):
        """
        Tests worker calculation when both CPU count and available RAM allow for the same number of workers.

        Simulates a system with 4 CPUs and 2 GB RAM, where each worker requires 0.5 GB of RAM.
        Both CPU and RAM resources permit exactly 4 workers, so the calculation should return 4.

        Parameters
        ----------
        mockVm : unittest.mock.Mock
            Mock object for `psutil.virtual_memory`.
        mockCpuCount : unittest.mock.Mock
            Mock object for `multiprocessing.cpu_count`.

        Returns
        -------
        None
            Asserts that the calculated number of workers is 4, matching both CPU and RAM constraints.
        """
        # Set the mocked total RAM to 2 GB
        mockVm.return_value.total = 2 * 1024 ** 3

        # Create Workers instance with 0.5 GB RAM required per worker
        workers = Workers(ram_per_worker=0.5)

        # Assert that the number of workers is limited to 4 by both CPU and RAM
        self.assertEqual(workers.calculate(), 4)

    @patch('multiprocessing.cpu_count', return_value=2)
    @patch('psutil.virtual_memory')
    def testCalculateLowRam(self, mockVm, mockCpuCount):
        """
        Tests worker calculation when available RAM is lower than CPU count, restricting the number of workers.

        Simulates a system with 2 CPUs and 0.7 GB RAM, where each worker requires 0.5 GB of RAM.
        Although the CPU count could support up to 2 workers, the available RAM restricts the number
        of workers to 1.

        Parameters
        ----------
        mockVm : unittest.mock.Mock
            Mock object for `psutil.virtual_memory`.
        mockCpuCount : unittest.mock.Mock
            Mock object for `multiprocessing.cpu_count`.

        Returns
        -------
        None
            Asserts that the calculated number of workers is limited to 1 by available RAM.
        """

        # Set the mocked total RAM to 0.7 GB
        mockVm.return_value.total = 0.7 * 1024 ** 3

        # Create Workers instance with 0.5 GB RAM required per worker
        workers = Workers(ram_per_worker=0.5)

        # Assert that the number of workers is limited to 1 by available RAM
        self.assertEqual(workers.calculate(), 1)