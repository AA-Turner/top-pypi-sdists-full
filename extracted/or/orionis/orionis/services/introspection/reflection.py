from typing import Any, Type
from orionis.services.introspection.abstract.reflection import ReflectionAbstract
from orionis.services.introspection.callables.reflection import ReflectionCallable
from orionis.services.introspection.concretes.reflection import ReflectionConcrete
from orionis.services.introspection.objects.types import Type
from orionis.services.introspection.instances.reflection import ReflectionInstance
from orionis.services.introspection.modules.reflection import ReflectionModule

class Reflection:
    """
    Provides static methods to create reflection objects for various Python constructs.

    This class offers factory methods to obtain specialized reflection objects for instances,
    abstract classes, concrete classes, and modules. Each method returns an object that
    encapsulates the target and provides introspection capabilities.
    """

    @staticmethod
    def instance(instance: Any) -> 'ReflectionInstance':
        """
        Create a ReflectionInstance for the given object instance.

        Parameters
        ----------
        instance : Any
            The object instance to reflect.

        Returns
        -------
        ReflectionInstance
            A reflection object for the given instance.
        """
        return ReflectionInstance(instance)

    @staticmethod
    def abstract(abstract: Type) -> 'ReflectionAbstract':
        """
        Create a ReflectionAbstract for the given abstract class.

        Parameters
        ----------
        abstract : Type
            The abstract class to reflect.

        Returns
        -------
        ReflectionAbstract
            A reflection object for the given abstract class.
        """
        return ReflectionAbstract(abstract)

    @staticmethod
    def concrete(concrete: Type) -> 'ReflectionConcrete':
        """
        Create a ReflectionConcrete for the given concrete class.

        Parameters
        ----------
        concrete : Type
            The concrete class to reflect.

        Returns
        -------
        ReflectionConcrete
            A reflection object for the given concrete class.
        """
        return ReflectionConcrete(concrete)

    @staticmethod
    def module(module: str) -> 'ReflectionModule':
        """
        Create a ReflectionModule for the given module name.

        Parameters
        ----------
        module : str
            The name of the module to reflect.

        Returns
        -------
        ReflectionModule
            A reflection object for the given module.
        """
        return ReflectionModule(module)

    @staticmethod
    def callable(fn: callable) -> 'ReflectionCallable':
        """
        Create a ReflectionCallable instance for the given callable function.

        Parameters
        ----------
        fn : callable
            The function or method to wrap in a ReflectionCallable.

        Returns
        -------
        ReflectionCallable
            A reflection object that encapsulates the provided callable.
        """
        return ReflectionCallable(fn)

    @staticmethod
    def isAbstract(obj: Any) -> bool:
        """
        Check if the object is an abstract base class.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is abstract, False otherwise.
        """
        return Type(obj).isAbstract()

    @staticmethod
    def isAsyncGen(obj: Any) -> bool:
        """
        Check if the object is an asynchronous generator.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is an async generator, False otherwise.
        """
        return Type(obj).isAsyncGen()

    @staticmethod
    def isAsyncGenFunction(obj: Any) -> bool:
        """
        Check if the object is an asynchronous generator function.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is an async generator function, False otherwise.
        """
        return Type(obj).isAsyncGenFunction()

    @staticmethod
    def isAwaitable(obj: Any) -> bool:
        """
        Check if the object can be awaited.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is awaitable, False otherwise.
        """
        return Type(obj).isAwaitable()

    @staticmethod
    def isBuiltin(obj: Any) -> bool:
        """
        Check if the object is a built-in function or method.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a built-in, False otherwise.
        """
        return Type(obj).isBuiltin()

    @staticmethod
    def isClass(obj: Any) -> bool:
        """
        Check if the object is a class.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a class, False otherwise.
        """
        return Type(obj).isClass()

    @staticmethod
    def isCode(obj: Any) -> bool:
        """
        Check if the object is a code object.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a code object, False otherwise.
        """
        return Type(obj).isCode()

    @staticmethod
    def isCoroutine(obj: Any) -> bool:
        """
        Check if the object is a coroutine.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a coroutine, False otherwise.
        """
        return Type(obj).isCoroutine()

    @staticmethod
    def isCoroutineFunction(obj: Any) -> bool:
        """
        Check if the object is a coroutine function.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a coroutine function, False otherwise.
        """
        return Type(obj).isCoroutineFunction()

    @staticmethod
    def isDataDescriptor(obj: Any) -> bool:
        """
        Check if the object is a data descriptor.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a data descriptor, False otherwise.
        """
        return Type(obj).isDataDescriptor()

    @staticmethod
    def isFrame(obj: Any) -> bool:
        """
        Check if the object is a frame object.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a frame object, False otherwise.
        """
        return Type(obj).isFrame()

    @staticmethod
    def isFunction(obj: Any) -> bool:
        """
        Check if the object is a Python function.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a function, False otherwise.
        """
        return Type(obj).isFunction()

    @staticmethod
    def isGenerator(obj: Any) -> bool:
        """
        Check if the object is a generator.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a generator, False otherwise.
        """
        return Type(obj).isGenerator()

    @staticmethod
    def isGeneratorFunction(obj: Any) -> bool:
        """
        Check if the object is a generator function.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a generator function, False otherwise.
        """
        return Type(obj).isGeneratorFunction()

    @staticmethod
    def isGetSetDescriptor(obj: Any) -> bool:
        """
        Check if the object is a getset descriptor.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a getset descriptor, False otherwise.
        """
        return Type(obj).isGetSetDescriptor()

    @staticmethod
    def isMemberDescriptor(obj: Any) -> bool:
        """
        Check if the object is a member descriptor.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a member descriptor, False otherwise.
        """
        return Type(obj).isMemberDescriptor()

    @staticmethod
    def isMethod(obj: Any) -> bool:
        """
        Check if the object is a method.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a method, False otherwise.
        """
        return Type(obj).isMethod()

    @staticmethod
    def isMethodDescriptor(obj: Any) -> bool:
        """
        Check if the object is a method descriptor.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a method descriptor, False otherwise.
        """
        return Type(obj).isMethodDescriptor()

    @staticmethod
    def isModule(obj: Any) -> bool:
        """
        Check if the object is a module.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a module, False otherwise.
        """
        return Type(obj).isModule()

    @staticmethod
    def isRoutine(obj: Any) -> bool:
        """
        Check if the object is a user-defined or built-in function or method.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a routine, False otherwise.
        """
        return Type(obj).isRoutine()

    @staticmethod
    def isTraceback(obj: Any) -> bool:
        """
        Check if the object is a traceback object.

        Parameters
        ----------
        obj : Any
            The object to check.

        Returns
        -------
        bool
            True if the object is a traceback object, False otherwise.
        """
        return Type(obj).isTraceback()
