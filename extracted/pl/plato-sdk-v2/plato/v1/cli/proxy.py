"""Gateway commands for connecting to VMs through the WireGuard gateway.

This module provides CLI commands to connect to VMs via TLS + SNI routing
through an HAProxy gateway with WireGuard backend connectivity.

Commands:
    plato sandbox ssh <job_id> - SSH to a VM through the gateway
    plato sandbox tunnel <job_id> <port> - Open a local port forwarding tunnel to a VM
"""

import os
import socket
import ssl
import subprocess
import threading
from pathlib import Path

import typer

from plato._generated.api.v2.sessions import add_ssh_key as sessions_add_ssh_key
from plato._generated.models import AddSSHKeyRequest
from plato.v1.cli.ssh import generate_ssh_key_pair
from plato.v1.cli.utils import console, get_http_client, get_sandbox_state, require_api_key, save_sandbox_state

app = typer.Typer(help="Gateway commands for connecting to VMs.")

# Default gateway configuration
DEFAULT_GATEWAY_HOST = "gateway.plato.so"
DEFAULT_GATEWAY_PORT = 443


def get_gateway_config() -> tuple[str, int]:
    """Get gateway host and port from environment or defaults.

    Returns:
        Tuple of (host, port) for the gateway.
    """
    host = os.environ.get("PLATO_GATEWAY_HOST", DEFAULT_GATEWAY_HOST)
    port = int(os.environ.get("PLATO_GATEWAY_PORT", str(DEFAULT_GATEWAY_PORT)))
    return host, port


def create_tls_connection(
    gateway_host: str,
    gateway_port: int,
    sni: str,
    verify_ssl: bool = True,
) -> ssl.SSLSocket:
    """Create a TLS connection to the gateway with the specified SNI.

    Args:
        gateway_host: The gateway hostname.
        gateway_port: The gateway port.
        sni: The SNI (Server Name Indication) for routing.
        verify_ssl: Whether to verify SSL certificates.

    Returns:
        An SSL socket connected to the gateway.
    """
    # Create SSL context
    context = ssl.create_default_context()
    if not verify_ssl:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    # Create socket and wrap with TLS
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)

    # Wrap with TLS, using SNI for routing
    ssl_sock = context.wrap_socket(sock, server_hostname=sni)

    try:
        ssl_sock.connect((gateway_host, gateway_port))
    except Exception as e:
        ssl_sock.close()
        raise ConnectionError(f"Failed to connect to gateway: {e}") from e

    return ssl_sock


def forward_data(src: socket.socket, dst: socket.socket, name: str = "") -> None:
    """Forward data between two sockets until one closes.

    Args:
        src: Source socket to read from.
        dst: Destination socket to write to.
        name: Optional name for debugging.
    """
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass


