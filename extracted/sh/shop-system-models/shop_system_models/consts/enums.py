from enum import Enum


class OrderProcesses(str, Enum):
    without_payment = "The-devs.Shop.CreateOrder"
    tg_payment = "The-devs.Shop.MakeOrderWithTelegramPayments"
    ton_payment = "The-devs.Shop.MakeOrderWithTONPayments"
    life_pay = "The-devs.Shop.CreateLinkPaymentsOrder"


class PaymentTypes(str, Enum):
    manual_payment_request = "ManualPaymentRequest"
    external_card_payment_provider = "ExternalCardPaymentProvider"
    crypto_ton = "CryptoTON"
    xtr = "XTR"
    life_pay = "LifePay"
    yookassa = "yookassa"
    tkassa = "tkassa"
    cloud_payments = "CloudPayments"


class ShopStatuses(str, Enum):
    deploying = "deploying"
    active = "active"
    importing = "importing"
    blocked = "blocked"
    unavailable = "unavailable"
    deleted = "deleted"


class TaskStatuses(str, Enum):
    pending = "pending"
    expired = "expired"
    completed = "completed"


class ServiceNames(str, Enum):
    bot = "bot"


class UserRoles(str, Enum):
    user = "user"
    admin = "admin"
    shop_admin = "shop_admin"
    shop_manager = "shop_manager"


PAYMENTS_PROCESSES_MAPPING = {
    PaymentTypes.manual_payment_request.value: OrderProcesses.without_payment.value,
    PaymentTypes.external_card_payment_provider.value: OrderProcesses.tg_payment.value,
    PaymentTypes.xtr.value: OrderProcesses.tg_payment.value,
    PaymentTypes.crypto_ton.value: OrderProcesses.ton_payment.value,
    PaymentTypes.life_pay.value: OrderProcesses.life_pay.value,
    PaymentTypes.yookassa.value: OrderProcesses.life_pay.value,
    PaymentTypes.tkassa.value: OrderProcesses.life_pay.value,
}
