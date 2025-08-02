from orionis.container.entities.binding import Binding
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.exceptions.type import OrionisContainerTypeError
from orionis.test.cases.asynchronous import AsyncTestCase

class TestEntities(AsyncTestCase):

    async def testBindingInitialization(self):
        """
        Test initialization of a Binding object with default values.

        This test verifies that when a Binding instance is created without any arguments,
        all attributes are set to their expected default values.

        Parameters
        ----------
        self : TestBinding
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. Assertions are used to validate behavior.

        Raises
        ------
        AssertionError
            If any of the default values are incorrect or the Binding initialization fails.
        """

        # Create a Binding instance with default parameters
        binding: Binding = Binding()

        # Assert that all attributes are set to their default values
        self.assertIsNone(binding.contract)                         # Default contract should be None
        self.assertIsNone(binding.concrete)                         # Default concrete should be None
        self.assertIsNone(binding.instance)                         # Default instance should be None
        self.assertIsNone(binding.function)                         # Default function should be None
        self.assertEqual(binding.lifetime, Lifetime.TRANSIENT)      # Default lifetime should be TRANSIENT
        self.assertFalse(binding.enforce_decoupling)                # Default enforce_decoupling should be False
        self.assertIsNone(binding.alias)                            # Default alias should be None

    async def testBindingCustomValues(self):
        """
        Test initialization of a Binding object with custom values.

        This test verifies that when a Binding instance is created with explicit arguments,
        all attributes are set to the provided custom values, and the object reflects the intended configuration.

        Parameters
        ----------
        self : TestBinding
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. Assertions are used to validate correct attribute assignment.

        Raises
        ------
        AssertionError
            If the Binding initialization fails or custom values are not set correctly.
        """

        # Define dummy contract and concrete classes for testing
        class TestContract: pass
        class TestConcrete: pass

        # Create an instance for the 'instance' attribute
        instance = TestConcrete()

        # Define a factory function for the 'function' attribute
        factory_func = lambda: TestConcrete()

        # Initialize Binding with custom values
        binding = Binding(
            contract=TestContract,
            concrete=TestConcrete,
            instance=instance,
            function=factory_func,
            lifetime=Lifetime.SINGLETON,
            enforce_decoupling=True,
            alias="test_binding"
        )

        # Assert that all attributes are set to the provided custom values
        self.assertIs(binding.contract, TestContract)
        self.assertIs(binding.concrete, TestConcrete)
        self.assertIs(binding.instance, instance)
        self.assertIs(binding.function, factory_func)
        self.assertEqual(binding.lifetime, Lifetime.SINGLETON)
        self.assertTrue(binding.enforce_decoupling)
        self.assertEqual(binding.alias, "test_binding")

    async def testBindingPostInitValidation(self):
        """
        Validates that the `__post_init__` method of the `Binding` class raises appropriate
        exceptions when invalid types are provided for certain attributes.

        This test ensures that type validation is enforced for the `lifetime`, `enforce_decoupling`,
        and `alias` attributes during initialization. If an invalid type is passed, the
        `OrionisContainerTypeError` should be raised.

        Parameters
        ----------
        self : TestBinding
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. Assertions are used to validate that
            exceptions are raised for invalid input types.

        Raises
        ------
        AssertionError
            If the expected `OrionisContainerTypeError` is not raised when invalid types
            are provided for the attributes.
        """

        # Attempt to initialize Binding with an invalid lifetime type (should raise exception)
        with self.assertRaises(OrionisContainerTypeError):
            Binding(lifetime="not_a_lifetime")

        # Attempt to initialize Binding with an invalid enforce_decoupling type (should raise exception)
        with self.assertRaises(OrionisContainerTypeError):
            Binding(enforce_decoupling="not_a_bool")

        # Attempt to initialize Binding with an invalid alias type (should raise exception)
        with self.assertRaises(OrionisContainerTypeError):
            Binding(alias=123)

    async def testToDictMethod(self):
        """
        Tests the `toDict` method of the `Binding` class to ensure it returns a correct dictionary representation
        of the binding's attributes.

        This test verifies that the dictionary contains all expected keys and that their values match the attributes
        set during initialization. It also checks that the types and values are correctly preserved.

        Parameters
        ----------
        self : TestBinding
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. Assertions are used to validate the correctness of the dictionary representation.

        Raises
        ------
        AssertionError
            If the dictionary representation is incorrect or any attribute does not match the expected value.
        """

        # Define dummy contract and concrete classes for testing
        class TestContract: pass
        class TestConcrete: pass

        # Create a Binding instance with custom values
        binding = Binding(
            contract=TestContract,
            concrete=TestConcrete,
            lifetime=Lifetime.SINGLETON,
            enforce_decoupling=True,
            alias="test_binding"
        )

        # Get the dictionary representation of the binding
        result = binding.toDict()

        # Assert that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Assert that contract and concrete are correctly set
        self.assertIs(result["contract"], TestContract)
        self.assertIs(result["concrete"], TestConcrete)

        # Assert that instance and function are None by default
        self.assertIsNone(result["instance"])
        self.assertIsNone(result["function"])

        # Assert that lifetime, enforce_decoupling, and alias are correctly set
        self.assertEqual(result["lifetime"], Lifetime.SINGLETON)
        self.assertTrue(result["enforce_decoupling"])
        self.assertEqual(result["alias"], "test_binding")

    async def testGetFieldsMethod(self):
        """
        Tests the `getFields` method of the `Binding` class to ensure it returns accurate field metadata.

        This test verifies that the returned list contains the expected number of fields, that all expected
        field names are present, and that specific field metadata (such as default values and descriptions)
        are correctly provided for the `lifetime` field.

        Parameters
        ----------
        self : TestBinding
            The test case instance.

        Returns
        -------
        None
            This method does not return anything. Assertions are used to validate the correctness of the
            field metadata returned by `getFields`.

        Raises
        ------
        AssertionError
            If the field information is incorrect, such as missing fields, incorrect defaults, or missing metadata.
        """

        # Create a Binding instance with default parameters
        binding = Binding()

        # Retrieve field metadata using getFields
        fields_info = binding.getFields()

        # Assert that the returned value is a list
        self.assertIsInstance(fields_info, list)

        # Assert that there are exactly 7 fields
        self.assertEqual(len(fields_info), 7)

        # Extract field names from the metadata
        field_names = [field["name"] for field in fields_info]
        expected_names = ["contract", "concrete", "instance", "function", "lifetime", "enforce_decoupling", "alias"]

        # Assert that all expected field names are present
        self.assertTrue(all(name in field_names for name in expected_names))

        # Find the metadata for the 'lifetime' field
        lifetime_field = next(field for field in fields_info if field["name"] == "lifetime")

        # Assert that the default value for 'lifetime' is correct
        self.assertEqual(lifetime_field["default"], Lifetime.TRANSIENT.value)

        # Assert that the 'lifetime' field contains a description in its metadata
        self.assertIn("description", lifetime_field["metadata"])