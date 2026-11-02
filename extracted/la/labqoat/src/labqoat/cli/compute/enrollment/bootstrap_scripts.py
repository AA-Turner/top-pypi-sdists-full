"""Pure generation of the remote preflight, sandbox runtime, configuration and service scripts."""

from __future__ import annotations

import json
import shlex
from collections.abc import Mapping

from labqoat.json_document import JsonValue


class BootstrapScripts:
    """Render POSIX shell executed as root on the connected host through ``sh -s``."""

    STATE_DIR = "/var/lib/labqoat-agent"
    CONFIG_DIR = "/etc/labqoat"
    STORE_DIR = "/var/lib/labqoat"
    UNIT = "/etc/systemd/system/labqoat-agent.service"
    SANDBOX_RELEASE = "20261005.0"
    SANDBOX_SHA512 = (
        "27fed731b432d6a39d908956623fd273979fda66b3ccf4b9c12413ea417c516e"
        "18a9dc3cced403fb28efe495d64dce4251f51cf8c4d9f4a72f9833bd96b6bb35"
    )
    PREFLIGHT = """set -u
echo "arch=$(uname -m)"
if docker info >/dev/null 2>&1; then echo docker=ok; else echo docker=unavailable; fi
if [ -f /sys/fs/cgroup/cgroup.controllers ]; then echo cgroup=v2; else echo cgroup=v1; fi
if [ -S /run/containerd/containerd.sock ] && [ -d /var/lib/containerd ] && command -v ctr >/dev/null 2>&1; then
  echo containerd=ok
else
  echo containerd=unavailable
fi
if command -v curl >/dev/null 2>&1 && command -v zstd >/dev/null 2>&1; then echo fetch=ok; else echo fetch=unavailable; fi
nvidia-smi -L 2>/dev/null | grep '^GPU ' | sed 's/^/gpu=/' || true
if docker info --format '{{json .Runtimes}}' 2>/dev/null | grep -q nvidia &&
  command -v nvidia-container-cli >/dev/null 2>&1; then
  echo nvidia_toolkit=yes
else
  echo nvidia_toolkit=no
fi
"""
    GPU_MOUNTS = """set -- --gpus all
for tool in nvidia-container-cli nvidia-container-runtime-hook; do
  set -- "$@" --mount "type=bind,source=$(command -v "$tool"),target=/usr/bin/$tool,readonly"
done
for library in $(ldconfig -p | awk '/libnvidia-container(-go)?\\.so\\.1 /{print $NF}'); do
  set -- "$@" --mount "type=bind,source=$(readlink -f "$library"),target=/usr/lib/x86_64-linux-gnu/${library##*/},readonly"
done
"""

    @staticmethod
    def preflight() -> str:
        """Report architecture, Docker, control groups, containerd, download tools and GPUs as key=value lines."""
        return BootstrapScripts.PREFLIGHT

    @staticmethod
    def image_id(image_id: str) -> str:
        """Print the identifier of a loaded image so the transfer can be verified."""
        return f"docker image inspect --format '{{{{.Id}}}}' {shlex.quote(image_id)}"

    @staticmethod
    def gpu_check(image_id: str) -> str:
        """Prove the loaded agent image can start with every GPU attached."""
        return f"docker run --rm --pull=never --gpus all {shlex.quote(image_id)} true"

    @staticmethod
    def sandbox_runtime() -> str:
        """Install the pinned sandbox runtime every workload runs in, verified before anything is unpacked."""
        release = BootstrapScripts.SANDBOX_RELEASE
        url = f"https://storage.googleapis.com/gvisor/releases/release/{release}/x86_64/gvisor.tar.zstd"
        return f"""if ! /usr/local/bin/runsc --version 2>/dev/null | grep -q 'release-{release}'; then
  bundle="$(mktemp)"
  curl -fsS --retry 5 {url} -o "$bundle"
  printf '%s  %s\\n' {BootstrapScripts.SANDBOX_SHA512} "$bundle" | sha512sum -c - >/dev/null
  tar --zstd -xf "$bundle" -C /usr/local/bin
  rm -f "$bundle"
fi"""

    @staticmethod
    def launcher(image_id: str, gpus: bool) -> str:
        """Start the pinned agent with the host access it needs to run workloads straight on the sandbox runtime."""
        config = BootstrapScripts.CONFIG_DIR
        store = BootstrapScripts.STORE_DIR
        state = BootstrapScripts.STATE_DIR
        mounts = [
            "type=bind,source=/usr/local/bin/runsc,target=/usr/local/bin/runsc,readonly",
            "type=bind,source=/usr/local/bin/gvisor-bin,target=/usr/local/bin/gvisor-bin,readonly",
            'type=bind,source="$(command -v ctr)",target=/usr/bin/ctr,readonly',
            "type=bind,source=/run/containerd,target=/run/containerd,bind-propagation=rshared",
            "type=bind,source=/var/lib/containerd,target=/var/lib/containerd,readonly",
            f"type=bind,source={store},target={store},bind-propagation=rshared",
            "type=bind,source=/run/netns,target=/run/netns,bind-propagation=rshared",
            "type=bind,source=/run/labqoat,target=/run/labqoat",
            f"type=bind,source={config},target={config},readonly",
            f"type=bind,source={state},target={state}",
        ]
        arguments = " ".join(f"--mount {mount}" for mount in mounts)
        devices = BootstrapScripts.GPU_MOUNTS if gpus else "set --\n"
        return f"""#!/bin/sh
# The agent starts workloads straight on the sandbox runtime from images containerd holds. It needs the
# host's process and control-group namespaces, and a store and namespace directory whose mounts reach the host.
set -eu
install -d /run/labqoat /run/netns {store}
{devices}exec /usr/bin/docker run --rm --pull=never --name labqoat-agent --network host "$@" \\
  --privileged --pid host --cgroupns host -e LABQOAT_AGENT_CONFIG={config}/settings.json \\
  {arguments} {shlex.quote(image_id)}
"""

    @staticmethod
    def unit() -> str:
        """Run the launcher under systemd, replacing any earlier agent container first."""
        return f"""[Unit]
Description=Labqoat agent
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
ExecStartPre=-/usr/bin/docker rm -f labqoat-agent
ExecStart=/bin/sh {BootstrapScripts.CONFIG_DIR}/agent-host.sh
ExecStop=/usr/bin/docker stop labqoat-agent
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

    @staticmethod
    def install(agent_settings: Mapping[str, JsonValue], image_id: str, gpus: bool) -> str:
        """Install the sandbox runtime, write root-only settings, the image pin and the service, then (re)start it."""
        config = BootstrapScripts.CONFIG_DIR
        settings = json.dumps({**agent_settings, "state_dir": BootstrapScripts.STATE_DIR}, sort_keys=True)
        files = [
            BootstrapScripts.write(f"{config}/settings.json", settings, "0600"),
            BootstrapScripts.write(f"{config}/agent-image", image_id, "0644"),
            BootstrapScripts.write(f"{config}/agent-host.sh", BootstrapScripts.launcher(image_id, gpus), "0700"),
            BootstrapScripts.write(BootstrapScripts.UNIT, BootstrapScripts.unit(), "0644"),
        ]
        return "\n".join(
            [
                "set -eu",
                "umask 077",
                BootstrapScripts.sandbox_runtime(),
                f"install -d -m 0755 -o root -g root {config} {BootstrapScripts.STORE_DIR}",
                f"install -d -m 0700 -o root -g root {BootstrapScripts.STATE_DIR}",
                *files,
                "systemctl daemon-reload",
                "systemctl enable labqoat-agent",
                "systemctl restart labqoat-agent",
                "",
            ]
        )

    @staticmethod
    def write(path: str, content: str, mode: str) -> str:
        """Replace one root-owned file atomically with exact content and permissions."""
        staged = shlex.quote(f"{path}.tmp")
        target = shlex.quote(path)
        return (
            f"printf '%s\\n' {shlex.quote(content.rstrip(chr(10)))} > {staged}\n"
            f"chown root:root {staged}\nchmod {mode} {staged}\nmv -f {staged} {target}"
        )
