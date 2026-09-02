"""Classify container-launcher stdio commands into normalized OCI image identity.

Mode A of AI Watch container visibility (ENG-4201). An MCP server stored as
``command=docker`` + ``args=["run", "-i", "--rm", "mcp/github"]`` carries no
image identity today: it does not dedup by image and Enforce cannot govern it.
This module parses the docker / podman / nerdctl / compose ``run`` / ``exec``
flag grammar and extracts a canonical image identity
(``oci:<repo>@<digest>`` when a digest is pinned, else ``oci:<repo>:<tag>``)
so container-launched servers dedup by image and a future Enforce can allowlist
them the way the STDIO allowlist governs npx / uvx.

Stdlib-only, subprocess-free: this module is in the ``aiwatch`` bundle closure
guarded by ``tests/test_aiwatch_imports.py`` (the ``docker`` SDK is excluded).
It never touches the daemon — it only classifies the config string on disk.

The backend mirrors this parser in
``backend/app/domains/ai_watch/container_command.py``; the two are kept in
lockstep by a fixture-parity contract test. Any grammar change here must land
in both.
"""

from __future__ import annotations

from dataclasses import dataclass, field

CONTAINER_RUNTIME = "container"
HOST_RUNTIME = "host"

# Command basenames recognized as container launchers.
_CONTAINER_COMMANDS = frozenset({"docker", "podman", "nerdctl"})
_COMPOSE_COMMANDS = frozenset({"docker-compose", "podman-compose"})

# Subcommands that take an image positional (run/create) vs a running
# container positional (exec). ``compose`` is handled separately.
_IMAGE_SUBCOMMANDS = frozenset({"run", "create"})
_CONTAINER_SUBCOMMANDS = frozenset({"exec"})
_SUBCOMMAND_KEYWORDS = _IMAGE_SUBCOMMANDS | _CONTAINER_SUBCOMMANDS | {"compose"}

# Long ``run``/``create``/``exec`` flags that consume the following token as
# their value. Keep this broad: a value-flag missing from this set is treated
# as boolean, so its value would be misread as the image. ``--flag=value``
# forms are self-contained and handled without this set.
_VALUE_FLAGS = frozenset(
    {
        "--add-host",
        "--annotation",
        "--attach",
        "--blkio-weight",
        "--blkio-weight-device",
        "--cap-add",
        "--cap-drop",
        "--cgroup-parent",
        "--cgroupns",
        "--cidfile",
        "--cpu-period",
        "--cpu-quota",
        "--cpu-rt-period",
        "--cpu-rt-runtime",
        "--cpu-shares",
        "--cpus",
        "--cpuset-cpus",
        "--cpuset-mems",
        "--detach-keys",
        "--device",
        "--device-cgroup-rule",
        "--device-read-bps",
        "--device-read-iops",
        "--device-write-bps",
        "--device-write-iops",
        "--dns",
        "--dns-option",
        "--dns-search",
        "--entrypoint",
        "--env",
        "--env-file",
        "--expose",
        "--gpus",
        "--group-add",
        "--health-cmd",
        "--health-interval",
        "--health-retries",
        "--health-start-period",
        "--health-timeout",
        "--hostname",
        "--ip",
        "--ip6",
        "--ipc",
        "--isolation",
        "--kernel-memory",
        "--label",
        "--label-file",
        "--link",
        "--link-local-ip",
        "--log-driver",
        "--log-opt",
        "--mac-address",
        "--memory",
        "--memory-reservation",
        "--memory-swap",
        "--memory-swappiness",
        "--mount",
        "--name",
        "--network",
        "--network-alias",
        "--net",
        "--oom-score-adj",
        "--pid",
        "--pids-limit",
        "--platform",
        "--publish",
        "--pull",
        "--restart",
        "--runtime",
        "--security-opt",
        "--shm-size",
        "--stop-signal",
        "--stop-timeout",
        "--storage-opt",
        "--sysctl",
        "--tmpfs",
        "--ulimit",
        "--user",
        "--userns",
        "--uts",
        "--volume",
        "--volume-driver",
        "--volumes-from",
        "--workdir",
    }
)

