from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ShopDetailsModel(BaseModel):
    shop_id: str
    shop_name: str
    friendly_name: str
    shop_language: str = "RU"
    shop_api_url: str = "https://marketplace-api-dev.tg-shops.com"
    contact_phone: str | None = None
    contact_email: str
    orders_chat_id: int
    orders_history_chat_id: Optional[int] = None
    search_enabled: Optional[bool] = False
    warehouse_accounting: bool = False
    bot_url: str | None = None
    bot_token: str
    payment_token: str | None = None
    placeholder: str
    order_process: str
    nocodb_project_id: str
    nocodb_categories_table: str
    nocodb_products_table: str
    nocodb_orders_table: str
    nocodb_status_table: str
    nocodb_bot_commands_table: str
    nocodb_options_table: Optional[str] = None
    nocodb_options_category_table: Optional[str] = None
    topic_chat_id: Optional[int] = None
    premium_expiration_date: Optional[datetime] = None
    web_app_url: str = ""
