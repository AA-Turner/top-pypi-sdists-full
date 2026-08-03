"""The three-direction proof: /supply · /channels · /publish mean ONE thing each.

The CLI used to spend the word "channels" on PUBLISHING (Meta · Google · TikTok ·
LinkedIn · X) while the web has always used it for the opposite direction — the
ways to reach Nexplora. Whichever surface an operator learned second actively
misled them, which is worse than either name alone: not a gap, a contradiction.

    /supply    the AGENT gets its own account, and NX sends AS that agent
    /channels  how NX reaches YOU, besides this terminal and the web app
    /publish   posting OUT to an audience              (this was /channels)

These pin the split so it cannot quietly regress, and they pin the two failure
modes this rename could introduce, both of which are SILENT:

  1. Palette↔dispatch drift. The slash picker returns the raw command string and
     the REPL matches it with ==. Rename one side only and selecting the entry
     falls through to the model as chat — no error anywhere.
  2. The 10th /supply item. prompt_toolkit raises on kb.add("10"), and /supply's
     caller wraps the picker in a bare `except Exception` — so a 10th entry does
     not traceback, it makes /supply print nothing at all.

Run: python3 -m pytest nx/cli/tests/test_channels_publish_split.py
"""
import io
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLI = os.path.dirname(_HERE)
sys.path.insert(0, _CLI)

import nx_slash_menu
import nx_cli


def _menu_commands():
    return [c["cmd"] for c in nx_slash_menu.SECTIONS[0]["commands"]]


def _help_commands():
    return [cmd for _heading, cmds in nx_cli.HELP_GROUPS for cmd, _desc in cmds]


# ── the three directions exist, and are three ───────────────────────────────
def test_all_three_directions_are_reachable_commands():
    menu, helps = _menu_commands(), _help_commands()
    for cmd in ("/supply", "/channels", "/publish"):
        assert cmd in menu, f"{cmd} missing from the slash menu"
        assert cmd in helps, f"{cmd} missing from /help"


def test_publish_is_the_publishing_surface_and_channels_is_not():
    """The descriptions carry the meaning — an operator reads these, not the code."""
    desc = {c["cmd"]: c["desc"].lower() for c in nx_slash_menu.SECTIONS[0]["commands"]}
    assert "publish" in desc["/publish"], "/publish must say it publishes"
    assert "publish" not in desc["/channels"], (
        "/channels must NOT describe publishing — that is the collision this split removed"
    )
    assert "reach" in desc["/channels"], "/channels must say it is about reaching NX"


# ── palette ↔ dispatch: the silent-failure guard ────────────────────────────
def _repl_source():
    return io.open(os.path.join(_CLI, "nx_cli.py"), encoding="utf-8").read()


def test_every_menu_command_has_a_repl_dispatch_branch():
    """A menu entry with no matching branch is selectable and does nothing.

    Matches the two real dispatch shapes: `cmd=="/x"` and `cmd in ("/x", ...)`.
    """
    src = _repl_source()
    for cmd in ("/channels", "/publish", "/supply", "/go"):
        single = re.search(r'cmd\s*==\s*["\']' + re.escape(cmd) + r'["\']', src)
        grouped = re.search(r'cmd\s+in\s*\([^)]*["\']' + re.escape(cmd) + r'["\']', src)
        assert single or grouped, f"{cmd} is in the menu but the REPL never dispatches it"


def test_the_old_publish_command_no_longer_dispatches_as_publish():
    """/channels must route to the reach hub, not to the publish picker.

    Proven structurally: the publish picker's only caller is the /publish branch.
    """
    src = _repl_source()
    assert "run_publish_menu" in src, "the publish picker should be run_publish_menu now"
    assert "run_channels_menu" not in src, (
        "run_channels_menu still referenced — the picker rename is half-applied"
    )
    # The /channels branch calls the reach hub. Window is generous on purpose: the branch also handles the
    # "typed the old publish syntax" case, and a tight window made this assert fail on a comment growing.
    branch = src.split('if cmd=="/channels":', 1)
    assert len(branch) == 2, "/channels has no dispatch branch"
    assert "_run_channels" in branch[1][:1600], "/channels must route to the reach hub"


