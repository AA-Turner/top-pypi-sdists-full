"""FORCING GUARD — a test stand-in must never permanently own a production table.

THE DEFECT THIS EXISTS FOR (measured 2026-09-17)
------------------------------------------------
``matrx_ai.persistence.registry._tables`` is a PROCESS-GLOBAL dict and
``register_table`` is FIRST-WRITER-WINS by design: a conflicting registration
is refused with a banner and *"the original registration remains
authoritative"*. Correct for a host, which wires the package once.

Under pytest it is a landmine. ``test_chat_door_declares_actor.py`` leg 1
bound a package-shaped stand-in (``_PackageMessage``, which has no
``bulk_create``) under the REAL key ``chat.message`` and nothing put it back.
Leg 2 of the same file — and every later test in the process that flushed a
``chat.message`` op — then got the stub instead of the Model:

    pytest .../test_chat_door_declares_actor.py::test_the_flush_...  -> passed
    pytest .../test_chat_door_declares_actor.py                      -> FAILED
    pytest packages/matrx-ai/tests                                   -> FAILED
        AttributeError: type object '_PackageMessage' has no attribute 'bulk_create'

That is the worst shape a persistence bug can take: the ops are not written,
the Coordinator reports ``ops_lost``, and the test that caused it passes.

THE FIX IS THE CLASS, not that one call site:
``registry.override_table(...)`` is the sanctioned scoped bind — it restores
the previous binding (or its absence) on exit — and
``registry.stand_ins_left_registered()`` names every registered table whose
bound class cannot actually write. The third test below is the census.

GUT CHECK: change ``_bind_package_message_model`` in
``test_chat_door_declares_actor.py`` back to a plain ``register_table`` and
both the census test here and that file's leg 2 go red.
"""

from __future__ import annotations

from matrx_ai.persistence import registry

# A key nothing else uses, so these tests cannot be the thing that poisons the
# suite they are guarding.
_SCRATCH_KEY = "public.registry_isolation_scratch"


class _ScratchMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "registry_isolation_scratch"
    db_schema = "public"


class _StandIn:
    """Deliberately missing ``bulk_create`` — exactly like ``_PackageMessage``."""

    _meta = _ScratchMeta()


class _OtherStandIn:
    _meta = _ScratchMeta()


def test_override_table_restores_the_previous_binding() -> None:
    registry.register_table(_SCRATCH_KEY, _StandIn)
    assert registry.all_registered()[_SCRATCH_KEY] is _StandIn

    with registry.override_table(_SCRATCH_KEY, _OtherStandIn):
        assert registry.all_registered()[_SCRATCH_KEY] is _OtherStandIn, (
            "override_table must actually displace the first-writer binding — "
            "that is the whole point of it"
        )

    assert registry.all_registered()[_SCRATCH_KEY] is _StandIn, (
        "override_table left its stand-in behind; a scoped bind that does not "
        "unbind is the defect it exists to prevent"
    )


def test_override_table_unbinds_a_key_that_was_not_registered_before() -> None:
    key = "public.registry_isolation_never_registered"
    assert not registry.is_registered(key)
    with registry.override_table(key, _StandIn):
        assert registry.is_registered(key)
    assert not registry.is_registered(key), (
        "a key that did not exist before the block must not exist after it"
    )


def test_no_stand_in_owns_a_real_chat_table() -> None:
    """The census: no production ``chat.*`` key may be bound to a non-writable class.

    ``chat.*`` is what the Coordinator actually flushes for a live request, so a
    stand-in parked there silently loses a user's writes for the rest of the
    process. Order-sensitive on purpose — in a full-suite run it sees every
    test that ran before it, which is exactly the leak it is hunting.
    """
    leaked = {
        table: cls_name
        for table, cls_name in registry.stand_ins_left_registered().items()
        if table.startswith("chat.")
    }
    assert not leaked, (
        f"a test stand-in permanently owns a live Coordinator table: {leaked}. "
        "The registry is first-writer-wins, so the real Model can never take "
        "the key back in this process and every later flush of that table "
        "reports ops_lost. Bind stand-ins with "
        "registry.override_table(...), never register_table(...)."
    )
