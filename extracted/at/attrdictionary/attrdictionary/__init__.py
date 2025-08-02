"""
attrdictionary contains several mapping objects that allow access to their
keys as attributes.
"""
from attrdictionary.default import AttrDefault
from attrdictionary.dictionary import AttrDict
from attrdictionary.mapping import AttrMap

__all__ = ["AttrMap", "AttrDict", "AttrDefault"]
