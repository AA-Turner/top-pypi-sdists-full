from __future__ import annotations


def _main() -> None:
    # Presilence the SDK's import-time log banners before importing the CLI (which pulls in the SDK):
    # raise the noisy framework loggers by name so only their own chatter is dropped, leaving the user's
    # agent/tool logs intact. AGENTS_SDK_DEBUG=1 keeps the full SDK logs (presilence is a no-op then).
    from mistralai.agents import _silence  # noqa: PLC0415

    _silence.presilence()
    from mistralai.vibe_agents.sdk.app.cli import app  # noqa: PLC0415

    app(prog_name="agents")


if __name__ == "__main__":
    _main()
