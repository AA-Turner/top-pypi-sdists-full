from __future__ import annotations

import inspect
import json
import sys
from abc import abstractmethod
from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, Iterable, Literal, Tuple, Union

from typing_extensions import Self, dataclass_transform, get_type_hints

from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_basemodel, is_pydantic_basemodel_instance

BYTEMODEL_MAGIC_STR: str = "CHALK_BYTE_TRANSMISSION"
BYTEMODEL_NUM_LEN_BYTES: int = 8

if TYPE_CHECKING:
    from pydantic import BaseModel
else:
    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel


class ByteSerializable:
    @abstractmethod
    def serialize(self) -> bytes:
        ...

    @classmethod
    @abstractmethod
    def deserialize(cls, body_bytes: bytes) -> Self:
        ...


@dataclass_transform()
class ByteBaseModel(ByteSerializable):
    @staticmethod
    def check_len(byte_arr: bytes, start_idx: int, desired_len: int) -> None:
        if start_idx + desired_len > len(byte_arr):
            raise RuntimeError("Tried to consume more bytes than were available!")

    @classmethod
    def produce_len_val(
        cls, start_idx: int, buffer: BytesIO, l: int, endianness: Literal["little", "big"] = "big"
    ) -> Tuple[int, int]:
        len_bytes = l.to_bytes(BYTEMODEL_NUM_LEN_BYTES, endianness)
        buffer.write(len_bytes)
        return start_idx + len(len_bytes), len(len_bytes)

    @classmethod
    def consume_len(
        cls, start_idx: int, bytes_arr: bytes, endianness: Literal["little", "big"] = "big"
    ) -> Tuple[int, int]:
        cls.check_len(bytes_arr, start_idx, BYTEMODEL_NUM_LEN_BYTES)
        return start_idx + BYTEMODEL_NUM_LEN_BYTES, int.from_bytes(
            bytes_arr[start_idx : start_idx + BYTEMODEL_NUM_LEN_BYTES], endianness
        )

    @classmethod
    def consume_magic_str(cls, start_idx: int, candidate_bytes: bytes) -> Tuple[int, None]:
        magic_bytes = BYTEMODEL_MAGIC_STR.encode("utf-8")
        cls.check_len(candidate_bytes, start_idx, len(magic_bytes))
        if magic_bytes != candidate_bytes[start_idx : len(magic_bytes)]:
            raise RuntimeError(f'Failed to find the magic string, "f{BYTEMODEL_MAGIC_STR}".')
        return start_idx + len(magic_bytes), None

    @classmethod
    def produce_magic_str(cls, start_idx: int, buffer: BytesIO) -> Tuple[int, int]:
        magic_str_bytes = BYTEMODEL_MAGIC_STR.encode("utf-8")
        buffer.write(magic_str_bytes)
        return start_idx + len(magic_str_bytes), len(magic_str_bytes)

    @classmethod
    def produce_json_attrs_bytes(cls, start_idx: int, buffer: BytesIO, model: ByteBaseModel) -> Tuple[int, int]:
        attrs_json_bytes = json.dumps(model.get_non_byte_non_pydantic_attr_map()).encode("utf-8")
        cur_idx = start_idx
        cur_idx, _ = cls.produce_len_val(cur_idx, buffer, len(attrs_json_bytes))
        buffer.write(attrs_json_bytes)
        cur_idx += len(attrs_json_bytes)
        return cur_idx, cur_idx - start_idx

    @classmethod
    def consume_json_attrs(cls, start_idx: int, byte_arr: bytes) -> Tuple[int, dict]:
        cur_idx, json_len = cls.consume_len(start_idx, byte_arr)
        cls.check_len(byte_arr, cur_idx, json_len)
        attrs_dict = json.loads(byte_arr[cur_idx : cur_idx + json_len].decode("utf-8"))
        cur_idx += json_len
        return cur_idx, attrs_dict

    @classmethod
    def produce_pydantic_attrs_bytes(cls, start_idx: int, buffer: BytesIO, model: ByteBaseModel) -> Tuple[int, int]:
        pydantic_map: Dict[str, BaseModel] = model.get_pydantic_models_map()
        pydantic_as_json_map = {k: v.json() for k, v in pydantic_map.items()}
        pydantic_map_as_bytes = json.dumps(pydantic_as_json_map).encode("utf-8")
        cur_idx = start_idx
        cur_idx, _ = cls.produce_len_val(cur_idx, buffer, len(pydantic_map_as_bytes))
        buffer.write(pydantic_map_as_bytes)
        cur_idx += len(pydantic_map_as_bytes)
        return cur_idx, cur_idx - start_idx

    @classmethod
    def consume_pydantic_attrs(cls, start_idx: int, byte_arr: bytes) -> Tuple[int, dict]:
        cur_idx, json_len = cls.consume_len(start_idx, byte_arr)
        cls.check_len(byte_arr, cur_idx, json_len)
        attrs_dict: Dict = json.loads(byte_arr[cur_idx : cur_idx + json_len].decode("utf-8"))
        cur_idx += json_len
        pydantic_model_classes = [c for c in cls.get_field_annotations().values() if is_pydantic_basemodel(c)]
        pydantic_models_dict = {k: c(**json.loads(v)) for c, (k, v) in zip(pydantic_model_classes, attrs_dict.items())}

        return cur_idx, pydantic_models_dict

    @classmethod
    def create_byte_items_map_bytes(cls, byte_items_map: Dict[str, bytes]) -> bytes:
        return json.dumps({k: len(v) for k, v in byte_items_map.items()}).encode("utf-8")

    @classmethod
    def produce_byte_items_map(
        cls,
        start_idx: int,
        buffer: BytesIO,
        byte_serializable_items_map: Mapping[str, Union[bytes, ByteSerializable]],
    ):
        curr_idx = start_idx
        byte_items_map = {
            k: (v.serialize() if isinstance(v, ByteSerializable) else v) for k, v in byte_serializable_items_map.items()
        }
        data = cls.create_byte_items_map_bytes(byte_items_map)
        curr_idx, _ = cls.produce_len_val(curr_idx, buffer, len(data))
        buffer.write(data)
        curr_idx += len(data)
        return curr_idx, curr_idx - start_idx

    @classmethod
    def produce_byte_items_data(cls, start_idx: int, buffer: BytesIO, bytes_items: Iterable[bytes]) -> Tuple[int, int]:
        curr_idx = start_idx
        for byte_item in bytes_items:
            buffer.write(byte_item)
            curr_idx += len(byte_item)
        return curr_idx, curr_idx - start_idx

    @classmethod
    def consume_byte_items_map(cls, start_idx: int, byte_arr: bytes) -> Tuple[int, Dict[str, int]]:
        cur_idx, json_len = cls.consume_len(start_idx, byte_arr)
        cls.check_len(byte_arr, cur_idx, json_len)
        byte_items_map: Dict[str, int] = json.loads(byte_arr[cur_idx : cur_idx + json_len].decode("utf-8"))
        cur_idx += json_len
        return cur_idx, byte_items_map

    @classmethod
    def consume_byte_items(cls, start_idx: int, byte_arr: bytes) -> Tuple[int, Dict[str, bytes]]:
        cur_idx, byte_items_map = cls.consume_byte_items_map(start_idx, byte_arr)
        attrs_dict: Dict[str, bytes] = {}
        for attr_name, attr_byte_len in byte_items_map.items():
            cls.check_len(byte_arr, start_idx, attr_byte_len)
            attrs_dict[attr_name] = byte_arr[cur_idx : cur_idx + attr_byte_len]
            cur_idx += attr_byte_len
        return cur_idx, attrs_dict

    def get_byte_attr_map(self) -> Dict[str, bytes]:
        return {k: v for k, v in self.dict().items() if isinstance(v, bytes)}

    def get_byte_serializables_map(self):
        return {k: v for k, v in self.dict().items() if isinstance(v, ByteSerializable)}

    def get_pydantic_models_map(self):
        return {k: v for k, v in self.dict().items() if is_pydantic_basemodel_instance(v)}

    def get_non_byte_non_pydantic_attr_map(self) -> Dict[str, Any]:
        return {
            k: v
            for k, v in self.dict().items()
            if not isinstance(v, (bytes, ByteSerializable)) and not is_pydantic_basemodel_instance(v)
        }

    @classmethod
    def get_field_annotations(cls):
        return {k: v for k, v in get_type_hints(cls).items() if not k.startswith("_") and not inspect.ismethod(v)}

    @classmethod
    def get_byte_serializable_classes(cls):
        byte_serializable_classes_in_order = []
        for c in cls.get_field_annotations().values():
            if isinstance(c, str):
                if hasattr(sys.modules[__name__], c):
                    c_local = getattr(sys.modules[__name__], c)
                    if inspect.isclass(c_local) and issubclass(c_local, ByteSerializable):
                        byte_serializable_classes_in_order.append(c_local)
            elif inspect.isclass(c) and issubclass(c, ByteSerializable):
                byte_serializable_classes_in_order.append(c)
        return byte_serializable_classes_in_order

    @classmethod
    def deserialize(cls, body_bytes: bytes):
        curr_idx = 0
        curr_idx, _ = cls.consume_magic_str(curr_idx, body_bytes)
        curr_idx, non_byte_attrs = cls.consume_json_attrs(curr_idx, body_bytes)
        curr_idx, pydantic_attrs = cls.consume_pydantic_attrs(curr_idx, body_bytes)
        curr_idx, byte_attrs = cls.consume_byte_items(curr_idx, body_bytes)

        curr_idx, byte_serializables_bytes_items = cls.consume_byte_items(curr_idx, body_bytes)

        final_attrs = {k: v for k, v in non_byte_attrs.items()}
        final_attrs.update(byte_attrs)

        final_attrs.update(pydantic_attrs)

        byte_serializable_attrs = {}

        for (field_name, field_bytes), cls_for_bytes in zip(
            byte_serializables_bytes_items.items(), cls.get_byte_serializable_classes()
        ):

            byte_serializable_attrs[field_name] = cls_for_bytes.deserialize(field_bytes)

        final_attrs.update(byte_serializable_attrs)
        return cls(**final_attrs)

    def dict(self):
        return {k: v for k, v in self.__dict__.items() if k[0] != "_"}

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.dict())})"

    def serialize(self) -> bytes:
        # Magic str
        # attrs json len
        # attrs json
        # pydantic len
        # pydantic json
        # attr and byte offset json len
        # attr and byte offset json
        # concatenated byte objects
        # attr and byte offset json len
        # attr and byte offsets for serializables
        # concatenated byte objects

        buffer = BytesIO()

        cur_idx = 0

        # regular stuff
        cur_idx, _ = self.produce_magic_str(cur_idx, buffer)
        cur_idx, _ = self.produce_json_attrs_bytes(cur_idx, buffer, self)

        # pydantic objects
        cur_idx, _ = self.produce_pydantic_attrs_bytes(cur_idx, buffer, self)

        # bytes objects
        cur_idx, _ = self.produce_byte_items_map(cur_idx, buffer, self.get_byte_attr_map())
        cur_idx, _ = self.produce_byte_items_data(cur_idx, buffer, self.get_byte_attr_map().values())

        # byte-serializables objects
        byte_serializables_map = self.get_byte_serializables_map()
        cur_idx, _ = self.produce_byte_items_map(cur_idx, buffer, byte_serializables_map)
        cur_idx, _ = self.produce_byte_items_data(
            cur_idx, buffer, [v.serialize() for v in byte_serializables_map.values()]
        )

        buffer.seek(0)

        return buffer.getvalue()

    def __init__(self, **kwargs: Any):
        super().__init__()
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __eq__(self, other: object):
        if not isinstance(other, ByteBaseModel):
            return NotImplemented

        if self.get_byte_attr_map() != other.get_byte_attr_map():
            return False

        if self.get_byte_serializables_map() != other.get_byte_serializables_map():
            return False

        if self.get_non_byte_non_pydantic_attr_map() != other.get_non_byte_non_pydantic_attr_map():
            return False

        return True

    def __hash__(self):
        return hash(
            (self.get_byte_attr_map(), self.get_byte_serializables_map(), self.get_non_byte_non_pydantic_attr_map())
        )


