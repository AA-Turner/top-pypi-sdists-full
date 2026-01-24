"""
CompZ CLI tools for command-line usage.

Provides compz-anchor and compz-verify commands.
"""

import typer
import json
import sys
import os
import time
import base64
import webbrowser
import threading
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import quote
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv
from .hash import hash_compliance, create_memo
from .normalize import normalize_json
from .pci.evaluator import PCIEvaluator

# Load environment variables
load_dotenv()

from .client import CompZClient

app = typer.Typer(
    name="compz",
    help="CompZ - Privacy-Preserving Compliance Attestation SDK",
    add_completion=False
)
console = Console()

PCI_APP = typer.Typer(name="pci", help="PCI-DSS Compliance tools")
app.add_typer(PCI_APP, name="pci")


@PCI_APP.command("list-policies")
def pci_list_policies():
    """List available PCI policy packs."""
    try:
        policies_dir = Path(__file__).parent / "pci" / "policies"
        items = sorted(policies_dir.glob("*.json"))
        if not items:
            console.print("[yellow]No PCI policies found.[/yellow]")
            raise typer.Exit(code=0)

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Policy ID")
        table.add_column("Name")
        table.add_column("Version")

        for p in items:
            try:
                data = json.loads(p.read_text())
                table.add_row(
                    data.get("id", p.stem),
                    data.get("name", ""),
                    data.get("version", "")
                )
            except Exception:
                table.add_row(p.stem, "<unreadable>", "")

        console.print(table)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@PCI_APP.command("check")
def pci_check(
    path: Path = typer.Argument(..., exists=True, help="Path to repository or directory to scan"),
    policy: str = typer.Option("pci-dss-basic", "--policy", "-p", help="Policy pack ID"),
    repo_id: str = typer.Option(None, "--repo", help="Repository/system identifier"),
    commit: str = typer.Option(None, "--commit", help="Commit hash or version"),
    output: Path = typer.Option(None, "--output", "-o", help="Save ComplianceResult JSON"),
):
    """Run PCI checks and produce a ComplianceResult JSON compatible with CompZ."""
    try:
        console.print("\n[bold]PCI-DSS Scan[/bold]")
        console.print(f"Path: [cyan]{path}[/cyan]  Policy: [magenta]{policy}[/magenta]")

        evaluator = PCIEvaluator(policy_id=policy)
        result = evaluator.evaluate(str(path), repo_id=repo_id, commit_hash=commit)

        # Summary table
        table = Table(show_header=False, box=None)
        table.add_row("[bold]Frameworks:[/bold]", ", ".join(result.frameworks))
        meta = result.metadata or {}
        table.add_row("[bold]Files Scanned:[/bold]", str(meta.get("scanned_files")))
        table.add_row("[bold]Controls Evaluated:[/bold]", str(meta.get("total_controls_evaluated")))
        table.add_row("[bold]Passed:[/bold]", str(meta.get("passed_controls")))
        table.add_row("[bold]Failed:[/bold]", str(meta.get("failed_controls")))
        table.add_row("[bold]Risk Score:[/bold]", f"{result.risk_score:.2f}")
        table.add_row("[bold]Timestamp:[/bold]", result.timestamp)
        console.print(table)

        # Show violations list
        if any(not ev.passed for ev in result.control_evaluations):
            console.print("\n[bold]Violations:[/bold]")
            vt = Table(show_header=True, header_style="bold red")
            vt.add_column("Control ID")
            vt.add_column("Severity")
            vt.add_column("Reason")
            for ev in result.control_evaluations:
                if not ev.passed:
                    vt.add_row(ev.control_id, ev.severity or "", ev.reason)
            console.print(vt)
        else:
            console.print("\n[green]No violations detected under selected policy.[/green]")

        # Write output if requested
        if output:
            with open(output, "w") as f:
                json.dump(result.model_dump(), f, indent=2)
            console.print(f"\n💾 Saved ComplianceResult to [cyan]{output}[/cyan]")
            console.print("Next: anchor on Zcash via Zashi:\n  compz pay " + str(output) + " --amount 0.0001 --serve --qr")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def anchor(
    file: Path = typer.Argument(
        ...,
        help="Path to compliance JSON file",
        exists=True
    ),
    wait: bool = typer.Option(
        False,
        "--wait",
        "-w",
        help="Wait for blockchain confirmation"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Save result to file"
    ),
    mode: Optional[str] = typer.Option(
        None,
        "--mode",
        "-m",
        help="Mode: 'demo' or 'self-hosted'"
    )
):
    """
    Anchor compliance data to Zcash blockchain.
    
    Examples:
        compz anchor compliance.json
        compz anchor compliance.json --wait
        compz anchor compliance.json --mode demo
        compz anchor compliance.json -o result.json
    """
    try:
        # Load compliance data
        with console.status("[bold green]Loading compliance data..."):
            with open(file) as f:
                data = json.load(f)
        
        console.print(f"📄 Loaded: [cyan]{file}[/cyan]")
        console.print(f"📊 Size: [yellow]{file.stat().st_size}[/yellow] bytes")
        
        # Initialize client
        kwargs = {}
        if mode:
            kwargs['mode'] = mode
        
        client = CompZClient(**kwargs)
        
        # Anchor
        with console.status("[bold green]Anchoring to blockchain..."):
            result = client.anchor(data, wait_for_confirmation=wait)
        
        # Display result
        console.print("\n[bold green]✅ Successfully anchored![/bold green]\n")
        
        table = Table(show_header=False, box=None)
        table.add_row("[bold]Hash:[/bold]", f"[cyan]{result.hash}[/cyan]")
        table.add_row("[bold]TXID:[/bold]", f"[yellow]{result.txid}[/yellow]")
        table.add_row("[bold]Network:[/bold]", f"[blue]{result.network}[/blue]")
        table.add_row("[bold]Mode:[/bold]", f"[magenta]{result.mode}[/magenta]")
        table.add_row("[bold]Timestamp:[/bold]", f"[green]{result.timestamp}[/green]")
        
        if result.explorer_url:
            table.add_row("[bold]Explorer:[/bold]", f"[link={result.explorer_url}]{result.explorer_url}[/link]")
        
        console.print(table)
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(result.model_dump(), f, indent=2)
            console.print(f"\n💾 Result saved to: [cyan]{output}[/cyan]")
        
        # Success exit
        sys.exit(0)
    
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        sys.exit(1)


