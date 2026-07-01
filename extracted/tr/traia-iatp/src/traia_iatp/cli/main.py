"""IATP CLI interface."""

import asyncio
import csv
import json
from pathlib import Path
from typing import Optional, List
import typer
from eth_account import Account
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from pydantic import HttpUrl

from ..core.models import MCPServer, MCPServerType, UtilityAgent
from ..server.iatp_server_agent_generator import IATPServerAgentGenerator
from ..registry.mongodb_registry import UtilityAgentRegistry, MCPServerRegistry
from ..utils.docker_utils import use_run_local_docker_script, LocalDockerRunner
from ..client.a2a_client import create_utility_agency_tools
from ..contracts.wallet_creator import create_iatp_wallet
from ..d402.clients.base import decode_x_payment_response
from ..d402.clients.httpx import d402HttpxClient
from ..mcp.mcp_server_template_generator import MCPServerTemplateGenerator, LocalMCPServerConfig, LocalMCPEndpoint

app = typer.Typer(
    name="iatp",
    help="Inter Agent Transfer Protocol - Enable AI Agents to utilize other AI Agents as tools"
)
console = Console()


def _normalize_mcp_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/mcp"):
        normalized = normalized[:-4]
    return normalized


def _parse_mcp_response_text(response_text: str):
    content = response_text.strip()
    if not content:
        return {}

    if "data:" in content:
        for line in content.splitlines():
            if line.startswith("data:"):
                data = line[5:].strip()
                if data:
                    return json.loads(data)

    return json.loads(content)


def _parse_multi_value_option(values: Optional[List[str]]) -> list[str]:
    if not values:
        return []

    def _parse_csv_parts(raw_value: str) -> list[str]:
        preferred_quotechars: list[str] = []
        if '"' in raw_value:
            preferred_quotechars.append('"')
        if "'" in raw_value:
            preferred_quotechars.append("'")
        if not preferred_quotechars:
            preferred_quotechars.append('"')

        for quotechar in preferred_quotechars:
            try:
                return next(csv.reader([raw_value], skipinitialspace=True, quotechar=quotechar))
            except csv.Error:
                continue

        return raw_value.split(",")

    parsed: list[str] = []
    for value in values:
        for part in _parse_csv_parts(value):
            cleaned = part.strip()
            if cleaned:
                parsed.append(cleaned)
    return parsed


def _hex_key(key) -> str:
    """Normalise an eth_account key to a 0x-prefixed hex string."""
    raw = key.hex() if hasattr(key, "hex") else str(key)
    return raw if raw.startswith("0x") else f"0x{raw}"


@app.command(name="print-skill")
def print_skill():
    """Print the traia-iatp agent skill to stdout.

    Pipe this into your agent context to give it full knowledge of every
    command, workflow, and key concept:

      traia-iatp print-skill

    The skill is bundled with the package so it is always in sync with the
    installed version.
    """
    from importlib.resources import files
    try:
        skill_text = (files("traia_iatp") / "SKILL.md").read_text(encoding="utf-8")
        console.print(skill_text)
    except FileNotFoundError:
        console.print("❌ SKILL.md not found in package.", style="bold red")
        raise typer.Exit(code=1)


@app.command(name="create-eth-wallet")
def create_eth_wallet(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Save wallet info to JSON file"),
):
    """Generate a plain ETH keypair with no on-chain transaction.

    Use this to get an address you can fund with ETH before creating an IATP wallet.

    Example:
      traia-iatp create-eth-wallet
    """
    account = Account.create()
    wallet = {
        "privateKey": _hex_key(account.key),
        "address": account.address,
    }
    console.print("\n🔑 New ETH Wallet", style="bold")
    console.print(json.dumps(wallet, indent=2))
    console.print("\n⚠️  Save the private key securely. It cannot be recovered.", style="yellow")
    console.print(
        f"\nFund {account.address} with at least 0.001 ETH on arbitrum_one before creating an IATP wallet.",
        style="dim",
    )
    console.print(
        "Then run: traia-iatp create-iatp-wallet --owner-key <privateKey> --wallet-type CLIENT",
        style="dim",
    )
    if output:
        with open(output, "w") as f:
            json.dump(wallet, f, indent=2)
        console.print(f"\n💾 Saved to: {output}", style="green")


