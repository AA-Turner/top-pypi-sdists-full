"""A swap value that also sits INSIDE a swap key is not a leak: keys are what persistence stores.

The reverse swap puts each key back where its value was on the wire. When one swap's key carries
another swap's value (a reference fence whose text names the very string a sibling fence resolves
to), the restored key re-introduces that value, and the survival check dropped the whole snapshot
as "a swapped value survived the reverse swap" (system_error kind request_snapshot_dropped,
mandate conversation.label_agent_run, 2026-11-10). The per-value ``str.replace`` loop also
re-scanned keys it had just restored and mangled them. One pass, then a check that ignores what
sits inside the restored keys, fixes both.
"""

from matrx_ai.config.picklist_runtime import redact_wire_payload, set_wire_swaps

TITLE = "Quarterly revenue review for Acme"  # 33 chars, like the captured row
SHORT = "a short value, 20ch"  # >= 16 chars, shorter than TITLE
KEY_NAMING_TITLE = '```matrx\n{"ref":"record","label":"' + TITLE + '"}\n```'
KEY_TITLE = '```matrx\n{"ref":"record","field":"title"}\n```'


def _msg(text: str) -> dict:
    return {"messages": [{"role": "user", "content": text}]}


def test_a_restored_key_that_names_a_longer_value_keeps_the_payload():
    # TITLE is reversed first (longest); then SHORT's key brings TITLE back inside itself.
    set_wire_swaps({KEY_NAMING_TITLE: SHORT, KEY_TITLE: TITLE})
    out = redact_wire_payload(_msg(f"A: {SHORT}\nB: {TITLE}"))
    assert out == _msg(f"A: {KEY_NAMING_TITLE}\nB: {KEY_TITLE}")


def test_a_restored_key_is_never_rewritten_by_a_shorter_value():
    whole = "Full record body that is much longer than the title, " + TITLE
    set_wire_swaps({KEY_NAMING_TITLE: whole, KEY_TITLE: TITLE})
    out = redact_wire_payload(_msg(f"A: {whole}\nB: {TITLE}"))
    assert out == _msg(f"A: {KEY_NAMING_TITLE}\nB: {KEY_TITLE}")


def test_a_short_value_that_only_sits_inside_a_restored_key_keeps_the_payload():
    # request_snapshot_dropped 2026-11-08 (value_chars=4, conversation.label_agent_run): a value too
    # short to swap (< 16 chars) that appears ONLY inside a key put back on the wire hides nothing.
    short_value = "Acme"
    key_naming_short = '```matrx\n{"ref":"record","label":"Acme"}\n```'
    key_short = '```matrx\n{"ref":"record","field":"org"}\n```'
    set_wire_swaps({key_naming_short: TITLE, key_short: short_value})
    out = redact_wire_payload(_msg(f"A: {TITLE}"))
    assert out == _msg(f"A: {key_naming_short}")


def test_a_short_value_outside_every_key_still_fails_closed():
    set_wire_swaps({KEY_TITLE: TITLE, '```matrx\n{"ref":"record","field":"org"}\n```': "Acme"})
    assert redact_wire_payload(_msg(f"A: {TITLE} at Acme")) is None