@app.command()
def pay(
    file: Path = typer.Argument(
        ...,
        help="Path to compliance JSON file",
        exists=True
    ),
    address: Optional[str] = typer.Option(
        None,
        "--address",
        "-a",
        help="Recipient Zcash unified address (defaults to ZCASH_DEFAULT_ADDRESS)"
    ),
    amount: float = typer.Option(
        0.0001,
        "--amount",
        "-n",
        help="Amount in ZEC (up to 8 decimals)"
    ),
    label: Optional[str] = typer.Option(
        "CompZ Attestation",
        "--label",
        "-l",
        help="Payment label (optional)"
    ),
    open_link: bool = typer.Option(
        False,
        "--open",
        help="Attempt to open the zcash: link on this machine"
    ),
    qr: bool = typer.Option(
        False,
        "--qr",
        help="Render a QR code if the 'qrcode' package is installed"
    ),
    serve: bool = typer.Option(
        False,
        "--serve",
        help="Serve a temporary browser URL that redirects to the zcash: link"
    ),
    host: str = typer.Option(
        "0.0.0.0",
        "--host",
        help="Host to bind the temporary server (use 0.0.0.0 to share on LAN)"
    ),
    port: int = typer.Option(
        8765,
        "--port",
        help="Port for the temporary server (0 = random)"
    ),
    duration: int = typer.Option(
        120,
        "--serve-seconds",
        help="How long to keep the server running (seconds)"
    )
):
    """
    Generate a real Zcash payment deep link (ZIP-321) with the CompZ memo.

    This pre-fills the recipient, amount, and memo in Zashi or any ZIP-321 wallet.

    Example:
        compz pay examples/compliance_result.json --amount 0.0001 --qr
    """
    try:
        # Determine recipient address
        recipient = address or os.getenv("ZCASH_DEFAULT_ADDRESS")
        if not recipient:
            console.print("[red]❌ No recipient address provided.[/red]")
            console.print("Set --address or ZCASH_DEFAULT_ADDRESS in .env")
            raise typer.Exit(code=1)
        # Sanitize: remove any whitespace/newlines accidentally pasted
        recipient = "".join(str(recipient).split())

        # Load compliance data
        with console.status("[bold green]Loading compliance data..."):
            with open(file) as f:
                data = json.load(f)

        # Compute memo from normalized hash
        normalized = normalize_json(data)
        comp_hash = hash_compliance(normalized)
        memo_text = create_memo(comp_hash)  # e.g., "compz:v1:<hash>"

        # Base64url encode memo (no padding) per ZIP-321
        memo_b64url = base64.urlsafe_b64encode(memo_text.encode("utf-8")).decode("ascii").rstrip("=")

        # Amount formatting (up to 8 decimals)
        amt = f"{amount:.8f}".rstrip('0').rstrip('.') if amount is not None else None

        # Build ZIP-321 URI
        params = []
        if amt:
            params.append(f"amount={amt}")
        params.append(f"memo={memo_b64url}")
        if label:
            params.append(f"label={quote(label)}")

        uri = f"zcash:{recipient}?" + "&".join(params)

        console.print("\n[bold]✅ ZIP-321 Payment Link[/bold]")
        console.print(f"[link={uri}]{uri}[/link]")

        # Optionally open the link (useful if a desktop wallet handles zcash:) 
        if open_link:
            try:
                webbrowser.open(uri)
                console.print("\n[green]Attempted to open the zcash: link.[/green]")
            except Exception:
                console.print("[yellow]Could not open link automatically on this device.[/yellow]")

        # Optionally render QR for direct zcash: link (when not serving a browser URL)
        if qr and not serve:
            try:
                import qrcode
                qr_img = qrcode.make(uri)
                out_png = Path.cwd() / "compz_payment_qr.png"
                qr_img.save(out_png)
                console.print(f"\n🖼️  QR saved: [cyan]{out_png}[/cyan]")
                console.print("Scan this QR in Zashi to prefill the transaction.")
            except Exception:
                console.print("[yellow]QR generation requires 'qrcode' package. Install:[/yellow] \n  pip install qrcode pillow")

        # Serve a browser URL that redirects to the zcash: link
        if serve:
            def _get_local_ip() -> str:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    ip = s.getsockname()[0]
                    s.close()
                    return ip
                except Exception:
                    return "127.0.0.1"

            class _DLHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    html = (
                        "<!doctype html><html><head><meta charset='utf-8'>"
                        f"<meta http-equiv='refresh' content='0; url={uri}'>"
                        "<title>Open Zcash Wallet</title>"
                        "</head><body>"
                        "<h3>Opening your Zcash wallet…</h3>"
                        f"<p>If nothing happens, <a href='{uri}'>tap here</a>.</p>"
                        "</body></html>"
                    )
                    body = html.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)

                def log_message(self, format, *args):
                    # Silence default HTTP server logs
                    return

            try:
                httpd = HTTPServer((host, port), _DLHandler)
                actual_port = httpd.server_address[1]
                ip = _get_local_ip() if host in ("0.0.0.0", "") else host
                http_url = f"http://{ip}:{actual_port}/"

                console.print("\n[bold]🌐 Browser URL[/bold]")
                console.print(f"[link={http_url}]{http_url}[/link]")

                # Start server in background
                th = threading.Thread(target=httpd.serve_forever, daemon=True)
                th.start()

                if open_link:
                    try:
                        webbrowser.open(http_url)
                    except Exception:
                        pass

                # If QR requested, generate QR for the browser URL
                if qr:
                    try:
                        import qrcode
                        qr_img = qrcode.make(http_url)
                        out_png = Path.cwd() / "compz_payment_qr.png"
                        qr_img.save(out_png)
                        console.print(f"\n🖼️  QR saved: [cyan]{out_png}[/cyan]")
                        console.print("Scan this QR to open the browser, which redirects to Zashi.")
                    except Exception:
                        console.print("[yellow]QR generation requires 'qrcode' package. Install:[/yellow] \n  pip install qrcode pillow")

                console.print(f"\n⏳ Serving for {duration}s (Ctrl+C to stop)…")
                try:
                    time.sleep(duration)
                finally:
                    httpd.shutdown()
                    th.join(timeout=2)
            except Exception as se:
                console.print(f"[yellow]Couldn't start local server: {se}[/yellow]")

        # Show memo and hash to the user
        console.print("\n[bold]📝 Memo:[/bold] " + memo_text)
        console.print("[bold]🔐 Hash:[/bold] " + comp_hash)

        console.print("\n[green]Next:[/green] Scan the QR or open the link on your phone, then send.\n"
                       "After sending, run:\n  compz verify " + str(file) + " <txid>")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        sys.exit(1)