@app.command(name="create-iatp-wallet")
def create_wallet_cli(
    owner_key: Optional[str] = typer.Option(None, "--owner-key", help="Owner private key. Owner pays gas if no --maintainer-key is given."),
    maintainer_key: Optional[str] = typer.Option(None, "--maintainer-key", help="Funded ETH key that pays gas. Enables generating a fresh owner wallet at no cost to the owner."),
    wallet_name: str = typer.Option("", "--wallet-name", help="Name for the wallet"),
    wallet_type: str = typer.Option("CLIENT", "--wallet-type", help="CLIENT (for d402HttpxClient calls) or HUMAN (for local direct calls)"),
    wallet_description: str = typer.Option("", "--wallet-description", help="Description of the wallet"),
    network: str = typer.Option("arbitrum_one", "--network", help="Network to deploy on"),
    rpc_url: Optional[str] = typer.Option(None, "--rpc-url", help="Custom RPC URL"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Save wallet info to JSON file"),
):
    """Deploy a CLIENT or HUMAN IATP wallet on-chain.

    Gas payment options:

      1. Owner pays — pass --owner-key with a funded ETH wallet:
           traia-iatp create-iatp-wallet --owner-key 0x... --wallet-type CLIENT

      2. Maintainer pays — pass --maintainer-key with a funded ETH wallet.
         The owner and operator are generated fresh (or supply --owner-key for a specific owner):
           traia-iatp create-iatp-wallet --maintainer-key 0x... --wallet-type CLIENT

      3. Generate keys first, fund, then create:
           traia-iatp create-eth-wallet          # get an address
           # fund the address with 0.001+ ETH
           traia-iatp create-iatp-wallet --owner-key <privateKey> --wallet-type CLIENT
    """
    try:
        if wallet_type.upper() not in {"CLIENT", "HUMAN", "MCP_SERVER", "WEB_SERVER", "AGENT"}:
            raise typer.BadParameter("wallet-type must be one of: CLIENT, HUMAN, MCP_SERVER, WEB_SERVER, AGENT")

        # Require at least one funded-key path.
        if not owner_key and not maintainer_key:
            console.print("\n❌ Provide at least one of:", style="bold red")
            console.print("  --owner-key <funded ETH key>      owner pays gas")
            console.print("  --maintainer-key <funded ETH key> maintainer pays gas, fresh owner generated")
            console.print("\nTo generate a new ETH address to fund first:")
            console.print("  traia-iatp create-eth-wallet")
            raise typer.Exit(code=1)

        # Resolve owner account.
        if owner_key:
            owner_account = Account.from_key(owner_key)
            generated_owner = False
        else:
            # maintainer pays — generate fresh owner
            owner_account = Account.create()
            owner_key = _hex_key(owner_account.key)
            generated_owner = True

        # Always generate a fresh operator.
        operator_account = Account.create()

        # Print credentials before the on-chain call so they are visible even if the tx fails.
        credentials: dict = {
            "privateKey": owner_key if owner_key.startswith("0x") else f"0x{owner_key}",
            "address": owner_account.address,
            "operatorPrivateKey": _hex_key(operator_account.key),
            "operatorAddress": operator_account.address,
        }
        if generated_owner:
            console.print("\n🔑 Generated Owner + Operator", style="bold")
        else:
            console.print("\n🔑 Wallet Credentials", style="bold")
        console.print(json.dumps(credentials, indent=2))

        # Deploy on-chain.
        console.print("\n🔧 Deploying IATP wallet on-chain...\n", style="bold")
        result = create_iatp_wallet(
            owner_private_key=owner_key,
            operator_address=operator_account.address,
            create_operator=False,
            wallet_name=wallet_name,
            wallet_type=wallet_type,
            wallet_description=wallet_description,
            network=network,
            rpc_url=rpc_url,
            maintainer_private_key=maintainer_key,
        )

        credentials["iatpWalletAddress"] = result["wallet_address"]

        console.print("\n✅ IATP Wallet Created", style="bold green")
        console.print(json.dumps(credentials, indent=2))

        if output:
            with open(output, "w") as f:
                json.dump(credentials, f, indent=2)
            console.print(f"\n💾 Saved to: {output}", style="green")

        wallet_type_upper = wallet_type.upper()
        console.print("\n📝 Next Steps:", style="bold")
        console.print("1. Save these credentials securely.")
        console.print("2. Fund iatpWalletAddress with USDC (or your settlement token) before testing payments.")
        if wallet_type_upper in {"CLIENT", "HUMAN"}:
            console.print("3. Set environment variables for payment testing:")
            console.print(f"   export CLIENT_OPERATOR_PRIVATE_KEY={credentials['operatorPrivateKey']}")
            console.print(f"   export CLIENT_WALLET_ADDRESS={credentials['iatpWalletAddress']}")
            console.print("4. Create your MCP server repo with `create-mcp --server-wallet-owner-key <privateKey>`")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")
        import traceback
        console.print(traceback.format_exc(), style="red")
        raise typer.Exit(code=1)


@app.command(name="create-mcp")
def create_mcp(
    name: str = typer.Option(..., "--name", help="Human-readable MCP server name"),
    api_url: str = typer.Option(..., "--api-url", help="Base URL of the upstream API"),
    endpoint_path: Optional[List[str]] = typer.Option(None, "--endpoint-path", help="Endpoint path(s); repeat the flag or separate values with commas"),
    endpoint_name: Optional[List[str]] = typer.Option(None, "--endpoint-name", help="Tool name(s); repeat the flag or separate values with commas"),
    description: Optional[List[str]] = typer.Option(None, "--description", help="Optional endpoint description(s); repeat the flag or separate values with commas"),
    price_usd: float = typer.Option(..., "--price-usd", help="Price per call in token units, for example 0.01"),
    method: Optional[List[str]] = typer.Option(None, "--method", help="HTTP method(s); repeat the flag or separate values with commas"),
    docs_url: Optional[str] = typer.Option(None, "--docs-url", help="Documentation URL for the upstream API"),
    sdk_package: Optional[str] = typer.Option(None, "--sdk-package", help="Optional extra SDK package dependency to add"),
    requires_auth: bool = typer.Option(False, "--requires-auth", help="Whether the upstream API requires an API key"),
    api_key_env: Optional[str] = typer.Option(None, "--api-key-env", help="Environment variable name for the upstream API key"),
    api_key_header: str = typer.Option("Bearer", "--api-key-header", help="Authorization header mode: Bearer, X-API-Key, or a custom header name"),
    server_wallet_owner_key: Optional[str] = typer.Option(None, "--server-wallet-owner-key", help="Owner private key used to create the MCP server wallet (owner pays gas)"),
    maintainer_key: Optional[str] = typer.Option(None, "--maintainer-key", help="Funded ETH key that pays gas for server wallet creation. A fresh server owner is generated when this is used without --server-wallet-owner-key."),
    server_address: Optional[str] = typer.Option(None, "--server-address", help="Existing MCP server wallet address"),
    operator_address: Optional[str] = typer.Option(None, "--operator-address", help="Existing operator address"),
    operator_private_key: Optional[str] = typer.Option(None, "--operator-private-key", help="Existing operator private key"),
    network: str = typer.Option("arbitrum_one", "--network", help="Settlement network"),
    token_symbol: str = typer.Option("USDC", "--token-symbol", help="Settlement token symbol: USDC or USDT"),
    facilitator_url: str = typer.Option("https://facilitator.d402.net", "--facilitator-url", help="Facilitator URL for paid requests"),
    testing_mode: bool = typer.Option(True, "--testing-mode/--no-testing-mode", help="Enable local verification without settlement"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", help="Directory where the generated MCP repo will be written"),
    boilerplate_only: bool = typer.Option(False, "--boilerplate-only", help="Generate the MCP scaffold with sample commented tools and no concrete endpoints"),
    endpoints_file: Optional[Path] = typer.Option(None, "--endpoints-file", help="Path to an endpoints.json file (OpenAPI-style). Each entry must have endpoint_path, endpoint_name, endpoint_method; optionally endpoint_description, endpoint_input_schema, payment_price_float."),
):
    """Create a local MCP repo for rapid d402 testing."""
    # Resolve output dir at call time so it reflects the user's actual CWD.
    if output_dir is None:
        output_dir = Path.cwd()
    try:
        # ------------------------------------------------------------------
        # Resolve endpoint definitions
        # Either from --endpoints-file (rich, schema-aware) or from the
        # individual --endpoint-name / --endpoint-path / ... flags.
        # ------------------------------------------------------------------
        endpoint_schemas: list = []
        endpoint_prices: list = []

        if endpoints_file:
            if not endpoints_file.exists():
                raise typer.BadParameter(f"endpoints-file not found: {endpoints_file}")
            raw_entries = json.loads(endpoints_file.read_text())
            if not isinstance(raw_entries, list) or not raw_entries:
                raise typer.BadParameter("endpoints-file must be a non-empty JSON array")
            endpoint_names  = [e["endpoint_name"] for e in raw_entries]
            endpoint_paths  = [e["endpoint_path"] for e in raw_entries]
            methods         = [e.get("endpoint_method", "POST").upper() for e in raw_entries]
            descriptions    = [e.get("endpoint_description") or None for e in raw_entries]
            endpoint_schemas = [
                e.get("endpoint_input_schema") or e.get("input_schema") or None
                for e in raw_entries
            ]
            endpoint_prices = [e.get("payment_price_float") for e in raw_entries]
        else:
            endpoint_names = _parse_multi_value_option(endpoint_name)
            endpoint_paths = _parse_multi_value_option(endpoint_path)
            methods = [value.upper() for value in _parse_multi_value_option(method)] or ["GET"]
            descriptions = _parse_multi_value_option(description)
            endpoint_schemas = [None] * max(len(endpoint_names), 1)
            endpoint_prices  = [None] * max(len(endpoint_names), 1)

        if token_symbol.upper() not in {"USDC", "USDT"}:
            raise typer.BadParameter("token-symbol must be USDC or USDT")

        if network != "arbitrum_one":
            raise typer.BadParameter("This command currently supports only arbitrum_one")

        if not boilerplate_only:
            if not endpoint_names or not endpoint_paths:
                raise typer.BadParameter(
                    "Provide --endpoint-name and --endpoint-path, --endpoints-file, or use --boilerplate-only"
                )
            if len(endpoint_names) != len(endpoint_paths):
                raise typer.BadParameter("--endpoint-name and --endpoint-path must have the same number of values")
            if not endpoints_file:
                # Extra validation only needed for flag-based input
                if len(methods) not in {1, len(endpoint_names)}:
                    raise typer.BadParameter("Provide one --method for all endpoints or one method per endpoint")
                if any(value not in {"GET", "POST"} for value in methods):
                    raise typer.BadParameter("Only GET and POST are currently supported")
                if len(descriptions) not in {0, 1, len(endpoint_names)}:
                    raise typer.BadParameter(
                        "Provide no --description, one description for all endpoints, or one description per endpoint"
                    )
        else:
            endpoint_names   = []
            endpoint_paths   = []
            descriptions     = []
            endpoint_schemas = []
            endpoint_prices  = []

        if not endpoints_file:
            if len(methods) == 1 and endpoint_names:
                methods = methods * len(endpoint_names)
            if len(descriptions) == 1 and endpoint_names:
                descriptions = descriptions * len(endpoint_names)
            if not descriptions and endpoint_names:
                descriptions = [None] * len(endpoint_names)

        server_description = descriptions[0] if descriptions else ""

        endpoints = [
            LocalMCPEndpoint(
                endpoint_name=endpoint_names[index],
                endpoint_path=endpoint_paths[index],
                method=methods[index],
                description=descriptions[index] if descriptions else None,
                input_schema=endpoint_schemas[index] if index < len(endpoint_schemas) else None,
                price_usd=endpoint_prices[index] if index < len(endpoint_prices) else None,
            )
            for index in range(len(endpoint_names))
        ]

        has_existing_wallet = all([server_address, operator_address, operator_private_key])

        if has_existing_wallet:
            # Use pre-existing wallet credentials — nothing to deploy.
            pass
        else:
            # Need to deploy a new MCP_SERVER wallet.
            # Three gas-payment paths (mirror create-iatp-wallet):
            #   1. --server-wallet-owner-key supplied → owner pays gas
            #   2. --maintainer-key supplied → maintainer pays gas, fresh owner generated (or use
            #      --server-wallet-owner-key for a specific owner without needing it to hold ETH)
            #   3. Neither supplied → print instructions and exit cleanly

            if not server_wallet_owner_key and not maintainer_key:
                console.print("\n❌ A funded ETH key is required to deploy the server wallet.", style="bold red")
                console.print("\n  Option A — owner pays gas:")
                console.print("    --server-wallet-owner-key <funded ETH private key>")
                console.print("\n  Option B — maintainer pays gas (generates fresh server owner):")
                console.print("    --maintainer-key <funded ETH private key>")
                console.print("\n  Option C — reuse an existing wallet (no on-chain call):")
                console.print("    --server-address <addr> --operator-address <addr> --operator-private-key <key>")
                console.print("\nTo generate a fresh ETH address to fund:")
                console.print("  traia-iatp create-eth-wallet")
                raise typer.Exit(code=1)

            if server_wallet_owner_key:
                server_owner_account = Account.from_key(server_wallet_owner_key)
                generated_server_owner = False
            else:
                # maintainer pays — generate fresh server owner
                server_owner_account = Account.create()
                server_wallet_owner_key = _hex_key(server_owner_account.key)
                generated_server_owner = True

            server_operator_account = Account.create()

            # Show server credentials before the on-chain call.
            server_credentials = {
                "privateKey": server_wallet_owner_key if server_wallet_owner_key.startswith("0x") else f"0x{server_wallet_owner_key}",
                "address": server_owner_account.address,
                "operatorPrivateKey": _hex_key(server_operator_account.key),
                "operatorAddress": server_operator_account.address,
            }
            if generated_server_owner:
                console.print("\n🔑 Generated Server Owner + Operator", style="bold")
            else:
                console.print("\n🔑 Server Wallet Credentials", style="bold")
            console.print(json.dumps(server_credentials, indent=2))

            console.print("\n🔧 Deploying MCP server wallet on-chain...\n", style="bold")
            wallet_result = create_iatp_wallet(
                owner_private_key=server_wallet_owner_key,
                operator_address=server_operator_account.address,
                create_operator=False,
                wallet_name=name,
                wallet_type="MCP_SERVER",
                wallet_description=server_description,
                network=network,
                maintainer_private_key=maintainer_key,
            )
            server_address = wallet_result["wallet_address"]
            operator_address = server_operator_account.address
            operator_private_key = _hex_key(server_operator_account.key)

        generator = MCPServerTemplateGenerator()
        config = LocalMCPServerConfig(
            api_name=name,
            api_url=api_url,
            description=server_description,
            price_usd=price_usd,
            requires_auth=requires_auth,
            api_key_env=api_key_env,
            api_key_header=api_key_header,
            output_dir=output_dir,
            docs_url=docs_url,
            sdk_package=sdk_package,
            server_address=server_address,
            operator_address=operator_address,
            operator_private_key=operator_private_key,
            network=network,
            token_symbol=token_symbol.upper(),
            facilitator_url=facilitator_url,
            testing_mode=testing_mode,
            endpoints=endpoints,
            boilerplate_only=boilerplate_only,
        )
        repo_path = generator.create_local_repo(config)

        console.print("\n✅ Created local MCP repo", style="bold green")
        console.print(f"   Folder: {repo_path}")
        if endpoints:
            console.print(f"   Tools: {', '.join(endpoint.endpoint_name for endpoint in endpoints)}")
            console.print(f"   Paths: {', '.join(endpoint.endpoint_path for endpoint in endpoints)}")
        else:
            console.print("   Tools: boilerplate only")
        console.print(f"   Price: {price_usd:.6f} {token_symbol.upper()} per call")
        console.print(f"   Settlement token: {token_symbol.upper()}")
        console.print(f"   Network: {network}")
        console.print(f"   Testing mode: {'enabled' if testing_mode else 'disabled'}")

        console.print("\n🔑 Server Wallet", style="bold")
        console.print(json.dumps({
            "iatpWalletAddress": server_address,
            "operatorAddress": operator_address,
            "operatorPrivateKey": operator_private_key,
        }, indent=2))
        console.print("\n   The server wallet is wired into the generated .env automatically.")
        console.print("   The client wallet (for test-mcp / d402HttpxClient) is separate.")
        console.print("   Create it with: traia-iatp create-iatp-wallet --wallet-type CLIENT")

        console.print("\n📝 Next Steps:", style="bold")
        console.print(f"1. cd {repo_path}")
        console.print("2. Review `.env` and add your upstream API key if required")
        console.print("3. Start with Docker: `./run_local_docker.sh`")
        console.print("4. Or run directly: `uv run python server.py`")
        console.print("5. Test from CLI with `traia-iatp test-mcp`")
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")
        import traceback
        console.print(traceback.format_exc(), style="red")
        raise typer.Exit(code=1)


@app.command(name="create-mcp-template")
def create_mcp_template(
    name: str = typer.Option(..., "--name", help="Human-readable MCP server name"),
    api_url: str = typer.Option(..., "--api-url", help="Base URL of the upstream API"),
    description: Optional[str] = typer.Option(None, "--description", help="Optional server description"),
    price_usd: float = typer.Option(0.01, "--price-usd", help="Default price per call (placeholder; tune in generated code)"),
    docs_url: Optional[str] = typer.Option(None, "--docs-url", help="Documentation URL for the upstream API"),
    sdk_package: Optional[str] = typer.Option(None, "--sdk-package", help="Optional extra SDK package dependency to add"),
    requires_auth: bool = typer.Option(False, "--requires-auth", help="Whether the upstream API requires an API key"),
    api_key_env: Optional[str] = typer.Option(None, "--api-key-env", help="Environment variable name for the upstream API key"),
    api_key_header: str = typer.Option("Bearer", "--api-key-header", help="Authorization header mode: Bearer, X-API-Key, or a custom header name"),
    network: str = typer.Option("arbitrum_one", "--network", help="Settlement network"),
    token_symbol: str = typer.Option("USDC", "--token-symbol", help="Settlement token symbol: USDC or USDT"),
    facilitator_url: str = typer.Option("https://facilitator.d402.net", "--facilitator-url", help="Facilitator URL for paid requests"),
    testing_mode: bool = typer.Option(True, "--testing-mode/--no-testing-mode", help="Enable local verification without settlement"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-o", help="Directory where the generated MCP repo will be written. Defaults to the current working directory."),
):
    """Internal: generate the MCP boilerplate scaffold with no server wallet.

    Same scaffold as `create-mcp --boilerplate-only`, but skips on-chain wallet
    deployment entirely. The generated `.env` leaves SERVER_ADDRESS,
    MCP_OPERATOR_ADDRESS, and MCP_OPERATOR_PRIVATE_KEY empty — populate them at
    deployment time. Intended for internal use; the public-facing flow remains
    `create-mcp --boilerplate-only`.
    """
    if output_dir is None:
        output_dir = Path.cwd()
    try:
        if token_symbol.upper() not in {"USDC", "USDT"}:
            raise typer.BadParameter("token-symbol must be USDC or USDT")

        if network != "arbitrum_one":
            raise typer.BadParameter("This command currently supports only arbitrum_one")

        generator = MCPServerTemplateGenerator()
        config = LocalMCPServerConfig(
            api_name=name,
            api_url=api_url,
            description=description or "",
            price_usd=price_usd,
            requires_auth=requires_auth,
            api_key_env=api_key_env,
            api_key_header=api_key_header,
            output_dir=output_dir,
            docs_url=docs_url,
            sdk_package=sdk_package,
            server_address="",
            operator_address="",
            operator_private_key="",
            network=network,
            token_symbol=token_symbol.upper(),
            facilitator_url=facilitator_url,
            testing_mode=testing_mode,
            endpoints=[],
            boilerplate_only=True,
        )
        repo_path = generator.create_local_repo(config)

        console.print("\n✅ Created MCP boilerplate template (no server wallet)", style="bold green")
        console.print(f"   Folder: {repo_path}")
        console.print(f"   Settlement token: {token_symbol.upper()}")
        console.print(f"   Network: {network}")
        console.print(f"   Testing mode: {'enabled' if testing_mode else 'disabled'}")

        console.print(
            "\n⚠️  No server wallet was deployed — `.env` server credentials are empty.",
            style="yellow",
        )
        console.print(
            "   Populate SERVER_ADDRESS, MCP_OPERATOR_ADDRESS, and MCP_OPERATOR_PRIVATE_KEY at deployment time."
        )

        console.print("\n📝 Next Steps:", style="bold")
        console.print(f"1. cd {repo_path}")
        console.print("2. Implement tools in server.py")
        console.print("3. Populate `.env` server wallet credentials before running")
        console.print("4. Add your upstream API key in `.env` if required")
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")
        import traceback
        console.print(traceback.format_exc(), style="red")
        raise typer.Exit(code=1)


@app.command(name="test-mcp")
def test_mcp(
    base_url: str = typer.Option(..., "--base-url", help="Base MCP server URL, with or without /mcp"),
    tool_name: str = typer.Option(..., "--tool-name", help="MCP tool name to call"),
    arguments: str = typer.Option("{}", "--arguments", help="Tool arguments as a JSON object string"),
    client_operator_private_key: Optional[str] = typer.Option(
        None,
        "--client-operator-private-key",
        envvar="CLIENT_OPERATOR_PRIVATE_KEY",
        help="Client operator private key",
    ),
    client_wallet_address: Optional[str] = typer.Option(
        None,
        "--client-wallet-address",
        envvar="CLIENT_WALLET_ADDRESS",
        help="Client wallet contract address",
    ),
    max_value: int = typer.Option(1000000, "--max-value", help="Maximum payment in base units"),
    timeout: float = typer.Option(30.0, "--timeout", help="Request timeout in seconds"),
    protocol_version: str = typer.Option("2024-11-05", "--protocol-version", help="MCP protocol version"),
    client_name: str = typer.Option("traia-iatp-cli", "--client-name", help="Client name for MCP initialize"),
    client_version: str = typer.Option("1.0.0", "--client-version", help="Client version for MCP initialize"),
):
    """Call a paid MCP tool from the CLI using d402HttpxClient."""

    async def _test():
        if not client_operator_private_key:
            raise typer.BadParameter("Provide --client-operator-private-key or set CLIENT_OPERATOR_PRIVATE_KEY")
        if not client_wallet_address:
            raise typer.BadParameter("Provide --client-wallet-address or set CLIENT_WALLET_ADDRESS")

        try:
            tool_arguments = json.loads(arguments)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"--arguments must be valid JSON: {exc}") from exc

        if not isinstance(tool_arguments, dict):
            raise typer.BadParameter("--arguments must decode to a JSON object")

        operator_account = Account.from_key(client_operator_private_key)
        normalized_base_url = _normalize_mcp_base_url(base_url)

        async with d402HttpxClient(
            operator_account=operator_account,
            wallet_address=client_wallet_address,
            max_value=max_value,
            base_url=normalized_base_url,
            timeout=timeout,
        ) as client:
            init_response = await client.post(
                "/mcp",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
                json={
                    "jsonrpc": "2.0",
                    "id": "init-1",
                    "method": "initialize",
                    "params": {
                        "protocolVersion": protocol_version,
                        "capabilities": {},
                        "clientInfo": {
                            "name": client_name,
                            "version": client_version,
                        },
                    },
                },
            )
            init_response.raise_for_status()
            session_id = init_response.headers.get("mcp-session-id")

            call_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            }
            if session_id:
                call_headers["mcp-session-id"] = session_id

            tool_call_response = await client.post(
                "/mcp",
                headers=call_headers,
                json={
                    "jsonrpc": "2.0",
                    "id": "call-1",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": tool_arguments,
                    },
                },
            )

            console.print("\n✅ MCP request completed", style="bold green")
            console.print(f"   Base URL: {normalized_base_url}")
            console.print(f"   Tool: {tool_name}")
            console.print(f"   HTTP status: {tool_call_response.status_code}")
            if session_id:
                console.print(f"   Session: {session_id}")

            parsed_response = _parse_mcp_response_text(tool_call_response.text)
            console.print("\nResponse:", style="bold")
            console.print_json(json.dumps(parsed_response, indent=2))

            payment_response_header = tool_call_response.headers.get("X-PAYMENT-RESPONSE")
            if payment_response_header:
                try:
                    decoded_payment = decode_x_payment_response(payment_response_header)
                    console.print("\nPayment Response:", style="bold")
                    console.print_json(json.dumps(decoded_payment, indent=2))
                except Exception:
                    console.print("\nPayment Response Header:", style="bold")
                    console.print(payment_response_header)

            if tool_call_response.status_code >= 400:
                raise typer.Exit(code=1)

    try:
        asyncio.run(_test())
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")
        import traceback
        console.print(traceback.format_exc(), style="red")
        raise typer.Exit(code=1)


