"""SQLModel interface."""

from pptx.util import Length
from sqlalchemy.types import TypeDecorator, Float


class LengthAsFloat(TypeDecorator):
    impl = Float

    def process_bind_param(self, value, dialect):
        """Convert Python object to number for storing in database."""
        if value is None:
            return value
        return float(value)

    def process_result_value(self, value, dialect):
        """Convert the integer from the database back into a Length."""
        if value is None:
            return None
        return Length(value)
