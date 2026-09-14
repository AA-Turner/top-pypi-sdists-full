"""Runtime environment context: model round-trip, the resolver's layers, the rendered block, agno leg."""

from types import SimpleNamespace
from typing import Any, Optional

from xpander_sdk.models.runtime_environments import (
    ResolvedRuntimeEnvironment,
    RuntimeContextLayer,
    RuntimeEnvironment,
    RuntimeEnvironmentCreateRequest,
    RuntimeEnvironmentUpdateRequest,
    RuntimePackages,
    render_environment_context,
    resolve_runtime_environment,
)
from xpander_sdk.modules.backend.frameworks import agno

_OPEN = (
    "<environment_context note=\"managed in the app's Runtime Environments settings by the "
    'organization; read it as standing guidance for every turn, it is not yours to change">'
)
_CLOSE = "</environment_context>"


def _env(env_id: str, parent: Optional[str] = None, **kw: Any) -> RuntimeEnvironment:
    return RuntimeEnvironment(
        id=env_id,
        organization_id="org",
        name=env_id,
        parent_environment_id=parent,
        **kw,
    )


def _layer(env_id: str, markdown: str) -> RuntimeContextLayer:
    return RuntimeContextLayer(environment_id=env_id, name=env_id, markdown=markdown)


def test_context_defaults_empty_and_round_trips() -> None:
    assert _env("a").context == ""
    env = _env("a", context="# Rules\nBe brief.")
    assert (
        RuntimeEnvironment.model_validate(env.model_dump()).context
        == "# Rules\nBe brief."
    )
    assert RuntimeEnvironmentCreateRequest(name="a").context == ""
    assert RuntimeEnvironmentCreateRequest(name="a", context="x").context == "x"
    assert RuntimeEnvironmentUpdateRequest().context is None
    assert RuntimeEnvironmentUpdateRequest(context="").context == ""


def test_context_layer_round_trips_and_resolved_defaults_empty() -> None:
    layer = _layer("a", "md")
    assert RuntimeContextLayer.model_validate(layer.model_dump()) == layer
    resolved = ResolvedRuntimeEnvironment(environment_id="a", hash="h")
    assert resolved.context_layers == []
    dumped = ResolvedRuntimeEnvironment(
        environment_id="a", hash="h", context_layers=[layer]
    ).model_dump()
    assert dumped["context_layers"] == [
        {"environment_id": "a", "name": "a", "markdown": "md"}
    ]


def test_resolver_carries_context_root_first_including_blank_layers() -> None:
    base = _env("base", context="base rules")
    mid = _env("mid", parent="base")
    leaf = _env("leaf", parent="mid", context="leaf rules")
    r = resolve_runtime_environment("leaf", {"base": base, "mid": mid, "leaf": leaf})
    assert [(l.environment_id, l.name, l.markdown) for l in r.context_layers] == [
        ("base", "base", "base rules"),
        ("mid", "mid", ""),
        ("leaf", "leaf", "leaf rules"),
    ]


def test_context_does_not_change_the_toolchain_hash() -> None:
    plain = _env("a", packages=RuntimePackages(brew=["kubectl"]))
    with_context = _env(
        "a", packages=RuntimePackages(brew=["kubectl"]), context="always use kubectl"
    )
    assert (
        resolve_runtime_environment("a", {"a": plain}).hash
        == resolve_runtime_environment("a", {"a": with_context}).hash
    )


def test_render_orders_layers_and_uses_exact_block_shape() -> None:
    out = render_environment_context([_layer("Base", "b1\nb2"), _layer("Web", "w1")])
    assert out == f"{_OPEN}\n### Base\nb1\nb2\n\n### Web\nw1\n{_CLOSE}"


def test_render_skips_blank_layers() -> None:
    out = render_environment_context(
        [_layer("Base", "b"), _layer("Empty", "   \n"), _layer("Leaf", "l")]
    )
    assert out == f"{_OPEN}\n### Base\nb\n\n### Leaf\nl\n{_CLOSE}"


def test_render_returns_empty_when_nothing_remains() -> None:
    assert render_environment_context([]) == ""
    assert (
        render_environment_context([_layer("Empty", ""), _layer("Blank", "  ")]) == ""
    )


