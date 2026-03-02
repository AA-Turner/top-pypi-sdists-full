# """Verification CLI commands for Plato simulator creation pipeline.

# All verification commands follow the convention:
# - Exit 0 = verification passed
# - Exit 1 = verification failed
# - Stderr = actionable error message for agents

# Usage:
#     plato sandbox verify <check>
#     plato pm verify <check>
# """

# from __future__ import annotations

# import os
# import subprocess
# import sys
# from collections import defaultdict
# from pathlib import Path
# from typing import NoReturn

# import typer
# import yaml

# from plato.cli.utils import (
#     STATE_FILE,
#     get_http_client,
#     get_sandbox_state,
#     require_api_key,
# )


# def _error(msg: str) -> None:
#     """Write error to stderr."""
#     sys.stderr.write(f"{msg}\n")


# def _fail(msg: str) -> NoReturn:
#     """Write error to stderr and exit 1."""
#     _error(msg)
#     raise typer.Exit(1)


# # =============================================================================
# # SANDBOX VERIFY COMMANDS
# # =============================================================================

# sandbox_verify_app = typer.Typer(help="Verify sandbox setup and state")


# @sandbox_verify_app.callback(invoke_without_command=True)
# def sandbox_verify_default(
#     ctx: typer.Context,
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify sandbox is properly configured.

#     Checks that .plato/state.yaml exists and contains all required fields.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     if ctx.invoked_subcommand is not None:
#         return

#     state = get_sandbox_state(working_dir)
#     if not state:
#         _fail(f"File not found: {STATE_FILE}")

#     # Core required fields
#     required_fields = ["job_id", "session_id", "public_url", "plato_config_path", "service"]
#     missing = [f for f in required_fields if f not in state or not state[f]]

#     # Check plato_config_path exists
#     plato_config = state.get("plato_config_path")
#     if plato_config:
#         # Convert container path to relative path for checking
#         if plato_config.startswith("/workspace/"):
#             check_path = Path(plato_config[len("/workspace/") :])
#         else:
#             check_path = Path(plato_config)

#         if not check_path.exists():
#             missing.append(f"plato_config_path (file): File not found: {plato_config}")

#     if missing:
#         _fail(f"Missing fields in {STATE_FILE}: {missing}")

#     # Success - exit 0


# @sandbox_verify_app.command(name="services")
# def verify_services(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify containers are running and public URL returns 200.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     state = get_sandbox_state(working_dir)
#     if not state:
#         _fail(f"File not found: {STATE_FILE}")

#     ssh_config = state.get("ssh_config_path")
#     ssh_host = state.get("ssh_host", "sandbox")
#     public_url = state.get("public_url")

#     if not ssh_config:
#         _fail("No ssh_config_path in state")

#     # Check containers via SSH
#     try:
#         result = subprocess.run(
#             [
#                 "ssh",
#                 "-F",
#                 os.path.expanduser(ssh_config),
#                 ssh_host,
#                 "docker ps -a --format '{{.Names}}\t{{.Status}}'",
#             ],
#             capture_output=True,
#             text=True,
#             timeout=30,
#         )

#         if result.returncode != 0:
#             _fail(f"Failed to check containers via SSH: {result.stderr.strip()}")

#         unhealthy = []
#         for line in result.stdout.strip().split("\n"):
#             if not line:
#                 continue
#             parts = line.split("\t")
#             if len(parts) >= 2:
#                 name, status = parts[0], parts[1]
#                 if "unhealthy" in status.lower() or "exited" in status.lower() or "dead" in status.lower():
#                     unhealthy.append(f"{name}: {status}")

#         if unhealthy:
#             _fail(f"Unhealthy containers: {unhealthy}")

#     except subprocess.TimeoutExpired:
#         _fail("SSH connection timed out")
#     except FileNotFoundError:
#         _fail("SSH not found")

#     # Check public URL
#     if public_url:
#         try:
#             import urllib.error
#             import urllib.request

