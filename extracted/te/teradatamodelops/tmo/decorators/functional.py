import inspect
import logging

from typing import Optional, Literal, Any, Union

logger = logging.getLogger(__name__)


class functional(object):  # noqa @ NOSONAR
    """
    A class decorator that converts class attributes to properties with getter and setter methods following the functional programming paradigm.
    It also adds class-level getter, setter, and deleter methods to manage multiple attributes at once.

    Example:
        @functional
        class Point:
            x = 0
            y = 0

        # Create instance
        p = Point(1, 2)
        print(p.x)  # 1
        print(p.y)  # 2

        # Use functional getters and setters
        p.set_x(10)
        print(p.get_x())  # 10

        # Get all attributes as a dict
        print(p.get("dict"))  # {'x': 10, 'y': 2}

        # Change several attributes at once
        p.set(x=5, y=7)
        print(p.get())  # [5, 7]

        # Delete attributes
        p.del(["x"])
        # print(p.x)  # AttributeError

    Usage:
        - Decorate a class with @functional to enable functional access to its attributes.
        - Use get_<attr>(), set_<attr>(), del_<attr>() methods to manipulate individual attributes.
        - Use get(), set(), del() methods to manipulate multiple attributes.
    """

    _cls = None
    _instance_obj = None
    _init_args = []
    _final_args = {}

    def __init__(self, *args, **kwargs) -> None:
        self._has_init = True if args[0].__init__ is not object.__init__ else False
        self._init_args = [
            x for x in inspect.getfullargspec(args[0].__init__).args if x != "self"
        ]
        if (
            len(args) == 0
            or len(kwargs) > 0
            or ((len(args) > 0) and not inspect.isclass(args[0]))
        ):
            raise TypeError(
                f"@{self.__class__.__name__} decorator can only be used to decorate"
                " classes and does not take any arguments."
            )

        self._cls = args[0]

    def __call__(self, *args, **kwargs):
        if len(args) > 0 and len(kwargs) > 0:
            raise TypeError(
                f"@{self.__class__.__name__} {self._cls.__name__} can only take either"
                " positional or keyword arguments, not both."
            )

        if (
            self._has_init is False
            and len(kwargs) == 0
            and len(args) > len(self._get_cls_attrs(self._cls))
        ):
            raise TypeError(
                f"@{self.__class__.__name__} {self._cls.__name__} takes at most"
                f" {len(self._get_cls_attrs(self._cls))} positional arguments but"
                f" {len(args)} were given."
            )

        self._args = args
        self._kwargs = kwargs
        self._final_args = dict(zip(self._init_args, self._args))

        if len(args) > 0 and len(self._init_args) > 0:
            self._instance_obj = self._cls(*args)
        elif len(kwargs) > 0 and self._has_init is True:
            self._instance_obj = self._cls(**kwargs)
        else:
            self._instance_obj = self._cls()

        return self._process_class()

    def _process_class(self) -> object:
        """Processes the class and adds properties and getter/setter methods for each attribute, then initializes the attributes values depending on the default values and the values passed in the builder."""
        attr_index = 0
        for attr, value in self._get_cls_attrs(self._cls).items():
            self._instance_obj = self._add_properties(self._instance_obj, attr, value)
            self._instance_obj = self._value_initializer(
                self._instance_obj, attr, value, attr_index
            )
            attr_index += 1

        return self._functional_cls_getter_setter(self._instance_obj)

    def _add_properties(self, cls=None, name=None, attr=None) -> object:
        """Adds a private property to the class for the specified attribute name and also adds getter, setter, and deleter methods."""
        setattr(cls, f"_{name}", attr)  # store the actual value in a private attribute
        prop = property(
            fget=lambda selfie: getattr(cls, f"_{name}"),
            fset=lambda selfie, value: setattr(cls, f"_{name}", value),
            fdel=lambda selfie: delattr(cls, f"_{name}"),
            doc=f"Property for {name}",
        )
        setattr(cls, name, prop)

        return self._functional_attr_getter_setter(cls, name)

    def _functional_attr_getter_setter(self, cls: object, name: str) -> object:
        """Adds getter, setter, and deleter methods to the class for the specified attribute name."""
        self._add_attr_getter(cls, name)
        self._add_attr_setter(cls, name)
        self._add_attr_deleter(cls, name)
        return cls

    def _functional_cls_getter_setter(self, cls: object) -> object:
        """Adds class-level getter, setter, and deleter methods to the class."""
        self._add_cls_getter(cls)
        self._add_cls_setter(cls)
        self._add_cls_deleter(cls)
        return cls

    def _value_initializer(
        self, cls: object, name: str, attr: Any, index: int = 0
    ) -> object:
        """Initializes the attribute value based on the provided positional or keyword arguments."""
        if len(self._final_args) > 0:
            if name in self._final_args.keys():
                setattr(cls, name, self._final_args[name])
            else:
                setattr(cls, name, attr)
        elif len(self._args) > 0:
            if index < len(self._args):
                setattr(cls, name, self._args[index])
            else:
                setattr(cls, name, attr)
        elif len(self._kwargs) > 0 and name in self._kwargs:
            setattr(cls, name, self._kwargs[name])
        else:
            setattr(cls, name, attr)
        return cls

    @staticmethod
    def _add_attr_getter(cls: object, name: str) -> object:
        """Adds a getter method to the class for the specified attribute name."""

        def wrapper():
            return getattr(cls, name)

        setattr(cls, f"get_{name}", wrapper)
        setattr(
            getattr(cls, f"get_{name}"),
            "__doc__",
            f"""Functional getter for {cls.__class__.__name__}.{name}""",
        )
        return wrapper

    @staticmethod
    def _add_attr_setter(cls: object, name: str) -> object:
        """Adds a setter method to the class for the specified attribute name."""

        def wrapper(value):
            setattr(cls, name, value)
            return cls

        setattr(cls, f"set_{name}", wrapper)
        setattr(
            getattr(cls, f"set_{name}"),
            "__doc__",
            f"""Functional setter for {cls.__class__.__name__}.{name}""",
        )
        return wrapper

    @staticmethod
    def _add_attr_deleter(cls: object, name: str) -> object:
        """Adds a deleter method to the class for the specified attribute name."""

        def wrapper():
            delattr(cls, name)
            return cls

        setattr(cls, f"del_{name}", wrapper)
        setattr(
            getattr(cls, f"del_{name}"),
            "__doc__",
            f"""Functional deleter for {cls.__class__.__name__}.{name}""",
        )
        setattr(cls, f"delete_{name}", wrapper)
        setattr(
            getattr(cls, f"delete_{name}"),
            "__doc__",
            f"""Functional deleter for {cls.__class__.__name__}.{name}""",
        )
        return wrapper

    @staticmethod
    def _add_cls_getter(cls: object) -> object:
        """Adds an attributes getter method to the class. Takes a list of attribute names to get and an output type (dict or list)."""

        def wrapper(
            attributes: Optional[
                Union[list[str], Literal["dict", "list", "all"]]
            ] = None,
            output: Literal["dict", "list"] = "list",
        ):
            if attributes in ["dict", "list"]:
                output = attributes
                attributes = None
            if attributes is None or len(attributes) == 0 or attributes == "all":
                attributes = [
                    attr for attr, val in functional._get_cls_attrs(cls).items()
                ]
            if output == "dict":
                return {attr: getattr(cls, attr) for attr in attributes}
            elif output == "list":
                return [getattr(cls, attr) for attr in attributes]
            else:
                raise ValueError("Output type must be either 'dict' or 'list'")

        setattr(cls, "get", wrapper)
        setattr(
            getattr(cls, "get"),
            "__doc__",
            f"""Functional getter for {cls.__class__.__name__}""",
        )
        return wrapper

    @staticmethod
    def _add_cls_setter(cls: object) -> object:
        """Adds an attributes setter method to the class. Takes either a list of positional arguments or keyword arguments to set the attributes."""

        def wrapper(*args, **kwargs):
            if len(args) > 0 and len(kwargs) > 0:
                raise TypeError(
                    "set() can only take either positional or keyword arguments, not"
                    " both."
                )
            if len(args) > 0:
                attributes = [
                    attr for attr, name in functional._get_cls_attrs(cls).items()
                ]
                if len(args) > len(attributes):
                    raise ValueError(
                        "Number of arguments exceeds number of attributes in the class."
                    )
                for i, value in enumerate(args):
                    setattr(cls, attributes[i], value)
            elif len(kwargs) > 0:
                functional._add_csl_setter_kwargs(cls, kwargs)
            return cls

        setattr(cls, "set", wrapper)
        setattr(
            getattr(cls, "set"),
            "__doc__",
            f"""Functional getter for {cls.__class__.__name__}""",
        )
        return wrapper

    @staticmethod
    def _add_csl_setter_kwargs(cls: object, kwargs) -> object:
        for key, value in kwargs.items():
            if key not in functional._get_cls_attrs(cls).keys():
                raise AttributeError(
                    f"Attribute {key} not found in class {cls.__class__.__name__}"
                )
            setattr(cls, key, value)

    @staticmethod
    def _add_cls_deleter(cls: object) -> object:
        """Adds an attributes deleter method to the class. Takes a list of attribute names to delete."""

        def wrapper(
            attributes: Optional[Union[list[str], Literal["all"]]] = None,
        ) -> object:
            if attributes is None or len(attributes) == 0:
                raise ValueError("Attributes list cannot be None or empty")
            cls_attrs = [attr for attr, val in functional._get_cls_attrs(cls).items()]
            if attributes == "all":
                attributes = cls_attrs
            for attr in attributes:
                if attr not in cls_attrs:
                    raise ValueError(
                        f"Attribute {attr} not found in class {cls.__class__.__name__}"
                    )
                delattr(cls, attr)
                delattr(cls, f"_{attr}")
            return cls

        setattr(cls, "del", wrapper)
        setattr(
            getattr(cls, "del"),
            "__doc__",
            f"""Functional deleter for {cls.__class__.__name__}""",
        )
        setattr(cls, "delete", wrapper)
        setattr(
            getattr(cls, "delete"),
            "__doc__",
            f"""Functional deleter for {cls.__class__.__name__}""",
        )
        return wrapper

    @staticmethod
    def _get_cls_attrs(cls: object) -> dict:
        """Returns a dictionary of class attributes excluding dunder and sunder methods, callable and private attributes or methods, and 'self'."""
        return {
            name: attr
            for name, attr in cls.__dict__.items()
            if not (
                (name.startswith("__") and name.endswith("__")) or name.startswith("_")
            )
            and not callable(attr)
            and attr != "self"
        }
