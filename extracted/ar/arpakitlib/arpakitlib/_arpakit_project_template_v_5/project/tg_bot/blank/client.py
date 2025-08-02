from functools import lru_cache

from emoji import emojize

from project.tg_bot.blank.common import SimpleBlankTgBot
from project.tg_bot.const import ClientTgBotCommands


class ClientTgBotBlank(SimpleBlankTgBot):
    def command_to_desc(self) -> dict[str, str]:
        return {
            ClientTgBotCommands.start: emojize(":waving_hand: Начать"),
            ClientTgBotCommands.about: emojize(":information: О проекте"),
            ClientTgBotCommands.author: emojize(":bust_in_silhouette: Авторы"),
            ClientTgBotCommands.support: emojize(":red_heart: Поддержка"),
            ClientTgBotCommands.cancel: emojize(":right_arrow_curving_left: Отмена"),
        }

    def but_support(self) -> str:
        res = ":red_heart: Поддержка"
        return emojize(res.strip())

    def error(self) -> str:
        res = ":warning: <b>Упс! Что-то пошло не так...</b> :warning:"
        res += "\n\n:wrench:  Мы уже работаем над решением проблемы"
        res += "\n\n:red_heart: Приносим извинения за неудобства :red_heart:"
        return emojize(res.strip())

    def healthcheck(self) -> str:
        res = "healthcheck"
        return emojize(res.strip())

    def author(self) -> str:
        res = "<b>ARPAKIT Company</b>"
        res += "\n\n<i>Мы создаём качественные IT продукты</i>"
        res += "\n\n:link: https://arpakit.com/"
        res += "\n\n:e-mail: support@arpakit.com"
        return emojize(res.strip())

    def welcome(self) -> str:
        res = ":waving_hand: <b>Welcome</b> :waving_hand:"
        return emojize(res.strip())

    def raw_message(self) -> str:
        res = ":warning: <b>Сообщение не обработано</b> :warning:"
        return emojize(res.strip())

    def about(self) -> str:
        res = ":information: <b>О проекте</b>"
        return emojize(res.strip())

    def support(self) -> str:
        res = ":red_heart: <b>Поддержка</b> :red_heart:"
        res += f"\n\n:link: https://t.me/arpakit"
        return emojize(res.strip())

    def keyboard_is_old(self) -> str:
        res = ":information: Эта клавиатура устарела :information:"
        return emojize(res.strip())

    def cancel(self) -> str:
        res = ":right_arrow_curving_left: <b>Отмена</b>"
        return emojize(res.strip())


@lru_cache()
def get_cached_rus_client_tg_bot_blank() -> ClientTgBotBlank:
    return ClientTgBotBlank(lang=ClientTgBotBlank.Languages.rus)


def __example():
    print(get_cached_rus_client_tg_bot_blank().author())


if __name__ == '__main__':
    __example()
