from orionis.foundation.config.queue.entities.database import Database
from orionis.foundation.config.queue.enums.strategy import Strategy
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigQueueDatabase(AsyncTestCase):

    async def testDefaultInitialization(self):
        """
        Test default initialization of Database.

        Ensures that a Database instance is initialized with the correct default values for
        table name, queue name, retry_after, and strategy.

        Returns
        -------
        None
        """
        db_queue = Database()
        self.assertEqual(db_queue.table, "jobs")
        self.assertEqual(db_queue.queue, "default")
        self.assertEqual(db_queue.retry_after, 90)
        self.assertEqual(db_queue.strategy, Strategy.FIFO.value)

    async def testTableNameValidation(self):
        """
        Test validation of the table name attribute.

        Checks that invalid table names raise an OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Database(table="1jobs")  # Starts with number
        with self.assertRaises(OrionisIntegrityException):
            Database(table="Jobs")  # Uppercase letter
        with self.assertRaises(OrionisIntegrityException):
            Database(table="jobs-table")  # Invalid character
        with self.assertRaises(OrionisIntegrityException):
            Database(table=123)  # Non-string value

    async def testQueueNameValidation(self):
        """
        Test validation of the queue name attribute.

        Checks that non-ASCII queue names and non-string values raise an OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Database(queue="café")  # Non-ASCII character
        with self.assertRaises(OrionisIntegrityException):
            Database(queue=123)  # Non-string value

    async def testRetryAfterValidation(self):
        """
        Test validation of the retry_after attribute.

        Ensures that non-positive integers and non-integer values raise an OrionisIntegrityException.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Database(retry_after=0)
        with self.assertRaises(OrionisIntegrityException):
            Database(retry_after=-1)
        with self.assertRaises(OrionisIntegrityException):
            Database(retry_after="90")  # String instead of int

    async def testStrategyValidation(self):
        """
        Test validation and normalization of the strategy attribute.

        Verifies that both string and Strategy enum inputs are handled properly, and that
        invalid inputs raise an OrionisIntegrityException.

        Returns
        -------
        None
        """
        # Test string inputs (case-insensitive)
        db1 = Database(strategy="fifo")
        self.assertEqual(db1.strategy, Strategy.FIFO.value)
        db2 = Database(strategy="LIFO")
        self.assertEqual(db2.strategy, Strategy.LIFO.value)

        # Test enum inputs
        db3 = Database(strategy=Strategy.PRIORITY)
        self.assertEqual(db3.strategy, Strategy.PRIORITY.value)

        # Test invalid inputs
        with self.assertRaises(OrionisIntegrityException):
            Database(strategy="invalid_strategy")
        with self.assertRaises(OrionisIntegrityException):
            Database(strategy=123)

    async def testToDictMethod(self):
        """
        Test the toDict method.

        Ensures that the toDict method returns a dictionary representation of the Database
        instance with all fields included and correct values.

        Returns
        -------
        None
        """
        db_queue = Database()
        result = db_queue.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["table"], "jobs")
        self.assertEqual(result["queue"], "default")
        self.assertEqual(result["retry_after"], 90)
        self.assertEqual(result["strategy"], Strategy.FIFO.value)

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that the Database class requires keyword arguments for initialization,
        enforcing kw_only=True in its dataclass decorator.

        Returns
        -------
        None
        """
        with self.assertRaises(TypeError):
            Database("jobs", "default", 90, Strategy.FIFO)