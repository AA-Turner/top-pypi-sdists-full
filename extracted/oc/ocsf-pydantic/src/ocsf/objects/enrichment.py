from pydantic import BaseModel

class Enrichment(BaseModel):
    """
    The Enrichment object provides inline enrichment data for specific attributes of
    interest within an event. It serves as a mechanism to enhance or supplement the
    information associated with the event by adding additional relevant details or
    context.
    """

    data: dict # The enrichment data associated with the attribute and value. The meaning
               # of this data depends on the type the enrichment record.
    name: str # The name of the attribute to which the enriched data pertains.
    value: str # The value of the attribute to which the enriched data pertains.

    # Recommended:
    provider: str | None = None # The enrichment data provider name.
    type: str | None = None # The enrichment type. For example: `location`.
