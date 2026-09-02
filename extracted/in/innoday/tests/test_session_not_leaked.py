"""Calling `get_session()` by hand leaks the connection. Prove it, then pin the fix.

`get_session` is a generator so FastAPI can close it when a request ends.
`next(get_session())` advances it to the `yield` and drops the generator, so the
`with Session(...)` inside never exits deterministically -- the connection goes
back to the pool only when the garbage collector finalises the generator.

On SQLite that is invisible. Behind Supabase's pooler it is a session stuck
`idle in transaction`, holding locks that make a later `ALTER`/`DROP` hang
forever rather than fail -- which is exactly what blocked the PF-399 migration
work twice (#482).

Two things are checked, because either alone is weak. The behavioural test needs
a pool that actually tracks checkouts (SQLite's default in-memory pool does
not), and the structural test needs the AST rather than a substring search --
a `grep` for the call would match this very docstring, and did on the first
attempt.
"""

import ast
import gc
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlmodel import Session


def _tracked_engine(tmp_path, name):
    """A QueuePool engine, so `checkedout()` means something.

    `create_engine("sqlite://")` uses SingletonThreadPool, which does not track
    checkouts -- the assertions below would read 0 whether or not a connection
    was leaked, and prove nothing.
    """
    return create_engine(f"sqlite:///{tmp_path / name}", poolclass=QueuePool)


class TestTheLeakIsReal:
    """Documents *why* this matters, so it cannot be mistaken for style."""

    def test_a_discarded_generator_keeps_its_connection_checked_out(self, tmp_path):
        engine = _tracked_engine(tmp_path, "leak.db")

        def gen():
            with Session(engine) as session:
                yield session

        session = next(gen())  # the broken pattern, on purpose
        session.execute(text("SELECT 1"))

        assert engine.pool.checkedout() == 1, (
            "expected the discarded generator to still hold its connection; if "
            "this reads 0, SQLAlchemy now finalises it eagerly and session_scope "
            "can be revisited"
        )

        # Only dropping the last reference and forcing collection frees it --
        # precisely the non-determinism that makes this a leak rather than a
        # slightly-late release.
        del session
        gc.collect()
        assert engine.pool.checkedout() == 0

    def test_session_scope_returns_the_connection_immediately(self, tmp_path):
        engine = _tracked_engine(tmp_path, "scoped.db")
        from contextlib import contextmanager

        @contextmanager
        def scope():
            with Session(engine) as session:
                yield session

        with scope() as session:
            session.execute(text("SELECT 1"))

        assert engine.pool.checkedout() == 0


class TestTheRootEndpointDoesNotLeak:
    """`/` is the one that mattered: every `innoday ping api` and every browser
    landing hits it, so a per-call leak compounds faster there than anywhere."""

    def test_it_no_longer_calls_the_generator_by_hand(self):
        """Structural, via the AST -- a substring search would match the prose
        explaining the bug, which is how the first version of this test failed.
        """
        import src.api.app as app_module

        tree = ast.parse(Path(app_module.__file__).read_text())
        offenders = [
            node.lineno
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "next"
            and node.args
            and isinstance(node.args[0], ast.Call)
            and getattr(node.args[0].func, "id", None) == "get_session"
        ]
        assert not offenders, (
            f"next(get_session()) at line(s) {offenders} -- use session_scope(); "
            "the generator is only closed by FastAPI's Depends machinery"
        )
