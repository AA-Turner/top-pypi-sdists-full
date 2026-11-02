

class PhoneNumber(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v.startswith("+"):
            return v[1:]
        return v
    
    
