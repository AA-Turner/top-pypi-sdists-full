import flufl.bounce


def test_module_attributes_in_all():
    # ruff's F822 skips __init__.py, so this is what catches a name listed in __all__ that the
    # module doesn't define: the star import raises AttributeError on it.  The comparison then
    # checks the converse, that the star import brings in nothing __all__ doesn't name.
    namespace = {}
    attributes = set(flufl.bounce.__all__)
    exec('from flufl.bounce import *', namespace)
    # __builtins__ is implicitly added to the namespace.
    del namespace['__builtins__']
    assert attributes == set(namespace)
