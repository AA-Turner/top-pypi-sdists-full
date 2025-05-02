from pydantic import BaseModel


class BaseRequest(BaseModel):
    """Base class for API requests."""

    @classmethod
    def example(cls):
        field_values = {}
        for name, field in cls.model_fields.items():
            if field.examples is not None and len(field.examples) > 0:
                field_values[name] = field.examples[0]
            else:
                field_values[name] = field.default
        return cls(**field_values)
