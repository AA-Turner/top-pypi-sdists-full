"""Authenticated user-data ACL metadata controls, independent of storage bootstrap.

Canonical controls always address logical prod. Pagination is a bounded observed
traversal, not a snapshot or a proof of absence during concurrent mutations.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
import inspect
import math
import re
from urllib.parse import urlencode

from ..errors import SchemaError, TransportError, RequestDeadlineExceeded
from .user_data_entries import _text, _path, _timestamp
from .user_data_writes import _Budget

_ROLES = {r: 'built-in:user-data-' + r for r in ('reader', 'writer', 'admin')}
_UID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}')
_LEGACY_ENVS = frozenset(('dev', 'internal-dev', 'external-dev'))
_MAX_ROWS = 1000
_MAX_PAGES = 5
_PAGE_SIZE = 200
_BASE = '/apis/v1/role-bindings'


class UserDataACLIncomplete(SchemaError):
    """The bounded traversal cannot truthfully return a complete ACL list."""


class UserDataACLUnauthorized(TransportError):
    """Fresh user-data control authorization was denied; no cached permission."""


def _invalid():
    return SchemaError('invalid user-data ACL input or response')


def _budget(seconds):
    valid = False
    try:
        valid = type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0
    except (OverflowError, ValueError):
        pass
    if not valid:
        raise _invalid()
    value = _Budget(seconds)
    value.raise_if_exhausted()
    return value


def _uid(value):
    if type(value) is not str or not _UID.fullmatch(value):
        raise _invalid()
    return value


def _name(value, *, maximum=256):
    value = _text(value, maximum)
    if type(value) is not str or any(c.isspace() for c in value) or any(c in value for c in '/\\%*?'):
        raise _invalid()
    return value


def _scope(owner, subpath, env):
    owner = _uid(owner)
    subpath = _path(subpath, root=True)
    if env != 'prod' and (any(c.isspace() for c in subpath) or '..' in subpath
                          or any(c in subpath for c in '*?')):
        raise _invalid()
    key = 'swe/user-data/users/' + owner + '/' + subpath
    if len(key.encode('utf-8')) > 1023:
        raise _invalid()
    return env + '/' + owner + ('/' + subpath if subpath else '')


def _principal(value, principal_type):
    if principal_type not in ('user', 'user_group') or type(principal_type) is not str:
        raise _invalid()
    return _uid(value) if principal_type == 'user' else _name(value)


def _role(value, *, grant=False):
    if type(value) is not str:
        raise _invalid()
    if value in _ROLES:
        return _ROLES[value]
    if not grant:
        return _full_role_id(value)
    raise _invalid()


def _full_role_id(value):
    # Response identities must already be full IDs. Command aliases are mapped
    # only by _role before a request, never while validating an observed row.
    value = _name(value)
    if ':' in value or re.fullmatch(r'role-[0-9a-z]{1,128}', value):
        return value
    raise _invalid()


def _supported(transport, name, *args, **kwargs):
    """Check ABI before IO; never retry a call after a TypeError."""
    method = getattr(transport, name, None)
    valid = False
    try:
        if callable(method):
            inspect.signature(method).bind(*args, **kwargs)
            valid = True
    except (TypeError, ValueError):
        pass
    if not valid:
        raise SchemaError('user-data ACL requires bounded metadata-aware transport')
    return method


def _call(method, budget, *args, **kwargs):
    budget.raise_if_exhausted()
    safe = None
    try:
        result = method(*args, timeout=budget.remaining_seconds(), **kwargs)
    except RequestDeadlineExceeded:
        safe = RequestDeadlineExceeded('user-data ACL deadline exhausted')
    except TransportError as error:
        status = error.status if type(error.status) is int and 100 <= error.status <= 599 else None
        code = error.biz_code if type(error.biz_code) is int else None
        kind = UserDataACLUnauthorized if code in (94022, 10003) or (code is None and status in (401, 403)) else TransportError
        safe = kind('user-data ACL control request failed', status=status, biz_code=code, data={})
    except (TimeoutError, ConnectionError):
        safe = TransportError('user-data ACL network outcome unknown', data={})
    except Exception:
        safe = _invalid()
    if safe is not None:
        # No raw exception object, URL/body, cause or context leaves this boundary.
        raise safe
    budget.raise_if_exhausted()
    return result


@dataclass(frozen=True)
class UserDataACLBinding:
    scope: str
    resource_type: str
    resource_id: str
    principal_type: str
    principal_id: str
    role_id: str
    added_by: str
    added_at: str
    principal_name: str = ''
    principal_realname: str = ''

    def to_dict(self):
        value = asdict(self)
        for name in ('principal_name', 'principal_realname'):
            if not value[name]:
                value.pop(name)
        return value


@dataclass(frozen=True)
class UserDataACLPage:
    resource_id: str
    page: int
    page_size: int
    total: int
    bindings: tuple[UserDataACLBinding, ...]

    @property
    def complete(self):
        return self.page * self.page_size >= self.total


def _binding(value, resource):
    fields = set(UserDataACLBinding.__dataclass_fields__)
    required = fields - {'principal_name', 'principal_realname'}
    if (type(value) is not dict or not required <= set(value)
            or not set(value) <= fields | {'workspace_id'}
            or value.get('workspace_id', '') != ''
            or value['scope'] != 'resource' or value['resource_type'] != 'user_data'
            or value['resource_id'] != resource):
        raise _invalid()
    _principal(value['principal_id'], value['principal_type'])
    _full_role_id(value['role_id'])
    _uid(value['added_by'])
    _timestamp(value['added_at'])
    for name in ('principal_name', 'principal_realname'):
        if name in value:
            _text(value[name], 1024, empty=True)
    return UserDataACLBinding(**{k: v for k, v in value.items() if k in fields})


def _identity(binding):
    return (binding.principal_type, binding.principal_id, binding.role_id)


def _time(binding):
    return datetime.fromisoformat(binding.added_at.replace('Z', '+00:00'))


class _UserDataACLControlClient:
    def __init__(self, transport, *, storage_env):
        if type(storage_env) is not str or storage_env not in _LEGACY_ENVS | {'prod'}:
            raise _invalid()
        self._transport = transport
        self._env = storage_env

    def _request(self, method, path, body, budget, *, mutate=False):
        fn = _supported(self._transport, 'request', method, path, body,
            idempotent=not mutate, timeout=1.0)
        return _call(fn, budget, method, path, body, idempotent=not mutate)

    def grant(self, *, owner, principal, role, principal_type='user', subpath='', deadline=30.0):
        budget = _budget(deadline)
        resource = _scope(owner, subpath, self._env)
        body = dict(scope='resource', resource_type='user_data', resource_id=resource,
            principal_type=principal_type, principal_id=_principal(principal, principal_type), role_id=_role(role, grant=True))
        result = self._request('POST', _BASE, body, budget, mutate=True)
        binding = _binding(result, resource)
        if any(getattr(binding, key) != value for key, value in body.items()):
            raise _invalid()
        budget.raise_if_exhausted()
        return binding

    def revoke(self, *, owner, principal, role='reader', principal_type='user', subpath='', deadline=30.0):
        budget = _budget(deadline)
        query = dict(scope='resource', resource_type='user_data', resource_id=_scope(owner, subpath, self._env),
            principal_type=principal_type, principal_id=_principal(principal, principal_type), role_id=_role(role))
        result = self._request('DELETE', _BASE + '?' + urlencode(query), None, budget, mutate=True)
        if result is not None:
            raise _invalid()
        budget.raise_if_exhausted()

    def _page(self, resource, page, page_size, budget):
        if type(page) is not int or not 1 <= page <= _MAX_PAGES or type(page_size) is not int or not 1 <= page_size <= _PAGE_SIZE:
            raise _invalid()
        query = dict(scope='resource', resource_type='user_data', resource_id=resource, page=page, page_size=page_size)
        path = _BASE + '?' + urlencode(query)
        fn = _supported(self._transport, 'request_with_meta', 'GET', path, timeout=1.0)
        response = _call(fn, budget, 'GET', path)
        if type(response) is not tuple or len(response) != 2:
            raise _invalid()
        rows, meta = response
        if (type(rows) is not list or len(rows) > page_size or type(meta) is not dict
                or set(meta) != {'total', 'page', 'pageSize'}
                or any(type(meta[k]) is not int for k in meta)
                or meta['total'] < 0 or meta['page'] != page or meta['pageSize'] != page_size):
            raise _invalid()
        total = meta['total']
        if total > _MAX_ROWS or total > _MAX_PAGES * page_size:
            raise UserDataACLIncomplete('user-data ACL traversal exceeds bound')
        if len(rows) != min(page_size, max(0, total - (page - 1) * page_size)):
            raise UserDataACLIncomplete('user-data ACL page is incomplete')
        values = tuple(_binding(row, resource) for row in rows)
        if len(set(_identity(b) for b in values)) != len(values):
            raise UserDataACLIncomplete('user-data ACL traversal changed')
        if any(_time(a) < _time(b) for a, b in zip(values, values[1:])):
            raise UserDataACLIncomplete('user-data ACL order changed')
        budget.raise_if_exhausted()
        return UserDataACLPage(resource, page, page_size, total, values)

    def list_page(self, *, owner, subpath='', page=1, page_size=200, deadline=30.0):
        budget = _budget(deadline)
        return self._page(_scope(owner, subpath, self._env), page, page_size, budget)

    def list_all(self, *, owner, subpath='', deadline=30.0):
        budget = _budget(deadline)
        resource = _scope(owner, subpath, self._env)
        results, seen, total, prior_time = [], set(), None, None
        for page in range(1, _MAX_PAGES + 1):
            current = self._page(resource, page, _PAGE_SIZE, budget)
            if total is not None and current.total != total:
                raise UserDataACLIncomplete('user-data ACL total changed')
            total = current.total
            for binding in current.bindings:
                identity = _identity(binding)
                stamp = _time(binding)
                if identity in seen or (prior_time is not None and prior_time < stamp):
                    raise UserDataACLIncomplete('user-data ACL traversal changed')
                seen.add(identity)
                results.append(binding)
                prior_time = stamp
            if current.complete:
                if len(results) != total:
                    raise UserDataACLIncomplete('user-data ACL traversal is incomplete')
                budget.raise_if_exhausted()
                return tuple(results)
        raise UserDataACLIncomplete('user-data ACL traversal exceeds bound')

    def permissions(self, *, owner, subpath='', deadline=30.0):
        budget = _budget(deadline)
        query = dict(resource_type='user_data', resource_id=_scope(owner, subpath, self._env))
        result = self._request('GET', '/apis/v1/me/resource-permissions?' + urlencode(query), None, budget)
        if (type(result) is not dict or set(result) != {'actions'} or type(result['actions']) is not list
                or any(type(a) is not str or a not in ('get', 'use', 'assign') for a in result['actions'])
                or len(set(result['actions'])) != len(result['actions'])):
            raise _invalid()
        budget.raise_if_exhausted()
        return tuple(result['actions'])


class UserDataACLClient(_UserDataACLControlClient):
    """Canonical prod-only ACL controls over an actual authenticated transport."""
    def __init__(self, transport):
        super().__init__(transport, storage_env='prod')
