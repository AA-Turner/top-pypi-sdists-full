# arpakit

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class CollectingSubclassesMeta(type):
    """
    Метакласс для автоматического сбора всех наследников в поле ALL_SUBCLASSES.
    """

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)
        if not hasattr(cls, "all_subclasses"):
            cls.all_subclasses = []
        elif bases:
            cls.all_subclasses.append(cls)


def create_combined_meta(*metas):
    """
    Создает объединённый метакласс для устранения конфликтов.
    """

    class CombinedMeta(*metas):
        pass

    return CombinedMeta
