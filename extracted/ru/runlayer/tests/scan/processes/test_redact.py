"""Redaction + hashing tests for the process channel.

argv is the highest-risk field (MCP launchers routinely pass API keys / tokens
as flags), so these lock in that secret-looking tokens are scrubbed, the
correlation hash is stable + independent of the display cap, and cwd/exe never
leak the host layout or account name.
"""

from __future__ import annotations

from runlayer_cli.scan.processes.redact import (
    MAX_ARGV_TOKENS,
    command_hash,
    redact_argv,
    redact_cwd_project,
    redact_exe,
)


class TestRedactArgv:
    def test_plain_flags_unchanged(self):
        argv = ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp/proj"]
        assert redact_argv(argv) == argv

    def test_github_token_scrubbed(self):
        # A ghp_ token embedded as a flag value must not survive.
        token = "ghp_" + "a" * 36
        out = redact_argv(["server", "--token", token])
        assert token not in " ".join(out)
        assert "<redacted>" in " ".join(out)

    def test_sk_key_scrubbed(self):
        key = "sk-" + "A" * 32
        out = redact_argv(["mcp", "--api-key", key])
        assert key not in " ".join(out)

    def test_keyed_value_scrubbed(self):
        out = redact_argv(["run", "--password=hunter2supersecret"])
        assert "hunter2supersecret" not in " ".join(out)

    def test_url_credentials_scrubbed(self):
        out = redact_argv(["proxy", "https://user:pass@example.com/mcp"])
        joined = " ".join(out)
        assert "user:pass" not in joined
        assert "example.com/mcp" in joined

    def test_known_username_scrubbed(self):
        out = redact_argv(["node", "/Users/alice/proj/server.js"], usernames=["alice"])
        assert "/Users/alice/" not in " ".join(out)

    def test_token_list_capped(self):
        argv = ["cmd"] + [f"--flag{i}" for i in range(MAX_ARGV_TOKENS + 20)]
        out = redact_argv(argv)
        # Capped list + one "(+N more)" marker.
        assert len(out) == MAX_ARGV_TOKENS + 1
        assert out[-1].startswith("...(+")

    def test_overlong_token_truncated(self):
        out = redact_argv(["cmd", "x" * 5000])
        assert out[1].endswith("...(truncated)")


class TestCommandHash:
    def test_stable(self):
        argv = ["npx", "-y", "@modelcontextprotocol/server-git"]
        assert command_hash(argv) == command_hash(list(argv))

    def test_sensitive_to_token_boundaries(self):
        # Joining with a separator that can't appear in argv avoids collisions.
        assert command_hash(["a b"]) != command_hash(["a", "b"])

    def test_independent_of_display_cap(self):
        # The hash covers the full argv even past the display cap, so two long
        # commands differing only past the cap still hash differently.
        base = ["cmd"] + [f"a{i}" for i in range(MAX_ARGV_TOKENS + 10)]
        other = list(base)
        other[-1] = "DIFFERENT"
        assert command_hash(base) != command_hash(other)

    def test_hex_digest_shape(self):
        digest = command_hash(["x"])
        assert len(digest) == 64
        assert all(c in "0123456789abcdef" for c in digest)


class TestRedactCwdProject:
    def test_none_passthrough(self):
        assert redact_cwd_project(None) is None

    def test_posix_basename_only(self):
        assert redact_cwd_project("/Users/alice/code/my-agent") == "my-agent"

    def test_windows_basename_only(self):
        assert redact_cwd_project(r"C:\Users\bob\code\my-agent") == "my-agent"

    def test_basename_username_still_scrubbed(self):
        # If the leaf dir is itself the account name, scrub it.
        assert redact_cwd_project("/home/alice", usernames=["alice"]) == "<redacted>"


class TestRedactExe:
    def test_none_passthrough(self):
        assert redact_exe(None) is None

    def test_system_path_unchanged(self):
        assert redact_exe("/usr/local/bin/node") == "/usr/local/bin/node"

    def test_home_username_scrubbed(self):
        assert (
            redact_exe("/Users/alice/.local/bin/uvx")
            == "/Users/<redacted>/.local/bin/uvx"
        )
