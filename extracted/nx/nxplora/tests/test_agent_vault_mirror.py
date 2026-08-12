"""The terminal can mirror an agent's credential into the vault — and the address must match the web's.

WHY THIS EXISTS. Supplying an agent in the terminal stores its credential in the macOS Keychain, which the
web cannot read. Without a mirror, such an agent can only ever send FROM the terminal: the web shows the
binding and then sends as Nexplora, which is honest but is not what the operator asked for.

THE ADDRESS IS THE WHOLE RISK. Both sides derive `agent:<agent_id>` independently — Python here,
TypeScript in lib/channels/adapters/agent-credential-scope.ts. A mismatch would NOT error. The vault write
would succeed, the web's lookup would miss, and the web would quietly fall back to sending as Nexplora
while the operator believed they had just fixed exactly that. Silent, and indistinguishable from having
never mirrored at all.

So the string is pinned here and on the other side, and the CLI-slug-IS-agent_id fact it rests on is
pinned too.

Run: python3 -m pytest nx/cli/tests/test_agent_vault_mirror.py
"""
import io
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLI = os.path.dirname(_HERE)
sys.path.insert(0, _CLI)

import nx_cli


def test_scope_matches_the_web_derivation():
    # lib/channels/adapters/agent-credential-scope.ts:
    #   export const agentChannelScope = (agentId: string): string => `agent:${agentId}`
    assert nx_cli._agent_vault_scope("vinny") == "agent:vinny"
    assert nx_cli._agent_vault_scope("a-1") == "agent:a-1"


def test_scope_is_namespaced_away_from_the_operators_own_grant():
    # The operator's own Telegram grant and an agent's bot token are both "telegram" credentials in the
    # vault; only the scope separates them. An unnamespaced scope would let them overwrite each other,
    # and the symptom — messages from the wrong identity — is not one anybody traces to a scope string.
    assert nx_cli._agent_vault_scope("vinny").startswith("agent:")
    assert nx_cli._agent_vault_scope("vinny") != "telegram"


def test_two_agents_never_share_an_address():
    assert nx_cli._agent_vault_scope("a-1") != nx_cli._agent_vault_scope("a-2")


def test_prefixes_are_not_matches():
    # agent:a-1 and agent:a-11 are different agents. The web verifies with an exact `includes`, so this
    # only holds if the strings genuinely differ.
    assert nx_cli._agent_vault_scope("a-1") != nx_cli._agent_vault_scope("a-11")


def _mirror_src() -> str:
    src = io.open(os.path.join(_CLI, "nx_cli.py"), encoding="utf-8").read()
    start = src.index("def _mirror_agent_secret_to_vault(")
    return src[start : src.index("\ndef ", start + 10)]


def test_the_mirror_is_opt_in_and_defaults_to_no():
    # Everything else /supply stores stays on this machine. Mirroring puts a secret on the network, which
    # is a change in posture rather than an implementation detail — so it is asked, and the default is no.
    body = _mirror_src()
    assert "_choose(" in body, "the operator must be asked"
    assert "current=0" in body, "and the default must be the local-only option"
    assert re.search(r'\("No', body), "the first (default) option must be the refusal"
    assert "_pick != 1" in body, "anything but an explicit yes keeps it local"


def test_a_refusal_says_nothing_left_the_machine():
    assert "nothing left this machine" in _mirror_src()


def test_the_keychain_copy_is_kept_either_way():
    # This ADDS a home; it does not move the credential. The terminal must keep working even if the vault
    # is unreachable — otherwise a network blip would take away the capability that already worked.
    body = _mirror_src()
    assert "kept local only" in body, "a vault failure must say the local copy stands"
    assert "still send as this agent" in body, "and that the terminal is unaffected"


def test_every_failure_is_named_rather_than_swallowed():
    # The Keychain write already succeeded by this point, so a silent vault failure would leave the
    # operator believing they had done something they had not.
    body = _mirror_src()
    for expected in ["Couldn't store it in the vault", "returned no reference", "Couldn't reach the vault"]:
        assert expected in body, f"unhandled failure path: {expected}"


def test_not_signed_in_is_a_plain_answer_not_an_error():
    assert "no vault to store it in" in _mirror_src()


def test_the_mirror_is_only_offered_after_a_successful_local_store():
    # Mirroring a credential we failed to keep locally would leave a vault copy and a terminal that
    # cannot send — the exact inverse of the problem this solves.
    src = io.open(os.path.join(_CLI, "nx_cli.py"), encoding="utf-8").read()
    # CALL sites only — `def _mirror_agent_secret_to_vault(cfg, ...` matches the same text, and asserting
    # against the definition would have this fail on correct code.
    calls = [m for m in re.finditer(r"(?<!def )_mirror_agent_secret_to_vault\(cfg", src)]
    assert len(calls) >= 3, f"expected the mirror on every secret-storing channel, found {len(calls)}"
    for m in calls:
        preceding = src[max(0, m.start() - 400) : m.start()]
        assert "if stored:" in preceding, "the mirror must be gated on the Keychain store succeeding"


def test_the_mirror_never_prints_the_credential():
    # A secret in terminal scrollback is a secret in a screenshot.
    body = _mirror_src()
    for line in body.split("\n"):
        if "print(" in line:
            assert "value" not in line, f"a print references the credential: {line.strip()}"
