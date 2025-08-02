import threading
import time
from orionis.foundation.application import Application as Orionis
from orionis.container.container import Container
from orionis.test.cases.asynchronous import AsyncTestCase

class TestSingleton(AsyncTestCase):

    async def testSingletonBasicFunctionality(self) -> None:
        """
        Tests the fundamental behavior of the singleton pattern for `Container` and `Orionis` classes.

        This method verifies the following:
        - Multiple instances of `Container` refer to the same object.
        - Multiple instances of `Orionis` refer to the same object.
        - The singleton instances of `Container` and `Orionis` are distinct from each other.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate singleton behavior.
        """
        # Create multiple instances of Container and Orionis
        container1 = Container()
        container2 = Container()
        orionis1 = Orionis()
        orionis2 = Orionis()

        # Assert that all Container instances are the same object
        self.assertIs(container1, container2)
        self.assertEqual(id(container1), id(container2))

        # Assert that all Orionis instances are the same object
        self.assertIs(orionis1, orionis2)
        self.assertEqual(id(orionis1), id(orionis2))

        # Assert that Container and Orionis are different singleton instances
        self.assertIsNot(container1, orionis1)

    async def testSingletonThreadingSafety(self) -> None:
        """
        Validates the thread safety of the singleton pattern for `Container` and `Orionis` classes.

        This method ensures that, even when multiple threads attempt to instantiate
        `Container` and `Orionis` simultaneously, only one instance of each class is created.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate thread-safe singleton behavior.
        """
        container_instances = []
        orionis_instances = []

        def create_container():
            """Create and append a Container instance in a thread."""
            time.sleep(0.01)  # Increase chance of race condition
            container_instances.append(Container())

        def create_orionis():
            """Create and append an Orionis instance in a thread."""
            time.sleep(0.01)  # Increase chance of race condition
            orionis_instances.append(Orionis())

        # Create threads for concurrent instantiation
        threads = []
        for i in range(10):
            t1 = threading.Thread(target=create_container)
            t2 = threading.Thread(target=create_orionis)
            threads.extend([t1, t2])

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Collect instance IDs for verification
        container_ids = [id(c) for c in container_instances]
        orionis_ids = [id(o) for o in orionis_instances]

        # Assert that only one unique instance exists for each class
        self.assertEqual(len(set(container_ids)), 1)
        self.assertEqual(len(set(orionis_ids)), 1)
        self.assertEqual(len(container_instances), 10)
        self.assertEqual(len(orionis_instances), 10)

    async def testInheritanceSeparation(self) -> None:
        """
        Ensures that singleton instances are maintained separately for `Container` and `Orionis` classes.

        This method checks that:
        - Each class maintains its own singleton instance.
        - Data added to one singleton does not affect the other.
        - Both classes correctly implement the singleton pattern independently.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate singleton separation.
        """
        container = Container()
        orionis = Orionis()

        # Add a callable to the Container singleton
        container.callable("test_container", lambda: "container_value")

        # Verify that Container and Orionis are distinct singletons
        self.assertEqual(type(container).__name__, "Container")
        self.assertEqual(type(orionis).__name__, "Application")
        self.assertIsNot(container, orionis)

        # Check that the callable is bound only to Container
        self.assertTrue(container.bound('test_container'))
        self.assertFalse(orionis.bound('test_container'))