# ── the 10th /supply item: the silent-crash guard ───────────────────────────
def test_no_picker_registers_a_two_digit_jump_key():
    """Every kb.add jump loop must be bounded at 9. There is no key "10"."""
    src = io.open(os.path.join(_CLI, "nx_slash_menu.py"), encoding="utf-8").read()
    unbounded = re.findall(r"for\s+_i\s+in\s+range\(len\((\w+)\)\):\s*\n\s*kb\.add\(", src)
    assert not unbounded, (
        "unbounded jump-key loop over "
        + ", ".join(unbounded)
        + " — prompt_toolkit raises on kb.add('10') and /supply swallows it, so the "
          "picker would silently render nothing. Bound with min(9, len(...))."
    )


def test_supply_menu_stays_within_reach_of_its_jump_keys():
    """Items past 9 are arrow-reachable, not jump-reachable — say so out loud.

    Not a cap on the list; a check that the footer does not promise a key that is
    not bound. If /supply grows past 9, the '1-9' hint has to stop claiming to
    cover everything.
    """
    n = len(nx_slash_menu._SUPPLY_ITEMS)
    src = io.open(os.path.join(_CLI, "nx_slash_menu.py"), encoding="utf-8").read()
    footer = re.search(r'give an agent its own channel · ([^·]+) ·', src)
    assert footer, "the /supply footer hint moved — re-pin it"
    if n > 9:
        assert "1-9" in footer.group(1), (
            f"/supply has {n} items but the footer promises "
            f"'{footer.group(1).strip()}' — only 1-9 are bound"
        )


# ── the reach hub reports real state, never a flattering guess ──────────────
def _run_channels_capture(states, pick_ret="n"):
    """Run _run_channels against a stubbed nx_message.channels_state."""
    import builtins
    import contextlib
    import nx_message

    orig_state = nx_message.channels_state
    orig_input = builtins.input
    nx_message.channels_state = lambda cfg=None: states
    builtins.input = lambda *a, **k: pick_ret
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            nx_cli._run_channels({})
    finally:
        nx_message.channels_state = orig_state
        builtins.input = orig_input
    return buf.getvalue()


def _blank():
    return {c: {"configured": False, "active": False} for c in
            ("telegram", "email", "imessage", "whatsapp", "sms")}


def test_nothing_linked_says_so_plainly():
    out = _run_channels_capture(_blank())
    assert "not linked" in out
    assert "Nothing linked yet" in out


def test_a_linked_channel_shows_its_address():
    # Email, which genuinely stores its address under "to". The telegram case lives in its own test below,
    # because telegram is the ONE channel that does not — and this test previously used a hand-invented
    # {"to": ...} telegram entry, a shape channels_state cannot produce, so it was green against a real bug.
    st = _blank()
    st["email"] = {"configured": True, "active": True, "to": "vic@example.com"}
    out = _run_channels_capture(st)
    assert "vic@example.com" in out, "the linked address is the proof — show it"
    assert "linked" in out


def test_configured_but_muted_is_not_reported_as_simply_linked():
    """configured-and-off is a real, distinct state. Calling it 'linked' overstates
    a channel NX will not actually use."""
    st = _blank()
    st["email"] = {"configured": True, "active": False, "to": "vic@example.com"}
    out = _run_channels_capture(st)
    assert "muted" in out, "a configured-but-inactive channel must not read as plain 'linked'"


def test_the_reach_hub_never_offers_publishing():
    """/channels is one direction. If publishing leaks back into it, the whole
    rename was pointless."""
    out = _run_channels_capture(_blank())
    for word in ("Meta", "TikTok", "LinkedIn", "Publish", "publish"):
        assert word not in out, f"the reach surface must not mention {word!r}"


# ── /supply: the CLI ↔ web mirror ────────────────────────────────────────────
# The picker is NUMBERED, so operators read it positionally. If the two surfaces disagree about the order,
# "press 7" means different things depending on which one you learned — the exact class of contradiction
# the /channels rename existed to remove, reintroduced one layer down.

_WEB_SUPPLY_ORDER = [
    # lib/desk/supply-channels.ts SUPPLY_CHANNELS, in order.
    "email", "telegram", "sms", "whatsapp", "imessage", "discord",
    "x", "facebook", "instagram", "linkedin", "tiktok", "youtube", "pinterest",
]


