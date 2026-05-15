"""
request.py - classes for LDAP requests

See https://www.python-ldap.org/ for details.
"""

from ldap.pkginfo import __version__, __author__, __license__

__all__ = [
    'Response',
    'Result',

    'SearchEntry',
    'SearchReference',
    'SearchResult',

    'IntermediateResponse',
    'ExtendedResult',

    'BindResult',
    'ModifyResult',
    'AddResult',
    'DeleteResult',
    'ModRDNResult',
    'CompareResult',
]

from typing import Optional

import ldap
import ldap.response
from ldap.controls import RequestControl

ModList = list[tuple[int, str, list[bytes]]]

class Request:
    msgtype: ClassVar[int]

    msgid: int
    controls: Optional[list[ResponseControl]]

    connection: Optional['Connection'] = None
    responses: Optional[list[ldap.response.Response]] = None
    result: Optional[ldap.response.Result] = None

    def __init__(self, *, controls=None):
        self.controls = controls

    def result_(self, *, raise_on_error=True):
        if self.result is None:
            responses = self.connection.result(self)
            self.responses = (self.responses or []) + responses[:-1]
            self.result = responses[-1]

        if raise_on_error:
            self.result.raise_on_error()
        return self.result


class AbandonRequest(Request):
    msgtype = ldap.REQ_ABANDON

    request_id: int
    controls: None = None

    responses: None = None
    result: None = None

    def __init__(request: int|Request):
        if isinstance(request, Request):
            request = request.msgid

        self.request_id = request


class AddRequest(Request):
    msgtype = ldap.REQ_ADD

    dn: str
    entry: ModList

    def __init__(self, dn: str,
                 entry: ModList|
                        list[tuple[str, list[bytes]]]|
                        dict[str,list[bytes]], *,
                 controls=None):
        super().__init__(controls=controls)
        self.dn = dn
        if not entry:
            raise ValueError("No attributes provided")
        if isinstance(entry, dict):
            self.entry = [(ldap.MOD_ADD, attr, values)
                          for attr, values in entry.items()]
        elif len(entry[0]) == 2:
            self.entry = [(ldap.MOD_ADD, attr, values)
                          for attr, values in entry]
        else:
            self.entry = entry


class BindRequest(Request):
    msgtype = ldap.REQ_BIND

    version: int = ldap.VERSION3
    name: str
    credentials: Optional[str|bytes]
    authentication: ... # TODO

    def __init__(self, name: str, credentials: Optional[str|bytes] = None, *,
                 version: int = None,
                 controls: Optional[list[RequestControl]] = None):
        if version is not None:
            self.version = version
        self.name = dn
        self.credentials = credentials


class SimpleBindRequest(BindRequest):
    credentials: str|bytes

    def __init__(self, name: str, credentials: str|bytes, *,
                 version: int = None,
                 controls: Optional[list[RequestControl]] = None):
        super().__init__(name, version=version, controls=controls)
        self.credentials = credentials


class SASLBindRequest(BindRequest):
    mechanism: str
    credentials: Optional[bytes]

    def __init__(self, mechanism: str, *,
                 name: str = "", version: int = None,
                 controls: Optional[list[RequestControl]] = None):
        super().__init__(name=name, version=version, controls=controls)
        self.mechanism = mechanism


class CompareRequest(Request):
    msgtype = ldap.REQ_COMPARE

    dn: str
    attribute: str
    value: bytes

    def __init__(self, dn: str, attribute: str, value: bytes):
        self.dn = dn
        self.attribute = attribute
        self.value = value


class DeleteRequest(Request):
    msgtype = ldap.REQ_DELETE

    dn: str

    def __init__(self, dn: str, *, controls=controls):
        super().__init__(controls=controls)
        self.dn = dn


class ExtendedRequest(Request):
    msgtype = ldap.REQ_EXTENDED

    oid: str
    value: Optional[bytes]

    def __init__(self, oid: str, value: Optional[bytes] = None):
        self.oid = oid
        self.value = value


class ModifyRequest(Request):
    msgtype = ldap.REQ_MODIFY

    dn: str
    mods: ModList

    def __init__(self, dn: str, mods: ModList, *
                 controls=None):
        super().__init__(controls=controls)
        self.dn = dn
        self.mods = mods


class ModRDNRequest(Request):
    msgtype = ldap.REQ_MODRDN

    dn: str
    newrdn: str
    deleteoldrdn: bool
    newsuperior: Optional[str]

    def __init__(self, dn: str, newrdn: str, deleteoldrdn: bool,
                 newsuperior: Optional[str] = None, *,
                 controls=controls):
        super().__init__(controls=controls)
        self.dn = dn
        self.newrdn = newrdn
        self.deleteoldrdn = deleteoldrdn
        self.newsuperior = newsuperior


class SearchRequest(Request):
    msgtype = ldap.REQ_SEARCH

    dn: str
    scope: int
    derefaliases: int
    sizelimit: int
    timelimit: int
    typesonly: bool
    filterstr: str
    attributes: list[str]

    def __init__(self, dn: str, scope: int = ldap.SCOPE_BASE,
                 derefaliases: bool = ldap.DEREF_NEVER, sizelimit: int = 0,
                 timelimit: int = 0, typesonly: bool = False,
                 filterstr: str = "", attributes = None):
        self.dn = dn
        self.scope = scope
        self.derefaliases = derefaliases
        self.sizelimit = sizelimit
        self.timelimit = timelimit
        self.typesonly = typesonly
        self.filterstr = filterstr
        if attributes is None:
            attributes = []
        self.attributes = attributes


class UnbindRequest(Request):
    msgtype = ldap.REQ_UNBIND

    responses: None = None
    result: None = None