@app.command()
def create_agency(
    name: str = typer.Option(..., "--name", "-n", help="Name of the utility agency"),
    description: str = typer.Option(..., "--description", "-d", help="Description of the agency"),
    mcp_name: str = typer.Option(..., "--mcp-name", help="Name of existing MCP server in registry"),
    output_dir: str = typer.Option("utility_agencies", "--output-dir", "-o", help="Output directory"),
    deploy: bool = typer.Option(False, "--deploy", help="Deploy immediately after creation"),
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Port to deploy on"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry")
):
    """Create a new utility agency from an existing MCP server in the registry."""
    async def _create():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating utility agency...", total=None)
            
            try:
                # Look up MCP server in registry
                mcp_registry = MCPServerRegistry(mongodb_uri)
                try:
                    mcp_data = await mcp_registry.get_mcp_server(mcp_name)
                    
                    if not mcp_data:
                        console.print(f"❌ MCP server '{mcp_name}' not found in registry", style="red")
                        return None, None
                    
                    # Create MCPServer object from registry data
                    mcp_server = MCPServer(
                        id=str(mcp_data.get("_id", "")),
                        name=mcp_data["name"],
                        url=mcp_data["url"],
                        description=mcp_data["description"],
                        server_type=mcp_data.get("server_type", MCPServerType.STREAMABLE_HTTP),
                        capabilities=mcp_data.get("capabilities", []),
                        metadata=mcp_data.get("metadata", {})
                    )
                finally:
                    mcp_registry.close()
                
                # Create agency generator
                generator = IATPServerAgentGenerator(output_base_dir=Path(output_dir))
                
                # Generate the agency
                agency = generator.generate_agent(
                    mcp_server=mcp_server,
                    agency_name=name,
                    agency_description=description,
                    use_simple_server=False  # Use modular server for CLI
                )
                
                folder_path = agency.code_path
                
                progress.update(task, description="Agency created successfully!")
                
                console.print(f"\n✅ Created utility agency: {agency.name}")
                console.print(f"   ID: {agency.id}")
                console.print(f"   Status: {agency.status}")
                console.print(f"   Folder: {folder_path}")
                console.print(f"   MCP Server: {mcp_server.name}")
                console.print(f"   Capabilities: {', '.join(agency.capabilities)}")
                
                if deploy:
                    progress.update(task, description="Deploying agency to Docker...")
                    
                    # Use the docker utilities to run the generated agency
                    runner = LocalDockerRunner()
                    deployment_info = await runner.run_agent_docker(
                        agent_path=Path(folder_path),
                        port=port or 8000,
                        detached=True
                    )
                    
                    if deployment_info["success"]:
                        console.print(f"\n🚀 Deployed agency:")
                        console.print(f"   Base URL: {deployment_info['base_url']}")
                        console.print(f"   IATP Endpoint: {deployment_info['iatp_endpoint']}")
                        console.print(f"   Container: {deployment_info['container_name']}")
                        console.print(f"   Port: {deployment_info['port']}")
                        console.print(f"\n📝 Useful commands:")
                        console.print(f"   View logs: {deployment_info['logs_command']}")
                        console.print(f"   Stop: {deployment_info['stop_command']}")
                        
                        # Register the deployed agency if MongoDB is configured
                        if mongodb_uri:
                            registry = UtilityAgentRegistry(mongodb_uri)
                            try:
                                await registry.add_utility_agency(
                                    agency=agency,
                                    endpoint=deployment_info['iatp_endpoint'],
                                    tags=["docker", "cli-deployed"]
                                )
                                console.print(f"   ✅ Registered in MongoDB")
                            finally:
                                registry.close()
                    else:
                        console.print(f"❌ Deployment failed", style="red")
                
                return agency, folder_path
                
            except Exception as e:
                console.print(f"❌ Error creating agency: {e}", style="red")
                raise
    
    asyncio.run(_create())