def test_supply_channels_match_the_web_exactly_and_in_order():
    cli = [i["cmd"] for i in nx_slash_menu._SUPPLY_ITEMS if i.get("kind") != "manage"]
    assert cli == _WEB_SUPPLY_ORDER, (
        "the CLI /supply picker has drifted from lib/desk/supply-channels.ts.\n"
        f"  cli: {cli}\n  web: {_WEB_SUPPLY_ORDER}"
    )


def test_the_manage_rows_come_last():
    kinds = [i.get("kind") for i in nx_slash_menu._SUPPLY_ITEMS]
    first_manage = kinds.index("manage")
    assert all(k == "manage" for k in kinds[first_manage:]), "Active/Revoke must be the tail, not interleaved"


def test_publishing_is_grouped_after_conversation():
    kinds = [i.get("kind") for i in nx_slash_menu._SUPPLY_ITEMS if i.get("kind") != "manage"]
    first_pub = kinds.index("publishing")
    assert first_pub > 0
    assert all(k == "publishing" for k in kinds[first_pub:]), "the two groups have interleaved"


def test_every_supply_entry_has_a_dispatch_arm():
    """A menu entry with no arm in _handle_supply is a SILENT no-op — the picker closes and nothing
    happens, which an operator cannot distinguish from having cancelled."""
    src = io.open(os.path.join(_CLI, "nx_cli.py"), encoding="utf-8").read()
    body = src.split("def _handle_supply(", 1)
    assert len(body) == 2, "_handle_supply not found"
    body = body[1].split("\ndef ", 1)[0]
    for it in nx_slash_menu._SUPPLY_ITEMS:
        cmd = it["cmd"]
        direct = f'pick == "{cmd}"' in body
        # publishing channels dispatch as a group through _SUPPLY_PUBLISH
        grouped = 'pick in _SUPPLY_PUBLISH' in body and it.get("kind") == "publishing"
        assert direct or grouped, f"/supply offers '{cmd}' but _handle_supply never handles it"


def test_handle_supply_says_something_when_it_cannot_route():
    """The fallback arm. Without it the function falls off the end and returns None silently."""
    src = io.open(os.path.join(_CLI, "nx_cli.py"), encoding="utf-8").read()
    body = src.split("def _handle_supply(", 1)[1].split("\ndef ", 1)[0]
    assert "isn't wired up yet" in body, "_handle_supply has no fallback — an unrouted pick is silent"


def test_every_publishing_channel_is_declared_in_the_assign_table():
    import nx_cli as _c
    declared = set(_c._SUPPLY_PUBLISH)
    offered = {i["cmd"] for i in nx_slash_menu._SUPPLY_ITEMS
               if i.get("kind") == "publishing" and i["cmd"] != "x"}
    assert offered == declared, (
        f"picker and assign table disagree — picker-only: {offered - declared}, "
        f"table-only: {declared - offered}"
    )


def test_every_supplied_channel_declares_whether_it_owns_a_keychain_secret():
    """_AGENT_CHANNEL_SECRET is read by BOTH the assign path and /revoke. A channel missing from it does
    not error — revoke simply skips deleting its token, leaving a live credential in the operator's
    Keychain for a channel they just took away. That is exactly what happened to discord and x."""
    import nx_cli as _c
    for it in nx_slash_menu._SUPPLY_ITEMS:
        if it.get("kind") == "manage":
            continue
        assert it["cmd"] in _c._AGENT_CHANNEL_SECRET, (
            f"{it['cmd']} is suppliable but absent from _AGENT_CHANNEL_SECRET — /revoke would silently "
            f"leave its credential behind"
        )


def test_publishing_channels_hold_no_per_agent_secret():
    """They use the operator's ONE platform grant from /publish. Claiming a per-agent secret would imply
    a login the platform does not offer, and would make revoke promise a deletion it cannot perform."""
    import nx_cli as _c
    for it in nx_slash_menu._SUPPLY_ITEMS:
        if it.get("kind") != "publishing" or it["cmd"] == "x":
            continue
        assert _c._AGENT_CHANNEL_SECRET[it["cmd"]] is None, (
            f"{it['cmd']} claims a per-agent Keychain secret, but /supply never asks it for one"
        )


