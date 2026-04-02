from typing import Dict

from seshat.data_class import SFrame, SF_MAP, RAW_MAP
from seshat.general import configs


class SFHandlerDispatcherMixin:
    HANDLER_NAME: str = "handle"
    DEFAULT_GROUP_KEYS: Dict[str, str] = {"default": configs.DEFAULT_SF_KEY}
    ONLY_GROUP: bool = False

    def __init__(self, group_keys=None):
        self.group_keys = group_keys or self.DEFAULT_GROUP_KEYS

    def call_handler(self, sf: SFrame, *args, **kwargs):
        handler = getattr(self, f"{self.HANDLER_NAME}_{sf.frame_name}")
        return handler(*args, **kwargs)

    def should_convert(self, sf: SFrame):
        return not hasattr(self, f"{self.HANDLER_NAME}_{sf.frame_name}")

    def extract_raw(self, sf: SFrame) -> Dict[str, object]:
        return {k: getattr(sf.get(v), "data", None) for k, v in self.group_keys.items()}

    def set_raw(self, sf: SFrame, result: Dict[str, object]):
        for k, v in result.items():
            sf.set_raw(self.group_keys.get(k, k), v)


class RawHandlerDispatcherMixin:
    """
    This mixin is used to dispatch raw input to related handler based on it's type.
    """

    HANDLER_NAME: str = "handler"

    def call_handler(self, raw: object, *args, **kwargs):
        raw_name = self.raw_to_name(raw)
        handler = getattr(self, f"{self.HANDLER_NAME}_{raw_name}")
        return handler(raw, *args, **kwargs)

    @staticmethod
    def raw_to_name(raw):
        for name, sf_type in RAW_MAP.items():
            if isinstance(raw, sf_type):
                return name
        raise KeyError(
            "Raw is not valid. Supported types are: %s" % (", ".join(SF_MAP.values()))
        )
