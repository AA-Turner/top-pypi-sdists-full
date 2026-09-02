from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, load_all
from matrx_ai.tools.vfs.commands.registry import get
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv

load_all()


@pytest.fixture
async def vfs():
    backend = MemoryBackend()
    ws = "ws-test"
    await backend.ensure_workspace_root(ws)
    fs = MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)
    await fs._mkdir("/tmp", create_parents=False)
    await fs._pipe_file("/tmp/a.txt", b"alpha\nbeta\n")
    await fs._pipe_file("/tmp/b.txt", b"gamma\n")
    await fs._mkdir("/proj", create_parents=False)
    await fs._pipe_file("/proj/Makefile", b"all:\n\techo hi\n")
    await fs._mkdir("/empty", create_parents=False)
    return fs


def _ctx(vfs, argv, stdin=b"", cwd="/tmp"):
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


async def _run(vfs, argv, stdin=b"", cwd="/tmp"):
    cmd = get(argv[0])
    assert cmd is not None, f"command not registered: {argv[0]}"
    return await cmd(_ctx(vfs, argv, stdin, cwd))


# --- Editors -----------------------------------------------------------------


async def test_vim(vfs):
    r = await _run(vfs, ["vim", "file.txt"])
    assert r.exit_code == 1
    assert b"Vim: Warning: Output is not to a terminal" in r.stderr
    assert b"Vim: Warning: Input is not from a terminal" in r.stderr


async def test_nvim_alias(vfs):
    r = await _run(vfs, ["nvim"])
    assert r.exit_code == 1
    assert b"Vim: Warning" in r.stderr


async def test_vi_alias(vfs):
    r = await _run(vfs, ["vi"])
    assert r.exit_code == 1


async def test_nano(vfs):
    r = await _run(vfs, ["nano", "x"])
    assert r.exit_code == 1
    assert r.stderr == b"Error opening terminal: dumb.\n"


async def test_emacs(vfs):
    r = await _run(vfs, ["emacs"])
    assert r.exit_code == 1
    assert r.stderr == b"emacs: standard input is not a tty\n"


# --- less / more -------------------------------------------------------------


