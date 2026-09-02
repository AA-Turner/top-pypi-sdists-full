from pydantic import BaseModel


class Rows(BaseModel):
    """Describes the rows response from DealCloud"""

    totalRecords: int
    rows: list
