from dataclasses import asdict, is_dataclass

class DataClass:

    def __init__(self, dataclass_cls: type):
        """
        Initialize the DataClass wrapper with a dataclass type.

        Parameters
        ----------
        dataclass_cls : type
            The class to be wrapped. Must be a dataclass type.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the provided class is not a dataclass type or is an instance.

        Notes
        -----
        This constructor validates that the input is a dataclass type (not an instance).
        If valid, it stores the class for further operations and initializes internal
        dictionaries for property management. Raises an error if the input is not a valid
        dataclass type.
        """

        # Ensure the provided class is a dataclass and not an instance
        if not (is_dataclass(dataclass_cls) and isinstance(dataclass_cls, type)):
            raise ValueError(
                f"The provided class '{getattr(dataclass_cls, '__name__', type(dataclass_cls).__name__)}' must be a dataclass type, not an instance."
            )

        # Store the dataclass type for use in other methods
        self.__cls = dataclass_cls

        # Initialize dictionaries to manage strict and extra properties
        self.__strict_properties = {}
        self.__extra_properties = {}

    def getOriginalProperties(self) -> set:
        """
        Get the set of original field names defined in the wrapped dataclass type.

        Parameters
        ----------
        None

        Returns
        -------
        set of str
            Set containing the names of all original fields defined in the dataclass type.

        Raises
        ------
        AttributeError
            If the wrapped class does not have dataclass fields.

        Notes
        -----
        This method retrieves the field names from the dataclass type stored in `self.__cls`.
        If the internal reference is an instance, its type is used to access the field definitions.
        The returned set includes only the names of fields originally declared in the dataclass,
        excluding any dynamically added attributes.
        """

        # Use the class stored in self.__cls; if it's an instance, get its type
        cls = self.__cls
        if not isinstance(cls, type):
            cls = type(cls)

        # Return the set of field names defined in the dataclass
        return set(cls.__dataclass_fields__.keys())

    def fromDict(self, props: dict) -> 'DataClass':
        """
        Populate the wrapped dataclass instance with properties from a dictionary.

        Parameters
        ----------
        props : dict
            Dictionary containing property names and values to assign to the dataclass instance.

        Returns
        -------
        DataClass
            The current instance of the DataClass wrapper, with the dataclass instance populated
            according to the provided dictionary. The internal reference (`self.__cls`) is updated
            to the new dataclass instance created with the provided properties.

        Raises
        ------
        ValueError
            If the `props` parameter is not a dictionary.

        Notes
        -----
        - Properties matching the original dataclass fields are assigned as strict properties.
        - Properties not matching the original fields are assigned as extra properties and set as attributes.
        - The method creates a new instance of the dataclass using only the strict properties, then sets extra properties as attributes.
        - The dataclass type itself is not modified; only the instance managed by this wrapper is updated.
        """

        # Ensure the input is a dictionary
        if not isinstance(props, dict):
            raise ValueError("The 'props' parameter must be a dictionary.")

        # Get the set of original field names from the dataclass
        original_fields = self.getOriginalProperties()

        # Separate strict (original) and extra properties
        for key, value in props.items():
            if key in original_fields:
                self.__strict_properties[key] = value  # Assign to strict properties
            else:
                self.__extra_properties[key] = value   # Assign to extra properties

        # Create a new instance of the dataclass with strict properties only
        instance = self.__cls(**self.__strict_properties)

        # Set extra properties as attributes on the instance
        for key, value in self.__extra_properties.items():
            instance.__setattr__(key, value)

        # Update the internal reference to the new instance
        self.__cls = instance

        # Return self to allow method chaining
        return self

    def fromDataclass(self, instance) -> 'DataClass':
        """
        Populate the wrapped dataclass instance with properties from another dataclass instance.

        Parameters
        ----------
        instance : object
            An instance of a dataclass from which properties will be extracted and assigned to the wrapped dataclass.

        Returns
        -------
        DataClass
            Returns the current instance of the DataClass wrapper after populating its internal dataclass instance
            with the properties extracted from the provided dataclass instance.

        Raises
        ------
        ValueError
            If the provided `instance` is not a dataclass.

        Notes
        -----
        This method extracts all properties from the provided dataclass instance using `asdict` if it is already
        initialized (i.e., not a class). If the input is a dataclass type, it extracts properties from its `__dict__`.
        The extracted properties are then delegated to `fromDict`, which handles property validation and assignment,
        including strict property checking if enabled.
        """

        # Ensure the provided instance is a dataclass
        if not is_dataclass(instance):
            raise ValueError("The provided instance is not a dataclass.")

        # Extract properties from the dataclass instance using asdict if it's an instance,
        # otherwise use __dict__ for class-level attributes
        if is_dataclass(instance) and not isinstance(instance, type):
            props = asdict(instance)
        else:
            props = {k: v for k, v in instance.__dict__.items() if not k.startswith("__")}

        # Delegate property assignment to fromDict, which handles validation and assignment
        return self.fromDict(props)

    def get(self) -> type:
        """
        Retrieve the dataclass type or instance currently managed by this wrapper.

        Returns
        -------
        type or object
            Returns the dataclass type if no instance has been set, or the dataclass instance if one has been created and assigned.
            The returned value reflects the current state of the wrapper: either the original dataclass type or the most recently set instance.

        Notes
        -----
        This method provides direct access to the underlying dataclass type or instance managed by the wrapper.
        It is useful for introspection, further manipulation, or integration with other components.
        The returned value is determined by the internal state of the wrapper (`self.__cls`), which may be either a class or an instance.
        """

        # Return the current dataclass type or instance managed by the wrapper
        return self.__cls

    def toDict(self) -> dict:
        """
        Convert the managed dataclass instance to a dictionary representation, including both original fields and any extra properties.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            Dictionary containing all original dataclass fields and any extra properties added to the instance.
            - If the internal reference is an instance, original fields are recursively converted using `dataclasses.asdict`.
            - Extra properties (not defined in the dataclass) are merged into the result.
            - If the internal reference is still a class (not an instance), only strict properties are returned.

        Notes
        -----
        - Original dataclass fields are obtained using `dataclasses.asdict` for instances.
        - Extra properties are those added to the instance that are not part of the original dataclass definition.
        - The returned dictionary represents the complete state of the managed dataclass instance, including dynamic attributes.
        """

        # If self.__cls is an instance, use asdict to get original (strict) properties
        if not isinstance(self.__cls, type):
            result = asdict(self.__cls)
        else:
            # If it's still a class, just return the strict properties dictionary
            result = dict(self.__strict_properties)

        # Merge extra properties (not defined in the dataclass) into the result
        result.update(self.__extra_properties)

        # Return the combined dictionary
        return result