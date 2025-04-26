import typedload
from typing import *

typedload.load("a", Literal["a"])

def wantint(i: int) -> None: ...

wantint(typedload.load("3", int))
