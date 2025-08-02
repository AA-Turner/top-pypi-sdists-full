from functools import lru_cache

from emoji import emojize

from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.tg_bot.blank.common import SimpleBlankTgBot


class AdminTgBotBlank(SimpleBlankTgBot):
    def but_hello_world(self) -> str:
        res = "hello_world"
        return emojize(res.strip())

    def good(self) -> str:
        res = "Good"
        return emojize(res.strip())

    def user_dbm(self, *, user_dbm: UserDBM | None) -> str:
        if user_dbm is None:
            return "None"
        return transfer_data_to_json_str(user_dbm.simple_dict(), beautify=True)


@lru_cache()
def get_cached_eng_admin_tg_bot_blank() -> AdminTgBotBlank:
    return AdminTgBotBlank(lang=AdminTgBotBlank.Languages.rus)


def __example():
    pass


if __name__ == '__main__':
    __example()
