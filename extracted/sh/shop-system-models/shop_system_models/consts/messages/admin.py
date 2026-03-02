ADMIN_ORDER_CREATED_MESSAGE: dict[str, str] = {
    "RU": "{user} создал заказ: {order_number}.\n\n"
    "<b>{order_products}</b>\n"
    "Тип доставки: {order_delivery_type}\n"
    "Данные для доставки: <code>{order_delivery_info}</code>\n"
    "Желаемая дата доставки: {order_date_from}\n"
    "Телефон для связи: <code>{user_contact_number}</code>\n"
    "Комментарий: <code>{order_comment}</code>\n\n"
    "Сумма заказа: <b>{order_amount} {currency}</b>{payment_type_text}\n\n"
    "Установите статус👇",
    "EN": "{user} has created an order: {order_number}.\n\n"
    "<b>{order_products}</b>\n"
    "Delivery type: {order_delivery_type}\n"
    "Delivery info: <code>{order_delivery_info}</code>\n"
    "Desired delivery date: {order_date_from}\n"
    "Contact phone number: <code>{user_contact_number}</code>\n"
    "Comment: <code>{order_comment}</code>\n\n"
    "Order amount: <b>{order_amount} {currency}</b>{payment_type_text}\n\n"
    "Set the status👇",
}

ADMIN_ORDER_UPDATED_STATUS_MESSAGE: dict[str, str] = {
    "RU": "Статус заказа {order_number} от {user} изменен.\n\n"
    "<b>{order_products}</b>\n"
    "Тип доставки: {order_delivery_type}\n"
    "Данные для доставки: <code>{order_delivery_info}</code>\n"
    "Желаемая дата доставки: {order_date_from}\n"
    "Телефон для связи: <code>{user_contact_number}</code>\n"
    "Комментарий: <code>{order_comment}</code>\n\n"
    "Сумма заказа: <b>{order_amount} {currency}</b>{payment_type_text}\n"
    "Обновленный статус: 👉 <b>{order_status}</b>",
    "EN": "The status of the order {order_number} from {user} has been changed.\n\n"
    "<b>{order_products}</b>\n"
    "Delivery type: {order_delivery_type}\n"
    "Delivery info: <code>{order_delivery_info}</code>\n"
    "Desired delivery date: {order_date_from}\n"
    "Contact phone number: <code>{user_contact_number}</code>\n"
    "Comment: <code>{order_comment}</code>\n\n"
    "Order amount: <b>{order_amount} {currency}</b>{payment_type_text}\n"
    "Updated status: 👉 <b>{order_status}</b>",
}


DEFAULT_USER_STATUS_MESSAGES: dict[str, dict[str, str]] = {
    "EN": {
        "Not payed": """Order {order_number} created
{order_products}

Delivery type: {order_delivery_type}
Delivery info: {order_delivery_info}
Delivery Date: {order_date_from}
Comment: {order_comment}
Total Amount: {order_amount} 

Status: Not paid""",
        "Booking request": """Booking request {order_number} created
{order_products}

Delivery type: {order_delivery_type}
From date: {order_booking_details_from_date}
Till date: {order_booking_details_till_date}
Comment: {order_comment}

Status: Booking Requested""",
        "Payed": """Order {order_number} updated
{order_products}
Delivery Type: {order_delivery_type}
Delivery Information: {order_delivery_info}
Desired Delivery Date: {order_date_from}
Comment: {order_comment}
Amount: {order_amount} 

Status: Paid""",
        "Preparing": """Order {order_number} updated
{order_products}
Delivery Type: {order_delivery_type}
Delivery Information: {order_delivery_info}
Desired Delivery Date: {order_date_from}
Comment: {order_comment}
Amount: {order_amount} 

Status: Preparing""",
        "On the way": """Order {order_number} updated
{order_products}
Delivery Type: {order_delivery_type}
Delivery Information: {order_delivery_info}
Desired Delivery Date: {order_date_from}
Comment: {order_comment}
Amount: {order_amount} 

Status: On the way""",
        "Delivered": """Order {order_number} updated
{order_products}
Delivery Type: {order_delivery_type}
Delivery Information: {order_delivery_info}
Desired Delivery Date: {order_date_from}
Comment: {order_comment}
Amount: {order_amount} 

Status: Delivered""",
        "Cancelled": """Order {order_number} updated
{order_products}
Delivery Type: {order_delivery_type}
Delivery Information: {order_delivery_info}
Desired Delivery Date: {order_date_from}
Comment: {order_comment}
Amount: {order_amount} 

Status: Cancelled""",
        "default": """Order {order_number} updated
{order_products}
Delivery Type: {order_delivery_type}
Delivery Information: {order_delivery_info}
Desired Delivery Date: {order_date_from}
Comment: {order_comment}
Amount: {order_amount} 

Status: {status}""",
    },
    "RU": {
        "Не оплачен": """Создан заказ {order_number}
{order_products}

Тип доставки: {order_delivery_type}
Данные для доставки: {order_delivery_info}
Желаемая дата доставки: {order_date_from}
Комментарий: {order_comment}
Сумма заказа: {order_amount} 

Статус: Не оплачен""",
        "Запрос Брони": """Бронь {order_number} создана
{order_products}

{order_booking_details_from_date} - {order_booking_details_till_date}
Комментарий: {order_comment}

Статус: Запрошена Бронь""",
        "Оплачен": """Статус заказа {order_number} обновлен
{order_products}

Тип доставки: {order_delivery_type}
Данные для доставки: {order_delivery_info}
Желаемая дата доставки: {order_date_from}
Комментарий: {order_comment}
Сумма заказа: {order_amount} 

Статус: Оплачен""",
        "Собирается": """Статус заказа {order_number} обновлен
{order_products}

Тип доставки: {order_delivery_type}
Данные для доставки: {order_delivery_info}
Желаемая дата доставки: {order_date_from}
Комментарий: {order_comment}
Сумма заказа: {order_amount} 

Статус: Собирается""",
        "В пути": """Статус заказа {order_number} обновлен
{order_products}

Тип доставки: {order_delivery_type}
Данные для доставки: {order_delivery_info}
Желаемая дата доставки: {order_date_from}
Комментарий: {order_comment}
Сумма заказа: {order_amount} 

Статус: В пути""",
        "Доставлен": """Статус заказа {order_number} обновлен
{order_products}

Тип доставки: {order_delivery_type}
Данные для доставки: {order_delivery_info}
Желаемая дата доставки: {order_date_from}
Комментарий: {order_comment}
Сумма заказа: {order_amount} 

Статус: Доставлен""",
        "Отменен": """Статус заказа {order_number} обновлен
{order_products}

Тип доставки: {order_delivery_type}
Данные для доставки: {order_delivery_info}
Желаемая дата доставки: {order_date_from}
Комментарий: {order_comment}
Сумма заказа: {order_amount} 

Статус: Отменен""",
        "default": """Статус заказа {order_number} обновлен
{order_products}

Тип доставки: {order_delivery_type}
Данные для доставки: {order_delivery_info}
Желаемая дата доставки: {order_date_from}
Комментарий: {order_comment}
Сумма заказа: {order_amount} 

Статус: {status}""",
    },
}
