"""The keys Core gives out, and whether a call of a model must carry one.

Core's own two keys (the host's programs' and its API key: serve/serve.py) open everything. The keys here are the
ones an operator makes for others, each by a name, in the console's API tab:

    api      a caller's key for calls of models (the routes Core passes on to a wrapper: relay/)
    guest    the same, ending by itself after the time it was made for
    enroll   the key a new wrapper's install carries to connect itself (POST /api/fleet/workers/connect), for a day

A key is shown once, when it is made. What is kept is its digest (hugpy_resources key_digest) and its first
characters, so a person can tell the keys apart; a key that was lost is revoked and another is made.

Whether a call must carry a key at all is one switch (the console's "require an API key for /v1 calls"), a row of
Core's settings table. It is off until an operator turns it on: Core's door is then open for calls to whoever
reaches it, and what stands in front of the door (a web front) decides who that is.
"""
from ..imports import (
    key_digest,
    new_key,
    read_settings,
    time,
    uuid,
    write_settings,
)
from .. import settings, sql

MARK = 'hk-'                      # how a key Core gave out begins
KINDS = ('api', 'guest', 'enroll')
SWITCH = 'calls_ask_key'          # the settings row of the switch
ENROLL_DAYS = 1.0                 # a key to connect a wrapper with opens for this long unless it says otherwise
USE_NOTED_S = 60                  # a key's last use is written at most this often
COLUMNS = 'id, name, kind, prefix, created_at, created_by, expires_at, last_used_at'


def shown(row: dict, now: float = None) -> dict:
    """A key as it may be shown: everything kept of it but its digest, and whether its time is over."""
    now = time.time() if now is None else now
    return dict({name: row[name] for name in COLUMNS.split(', ')},
                expired=bool(row['expires_at'] and row['expires_at'] <= now))


def listed() -> list:
    """Every key Core gave out that was not revoked, newest first."""
    now = time.time()
    return [shown(row, now) for row in sql.rows(f'SELECT {COLUMNS} FROM api_keys ORDER BY created_at DESC')]


def make(name: str, kind: str = None, expires_days: float = None, by: str = None) -> dict:
    """Make a key. Returns it as shown, with ``key``: the key itself, which is said this once and never kept.
    A request that names no kind is a wrapper's install asking for the key it connects with (enroll)."""
    kind = kind or 'enroll'
    if kind not in KINDS:
        raise ValueError(f"kind: one of {', '.join(KINDS)}")
    name = str(name or '').strip() or kind
    days = float(expires_days) if expires_days not in (None, '') else (ENROLL_DAYS if kind == 'enroll' else None)
    if kind == 'guest' and not days:
        raise ValueError('a guest pass says how long it opens for (expires_days)')
    key, prefix, digest = new_key(MARK)
    now = time.time()
    row = dict(id=uuid.uuid4().hex[:12], name=name, kind=kind, prefix=prefix, created_at=now, created_by=by,
               expires_at=now + days * 86400 if days else None, last_used_at=None)
    conn = sql.writer()
    try:
        with conn:
            conn.execute(f"INSERT INTO api_keys ({COLUMNS}, digest) VALUES (?,?,?,?,?,?,?,?,?)",
                         (*(row[name] for name in COLUMNS.split(', ')), digest))
    finally:
        conn.close()
    return dict(shown(row, now), key=key)


def revoke(key_id: str, *, install_link_only: bool = False) -> bool:
    """Revoke a key: it opens nothing from now on. Returns whether there was one."""
    conn = sql.writer()
    try:
        with conn:
            rule = " AND created_by LIKE 'install-link:%'" if install_link_only else ''
            return bool(conn.execute('DELETE FROM api_keys WHERE id = ?' + rule, (key_id,)).rowcount)
    finally:
        conn.close()


def prune(expired: bool = True, older_than_days: float = None, unused_only: bool = False) -> int:
    """Remove the keys whose time is over and, when asked, those made longer ago than ``older_than_days``
    (``unused_only``: of those, only the ones never used). Returns how many were removed."""
    now, where, params = time.time(), [], []
    if expired:
        where.append('(expires_at IS NOT NULL AND expires_at <= ?)')
        params.append(now)
    if older_than_days:
        where.append('(created_at <= ?' + (' AND last_used_at IS NULL' if unused_only else '') + ')')
        params.append(now - float(older_than_days) * 86400)
    if not where:
        return 0
    conn = sql.writer()
    try:
        with conn:
            return conn.execute('DELETE FROM api_keys WHERE ' + ' OR '.join(where), params).rowcount
    finally:
        conn.close()


def holder(given: str, kinds=KINDS):
    """The key ``given`` is, as shown, when it is one Core gave out that still opens and is of ``kinds``; else
    None. Its use is noted (at most every USE_NOTED_S: a call is not a write)."""
    given = str(given or '')
    if not given.startswith(MARK):
        return None
    now = time.time()
    found = sql.rows(f'SELECT {COLUMNS} FROM api_keys WHERE digest = ?', (key_digest(given),))
    if not found or found[0]['kind'] not in kinds or (found[0]['expires_at'] and found[0]['expires_at'] <= now):
        return None
    if now - (found[0]['last_used_at'] or 0) >= USE_NOTED_S:
        conn = sql.writer()
        try:
            with conn:
                conn.execute('UPDATE api_keys SET last_used_at = ? WHERE id = ?', (now, found[0]['id']))
        finally:
            conn.close()
    return shown(found[0], now)


def required() -> bool:
    """Whether a call of a model must carry a key."""
    return bool(read_settings(settings.database()).get(SWITCH))


def require(on: bool, by: str = None) -> bool:
    """Turn the switch. Returns how it stands."""
    write_settings(settings.database(), {SWITCH: bool(on)}, by=by)
    return required()


__all__ = ['KINDS', 'holder', 'listed', 'make', 'prune', 'require', 'required', 'revoke', 'shown']