# Short forms (single dash) that consume the following token as their value.
_SHORT_VALUE_FLAGS = frozenset(
    {
        "a",  # --attach
        "c",  # --cpu-shares
        "e",  # --env
        "h",  # --hostname
        "l",  # --label
        "m",  # --memory
        "p",  # --publish
        "u",  # --user
        "v",  # --volume
        "w",  # --workdir
    }
)


@dataclass
class ContainerLaunch:
    """Result of classifying a container-launcher command.

    ``image_ref`` is ``None`` for ``exec``, ``compose run``, and
    ``compose exec`` (a container name / compose service, not a resolvable
    image) — ``runtime`` is still ``container`` in those cases. ``env_keys`` and ``mounts`` are parsed as
    future governance / exfil signals; Phase 1 does not persist them.
    """

    runtime: str
    subcommand: str | None
    raw_image: str | None
    image_ref: str | None
    image_digest: str | None
    env_keys: list[str] = field(default_factory=list)
    mounts: list[str] = field(default_factory=list)


def _command_basename(command: str) -> str:
    """Lowercased basename of ``command``, stripped of a ``.exe`` suffix.

    Splits on both POSIX and Windows separators so an absolute launcher path
    (``/usr/bin/docker``, ``C:\\Program Files\\Docker\\docker.exe``) resolves
    to the bare command name.
    """
    normalized = command.strip().replace("\\", "/")
    base = normalized.rsplit("/", 1)[-1]
    if base.lower().endswith(".exe"):
        base = base[:-4]
    return base.lower()


def _find_subcommand(args: list[str]) -> tuple[int, str] | None:
    """Return ``(index, keyword)`` of the first recognized subcommand token.

    Scans left-to-right for the first token in ``_SUBCOMMAND_KEYWORDS``. This
    skips global flags (``docker --context foo run ...``) without enumerating
    them, at the cost of a theoretical miss if a global flag *value* equals a
    subcommand keyword — not observed in real MCP configs.
    """
    for idx, tok in enumerate(args):
        if tok in _SUBCOMMAND_KEYWORDS:
            return idx, tok
    return None


def _parse_short_cluster(
    token: str, next_token: str | None
) -> tuple[list[tuple[str, str | None]], bool]:
    """Decompose a single-dash short cluster into ``(letter, value)`` pairs.

    A value-short (``-e``) takes the rest of the cluster as its value when
    attached (``-eFOO`` -> ``FOO``) or the next token otherwise (``-e FOO`` /
    ``-ite FOO``); it ends the cluster. Booleans (``-it``) yield
    ``(letter, None)`` pairs and consume nothing. Returns the pairs plus
    whether the *next* token was consumed as a value.
    """
    body = token[1:]
    pairs: list[tuple[str, str | None]] = []
    consumed_next = False
    for idx, ch in enumerate(body):
        if ch in _SHORT_VALUE_FLAGS:
            attached = body[idx + 1 :]
            if attached:
                pairs.append((ch, attached))
            else:
                pairs.append((ch, next_token))
                consumed_next = True
            break
        pairs.append((ch, None))
    return pairs, consumed_next


def _record_flag_value(
    key: str, value: str | None, env_keys: list[str], mounts: list[str]
) -> None:
    """Record an env key (name only) or a mount spec from a value-taking flag.

    ``key`` is a long flag name (``--env``) or a short letter (``e``).
    ``--env-file`` is intentionally not recorded (it references a file).
    """
    if value is None:
        return
    if key in ("--env", "e"):
        env_keys.append(value.split("=", 1)[0])
    elif key in ("--volume", "--mount", "v"):
        mounts.append(value)


def _parse_run_args(tokens: list[str]) -> tuple[str | None, list[str], list[str]]:
    """Single pass over ``run``/``create`` args -> ``(image, env_keys, mounts)``.

    One walker keeps the image positional, env keys, and mount specs consistent
    under the same flag grammar (long, short, clustered, ``=``-inline, ``--``).
    """
    image: str | None = None
    env_keys: list[str] = []
    mounts: list[str] = []
    i = 0
    n = len(tokens)
    while i < n:
        tok = tokens[i]
        if tok == "--":
            if i + 1 < n:
                image = tokens[i + 1]
            break
        if tok.startswith("--"):
            name, eq, inline = tok.partition("=")
            if name in _VALUE_FLAGS:
                value = inline if eq else (tokens[i + 1] if i + 1 < n else None)
                _record_flag_value(name, value, env_keys, mounts)
                i += 1 if eq else 2
            else:
                i += 1
            continue
        if tok.startswith("-") and len(tok) > 1:
            pairs, consumed_next = _parse_short_cluster(
                tok, tokens[i + 1] if i + 1 < n else None
            )
            for letter, value in pairs:
                _record_flag_value(letter, value, env_keys, mounts)
            i += 2 if consumed_next else 1
            continue
        image = tok
        break
    return image, env_keys, mounts


