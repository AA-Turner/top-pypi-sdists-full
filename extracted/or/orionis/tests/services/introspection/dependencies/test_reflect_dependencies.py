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
    Test suite for verifying the functionality of the ReflectDependencies class in resolving and reflecting dependencies for class constructors and methods.
    This test class covers:
        - Retrieval and resolution of constructor dependencies for the UserController class.
        - Validation that constructor dependencies are correctly identified as instances of ClassDependency.
        - Verification that resolved dependencies (such as 'user_repository') are instances of KnownDependency and have the expected module name, class name, full class path, and type.
        - Reflection and resolution of method dependencies for specific methods (e.g., 'createUserWithPermissions').
        - Validation that method dependencies are correctly identified as instances of MethodDependency.
        - Verification that resolved method dependencies (such as 'user_permissions' and 'permissions') are instances of KnownDependency and have the expected attributes.
        - Ensuring that unresolved dependencies lists are empty where appropriate.
    """

    async def testReflectionDependenciesGetConstructorDependencies(self):
        """
        Test that ReflectDependencies correctly retrieves and resolves constructor dependencies for the UserController class.
        This test verifies:
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
        Tests the `getMethodDependencies` method of the `ReflectDependencies` class for the 'createUserWithPermissions' method
        of the `UserController`.
        This test verifies:
            - The returned object is an instance of `MethodDependency`.
            - There are no unresolved dependencies.
            - The 'user_permissions' dependency is correctly resolved as an instance of `KnownDependency` with the expected
              module name, class name, full class path, and type (`FakeUserWithPermissions`).
            - The 'permissions' dependency is correctly resolved as an instance of `KnownDependency` with the expected
              module name, class name, full class path, and type (`list[str]`).
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
        Tests the `getCallableDependencies` method of the `ReflectDependencies` class for a callable function.
        This test verifies:
            - The returned dependencies are an instance of `MethodDependency`.
            - There are no unresolved dependencies.
            - The 'x' and 'y' parameters are correctly resolved as instances of `KnownDependency` with the expected
              module name, class name, full class path, and type (`int`).
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