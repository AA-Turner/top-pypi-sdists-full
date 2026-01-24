from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from django.db.backends.utils import CursorWrapper


def get_columns(cursor: "CursorWrapper") -> list[str]:
    return [col[0] for col in cursor.description or []]


def dictfetchall[T](cursor: "CursorWrapper", dict_type: type[T] = dict) -> Iterator[T]:
    columns = get_columns(cursor)
    for row in cursor.fetchall():
        # The spec for TypedDict is not compliant with the sepc for dict
        yield dict_type(zip(columns, row, strict=False))  # type: ignore


def dictfetchone(cursor: "CursorWrapper") -> dict:
    columns = get_columns(cursor)
    return dict(zip(columns, cursor.fetchone() or [], strict=False))
