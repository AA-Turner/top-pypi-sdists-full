from orionis.container.container import Container
from orionis.container.facades.facade import Facade
from orionis.foundation.application import Application
from orionis.test.cases.asynchronous import AsyncTestCase
from tests.container.mocks.mock_simple_classes import Car, ICar

class TestContainer(AsyncTestCase):

    async def testTransientRegistration(self) -> None:
        """
        Tests the transient registration of a service in the container.

        This method verifies the following behaviors:
            - The `container.transient()` method correctly registers a transient binding from an abstract type (`ICar`) to a concrete implementation (`Car`).
            - Each call to `container.make(ICar)` returns a new instance of `Car`, confirming transient behavior.
            - The resolved instances are of the correct type (`Car`), and each instance is a distinct object.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        After the test, the registration for `ICar` is dropped from the container to clean up.
        """

        # Create a new container instance
        container = Container()

        # Register ICar as a transient binding to Car
        container.transient(ICar, Car)

        # Resolve two instances of ICar (should be different objects)
        instance1 = container.make(ICar)
        instance2 = container.make(ICar)

        # Assert both instances are of type Car
        self.assertIsInstance(instance1, Car)
        self.assertIsInstance(instance2, Car)

        # Assert that the instances are not the same object (transient behavior)
        self.assertIsNot(instance1, instance2)

        # Clean up registration
        container.drop(abstract=ICar)

    async def testSingletonRegistration(self) -> None:
        """
        Tests singleton registration and resolution from the container.

        This method ensures:
            - A class (`Car`) can be registered as a singleton implementation of an interface (`ICar`).
            - The container returns an instance of the registered implementation.
            - Multiple requests for the same interface return the same instance, confirming singleton behavior.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registration for `ICar` is dropped after the test.
        """

        # Create a new container instance
        container = Container()

        # Register ICar as a singleton binding to Car
        container.singleton(ICar, Car)

        # Resolve two instances of ICar (should be the same object)
        instance1 = container.make(ICar)
        instance2 = container.make(ICar)

        # Assert both instances are of type Car
        self.assertIsInstance(instance1, Car)
        self.assertIsInstance(instance2, Car)

        # Assert that both instances are the same object (singleton behavior)
        self.assertIs(instance1, instance2)

        # Clean up registration
        container.drop(abstract=ICar)

    async def testScopedRegistration(self) -> None:
        """
        Tests the scoped registration functionality of the container.

        This method verifies:
            - Within a single context, scoped registrations return the same instance when the same interface is requested multiple times.
            - Different contexts produce different instances of the same registration.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registration for `ICar` is dropped after the test.
        """

        # Create a new container instance
        container = Container()

        # First context: instances should be the same
        with container.createContext():
            container.scoped(ICar, Car)
            instance1 = container.make(ICar)
            instance2 = container.make(ICar)

            self.assertIsInstance(instance1, Car)
            self.assertIsInstance(instance2, Car)
            self.assertIs(instance1, instance2)

        # Second context: instance should be different from previous context
        with container.createContext():
            container.scoped(ICar, Car)
            instance3 = container.make(ICar)
            self.assertIsNot(instance1, instance3)

        # Clean up registration
        container.drop(abstract=ICar)

    async def testInstanceRegistration(self) -> None:
        """
        Tests instance registration in the container.

        This method ensures:
            - When an instance is registered to a service in the container, the container returns exactly the same instance when resolving that service.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registration for `ICar` is dropped after the test.
        """

        # Create a specific instance of Car
        car_instance = Car()
        container = Container()

        # Register a specific instance of Car to ICar
        container.instance(ICar, car_instance)

        # Resolve ICar and check that it returns the same instance
        resolved = container.make(ICar)
        self.assertIs(resolved, car_instance)

        # Clean up registration
        container.drop(abstract=ICar)

    async def testCallableRegistration(self) -> None:
        """
        Tests that callables can be registered and resolved from the container.

        This method verifies:
            - Functions can be registered in the container using the `callable()` method.
            - Registered functions can be resolved and executed using the `make()` method.
            - Arguments can be passed to the resolved functions as positional and keyword arguments.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registrations for 'add' and 'multiply' are dropped after the test.
        """

        # Define some simple functions to register
        def add(a: int, b: int) -> int:
            return a + b


        # Define another function to register
        def multiply(a: int, b: int) -> int:
            return a * b

        # Create a new container instance
        container = Container()

        # Register callables
        container.callable('add', add)
        container.callable('multiply', multiply)

        # Test resolution and execution with positional and keyword arguments
        self.assertEqual(container.make('add', 1, 2), 3)
        self.assertEqual(container.make('multiply', 3, 4), 12)
        self.assertEqual(container.make('add', a=5, b=7), 12)

        # Clean up registrations
        container.drop(alias='add')
        container.drop(alias='multiply')

    async def testTransientFacade(self) -> None:
        """
        Tests transient instance resolution using the Facade pattern.

        This method validates:
            - The container can register a transient binding between an interface and a class.
            - The Facade pattern correctly resolves instances of the registered interface.
            - Multiple calls to the Facade's `resolve()` method return different instances, confirming transient behavior.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registration for `ICar` is dropped after the test.
        """

        # Create a new container instance
        container = Application()

        # Register ICar as a transient binding to Car
        container.transient(ICar, Car)

        # Define a Facade class to access the ICar binding
        class CarFacade(Facade):
            @classmethod
            def getFacadeAccessor(cls):
                return ICar

        # Resolve two instances via Facade (should be different objects)
        instance1 = CarFacade.resolve()
        instance2 = CarFacade.resolve()

        self.assertIsInstance(instance1, Car)
        self.assertIsInstance(instance2, Car)
        self.assertIsNot(instance1, instance2)

        # Clean up registration
        container.drop(abstract=ICar)

    async def testSingletonFacade(self) -> None:
        """
        Tests singleton instance resolution using the Facade pattern.

        This method verifies:
            - A singleton binding can be registered in the container.
            - A Facade class can be created to access this binding.
            - Multiple resolutions through the Facade return the same instance, confirming singleton behavior.
            - The resolved instances are of the correct type (`Car`).

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registration for `ICar` is dropped after the test.
        """

        # Create a new container instance
        container = Application()

        # Register ICar as a singleton binding to Car
        container.singleton(ICar, Car)

        # Define a Facade class to access the ICar binding
        class CarFacade(Facade):
            @classmethod
            def getFacadeAccessor(cls):
                return ICar

        # Resolve two instances via Facade (should be the same object)
        instance1 = CarFacade.resolve()
        instance2 = CarFacade.resolve()

        # Assert both instances are of type Car and are the same object
        self.assertIsInstance(instance1, Car)
        self.assertIsInstance(instance2, Car)
        self.assertIs(instance1, instance2)

        # Clean up registration
        container.drop(abstract=ICar)

    async def testScopedFacade(self) -> None:
        """
        Tests the functionality of a Facade accessing a scoped service within a container context.

        This method verifies:
            - The Facade can properly resolve a scoped service.
            - Multiple resolves within the same scope return the same instance, confirming scoped behavior.
            - The resolved instance is of the correct type (`Car`).

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registration for `ICar` is dropped after the test.
        """

        # Create a new container instance
        container = Application()

        # Create a new scope/context
        with container.createContext():

            # Register ICar as a scoped binding to Car
            container.scoped(ICar, Car)

            # Define a Facade class to access the ICar binding
            class CarFacade(Facade):
                @classmethod
                def getFacadeAccessor(cls):
                    return ICar

            # Resolve two instances via Facade (should be the same object within the scope)
            instance1 = CarFacade.resolve()
            instance2 = CarFacade.resolve()

            # Assert both instances are of type Car and are the same object
            self.assertIsInstance(instance1, Car)
            self.assertIsInstance(instance2, Car)
            self.assertIs(instance1, instance2)

        # Clean up registration
        container.drop(abstract=ICar)

    async def testResolvingUnregisteredType(self) -> None:
        """
        Tests that attempting to resolve an unregistered type from the container raises an exception.

        This method ensures:
            - The container correctly validates that a type is registered before attempting to resolve it.
            - An exception is raised when attempting to resolve an unregistered type.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Raises
        ------
        Exception
            Raised when attempting to resolve an unregistered type.
        """

        # Create a new container instance
        container = Container()

        # Attempt to resolve an unregistered type; should raise Exception
        with self.assertRaises(Exception):
            container.make('ICar')

    async def testOverridingRegistration(self) -> None:
        """
        Tests the ability of the container to override existing registrations.

        This method verifies:
            - When a class is registered as a singleton for an interface.
            - A different class can later be registered for the same interface.
            - The container returns the new class when resolving the interface.
            - The new instance is different from the previous instance, confirming the override.

        Parameters
        ----------
        self : TestContainer
            The test case instance.

        Returns
        -------
        None
            This method does not return any value. Assertions are used to validate expected behavior.

        Notes
        -----
        The registration for `ICar` is dropped after the test.
        """

        # Create a new container instance
        class SportsCar(Car):
            def start(self):
                return f"{self.brand} {self.model} is starting."
            def stop(self):
                return f"{self.brand} {self.model} is stopping."

        # Create a new container instance
        container = Container()

        # Register ICar as a singleton binding to Car
        container.singleton(ICar, Car)
        first = container.make(ICar)
        self.assertIsInstance(first, Car)
        self.assertNotIsInstance(first, SportsCar)

        # Override registration: register ICar as a singleton binding to SportsCar
        container.singleton(ICar, SportsCar)
        second = container.make(ICar)
        self.assertIsInstance(second, SportsCar)
        self.assertIsNot(first, second)

        # Clean up registration
        container.drop(abstract=ICar)