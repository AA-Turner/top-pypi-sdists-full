from pydantic import field_validator

from shop_system_models.shop_api.shop.request.payment_methods import PaymentMethodModel


class PaymentMethodDBResponseModel(PaymentMethodModel):
    id: str


class PaymentMethodResponseModel(PaymentMethodDBResponseModel):
    @field_validator("payment_data", mode="before")
    def back_zeros(cls, value):
        return "********"