#             req = urllib.request.Request(public_url, method="HEAD")
#             req.add_header("User-Agent", "plato-verify/1.0")

#             try:
#                 with urllib.request.urlopen(req, timeout=10) as response:
#                     if response.getcode() != 200:
#                         _fail(f"HTTP {response.getcode()} from {public_url}")
#             except urllib.error.HTTPError as e:
#                 if e.code == 502:
#                     _fail("HTTP 502 Bad Gateway - check app_port in plato-config.yml and nginx config")
#                 else:
#                     _fail(f"HTTP {e.code} from {public_url}")

#         except Exception as e:
#             _fail(f"Failed to check public URL: {e}")

#     # Success - exit 0


# @sandbox_verify_app.command(name="login")
# def verify_login(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify login page is accessible.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     state = get_sandbox_state(working_dir)
#     if not state:
#         _fail(f"File not found: {STATE_FILE}")

#     public_url = state.get("public_url")
#     if not public_url:
#         _fail("No public_url in .sandbox.yaml")

#     try:
#         import urllib.error
#         import urllib.request

#         req = urllib.request.Request(public_url, method="GET")
#         req.add_header("User-Agent", "plato-verify/1.0")

#         with urllib.request.urlopen(req, timeout=10) as response:
#             if response.getcode() != 200:
#                 _fail(f"HTTP {response.getcode()} from {public_url}")
#     except urllib.error.HTTPError as e:
#         _fail(f"HTTP {e.code} from {public_url}")
#     except Exception as e:
#         _fail(f"Failed to check login page: {e}")

#     # Success - exit 0


# @sandbox_verify_app.command(name="worker")
# def verify_worker(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify Plato worker is connected and audit triggers installed.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     state = get_sandbox_state(working_dir)
#     if not state:
#         _fail(f"File not found: {STATE_FILE}")

#     session_id = state.get("session_id")
#     if not session_id:
#         _fail("No session_id in state")

#     api_key = require_api_key()

#     try:
#         from plato._generated.api.v2.sessions import state as sessions_state

#         with get_http_client() as client:
#             state_response = sessions_state.sync(
#                 session_id=session_id,
#                 client=client,
#                 x_api_key=api_key,
#             )

#         if state_response is None:
#             _fail("State API returned no data")

#         if not state_response.results:
#             _fail("State API returned empty results")

#         for job_id, result in state_response.results.items():
#             if hasattr(result, "error") and result.error:
#                 _fail(f"Worker error: {result.error}")

#             state_data = result.state if hasattr(result, "state") and result.state else {}
#             if isinstance(state_data, dict):
#                 if "error" in state_data:
#                     _fail(f"Worker error: {state_data['error']}")

#                 if "db" in state_data:
#                     db_state = state_data["db"]
#                     if not db_state.get("is_connected", False):
#                         _fail("Worker not connected to database")
#                     # Success - worker connected
#                     return
#                 else:
#                     _fail("Worker not initialized (no db state)")

#         _fail("No worker state found")

#     except typer.Exit:
#         raise
#     except Exception as e:
#         if "502" in str(e):
#             _fail("Worker not ready (502)")
#         _fail(f"Failed to check worker: {e}")


# @sandbox_verify_app.command(name="audit-clear")
# def verify_audit_clear(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify audit log is cleared (0 mutations).

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     state = get_sandbox_state(working_dir)
#     if not state:
#         _fail(f"File not found: {STATE_FILE}")

#     session_id = state.get("session_id")
#     api_key = require_api_key()

#     try:
#         from plato._generated.api.v2.sessions import state as sessions_state

#         with get_http_client() as client:
#             state_response = sessions_state.sync(
#                 session_id=session_id,
#                 client=client,
#                 x_api_key=api_key,
#             )

#         if state_response is None:
#             _fail("State API returned no data")

