from orionis.foundation.config.mail.entities.mailers import Mailers
from orionis.foundation.config.mail.entities.smtp import Smtp
from orionis.foundation.config.mail.entities.file import File
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigMailMailers(AsyncTestCase):
    """
    Unit tests for the Mailers class.

    This test suite verifies the correct initialization, type validation,
    custom initialization, dictionary conversion, and keyword-only enforcement
    of the Mailers class.
    """

    async def testDefaultInitialization(self):
        """
        Test default initialization of Mailers.

        Ensures that a Mailers instance is initialized with default factories
        and that the `smtp` and `file` attributes are instances of their
        respective types.

        Returns
        -------
        None
        """
        mailers = Mailers()
        self.assertIsInstance(mailers.smtp, Smtp)
        self.assertIsInstance(mailers.file, File)

    async def testTypeValidation(self):
        """
        Test type validation for smtp and file attributes.

        Ensures that providing invalid types for `smtp` or `file` raises
        an OrionisIntegrityException.

        Returns
        -------
        None

        Raises
        ------
        OrionisIntegrityException
            If an invalid type is provided for `smtp` or `file`.
        """
        with self.assertRaises(OrionisIntegrityException):
            Mailers(smtp="invalid_smtp")
        with self.assertRaises(OrionisIntegrityException):
            Mailers(file="invalid_file")

    async def testCustomInitialization(self):
        """
        Test custom initialization with valid parameters.

        Ensures that valid Smtp and File instances can be provided to the
        Mailers constructor and are correctly assigned.

        Returns
        -------
        None
        """
        custom_smtp = Smtp()
        custom_file = File()
        mailers = Mailers(smtp=custom_smtp, file=custom_file)
        self.assertIs(mailers.smtp, custom_smtp)
        self.assertIs(mailers.file, custom_file)

    async def testToDictMethod(self):
        """
        Test the toDict method of Mailers.

        Ensures that the `toDict` method returns a dictionary representation
        containing all fields with correct values and types.

        Returns
        -------
        None
        """
        mailers = Mailers()
        result = mailers.toDict()
        self.assertIsInstance(result, dict)
        self.assertIn("smtp", result)
        self.assertIn("file", result)
        self.assertIsInstance(result["smtp"], dict)
        self.assertIsInstance(result["file"], dict)

    async def testKwOnlyInitialization(self):
        """
        Test keyword-only initialization enforcement.

        Ensures that the Mailers class enforces keyword-only arguments
        during initialization (i.e., `kw_only=True` in its dataclass decorator).

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If positional arguments are provided to the constructor.
        """
        with self.assertRaises(TypeError):
            Mailers(Smtp(), File())