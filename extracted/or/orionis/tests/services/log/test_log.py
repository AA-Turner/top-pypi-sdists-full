from orionis.services.log.log_service import LoggerService
from orionis.support.facades.logger import Log
from orionis.test.cases.asynchronous import AsyncTestCase

class TestLoggerService(AsyncTestCase):

    async def testHasInfoMethod(self):
        """
        Checks if the LoggerService class has an 'info' method.

        Returns
        -------
        None
            This test passes if the 'info' method exists, otherwise it fails.
        """
        self.assertTrue(hasattr(LoggerService, "info"))

    async def testHasErrorMethod(self):
        """
        Checks if the LoggerService class has an 'error' method.

        Returns
        -------
        None
            This test passes if the 'error' method exists, otherwise it fails.
        """
        self.assertTrue(hasattr(LoggerService, "error"))

    async def testHasWarningMethod(self):
        """
        Checks if the LoggerService class has a 'warning' method.

        Returns
        -------
        None
            This test passes if the 'warning' method exists, otherwise it fails.
        """
        self.assertTrue(hasattr(LoggerService, "warning"))

    async def testHasDebugMethod(self):
        """
        Checks if the LoggerService class has a 'debug' method.

        Returns
        -------
        None
            This test passes if the 'debug' method exists, otherwise it fails.
        """
        self.assertTrue(hasattr(LoggerService, "debug"))

    async def testLoggerWritesInfo(self):
        """
        Tests that the logger writes an info-level message.

        Returns
        -------
        None
            This test passes if the info message is processed without error.
        """
        # Log an info message
        Log.info("Mensaje de prueba info")

    async def testLoggerWritesError(self):
        """
        Tests that the logger writes an error-level message.

        Returns
        -------
        None
            This test passes if the error message is processed without error.
        """
        # Log an error message
        Log.error("Mensaje de prueba error")

    async def testLoggerWritesWarning(self):
        """
        Tests that the logger writes a warning-level message.

        Returns
        -------
        None
            This test passes if the warning message is processed without error.
        """
        # Log a warning message
        Log.warning("Mensaje de prueba warning")

    async def testLoggerWritesDebug(self):
        """
        Tests that the logger writes a debug-level message.

        Returns
        -------
        None
            This test passes if the debug message is processed without error.
        """
        # Log a debug message
        Log.debug("Mensaje de prueba debug")