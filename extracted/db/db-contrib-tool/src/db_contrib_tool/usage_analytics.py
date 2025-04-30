"""Usage data collecting and storing in external sources."""

import sys
import platform
import git
from typing import Any, Optional

import click
from pydantic import BaseModel

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

COLLECTOR_ENDPOINT = "otel-collector.prod.corp.mongodb.com:443"


class CommandUsage(BaseModel):
    """
    Command usage information.

    * command: Name of subcommand being invoked.
    """

    command: Optional[str]


def _should_skip_grpc_tracing() -> bool:
    """Check whether grpc tracing is enabled on the current machine's OS."""
    return sys.platform.startswith("linux") and platform.machine().startswith(
        ("ppc", "powerpc", "s390")
    )


class CommandWithUsageTracking(click.Command):
    """Class to track click command usage."""

    def invoke(self, ctx: click.Context) -> Any:
        """
        Given a context, this invokes the attached callback (if it exists) in the right way.

        :param ctx: Invocation context for this command.
        :return: Invocation result.
        """
        ctx.ensure_object(CommandUsage)
        if _should_skip_grpc_tracing():
            return super().invoke(ctx)
        try:
            user_email = git.config.GitConfigParser().get_value("user", "email")
        except Exception:
            # We'll only track local usage we can actually follow back to real users.
            return super().invoke(ctx)

        # Ths is only available on non 390x and non ppc hosts so we wait to import it.
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

        resource = Resource(attributes={SERVICE_NAME: "db-contrib-tool"})
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=COLLECTOR_ENDPOINT))
        )

        span_attributes = {}
        for key, value in ctx.params.items():
            if value is not None:
                span_attributes[f"command.param.{key}"] = value
        span_attributes["user.email"] = user_email

        tracer = provider.get_tracer("db-contrib-tool")
        with tracer.start_as_current_span(name=ctx.obj.command, attributes=span_attributes):
            result = super().invoke(ctx)
        provider.force_flush()
        return result
