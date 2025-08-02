# arpakit
from arpakitlib.ar_enumeration_util import Enumeration

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseBlank:
    class Languages(Enumeration):
        rus = "ru"        # Русский
        eng = "en"        # Английский
        spa = "es"        # Испанский
        deu = "de"        # Немецкий
        fra = "fr"        # Французский
        ita = "it"        # Итальянский
        por = "pt"        # Португальский
        jpn = "ja"        # Японский
        kor = "ko"        # Корейский
        zho = "zh"        # Китайский
        ara = "ar"        # Арабский

    def __init__(self, *, lang: str = "ru", **kwargs):
        self.lang = lang.strip()

    def compare_lang(self, v: str) -> bool:
        if self.lang.lower() == v.lower().strip():
            return True
        return False

    def hello_world(self) -> str:
        if self.compare_lang(self.Languages.rus):
            return "Привет, мир!"   # Русский

        if self.compare_lang(self.Languages.eng):
            return "Hello, world!"  # Английский

        if self.compare_lang(self.Languages.spa):
            return "¡Hola, mundo!"  # Испанский

        if self.compare_lang(self.Languages.deu):
            return "Hallo, Welt!"   # Немецкий

        if self.compare_lang(self.Languages.fra):
            return "Bonjour, le monde!"  # Французский

        if self.compare_lang(self.Languages.ita):
            return "Ciao, mondo!"    # Итальянский

        if self.compare_lang(self.Languages.por):
            return "Olá, mundo!"     # Португальский

        if self.compare_lang(self.Languages.jpn):
            return "こんにちは、世界！"  # Японский

        if self.compare_lang(self.Languages.kor):
            return "안녕, 세상!"       # Корейский

        if self.compare_lang(self.Languages.zho):
            return "你好，世界！"      # Китайский

        if self.compare_lang(self.Languages.ara):
            return "مرحبا بالعالم!"   # Арабский

        # если язык не найден
        return "Hello, world!"

