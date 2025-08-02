from orionis.support.standard.exceptions import OrionisStdValueException
from orionis.support.standard.std import StdClass
from orionis.test.cases.asynchronous import AsyncTestCase

class TestSupportStd(AsyncTestCase):

    async def testInitializationAndAccess(self):
        """
        Test the initialization of StdClass and access to its attributes.

        Notes
        -----
        Verifies that an instance of StdClass can be created with the given
        first name, last name, and age, and that these attributes can be accessed
        correctly after initialization.
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
        Test that the toDict method of StdClass returns a dictionary with the correct data.

        Notes
        -----
        Creates an instance of StdClass with specific attributes and verifies
        that calling toDict() returns a dictionary containing those attributes and their values.
        """
        obj = StdClass(a=1, b=2)
        expected = {'a': 1, 'b': 2}
        self.assertEqual(obj.toDict(), expected)

    async def testUpdateAttributes(self):
        """
        Test that the `update` method of `StdClass` correctly sets multiple attributes.

        Notes
        -----
        Creates an instance of `StdClass`, updates its attributes using the `update` method,
        and asserts that the attributes `foo` and `number` are set to the expected values.
        """
        obj = StdClass()
        obj.update(foo='bar', number=42)
        self.assertEqual(obj.foo, 'bar')
        self.assertEqual(obj.number, 42)

    async def testUpdateReservedAttributeRaisesError(self):
        """
        Test that updating a reserved attribute (such as '__init__') on a StdClass instance
        raises a ValueError exception.

        Notes
        -----
        Ensures that updating a reserved attribute raises an OrionisStdValueException.
        """
        obj = StdClass()
        with self.assertRaises(OrionisStdValueException):
            obj.update(__init__='bad')

    async def testUpdateConflictingAttributeRaisesError(self):
        """
        Test that updating an object with a conflicting attribute name ('toDict') raises a ValueError.

        Notes
        -----
        Ensures that attempting to update the StdClass instance with a keyword argument
        that conflicts with an existing method or reserved attribute ('toDict') correctly triggers
        an OrionisStdValueException, enforcing attribute safety.
        """
        obj = StdClass()
        with self.assertRaises(OrionisStdValueException):
            obj.update(toDict='oops')

    async def testRemoveExistingAttributes(self):
        """
        Test that the `remove` method of `StdClass` successfully removes an existing attribute.

        Notes
        -----
        Removes attribute 'x' from the object and checks that 'y' remains.
        """
        obj = StdClass(x=1, y=2)
        obj.remove('x')
        self.assertFalse(hasattr(obj, 'x'))
        self.assertTrue(hasattr(obj, 'y'))

    async def testRemoveNonExistingAttributeRaisesError(self):
        """
        Test that attempting to remove a non-existing attribute from a StdClass instance raises an AttributeError.

        Notes
        -----
        Verifies that the `remove` method of `StdClass` raises an AttributeError
        when called with the name of an attribute that does not exist on the object.
        """
        obj = StdClass()
        with self.assertRaises(AttributeError):
            obj.remove('not_there')

    async def testFromDictCreatesEquivalentInstance(self):
        """
        Test that StdClass.from_dict creates an instance equivalent to the original data.

        Notes
        -----
        Verifies that when a dictionary is passed to StdClass.from_dict,
        the resulting object's toDict() method returns a dictionary equal to the original input.
        """
        data = {'a': 10, 'b': 20}
        obj = StdClass.fromDict(data)
        self.assertEqual(obj.toDict(), data)

    async def testReprAndStr(self):
        """
        Test that the __repr__ and __str__ methods of StdClass include the class name and the value of 'x' respectively.

        Notes
        -----
        - Checks that repr(obj) contains the class name 'StdClass'.
        - Checks that str(obj) contains the key-value pair "'x': 5".
        """
        obj = StdClass(x=5)
        self.assertIn("StdClass", repr(obj))
        self.assertIn("'x': 5", str(obj))

    async def testEquality(self):
        """
        Test the equality and inequality operations for StdClass instances.

        Notes
        -----
        Creates three instances of StdClass:
        - 'a' and 'b' with identical attributes (x=1, y=2), which should be considered equal.
        - 'c' with a different attribute (x=3), which should not be equal to 'a'.

        Asserts
        -------
        - 'a' and 'b' are equal.
        - 'a' and 'c' are not equal.
        """
        a = StdClass(x=1, y=2)
        b = StdClass(x=1, y=2)
        c = StdClass(x=3)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)