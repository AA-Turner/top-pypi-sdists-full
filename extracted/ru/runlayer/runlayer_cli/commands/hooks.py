"""Hidden hook relay command for ``runlayer-hook.sh`` (delegates to ``hook.relay``)."""

import json
import sys

import typer

app = typer.Typer(hidden=True)


@app.command()
def relay(
    target: str = typer.Argument(
        help="Relay target: 'enforce', 'event', 'tool-pre', or 'tool-post'"
    ),
    timeout: int | None = typer.Option(None, help="Override default timeout (seconds)"),
    debug: bool = typer.Option(False, "--debug", hidden=True),
) -> None:
    """Read JSON from stdin, resolve credentials, POST to the hooks endpoint."""
    # Lazy so the non-hook ``runlayer`` startup path never imports the relay chain.
    from runlayer_cli.hook import relay as hook_relay  # noqa: PLC0415
    from runlayer_cli.hook.log_silence import silence_hook_logging  # noqa: PLC0415

    # Hooks must never emit log output: stdout is the protocol channel and
    # clients treat any stderr as a hook error. Silence before anything logs.
    silence_hook_logging()

    if target == "stream-transcript":
        stream_transcript(debug=debug)
        return

    if target not in hook_relay.HOOK_RELAY_TARGETS:
        typer.echo(
            "Unknown target: "
            f"{target}. Use 'enforce', 'event', 'tool-pre', or 'tool-post'.",
            err=True,
        )
        raise typer.Exit(1)
    payload = sys.stdin.read()
    try:
        host, secret = hook_relay._load_credentials()
    except hook_relay.RelayError as e:
        raise typer.Exit(e.exit_code)

    try:
        text = hook_relay._post(
            host,
            secret,
            payload,
            target=target,
            timeout=timeout,
            debug=debug,
        )
    except hook_relay.RelayError as e:
        if e.body:
            sys.stdout.write(e.body)
        raise typer.Exit(e.exit_code)

    sys.stdout.write(text)
    raise typer.Exit(0)


def stream_transcript(
    debug: bool = False,
) -> None:
    """Read a transcript stream request from stdin and forward live events."""
    from runlayer_cli.hook.transcript_stream import (  # noqa: PLC0415
        clear_transcript_stream_active,
        run_transcript_stream,
    )

    payload = {}
    try:
        wrapper = json.loads(sys.stdin.read() or "{}")
        if not isinstance(wrapper, dict):
            raise typer.Exit(0)
        client_name = wrapper.get("client")
        raw_payload = wrapper.get("payload")
        if not isinstance(client_name, str) or not isinstance(raw_payload, dict):
            raise typer.Exit(0)
        payload = raw_payload
        start_offset = wrapper.get("start_offset", 0)
        if not isinstance(start_offset, int):
            start_offset = 0
        run_transcript_stream(
            client_name=client_name,
            payload=payload,
            start_offset=start_offset,
            debug=debug,
        )
    except typer.Exit:
        raise
    except Exception:
        clear_transcript_stream_active(payload)
