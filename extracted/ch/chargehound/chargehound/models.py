from collections import namedtuple
from munch import Munch


class ChargehoundObject(Munch):
    pass


class List(ChargehoundObject):
    pass


class Dispute(ChargehoundObject):
    pass


class Product(ChargehoundObject):
    pass


class Response(ChargehoundObject):
    pass


class CorrespondenceItem(ChargehoundObject):
    pass


class PastPayment(ChargehoundObject):
    pass


HTTPResponse = namedtuple('HTTPResponse', 'status')
