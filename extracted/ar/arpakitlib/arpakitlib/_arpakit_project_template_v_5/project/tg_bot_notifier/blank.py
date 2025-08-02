from functools import lru_cache

from arpakitlib.ar_blank_util import BaseBlank


class TgBotNotifierBlank(BaseBlank):
    pass


@lru_cache()
def get_cached_rus_tg_bot_notifier_blank() -> TgBotNotifierBlank:
    return TgBotNotifierBlank(lang=TgBotNotifierBlank.Languages.rus)


def __example():
    print(get_cached_rus_tg_bot_notifier_blank().hello_world())


if __name__ == '__main__':
    __example()
