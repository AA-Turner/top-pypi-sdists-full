from pydantic import BaseModel, field_validator

from shop_system_models.shop_api.bot.request import ButtonModel


class BotCommandModel(BaseModel):
    name: str
    message: str

    @field_validator("name", mode="before")
    def command_validation(cls, value):
        if value.startswith("/"):
            return value
        raise ValueError('Bot command should start with "/"')


class NotificationPayloadModel(BaseModel):
    chat_id: int
    message_id: int | None = -1
    text: str
    buttons: list[ButtonModel] = []
