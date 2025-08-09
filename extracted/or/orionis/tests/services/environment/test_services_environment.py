from orionis.services.environment.core.dot_env import DotEnv
from orionis.services.environment.env import Env
from orionis.services.environment.enums.value_type import EnvironmentValueType
from orionis.services.environment.key.key_generator import SecureKeyGenerator
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServicesEnvironment(AsyncTestCase):

    async def testSetAndGetConstants(self):
        """
        Stores and retrieves framework metadata constants using Env.set and Env.get.

        This test imports several metadata constants from the `orionis.metadata.framework` module,
        sets each constant in the Env storage using `Env.set`, and verifies that the operation succeeds.
        It then retrieves each constant using `Env.get` and asserts that the retrieved value matches
        the original constant.

        Parameters
        ----------
        self : TestServicesEnvironment
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate behavior.

        Notes
        -----
        - Ensures that `Env.set` returns True for each constant.
        - Ensures that `Env.get` returns the correct value for each constant.
        """
        from orionis.metadata.framework import (
            NAME, VERSION, AUTHOR, AUTHOR_EMAIL, DESCRIPTION,
            SKELETON, FRAMEWORK, DOCS, API, PYTHON_REQUIRES
        )

        # Prepare a dictionary of constant names and their values
        constants = {
            "NAME": NAME,
            "VERSION": VERSION,
            "AUTHOR": AUTHOR,
            "AUTHOR_EMAIL": AUTHOR_EMAIL,
            "DESCRIPTION": DESCRIPTION,
            "SKELETON": SKELETON,
            "FRAMEWORK": FRAMEWORK,
            "DOCS": DOCS,
            "API": API,
            "PYTHON_REQUIRES": PYTHON_REQUIRES
        }

        # Set each constant in the environment and assert the operation succeeds
        for key, value in constants.items():
            result = Env.set(key, value)
            self.assertTrue(result)

        # Retrieve each constant and assert the value matches the original
        for key, value in constants.items():
            retrieved = Env.get(key)
            self.assertEqual(retrieved, value)

    async def testGetNonExistentKey(self):
        """
        Test the behavior of `Env.get` when retrieving a non-existent environment key.

        This test verifies that attempting to retrieve a value for a key that has not been set
        in the environment returns `None`. This ensures that the environment behaves as expected
        when queried for missing keys.

        Parameters
        ----------
        self : TestServicesEnvironment
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate that `Env.get`
            returns `None` for a non-existent key.

        Notes
        -----
        - Ensures that `Env.get` returns `None` when the specified key does not exist in the environment.
        """

        # Attempt to retrieve a value for a key that has not been set.
        self.assertIsNone(Env.get("NON_EXISTENT_KEY"))

    async def testDotEnvSetAndGetWithType(self):
        """
        Test DotEnv.set and DotEnv.get with explicit EnvironmentValueType for various data types.

        This test verifies that the `DotEnv` class correctly stores and retrieves environment variables
        when an explicit `EnvironmentValueType` is provided. For each supported data type, the test sets
        a value using `DotEnv.set` with the corresponding `EnvironmentValueType`, then retrieves it using
        `DotEnv.get` and asserts that the returned value is correctly prefixed or formatted according to
        the specified type.

        Parameters
        ----------
        self : TestServicesEnvironment
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate the correct behavior
            of `DotEnv.set` and `DotEnv.get` with explicit type information.

        Notes
        -----
        - Ensures that values are stored and retrieved with the correct type prefixes or formatting.
        - Covers all supported types: PATH, STR, INT, FLOAT, BOOL, LIST, DICT, TUPLE, SET, BASE64.
        """

        env = DotEnv()

        # Set and assert a PATH value with explicit type
        env.set("CAST_EXAMPLE_PATH", '/tests', EnvironmentValueType.PATH)
        self.assertTrue(env.get("CAST_EXAMPLE_PATH").endswith('/tests'))

        # Set and assert a string value with explicit type
        env.set("CAST_EXAMPLE_STR", 'hello', EnvironmentValueType.STR)
        self.assertEqual(env.get("CAST_EXAMPLE_STR"), "hello")

        # Set and assert an integer value with explicit type
        env.set("CAST_EXAMPLE_INT", 123, EnvironmentValueType.INT)
        self.assertEqual(env.get("CAST_EXAMPLE_INT"), 123)

        # Set and assert a float value with explicit type
        env.set("CAST_EXAMPLE_FLOAT", 3.14, EnvironmentValueType.FLOAT)
        self.assertEqual(env.get("CAST_EXAMPLE_FLOAT"), 3.14)

        # Set and assert a boolean value with explicit type
        env.set("CAST_EXAMPLE_BOOL", True, EnvironmentValueType.BOOL)
        self.assertEqual(env.get("CAST_EXAMPLE_BOOL"), True)

        # Set and assert a list value with explicit type
        env.set("CAST_EXAMPLE_LIST", [1, 2, 3], EnvironmentValueType.LIST)
        self.assertEqual(env.get("CAST_EXAMPLE_LIST"), [1, 2, 3])

        # Set and assert a dictionary value with explicit type
        env.set("CAST_EXAMPLE_DICT", {"a": 1, "b": 2}, EnvironmentValueType.DICT)
        self.assertEqual(env.get("CAST_EXAMPLE_DICT"), {"a": 1, "b": 2})

        # Set and assert a tuple value with explicit type
        env.set("CAST_EXAMPLE_TUPLE", (1, 2), EnvironmentValueType.TUPLE)
        self.assertEqual(env.get("CAST_EXAMPLE_TUPLE"), (1, 2))

        # Set and assert a set value with explicit type
        env.set("CAST_EXAMPLE_SET", {1, 2, 3}, EnvironmentValueType.SET)
        self.assertEqual(env.get("CAST_EXAMPLE_SET"), {1, 2, 3})

        # Set and assert a base64 value with explicit type
        ramdon_text = SecureKeyGenerator.generate()
        env.set("CAST_EXAMPLE_BASE64", ramdon_text, EnvironmentValueType.BASE64)
        self.assertEqual(env.get("CAST_EXAMPLE_BASE64"), ramdon_text)

    async def testDotEnvSetAndGetWithoutType(self):
        """
        Test DotEnv.set and DotEnv.get without explicit EnvironmentValueType for various data types.

        This test verifies that the `DotEnv` class can store and retrieve environment variables of different
        Python data types without specifying an explicit `EnvironmentValueType`. It checks that the values
        are stored and retrieved as their string representations, and asserts the correctness of the returned
        values for each data type.

        Parameters
        ----------
        self : TestServicesEnvironment
            The test case instance.

        Returns
        -------
        None
            This method does not return a value. Assertions are used to validate that the returned values
            from `DotEnv.get` match the expected string representations for each data type.

        Notes
        -----
        - Ensures that values are stored and retrieved as strings when no explicit type is provided.
        - Covers various data types: path, str, int, float, bool, list, dict, tuple, set, and base64.
        """

        env = DotEnv()

        # Set and get a path value without explicit type
        env.set("EXAMPLE_PATH", '/tests')
        self.assertEqual(env.get("EXAMPLE_PATH"), '/tests')

        # Set and get a string value without explicit type
        env.set("EXAMPLE_STR", 'hello')
        self.assertEqual(env.get("EXAMPLE_STR"), 'hello')

        # Set and get an integer value without explicit type
        env.set("EXAMPLE_INT", 123)
        self.assertEqual(env.get("EXAMPLE_INT"), 123)

        # Set and get a float value without explicit type
        env.set("EXAMPLE_FLOAT", 3.14)
        self.assertEqual(env.get("EXAMPLE_FLOAT"), 3.14)

        # Set and get a boolean value without explicit type
        env.set("EXAMPLE_BOOL", True)
        self.assertEqual(env.get("EXAMPLE_BOOL"), True)

        # Set and get a list value without explicit type
        env.set("EXAMPLE_LIST", [1, 2, 3])
        self.assertEqual(env.get("EXAMPLE_LIST"), [1, 2, 3])

        # Set and get a dictionary value without explicit type
        env.set("EXAMPLE_DICT", {"a": 1, "b": 2})
        self.assertEqual(env.get("EXAMPLE_DICT"), {"a": 1, "b": 2})

        # Set and get a tuple value without explicit type
        env.set("EXAMPLE_TUPLE", (1, 2))
        self.assertEqual(env.get("EXAMPLE_TUPLE"), (1, 2))

        # Set and get a set value without explicit type
        env.set("EXAMPLE_SET", {1, 2, 3})
        self.assertEqual(env.get("EXAMPLE_SET"), {1, 2, 3})

        # Set and get a base64 value without explicit type
        ramdon_text = SecureKeyGenerator.generate()
        env.set("EXAMPLE_BASE64", ramdon_text)
        self.assertEqual(env.get("EXAMPLE_BASE64"), ramdon_text)