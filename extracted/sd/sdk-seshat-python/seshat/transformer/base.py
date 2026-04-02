from typing import Type, Dict, Callable

from seshat.data_class import SFrame, GroupSFrame, DFrame
from seshat.general import configs
from seshat.general.exceptions import OnlyGroupRequiredError, ColDoesNotExistError
from seshat.utils.mixin import SFHandlerDispatcherMixin


class Transformer(SFHandlerDispatcherMixin):
    """
    Manages and transforms SFrame data by dynamically applying transformations
    such as adding new columns, performing aggregations, or generating new SFrames.
    While it primarily handles SFrames, it can convert data to alternative format
    when required by specific transformation processes.

    Parameters
    ----------
    group_keys : dict
        Keys used to identify and retrieve data from a grouped SFrame for processing.

    Attributes
    ----------
    HANDLER_NAME : str
        The name of the handler method intended to be invoked for transforming the sf.
        This should correspond to the method tailored for the specific transformation required,
        including a suffix that identifies the type of data (e.g., '_df' for DataFrame handling).
    DEFAULT_FRAME : SFrame
        The default SFrame to use for conversion if no handler provided for input sframe
    ONLY_GROUP : bool
        A flag that, if set to True, restricts input to only grouped SFrames.
        If False, both single and grouped SFrames can be processed.
    DEFAULT_GROUP_KEYS : dict
        Default values for `group_keys` used if no specific `group_keys` are
        provided during initialization. Helps standardize how data is grouped
        or processed if not explicitly defined by the user.


    Notes
    -----
    Handler methods should be implemented for a variety of data types,
    each with a specific suffix (e.g., `_df` for handling dframe, `_spf` for spframe).

    """

    DEFAULT_FRAME: Type[SFrame] = DFrame
    HANDLER_NAME: str = "transform"

    def __init__(self, group_keys=None, *args, **kwargs):
        super().__init__(group_keys)
        self.default_sf_key = self.group_keys["default"]

    def __call__(self, sf_input: SFrame, *args: object, **kwargs: object) -> SFrame:
        self.validate(sf_input)
        if self.should_convert(sf_input):
            converted = sf_input.convert(
                to=self.DEFAULT_FRAME(), default_key=self.default_sf_key
            )
            converted = self.execute(converted, *args, **kwargs)
            return converted.convert(sf_input)
        else:
            return self.execute(sf_input, *args, **kwargs)

    @staticmethod
    def is_output_group_type(handler_output: Dict[str, object], *, sf_input: SFrame):
        if not isinstance(sf_input, GroupSFrame) and len(handler_output) > 1:
            return True
        return False

    def execute(self, sf_input: SFrame, *args, **kwargs):
        result = self.call_handler(sf_input, *args, **kwargs)
        if self.is_output_group_type(result, sf_input=sf_input):
            sf_output = sf_input.make_group(self.default_sf_key)
        else:
            sf_output = sf_input.from_raw(**self.get_from_raw_kwargs(sf_input))
        self.set_raw(sf_output, result)
        return sf_output

    def validate(self, sf: SFrame):
        if self.ONLY_GROUP and not isinstance(sf, GroupSFrame):
            raise OnlyGroupRequiredError()

    def _validate_columns(self, sf: SFrame, key=None, *cols):
        not_exist_cols = set(cols) - set(sf.get_columns(key))
        if not_exist_cols:
            raise ColDoesNotExistError(not_exist_cols)

    def call_handler(self, sf: SFrame, *args, **kwargs) -> Dict[str, object]:
        input_raw = self.extract_raw(sf)
        return super().call_handler(sf, *args, **input_raw, **kwargs)

    def extract_raw(self, sf: SFrame) -> Dict[str, object]:
        keys = self.group_keys
        if not isinstance(sf, GroupSFrame):
            keys = {"default": self.default_sf_key}
        return {k: getattr(sf.get(v), "data", None) for k, v in keys.items()}

    def set_raw(self, sf: SFrame, result: Dict[str, object]):
        for k, v in result.items():
            sf.set_raw(self.group_keys.get(k, k), v)

    @staticmethod
    def get_from_raw_kwargs(sf_input: SFrame):
        return {
            "children": dict(getattr(sf_input, "children", {})),
            "sframe_class": getattr(sf_input, "sframe_class", None),
            "data": None,
        }

    def calculate_complexity(self):
        raise NotImplementedError()


class GeneralTransformer(Transformer):
    """
    The general transformer takes a callable handler as input and
    passes default sf to it. The result is replaced with the default or
    kept in a separate sf called result, based on the keep_separate value.
    """

    DEFAULT_GROUP_KEYS: Dict[str, str] = {
        "default": configs.DEFAULT_SF_KEY,
        "result": "result",
    }

    def __init__(
        self,
        handler: Callable,
        keep_separate: bool = False,
        group_keys=None,
        *args,
        **kwargs
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.handler = handler
        self.keep_separate = keep_separate

    def transform(self, default: object, *args, **kwargs):
        result = self.handler(default)
        return (
            {"default": default, "result": result}
            if self.keep_separate
            else {"default": default}
        )

    def call_handler(self, sf: SFrame, *args, **kwargs) -> Dict[str, object]:
        input_raw = self.extract_raw(sf)
        return self.transform(**input_raw)
