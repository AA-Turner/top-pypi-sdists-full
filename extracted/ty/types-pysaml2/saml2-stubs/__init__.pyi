from logging import Logger
from typing import Any, Union, Protocol, Optional

import six
from xml.etree.ElementTree import ElementTree
from xmlschema import XMLSchema

class InstantiableFromXML(Protocol):
    c_namespace: str
    c_tag: str

logger: Logger
NAMESPACE: str
NAMEID_FORMAT_EMAILADDRESS: str
DECISION_TYPE_PERMIT: str
DECISION_TYPE_DENY: str
DECISION_TYPE_INDETERMINATE: str
VERSION: str
BINDING_SOAP: str
BINDING_PAOS: str
BINDING_HTTP_REDIRECT: str
BINDING_HTTP_POST: str
BINDING_HTTP_ARTIFACT: str
BINDING_URI: str

def class_name(instance: InstantiableFromXML) -> str: ...
def create_class_from_xml_string(
    target_class: type[InstantiableFromXML], xml_string: Union[str, six.binary_type]
) -> Any: ...
def create_class_from_element_tree(
    target_class: type[InstantiableFromXML], tree: ElementTree, namespace: Optional[str] = ..., tag: Optional[str] = ...
) -> Optional[Any]: ...

class Error(Exception): ...
class SAMLError(Exception): ...

class ExtensionElement:
    namespace: str
    tag: str
    attributes: dict[str, str]
    children: Optional[list[ExtensionElement]]
    text: str

    def __init__(
        self,
        tag: str,
        namespace: Optional[str] = ...,
        attributes: Optional[dict[str, str]] = ...,
        children: Optional[list[ExtensionElement]] = ...,
        text: Optional[str] = ...,
    ) -> None: ...
    def to_string(self) -> str: ...
    def transfer_to_element_tree(self) -> Optional[ElementTree]: ...
    def become_child_element_of(self, element_tree: ElementTree) -> None: ...
    def find_children(self, tag: Optional[str] = ..., namespace: Optional[str] = ...) -> list[ExtensionElement]: ...
    def loadd(self, ava: dict[str, Any]) -> ExtensionElement: ...

def extension_element_from_string(xml_string: Union[str, six.binary_type]) -> ExtensionElement: ...

class ExtensionContainer:
    c_tag: str
    c_namespace: str
    text: Optional[str]
    extension_elements: list[ExtensionElement]
    extension_attributes: dict[str, Any]
    encrypted_assertion: Any

    def __init__(
        self,
        text: Optional[str] = ...,
        extension_elements: Optional[list[ExtensionElement]] = ...,
        extension_attributes: Optional[dict[str, Any]] = ...,
    ) -> None: ...
    def harvest_element_tree(self, tree: ElementTree) -> None: ...
    def find_extensions(self, tag: Optional[str] = ..., namespace: Optional[str] = ...) -> list[ExtensionElement]: ...
    def extensions_as_elements(self, tag: str, schema: XMLSchema) -> list[ExtensionElement]: ...
    def add_extension_elements(self, items: list[ExtensionElement]) -> None: ...
    def add_extension_element(self, item: ExtensionElement) -> None: ...
    def add_extension_attribute(self, name: str, value: Any) -> None: ...

REQUIRED: int

def __getattr__(name: str) -> Any: ...  # incomplete
