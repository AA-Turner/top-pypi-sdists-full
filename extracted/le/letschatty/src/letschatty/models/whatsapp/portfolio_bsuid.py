from pydantic import BaseModel, ConfigDict


class PortfolioBsuid(BaseModel):
    """A person's BSUID in one business portfolio. Meta gives the same person a different
    BSUID in each portfolio, and a number can only message the BSUID of its own portfolio."""
    portfolio_id: str
    bsuid: str

    model_config = ConfigDict(frozen=True)
