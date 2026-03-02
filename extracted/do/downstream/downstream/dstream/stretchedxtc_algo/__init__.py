"""stretchedxtc (eXTended Compressing) generalizes stretched curation past the
domain restriction of the naive stretched algorithm (2**S - 1).

Uses compressing steady curation to maintains first (head) observed instance of
steady-curated hanoi values after S hanoi values have been observed.
"""
import lazy_loader

__getattr__, __dir__, _ = lazy_loader.attach_stub(__name__, __file__)
