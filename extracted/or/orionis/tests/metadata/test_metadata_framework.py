from orionis.metadata.framework import *
from orionis.test.cases.asynchronous import AsyncTestCase

class TestMetadataFramework(AsyncTestCase):
    """
    Test cases for the metadata constants and utility functions in orionis.metadata.framework.
    """

    async def testConstantsExistAndAreStr(self):
        """
        Test that all required metadata constants exist and are of type `str`.

        This method iterates over a predefined list of metadata constants and checks
        that each is an instance of `str`. This ensures that the metadata values
        required by the framework are properly defined and typed.

        Returns
        -------
        None
            This is a test method and does not return any value. Assertions are used
            to validate the conditions.
        """

        # List of metadata constants to check
        for const in [
            NAME, VERSION, AUTHOR, AUTHOR_EMAIL, DESCRIPTION,
            SKELETON, FRAMEWORK, DOCS, API, PYTHON_REQUIRES
        ]:
            # Assert that each constant is a string
            self.assertIsInstance(const, str)

    async def testClassifiersStructure(self):
        """
        Validate the structure and type of the `CLASSIFIERS` metadata constant.

        This test ensures that the `CLASSIFIERS` constant is a list of strings,
        and that each string contains at least one '::' separator, which is
        typical for Python package classifiers.

        Parameters
        ----------
        self : TestMetadataFramework
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to
            validate the structure and contents of `CLASSIFIERS`.
        """

        # Assert that CLASSIFIERS is a list
        self.assertIsInstance(CLASSIFIERS, list)
        for item in CLASSIFIERS:

            # Assert that each item in CLASSIFIERS is a string
            self.assertIsInstance(item, str)

            # Assert that each classifier string contains at least one '::' separator
            self.assertTrue("::" in item or len(item.split("::")) > 1)

    async def testKeywords(self):
        """
        Validate the structure and contents of the `KEYWORDS` metadata constant.

        This test checks that the `KEYWORDS` constant is a list of strings, ensuring
        that each keyword is properly typed. Additionally, it verifies that the list
        contains the essential keywords "orionis" and "framework", which are required
        for accurate metadata representation.

        Parameters
        ----------
        self : TestMetadataFramework
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate
            the structure and contents of `KEYWORDS`.
        """

        # Assert that KEYWORDS is a list
        self.assertIsInstance(KEYWORDS, list)

        # Check that each keyword in KEYWORDS is a string
        for kw in KEYWORDS:
            self.assertIsInstance(kw, str)

        # Ensure essential keywords are present in the list
        self.assertIn("orionis", KEYWORDS)
        self.assertIn("framework", KEYWORDS)

    async def testRequiresStructure(self):
        """
        Validate the structure and contents of the `REQUIRES` metadata constant.

        This test checks that the `REQUIRES` constant is a list of strings, where each string
        represents a package requirement and contains the '>=' version specifier. This ensures
        that all requirements are properly typed and formatted for dependency management.

        Parameters
        ----------
        self : TestMetadataFramework
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate
            the structure and contents of `REQUIRES`.
        """

        # Assert that REQUIRES is a list
        self.assertIsInstance(REQUIRES, list)

        # Check that each requirement in REQUIRES is a string and contains '>='
        for req in REQUIRES:
            self.assertIsInstance(req, str)  # Each requirement should be a string
            self.assertIn(">=", req)         # Each requirement should specify a minimum version

    async def testIconFunction(self):
        """
        Test the behavior and return type of the `icon()` utility function.

        This test verifies that the `icon()` function returns either a string containing
        SVG data or `None` if the icon file is not found. It ensures that the function's
        output is correctly typed and handles missing resources gracefully.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate
            the type and behavior of the `icon()` function.
        """
        # Call the icon() function and store the result
        result = icon()

        # Assert that the result is either a string (SVG data) or None (file not found)
        self.assertTrue(isinstance(result, str) or result is None)
