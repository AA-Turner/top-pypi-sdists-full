from collections.abc import Callable
from itertools import pairwise

from ..common import TypeHint
from ..type_tools.type_rendering import TypeHintRenderer
from .loc_stack_filtering import LocStack
from .location import AnyLoc, FieldLoc, InputFuncFieldLoc, TypeHintLoc


def format_type(tp: TypeHint, *, brackets: bool = True, uri_faced=False) -> str:
    text = TypeHintRenderer(uri_faced=uri_faced).render_type(tp)
    return f"‹{text}›" if brackets else text


def get_callable_name(func: Callable) -> str:
    return getattr(func, "__qualname__", None) or repr(func)


def format_loc_stack(loc_stack: LocStack[AnyLoc], *, always_wrap_with_brackets: bool = False) -> str:
    fmt_tp = format_type(loc_stack.last.type, brackets=False)

    try:
        field_loc = loc_stack.last.cast(FieldLoc)
    except TypeError:
        return f"‹{fmt_tp}›" if always_wrap_with_brackets else fmt_tp
    else:
        fmt_field = f"{field_loc.field_id}: {fmt_tp}"

    if loc_stack.last.is_castable(InputFuncFieldLoc):
        return f"parameter ‹{fmt_field}›"

    if len(loc_stack) >= 2:  # noqa: PLR2004
        src_owner = format_type(loc_stack[-2].type, brackets=False)
        return f"‹{src_owner}.{fmt_field}›"

    return f"‹{fmt_field}›"


def find_owner_with_field(stack: LocStack) -> tuple[TypeHintLoc, FieldLoc]:
    for next_loc, prev_loc in pairwise(reversed(stack)):
        if next_loc.is_castable(FieldLoc):
            return prev_loc, next_loc
    raise ValueError
