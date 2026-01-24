import json

from enum import IntEnum
from typing import Any, Dict, Optional
from cffi import FFI

ffi = FFI()

from .clib import clib

NodeHandle = int

def read_sized_string(sized_string) -> Optional[str]:
    if sized_string.length == 0:
        return None
    return bytes(sized_string.bytes[0:sized_string.length]).decode()

def read_bytes_to_string(ptr, length) -> Optional[str]:
    if length == 0:
        return None
    return bytes(ptr[0:length]).decode()

class NodePropsType(IntEnum):
    STRING = 0
    ENUM = 1
    INT = 2
    FLOAT = 3
    BOOL = 4
    OBJECT = 5
    VOID = 6
    UNKNOWN = 7

class NodeIteratorState(IntEnum):
    MAYBE_MORE = 0
    CONSUMED = 1

class NodeProps:
    handle: NodeHandle
    error: bool
    enum_value: Optional[str]
    object_type_name: Optional[str]
    type: NodePropsType

    def __init__(self, node_result):
        self.handle = node_result.id
        self.type = node_result.type
        self.error = node_result.error
        if not self.error:
            self.enum_value = read_sized_string(node_result.enum_value)
            self.object_type_name = read_sized_string(node_result.object_type_name)
        else:
            self.enum_value = None
            self.object_type_name = None

class NodePropsIterable:
    def __init__(self, iterator_result):
        self.handle = iterator_result.id
        self.error = iterator_result.error

    def __iter__(self):
        return self
    
    def __next__(self) -> NodeProps:
        if self.error:
            raise StopIteration()

        next_result = clib.node_iterator_next(self.handle)
        if next_result.state == NodeIteratorState.CONSUMED:
            raise StopIteration()
        elif next_result.error:
            raise StopIteration()
        
        return NodeProps(next_result.node)

class Node:
    def __init__(self, props: NodeProps):
        self._props = props
    
    def __del__(self):
        clib.node_free(self._props.handle)
    
    def wait_for_initialization(self):
        clib.wait_for_initialization(self._props.handle)

    def flush_logs(self):
        clib.node_flush_logs(self._props.handle)

    def close(self):
        clib.node_close(self._props.handle)

    def _get_field(self, field: str, arguments: Dict[str, Any]) -> NodeProps:
        arguments_json = json.dumps(arguments)
        return NodeProps(clib.node_get_field(
            self._props.handle, field.encode(), arguments_json.encode()
        ))

    def _get_items(self, list_fallback_length) -> NodePropsIterable:
        return NodePropsIterable(clib.node_get_items(self._props.handle))

    def _evaluate(self) -> Optional[Any]:
        evaluate_result = clib.node_evaluate(self._props.handle)
        if evaluate_result.error:
            raise Exception("Evaluation encountered an error")

        value_string = read_bytes_to_string(
            evaluate_result.value,
            evaluate_result.length
        )
        if value_string is None:
            return None
        
        return json.loads(value_string)

    def _log_unexpected_type_error(self):
        clib.node_log_unexpected_type_error(self._props.handle)

    def _log_unexpected_value_error(self, value):
        clib.node_log_unexpected_value_error(self._props.handle)

class VoidNode(Node):
    def get(self) -> None:
        try:
            result = self._evaluate()
        except:
            return
        
        if isinstance(result, bool) and result:
            return
        
        self._log_unexpected_value_error(result)


class BooleanNode(Node):
    def get(self, fallback: bool) -> bool:
        try:
            result = self._evaluate()
        except:
            return fallback

        if not isinstance(result, bool):
            self._log_unexpected_value_error(result)
            return fallback
        
        return result

class IntNode(Node):
    def get(self, fallback: int) -> int:
        try:
            result = self._evaluate()
        except:
            return fallback

        if not isinstance(result, int):
            self._log_unexpected_value_error(result)
            return fallback

        return result

class FloatNode(Node):
    def get(self, fallback: float) -> float:
        try:
            result = self._evaluate()
        except:
            return fallback
        
        if not isinstance(result, float) and not isinstance(result, int):
            self._log_unexpected_value_error(result)
            return fallback
        
        return float(result)

class StringNode(Node):
    def get(self, fallback: str) -> str:
        try:
            result = self._evaluate()
        except:
            return fallback

        if not isinstance(result, str):
            self._log_unexpected_value_error(result)
            return fallback

        return result