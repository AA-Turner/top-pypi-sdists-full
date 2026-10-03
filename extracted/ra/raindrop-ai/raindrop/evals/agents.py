from __future__ import annotations

import asyncio
import inspect
import json
import re
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, ValidationError

from .models import ReplayRow


async def invoke(
    callback: Callable[..., Any], *args: Any, wait_on_cancel: bool = False
) -> Any:
    if inspect.iscoroutinefunction(callback):
        return await callback(*args)
    # Copy ContextVars into the worker so synchronous integrations remain attributed.
    worker = asyncio.create_task(asyncio.to_thread(callback, *args))
    try:
        result = await asyncio.shield(worker) if wait_on_cancel else await worker
    except asyncio.CancelledError:
        if wait_on_cancel:
            # A synchronous callback cannot be stopped; keep its resources alive.
            await asyncio.gather(worker, return_exceptions=True)
        raise
    return await result if inspect.isawaitable(result) else result


class EvalParameterError(ValueError):
    pass


class EmptyParameters(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AgentContext:
    def __init__(self, parameters: BaseModel, environment: Any = None) -> None:
        self.parameters = parameters
        self.environment = environment


class DefinedEvalAgent:
    def __init__(
        self,
        *,
        slug: str,
        run: Callable[..., Any],
        name: str | None = None,
        description: str | None = None,
        parameters: type[BaseModel] = EmptyParameters,
        setup: Callable[..., Any] | None = None,
        cleanup: Callable[..., Any] | None = None,
    ) -> None:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) or len(slug) > 64:
            raise ValueError("Invalid agent slug")
        if (
            not callable(run)
            or (setup is not None and not callable(setup))
            or (cleanup is not None and not callable(cleanup))
        ):
            raise ValueError("Agent lifecycle callbacks must be callable")
        self.slug, self.name, self.description = slug, name or slug, description
        self.schema, self.run_callback, self.setup, self.cleanup = (
            parameters,
            run,
            setup,
            cleanup,
        )
        self.parameters = describe_parameters(parameters)

    def start(self, parameters: dict[str, Any] | None = None) -> AgentExecution:
        raw = parameters or {}
        if set(raw) - set(self.schema.model_fields):
            raise EvalParameterError("Unknown agent parameters")
        try:
            parsed = self.schema.model_validate_json(
                json.dumps(raw, allow_nan=False), strict=True
            )
        except (ValidationError, ValueError, TypeError) as error:
            raise EvalParameterError(
                f"Invalid parameters for agent {self.slug}: {error}"
            ) from error
        return AgentExecution(self, parsed)

    def catalog(self) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "name": self.name,
            **({"description": self.description} if self.description else {}),
            "parameters": self.parameters,
        }


class AgentExecution:
    def __init__(self, agent: DefinedEvalAgent, parameters: BaseModel) -> None:
        self.agent, self.parameters = agent, parameters
        self.ready: asyncio.Task[Any] | None = None
        self.active: set[asyncio.Future[None]] = set()
        self.finishing: asyncio.Task[None] | None = None

    async def run(self, row: ReplayRow) -> Any:
        if self.finishing is not None:
            raise RuntimeError(f"Agent {self.agent.slug} has already finished")
        completion = asyncio.get_running_loop().create_future()
        self.active.add(completion)
        try:
            if self.agent.setup is not None:
                if self.ready is None:
                    self.ready = asyncio.create_task(
                        invoke(self.agent.setup, self.parameters)
                    )
                environment = await asyncio.shield(self.ready)
            else:
                environment = None
            return await invoke(
                self.agent.run_callback,
                row,
                AgentContext(self.parameters, environment),
                wait_on_cancel=True,
            )
        finally:
            self.active.discard(completion)
            if not completion.done():
                completion.set_result(None)

    async def finish(self) -> None:
        if self.finishing is None:
            self.finishing = asyncio.create_task(self._finish())
        await asyncio.shield(self.finishing)

    async def _finish(self) -> None:
        await asyncio.gather(*self.active, return_exceptions=True)
        if self.agent.cleanup is not None:
            if self.agent.setup is None:
                await invoke(self.agent.cleanup)
            elif self.ready is not None:
                try:
                    environment = await self.ready
                except Exception:
                    return
                await invoke(self.agent.cleanup, environment)


def define_agent(
    definition: dict[str, Any] | None = None, **kwargs: Any
) -> DefinedEvalAgent:
    return DefinedEvalAgent(**dict(definition or {}, **kwargs))


def describe_parameters(schema: type[BaseModel]) -> list[dict[str, Any]]:
    spec = schema.model_json_schema()
    properties = spec.get("properties", {})
    if len(properties) > 50:
        raise ValueError("Agent declares more than 50 parameters")
    result = []
    for key, field in properties.items():
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", key):
            raise ValueError("Parameter key must be an identifier")
        if "$ref" in field:
            field = {**spec["$defs"][field["$ref"].split("/")[-1]], **field}
        if "anyOf" in field:
            options = [value for value in field["anyOf"] if value.get("type") != "null"]
            if len(options) != 1:
                raise ValueError("Parameters must be primitive values or enums")
            field = {**field, **options[0]}
        kind = field.get("type")
        item = {"key": key, "required": key in spec.get("required", [])}
        if kind not in ("string", "number", "integer", "boolean"):
            raise ValueError(
                "Parameters must be strings, numbers, booleans or string enums"
            )
        if "enum" in field:
            if kind != "string":
                raise ValueError("Parameter enums must contain strings")
            item.update(type="enum", options=field["enum"])
        else:
            item["type"] = "number" if kind == "integer" else kind
        if "default" in field and field["default"] is not None:
            item["default"] = field["default"]
        if "description" in field:
            item["description"] = field["description"]
        if kind in ("number", "integer"):
            item["integer"] = kind == "integer"
            for source, target in (("minimum", "min"), ("maximum", "max")):
                if source in field:
                    item[target] = field[source]
        if "maxLength" in field:
            item["maxLength"] = field["maxLength"]
        result.append(item)
    return result