#         audit_count = 0
#         if state_response.results:
#             for job_id, result in state_response.results.items():
#                 state_data = result.state if hasattr(result, "state") and result.state else {}
#                 if isinstance(state_data, dict) and "db" in state_data:
#                     audit_count = state_data["db"].get("audit_log_count", 0)
#                     break

#         if audit_count != 0:
#             _fail(f"Audit log not clear: {audit_count} mutations")

#         # Success - exit 0

#     except typer.Exit:
#         raise
#     except Exception as e:
#         _fail(f"Failed to check audit: {e}")


# @sandbox_verify_app.command(name="flow")
# def verify_flow():
#     """Verify login flow exists and is valid.

#     Checks that flows.yml (or base/flows.yml) exists and contains a valid 'login'
#     flow definition with required fields (name, steps, etc.).

#     Exit code 0 = valid flow found, exit code 1 = missing or invalid.
#     """
#     flow_paths = ["flows.yml", "base/flows.yml", "login-flow.yml"]
#     flow_file = None

#     for path in flow_paths:
#         if Path(path).exists():
#             flow_file = path
#             break

#     if not flow_file:
#         _fail(f"No flows.yml found. Searched: {flow_paths}")

#     assert flow_file is not None  # for type checker

#     try:
#         with open(flow_file) as f:
#             flows = yaml.safe_load(f)

#         if not flows:
#             _fail(f"Flows file is empty: {flow_file}")

#         if "login" not in flows:
#             _fail(f"No 'login' flow defined in {flow_file}")

#         # Success - exit 0

#     except yaml.YAMLError as e:
#         _fail(f"Invalid YAML in {flow_file}: {e}")


# @sandbox_verify_app.command(name="mutations")
# def verify_mutations(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify no mutations after login flow.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     state = get_sandbox_state(working_dir)
#     if not state:
#         _fail(f"File not found: {STATE_FILE}")

#     session_id = state.get("session_id")
#     api_key = require_api_key()

#     try:
#         from plato._generated.api.v2.sessions import state as sessions_state

#         with get_http_client() as client:
#             state_response = sessions_state.sync(
#                 session_id=session_id,
#                 client=client,
#                 x_api_key=api_key,
#             )

#         if state_response is None:
#             _fail("State API returned no data")

#         mutations = []
#         audit_count = 0
#         if state_response.results:
#             for job_id, result in state_response.results.items():
#                 state_data = result.state if hasattr(result, "state") and result.state else {}
#                 if isinstance(state_data, dict) and "db" in state_data:
#                     audit_count = state_data["db"].get("audit_log_count", 0)
#                     mutations = state_data["db"].get("mutations", [])
#                     break

#         if audit_count == 0:
#             # Success - exit 0
#             return

#         # Build table breakdown
#         table_ops: dict[str, dict[str, int]] = defaultdict(lambda: {"INSERT": 0, "UPDATE": 0, "DELETE": 0})
#         for mutation in mutations:
#             table = mutation.get("table", "unknown")
#             op = mutation.get("operation", "UNKNOWN").upper()
#             if op in table_ops[table]:
#                 table_ops[table][op] += 1

#         # Format error message
#         table_summary = {t: dict(ops) for t, ops in table_ops.items()}
#         _fail(f"Found {audit_count} mutations: {table_summary}")

#     except typer.Exit:
#         raise
#     except Exception as e:
#         _fail(f"Failed to check mutations: {e}")


# @sandbox_verify_app.command(name="audit-active")
# def verify_audit_active():
#     """Verify audit system is tracking changes.

#     This is a manual verification step that requires making a change in the app
#     and confirming mutations appear. Always exits 0 - actual verification is manual.
#     """
#     # This step requires manual verification - just pass
#     pass


# @sandbox_verify_app.command(name="snapshot")
# def verify_snapshot(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify snapshot was created.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     state = get_sandbox_state(working_dir)
#     if not state:
#         _fail(f"File not found: {STATE_FILE}")

