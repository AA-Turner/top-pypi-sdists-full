from pydantic import BaseModel

from shop_system_models.consts.enums import PaymentTypes


class Metadata(BaseModel):
    key: str
    value: list[str]


class PaymentMethodModel(BaseModel):
    name: str
    type: PaymentTypes
    payment_data: str | None = None  # payment_token, TON address etc....
    meta: list[Metadata] | None = []

    class Config:
        use_enum_values = True