# ── the publish-handle port: CLI must agree with the web, case for case ──────
# nx_cli._normalize_publish_handle / _publish_handle_error are a hand-port of
# lib/desk/supply-channels.ts (normalizeAddress + HANDLE_RULES + addressError). Both surfaces write to ONE
# store through ONE endpoint, and the web POST validates while the CLI's snapshot ingest does not — so a
# CLI that normalized differently could persist an address the web's own form rejects with a 400.
#
# Python cannot import the TypeScript, so THIS TABLE is the contract. Every row is also asserted against
# the web module by tests in nexplora-v2: lib/desk/supply-channels.test.ts.

# (channel, raw input, expected normalized, expect_error)
_PORT_CASES = [
    # x — 1-15, letters/numbers/underscore
    ("x", "yourcompany", "@yourcompany", False),
    ("x", "@@yourcompany", "@yourcompany", False),
    ("x", "  @acme  ", "@acme", False),
    ("x", "@a", "@a", False),
    ("x", "sixteencharacter", "@sixteencharacter", True),
    ("x", "has-a-dash", "@has-a-dash", True),
    # facebook — Page usernames are 5+ chars, letters/numbers/periods
    ("facebook", "acmepages", "@acmepages", False),
    ("facebook", "abcd", "@abcd", True),
    ("facebook", "acme_pages", "@acme_pages", True),        # underscores are not legal on FB Pages
    # instagram — up to 30
    ("instagram", "a", "@a", False),
    ("instagram", "has spaces", "@has spaces", True),
    # tiktok — 2-24
    ("tiktok", "ac", "@ac", False),
    ("tiktok", "a", "@a", True),
    # youtube — 3-30, hyphens legal
    ("youtube", "acme-co", "@acme-co", False),
    ("youtube", "ab", "@ab", True),
    # pinterest — 3-30, no periods
    ("pinterest", "acme_co", "@acme_co", False),
    ("pinterest", "acme.co", "@acme.co", True),
    # linkedin — slug, extracted from a pasted URL
    ("linkedin", "https://www.linkedin.com/company/nexplora-ai/", "nexplora-ai", False),
    ("linkedin", "linkedin.com/company/nexplora-ai", "nexplora-ai", False),
    ("linkedin", "https://linkedin.com/company/nexplora-ai?trk=x", "nexplora-ai", False),
    ("linkedin", "https://www.linkedin.com/company/nexplora-ai/about/", "nexplora-ai", False),
    ("linkedin", "NEXPLORA-AI", "nexplora-ai", False),
    # …and the case that made this a defect: a URL cut short at the keyword must NOT become the slug
    # "company". It is handed back whole so the error can name the real problem.
    ("linkedin", "https://www.linkedin.com/company/", "https://www.linkedin.com/company/", True),
    ("linkedin", "some/other/path", "some/other/path", True),
]


def test_publish_handle_normalization_matches_the_ported_table():
    import nx_cli as _c
    for channel, raw, expected, _err in _PORT_CASES:
        got = _c._normalize_publish_handle(channel, raw)
        assert got == expected, f"{channel}: normalize({raw!r}) -> {got!r}, expected {expected!r}"


def test_publish_handle_validation_matches_the_ported_table():
    import nx_cli as _c
    for channel, raw, expected, err in _PORT_CASES:
        got = _c._publish_handle_error(channel, expected)
        if err:
            assert got, f"{channel}: {expected!r} should have been refused"
        else:
            assert got is None, f"{channel}: {expected!r} was refused — {got}"


def test_a_linkedin_url_truncated_at_the_keyword_is_never_turned_into_a_slug():
    """The specific regression: last-path-segment guessing produced the confident, plausible, WRONG slug
    'company', which then PASSED validation — so the operator saw a saved binding naming a page that does
    not exist, with nothing suggesting a problem."""
    import nx_cli as _c
    for bad in ("https://www.linkedin.com/company/", "https://www.linkedin.com/school/",
                "https://www.linkedin.com/in/"):
        got = _c._normalize_publish_handle("linkedin", bad)
        assert got not in ("company", "school", "in"), f"{bad} became the slug {got!r}"
        assert _c._publish_handle_error("linkedin", got), f"{bad} normalized to {got!r} and was ACCEPTED"


