# this code is only meant to be "running" through mypy and not an actual python interpreter!
import typing

from typing_extensions import assert_type

from test.type_stub_helpers import e2e_example_export

blocking_foo = e2e_example_export.BlockingFoo("hello")

blocking_foo.some_static()