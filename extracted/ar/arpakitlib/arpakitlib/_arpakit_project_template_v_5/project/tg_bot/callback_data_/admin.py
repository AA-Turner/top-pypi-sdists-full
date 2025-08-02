from project.tg_bot.callback_data_.common import BaseCD


class HelloWorldAdminCD(BaseCD):
    hello_world: bool = True