def test_every_publishing_channel_has_a_shape_rule():
    """A channel offered by the picker with no rule would be persisted unvalidated."""
    import nx_cli as _c
    for it in nx_slash_menu._SUPPLY_ITEMS:
        if it.get("kind") != "publishing":
            continue
        ch = it["cmd"]
        has = ch == "linkedin" or ch in _c._PUBLISH_HANDLE_RULES
        assert has, f"{ch} is offered by /supply but has no address shape rule"


# ── the reach hub reads the address from the ONE canonical rule ──────────────
def test_telegram_address_is_read_from_chat_id_not_to():
    """Telegram stores chat_id; every other channel stores 'to'. The hub restated that rule inline and got
    it wrong, rendering a permanently blank address for the flagship channel while /message showed it
    correctly for the identical config."""
    import nx_message as _m
    assert _m.channel_handle("telegram", {"chat_id": "6672341304"}) == "6672341304"
    assert _m.channel_handle("telegram", {"to": "6672341304"}) == "", "telegram must not read 'to'"
    assert _m.channel_handle("email", {"to": "v@example.com"}) == "v@example.com"


def test_the_hub_shows_a_real_telegram_chat_id():
    """Built from the shape channels_state ACTUALLY produces (chat_id), not a hand-invented 'to'. The
    earlier version of this test fabricated {'to': ...} — a shape the module cannot emit — so it was green
    against the bug and would have stayed green forever."""
    st = _blank()
    st["telegram"] = {"configured": True, "active": True, "chat_id": "6672341304"}
    out = _run_channels_capture(st)
    assert "6672341304" in out, "the linked chat id is the proof — show it"


def test_no_two_reach_rows_share_a_display_name():
    """'Text' named iMessage in /message and SMS in the hub — one word, two channels, one click apart."""
    import nx_cli as _c
    src = io.open(os.path.join(_CLI, "nx_cli.py"), encoding="utf-8").read()
    body = src.split("def _run_channels(", 1)[1].split("\ndef ", 1)[0]
    names = re.findall(r'\(\s*"(\w+)",\s*"([^"]+)"\s*\)', body.split("_ROWS = [", 1)[1].split("]", 1)[0])
    labels = [n for _k, n in names]
    assert len(labels) == len(set(labels)), f"duplicate reach-row label: {labels}"
    menu = [c["name"] for c in nx_slash_menu.MESSAGE_CHANNELS]
    assert len(menu) == len(set(menu)), f"duplicate /message label: {menu}"
    assert "Text" not in labels and "Text" not in menu, "'Text' is ambiguous across SMS and iMessage"


def test_the_message_picker_covers_every_report_back_channel():
    """A channel in nx_message.CHANNELS but missing from the picker is configurable only by someone who
    already knows the command — and the /channels hub lists a row they cannot act on."""
    import nx_message as _m
    picker = {c["key"] for c in nx_slash_menu.MESSAGE_CHANNELS}
    missing = set(_m.CHANNELS) - picker
    assert not missing, f"/message picker is missing: {sorted(missing)}"


def test_channels_with_arguments_points_at_publish_instead_of_silently_opening_the_hub():
    """`/channels connect meta` was the publish command for a long time and muscle memory outlives a
    rename. Swallowing the argument would look like the old command still worked."""
    src = io.open(os.path.join(_CLI, "nx_cli.py"), encoding="utf-8").read()
    branch = src.split('if cmd=="/channels":', 1)[1][:1200]
    assert "user.split()" in branch, "/channels ignores its arguments entirely"
    assert "/publish" in branch, "/channels with arguments must point at /publish"


def test_a_configured_channel_with_no_address_is_not_called_linked():
    """Telegram counts as `configured` on the bot token ALONE, so the DEFAULT first run — paste token,
    haven't DM'd the bot yet — produced a green ● "linked" row with an empty address for a channel that
    could not reach anyone. Delivery is not established by a token; it needs the chat id too."""
    st = _blank()
    st["telegram"] = {"configured": True, "active": True}   # token stored, no chat_id yet
    out = _run_channels_capture(st)
    assert "no address yet" in out, "a channel that cannot deliver must not read as plainly linked"