async def test_less_existing_file(vfs):
    r = await _run(vfs, ["less", "a.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha\nbeta\n"
    assert r.stderr == b""


async def test_less_missing_file(vfs):
    r = await _run(vfs, ["less", "/missing"])
    assert r.exit_code == 1
    assert b"cannot" not in r.stderr  # uses 'No such file or directory' wording
    assert r.stderr == b"less: /missing: No such file or directory\n"


async def test_more_multiple_files(vfs):
    r = await _run(vfs, ["more", "a.txt", "b.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha\nbeta\ngamma\n"


async def test_less_no_args_passes_stdin(vfs):
    r = await _run(vfs, ["less"], stdin=b"piped\n")
    assert r.exit_code == 0
    assert r.stdout == b"piped\n"


async def test_less_directory(vfs):
    r = await _run(vfs, ["less", "/tmp"])
    assert r.exit_code == 1
    assert b"Is a directory" in r.stderr


# --- Network -----------------------------------------------------------------


async def test_ssh_with_user_at_host(vfs):
    r = await _run(vfs, ["ssh", "alice@example.com"])
    assert r.exit_code == 255
    assert r.stderr == b"ssh: connect to host example.com port 22: Network is unreachable\n"


async def test_ssh_no_args(vfs):
    r = await _run(vfs, ["ssh"])
    assert r.exit_code == 255
    assert b"host host port 22" in r.stderr


async def test_scp(vfs):
    r = await _run(vfs, ["scp", "file.txt", "user@remote:/tmp/"])
    assert r.exit_code == 1
    assert b"connect to host remote port 22" in r.stderr
    assert b"lost connection" in r.stderr


async def test_rsync(vfs):
    r = await _run(vfs, ["rsync", "-av", "src/", "dest/"])
    assert r.exit_code == 12
    assert b"connection unexpectedly closed" in r.stderr
    assert b"code 12" in r.stderr


async def test_curl_extracts_host(vfs):
    r = await _run(vfs, ["curl", "https://example.com/path?q=1"])
    assert r.exit_code == 6
    assert r.stderr == b"curl: (6) Could not resolve host: example.com\n"


async def test_curl_with_flags(vfs):
    r = await _run(vfs, ["curl", "-s", "-X", "POST", "-H", "X: Y", "https://api.example.com"])
    assert r.exit_code == 6
    assert b"Could not resolve host: api.example.com" in r.stderr


async def test_curl_no_url(vfs):
    r = await _run(vfs, ["curl"])
    assert r.exit_code == 6
    assert b"Could not resolve host: host" in r.stderr


async def test_wget(vfs):
    r = await _run(vfs, ["wget", "https://example.com/file.tar.gz"])
    assert r.exit_code == 4
    assert b"Resolving example.com" in r.stderr
    assert b"unable to resolve host address 'example.com'" in r.stderr


async def test_nc(vfs):
    r = await _run(vfs, ["nc", "example.com", "80"])
    assert r.exit_code == 1
    assert r.stderr == b"nc: connect: Network is unreachable\n"


async def test_netcat_alias(vfs):
    r = await _run(vfs, ["netcat", "host", "80"])
    assert r.exit_code == 1
    assert r.stderr == b"netcat: connect: Network is unreachable\n"


async def test_telnet(vfs):
    r = await _run(vfs, ["telnet", "host"])
    assert r.exit_code == 1
    assert r.stderr == b"telnet: connect: Network is unreachable\n"


async def test_ftp(vfs):
    r = await _run(vfs, ["ftp", "host"])
    assert r.exit_code == 1
    assert r.stderr == b"ftp: connect: Network is unreachable\n"


async def test_ping(vfs):
    r = await _run(vfs, ["ping", "google.com"])
    assert r.exit_code == 2
    assert r.stderr == b"ping: google.com: Temporary failure in name resolution\n"


# --- Containers / orchestration ---------------------------------------------


async def test_docker_ps(vfs):
    r = await _run(vfs, ["docker", "ps"])
    assert r.exit_code == 1
    assert r.stderr == (
        b"Cannot connect to the Docker daemon at unix:///var/run/docker.sock."
        b" Is the docker daemon running?\n"
    )


async def test_kubectl(vfs):
    r = await _run(vfs, ["kubectl", "get", "pods"])
    assert r.exit_code == 1
    assert b"connection to the server localhost:8080 was refused" in r.stderr


async def test_podman(vfs):
    r = await _run(vfs, ["podman", "ps"])
    assert r.exit_code == 125
    assert b"Cannot connect to Podman" in r.stderr


# --- Build tools -------------------------------------------------------------


async def test_make_no_makefile(vfs):
    r = await _run(vfs, ["make"], cwd="/empty")
    assert r.exit_code == 2
    assert r.stderr == b"make: *** No targets specified and no makefile found.  Stop.\n"


async def test_make_with_makefile_no_target(vfs):
    r = await _run(vfs, ["make"], cwd="/proj")
    assert r.exit_code == 0
    assert r.stdout == b"make: Nothing to be done for 'all'.\n"


async def test_make_with_target(vfs):
    r = await _run(vfs, ["make", "clean"], cwd="/proj")
    assert r.exit_code == 2
    assert r.stderr == b"make: *** No rule to make target 'clean'.  Stop.\n"


async def test_cmake(vfs):
    r = await _run(vfs, ["cmake", "."])
    assert r.exit_code == 127
    assert r.stderr == b"bash: cmake: command not found\n"


async def test_ninja(vfs):
    r = await _run(vfs, ["ninja"])
    assert r.exit_code == 127
    assert r.stderr == b"bash: ninja: command not found\n"


# --- Language runtimes -------------------------------------------------------


async def test_python_version_long(vfs):
    r = await _run(vfs, ["python", "--version"])
    assert r.exit_code == 0
    assert r.stdout == b"Python 3.13.0\n"


async def test_python_version_short(vfs):
    r = await _run(vfs, ["python3", "-V"])
    assert r.exit_code == 0
    assert r.stdout == b"Python 3.13.0\n"


async def test_python_dash_c(vfs):
    r = await _run(vfs, ["python", "-c", "print(1)"])
    assert r.exit_code == 127
    assert r.stderr == b"bash: python: command not found\n"


async def test_python_missing_script(vfs):
    r = await _run(vfs, ["python", "missing.py"])
    assert r.exit_code == 2
    assert b"can't open file 'missing.py'" in r.stderr
    assert b"No such file or directory" in r.stderr


async def test_python_existing_script(vfs):
    r = await _run(vfs, ["python", "a.txt"])
    assert r.exit_code == 127
    assert r.stderr == b"bash: python: command not found\n"


async def test_python313_alias(vfs):
    r = await _run(vfs, ["python3.13", "--version"])
    assert r.exit_code == 0
    assert r.stdout == b"Python 3.13.0\n"


async def test_node_version(vfs):
    r = await _run(vfs, ["node", "--version"])
    assert r.exit_code == 0
    assert r.stdout == b"v20.0.0\n"


async def test_node_v_short(vfs):
    r = await _run(vfs, ["node", "-v"])
    assert r.exit_code == 0
    assert r.stdout == b"v20.0.0\n"


async def test_node_missing_script(vfs):
    r = await _run(vfs, ["node", "missing.js"])
    assert r.exit_code == 1
    assert r.stderr == b"node: cannot open 'missing.js': No such file or directory\n"


async def test_node_no_args(vfs):
    r = await _run(vfs, ["node"])
    assert r.exit_code == 127
    assert r.stderr == b"bash: node: command not found\n"


async def test_nodejs_alias(vfs):
    r = await _run(vfs, ["nodejs", "--version"])
    assert r.exit_code == 0


@pytest.mark.parametrize(
    "name", ["npm", "pip", "pip3", "cargo", "go", "rustc", "gcc", "clang"]
)
async def test_lang_missing(vfs, name):
    r = await _run(vfs, [name, "install"])
    assert r.exit_code == 127
    assert r.stderr == f"bash: {name}: command not found\n".encode()


# --- TTY utilities -----------------------------------------------------------


async def test_htop(vfs):
    r = await _run(vfs, ["htop"])
    assert r.exit_code == 127
    assert r.stderr == b"bash: htop: command not found\n"


async def test_top(vfs):
    r = await _run(vfs, ["top"])
    assert r.exit_code == 127
    assert r.stderr == b"bash: top: command not found\n"


# --- Registration sanity -----------------------------------------------------


def test_all_stubs_registered():
    expected = [
        "vim", "nvim", "vi", "nano", "emacs",
        "less", "more",
        "ssh", "scp", "rsync", "curl", "wget",
        "nc", "netcat", "telnet", "ftp", "ping",
        "docker", "kubectl", "podman",
        "make", "cmake", "ninja",
        "python", "python3", "python3.13",
        "node", "nodejs",
        "npm", "pip", "pip3", "cargo", "go", "rustc", "gcc", "clang",
        "htop", "top",
    ]
    for name in expected:
        assert get(name) is not None, f"{name} not registered"
