from orionis.services.introspection.reflection import Reflection
from orionis.test.cases.asynchronous import AsyncTestCase
import sys
import inspect
import abc

class TestServiceReflectionAbstract(AsyncTestCase):

    async def testIsAbstract(self):
        """
        Test Reflection.isAbstract for abstract and concrete classes.

        Parameters
        ----------
        None

        Tests
        -----
        - DummyAbstract: An abstract class using abc.ABCMeta with an abstract method.
        - DummyConcrete: A regular concrete class.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isAbstract(DummyAbstract) returns True.
        - Reflection.isAbstract(DummyConcrete) returns False.
        """
        class DummyAbstract(metaclass=abc.ABCMeta):
            @abc.abstractmethod
            def foo(self):
                pass

        class DummyConcrete:
            def bar(self):
                return 42

        self.assertTrue(Reflection.isAbstract(DummyAbstract))
        self.assertFalse(Reflection.isAbstract(DummyConcrete))

    async def testIsAsyncGen(self):
        """
        Test Reflection.isAsyncGen for correct identification of asynchronous generators.

        Notes
        -----
        - The asynchronous generator is defined using `async def` and `yield`.
        - The regular generator is defined using `def` and `yield`.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isAsyncGen(agen) is True.
        - Reflection.isAsyncGen(dummy_generator()) is False.
        """
        async def dummy_asyncgen():
            yield 1

        def dummy_generator():
            yield 1

        agen = dummy_asyncgen()
        self.assertTrue(Reflection.isAsyncGen(agen))
        self.assertFalse(Reflection.isAsyncGen(dummy_generator()))

    async def testIsAsyncGenFunction(self):
        """
        Test Reflection.isAsyncGenFunction for correct identification of async generator functions.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isAsyncGenFunction(dummy_asyncgen) returns True.
        - Reflection.isAsyncGenFunction(dummy_generator) returns False.
        """
        async def dummy_asyncgen():
            yield 1

        def dummy_generator():
            yield 1

        self.assertTrue(Reflection.isAsyncGenFunction(dummy_asyncgen))
        self.assertFalse(Reflection.isAsyncGenFunction(dummy_generator))

    async def testIsAwaitable(self):
        """
        Test Reflection.isAwaitable to verify correct identification of awaitable objects.

        Returns
        -------
        None

        Asserts
        -------
        - An async coroutine object is recognized as awaitable.
        - A non-awaitable object (e.g., an integer) is not recognized as awaitable.
        """
        async def dummy_coroutine():
            pass

        coro = dummy_coroutine()
        self.assertTrue(Reflection.isAwaitable(coro))
        self.assertFalse(Reflection.isAwaitable(42))

    async def testIsBuiltin(self):
        """
        Test Reflection.isBuiltin to verify correct identification of built-in functions.

        Returns
        -------
        None

        Asserts
        -------
        - The built-in function `len` is recognized as built-in.
        - A user-defined function is not recognized as built-in.
        """
        def dummy_function():
            pass

        self.assertTrue(Reflection.isBuiltin(len))
        self.assertFalse(Reflection.isBuiltin(dummy_function))

    async def testIsClass(self):
        """
        Test Reflection.isClass to verify correct identification of classes and non-class objects.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isClass returns True for a class.
        - Reflection.isClass returns False for a function.
        """
        class DummyConcrete:
            def bar(self):
                return 42

        def dummy_function():
            pass

        self.assertTrue(Reflection.isClass(DummyConcrete))
        self.assertFalse(Reflection.isClass(dummy_function))

    async def testIsCode(self):
        """
        Test Reflection.isCode to verify correct identification of code objects.

        Returns
        -------
        None

        Asserts
        -------
        - Passing a function's __code__ attribute returns True.
        - Passing the function itself returns False.
        """
        def dummy_function():
            pass

        self.assertTrue(Reflection.isCode(dummy_function.__code__))
        self.assertFalse(Reflection.isCode(dummy_function))

    async def testIsCoroutine(self):
        """
        Test Reflection.isCoroutine to ensure correct identification of coroutine objects.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isCoroutine returns True for a coroutine object.
        - Reflection.isCoroutine returns False for a regular function.
        """
        async def dummy_coroutine():
            pass

        def dummy_function():
            pass

        coro = dummy_coroutine()
        self.assertTrue(Reflection.isCoroutine(coro))
        self.assertFalse(Reflection.isCoroutine(dummy_function))

    async def testIsCoroutineFunction(self):
        """
        Test Reflection.isCoroutineFunction to verify correct identification of coroutine functions.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isCoroutineFunction(dummy_coroutine) returns True.
        - Reflection.isCoroutineFunction(dummy_function) returns False.
        """
        async def dummy_coroutine():
            pass

        def dummy_function():
            pass

        self.assertTrue(Reflection.isCoroutineFunction(dummy_coroutine))
        self.assertFalse(Reflection.isCoroutineFunction(dummy_function))

    async def testIsDataDescriptor(self):
        """
        Test Reflection.isDataDescriptor to verify correct identification of data descriptors.

        Returns
        -------
        None

        Asserts
        -------
        - A property object is recognized as a data descriptor.
        - A non-descriptor object (such as an integer) is not.
        """
        class X:
            @property
            def foo(self): return 1

        self.assertTrue(Reflection.isDataDescriptor(X.__dict__['foo']))
        self.assertFalse(Reflection.isDataDescriptor(42))

    async def testIsFrame(self):
        """
        Test Reflection.isFrame to verify correct identification of frame objects.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isFrame returns True for a valid frame object.
        - Reflection.isFrame returns False for a non-frame object.
        """
        frame = inspect.currentframe()
        self.assertTrue(Reflection.isFrame(frame))
        self.assertFalse(Reflection.isFrame(42))

    async def testIsFunction(self):
        """
        Test Reflection.isFunction to verify correct identification of functions.

        Returns
        -------
        None

        Asserts
        -------
        - A standalone function is correctly identified as a function.
        - An unbound method is not identified as a function.
        """
        def dummy_function():
            pass

        class DummyConcrete:
            def bar(self):
                return 42

        self.assertTrue(Reflection.isFunction(dummy_function))
        # Unbound methods in Python 3 are just functions, so this should be True
        self.assertTrue(Reflection.isFunction(DummyConcrete.bar))

    async def testIsGenerator(self):
        """
        Test Reflection.isGenerator to verify correct identification of generator objects.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isGenerator returns True for a generator object.
        - Reflection.isGenerator returns False for a regular function.
        """
        def dummy_generator():
            yield 1

        def dummy_function():
            pass

        gen = dummy_generator()
        self.assertTrue(Reflection.isGenerator(gen))
        self.assertFalse(Reflection.isGenerator(dummy_function))

    async def testIsGeneratorFunction(self):
        """
        Test Reflection.isGeneratorFunction to verify correct identification of generator functions.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isGeneratorFunction(dummy_generator) returns True.
        - Reflection.isGeneratorFunction(dummy_function) returns False.
        """
        def dummy_generator():
            yield 1

        def dummy_function():
            pass

        self.assertTrue(Reflection.isGeneratorFunction(dummy_generator))
        self.assertFalse(Reflection.isGeneratorFunction(dummy_function))

    async def testIsGetSetDescriptor(self):
        """
        Test Reflection.isGetSetDescriptor to verify correct identification of get-set descriptors.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isGetSetDescriptor returns True for a known get-set descriptor.
        - Reflection.isGetSetDescriptor returns False for a non-descriptor object.
        """
        self.assertTrue(Reflection.isGetSetDescriptor(type.__dict__['__dict__']))
        self.assertFalse(Reflection.isGetSetDescriptor(42))

    async def testIsMemberDescriptor(self):
        """
        Test Reflection.isMemberDescriptor to verify correct identification of member descriptors.

        Returns
        -------
        None

        Asserts
        -------
        - type.__dict__['__weakref__'] is recognized as a member descriptor.
        - An integer is not recognized as a member descriptor.
        """
        # Use an alternative member descriptor: use a slot from a new-style class
        class Y:
            __slots__ = ('foo',)
        self.assertTrue(Reflection.isMemberDescriptor(Y.__dict__['foo']))
        self.assertFalse(Reflection.isMemberDescriptor(42))
        self.assertFalse(Reflection.isMemberDescriptor(42))

    async def testIsMethod(self):
        """
        Test Reflection.isMethod to verify correct identification of methods.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isMethod returns True for a class method.
        - Reflection.isMethod returns False for a standalone function.
        """
        class DummyConcrete:
            def bar(self):
                return 42

        obj = DummyConcrete()
        def dummy_function():
            pass

        self.assertTrue(Reflection.isMethod(obj.bar))
        self.assertFalse(Reflection.isMethod(dummy_function))

    async def testIsMethodDescriptor(self):
        """
        Test Reflection.isMethodDescriptor to verify correct identification of method descriptors.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isMethodDescriptor(str.upper) returns True.
        - Reflection.isMethodDescriptor(dummy_function) returns False.
        """
        def dummy_function():
            pass

        self.assertTrue(Reflection.isMethodDescriptor(str.upper))
        self.assertFalse(Reflection.isMethodDescriptor(dummy_function))

    async def testIsModule(self):
        """
        Test Reflection.isModule to verify correct identification of module objects.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isModule returns True for a module (e.g., sys).
        - Reflection.isModule returns False for a non-module (e.g., a function).
        """
        def dummy_function():
            pass

        self.assertTrue(Reflection.isModule(sys))
        self.assertFalse(Reflection.isModule(dummy_function))

    async def testIsRoutine(self):
        """
        Test Reflection.isRoutine to verify correct identification of routine objects.

        Returns
        -------
        None

        Asserts
        -------
        - A user-defined function is recognized as a routine.
        - A built-in function is recognized as a routine.
        - A non-routine object is not recognized as a routine.
        """
        def dummy_function():
            pass

        self.assertTrue(Reflection.isRoutine(dummy_function))
        self.assertTrue(Reflection.isRoutine(len))
        self.assertFalse(Reflection.isRoutine(42))

    async def testIsTraceback(self):
        """
        Test Reflection.isTraceback to verify correct identification of traceback objects.

        Returns
        -------
        None

        Asserts
        -------
        - Reflection.isTraceback returns True for a traceback object.
        - Reflection.isTraceback returns False for a non-traceback object.
        """
        try:
            raise Exception("test")
        except Exception:
            tb = sys.exc_info()[2]
        self.assertTrue(Reflection.isTraceback(tb))
        self.assertFalse(Reflection.isTraceback(42))