import copy
from typing import Dict, Iterable, Type, List, Any

from seshat.general import configs
from seshat.general.exceptions import (
    SFrameDoesNotExistError,
    UnknownDataClassError,
    InvalidArgumentsError,
)


class SFrame:
    """
    An interface for Seshat frames, providing a unified interface
    for either pandas or PySpark dataframes or others.
    This class facilitates additional functionalities over the standard dataframe operations,
    making it versatile for various data manipulation tasks.

    Attributes
    ----------
    data : pandas.DataFrame or pyspark.sql.DataFrame
        The actual dataframe object that is wrapped by this class.
        Depending on initialization,this can be a pandas or PySpark dataframe.
    frame_name : str
        A name assigned to the dataframe. This name is used to identify the dataframe
        and can be particularly useful working with multiple dataframes simultaneously.
    """

    frame_name: str
    data: object

    def __init__(self, data=None, *args, **kwargs):
        self.data = data

    def __add__(self, other):
        if other:
            self.extend(other.data)
        return self

    def __copy__(self):
        return type(self)(self.data)

    def __deepcopy__(self, memo):
        return type(self)(copy.deepcopy(self.data, memo))

    @property
    def empty(self, default_key=configs.DEFAULT_SF_KEY):
        pass

    def to_raw(self) -> Any:
        return self.data

    def set_raw(self, key: str, data: Any):
        self.data = data

    def get(self, key: str) -> "SFrame":
        return self

    def get_columns(self, *args) -> Iterable[str]:
        pass

    def to_dict(self, *cols: str, key: str = configs.DEFAULT_SF_KEY) -> List[Dict]:
        pass

    def iterrows(self, column_name: str, key: str = configs.DEFAULT_SF_KEY):
        pass

    def make_group(self, default_key=configs.DEFAULT_SF_KEY) -> "GroupSFrame":
        pass

    def convert(
        self, to: "SFrame", default_key: str = configs.DEFAULT_SF_KEY
    ) -> "SFrame":
        """
        Converts the current SFrame to match to the another SFrame.

        Parameters
        ----------
        to: SFrame
            The SFrame to which the current SFrame's data will be converted.

        Returns
        -------
        SFrame
            A converted SFrame instance.
        """
        if self.frame_name == to.frame_name:
            return self
        return self._convert(to)

    def _convert(self, to: "SFrame") -> "SFrame":
        return self.call_conversion_handler(self, to)

    def extend_from_csv(self, path, *args, **kwargs):
        new_data = self.read_csv(path, *args, **kwargs)
        self.extend(new_data)

    def extend(
        self,
        other: object,
        axis: int = 0,
        on: str = None,
        left_on: str = None,
        right_on: str = None,
        how: str = "left",
    ) -> object:
        if self.data is None:
            self.data = other
        elif axis == 0:
            self.extend_vertically(other)
        elif axis == 1:
            self.extend_horizontally(other, on, left_on, right_on, how)

        return self.data

    def extend_vertically(self, other: object):
        pass

    def extend_horizontally(
        self, other: object, on: str, left_on: str, right_on: str, how: str
    ):
        if on is None and (left_on is None or right_on is None):
            raise InvalidArgumentsError(
                "`on` or `left_on` and `right_on` cannot be None while trying to extend horizontally"
            )

    @classmethod
    def read_csv(cls, path, *args, **kwargs):
        pass

    @staticmethod
    def call_conversion_handler(from_: "SFrame", to: "SFrame") -> "SFrame":
        handler_name = f"to_{to.frame_name}"
        try:
            handler = getattr(from_, handler_name)
            return handler()
        except AttributeError:
            raise NotImplementedError(
                "handler for conversion to %s is not implemented" % to.frame_name
            )

    @classmethod
    def from_raw(cls, *args, **kwargs) -> "SFrame":
        return cls(*args, **kwargs)

    def __getitem__(self, item):
        return self

    def __setitem__(self, key, value):
        self.data = value.to_raw()


class GroupSFrame(SFrame):
    """
    A specialized class derived from SFrame that manages a collection of SFrames
    stored in a dictionary. Each SFrame within the dictionary can be accessed
    using a unique key. This class is designed to handle grouped data where
    each group is represented as an individual SFrame, allowing for operations
    to be performed on specific subsets of data efficiently.

    Parameters
    ----------
    children : dict
        A dictionary where each key-value pair consists of a string key
        and an SFrame as the value. This structure allows for easy access
        to each group's sframe by using its corresponding key.
    """

    # TODO: handle multiple types as children
    def __init__(
        self,
        children: Dict[str, SFrame] = None,
        sframe_class: Type[SFrame] = None,
        *args,
        **kwargs,
    ):
        super().__init__()
        if children is None:
            children = {}

        self.children = children
        self.sframe_class = sframe_class or self.find_sframe_class(
            raise_exception=False
        )

    def __copy__(self):
        return GroupSFrame(self.children, self.sframe_class)

    def __deepcopy__(self, memo):
        return type(self)(copy.deepcopy(self.children, memo), self.sframe_class)

    @property
    def empty(self, default_key=configs.DEFAULT_SF_KEY):
        return self[default_key].empty()

    def to_raw(self) -> Dict[str, object]:
        raw = {}
        for key, sf in self.children.items():
            raw[key] = sf.to_raw()
        return raw

    def set_raw(self, key, data: object):
        if self.sframe_class is None:
            self.sframe_class = self.find_sframe_class()
        if not isinstance(data, SFrame):
            data = self.sframe_class.from_raw(data)
        self.children[key] = data

    def get(self, key: str) -> SFrame:
        return self.children.get(key)

    def set_frame(self, key: str, new_frame: "SFrame") -> None:
        if isinstance(new_frame, GroupSFrame):
            for k, v in new_frame.children.items():
                self.children[k] = v
        else:
            self.children[key] = new_frame

    def get_columns(self, key) -> Iterable[str]:
        return self.get(key).get_columns()

    def to_dict(self, *cols: str, key: str = configs.DEFAULT_SF_KEY) -> List[Dict]:
        return self.get(key).to_dict(*cols)

    def iterrows(self, column_name: str, key: str = configs.DEFAULT_SF_KEY):
        return self.get(key).iterrows(column_name)

    def convert(
        self, to: "GroupSFrame", default_key: str = configs.DEFAULT_SF_KEY
    ) -> SFrame:
        if not isinstance(to, GroupSFrame):
            to = to.make_group(default_key)
        return super().convert(to)

    def _convert(self, to: "GroupSFrame") -> SFrame:
        for k, v in self.children.items():
            to[k] = self.call_conversion_handler(v, to)
        return to

    def make_group(self, default_key=configs.DEFAULT_SF_KEY):
        return self

    def raise_unknown_sf_exception(self):
        raise UnknownDataClassError(
            "one of the `children` or `sframe_class` must be set while calling `set_raw`"
        )

    def find_sframe_class(self, raise_exception=True):
        if hasattr(self, "children") and len(self.children) > 0:
            return list(self.children.values())[0].__class__
        if raise_exception:
            raise self.raise_unknown_sf_exception()

    @property
    def keys(self):
        for key in self.children.keys():
            yield key

    @property
    def frame_name(self) -> str:
        if self.sframe_class is None:
            self.sframe_class = self.find_sframe_class()
        return self.sframe_class.frame_name

    def __getitem__(self, key):
        try:
            return self.children[key]
        except KeyError:
            raise SFrameDoesNotExistError(self.__class__.__name__, key)

    def __setitem__(self, key, value):
        self.children[key] = value

    def __add__(self, other):
        return {**self.children, **other.children}