#     artifact_id = state.get("artifact_id")

#     if not artifact_id:
#         _fail("No artifact_id - run 'plato sandbox snapshot' first")

#     # Validate UUID format
#     import re

#     uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

#     if not uuid_pattern.match(artifact_id):
#         _fail(f"Invalid artifact_id format: {artifact_id}")

#     # Success - exit 0


# # =============================================================================
# # PM VERIFY COMMANDS
# # =============================================================================

# pm_verify_app = typer.Typer(help="Verify review and submit steps")


# @pm_verify_app.command(name="review")
# def verify_review(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify review prerequisites.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     issues = []

#     # Check API key
#     if not os.environ.get("PLATO_API_KEY"):
#         issues.append("PLATO_API_KEY not set")

#     # Check state
#     state = get_sandbox_state(working_dir)
#     if not state:
#         issues.append(f"{STATE_FILE} not found")
#     else:
#         if not state.get("artifact_id"):
#             issues.append("No artifact_id - run 'plato sandbox snapshot' first")
#         if not state.get("service"):
#             issues.append("No service name in state")

#     # Check plato-config.yml
#     if not Path("plato-config.yml").exists() and not Path("plato-config.yaml").exists():
#         issues.append("plato-config.yml not found")

#     if issues:
#         _fail(f"Review prerequisites not met: {issues}")

#     # Success - exit 0


# @pm_verify_app.command(name="submit")
# def verify_submit(
#     working_dir: Path | None = typer.Option(None, "-w", "--working-dir", help="Working directory with .plato/"),
# ):
#     """Verify submit prerequisites.

#     Options:
#         -w, --working-dir: Working directory containing .plato/
#     """
#     issues = []

#     if not os.environ.get("PLATO_API_KEY"):
#         issues.append("PLATO_API_KEY not set")

#     state = get_sandbox_state(working_dir)
#     if not state:
#         issues.append(f"{STATE_FILE} not found")
#     else:
#         required = ["artifact_id", "service", "plato_config_path"]
#         for field in required:
#             if not state.get(field):
#                 issues.append(f"Missing {field} in state")

#     if issues:
#         _fail(f"Submit prerequisites not met: {issues}")

#     # Success - exit 0


# # =============================================================================
# # RESEARCH/VALIDATION/CONFIG VERIFY COMMANDS
# # =============================================================================


# @sandbox_verify_app.command(name="research")
# def verify_research(
#     report_path: str = typer.Option("research-report.yml", "--report", "-r"),
# ):
#     """Verify research report is complete.

#     Checks that the research report YAML file contains all required fields:
#     app_name, source, database.type, docker, and credentials.

#     Options:
#         -r, --report: Path to research report file (default: research-report.yml)

#     Exit code 0 = complete, exit code 1 = missing required fields.
#     """
#     if not Path(report_path).exists():
#         _fail(f"Research report not found: {report_path}")

#     try:
#         with open(report_path) as f:
#             report = yaml.safe_load(f)
#     except yaml.YAMLError as e:
#         _fail(f"Invalid YAML in {report_path}: {e}")

#     if not report:
#         _fail(f"Research report is empty: {report_path}")

#     required_fields = ["db_type", "docker_image", "docker_tag", "credentials", "github_url"]
#     missing = [f for f in required_fields if f not in report or not report[f]]

#     # Check credentials sub-fields
#     if "credentials" in report and report["credentials"]:
#         creds = report["credentials"]
#         if not creds.get("username"):
#             missing.append("credentials.username")
#         if not creds.get("password"):
#             missing.append("credentials.password")

#     # Check db_type is valid
#     valid_db_types = ["postgresql", "mysql", "mariadb"]
#     if report.get("db_type") and report["db_type"].lower() not in valid_db_types:
#         _fail(f"Invalid db_type: {report['db_type']}. Valid: {valid_db_types}")

