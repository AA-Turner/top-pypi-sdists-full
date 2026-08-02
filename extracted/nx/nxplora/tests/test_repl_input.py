"""A command line can NEVER be mis-read as chat and hallucinated about.

The finding: the operator typed /message (a real command) and NX's MODEL answered "/message isn't a standard
command in NX" and fabricated "Slack or email are already wired". Root cause: the input arrived with a stray
"nx " prefix (a paste habit) / surrounding whitespace, so it didn't start with "/" and fell through to the LLM.
_normalize_repl_input closes that: it strips whitespace and a leading "nx " before a /command or $skill, so a
command always dispatches (and unknown "/x" hits the fail-closed 'unknown: … /help' guard) — never the model.

Run: python3 nx/cli/tests/test_repl_input.py   (or via the nx verify gate)
"""
import sys, os

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))   # nx/cli

import nx_cli
N = nx_cli._normalize_repl_input


def test_nx_prefix_before_a_command_is_stripped_to_the_command():
    # the exact paste that broke: "nx /message" must become "/message" so it dispatches, not chat
    assert N("nx /message") == "/message"
    assert N("nx /message imessage +15551234567") == "/message imessage +15551234567"
    assert N("NX  /help") == "/help"
    assert N("nx $analyze_best_option") == "$analyze_best_option"


def test_surrounding_whitespace_never_hides_a_command():
    assert N("  /message  ") == "/message"
    assert N("\t/help") == "/help"
    assert N("/message") == "/message"


def test_plain_chat_and_nx_as_a_word_are_left_alone():
    # 'nx ' NOT before a slash/dollar → it's real prose, untouched
    assert N("nx is my company") == "nx is my company"
    assert N("what does nx do for me") == "what does nx do for me"
    assert N("hey whattup its NX") == "hey whattup its NX"


def test_menu_sentinels_pass_through_untouched():
    for s in ("__message__telegram", "__skill__analyze", "__mode__Autopilot", "__world__sales"):
        assert N(s) == s


def test_non_string_is_returned_unchanged():
    assert N(None) is None
    assert N("") == ""


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ %s" % n)
    print("ALL REPL-INPUT PROOFS PASS")