@app.command(name="register-mcp")
def register_mcp(
    email: str = typer.Option(..., "--email", help="Your d402.net account email"),
    name: str = typer.Option(..., "--name", "-n", help="Display name of the MCP server"),
    description: str = typer.Option(..., "--description", "-d", help="What the MCP server does"),
    url: str = typer.Option(..., "--url", "-u", help="Live MCP endpoint URL (e.g. https://yourserver.com/mcp)"),
    server_address: str = typer.Option(..., "--server-address", help="MCP server IATP wallet contract address (0x...) — from create-mcp or create-iatp-wallet output"),
    operator_address: str = typer.Option(..., "--operator-address", help="MCP server operator wallet address (0x...) — from create-mcp or create-iatp-wallet output"),
    requires_auth: bool = typer.Option(..., "--requires-auth/--no-requires-auth", help="Whether the MCP server requires callers to provide an API key"),
    token_symbol: str = typer.Option(..., "--token-symbol", help="Settlement token the MCP server charges: USDC or USDT"),
    endpoints_file: Path = typer.Option(..., "--endpoints-file", help="Path to endpoints.json — same format as create-mcp --endpoints-file"),
    icon_url: Optional[str] = typer.Option(None, "--icon-url", help="URL to the server icon image (optional)"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", help="Tags for discoverability; repeat for multiple (optional, default: ['d402'])"),
):
    """Register a deployed MCP server on the d402.net registry.

    The server must already be deployed, reachable at a public URL, and have
    all tool endpoints verified working before registering.

    You must have a d402.net account — sign up at https://d402.net first.

    --server-address and --operator-address are the MCP server's IATP wallet
    addresses, not your personal wallet or client wallet.

    The --endpoints-file format is identical to create-mcp --endpoints-file.
    Use the same endpoints.json file you passed to create-mcp.
    """
    # Map USDC/USDT to the payment_token_id expected by the public API.
    # USDC = 1, USDT = 2
    token_id_map = {"USDC": 1, "USDT": 2}
    token_upper = token_symbol.upper()
    if token_upper not in token_id_map:
        console.print("\n❌ --token-symbol must be USDC or USDT", style="bold red")
        raise typer.Exit(code=1)
    payment_token_id = token_id_map[token_upper]

    # Read and validate the endpoints file.
    if not endpoints_file.exists():
        console.print(f"\n❌ endpoints-file not found: {endpoints_file}", style="bold red")
        raise typer.Exit(code=1)
    try:
        raw_entries = json.loads(endpoints_file.read_text())
    except json.JSONDecodeError as exc:
        console.print(f"\n❌ endpoints-file is not valid JSON: {exc}", style="bold red")
        raise typer.Exit(code=1)
    if not isinstance(raw_entries, list) or not raw_entries:
        console.print("\n❌ endpoints-file must be a non-empty JSON array", style="bold red")
        raise typer.Exit(code=1)

    # Build the endpoints array that the public API expects.
    # Required fields per entry: endpoint_path, endpoint_name, endpoint_method, payment_price_float.
    endpoints_payload = []
    for entry in raw_entries:
        missing = [k for k in ("endpoint_path", "endpoint_name", "endpoint_method") if k not in entry]
        if missing:
            console.print(
                f"\n❌ Endpoint entry missing required fields: {', '.join(missing)}",
                style="bold red",
            )
            raise typer.Exit(code=1)
        ep: dict = {
            "endpoint_path": entry["endpoint_path"],
            "endpoint_name": entry["endpoint_name"],
            "endpoint_method": entry["endpoint_method"].upper(),
            "payment_price_float": entry.get("payment_price_float", 0.01),
        }
        # Pass optional documentation and schema fields when present.
        if entry.get("endpoint_description"):
            ep["endpoint_description"] = entry["endpoint_description"]
        if entry.get("endpoint_input_schema"):
            ep["endpoint_input_schema"] = entry["endpoint_input_schema"]
        if entry.get("endpoint_output_schema"):
            ep["endpoint_output_schema"] = entry["endpoint_output_schema"]
        endpoints_payload.append(ep)

    # Build the full request body.
    payload: dict = {
        "email": email,
        "name": name,
        "description": description,
        "url": url,
        "server_address": server_address,
        "operator_address": operator_address,
        "requires_auth": requires_auth,
        "payment_token_id": payment_token_id,
        "endpoints": endpoints_payload,
    }
    if icon_url:
        payload["icon_url"] = icon_url
    if tags:
        payload["tags"] = _parse_multi_value_option(tags)

    console.print("\n🚀 Registering MCP server on d402.net...", style="bold")
    console.print(f"   Name:              {name}")
    console.print(f"   URL:               {url}")
    console.print(f"   MCP server wallet: {server_address}")
    console.print(f"   MCP server oper.:  {operator_address}")
    console.print(f"   Token:             {token_upper} (payment_token_id={payment_token_id})")
    console.print(f"   Endpoints:         {len(endpoints_payload)}")

    try:
        import requests as _requests
        response = _requests.post(
            "https://api.d402.net/mcp/register-external",
            json=payload,
            timeout=30,
        )
        if response.status_code == 201:
            console.print("\n✅ MCP server registered successfully!", style="bold green")
            console.print_json(json.dumps(response.json(), indent=2))
        else:
            console.print(
                f"\n❌ Registration failed (HTTP {response.status_code})", style="bold red"
            )
            try:
                console.print_json(json.dumps(response.json(), indent=2))
            except Exception:
                console.print(response.text, style="red")
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as exc:
        console.print(f"\n❌ Error: {exc}", style="bold red")
        import traceback
        console.print(traceback.format_exc(), style="red")
        raise typer.Exit(code=1)


@app.command()
def list_agencies(
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    active_only: bool = typer.Option(True, "--active-only", help="Show only active agencies")
):
    """List all registered utility agencies."""
    async def _list():
        registry = UtilityAgentRegistry(mongodb_uri)
        
        try:
            agencies = await registry.query_agencies(active_only=active_only, limit=100)
            
            if not agencies:
                console.print("No agencies found.", style="yellow")
                return
            
            table = Table(title="Registered Utility Agencies")
            table.add_column("Name", style="cyan")
            table.add_column("ID", style="magenta")
            table.add_column("Endpoint", style="green")
            table.add_column("Capabilities", style="yellow")
            table.add_column("Active", style="blue")
            
            for agency in agencies:
                table.add_row(
                    agency.name,
                    agency.agency_id[:8] + "...",
                    str(agency.endpoint),
                    ", ".join(agency.capabilities[:3]) + ("..." if len(agency.capabilities) > 3 else ""),
                    "✅" if agency.is_active else "❌"
                )
            
            console.print(table)
            
        finally:
            registry.close()
    
    asyncio.run(_list())


@app.command()
def list_mcp_servers(
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    server_type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by server type")
):
    """List all registered MCP servers."""
    async def _list():
        registry = MCPServerRegistry(mongodb_uri)
        
        try:
            servers = await registry.query_mcp_servers(server_type=server_type)
            
            if not servers:
                console.print("No MCP servers found.", style="yellow")
                return
            
            table = Table(title="Registered MCP Servers")
            table.add_column("Name", style="cyan")
            table.add_column("URL", style="green")
            table.add_column("Type", style="yellow")
            table.add_column("Description", style="white")
            table.add_column("Capabilities", style="magenta")
            
            for server in servers:
                table.add_row(
                    server["name"],
                    server["url"],
                    server.get("server_type", "streamable-http"),
                    server["description"][:40] + "..." if len(server["description"]) > 40 else server["description"],
                    ", ".join(server.get("capabilities", [])[:3]) + ("..." if len(server.get("capabilities", [])) > 3 else "")
                )
            
            console.print(table)
            
        finally:
            registry.close()
    
    asyncio.run(_list())


@app.command()
def search_agencies(
    query: Optional[str] = typer.Argument(None, help="Search query"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Filter by tags"),
    capabilities: Optional[List[str]] = typer.Option(None, "--capability", "-c", help="Filter by capabilities"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results")
):
    """Search for utility agencies."""
    async def _search():
        registry = UtilityAgentRegistry(mongodb_uri)
        
        try:
            agencies = await registry.query_agencies(
                query=query,
                tags=tags,
                capabilities=capabilities,
                active_only=True,
                limit=limit
            )
            
            if not agencies:
                console.print("No agencies found matching criteria.", style="yellow")
                return
            
            table = Table(title=f"Search Results ({len(agencies)} found)")
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="white")
            table.add_column("Capabilities", style="yellow")
            table.add_column("Tags", style="green")
            
            for agency in agencies:
                table.add_row(
                    agency.name,
                    agency.description[:50] + "..." if len(agency.description) > 50 else agency.description,
                    ", ".join(agency.capabilities[:3]) + ("..." if len(agency.capabilities) > 3 else ""),
                    ", ".join(agency.tags[:3]) + ("..." if len(agency.tags) > 3 else "")
                )
            
            console.print(table)
            
        finally:
            registry.close()
    
    asyncio.run(_search())


@app.command()
def deploy(
    agency_path: Path = typer.Argument(..., help="Path to generated agency directory"),
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Port to deploy on"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    use_script: bool = typer.Option(False, "--use-script", help="Use the run_local_docker.sh script")
):
    """Deploy a utility agency from a generated directory."""
    async def _deploy():
        if not agency_path.exists():
            console.print(f"❌ Directory not found: {agency_path}", style="red")
            return
        
        # Check if it's a valid agency directory
        required_files = ["Dockerfile", "pyproject.toml"]
        missing_files = [f for f in required_files if not (agency_path / f).exists()]
        if missing_files:
            console.print(f"❌ Invalid agency directory. Missing files: {', '.join(missing_files)}", style="red")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deploying agency...", total=None)
            
            try:
                if use_script:
                    # Use the generated run_local_docker.sh script
                    script_path = agency_path / "run_local_docker.sh"
                    if not script_path.exists():
                        console.print(f"❌ run_local_docker.sh not found in {agency_path}", style="red")
                        return
                    
                    progress.update(task, description="Running deployment script...")
                    use_run_local_docker_script(str(agency_path))
                    
                    console.print(f"\n🚀 Agency deployed using run_local_docker.sh")
                    console.print(f"   Check the script output for connection details")
                else:
                    # Use LocalDockerRunner
                    runner = LocalDockerRunner()
                    deployment_info = await runner.run_agent_docker(
                        agent_path=agency_path,
                        port=port or 8000,
                        detached=True
                    )
                    
                    if deployment_info["success"]:
                        console.print(f"\n🚀 Deployed agency from: {agency_path}")
                        console.print(f"   Base URL: {deployment_info['base_url']}")
                        console.print(f"   IATP Endpoint: {deployment_info['iatp_endpoint']}")
                        console.print(f"   Container: {deployment_info['container_name']}")
                        console.print(f"   Port: {deployment_info['port']}")
                        console.print(f"\n📝 Useful commands:")
                        console.print(f"   View logs: {deployment_info['logs_command']}")
                        console.print(f"   Stop: {deployment_info['stop_command']}")
                        
                        # If MongoDB URI is provided and agent_config.json exists, register it
                        if mongodb_uri and (agency_path / "agent_config.json").exists():
                            with open(agency_path / "agent_config.json", 'r') as f:
                                agency_data = json.load(f)
                            
                            agency = UtilityAgent(**agency_data)
                            
                            registry = UtilityAgentRegistry(mongodb_uri)
                            try:
                                await registry.add_utility_agency(
                                    agency=agency,
                                    endpoint=deployment_info['iatp_endpoint'],
                                    tags=["docker", "cli-deployed"]
                                )
                                console.print(f"   ✅ Registered in MongoDB")
                            finally:
                                registry.close()
                    else:
                        console.print(f"❌ Deployment failed", style="red")
                
            except Exception as e:
                console.print(f"❌ Deployment failed: {e}", style="red")
                raise
    
    asyncio.run(_deploy())


@app.command()
def find_tools(
    query: Optional[str] = typer.Argument(None, help="Search query for tools"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Filter by tags"),
    capabilities: Optional[List[str]] = typer.Option(None, "--capability", "-c", help="Filter by capabilities"),
    mongodb_uri: Optional[str] = typer.Option(None, "--mongodb-uri", help="MongoDB URI for registry"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save tools configuration to file")
):
    """Find utility agency tools for use in CrewAI."""
    tools = create_utility_agency_tools(
        mongodb_uri=mongodb_uri,
        query=query,
        tags=tags,
        capabilities=capabilities
    )
    
    if not tools:
        console.print("No tools found matching criteria.", style="yellow")
        return
    
    table = Table(title=f"Available Tools ({len(tools)} found)")
    table.add_column("Tool Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Endpoint", style="green")
    
    tools_config = []
    for tool in tools:
        table.add_row(
            tool.name,
            tool.description[:60] + "..." if len(tool.description) > 60 else tool.description,
            tool.endpoint
        )
        
        tools_config.append({
            "name": tool.name,
            "description": tool.description,
            "endpoint": tool.endpoint,
            "agency_id": tool.agency_id,
            "capabilities": tool.capabilities
        })
    
    console.print(table)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(tools_config, f, indent=2)
        console.print(f"\n💾 Tools configuration saved to: {output_file}", style="green")


@app.command()
def example_crew():
    """Show an example of how to use utility agencies in a CrewAI crew."""
    example_code = '''
# Example: Using utility agencies in a CrewAI crew

from crewai import Agent, Crew, Task
from traia_iatp import create_utility_agency_tools

# Find and create tools from utility agencies
tools = create_utility_agency_tools(
    query="weather data analysis",  # Search for relevant agencies
    tags=["weather", "api"],        # Filter by tags
    capabilities=["forecast"]       # Filter by capabilities
)

# Create an agent with utility agency tools
analyst = Agent(
    role="Data Analyst",
    goal="Analyze weather patterns and provide insights",
    backstory="You are an expert at analyzing weather data and trends.",
    tools=tools,  # Use the utility agency tools
    allow_delegation=False,
    verbose=True
)

# Create a task
analysis_task = Task(
    description="Analyze the weather forecast for New York City for the next week",
    expected_output="A detailed analysis of weather patterns and recommendations",
    agent=analyst
)

# Create and run the crew
crew = Crew(
    agents=[analyst],
    tasks=[analysis_task],
    verbose=True
)

result = crew.kickoff()
print(result)
'''
    
    console.print("📚 Example: Using Utility Agencies in CrewAI\n", style="bold cyan")
    console.print(example_code, style="cyan")


if __name__ == "__main__":
    app() 