@app.command()
def verify(
    file: Path = typer.Argument(
        ...,
        help="Path to compliance JSON file",
        exists=True
    ),
    txid: str = typer.Argument(
        ...,
        help="Zcash transaction ID to verify against"
    ),
    mode: Optional[str] = typer.Option(
        None,
        "--mode",
        "-m",
        help="Mode: 'demo' or 'self-hosted'"
    )
):
    """
    Verify compliance data against blockchain transaction.
    
    Examples:
        compz verify compliance.json 9c8f7e6d5c4b3a2...
        compz verify compliance.json <txid> --mode demo
    """
    try:
        # Load compliance data
        with console.status("[bold green]Loading compliance data..."):
            with open(file) as f:
                data = json.load(f)
        
        console.print(f"📄 Loaded: [cyan]{file}[/cyan]")
        
        # Initialize client
        kwargs = {}
        if mode:
            kwargs['mode'] = mode
        
        client = CompZClient(**kwargs)
        
        # Verify
        with console.status("[bold green]Verifying against blockchain..."):
            result = client.verify(data, txid)
        
        # Display result
        if result.valid:
            console.print("\n[bold green]✅ VALID - Compliance data matches blockchain![/bold green]\n")
        else:
            console.print("\n[bold red]❌ INVALID - Verification failed![/bold red]\n")
        
        table = Table(show_header=False, box=None)
        table.add_row("[bold]Status:[/bold]", 
                     f"[green]VALID[/green]" if result.valid else f"[red]INVALID[/red]")
        table.add_row("[bold]Local Hash:[/bold]", f"[cyan]{result.local_hash}[/cyan]")
        table.add_row("[bold]On-chain Hash:[/bold]", f"[cyan]{result.onchain_hash}[/cyan]")
        table.add_row("[bold]TXID:[/bold]", f"[yellow]{result.txid}[/yellow]")
        table.add_row("[bold]Reason:[/bold]", f"[white]{result.reason}[/white]")
        
        if result.block_time:
            table.add_row("[bold]Block Time:[/bold]", f"[green]{result.block_time}[/green]")
        
        if result.confirmations is not None:
            table.add_row("[bold]Confirmations:[/bold]", f"[blue]{result.confirmations}[/blue]")
        
        console.print(table)
        
        # Exit with appropriate code
        sys.exit(0 if result.valid else 1)
    
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        sys.exit(1)


