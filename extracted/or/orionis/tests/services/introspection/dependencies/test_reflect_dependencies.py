import asyncio
from orionis.services.introspection.dependencies.entities.callable_dependencies import CallableDependency
from orionis.services.introspection.dependencies.reflection import (
    ReflectDependencies,
    ClassDependency,
    MethodDependency,
    KnownDependency
)
from orionis.test.cases.asynchronous import AsyncTestCase
from tests.services.introspection.dependencies.mocks.mock_user import FakeUser
from tests.services.introspection.dependencies.mocks.mock_user_controller import UserController
from tests.services.introspection.dependencies.mocks.mock_users_permissions import FakeUserWithPermissions

class TestReflectDependencies(AsyncTestCase):
    """
    Test suite for the ReflectDependencies class, which provides utilities for introspecting and resolving dependencies
    in class constructors, methods, and callables.

    This class contains asynchronous test cases that validate:
        - The correct retrieval and resolution of constructor dependencies for the UserController class.
        - The identification of constructor dependencies as instances of ClassDependency.
        - The resolution of dependencies such as 'user_repository' as KnownDependency instances, including validation
          of their module name, class name, full class path, and type.
        - The reflection and resolution of method dependencies for specific methods (e.g., 'createUserWithPermissions'),
          ensuring they are identified as MethodDependency instances.
        - The resolution of method dependencies such as 'user_permissions' and 'permissions' as KnownDependency instances,
          with correct attributes.
        - That unresolved dependency lists are empty when all dependencies are resolved.

    Attributes
    ----------
    Inherits from AsyncTestCase.

    Methods
    -------
    testReflectionDependenciesGetConstructorDependencies()
        Tests retrieval and validation of constructor dependencies for UserController.

    testReflectionDependenciesGetMethodDependencies()
        Tests retrieval and validation of method dependencies for the 'createUserWithPermissions' method.

    testReflectionDependenciesGetCallableDependencies()
        Tests retrieval and validation of dependencies for a sample asynchronous callable.
    """

    async def testReflectionDependenciesGetConstructorDependencies(self):
        """
        Retrieves and validates the constructor dependencies for the UserController class using the ReflectDependencies utility.

        Parameters
        ----------
        self : TestReflectDependencies
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        This test ensures that:
            - The returned constructor dependencies are an instance of ClassDependency.
            - The list of unresolved dependencies is empty.
            - The 'user_repository' dependency is resolved as an instance of KnownDependency.
            - The resolved dependency for 'user_repository' has the expected module name, class name, full class path, and type (FakeUser).
        """

        depend = ReflectDependencies(UserController)
        constructor_dependencies = depend.getConstructorDependencies()

        # Check Instance of ClassDependency
        self.assertIsInstance(constructor_dependencies, ClassDependency)

        self.assertEqual(constructor_dependencies.unresolved, [])

        # Check Instance of KnownDependency
        dep_user_repository = constructor_dependencies.resolved.get('user_repository')
        self.assertIsInstance(dep_user_repository, KnownDependency)

        # Check resolved dependencies for 'user_repository'
        dependencies:KnownDependency = dep_user_repository
        self.assertEqual(dependencies.module_name, 'tests.services.introspection.dependencies.mocks.mock_user')
        self.assertEqual(dependencies.class_name, 'FakeUser')
        self.assertEqual(dependencies.full_class_path, 'tests.services.introspection.dependencies.mocks.mock_user.FakeUser')
        self.assertEqual(dependencies.type, FakeUser)

    async def testReflectionDependenciesGetMethodDependencies(self):
        """
        Retrieves and validates the dependencies for the 'createUserWithPermissions' method of the UserController class
        using the ReflectDependencies utility.

        This test ensures that:
            - The returned object is an instance of MethodDependency.
            - The unresolved dependencies list is empty.
            - The 'user_permissions' dependency is resolved as a KnownDependency with the expected module name,
              class name, full class path, and type (FakeUserWithPermissions).
            - The 'permissions' dependency is resolved as a KnownDependency with the expected module name,
              class name, full class path, and type (list[str]).

        Parameters
        ----------
        self : TestReflectDependencies
            The test case instance.

        Returns
        -------
        None
        """

        depend = ReflectDependencies(UserController)
        method_dependencies = depend.getMethodDependencies('createUserWithPermissions')

        # Check Instance of MethodDependency
        self.assertIsInstance(method_dependencies, MethodDependency)

        # Check unresolved dependencies
        self.assertEqual(method_dependencies.unresolved, [])

        # Check Instance of KnownDependency for 'user_permissions'
        dep_user_permissions:KnownDependency = method_dependencies.resolved.get('user_permissions')
        self.assertIsInstance(dep_user_permissions, KnownDependency)

        # Check resolved dependencies for 'user_permissions'
        self.assertEqual(dep_user_permissions.module_name, 'tests.services.introspection.dependencies.mocks.mock_users_permissions')
        self.assertEqual(dep_user_permissions.class_name, 'FakeUserWithPermissions')
        self.assertEqual(dep_user_permissions.full_class_path, 'tests.services.introspection.dependencies.mocks.mock_users_permissions.FakeUserWithPermissions')
        self.assertEqual(dep_user_permissions.type, FakeUserWithPermissions)

        # Check Instance of KnownDependency for 'permissions'
        dep_permissions:KnownDependency = method_dependencies.resolved.get('permissions')
        self.assertIsInstance(dep_permissions, KnownDependency)

        # Check resolved dependencies for 'permissions'
        self.assertEqual(dep_permissions.module_name, 'builtins')
        self.assertEqual(dep_permissions.class_name, 'list')
        self.assertEqual(dep_permissions.full_class_path, 'builtins.list')
        self.assertEqual(dep_permissions.type, list[str])

    async def testReflectionDependenciesGetCallableDependencies(self):
        """
        Tests the `getCallableDependencies` method of the `ReflectDependencies` class for a given asynchronous function.

        Parameters
        ----------
        self : TestReflectDependencies
            The test case instance.

        Returns
        -------
        None

        Notes
        -----
        This test checks that:
            - The returned dependencies are an instance of `CallableDependency`.
            - There are no unresolved dependencies.
            - The 'x' and 'y' parameters are resolved to their default integer values (3 and 4, respectively).
        """

        async def fake_function(x: int = 3, y: int = 4) -> int:
            """Asynchronously adds two integers with a short delay."""
            await asyncio.sleep(0.1)
            return x + y

        depend = ReflectDependencies()
        callable_dependencies = depend.getCallableDependencies(fake_function)

        # Check Instance of MethodDependency
        self.assertIsInstance(callable_dependencies, CallableDependency)

        # Check unresolved dependencies
        self.assertEqual(callable_dependencies.unresolved, [])

        # Check Instance of KnownDependency for 'x'
        dep_x:KnownDependency = callable_dependencies.resolved.get('x')
        self.assertEqual(dep_x, 3)

        # Check Instance of KnownDependency for 'y'
        dep_y:KnownDependency = callable_dependencies.resolved.get('y')
        self.assertEqual(dep_y, 4)