@app.command()
def ssh(
    job_id: str | None = typer.Argument(None, help="The job ID to connect to (uses .sandbox.yaml if not provided)"),
    user: str = typer.Option("root", "--user", "-u", help="SSH username"),
    port: int = typer.Option(22, "--port", "-p", help="SSH port on the VM"),
    identity_file: str | None = typer.Option(None, "--identity", "-i", help="Path to SSH identity file"),
    no_verify: bool = typer.Option(False, "--no-verify", help="Skip SSL certificate verification"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose output including SSH command"),
    extra_args: list[str] | None = typer.Argument(None, help="Additional arguments to pass to SSH"),
) -> None:
    """SSH to a VM through the gateway.

    Connects to the VM's SSH port via TLS + SNI routing through HAProxy, then
    over WireGuard. If no job_id is provided, reads from .sandbox.yaml.

    Arguments:
        job_id: Job ID to connect to (optional - uses .sandbox.yaml if not provided)
        extra_args: Additional SSH arguments (pass after '--')

    Options:
        -u, --user: SSH username (default: root)
        -p, --port: SSH port on the VM (default: 22)
        -i, --identity: Path to SSH private key file (auto-loaded from .sandbox.yaml)
        --no-verify: Skip SSL certificate verification
        -v, --verbose: Show the SSH command being executed
    """
    # Try to load from .sandbox.yaml if job_id or identity_file not provided
    state = get_sandbox_state()

    if job_id is None:
        if state and state.get("job_id"):
            job_id = state["job_id"]
        else:
            console.print("[red]Error: No job_id provided and no .sandbox.yaml found[/red]")
            console.print("[dim]Run 'plato sandbox start' first or provide a job_id[/dim]")
            raise typer.Exit(1)

    # Auto-load identity file from state if not explicitly provided
    if identity_file is None and state:
        saved_key = state.get("ssh_private_key_path")
        if saved_key and Path(saved_key).exists():
            identity_file = saved_key
            console.print(f"[dim]Using SSH key: {saved_key}[/dim]")

    # If still no identity file, generate one and add to VM
    if identity_file is None:
        session_id = state.get("session_id") if state else None
        if session_id:
            console.print("[cyan]No SSH key found, generating and adding to VM...[/cyan]")
            try:
                api_key = require_api_key()

                # Generate key pair
                public_key, private_key_path = generate_ssh_key_pair(job_id[:8])
                identity_file = private_key_path

                # Add to VM via API
                add_key_request = AddSSHKeyRequest(
                    public_key=public_key,
                    username=user,
                )

                with get_http_client() as client:
                    response = sessions_add_ssh_key.sync(
                        client=client,
                        session_id=session_id,
                        body=add_key_request,
                        x_api_key=api_key,
                    )

                if response.success:
                    console.print("[green]SSH key added successfully[/green]")
                    # Update state with new key path
                    if state:
                        state["ssh_private_key_path"] = private_key_path
                        save_sandbox_state(state)
                else:
                    for jid, result in response.results.items():
                        if not result.success:
                            console.print(f"[red]Failed to add key to {jid[:8]}...: {result.error}[/red]")
                    raise typer.Exit(1)

            except Exception as e:
                console.print(f"[red]Failed to setup SSH key: {e}[/red]")
                raise typer.Exit(1)
        else:
            console.print("[red]Error: No SSH key and no session_id to add one[/red]")
            console.print("[dim]Provide -i <key_path> or run from a directory with .sandbox.yaml[/dim]")
            raise typer.Exit(1)

    gateway_host, gateway_port = get_gateway_config()
    sni = f"{job_id}--{port}.{gateway_host}"

    # Build ProxyCommand using openssl s_client
    verify_flag = ""
    if no_verify:
        verify_flag = "-verify_quiet"

    proxy_cmd = (
        f"openssl s_client -quiet -connect {gateway_host}:{gateway_port} -servername {sni} {verify_flag} 2>/dev/null"
    )

    # Build SSH command
    ssh_cmd = ["ssh", "-o", f"ProxyCommand={proxy_cmd}"]

    # Add identity file if available
    if identity_file:
        ssh_cmd.extend(["-i", identity_file])

    # Disable strict host key checking for gateway connections
    ssh_cmd.extend(
        [
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
        ]
    )

    # Add any extra SSH arguments
    if extra_args:
        ssh_cmd.extend(extra_args)

    # Add target
    ssh_cmd.append(f"{user}@{job_id}")

    console.print(f"[dim]Connecting to {job_id} via {gateway_host}...[/dim]")

    if verbose:
        console.print(f"[dim]SSH command: {' '.join(ssh_cmd)}[/dim]")

    try:
        # Execute SSH with inherited stdin/stdout/stderr
        result = subprocess.run(ssh_cmd)
        raise typer.Exit(result.returncode)
    except FileNotFoundError:
        console.print("[red]Error: ssh command not found[/red]")
        raise typer.Exit(1) from None
    except KeyboardInterrupt:
        console.print("\n[yellow]Connection interrupted[/yellow]")
        raise typer.Exit(130) from None


@app.command()
def tunnel(
    job_id: str = typer.Argument(..., help="The job ID to connect to"),
    remote_port: int = typer.Argument(..., help="Remote port on the VM to forward"),
    local_port: int | None = typer.Argument(None, help="Local port to listen on (defaults to remote_port)"),
    bind_address: str = typer.Option("127.0.0.1", "--bind", "-b", help="Local address to bind to"),
    no_verify: bool = typer.Option(False, "--no-verify", help="Skip SSL certificate verification"),
) -> None:
    """Open a local port forwarding tunnel to a VM.

    Creates a local TCP listener that forwards connections through the TLS
    gateway to the specified port on the remote VM.

    Arguments:
        job_id: Job ID of the VM to connect to
        remote_port: Port on the VM to forward to
        local_port: Local port to listen on (default: same as remote_port)

    Options:
        -b, --bind: Local address to bind to (default: 127.0.0.1)
        --no-verify: Skip SSL certificate verification
    """
    gateway_host, gateway_port = get_gateway_config()
    local = local_port or remote_port
    sni = f"{job_id}--{remote_port}.{gateway_host}"

    # Create local listener
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((bind_address, local))
        server.listen(5)
    except OSError as e:
        console.print(f"[red]Error: Could not bind to {bind_address}:{local}: {e}[/red]")
        raise typer.Exit(1) from None

    console.print(f"[green]Tunnel open:[/green] {bind_address}:{local} -> {job_id}:{remote_port}")
    console.print("[dim]Press Ctrl+C to stop[/dim]")

    def handle_client(client_sock: socket.socket, client_addr: tuple) -> None:
        """Handle a single client connection by forwarding to the VM."""
        try:
            # Connect to gateway via TLS
            gateway_sock = create_tls_connection(gateway_host, gateway_port, sni, verify_ssl=not no_verify)

            # Create bidirectional forwarding threads
            t1 = threading.Thread(
                target=forward_data,
                args=(client_sock, gateway_sock, "client->gateway"),
                daemon=True,
            )
            t2 = threading.Thread(
                target=forward_data,
                args=(gateway_sock, client_sock, "gateway->client"),
                daemon=True,
            )

            t1.start()
            t2.start()

            # Wait for both directions to complete
            t1.join()
            t2.join()

        except Exception as e:
            console.print(f"[red]Connection error: {e}[/red]")
        finally:
            try:
                client_sock.close()
            except OSError:
                pass

    try:
        while True:
            # Accept connections
            client_sock, client_addr = server.accept()
            console.print(f"[dim]Connection from {client_addr[0]}:{client_addr[1]}[/dim]")

            # Handle in a new thread
            thread = threading.Thread(
                target=handle_client,
                args=(client_sock, client_addr),
                daemon=True,
            )
            thread.start()

    except KeyboardInterrupt:
        console.print("\n[yellow]Tunnel closed[/yellow]")
    finally:
        server.close()


# Also expose ssh and tunnel as top-level commands (will be registered in main.py)
ssh_command = ssh
tunnel_command = tunnel
