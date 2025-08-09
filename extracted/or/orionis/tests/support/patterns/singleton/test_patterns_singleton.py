from orionis.support.patterns.singleton import Singleton
from orionis.test.cases.asynchronous import AsyncTestCase

class TestPatternsSingleton(AsyncTestCase):

    async def testSingleton(self):
        """
        Test the Singleton metaclass to ensure only one instance is created.

        This test verifies that a class using the Singleton metaclass will always return
        the same instance, regardless of how many times it is instantiated. It also checks
        that the initial state of the singleton instance does not change after subsequent
        instantiations with different arguments.

        Parameters
        ----------
        self : TestPatternsSingleton
            Instance of the test case.

        Returns
        -------
        None
        """
        # Define a class using the Singleton metaclass
        class SingletonClass(metaclass=Singleton):
            def __init__(self, value):
                self.value = value

        # Create the first instance of SingletonClass
        instance1 = SingletonClass(1)

        # Attempt to create a second instance with a different value
        instance2 = SingletonClass(2)

        # Assert that both instances are actually the same object
        self.assertIs(instance1, instance2)

        # Assert that the value remains as set by the first instantiation
        self.assertEqual(instance1.value, 1)
