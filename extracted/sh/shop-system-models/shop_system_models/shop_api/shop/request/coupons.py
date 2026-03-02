import datetime
from typing import Annotated

from annotated_types import Ge, Le
from pydantic import BaseModel, StringConstraints, model_validator


class SubmitCouponModel(BaseModel):
    exp_date: datetime.datetime | None = None
    amount: Annotated[float, Ge(0)] | None = None
    discount: Annotated[float, Ge(0), Le(100)] | None = None
    available_qty: Annotated[int, Ge(0)]
    code: Annotated[str, StringConstraints(min_length=1, max_length=10)]

    @model_validator(mode="after")
    def amount_xor_discount_validator(self):
        if self.amount is None and self.discount is None:
            raise ValueError("amount or discount must be specified")

        if self.amount is not None and self.discount is not None:
            raise ValueError("only one of amount and discount must be specified")

        return self


class CouponModel(SubmitCouponModel):
    def get_discount_amount(self, basket_amount: float) -> float:
        """
        Calculate the discount amount.

        It is guaranteed that the discount amount will be less than basket amount,
        i.e. final basket amount won't go below zero.
        """

        if self.amount is not None:
            discount_amount = self.amount
        else:
            assert self.discount is not None, "amount and discount are both None"  # for mypy

            # Round down discount_amount with precision of 2 digits after point
            discount_amount = int(self.discount * basket_amount) / 100

        return min(discount_amount, basket_amount - 1)
