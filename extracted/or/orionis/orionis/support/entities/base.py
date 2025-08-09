from dataclasses import asdict, fields, is_dataclass, MISSING
from enum import Enum

class BaseEntity:

    def __post_init__(self):
        """
        Called automatically after the dataclass instance is initialized.

        This method is intended to be overridden by subclasses to perform additional
        initialization or validation after all fields have been set.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass

    def toDict(self) -> dict:
        """
        Convert the dataclass instance to a dictionary.

        Returns
        -------
        dict
            Dictionary representation of the dataclass instance, including nested dataclasses.
        """
        return asdict(self)

    def getFields(self):
        """
        Get detailed information about each field in the dataclass instance.

        Returns
        -------
        list of dict
            A list where each element is a dictionary containing:
            - name : str
                The name of the field.
            - types : list of str
                The type(s) of the field as a list of type names.
            - default : Any
                The default value of the field, resolved from the field definition, default factory, or metadata.
            - metadata : dict
                The metadata associated with the field.

        Notes
        -----
        Handles complex field types, including unions and generics, by representing them as lists of type names.
        Resolves default values from direct assignment, default factories, or metadata, and normalizes dataclass and Enum values.
        Metadata defaults are normalized if present and callable or dataclass/Enum types.
        """

        # List to hold field information dictionaries
        __fields = []

        # Iterate over all fields defined in the dataclass
        for field in fields(self):

            # Extract the field name
            __name = field.name

            # Attempt to get the type name; handles simple types
            __type = getattr(field.type, '__name__', None)

            # If type name is not available, handle complex types (e.g., Unions)
            if __type is None:
                type_lst = []
                type_str = str(field.type).split('|')
                for itype in type_str:
                    type_lst.append(itype.strip())
                __type = type_lst

            # Ensure __type is always a list for consistency
            __type = type_lst if isinstance(__type, list) else [__type]

            # Extract metadata as a dictionary
            metadata = dict(field.metadata) if field.metadata else {}

            # Normalize default value in metadata if present
            if 'default' in metadata:
                metadata_default = metadata['default']
                if callable(metadata_default):
                    metadata_default = metadata_default()
                if is_dataclass(metadata_default):
                    metadata_default = asdict(metadata_default)
                elif isinstance(metadata_default, Enum):
                    metadata_default = metadata_default.value
                metadata['default'] = metadata_default

            __metadata = metadata

            # Initialize default value
            __default = None

            # Resolve default value from field definition
            if field.default is not MISSING:
                __default = field.default() if callable(field.default) else field.default
                if is_dataclass(__default):
                    __default = asdict(__default)
                elif isinstance(__default, Enum):
                    __default = __default.value

            # Resolve default value from default factory if present
            elif field.default_factory is not MISSING:
                __default = field.default_factory() if callable(field.default_factory) else field.default_factory
                if is_dataclass(__default):
                    __default = asdict(__default)
                elif isinstance(__default, Enum):
                    __default = __default.value

            # If no default found, check metadata for custom default
            else:
                __default = __metadata.get('default', None)

            # Append the field information dictionary to the list
            __fields.append({
                "name": __name,
                "types": __type,
                "default": __default,
                "metadata": __metadata
            })

        # Return the list of field information dictionaries
        return __fields