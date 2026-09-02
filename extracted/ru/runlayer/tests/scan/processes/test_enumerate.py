"""Parser + union unit tests for the process-discovery enumeration layer.

Every OS backend is split into a pure parser (text/data -> records) so the
per-OS output shapes are exercised here from captured fixtures, with no live
subprocess. This is the bulk of the channel's correctness surface: the runners
are thin best-effort wrappers, but a parser regression silently drops findings.
"""

from __future__ import annotations

from pathlib import Path

from runlayer_cli.scan.processes import enumerate as enumerate_module
from runlayer_cli.scan.processes.enumerate import (
    ListenerSocket,
    _decode_proc_cmdline,
    _enumerate_ps,
    bind_scope_from_hex_ip,
    bind_scope_from_host,
    parse_linux_proc_status,
    parse_lsof,
    parse_netstat,
    parse_proc_net_tcp,
    parse_ps_table,
    parse_windows_cim,
    union_by_pid,
)
from runlayer_cli.scan.processes.models import ProcessCandidate


# ---------------------------------------------------------------------------
# Bind-scope classification
# ---------------------------------------------------------------------------
class TestBindScopeFromHost:
    def test_ipv4_loopback(self):
        assert bind_scope_from_host("127.0.0.1") == "loopback"

    def test_ipv4_loopback_subnet(self):
        # The whole 127.0.0.0/8 block is loopback.
        assert bind_scope_from_host("127.1.2.3") == "loopback"

    def test_ipv6_loopback(self):
        assert bind_scope_from_host("::1") == "loopback"

    def test_ipv6_loopback_bracketed(self):
        assert bind_scope_from_host("[::1]") == "loopback"

    def test_localhost_name(self):
        assert bind_scope_from_host("localhost") == "loopback"

    def test_wildcard_all_interfaces(self):
        assert bind_scope_from_host("*") == "all_interfaces"

    def test_zero_address_all_interfaces(self):
        assert bind_scope_from_host("0.0.0.0") == "all_interfaces"

    def test_ipv6_any_all_interfaces(self):
        assert bind_scope_from_host("::") == "all_interfaces"

    def test_specific_lan_address_is_exposed(self):
        # A concrete non-loopback bind is reachable off-box -> treated as exposed.
        assert bind_scope_from_host("192.168.1.20") == "all_interfaces"


class TestBindScopeFromHexIp:
    def test_ipv4_loopback_hex(self):
        # 127.0.0.1 stored little-endian in /proc/net/tcp.
        assert bind_scope_from_hex_ip("0100007F") == "loopback"

    def test_ipv4_all_interfaces_hex(self):
        assert bind_scope_from_hex_ip("00000000") == "all_interfaces"

    def test_ipv6_loopback_hex(self):
        # ::1 as four little-endian words.
        assert bind_scope_from_hex_ip("00000000000000000000000001000000") == "loopback"

    def test_ipv6_any_hex(self):
        assert (
            bind_scope_from_hex_ip("00000000000000000000000000000000")
            == "all_interfaces"
        )

    def test_malformed_hex_defaults_exposed(self):
        # Never raise; unknown shapes fail safe toward "exposed".
        assert bind_scope_from_hex_ip("zzz") == "all_interfaces"


# ---------------------------------------------------------------------------
# Source A -- process table parsers
# ---------------------------------------------------------------------------
_PS_FIXTURE = (
    "  501     1 alice Wed Jul 15 09:27:01 2026 "
    "/Applications/Cursor.app/Contents/MacOS/Cursor --enable-crashpad\n"
    "  777   501 alice Wed Jul 15 09:28:00 2026 "
    "npx -y @modelcontextprotocol/server-filesystem /tmp/project\n"
    "\n"  # blank line tolerated
    " 1002     1 root Wed Jul 15 09:00:00 2026 /usr/sbin/cupsd -l\n"
)


class TestParsePsTable:
    def test_row_count_skips_blank(self):
        rows = parse_ps_table(_PS_FIXTURE)
        assert len(rows) == 3

    def test_pid_ppid_user(self):
        row = parse_ps_table(_PS_FIXTURE)[0]
        assert row.pid == 501
        assert row.ppid == 1
        assert row.user == "alice"

    def test_lstart_is_five_tokens(self):
        row = parse_ps_table(_PS_FIXTURE)[0]
        assert row.started_at == "Wed Jul 15 09:27:01 2026"

    def test_argv_preserved_after_lstart(self):
        row = parse_ps_table(_PS_FIXTURE)[1]
        assert row.argv == [
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/tmp/project",
        ]
        assert row.exe == "npx"

    def test_garbage_line_dropped(self):
        # Non-numeric pid -> skipped, not raised.
        assert parse_ps_table("not a ps row at all\n") == []


