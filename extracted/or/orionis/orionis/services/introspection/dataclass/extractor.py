class DataclassInspector:

    def __call__(self, dataclass_type: type) -> dict:
        """
        Extract attributes and their values from a given dataclass type.

        This method retrieves all attributes defined in the provided dataclass type,
        excluding special attributes (those whose names start with '__'). It returns
        a dictionary where the keys are the attribute names and the values are the
        corresponding attribute values.

        Parameters
        ----------
        dataclass_type : type
            The dataclass type from which to extract attributes. This must be a valid
            Python class type.

        Returns
        -------
        dict
            A dictionary where:
            - Keys are the names of the attributes defined in the dataclass type.
            - Values are the corresponding attribute values.
            Special attributes (those starting with '__') are excluded.

        Raises
        ------
        TypeError
            If the provided argument is not a valid Python class type.
        """

        # Ensure the input is a valid class type
        if isinstance(dataclass_type, type):

            # Extract attributes and their values, excluding special attributes
            values = {k: v for k, v in dataclass_type.__dict__.items() if not k.startswith("__")}

            # Return the extracted attributes and their values
            return values

        # Raise an error if the input is not a valid class type
        raise TypeError("The provided argument is not a valid dataclass type.")

# Instantiate the DataclassValues callable
extractor = DataclassInspector()