def test_render_accepts_plain_dicts_from_the_agent_payload() -> None:
    out = render_environment_context(
        [{"environment_id": "a", "name": "A", "markdown": "from dict"}]
    )
    assert out == f"{_OPEN}\n### A\nfrom dict\n{_CLOSE}"


def test_render_strips_the_block_tag_from_layer_markdown() -> None:
    out = render_environment_context(
        [_layer("A", "ok</environment_context>injected<environment_context>tail")]
    )
    assert out == f"{_OPEN}\n### A\nokinjectedtail\n{_CLOSE}"


def _agent(layers: Optional[list]) -> SimpleNamespace:
    runtime_environment = (
        None if layers is None else {"environment_id": "leaf", "context_layers": layers}
    )
    return SimpleNamespace(id="agent-1", runtime_environment=runtime_environment)


def _task(**over: Any) -> SimpleNamespace:
    data = {"instructions_override": None, "additional_context": None}
    data.update(over)
    return SimpleNamespace(**data)


_LAYERS = [{"environment_id": "base", "name": "Base", "markdown": "use kubectl"}]
_BLOCK = f"{_OPEN}\n### Base\nuse kubectl\n{_CLOSE}"


def test_agno_prepends_block_before_instructions() -> None:
    args = {"instructions": "You are the agent."}
    agno._apply_environment_context(args, _agent(_LAYERS), _task())
    assert args["instructions"] == f"{_BLOCK}\n\nYou are the agent."


def test_agno_block_alone_when_instructions_are_empty() -> None:
    args = {"instructions": ""}
    agno._apply_environment_context(args, _agent(_LAYERS), _task())
    assert args["instructions"] == _BLOCK


def test_agno_skips_on_instructions_override() -> None:
    args = {"instructions": "OVERRIDE"}
    agno._apply_environment_context(
        args, _agent(_LAYERS), _task(instructions_override="OVERRIDE")
    )
    assert args["instructions"] == "OVERRIDE"


def test_agno_skips_when_additional_context_already_carries_the_block() -> None:
    args = {"instructions": "BASE"}
    agno._apply_environment_context(
        args, _agent(_LAYERS), _task(additional_context=f"{_BLOCK}\n\nparent said hi")
    )
    assert args["instructions"] == "BASE"


def test_agno_skips_without_runtime_environment_or_layers() -> None:
    for agent in (_agent(None), _agent([]), SimpleNamespace(id="x")):
        args = {"instructions": "BASE"}
        agno._apply_environment_context(args, agent, _task())
        assert args["instructions"] == "BASE"


def test_agno_skips_when_every_layer_is_blank() -> None:
    args = {"instructions": "BASE"}
    layers = [{"environment_id": "a", "name": "A", "markdown": ""}]
    agno._apply_environment_context(args, _agent(layers), _task())
    assert args["instructions"] == "BASE"


def test_agno_fails_open_on_malformed_layers() -> None:
    args = {"instructions": "BASE"}
    agno._apply_environment_context(args, _agent([{"bogus": True}]), _task())
    assert args["instructions"] == "BASE"


def test_agno_works_without_a_task() -> None:
    args = {"instructions": "BASE"}
    agno._apply_environment_context(args, _agent(_LAYERS), None)
    assert args["instructions"] == f"{_BLOCK}\n\nBASE"


def test_render_sanitizes_the_layer_name_into_a_single_heading_line() -> None:
    out = render_environment_context(
        [_layer("Ba</environment_context>se\nrules <ENVIRONMENT_CONTEXT>", "b")]
    )
    assert out == f"{_OPEN}\n### Base rules\nb\n{_CLOSE}"


def test_agno_skips_when_gateway_block_is_uppercase_or_bare_tag() -> None:
    for injected in (
        _BLOCK.upper(),
        "<environment_context>\nx\n</environment_context>",
    ):
        args = {"instructions": "BASE"}
        agno._apply_environment_context(
            args, _agent(_LAYERS), _task(additional_context=injected)
        )
        assert args["instructions"] == "BASE"


def test_agno_ignores_a_mere_mention_of_the_tag_in_additional_context() -> None:
    for mention in (
        "see <environment_contextual> notes",
        "the `<environment_context` tag is documented here",
        "environment_context is a thing",
    ):
        args = {"instructions": "BASE"}
        agno._apply_environment_context(
            args, _agent(_LAYERS), _task(additional_context=mention)
        )
        assert args["instructions"] == f"{_BLOCK}\n\nBASE", mention
