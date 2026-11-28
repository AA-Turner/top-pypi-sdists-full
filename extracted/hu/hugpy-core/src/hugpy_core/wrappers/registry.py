"""The saved connections: the wrappers table of Core's database.

A wrapper is known by the name it gives itself (its /health "worker"). What is saved is where it is reached, its
API key (a linked wrapper's link secret), whether it connects out (link) and the operator's switch (connected).
A saved connection that is switched off keeps its address and key: switching it on again is one step, never a
new enrollment. The key is never published: public() is what leaves this module for a screen.
"""
from ..imports import (
    json,
    time,
)
from .. import sql

COLUMNS = ('name', 'url', 'key', 'link', 'connected', 'added_at', 'changed_at', 'added_by')


def saved() -> list:
    """Every saved connection, by name (each with its key: for the parts of Core that ask the wrapper)."""
    return sql.rows(f"SELECT {', '.join(COLUMNS)} FROM wrappers ORDER BY name")


def get(name: str):
    found = sql.rows(f"SELECT {', '.join(COLUMNS)} FROM wrappers WHERE name = ?", (name,))
    return found[0] if found else None


def connected() -> list:
    """The saved connections that are switched on."""
    return [row for row in saved() if row['connected']]


def public(row: dict) -> dict:
    """A connection as it may be shown: everything but its key."""
    return {key: value for key, value in row.items() if key != 'key'}


def save(name: str, url: str, key: str = '', link: bool = False, by: str = None) -> dict:
    """Save a connection, switched on. One already saved under the name takes the new address; its key is kept
    when none is given (unless it changes between direct and linked: a link secret is no API key)."""
    now = time.time()
    conn = sql.writer()
    try:
        with conn:
            conn.execute(
                "INSERT INTO wrappers (name, url, key, link, connected, added_at, changed_at, added_by) "
                "VALUES (?, ?, ?, ?, 1, ?, ?, ?) ON CONFLICT(name) DO UPDATE SET url = excluded.url, "
                "key = CASE WHEN excluded.key = '' AND wrappers.link = excluded.link THEN wrappers.key ELSE excluded.key END, "
                "link = excluded.link, "
                "connected = 1, changed_at = excluded.changed_at",
                (name, url.rstrip('/'), key or '', int(bool(link)), now, now, by))
    finally:
        conn.close()
    return get(name)


def switch(name: str, on: bool):
    """Switch a saved connection off or on. Returns it as it is now, or None when there is none of that name."""
    conn = sql.writer()
    try:
        with conn:
            conn.execute("UPDATE wrappers SET connected = ?, changed_at = ? WHERE name = ?", (int(bool(on)), time.time(), name))
    finally:
        conn.close()
    return get(name)


def set_wildcard(name: str, on: bool, by: str = None):
    """Say whether Core's own choice of a host may take this wrapper (the console's "wildcard"): on, a call of
    any model it can run may be sent to it; off, Core uses its routing allocations. Returns how it stands now, or None
    when there is no saved connection of that name."""
    if get(name) is None:
        return None
    conn = sql.writer()
    try:
        with conn:
            conn.execute("INSERT INTO wrapper_routing (name, wildcard, changed_at, changed_by) VALUES (?, ?, ?, ?) "
                         "ON CONFLICT(name) DO UPDATE SET wildcard = excluded.wildcard, changed_at = excluded.changed_at, "
                         "changed_by = excluded.changed_by", (name, int(bool(on)), time.time(), by))
    finally:
        conn.close()
    return wildcard(name)


def wildcard(name: str) -> bool:
    """Whether Core's own choice of a host may take this wrapper: as the operator said, else yes."""
    found = sql.rows("SELECT wildcard FROM wrapper_routing WHERE name = ?", (name,))
    return bool(found[0]['wildcard']) if found else True


def model_routes() -> list:
    return sql.rows("SELECT wrapper, model, explicit, pinned FROM wrapper_model_routes ORDER BY wrapper, model")


def clear_unpinned_routes() -> None:
    conn = sql.writer()
    try:
        with conn:
            conn.execute("DELETE FROM wrapper_model_routes WHERE pinned = 0")
    finally:
        conn.close()


def record_route(name: str, model: str, explicit: bool = False) -> bool:
    """Create a routing allocation. Observing a call preserves an existing operator choice and pin."""
    conn = sql.writer()
    try:
        with conn:
            return bool(conn.execute(
                "INSERT INTO wrapper_model_routes (wrapper, model, explicit) "
                "SELECT name, ?, ? FROM wrappers WHERE name = ? "
                "ON CONFLICT(wrapper, model) DO UPDATE SET explicit = max(explicit, excluded.explicit)",
                (model, int(explicit), name)).rowcount)
    finally:
        conn.close()


