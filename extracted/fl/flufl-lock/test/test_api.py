import flufl.lock


def test_module_attributes_in_all():
    namespace = {}
    attributes = set(flufl.lock.__all__)
    exec('from flufl.lock import *', namespace)
    # __builtins__ is implicitly added to the namespace.
    del namespace['__builtins__']
    assert attributes == set(namespace)
