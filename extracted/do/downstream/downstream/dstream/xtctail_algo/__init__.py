"""xtctail (eXTended Compressing) implements steady curation over binary
orders of magnitude, as a building block for the tiltedxtc algorithm.

Maintains most-recent (tail) observed instance of steady-curated hanoi values.
"""
import lazy_loader

__getattr__, __dir__, _ = lazy_loader.attach_stub(__name__, __file__)
