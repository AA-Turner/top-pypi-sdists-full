from typing import Dict

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.utils.mixin import SFHandlerDispatcherMixin


class Evaluator(SFHandlerDispatcherMixin):
    HANDLER_NAME = "evaluate"
    input_sf: SFrame
    DEFAULT_GROUP_KEYS: Dict[str, str] = {"test": configs.DEFAULT_SF_KEY}

    def __call__(self, test_sf: SFrame, **prediction_kwargs: object):
        test_kwargs = self.extract_raw(test_sf)
        return self.call_handler(test_sf, **prediction_kwargs, **test_kwargs)
