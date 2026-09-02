"""Selkies/Xvfb worker-side capture and input configuration (PLAN.md §Recommended
stack).

The browser worker runs headed Chromium against a private Xvfb display. During a
takeover, Selkies (WebRTC mode) captures that display and translates WebRTC
DataChannel input back through XTEST. This module generates the worker's launch
configuration; the actual process supervision is the worker image's entrypoint
(see ``deploy/worker/``), and the real capture/input tests are operator-runbook
steps (RUNBOOK-real-server-tests.md) because they need Selkies + an X server.

🚨 LICENSE: Selkies is **MPL-2.0**. Prefer an UNMODIFIED upstream deployment. If
any Selkies source file is modified, the MPL file-level source obligations apply
to those files. See ``deploy/LICENSE-NOTE-selkies.md``. This note is recorded so
the license review PLAN.md requires is not skipped.

The security-critical properties this config must preserve:

- **Encoder asleep until takeover (D-8, a REQUIREMENT).** The Selkies encoder is
  not started at worker boot. It starts when a control session is claimed and
  stops when control returns. Nothing streams by default.
- **Media policy is server-enforced.** Only video (+ optional audio) leaves the
  worker. Clipboard sync, microphone, camera, and file transport are OFF in the
  Selkies config itself, not merely hidden in the UI (S4 first-release media
  rules). A second layer (the gateway media block) declares the same policy.
- **The worker binds to the private network only.** Selkies' signalling/data
  ports are reachable only by the gateway on the private network; they are never
  public and never in an ICE candidate the client can read as a control address
  (S4 §4.1 item 3, §8).
- **XTEST input is the single writable path** and is gated by the worker input
  channel (``worker_input.py``): a `view` session, or any session after control
  is revoked, cannot inject.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import VIEWPORT_HEIGHT, VIEWPORT_WIDTH


@dataclass(frozen=True)
class SelkiesWorkerConfig:
    """Everything the worker entrypoint needs to launch Xvfb + headed Chromium +
    Selkies with the correct, locked-down policy."""

    display: str = ":99"
    xvfb_width: int = VIEWPORT_WIDTH
    xvfb_height: int = VIEWPORT_HEIGHT
    xvfb_depth: int = 24
    # Selkies signalling/data — PRIVATE network bind only.
    selkies_bind_host: str = "127.0.0.1"
    selkies_signalling_port: int = 8080
    # Media policy — enforced at the worker, matching CONTROL_MEDIA_POLICY.
    enable_video: bool = True
    enable_audio: bool = False
    enable_clipboard: bool = False
    enable_microphone: bool = False
    enable_camera: bool = False
    enable_file_transfer: bool = False
    # H.264/Opus per PLAN.md.
    video_codec: str = "h264"
    audio_codec: str = "opus"
    # Encoder is NOT started at boot (D-8).
    start_encoder_on_boot: bool = False

    def xvfb_args(self) -> list[str]:
        return [
            self.display,
            "-screen",
            "0",
            f"{self.xvfb_width}x{self.xvfb_height}x{self.xvfb_depth}",
            "-nolisten",
            "tcp",
        ]

    def selkies_env(self) -> dict[str, str]:
        """Environment for the Selkies process. These are the knobs that turn the
        forbidden capabilities OFF at the source, and pin the private bind."""
        return {
            "DISPLAY": self.display,
            "SELKIES_ENABLE_CLIPBOARD": _b(self.enable_clipboard),
            "SELKIES_ENABLE_MICROPHONE": _b(self.enable_microphone),
            "SELKIES_ENABLE_WEBCAM": _b(self.enable_camera),
            "SELKIES_ENABLE_FILE_TRANSFERS": _b(self.enable_file_transfer),
            "SELKIES_ENABLE_RESIZE": "false",  # fixed server-controlled viewport
            "SELKIES_AUDIO_ENABLED": _b(self.enable_audio),
            "SELKIES_ENCODER": self.video_codec,
            "SELKIES_AUDIO_CODEC": self.audio_codec,
            "SELKIES_ADDRESS": self.selkies_bind_host,
            "SELKIES_PORT": str(self.selkies_signalling_port),
        }

    def chromium_flags(self) -> list[str]:
        """Headed Chromium flags for a locked-down cloud browser worker. Extension
        install, device access, and the like are disabled in v1 (PLAN.md §Tabs,
        popups, downloads, and dialogs)."""
        return [
            f"--window-size={self.xvfb_width},{self.xvfb_height}",
            "--window-position=0,0",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-plugins",
            "--use-fake-ui-for-media-stream=deny",
        ]


def _b(v: bool) -> str:
    return "true" if v else "false"