@app.command()
def status():
    """
    Show CompZ SDK status and configuration.
    """
    try:
        client = CompZClient()
        status_info = client.get_status()
        
        console.print("\n[bold]CompZ SDK Status[/bold]\n")
        
        table = Table(show_header=False, box=None)
        table.add_row("[bold]Version:[/bold]", f"[cyan]{status_info['version']}[/cyan]")
        table.add_row("[bold]Mode:[/bold]", f"[magenta]{status_info['mode']}[/magenta]")
        
        if status_info['mode'] == 'local-only':
            table.add_row("[bold]Blockchain:[/bold]", f"[yellow]Not connected[/yellow]")
            table.add_row("[bold]Hashing:[/bold]", f"[green]{status_info['hashing']}[/green]")
            table.add_row("[bold]Verification:[/bold]", f"[green]{status_info['verification']}[/green]")
            console.print(table)
            console.print()
            console.print(f"[yellow]💡 {status_info['note']}[/yellow]")
            console.print()
        elif status_info['mode'] == 'blockchain-readonly':
            table.add_row("[bold]Blockchain:[/bold]", f"[green]Connected ✅ (Read-Only)[/green]")
            table.add_row("[bold]Network:[/bold]", f"[blue]{status_info['network']}[/blue]")
            table.add_row("[bold]Access:[/bold]", f"[cyan]{status_info['blockchain_access']}[/cyan]")
            table.add_row("[bold]Hashing:[/bold]", f"[green]{status_info['hashing']}[/green]")
            table.add_row("[bold]Verification:[/bold]", f"[green]{status_info['verification']}[/green]")
            table.add_row("[bold]Sending:[/bold]", f"[yellow]{status_info['sending']}[/yellow]")
            console.print(table)
            console.print()
            console.print(f"[green]✅ {status_info['note']}[/green]")
            console.print()
        else:
            table.add_row("[bold]Blockchain:[/bold]", f"[green]Connected ✅[/green]")
            table.add_row("[bold]Network:[/bold]", f"[blue]{status_info['network']}[/blue]")
            table.add_row("[bold]RPC URL:[/bold]", f"[yellow]{status_info['rpc_url']}[/yellow]")
            if status_info.get('address'):
                table.add_row("[bold]Address:[/bold]", f"[green]{status_info['address']}[/green]")
            console.print(table)
            console.print()
    
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        sys.exit(1)


@app.command()
def version():
    """Show CompZ version."""
    console.print("[bold cyan]CompZ SDK v1.0.0[/bold cyan]")
    console.print("Privacy-Preserving Compliance Attestation")
    console.print("https://github.com/Compliledger/CompZ")


def main():
    """Main entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
