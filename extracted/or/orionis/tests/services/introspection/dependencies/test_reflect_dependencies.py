import asyncio
from orionis.services.introspection.dependencies.entities.argument import Argument
from orionis.services.introspection.dependencies.entities.resolve_argument import ResolveArguments
from orionis.services.introspection.dependencies.reflection import ReflectDependencies
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

        This test method verifies the correct functioning of dependency introspection for class constructors.
        It ensures that the ReflectDependencies class can properly analyze and resolve constructor parameters,
        returning them in the expected format with correct type information and metadata.

        Parameters
        ----------
        self : TestReflectDependencies
            The test case instance containing the test context and assertion methods.

        Returns
        -------
        None
            This test method does not return any value. It performs assertions to validate the dependency
            resolution functionality and will raise AssertionError if any validation fails.

        Notes
        -----
        This test validates the following aspects of constructor dependency resolution:
            - The returned constructor dependencies are an instance of ResolveArguments.
            - The unresolved dependencies dictionary is properly structured.
            - The 'user_repository' dependency is resolved as an instance of Argument.
            - The resolved dependency for 'user_repository' contains accurate metadata including
              module name, class name, full class path, and type reference (FakeUser).
        """

        # Initialize the ReflectDependencies utility with the UserController class
        depend = ReflectDependencies(UserController)

        # Retrieve constructor dependencies for analysis
        constructor_dependencies = depend.getConstructorDependencies()

        # Validate that the result is an instance of ResolveArguments
        self.assertIsInstance(constructor_dependencies, ResolveArguments)

        # Verify that unresolved dependencies are returned as a dictionary structure
        self.assertIsInstance(constructor_dependencies.unresolved, dict)

        # Extract the 'user_repository' dependency from resolved dependencies
        dep_user_repository = constructor_dependencies.resolved.get('user_repository')

        # Validate that the dependency is properly resolved as an Argument instance
        self.assertIsInstance(dep_user_repository, Argument)

        # Perform detailed validation of the resolved dependency metadata
        dependencies: Argument = dep_user_repository

        # Verify the module name matches the expected mock module
        self.assertEqual(dependencies.module_name, 'tests.services.introspection.dependencies.mocks.mock_user')

        # Verify the class name matches the expected FakeUser class
        self.assertEqual(dependencies.class_name, 'FakeUser')

        # Verify the full class path is correctly constructed
        self.assertEqual(dependencies.full_class_path, 'tests.services.introspection.dependencies.mocks.mock_user.FakeUser')

        # Verify the type reference points to the actual FakeUser class
        self.assertEqual(dependencies.type, FakeUser)

    async def testReflectionDependenciesGetMethodDependencies(self):
        """
        Test the retrieval and validation of method dependencies for the UserController class.

        This test method validates the ReflectDependencies utility's ability to introspect and resolve
        dependencies for a specific method ('createUserWithPermissions') within a target class.
        It ensures that all method parameters are correctly identified, resolved, and contain
        accurate metadata including module information, class names, and type references.

        The test performs comprehensive validation of:
            - The returned dependency resolution object structure and type
            - The absence of unresolved dependencies when all parameters can be resolved
            - The correct resolution of complex type dependencies (custom classes)
            - The accurate resolution of built-in type dependencies (generic types with parameters)
            - The proper extraction of module paths, class names, and full qualified paths
            - The correct type reference mapping for both custom and built-in types

        Parameters
        ----------
        self : TestReflectDependencies
            The test case instance containing assertion methods and test context.

        Returns
        -------
        None
            This method performs assertions and does not return any value. Test failure
            will raise AssertionError if any validation fails.

        Notes
        -----
        This test specifically validates two types of dependencies:
            - Custom class dependencies (FakeUserWithPermissions) with full module path resolution
            - Built-in generic type dependencies (list[str]) with proper type parameter handling

        The test ensures that the ReflectDependencies utility correctly handles both
        user-defined classes and Python built-in generic types when analyzing method signatures.
        """

        # Initialize the ReflectDependencies utility with UserController as the target class
        depend = ReflectDependencies(UserController)

        # Retrieve method dependencies for the 'createUserWithPermissions' method
        method_dependencies = depend.getMethodDependencies('createUserWithPermissions')

        # Validate that the result is an instance of ResolveArguments (dependency resolution container)
        self.assertIsInstance(method_dependencies, ResolveArguments)

        # Verify that unresolved dependencies are returned as a dictionary structure
        self.assertIsInstance(method_dependencies.unresolved, dict)

        # Extract and validate the 'user_permissions' dependency from resolved dependencies
        dep_user_permissions: Argument = method_dependencies.resolved.get('user_permissions')

        # Ensure the dependency is properly resolved as an Argument instance
        self.assertIsInstance(dep_user_permissions, Argument)

        # Validate the module name for the custom FakeUserWithPermissions class
        self.assertEqual(dep_user_permissions.module_name, 'tests.services.introspection.dependencies.mocks.mock_users_permissions')

        # Validate the class name extraction for the custom class
        self.assertEqual(dep_user_permissions.class_name, 'FakeUserWithPermissions')

        # Validate the full qualified class path construction
        self.assertEqual(dep_user_permissions.full_class_path, 'tests.services.introspection.dependencies.mocks.mock_users_permissions.FakeUserWithPermissions')

        # Validate the type reference points to the actual FakeUserWithPermissions class
        self.assertEqual(dep_user_permissions.type, FakeUserWithPermissions)

        # Extract and validate the 'permissions' dependency (built-in generic type)
        dep_permissions: Argument = method_dependencies.resolved.get('permissions')

        # Ensure the built-in type dependency is properly resolved as an Argument instance
        self.assertIsInstance(dep_permissions, Argument)

        # Validate the module name for built-in types (should be 'builtins')
        self.assertEqual(dep_permissions.module_name, 'builtins')

        # Validate the base class name for the generic list type
        self.assertEqual(dep_permissions.class_name, 'list')

        # Validate the full qualified path for built-in types
        self.assertEqual(dep_permissions.full_class_path, 'builtins.list')

        # Validate the type reference includes generic type parameters (list[str])
        self.assertEqual(dep_permissions.type, list[str])

    async def testReflectionDependenciesGetCallableDependencies(self):
        """
        Test the retrieval and validation of callable dependencies for a standalone asynchronous function.

        This test method validates the ReflectDependencies utility's ability to introspect and resolve
        dependencies for a standalone callable function (not bound to a class). It ensures that function
        parameters with default values are correctly identified and resolved, and that the dependency
        resolution process handles callable introspection appropriately.

        The test performs comprehensive validation of:
            - The returned dependency resolution object structure and type
            - The absence of unresolved dependencies when all parameters have default values
            - The correct resolution of parameters with default values to their actual default values
            - The proper handling of built-in type annotations (int) for function parameters
            - The validation that resolved dependencies contain the expected default values

        Parameters
        ----------
        self : TestReflectDependencies
            The test case instance containing assertion methods and test context.

        Returns
        -------
        None
            This method performs assertions and does not return any value. Test failure
            will raise AssertionError if any validation fails.

        Notes
        -----
        This test specifically validates callable dependency resolution for:
            - Asynchronous functions with type-annotated parameters
            - Parameters with default values (integers in this case)
            - The correct mapping of parameter names to their default values

        The test ensures that the ReflectDependencies utility correctly handles standalone
        callable functions and resolves their parameters to appropriate default values
        when those defaults are provided in the function signature.
        """

        # Define a sample asynchronous function with default parameter values for testing
        async def fake_function(x: int = 3, y: int = 4) -> int:
            """Asynchronously adds two integers with a short delay."""
            await asyncio.sleep(0.1)
            return x + y

        # Initialize the ReflectDependencies utility with the callable function as target
        depend = ReflectDependencies(fake_function)

        # Retrieve callable dependencies for analysis
        callable_dependencies = depend.getCallableDependencies()

        # Validate that the result is an instance of ResolveArguments (dependency resolution container)
        self.assertIsInstance(callable_dependencies, ResolveArguments)

        # Verify that unresolved dependencies are returned as a dictionary structure
        self.assertIsInstance(callable_dependencies.unresolved, dict)

        # Extract and validate the 'x' parameter dependency from resolved dependencies
        dep_x: Argument = callable_dependencies.resolved.get('x')

        # Verify that the 'x' parameter resolves to its default value of 3
        self.assertEqual(dep_x, 3)

        # Extract and validate the 'y' parameter dependency from resolved dependencies
        dep_y: Argument = callable_dependencies.resolved.get('y')

        # Verify that the 'y' parameter resolves to its default value of 4
        self.assertEqual(dep_y, 4)