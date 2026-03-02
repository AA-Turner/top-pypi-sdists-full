from shop_system_models.consts.messages.admin import (
    ADMIN_ORDER_CREATED_MESSAGE,
    ADMIN_ORDER_UPDATED_STATUS_MESSAGE,
)
from shop_system_models.shop_api.bot.request import MessagesType

ADMIN_MESSAGES = {
    MessagesType.admin_order_created: ADMIN_ORDER_CREATED_MESSAGE,
    MessagesType.admin_order_updated: ADMIN_ORDER_UPDATED_STATUS_MESSAGE,
}

PAYMENT_MESSAGE = {"RU": "Способ оплаты: ", "EN": "Payment method: "}

OPEN_TG_PAYMENT_DETAILS_MESSAGE = {
    "RU": "Оплата заказа производится по банковской карте с помощью платежного провайдера телеграмма.",
    "EN": "Order payment is made by bank card using the telegram payment provider.",
}

OPEN_TG_STARS_DETAILS_MESSAGE = {
    "RU": "Оплата заказа производится с использованием Telegram Stars",
    "EN": "Order payment is made using Telegram Stars",
}
