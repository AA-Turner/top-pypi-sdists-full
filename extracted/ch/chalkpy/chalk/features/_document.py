from typing import TYPE_CHECKING, Type, TypeVar

from typing_extensions import Annotated

T = TypeVar("T")


if TYPE_CHECKING:

    class Document:
        ...

else:

    class DocumentMeta(type):
        def __getitem__(self, item: Type[T]) -> Type[T]:
            return Annotated[item, "__chalk_document__"]

    Document = DocumentMeta("Document", (object,), {})
