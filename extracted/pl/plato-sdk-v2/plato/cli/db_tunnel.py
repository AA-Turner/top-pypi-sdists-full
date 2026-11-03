"""plato db-tunnel — open a local DB tunnel to a running sim."""

import asyncio
import socket

import typer

from plato.cli.utils import console, require_api_key

db_tunnel_app = typer.Typer(help="Open a local DB tunnel to a sim's database.")


@db_tunnel_app.command(name="start")
def db_tunnel_start(
    sim: str = typer.Option(..., "--sim", "-s", help="Simulator name or name:artifact_id"),
):
    """Start a session, tunnel to its DB, and wait for commands.

    Examples:
        plato db-tunnel start -s mattermost
        plato db-tunnel start -s mattermost:1b642f11-10a5-44cd-...
    """

    async def _run():
        from plato._generated.api.v1.simulator import get_db_config
        from plato._generated.models import DbConfigResponse
        from plato.v2 import AsyncPlato, Env
        from plato.v2.sync.sandbox import Tunnel

        api_key = require_api_key()
        plato = None
        session = None
        tunnels: list[Tunnel] = []

        try:
            plato = AsyncPlato(api_key=api_key)

            if ":" in sim:
                name, artifact_id = sim.split(":", 1)
                console.print(f"Using artifact: {artifact_id}")
                session = await plato.sessions.create(envs=[Env.artifact(artifact_id, alias=name)])
            else:
                session = await plato.sessions.create(envs=[Env.simulator(sim)])

            env = session.envs[0]
            console.print(f"Session: {session.session_id}  |  Job: {env.job_id}")

            if not env.artifact_id:
                console.print("[red]No artifact_id found for this environment.[/red]")
                raise typer.Exit(1)

            db_configs_raw = await get_db_config.asyncio(
                client=plato._http, artifact_id=env.artifact_id, x_api_key=api_key
            )
            db_configs = [DbConfigResponse(**c) if isinstance(c, dict) else c for c in (db_configs_raw or [])]

            if not db_configs:
                console.print("[red]No databases found for this sim.[/red]")
                raise typer.Exit(1)

            for cfg in db_configs:
                with socket.socket() as s:
                    s.bind(("127.0.0.1", 0))
                    port = s.getsockname()[1]

                tunnel = Tunnel(job_id=env.job_id, remote_port=cfg.db_port, local_port=port)
                tunnel.start()
                tunnels.append(tunnel)
                await asyncio.sleep(1)

                db_type = cfg.db_type.lower()
                tables: list[str] = []

                if db_type == "postgresql":
                    try:
                        import psycopg2
                    except ImportError:
                        console.print("[red]psycopg2 required for postgres. Install with:[/red]")
                        console.print("  uv tool install plato-sdk-v2 --with psycopg2-binary")
                        raise typer.Exit(1)

                    conn = psycopg2.connect(
                        host="127.0.0.1",
                        port=port,
                        user=cfg.db_user,
                        password=cfg.db_password,
                        dbname=cfg.db_database,
                        connect_timeout=10,
                    )
                    cur = conn.cursor()
                    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename")
                    tables = [r[0] for r in cur.fetchall()]
                    cur.close()
                    conn.close()
                    url = f"postgresql://{cfg.db_user}:{cfg.db_password}@127.0.0.1:{port}/{cfg.db_database}"
                    cli_cmd = f"psql -h 127.0.0.1 -p {port} -U {cfg.db_user} -d {cfg.db_database}"

                elif db_type == "mysql":
                    try:
                        import pymysql
                    except ImportError:
                        console.print("[red]pymysql required for mysql. Install with:[/red]")
                        console.print("  uv tool install plato-sdk-v2 --with pymysql")
                        raise typer.Exit(1)

                    conn = pymysql.connect(
                        host="127.0.0.1",
                        port=port,
                        user=cfg.db_user,
                        password=cfg.db_password,
                        database=cfg.db_database,
                        connect_timeout=10,
                    )
                    cur = conn.cursor()
                    cur.execute("SHOW TABLES")
                    tables = [r[0] for r in cur.fetchall()]
                    cur.close()
                    conn.close()
                    url = f"mysql://{cfg.db_user}:{cfg.db_password}@127.0.0.1:{port}/{cfg.db_database}"
                    cli_cmd = f"mysql -h 127.0.0.1 -P {port} -u {cfg.db_user} -p{cfg.db_password} {cfg.db_database}"

                else:
                    url = f"{cfg.db_user}@127.0.0.1:{port}/{cfg.db_database}"
                    cli_cmd = "(unsupported db type)"

                console.print(f"\n{'=' * 60}")
                console.print(f"  {cfg.db_type} | {cfg.db_user}@127.0.0.1:{port}/{cfg.db_database}")
                console.print(f"  URL:  {url}")
                console.print(f"  CLI:  {cli_cmd}")
                console.print(f"{'=' * 60}")
                if tables:
                    console.print(f"Tables ({len(tables)}): {', '.join(tables)}\n")
                else:
                    console.print("")

            console.print("[bold]Commands:[/bold]  snapshot (cleanup + snapshot)  |  exit")
            while True:
                cmd = await asyncio.to_thread(input, "> ")
                cmd = cmd.strip().lower()

                if cmd == "snapshot":
                    console.print("Cleaning up audit logs...")
                    try:
                        cleanup_result = await session.cleanup_databases()
                    except ImportError:
                        console.print("[red]db-cleanup deps missing. Reinstall with:[/red]")
                        console.print(
                            '  uv tool install plato-sdk-v2 --with psycopg2-binary --with "sqlalchemy[asyncio]>=2.0" --with "asyncpg>=0.29" --force --reinstall'
                        )
                        continue

                    for alias, env_result in (cleanup_result.environments or {}).items():
                        for db_name, db_result in (env_result.databases or {}).items():
                            if db_result.success:
                                console.print(f"  {alias}/{db_name}: truncated {db_result.tables_truncated}")
                            else:
                                console.print(f"  [red]{alias}/{db_name}: FAILED - {db_result.error}[/red]")

                    console.print("Snapshotting...")
                    snap = await session.snapshot()
                    for job_id, result in (snap.results or {}).items():
                        if result.success:
                            console.print(f"  [green]{job_id}: artifact_id={result.artifact_id}[/green]")
                        else:
                            console.print(f"  [red]{job_id}: FAILED - {result.error}[/red]")

                elif cmd == "exit":
                    break

                else:
                    console.print("Unknown command. Use: snapshot | exit")

        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            console.print("\nShutting down...")
            for t in tunnels:
                t.stop()
            if session is not None:
                await session.close()
            if plato is not None:
                await plato.close()
            console.print("Done.")

    asyncio.run(_run())
