from typing import Optional

from pydantic import BaseModel


class DeployVariables(BaseModel):
    shop_name: str
    shop_id: str
    shop_template_id: str
    orders_chat_id: int
    contact_email: str
    tg_admin_id: int
    contact_phone: Optional[str]
    bot_token: Optional[str]
    invite_user: bool = True
