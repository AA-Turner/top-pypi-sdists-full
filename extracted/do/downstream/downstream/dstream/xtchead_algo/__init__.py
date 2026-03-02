"""xtchead (eXTended Compressing) implements steady curation over binary
orders of magnitude, as a building block for the stretchedxtc algorithm.

Maintains first (head) observed instance of steady-curated hanoi values.
"""
import lazy_loader

__getattr__, __dir__, _ = lazy_loader.attach_stub(__name__, __file__)