def split_image_reference(raw: str) -> tuple[str, str | None, str | None]:
    """Split a raw docker image reference into ``(repository, tag, digest)``.

    The tag separator is the ``:`` *after* the last ``/`` so a registry port
    (``localhost:5000/img``) is not mistaken for a tag. A ``@sha256:...``
    digest is split off first.
    """
    remainder = raw
    digest: str | None = None
    if "@" in remainder:
        remainder, digest = remainder.split("@", 1)
    slash_idx = remainder.rfind("/")
    colon_idx = remainder.rfind(":")
    tag: str | None = None
    if colon_idx > slash_idx:
        repository = remainder[:colon_idx]
        tag = remainder[colon_idx + 1 :] or None
    else:
        repository = remainder
    return repository, tag, digest


def canonical_image_identity(raw_image: str) -> tuple[str | None, str | None]:
    """Return ``(image_ref, image_digest)`` for a raw image token.

    ``image_ref`` is ``oci:<repo>@<digest>`` when a digest is pinned, else
    ``oci:<repo>:<tag>`` (defaulting the tag to ``latest``). Returns
    ``(None, None)`` for a token that is not a usable image reference.
    """
    raw = raw_image.strip()
    if not raw or raw.startswith("-"):
        return None, None
    repository, tag, digest = split_image_reference(raw)
    if not repository:
        return None, None
    if digest:
        return f"oci:{repository}@{digest}", digest
    return f"oci:{repository}:{tag or 'latest'}", None


def _compose_launch(args: list[str]) -> ContainerLaunch | None:
    """Classify a ``compose run`` / ``compose exec`` invocation.

    The compose positional is a service name, not an image, so ``image_ref``
    stays ``None``. Only ``run`` and ``exec`` are classified — ``create`` is
    not a service-launching compose pattern.
    """
    found = _find_subcommand(args)
    if found is not None and found[1] in ("run", "exec"):
        return ContainerLaunch(
            runtime=CONTAINER_RUNTIME,
            subcommand=f"compose {found[1]}",
            raw_image=None,
            image_ref=None,
            image_digest=None,
        )
    return None


def classify_container_command(
    command: str | None,
    args: list[str] | None,
) -> ContainerLaunch | None:
    """Classify a stdio ``command``/``args`` as a container launcher.

    Returns ``None`` when the command is not a recognized container launcher
    (the common host case), so callers can treat ``None`` as ``runtime=host``.
    """
    if not command:
        return None
    base = _command_basename(command)
    tokens = list(args or [])

    if base in _COMPOSE_COMMANDS:
        return _compose_launch(tokens)

    if base not in _CONTAINER_COMMANDS:
        return None

    found = _find_subcommand(tokens)
    if found is None:
        return None
    sub_idx, sub = found
    rest = tokens[sub_idx + 1 :]

    if sub == "compose":
        return _compose_launch(rest)

    if sub in _CONTAINER_SUBCOMMANDS:  # exec: positional is a container, not an image
        return ContainerLaunch(
            runtime=CONTAINER_RUNTIME,
            subcommand=sub,
            raw_image=None,
            image_ref=None,
            image_digest=None,
        )

    # run / create: first positional after the flags is the image.
    raw_image, env_keys, mounts = _parse_run_args(rest)
    if raw_image is None:
        return ContainerLaunch(
            runtime=CONTAINER_RUNTIME,
            subcommand=sub,
            raw_image=None,
            image_ref=None,
            image_digest=None,
            env_keys=env_keys,
            mounts=mounts,
        )
    image_ref, image_digest = canonical_image_identity(raw_image)
    return ContainerLaunch(
        runtime=CONTAINER_RUNTIME,
        subcommand=sub,
        raw_image=raw_image,
        image_ref=image_ref,
        image_digest=image_digest,
        env_keys=env_keys,
        mounts=mounts,
    )