#     if missing:
#         _fail(f"Missing fields in research report: {missing}")

#     # Success - exit 0


# @sandbox_verify_app.command(name="validation")
# def verify_validation(
#     report_path: str = typer.Option("research-report.yml", "--report", "-r"),
# ):
#     """Verify app can become a simulator.

#     Checks that the research report indicates a supported database type
#     (postgresql, mysql, mariadb, sqlite) and has no blocking issues.

#     Options:
#         -r, --report: Path to research report file (default: research-report.yml)

#     Exit code 0 = can become simulator, exit code 1 = has blockers.
#     """
#     if not Path(report_path).exists():
#         _fail(f"Research report not found: {report_path}")

#     with open(report_path) as f:
#         report = yaml.safe_load(f)

#     # Check database type
#     db_type = report.get("db_type", "").lower()
#     supported_dbs = ["postgresql", "mysql", "mariadb"]

#     if db_type == "sqlite":
#         _fail("SQLite not supported. Plato requires PostgreSQL, MySQL, or MariaDB")

#     if db_type not in supported_dbs:
#         _fail(f"Unknown database type: {db_type}. Supported: {supported_dbs}")

#     # Check for blockers
#     blockers = report.get("blockers", [])
#     if blockers:
#         _fail(f"Blockers found: {blockers}")

#     # Success - exit 0


# @sandbox_verify_app.command(name="config")
# def verify_config(
#     config_path: str = typer.Option("plato-config.yml", "--config", "-c"),
#     compose_path: str = typer.Option("base/docker-compose.yml", "--compose"),
# ):
#     """Verify configuration files are valid.

#     Checks that plato-config.yml and docker-compose.yml exist and contain valid
#     YAML. Validates required fields in plato-config.yml (service, datasets, etc.).

#     Options:
#         -c, --config: Path to plato-config.yml (default: plato-config.yml)
#         --compose: Path to docker-compose.yml (default: base/docker-compose.yml)

#     Exit code 0 = valid, exit code 1 = issues found.
#     """
#     issues = []

#     # Check plato-config.yml
#     if not Path(config_path).exists():
#         _fail(f"File not found: {config_path}")

#     try:
#         with open(config_path) as f:
#             config = yaml.safe_load(f)
#     except yaml.YAMLError as e:
#         _fail(f"Invalid YAML in {config_path}: {e}")

#     required_config_fields = ["service", "datasets"]
#     for field in required_config_fields:
#         if field not in config:
#             issues.append(f"{config_path}: Missing '{field}'")

#     # Check datasets.base structure
#     if "datasets" in config and "base" in config.get("datasets", {}):
#         base = config["datasets"]["base"]

#         if "metadata" not in base:
#             issues.append(f"{config_path}: Missing datasets.base.metadata")

#         if "listeners" not in base:
#             issues.append(f"{config_path}: Missing datasets.base.listeners")
#         elif "db" not in base.get("listeners", {}):
#             issues.append(f"{config_path}: Missing listeners.db")

#     # Check docker-compose.yml
#     if not Path(compose_path).exists():
#         _fail(f"File not found: {compose_path}")

#     try:
#         with open(compose_path) as f:
#             compose = yaml.safe_load(f)
#     except yaml.YAMLError as e:
#         _fail(f"Invalid YAML in {compose_path}: {e}")

#     services = compose.get("services", {})
#     standard_db_images = ["postgres:", "mysql:", "mariadb:"]

#     for svc_name, svc_config in services.items():
#         if svc_config.get("network_mode") != "host":
#             issues.append(f"{compose_path}: '{svc_name}' missing 'network_mode: host'")

#         image = svc_config.get("image", "")
#         for std_img in standard_db_images:
#             if image.startswith(std_img):
#                 issues.append(f"{compose_path}: '{svc_name}' uses standard DB image '{image}' - use Plato DB image")

#     if issues:
#         _fail(f"Config issues: {issues}")

#     # Success - exit 0
