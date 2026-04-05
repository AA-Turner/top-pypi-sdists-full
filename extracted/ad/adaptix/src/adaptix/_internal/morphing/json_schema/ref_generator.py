import re
import string

from ...provider.loc_stack_filtering import LocStack
from ...provider.loc_stack_tools import format_type
from .definitions import JSONSchema
from .resolver import RefGenerator

URI_SAFE = string.ascii_letters + string.digits + "-._~"
URI_UNSAFE_REGEX = re.compile(f"[^{re.escape(URI_SAFE)}]")


class BuiltinRefGenerator(RefGenerator):
    def generate_ref(self, json_schema: JSONSchema, loc_stack: LocStack) -> str:
        tp_fmt = format_type(loc_stack.last.type, brackets=False, uri_faced=True)
        return URI_UNSAFE_REGEX.sub("_", tp_fmt)