def remove_route(name: str, model: str) -> bool:
    conn = sql.writer()
    try:
        with conn:
            return bool(conn.execute("DELETE FROM wrapper_model_routes WHERE wrapper = ? AND model = ? AND pinned = 0",
                                     (name, model)).rowcount)
    finally:
        conn.close()


def pin_route(name: str, model: str, pinned: bool) -> bool:
    conn = sql.writer()
    try:
        with conn:
            return bool(conn.execute("UPDATE wrapper_model_routes SET pinned = ? WHERE wrapper = ? AND model = ?",
                                     (int(pinned), name, model)).rowcount)
    finally:
        conn.close()


def model_blocks() -> list:
    return sql.rows("SELECT wrapper, model FROM wrapper_model_blocks ORDER BY wrapper, model")


def set_model_block(name: str, model: str, blocked: bool) -> None:
    conn = sql.writer()
    try:
        with conn:
            if blocked:
                conn.execute("INSERT OR IGNORE INTO wrapper_model_blocks (wrapper, model) "
                             "SELECT name, ? FROM wrappers WHERE name = ?", (model, name))
            else:
                conn.execute("DELETE FROM wrapper_model_blocks WHERE wrapper = ? AND model = ?", (name, model))
    finally:
        conn.close()


def model_static(name: str = None) -> list:
    if name is None:
        return sql.rows("SELECT wrapper, model, enabled FROM wrapper_model_static ORDER BY wrapper, model")
    return sql.rows("SELECT model, enabled FROM wrapper_model_static WHERE wrapper = ? ORDER BY model", (name,))


def set_model_static(name: str, model: str, enabled: bool) -> bool:
    conn = sql.writer()
    try:
        with conn:
            return bool(conn.execute(
                "INSERT INTO wrapper_model_static (wrapper, model, enabled) "
                "SELECT name, ?, ? FROM wrappers WHERE name = ? "
                "ON CONFLICT(wrapper, model) DO UPDATE SET enabled = excluded.enabled",
                (model, int(enabled), name)).rowcount)
    finally:
        conn.close()


def context_edits(name: str) -> list:
    return sql.rows("SELECT model, patch FROM wrapper_context_edits WHERE wrapper = ? ORDER BY model", (name,))


def save_context_edit(name: str, model: str, patch: dict) -> bool:
    conn = sql.writer()
    try:
        with conn:
            return bool(conn.execute(
                "INSERT INTO wrapper_context_edits (wrapper, model, patch) "
                "SELECT name, ?, ? FROM wrappers WHERE name = ? "
                "ON CONFLICT(wrapper, model) DO UPDATE SET patch = "
                "(SELECT json_group_object(key, value) FROM ("
                "SELECT key, value FROM json_each(wrapper_context_edits.patch) "
                "WHERE key NOT IN (SELECT key FROM json_each(excluded.patch)) "
                "UNION ALL SELECT key, value FROM json_each(excluded.patch)))",
                (model, json.dumps(patch), name)).rowcount)
    finally:
        conn.close()


def clear_context_edit(name: str, model: str, patch: str) -> None:
    conn = sql.writer()
    try:
        with conn:
            conn.execute("DELETE FROM wrapper_context_edits WHERE wrapper = ? AND model = ? AND patch = ?",
                         (name, model, patch))
    finally:
        conn.close()


def forget(name: str) -> bool:
    """Drop a saved connection, what the collector noted of it and the documents last read of it (how it stood:
    of a wrapper Core no longer knows, they describe nothing). Its logs stay: its calls and loads happened.
    Returns whether there was one."""
    conn = sql.writer()
    try:
        with conn:
            gone = conn.execute("DELETE FROM wrappers WHERE name = ?", (name,)).rowcount
            conn.execute("DELETE FROM collector WHERE wrapper = ?", (name,))
            conn.execute("DELETE FROM wrapper_model_routes WHERE wrapper = ?", (name,))
            conn.execute("DELETE FROM wrapper_model_blocks WHERE wrapper = ?", (name,))
            conn.execute("DELETE FROM wrapper_model_static WHERE wrapper = ?", (name,))
            conn.execute("DELETE FROM wrapper_context_edits WHERE wrapper = ?", (name,))
            conn.execute("DELETE FROM wrapper_routing WHERE name = ?", (name,))
            conn.execute("DELETE FROM wrapper_documents WHERE wrapper = ?", (name,))
    finally:
        conn.close()
    return bool(gone)


def status() -> list:
    """Every saved connection with how it stands (the wrapper_status view): never a key."""
    return sql.rows("SELECT * FROM wrapper_status ORDER BY name")