def test_ps_enumerator_resolves_executable_symlink(monkeypatch, tmp_path: Path):
    executable = tmp_path / "Cellar" / "opencode" / "1.17.8" / "bin" / "opencode"
    executable.parent.mkdir(parents=True)
    executable.write_text("")
    symlink = tmp_path / "bin" / "opencode"
    symlink.parent.mkdir()
    symlink.symlink_to(executable)
    output = f"  501     1 alice Wed Jul 15 09:27:01 2026 {symlink} --version\n"
    monkeypatch.setattr(enumerate_module, "_run", lambda *_args, **_kwargs: output)

    [candidate] = _enumerate_ps(timeout=1)

    assert candidate.exe == str(executable)
    assert candidate.argv[0] == str(symlink)


_PROC_STATUS = """\
Name:\tnode
Umask:\t0022
State:\tS (sleeping)
Tgid:\t777
Pid:\t777
PPid:\t501
Uid:\t1001\t1000\t1000\t1000
Gid:\t1000\t1000\t1000\t1000
"""


class TestParseLinuxProcStatus:
    def test_ppid_and_effective_uid(self):
        ppid, uid = parse_linux_proc_status(_PROC_STATUS)
        assert ppid == 501
        assert uid == "1000"

    def test_missing_fields_are_none(self):
        ppid, uid = parse_linux_proc_status("Name:\tfoo\n")
        assert ppid is None
        assert uid is None


class TestDecodeProcCmdline:
    def test_nul_delimited_split(self):
        raw = b"npx\x00-y\x00@modelcontextprotocol/server-git\x00"
        assert _decode_proc_cmdline(raw) == [
            "npx",
            "-y",
            "@modelcontextprotocol/server-git",
        ]

    def test_empty_cmdline(self):
        assert _decode_proc_cmdline(b"") == []


_CIM_ARRAY = """\
[
  {"ProcessId": 4321, "ParentProcessId": 100, "Name": "node.exe",
   "CommandLine": "\\"C:\\\\Program Files\\\\nodejs\\\\node.exe\\" server.js --port 3000"},
  {"ProcessId": 8888, "ParentProcessId": 1, "Name": "python.exe", "CommandLine": null}
]
"""

_CIM_SINGLE = """\
{"ProcessId": 55, "ParentProcessId": 1, "Name": "svc.exe", "CommandLine": "svc.exe"}
"""


class TestParseWindowsCim:
    def test_array_shape(self):
        rows = parse_windows_cim(_CIM_ARRAY)
        assert len(rows) == 2
        assert rows[0].pid == 4321
        assert rows[0].ppid == 100

    def test_quoted_path_tokenized(self):
        rows = parse_windows_cim(_CIM_ARRAY)
        # The space inside the quoted program path is preserved as one token.
        assert rows[0].argv[0] == r"C:\Program Files\nodejs\node.exe"
        assert rows[0].argv[1:] == ["server.js", "--port", "3000"]

    def test_null_commandline_falls_back_to_name(self):
        rows = parse_windows_cim(_CIM_ARRAY)
        assert rows[1].argv == ["python.exe"]
        assert rows[1].exe == "python.exe"

    def test_single_object_shape(self):
        rows = parse_windows_cim(_CIM_SINGLE)
        assert len(rows) == 1
        assert rows[0].pid == 55

    def test_malformed_json_is_empty(self):
        assert parse_windows_cim("not json") == []


# ---------------------------------------------------------------------------
# Source B -- listener parsers
# ---------------------------------------------------------------------------
_LSOF_FIXTURE = (
    "p1234\n"
    "n127.0.0.1:3000\n"
    "p5678\n"
    "n*:8080\n"
    "n[::1]:5000\n"
    "p9999\n"
    "n192.168.1.5:6006->192.168.1.9:52000\n"  # established, no listener port
)


class TestParseLsof:
    def test_loopback_listener(self):
        listeners = parse_lsof(_LSOF_FIXTURE)
        assert ListenerSocket(pid=1234, port=3000, bind_scope="loopback") in listeners

    def test_wildcard_listener(self):
        listeners = parse_lsof(_LSOF_FIXTURE)
        assert (
            ListenerSocket(pid=5678, port=8080, bind_scope="all_interfaces")
            in listeners
        )

    def test_ipv6_loopback_listener(self):
        listeners = parse_lsof(_LSOF_FIXTURE)
        assert ListenerSocket(pid=5678, port=5000, bind_scope="loopback") in listeners

    def test_established_connection_ignored(self):
        listeners = parse_lsof(_LSOF_FIXTURE)
        assert all(lst.pid != 9999 for lst in listeners)


