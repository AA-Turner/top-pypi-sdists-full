from orionis.support.patterns.singleton import Singleton
from orionis.test.cases.asynchronous import AsyncTestCase

class TestPatternsSingleton(AsyncTestCase):

    async def testSingleton(self):
        """
        Tests the behavior of the Singleton metaclass.

        Validates that a class using the Singleton metaclass only ever creates a single instance,
        regardless of how many times it is instantiated. Also checks that the initial state of the
        singleton instance remains unchanged after subsequent instantiations.

        Parameters
        ----------
        self : TestPatternsSingleton
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to verify singleton behavior.

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