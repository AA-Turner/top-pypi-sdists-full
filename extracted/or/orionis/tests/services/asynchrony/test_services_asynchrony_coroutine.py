
import asyncio
from orionis.services.asynchrony.coroutines import Coroutine
from orionis.services.asynchrony.exceptions import OrionisCoroutineException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServicesAsynchronyCoroutine(AsyncTestCase):

    async def testExecuteWithActiveEventLoop(self):
        """
        Tests coroutine execution within an active event loop.

        This method verifies that a coroutine can be executed successfully when an event loop is already running,
        such as in asynchronous environments (e.g., Jupyter notebooks or ASGI applications). It ensures that the
        Coroutine wrapper correctly awaits and returns the result of the coroutine.

        Returns
        -------
        None
            This is a test method and does not return a value. It asserts that the coroutine result matches the expected output.
        """

        # Simple coroutine that returns a string
        async def sample_coroutine():
            asyncio.sleep(0.1)
            return "Hello, World!"

        # Await the result of running the coroutine using the Coroutine wrapper
        result = await Coroutine(sample_coroutine()).run()

        # Assert that the result matches the expected output
        self.assertEqual(result, "Hello, World!")

    def testExecuteWithoutActiveEventLoop(self):
        """
        Tests coroutine execution without an active event loop.

        This method simulates the scenario where a coroutine is executed in a synchronous context,
        such as a standard Python script, where no event loop is running. It verifies that the
        Coroutine wrapper can correctly create and manage an event loop internally, execute the
        coroutine, and return the expected result.

        Returns
        -------
        None
            This test method does not return a value. It asserts that the coroutine result matches the expected output.
        """

        # Define a simple coroutine that returns a string
        async def sample_coroutine():
            asyncio.sleep(0.1)
            return "Hello, World!"

        # Run the coroutine using the Coroutine wrapper, which should handle event loop creation
        result = Coroutine(sample_coroutine()).run()

        # Assert that the result matches the expected output
        self.assertEqual(result, "Hello, World!")

    def testExecuteWithNonCoroutine(self):
        """
        Tests execution of a non-coroutine object.

        This method verifies that passing a non-coroutine object to the Coroutine wrapper
        raises an OrionisCoroutineException. It ensures that the Coroutine class enforces
        the requirement for coroutine objects and does not accept regular functions or other types.

        Parameters
        ----------
        self : TestServicesAsynchronyCoroutine
            The test case instance.

        Returns
        -------
        None
            This test method does not return a value. It asserts that the appropriate exception is raised.
        """

        # Define a regular function (not a coroutine)
        def sample_no_coroutine():
            return "Hello, World!"

        # Assert that passing a non-coroutine raises OrionisCoroutineException
        with self.assertRaises(OrionisCoroutineException):
            Coroutine(sample_no_coroutine()).run()