import _my_library
from synchronicity import Synchronizer

synchronizer = Synchronizer()

foo = synchronizer.wrap(_my_library.foo, name="foo", target_module=__name__)
