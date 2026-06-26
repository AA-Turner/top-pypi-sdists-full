import socket, re
from urllib.parse import urlparse, urljoin
# tiktoken / wordsegment are heavy (and wordsegment.load() pulls a corpus); keep
# them lazy so importing urlManager stays light. Names behave as before on use.
from abstract_webtools._lazy import LazyModule as _LazyModule, LazyAttr as _LazyAttr
tiktoken = _LazyModule("tiktoken")
load = _LazyAttr("wordsegment", "load")


def segment(text):
    """Lazy word-segmentation: import + load corpus on first call, not at import."""
    import wordsegment
    if not getattr(wordsegment, "WORDS", None):
        wordsegment.load()
    return wordsegment.segment(text)
from abstract_utilities import eatAll,capitalize,make_list

