import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from orionis.foundation.application import Application as Orionis
from orionis.container.container import Container
from orionis.test.cases.asynchronous import AsyncTestCase

class TestThreadSafety(AsyncTestCase):

    async def testStressSingleton(self) -> None:
        """
        Stress test singleton behavior under extreme concurrent conditions.

        This method creates a large number of threads that simultaneously attempt to
        instantiate singleton objects (`Container` and `Orionis`). It verifies that
        only one unique instance of each singleton exists, regardless of concurrent
        access, and that the singleton instances are distinct from each other.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate
            singleton behavior under stress.

        Notes
        -----
        - Random delays are introduced to increase the likelihood of race conditions.
        - ThreadPoolExecutor is used to simulate high concurrency.
        - The test ensures that singleton integrity is maintained even under heavy load.
        """
        container_instances = []
        orionis_instances = []

        def create_container_with_delay():
            """Create a Container instance after a random delay to simulate real-world concurrency."""
            # Random delay to increase chance of race conditions
            time.sleep(random.uniform(0.001, 0.01))
            container = Container()
            container_instances.append(container)
            return id(container)

        def create_orionis_with_delay():
            """Create an Orionis instance after a random delay to simulate real-world concurrency."""
            # Random delay to increase chance of race conditions
            time.sleep(random.uniform(0.001, 0.01))
            orionis = Orionis()
            orionis_instances.append(orionis)
            return id(orionis)

        # Number of concurrent threads to simulate
        num_threads = 100

        # Use ThreadPoolExecutor to run tasks concurrently
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Submit container creation tasks
            container_futures = [
                executor.submit(create_container_with_delay)
                for _ in range(num_threads)
            ]

            # Submit orionis creation tasks
            orionis_futures = [
                executor.submit(create_orionis_with_delay)
                for _ in range(num_threads)
            ]

            # Wait for all tasks to complete and collect instance IDs
            container_ids = [future.result() for future in as_completed(container_futures)]
            orionis_ids = [future.result() for future in as_completed(orionis_futures)]

        # Verify all instances are the same (singleton property)
        unique_container_ids = set(container_ids)
        unique_orionis_ids = set(orionis_ids)

        self.assertEqual(len(container_instances), num_threads)
        self.assertEqual(len(unique_container_ids), 1)
        self.assertEqual(len(orionis_instances), num_threads)
        self.assertEqual(len(unique_orionis_ids), 1)

        # Verify that Container and Orionis are different singletons
        container_id = list(unique_container_ids)[0] if unique_container_ids else None
        orionis_id = list(unique_orionis_ids)[0] if unique_orionis_ids else None

        self.assertNotEqual(container_id, orionis_id)
