# Version of the python-kacl package
__version__ = "0.7.3"

from kacl.document import KACLDocument
from kacl.serializer import KACLMarkdownSerializer


def load(file):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    doc = None
    with open(file, "r") as f:
        document = f.read()
        try:
            doc = KACLDocument.parse(document, file)
        finally:
            f.close()
    return doc


def parse(text, file=None):
    return KACLDocument.parse(text, file)


def dump(document):
    return KACLMarkdownSerializer().serialize(document)


def new():
    return KACLDocument.init()
