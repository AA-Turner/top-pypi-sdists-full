import inspect
from typing import Any

class Type:

    def __init__(self, target: Any):
        """
        Initialize an inspection instance.

        Parameters
        ----------
        target : Any
            The object to be inspected.
        """
        self.__target = target

    def isAbstract(self) -> bool:
        """
        Check if the object is an abstract base class.

        Returns
        -------
        bool
            True if the object is abstract, False otherwise.
        """
        return inspect.isabstract(self.__target)

    def isAsyncGen(self) -> bool:
        """
        Check if the object is an asynchronous generator.

        Returns
        -------
        bool
            True if the object is an async generator, False otherwise.
        """
        return inspect.isasyncgen(self.__target)

    def isAsyncGenFunction(self) -> bool:
        """
        Check if the object is an asynchronous generator function.

        Returns
        -------
        bool
            True if the object is an async generator function, False otherwise.
        """
        return inspect.isasyncgenfunction(self.__target)

    def isAwaitable(self) -> bool:
        """
        Check if the object can be awaited.

        Returns
        -------
        bool
            True if the object is awaitable, False otherwise.
        """
        return inspect.isawaitable(self.__target)

    def isBuiltin(self) -> bool:
        """
        Check if the object is a built-in function or method.

        Returns
        -------
        bool
            True if the object is a built-in, False otherwise.
        """
        return inspect.isbuiltin(self.__target)

    def isClass(self) -> bool:
        """
        Check if the object is a class.

        Returns
        -------
        bool
            True if the object is a class, False otherwise.
        """
        return inspect.isclass(self.__target)

    def isCode(self) -> bool:
        """
        Check if the object is a code object.

        Returns
        -------
        bool
            True if the object is a code object, False otherwise.
        """
        return inspect.iscode(self.__target)

    def isCoroutine(self) -> bool:
        """
        Check if the object is a coroutine.

        Returns
        -------
        bool
            True if the object is a coroutine, False otherwise.
        """
        return inspect.iscoroutine(self.__target)

    def isCoroutineFunction(self) -> bool:
        """
        Check if the object is a coroutine function.

        Returns
        -------
        bool
            True if the object is a coroutine function, False otherwise.
        """
        return inspect.iscoroutinefunction(self.__target)

    def isDataDescriptor(self) -> bool:
        """
        Check if the object is a data descriptor.

        Returns
        -------
        bool
            True if the object is a data descriptor, False otherwise.
        """
        return inspect.isdatadescriptor(self.__target)

    def isFrame(self) -> bool:
        """
        Check if the object is a frame object.

        Returns
        -------
        bool
            True if the object is a frame object, False otherwise.
        """
        return inspect.isframe(self.__target)

    def isFunction(self) -> bool:
        """
        Check if the object is a Python function.

        Returns
        -------
        bool
            True if the object is a function, False otherwise.
        """
        return inspect.isfunction(self.__target)

    def isGenerator(self) -> bool:
        """
        Check if the object is a generator.

        Returns
        -------
        bool
            True if the object is a generator, False otherwise.
        """
        return inspect.isgenerator(self.__target)

    def isGeneratorFunction(self) -> bool:
        """
        Check if the object is a generator function.

        Returns
        -------
        bool
            True if the object is a generator function, False otherwise.
        """
        return inspect.isgeneratorfunction(self.__target)

    def isGetSetDescriptor(self) -> bool:
        """
        Check if the object is a getset descriptor.

        Returns
        -------
        bool
            True if the object is a getset descriptor, False otherwise.
        """
        return inspect.isgetsetdescriptor(self.__target)

    def isMemberDescriptor(self) -> bool:
        """
        Check if the object is a member descriptor.

        Returns
        -------
        bool
            True if the object is a member descriptor, False otherwise.
        """
        return inspect.ismemberdescriptor(self.__target)

    def isMethod(self) -> bool:
        """
        Check if the object is a method.

        Returns
        -------
        bool
            True if the object is a method, False otherwise.
        """
        return inspect.ismethod(self.__target)

    def isMethodDescriptor(self) -> bool:
        """
        Check if the object is a method descriptor.

        Returns
        -------
        bool
            True if the object is a method descriptor, False otherwise.
        """
        return inspect.ismethoddescriptor(self.__target)

    def isModule(self) -> bool:
        """
        Check if the object is a module.

        Returns
        -------
        bool
            True if the object is a module, False otherwise.
        """
        return inspect.ismodule(self.__target)

    def isRoutine(self) -> bool:
        """
        Check if the object is a user-defined or built-in function or method.

        Returns
        -------
        bool
            True if the object is a routine, False otherwise.
        """
        return inspect.isroutine(self.__target)

    def isTraceback(self) -> bool:
        """
        Check if the object is a traceback object.

        Returns
        -------
        bool
            True if the object is a traceback object, False otherwise.
        """
        return inspect.istraceback(self.__target)
