"""Bind a pack's persona slots to persona records and fixture people. See docs/exploration/personas.md.

live: account slots bind ``others`` in the order given, one per slot name (sorted) across the pack.
sim draws a different seeded set per round, so a clone that hard-codes one person fails the other rounds.
Nothing is composed: first/last name come from the record, else the name split at its first space."""

from __future__ import annotations

import hashlib
import random
from collections.abc import Sequence

from plato.personas.models import (
    WALKER_FIELDS,
    BindResult,
    FixturePerson,
    FixturePool,
    PersonaGap,
    PersonaMode,
    PersonaPack,
    PersonaRecord,
    PersonaRound,
    PersonaValues,
    SlotKind,
)


def split_name(name: str | None) -> tuple[str | None, str | None]:
    if not name or " " not in name:
        return None, None
    first, last = name.split(" ", 1)
    return first, last


def card_id(rec: PersonaRecord) -> str:
    return f"persona:{rec.login_key}/{rec.account}"


def record_values(rec: PersonaRecord) -> dict[str, str | None]:
    """The record's live values for the walker fields. Only first/last name are derived (a split of name)."""
    live = rec.live

    def val(field: str) -> str | None:
        v = getattr(live, field)
        return v.value if v is not None else None

    name = val("name")
    first, last = split_name(name)
    return {
        "name": name,
        "first_name": val("first_name") or first,
        "last_name": val("last_name") or last,
        "email": val("email"),
        "phone": val("phone"),
        "display_name": val("display_name") or name,
    }


def fixture_values(p: FixturePerson) -> dict[str, str | None]:
    return {f: getattr(p, f) for f in WALKER_FIELDS}


def bind_pack(
    pack: PersonaPack,
    pack_bytes: bytes,
    mode: PersonaMode,
    *,
    rounds: int = 3,
    acting: PersonaRecord | None = None,
    others: Sequence[PersonaRecord] = (),
    pool: FixturePool,
) -> BindResult:
    """Bind every persona slot of ``pack``. Raises ValueError when live has no acting record or the pool is short."""
    mode = PersonaMode(mode)
    if mode == PersonaMode.live and acting is None:
        raise ValueError("live mode needs the acting account's persona record")
    slots = pack.persona_slots
    people = pool.people
    out: dict[str, PersonaRound] = {}
    gaps: list[PersonaGap] = []
    for r in ["0"] if mode == PersonaMode.live else [str(i) for i in range(rounds)]:
        cards: dict[str, dict[str, str]] = {}
        values: dict[str, dict[str, dict[str, str | None]]] = {}
        # Acting and account slots are the clone's USERS: one person per slot name for the whole pack in a round,
        # so the seeded users match every story. Fixture slots are drawn per story from the rest of the pool.
        acct_kinds = (SlotKind.account,) if mode == PersonaMode.live else (SlotKind.acting, SlotKind.account)
        acct_slots = sorted({x.slot for rows in slots.values() for x in rows if x.kind in acct_kinds})
        rnd = random.Random(f"bind:{mode}:{r}:accounts")
        acct_pick = dict(zip(acct_slots, rnd.sample(people, len(acct_slots)))) if mode == PersonaMode.sim else {}
        taken = {p.card_id for p in acct_pick.values()}
        rest = [p for p in people if p.card_id not in taken]
        for sid, rows in slots.items():
            need = [x for x in rows if x.kind == SlotKind.fixture]
            rnd = random.Random(f"bind:{mode}:{r}:{sid}")
            if len(need) > len(rest):
                raise ValueError(f"{sid}: needs {len(need)} fixture people, pool has {len(rest)} left")
            pick = dict(zip([x.slot for x in need], rnd.sample(rest, len(need))))
            pick.update(acct_pick)
            cards[sid], values[sid] = {}, {}
            for x in rows:
                s = x.slot
                if mode == PersonaMode.live and x.kind == SlotKind.acting:
                    assert acting is not None
                    cards[sid][s], values[sid][s] = card_id(acting), record_values(acting)
                elif mode == PersonaMode.live and x.kind == SlotKind.account:
                    idx = acct_slots.index(s)
                    if idx < len(others):
                        cards[sid][s], values[sid][s] = card_id(others[idx]), record_values(others[idx])
                    else:
                        values[sid][s] = {f: None for f in WALKER_FIELDS}
                else:
                    cards[sid][s], values[sid][s] = pick[s].card_id, fixture_values(pick[s])
                for f in x.fields or WALKER_FIELDS:
                    if values[sid][s].get(f) is None:
                        gaps.append(PersonaGap(story_id=sid, slot=s, field=f))
        out[r] = PersonaRound(cards=cards, values=values)
    doc = PersonaValues(
        kind="persona-values", mode=mode, pack_sha256=hashlib.sha256(pack_bytes).hexdigest(), rounds=out
    )
    return BindResult(values=doc, gaps=gaps)
