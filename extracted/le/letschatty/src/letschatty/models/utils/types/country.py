from pycountry import countries

class Country(str):
    """
    A custom type representing a valid country name.
    
    This type ensures that the value is a string and corresponds to a valid
    country name as defined in the pycountry library.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if countries.get(name=v) is None:
            raise ValueError(f"Invalid country name: {v}")
        return v