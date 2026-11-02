"""Basic-auth platform diagnostics using the selected environment's dependencies."""

from __future__ import annotations

from urllib.parse import urlsplit

import click

from labqoat._generated.transport import Transport
from labqoat.cli.cli_context import CliContext
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument, JsonValue


class DoctorCommand(StrictCommand):
    """Check endpoint, Basic credentials, connectivity, and server prerequisites."""

    def __init__(self) -> None:
        """Construct the root diagnostic command."""
        super().__init__("doctor", help="Check Basic-auth platform access and server dependencies.")

    def invoke(self, ctx: click.Context) -> object:
        """Run independent safe checks and use a failing process status when needed."""
        context = ContextAccessor.current()
        checks = self._checks(context)
        passed = all(check.get("status") == "pass" for check in checks)
        documents: list[JsonValue] = list(checks)
        ResultWriter().write_dict({"checks": documents, "ok": passed})
        if not passed:
            ctx.exit(1)
        return None

    @classmethod
    def _checks(cls, context: CliContext) -> list[JsonDocument]:
        """Run the applicable checks without AWS or bearer-session state."""
        endpoint = cls._endpoint(context.profile.base_url)
        credentials = cls._credentials(context)
        checks = [endpoint, credentials]
        if endpoint["status"] == "pass" and credentials["status"] == "pass":
            checks.append(cls._connectivity(context))
            checks.extend(cls._capabilities(context))
        else:
            checks.append(cls._check("connectivity", False, "Connectivity requires a valid endpoint and credentials."))
        return checks

    @classmethod
    def _endpoint(cls, base_url: str) -> JsonDocument:
        """Validate the configured origin and local plain-HTTP policy."""
        try:
            parts = urlsplit(base_url)
            if not parts.hostname:
                raise ValueError("endpoint has no host")
            Transport.ensure_loopback(base_url)
        except ValueError as error:
            return cls._check("endpoint", False, str(error))
        return cls._check("endpoint", True, f"Configured endpoint is {base_url}.")

    @classmethod
    def _credentials(cls, context: CliContext) -> JsonDocument:
        """Check that noninteractive Basic credentials resolve without displaying them."""
        try:
            credentials = context.resolver.resolve(context.profile, prompt=False)
            Transport.ensure_credentials(credentials.username, credentials.password)
        except Exception:
            return cls._check("basic_credentials", False, "Basic credentials are unavailable or invalid.")
        return cls._check("basic_credentials", True, f"Basic username {credentials.username!r} is configured.")

    @classmethod
    def _connectivity(cls, context: CliContext) -> JsonDocument:
        """Authenticate against the status resource and close the connection."""
        client = context.client()
        try:
            status = client.status()
            okay = status.status == "ok"
            return cls._check("connectivity", okay, f"Platform status is {status.status!r}.")
        except Exception:
            return cls._check("connectivity", False, "The authenticated status request failed.")
        finally:
            client.close()

    @classmethod
    def _capabilities(cls, context: CliContext) -> list[JsonDocument]:
        """Probe the selected server's runtime, storage, catalog, and reconciliation readiness."""
        client = context.management()
        try:
            report = client.get("/api/v1/capabilities", {})
            dependencies = JsonDocument.expect_dict(report.get("dependencies"))
            return cls._dependency_checks(dependencies)
        except Exception:
            return [cls._check("capabilities", False, "The capability probe failed or returned an invalid document.")]
        finally:
            client.close()

    @classmethod
    def _dependency_checks(cls, dependencies: JsonDocument) -> list[JsonDocument]:
        """Render every declared dependency without assuming a particular execution provider."""
        if not dependencies:
            raise ValueError("Capability report must declare its dependencies")
        checks: list[JsonDocument] = []
        for name, value in dependencies.items():
            status = JsonDocument.expect_dict(value)
            available = status.get("available") is True
            detail = status.get("detail")
            message = detail if isinstance(detail, str) and detail else f"{name} is unavailable."
            checks.append(cls._check(name, available, message))
        return checks

    @staticmethod
    def _check(name: str, passed: bool, message: str) -> JsonDocument:
        """Build one stable diagnostic document."""
        return JsonDocument({"message": message, "name": name, "status": "pass" if passed else "fail"})
