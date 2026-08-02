"""Two nx sessions can't wipe each other's channel config.

The live bug: the operator configured an iMessage report-back channel, and it VANISHED between turns — a second
nx session saved its whole config (with a stale/absent message_channels) straight over the first. save_config now
preserves externally-owned subtrees (message_channels, written solely by nx_message) by re-reading the live file,
so a whole-file save can't clobber a channel someone else just set up.

Run: python3 nx/cli/tests/test_config_race.py   (or via the nx verify gate)
"""
import sys, os, tempfile, json

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))   # nx/cli

import nx_cli
import nx_message


def test_save_config_does_not_clobber_a_channel_another_session_wrote():
    with tempfile.TemporaryDirectory() as d:
        cfgpath = os.path.join(d, "config.json")
        o_cli, o_msg = nx_cli.CONFIG_PATH, nx_message._CONFIG
        nx_cli.CONFIG_PATH = cfgpath
        nx_message._CONFIG = cfgpath
        try:
            # session A (nx_message) sets up a channel
            nx_message.configure_imessage("+15551234567")
            assert nx_message.channels_state()["imessage"]["configured"] is True

            # session B (nx_cli) saves a WHOLE config with NO message_channels (a stale startup copy) —
            # this used to overwrite the file and wipe the channel.
            nx_cli.save_config({"token": "abc", "_schema": 1})

            st = nx_message.channels_state()["imessage"]
            assert st["configured"] is True, "channel config was clobbered by a foreign save"
            assert st["to"] == "+15551234567"

            disk = json.load(open(cfgpath))
            assert disk["token"] == "abc", "nx_cli's own keys must still be written"
            assert disk["message_channels"]["imessage"]["to"] == "+15551234567", "channel subtree must survive"
        finally:
            nx_cli.CONFIG_PATH, nx_message._CONFIG = o_cli, o_msg


def test_save_config_still_writes_normally_when_no_prior_file():
    with tempfile.TemporaryDirectory() as d:
        cfgpath = os.path.join(d, "config.json")
        o_cli = nx_cli.CONFIG_PATH
        nx_cli.CONFIG_PATH = cfgpath
        try:
            nx_cli.save_config({"token": "xyz"})   # no file yet → preserve step no-ops, write proceeds
            assert json.load(open(cfgpath))["token"] == "xyz"
        finally:
            nx_cli.CONFIG_PATH = o_cli


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ %s" % n)
    print("ALL CONFIG-RACE PROOFS PASS")
