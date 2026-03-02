from pydantic import BaseModel

class AutonomousSystem(BaseModel):
    """
    An autonomous system (AS) is a collection of connected Internet Protocol (IP)
    routing prefixes under the control of one or more network operators on behalf of
    a single administrative entity or domain that presents a common, clearly defined
    routing policy to the internet.
    """

    # Recommended:
    number: int | None = None # Unique number that the AS is identified by.
    name: str | None = None # Organization name for the Autonomous System.
