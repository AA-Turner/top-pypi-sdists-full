from orionis.support.standard.exceptions import OrionisStdValueException
from orionis.support.standard.std import StdClass
from orionis.test.cases.asynchronous import AsyncTestCase

class TestSupportStd(AsyncTestCase):

    async def testInitializationAndAccess(self):
        """
        Test initialization and attribute access of StdClass.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Verifies that StdClass can be instantiated with specific attributes and
        that those attributes are accessible after initialization.
        """
        obj = StdClass(
            first_name='Raul',
            last_name='Uñate',
            age=31
        )
        self.assertEqual(obj.first_name, 'Raul')
        self.assertEqual(obj.age, 31)

    async def testToDictReturnsCorrectData(self):
        """
        Test that StdClass.toDict returns a dictionary with correct attribute data.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Ensures that toDict() returns a dictionary containing all attributes and their values.
        """
        obj = StdClass(a=1, b=2)
        expected = {'a': 1, 'b': 2}
        self.assertEqual(obj.toDict(), expected)

    async def testUpdateAttributes(self):
        """
        Test updating multiple attributes using StdClass.update.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Verifies that update() sets multiple attributes as expected.
        """
        obj = StdClass()
        obj.update(foo='bar', number=42)
        self.assertEqual(obj.foo, 'bar')
        self.assertEqual(obj.number, 42)

    async def testUpdateReservedAttributeRaisesError(self):
        """
        Test that updating a reserved attribute raises OrionisStdValueException.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Ensures that attempting to update a reserved attribute (e.g., '__init__')
        raises the appropriate exception.
        """
        obj = StdClass()
        with self.assertRaises(OrionisStdValueException):
            obj.update(__init__='bad')

    async def testUpdateConflictingAttributeRaisesError(self):
        """
        Test that updating with a conflicting attribute name raises OrionisStdValueException.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Ensures that updating with a name that conflicts with an existing method
        or reserved attribute (e.g., 'toDict') raises an exception.
        """
        obj = StdClass()
        with self.assertRaises(OrionisStdValueException):
            obj.update(toDict='oops')

    async def testRemoveExistingAttributes(self):
        """
        Test removal of an existing attribute using StdClass.remove.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Removes an attribute and checks that it no longer exists, while others remain.
        """
        obj = StdClass(x=1, y=2)
        obj.remove('x')
        self.assertFalse(hasattr(obj, 'x'))
        self.assertTrue(hasattr(obj, 'y'))

    async def testRemoveNonExistingAttributeRaisesError(self):
        """
        Test that removing a non-existing attribute raises AttributeError.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Ensures that attempting to remove an attribute that does not exist raises an error.
        """
        obj = StdClass()
        with self.assertRaises(AttributeError):
            obj.remove('not_there')

    async def testFromDictCreatesEquivalentInstance(self):
        """
        Test creation of StdClass instance from a dictionary using fromDict.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Verifies that fromDict creates an instance whose attributes match the input dictionary.
        """
        data = {'a': 10, 'b': 20}
        obj = StdClass.fromDict(data)
        self.assertEqual(obj.toDict(), data)

    async def testReprAndStr(self):
        """
        Test __repr__ and __str__ methods of StdClass for expected output.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Checks that __repr__ includes the class name and __str__ includes attribute key-value pairs.
        """
        obj = StdClass(x=5)
        self.assertIn("StdClass", repr(obj))
        self.assertIn("'x': 5", str(obj))

    async def testEquality(self):
        """
        Test equality and inequality operations for StdClass instances.

        Parameters
        ----------
        self : TestSupportStd
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        Verifies that instances with identical attributes are equal and those with different attributes are not.
        """
        a = StdClass(x=1, y=2)
        b = StdClass(x=1, y=2)
        c = StdClass(x=3)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)