class ByteDict(ByteBaseModel):
    def __init__(self, *args: Mapping[str, Any], **kwargs: Any):
        for arg in args:
            if not isinstance(arg, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise ValueError(f"Need all args (non-kwargs) in constructor to be dict-like objects. Got: {type(arg)}")
            for k in arg:
                self[k] = arg[k]
        for k, v in kwargs.items():
            self[k] = v

        super().__init__()

    def __setitem__(self, key: str | bytes, value: Union[bytes, ByteSerializable]):
        if not isinstance(key, str):
            raise ValueError(f"Expected key to be a string, got {type(key)}")
        if not isinstance(value, bytes):
            raise ValueError(f"Expected value to be bytes, got {type(value)}")

        self.__dict__[key] = value

    def __getitem__(self, key: str):
        if not isinstance(key, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError(f"Need for keys to be strings, got {type(key)}")
        return self.__dict__[key]

    def __delitem__(self, key: str):
        del self.__dict__[key]

    def __contains__(self, key: str):
        return key in self.dict()

    def __len__(self):
        return len(self.dict())

    def __iter__(self):
        return iter(self.dict())

    def get(self, key: str, default: Any = None) -> Any:
        return self.__dict__.get(key, default)

    def keys(self):
        return self.dict().keys()

    def values(self):
        return self.dict().values()

    def items(self):
        return self.dict().items()