_PROC_NET_TCP = """\
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 0100007F:0BB8 00000000:0000 0A 00000000:00000000 00:00000000 00000000  1000        0 54321 1 0000000000000000 100 0 0 10 0
   1: 00000000:1F90 00000000:0000 0A 00000000:00000000 00:00000000 00000000  1000        0 54399 1 0000000000000000 100 0 0 10 0
   2: 0100007F:C000 0100007F:0BB8 01 00000000:00000000 00:00000000 00000000  1000        0 55000 1 0000000000000000 100 0 0 10 0
"""


class TestParseProcNetTcp:
    def test_listen_rows_only(self):
        rows = parse_proc_net_tcp(_PROC_NET_TCP)
        # Row 2 is state 01 (ESTABLISHED) and must be dropped.
        assert len(rows) == 2

    def test_loopback_port_and_inode(self):
        rows = parse_proc_net_tcp(_PROC_NET_TCP)
        assert (54321, 3000, "loopback") in rows

    def test_all_interfaces_port(self):
        rows = parse_proc_net_tcp(_PROC_NET_TCP)
        assert (54399, 8080, "all_interfaces") in rows


_NETSTAT_FIXTURE = """\

Active Connections

  Proto  Local Address          Foreign Address        State           PID
  TCP    127.0.0.1:3000         0.0.0.0:0              LISTENING       4321
  TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       8888
  TCP    127.0.0.1:52000        127.0.0.1:3000         ESTABLISHED     9999
  UDP    0.0.0.0:5353           *:*                                    1000
"""


class TestParseNetstat:
    def test_listening_rows_only(self):
        listeners = parse_netstat(_NETSTAT_FIXTURE)
        assert len(listeners) == 2

    def test_loopback_listener(self):
        listeners = parse_netstat(_NETSTAT_FIXTURE)
        assert ListenerSocket(pid=4321, port=3000, bind_scope="loopback") in listeners

    def test_all_interfaces_listener(self):
        listeners = parse_netstat(_NETSTAT_FIXTURE)
        assert (
            ListenerSocket(pid=8888, port=8080, bind_scope="all_interfaces")
            in listeners
        )

    def test_established_and_udp_ignored(self):
        listeners = parse_netstat(_NETSTAT_FIXTURE)
        pids = {lst.pid for lst in listeners}
        assert 9999 not in pids  # ESTABLISHED
        assert 1000 not in pids  # UDP


# ---------------------------------------------------------------------------
# Union by pid
# ---------------------------------------------------------------------------
class TestUnionByPid:
    def test_listener_folds_into_process(self):
        procs = [ProcessCandidate(pid=1234, exe="node", argv=["node", "srv.js"])]
        listeners = [ListenerSocket(pid=1234, port=3000, bind_scope="loopback")]
        merged = union_by_pid(procs, listeners)
        assert len(merged) == 1
        assert merged[0].listening_ports == [3000]
        assert merged[0].bind_scope == "loopback"
        assert merged[0].discovery_source == "proc_table"

    def test_orphan_listener_becomes_candidate(self):
        # A listener whose pid Source A missed still surfaces the port.
        merged = union_by_pid(
            [], [ListenerSocket(pid=42, port=9000, bind_scope="all_interfaces")]
        )
        assert len(merged) == 1
        assert merged[0].pid == 42
        assert merged[0].listening_ports == [9000]
        assert merged[0].discovery_source == "listening_port"

    def test_multiple_ports_sorted_and_scope_widened(self):
        procs = [ProcessCandidate(pid=7, exe="app")]
        listeners = [
            ListenerSocket(pid=7, port=8080, bind_scope="loopback"),
            ListenerSocket(pid=7, port=3000, bind_scope="all_interfaces"),
        ]
        merged = union_by_pid(procs, listeners)
        assert merged[0].listening_ports == [3000, 8080]
        # Scope widens toward the most exposed listener.
        assert merged[0].bind_scope == "all_interfaces"

    def test_duplicate_port_deduped(self):
        procs = [ProcessCandidate(pid=7, exe="app")]
        listeners = [
            ListenerSocket(pid=7, port=3000, bind_scope="loopback"),
            ListenerSocket(pid=7, port=3000, bind_scope="loopback"),
        ]
        merged = union_by_pid(procs, listeners)
        assert merged[0].listening_ports == [3000]
