from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentMethod(_message.Message):
    __slots__ = ("id", "brand", "last4", "exp_month", "exp_year", "is_default")
    ID_FIELD_NUMBER: _ClassVar[int]
    BRAND_FIELD_NUMBER: _ClassVar[int]
    LAST4_FIELD_NUMBER: _ClassVar[int]
    EXP_MONTH_FIELD_NUMBER: _ClassVar[int]
    EXP_YEAR_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    id: str
    brand: str
    last4: str
    exp_month: int
    exp_year: int
    is_default: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        brand: _Optional[str] = ...,
        last4: _Optional[str] = ...,
        exp_month: _Optional[int] = ...,
        exp_year: _Optional[int] = ...,
        is_default: bool = ...,
    ) -> None: ...

class StripeInvoice(_message.Message):
    __slots__ = (
        "id",
        "number",
        "amount_cents",
        "status",
        "created_at",
        "paid_at",
        "hosted_invoice_url",
        "pdf_url",
        "description",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_CENTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    PAID_AT_FIELD_NUMBER: _ClassVar[int]
    HOSTED_INVOICE_URL_FIELD_NUMBER: _ClassVar[int]
    PDF_URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    number: str
    amount_cents: int
    status: str
    created_at: _timestamp_pb2.Timestamp
    paid_at: _timestamp_pb2.Timestamp
    hosted_invoice_url: str
    pdf_url: str
    description: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        number: _Optional[str] = ...,
        amount_cents: _Optional[int] = ...,
        status: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        paid_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        hosted_invoice_url: _Optional[str] = ...,
        pdf_url: _Optional[str] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class CreditBalance(_message.Message):
    __slots__ = ("available_credits", "credit_price_cents")
    AVAILABLE_CREDITS_FIELD_NUMBER: _ClassVar[int]
    CREDIT_PRICE_CENTS_FIELD_NUMBER: _ClassVar[int]
    available_credits: int
    credit_price_cents: int
    def __init__(self, available_credits: _Optional[int] = ..., credit_price_cents: _Optional[int] = ...) -> None: ...

class AutoRechargeConfig(_message.Message):
    __slots__ = ("enabled", "threshold_credits", "recharge_to_credits")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_CREDITS_FIELD_NUMBER: _ClassVar[int]
    RECHARGE_TO_CREDITS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    threshold_credits: int
    recharge_to_credits: int
    def __init__(
        self, enabled: bool = ..., threshold_credits: _Optional[int] = ..., recharge_to_credits: _Optional[int] = ...
    ) -> None: ...

class SpendLimit(_message.Message):
    __slots__ = ("monthly_limit_credits", "current_month_usage_credits")
    MONTHLY_LIMIT_CREDITS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MONTH_USAGE_CREDITS_FIELD_NUMBER: _ClassVar[int]
    monthly_limit_credits: int
    current_month_usage_credits: int
    def __init__(
        self, monthly_limit_credits: _Optional[int] = ..., current_month_usage_credits: _Optional[int] = ...
    ) -> None: ...

class BillingPreferences(_message.Message):
    __slots__ = (
        "billing_email",
        "company_name",
        "company_address_line1",
        "company_address_line2",
        "company_city",
        "company_state",
        "company_postal_code",
        "company_country",
    )
    BILLING_EMAIL_FIELD_NUMBER: _ClassVar[int]
    COMPANY_NAME_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ADDRESS_LINE1_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ADDRESS_LINE2_FIELD_NUMBER: _ClassVar[int]
    COMPANY_CITY_FIELD_NUMBER: _ClassVar[int]
    COMPANY_STATE_FIELD_NUMBER: _ClassVar[int]
    COMPANY_POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COMPANY_COUNTRY_FIELD_NUMBER: _ClassVar[int]
    billing_email: str
    company_name: str
    company_address_line1: str
    company_address_line2: str
    company_city: str
    company_state: str
    company_postal_code: str
    company_country: str
    def __init__(
        self,
        billing_email: _Optional[str] = ...,
        company_name: _Optional[str] = ...,
        company_address_line1: _Optional[str] = ...,
        company_address_line2: _Optional[str] = ...,
        company_city: _Optional[str] = ...,
        company_state: _Optional[str] = ...,
        company_postal_code: _Optional[str] = ...,
        company_country: _Optional[str] = ...,
    ) -> None: ...

class GetBillingOverviewRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingOverviewResponse(_message.Message):
    __slots__ = ("credit_balance", "auto_recharge", "spend_limit", "has_payment_method", "subscription_plan_id")
    CREDIT_BALANCE_FIELD_NUMBER: _ClassVar[int]
    AUTO_RECHARGE_FIELD_NUMBER: _ClassVar[int]
    SPEND_LIMIT_FIELD_NUMBER: _ClassVar[int]
    HAS_PAYMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    credit_balance: CreditBalance
    auto_recharge: AutoRechargeConfig
    spend_limit: SpendLimit
    has_payment_method: bool
    subscription_plan_id: str
    def __init__(
        self,
        credit_balance: _Optional[_Union[CreditBalance, _Mapping]] = ...,
        auto_recharge: _Optional[_Union[AutoRechargeConfig, _Mapping]] = ...,
        spend_limit: _Optional[_Union[SpendLimit, _Mapping]] = ...,
        has_payment_method: bool = ...,
        subscription_plan_id: _Optional[str] = ...,
    ) -> None: ...

class GetPaymentMethodsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetPaymentMethodsResponse(_message.Message):
    __slots__ = ("payment_methods",)
    PAYMENT_METHODS_FIELD_NUMBER: _ClassVar[int]
    payment_methods: _containers.RepeatedCompositeFieldContainer[PaymentMethod]
    def __init__(self, payment_methods: _Optional[_Iterable[_Union[PaymentMethod, _Mapping]]] = ...) -> None: ...

class CreateSetupIntentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateSetupIntentResponse(_message.Message):
    __slots__ = ("client_secret",)
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_secret: str
    def __init__(self, client_secret: _Optional[str] = ...) -> None: ...

class SetDefaultPaymentMethodRequest(_message.Message):
    __slots__ = ("payment_method_id",)
    PAYMENT_METHOD_ID_FIELD_NUMBER: _ClassVar[int]
    payment_method_id: str
    def __init__(self, payment_method_id: _Optional[str] = ...) -> None: ...

class SetDefaultPaymentMethodResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeletePaymentMethodRequest(_message.Message):
    __slots__ = ("payment_method_id",)
    PAYMENT_METHOD_ID_FIELD_NUMBER: _ClassVar[int]
    payment_method_id: str
    def __init__(self, payment_method_id: _Optional[str] = ...) -> None: ...

class DeletePaymentMethodResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingHistoryRequest(_message.Message):
    __slots__ = ("limit", "starting_after")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    STARTING_AFTER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    starting_after: str
    def __init__(self, limit: _Optional[int] = ..., starting_after: _Optional[str] = ...) -> None: ...

class GetBillingHistoryResponse(_message.Message):
    __slots__ = ("invoices", "has_more")
    INVOICES_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_FIELD_NUMBER: _ClassVar[int]
    invoices: _containers.RepeatedCompositeFieldContainer[StripeInvoice]
    has_more: bool
    def __init__(
        self, invoices: _Optional[_Iterable[_Union[StripeInvoice, _Mapping]]] = ..., has_more: bool = ...
    ) -> None: ...

class PurchaseCreditsRequest(_message.Message):
    __slots__ = ("amount_cents",)
    AMOUNT_CENTS_FIELD_NUMBER: _ClassVar[int]
    amount_cents: int
    def __init__(self, amount_cents: _Optional[int] = ...) -> None: ...

class PurchaseCreditsResponse(_message.Message):
    __slots__ = ("invoice_id", "credits_granted")
    INVOICE_ID_FIELD_NUMBER: _ClassVar[int]
    CREDITS_GRANTED_FIELD_NUMBER: _ClassVar[int]
    invoice_id: str
    credits_granted: int
    def __init__(self, invoice_id: _Optional[str] = ..., credits_granted: _Optional[int] = ...) -> None: ...

class UpdateAutoRechargeRequest(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: AutoRechargeConfig
    def __init__(self, config: _Optional[_Union[AutoRechargeConfig, _Mapping]] = ...) -> None: ...

class UpdateAutoRechargeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateSpendLimitRequest(_message.Message):
    __slots__ = ("monthly_limit_credits",)
    MONTHLY_LIMIT_CREDITS_FIELD_NUMBER: _ClassVar[int]
    monthly_limit_credits: int
    def __init__(self, monthly_limit_credits: _Optional[int] = ...) -> None: ...

class UpdateSpendLimitResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingPreferencesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingPreferencesResponse(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: BillingPreferences
    def __init__(self, preferences: _Optional[_Union[BillingPreferences, _Mapping]] = ...) -> None: ...

class UpdateBillingPreferencesRequest(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: BillingPreferences
    def __init__(self, preferences: _Optional[_Union[BillingPreferences, _Mapping]] = ...) -> None: ...

class UpdateBillingPreferencesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CancelPlanRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CancelPlanResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
