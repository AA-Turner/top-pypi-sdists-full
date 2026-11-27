"""AgentSystem in the evaluation plugin: the workflow sends a reference, the task's activity runs the agent."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from mistralai.evaluations.models import System
from pydantic import BaseModel, ConfigDict

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.dependencies import Depends
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.plugins.evaluations import AgentSystem, _agents, evaluation
from mistralai.workflows.plugins.evaluations._activities import resolve_agent_system
from mistralai.workflows.plugins.evaluations._optimize import _candidate_system, _search_space
from mistralai.workflows.plugins.evaluations.types import (
    Evaluator,
    Score,
    ScorerContext,
    TaskContext,
    Tunable,
    TunableSystem,
)

from .test_evaluation_plugin import (
    _EVAL_ACTIVITIES,
    TaskWorkflowWithSystem,
    _create_test_worker_with_mock_obs,
    _make_mock_obs_client,
)


def _sdk_agents() -> Any:
    # Imported in the tests only: this module is also loaded in the workflow sandbox, where the SDK's
    # agents module (httpx) can't be imported.
    import mistralai.evaluations.agents

    return mistralai.evaluations.agents


class FakeAgent(BaseModel):
    """Shaped like an Agents SDK Agent: pydantic fields as settings, ``run`` to run it."""

    model_config = ConfigDict(validate_assignment=True)

    name: str
    instructions: str | None = None
    model: str = "mistral-small-latest"

    async def run(self, content: Any) -> SimpleNamespace:
        return SimpleNamespace(text=f"{self.instructions}|{self.model}|{content}")


support_bot = FakeAgent(name="support-bot", instructions="Be kind")
other_bot = FakeAgent(name="other-bot", instructions="Be terse")


@evaluation.task(agents=[support_bot, other_bot])
async def answer(ctx: TaskContext) -> str:
    result = await ctx.agent.run(ctx.input_record["question"])
    return str(result.text)


def _suffix() -> str:
    return "!"


@evaluation.task(agents=[support_bot])
async def answer_with_dependency(ctx: TaskContext, suffix: str = Depends(_suffix)) -> str:
    result = await ctx.agent.run(ctx.input_record["question"])
    return str(result.text) + suffix


@evaluation.task(agents=[support_bot])
async def answer_by_keyword(context: TaskContext) -> str:
    result = await context.agent.run(context.input_record["question"])
    return str(result.text)


def answer_sync(ctx: TaskContext) -> str:
    return ""


async def answer_not_a_task(ctx: TaskContext) -> str:
    return ""


@evaluation.task
async def answer_undeclared(ctx: TaskContext) -> str:
    result = await ctx.agent.run(ctx.input_record["question"])
    return str(result.text)


@evaluation.scorer
async def brief_and_large(ctx: ScorerContext) -> Score:
    ok = str(ctx.output).startswith("Be brief|mistral-large-latest|")
    return Score(value=1.0 if ok else 0.0)


@workflow.define(name="test-agent-system-code")
class AgentSystemCodeWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=[{"question": "Where is my order?"}],
            task=answer,
            evaluators=[Evaluator(name="brief_and_large", scorer=brief_and_large)],
            system=AgentSystem(
                agent=support_bot,
                overrides={"instructions": "Be brief", "model": "mistral-large-latest"},
                params={"sandbox": "none"},
            ),
            local=params["local"],
        )
        return {"run_id": result.run_id, "avg": result.statistics["brief_and_large"].avg}


@workflow.define(name="test-agent-system-depends")
class AgentSystemDependsWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=[{"question": "Where is my order?"}],
            task=answer_with_dependency,
            evaluators=[Evaluator(name="brief_and_large", scorer=brief_and_large)],
            system=AgentSystem(
                agent=support_bot, overrides={"instructions": "Be brief", "model": "mistral-large-latest"}
            ),
            local=True,
        )
        return {"avg": result.statistics["brief_and_large"].avg}


@workflow.define(name="test-agent-system-undeclared")
class AgentSystemUndeclaredWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        try:
            await evaluation.run(
                dataset=[{"question": "Where is my order?"}],
                task=answer_undeclared,
                evaluators=[Evaluator(name="brief_and_large", scorer=brief_and_large)],
                system=AgentSystem(agent=support_bot),
                local=True,
            )
        except ValueError as e:
            return {"error": str(e)}
        return {}


@workflow.define(name="test-agent-system-on-behalf-of", on_behalf_of=True)
class AgentSystemOnBehalfOfWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        try:
            await evaluation.run(
                dataset=[{"question": "Where is my order?"}],
                task=answer,
                evaluators=[Evaluator(name="brief_and_large", scorer=brief_and_large)],
                system=AgentSystem(agent=support_bot),
                local=True,
            )
        except ValueError as e:
            return {"error": str(e)}
        return {}


@workflow.define(name="test-agent-system-workflow-task")
class AgentSystemWorkflowTaskWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        try:
            await evaluation.run(
                dataset=[{"question": "Where is my order?"}],
                task=TaskWorkflowWithSystem,
                evaluators=[Evaluator(name="brief_and_large", scorer=brief_and_large)],
                system=AgentSystem(agent=support_bot),
                local=True,
            )
        except ValueError as e:
            return {"error": str(e)}
        return {}


@workflow.define(name="test-agent-system-deployed")
class AgentSystemDeployedWorkflow:
    @workflow.entrypoint
    async def run(self, params: dict) -> dict:
        result = await evaluation.run(
            dataset=[{"question": "Where is my order?"}],
            task=answer_undeclared,
            evaluators=[Evaluator(name="brief_and_large", scorer=brief_and_large)],
            system=AgentSystem(agent="support-bot-deployed", overrides={"additional_instructions": "Be brief"}),
        )
        return {"run_id": result.run_id, "avg": result.statistics["brief_and_large"].avg}


class FakeDeployedAgent:
    def __init__(self, overrides: dict[str, Any]) -> None:
        self.overrides = overrides

    async def run(self, content: Any) -> SimpleNamespace:
        return SimpleNamespace(text=f"{self.overrides['additional_instructions']}|mistral-large-latest|{content}")


async def _fake_resolve_deployed(name: str, reference: str, overrides: dict[str, Any], **_: Any) -> Any:
    spec = {
        "source": "deployed",
        "name": reference,
        "config": {"agent_id": "agent-1"},
        "base": {key: None for key in overrides},
        "managed_agent": {"agent_id": "agent-1", "agent_name": reference},
    }
    return _sdk_agents().ResolvedAgent(
        system=System(name=name, params=dict(overrides), kind="agent", spec=spec),
        agent=FakeDeployedAgent(dict(overrides)),
    )


async def _no_managed_agent(control_plane: Any, agent_name: str) -> None:
    return None


@pytest.fixture(autouse=True)
def _fresh_agent_cache() -> None:
    _agents._agents.clear()


async def _run(temporal_env: Any, workflow_cls: type, params: dict, mock_client: Any = None) -> Any:
    async with _create_test_worker_with_mock_obs(
        temporal_env,
        workflows=[workflow_cls, TaskWorkflowWithSystem],
        activities=[
            answer,
            answer_with_dependency,
            answer_undeclared,
            brief_and_large,
            resolve_agent_system,
            *_EVAL_ACTIVITIES,
        ],
        mock_client=mock_client,
    ):
        handle = await temporal_env.client.start_workflow(
            get_workflow_definition(workflow_cls).name,
            {"params": params},
            id=f"test-{get_workflow_definition(workflow_cls).name}-{params}",
            task_queue="test-task-queue",
        )
        return await handle.result()


class TestCodeAgent:
    @pytest.mark.asyncio
    async def test_the_task_runs_the_declared_agent_with_the_overrides(self, temporal_env: Any) -> None:
        result = await _run(temporal_env, AgentSystemCodeWorkflow, {"local": True})

        assert result["result"] == {"run_id": "local", "avg": 1.0}
        assert support_bot.instructions == "Be kind"

    @pytest.mark.asyncio
    async def test_the_run_records_the_agent(self, temporal_env: Any, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(_sdk_agents(), "_find_managed_agent", _no_managed_agent)
        mock_client = _make_mock_obs_client()

        result = await _run(temporal_env, AgentSystemCodeWorkflow, {"local": False}, mock_client)

        assert result["result"]["avg"] == 1.0
        system = mock_client.evaluation.beta.create_run.await_args.kwargs["system"]
        assert system.name == "support-bot"
        assert system.kind == "agent"
        assert system.params == {"sandbox": "none", "instructions": "Be brief", "model": "mistral-large-latest"}
        assert system.spec["source"] == "code"
        assert system.spec["base"] == {"instructions": "Be kind", "model": "mistral-small-latest"}

    @pytest.mark.asyncio
    async def test_a_task_with_a_dependency_runs_the_agent(self, temporal_env: Any) -> None:
        result = await _run(temporal_env, AgentSystemDependsWorkflow, {})

        assert result["result"] == {"avg": 1.0}

    @pytest.mark.asyncio
    async def test_a_context_passed_by_keyword_gets_the_agent(self) -> None:
        system = System(
            name="support-bot",
            params={"model": "mistral-large-latest"},
            kind="agent",
            spec={"source": "code", "name": "support-bot", "base": {"model": "mistral-small-latest"}},
        )

        output = await answer_by_keyword(context=TaskContext(input_record={"question": "Hi"}, system=system))

        assert output == "Be kind|mistral-large-latest|Hi"

    @pytest.mark.asyncio
    async def test_an_unreachable_agents_api_is_retried(
        self, temporal_env: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import httpx  # Not at module level: the workflow sandbox loads this module and refuses httpx.

        calls = []

        async def flaky_find(control_plane: Any, agent_name: str) -> None:
            calls.append(agent_name)
            if len(calls) == 1:
                raise ValueError("Could not reach the Agents API") from httpx.ConnectError("down")

        monkeypatch.setattr(_sdk_agents(), "_find_managed_agent", flaky_find)

        result = await _run(temporal_env, AgentSystemCodeWorkflow, {"local": False}, _make_mock_obs_client())

        assert result["result"]["avg"] == 1.0
        assert len(calls) == 2

    @pytest.mark.asyncio
    async def test_an_undeclared_agent_fails_before_the_run(self, temporal_env: Any) -> None:
        result = await _run(temporal_env, AgentSystemUndeclaredWorkflow, {})

        assert result["result"]["error"] == (
            "Agent 'support-bot' is not declared on task 'answer_undeclared' (declared: none). "
            "Declare it with @evaluation.task(agents=[...]) so the worker can run it"
        )

    @pytest.mark.asyncio
    async def test_an_agent_from_code_is_refused_in_an_on_behalf_of_workflow(self, temporal_env: Any) -> None:
        result = await _run(temporal_env, AgentSystemOnBehalfOfWorkflow, {})

        assert "An agent from code is not supported yet in an on_behalf_of workflow" in result["result"]["error"]

    @pytest.mark.asyncio
    async def test_a_workflow_task_is_refused(self, temporal_env: Any) -> None:
        result = await _run(temporal_env, AgentSystemWorkflowTaskWorkflow, {})

        assert "needs an @evaluation.task task" in result["result"]["error"]


class TestDeployedAgent:
    @pytest.mark.asyncio
    async def test_the_task_runs_the_deployed_agent_without_declaring_it(
        self, temporal_env: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        sdk_agents = _sdk_agents()
        monkeypatch.setattr(sdk_agents, "_resolve_deployed_agent", _fake_resolve_deployed)
        monkeypatch.setattr(
            _agents, "_worker_control_plane", lambda: sdk_agents.ControlPlane(url="https://api/v2/agents", api_key="k")
        )
        mock_client = _make_mock_obs_client()

        result = await _run(temporal_env, AgentSystemDeployedWorkflow, {}, mock_client)

        assert result["result"]["avg"] == 1.0
        system = mock_client.evaluation.beta.create_run.await_args.kwargs["system"]
        assert system.kind == "agent"
        assert system.spec["source"] == "deployed"
        assert system.params == {"additional_instructions": "Be brief"}

    @pytest.mark.asyncio
    async def test_another_identity_gets_its_own_agent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        sdk_agents = _sdk_agents()
        monkeypatch.setattr(sdk_agents, "_resolve_deployed_agent", _fake_resolve_deployed)
        monkeypatch.setattr(
            _agents, "_worker_control_plane", lambda: sdk_agents.ControlPlane(url="https://api/v2/agents", api_key="k")
        )
        system = System(
            name="support-bot-deployed",
            params={"additional_instructions": "Be brief"},
            kind="agent",
            spec={"source": "deployed", "name": "support-bot-deployed", "base": {"additional_instructions": None}},
        )
        identity = ("worker",)
        monkeypatch.setattr(_agents, "_identity", lambda: identity)

        first = await _agents.task_agent(system, {})

        assert await _agents.task_agent(system, {}) is first
        identity = ("executor", "root-1")
        assert await _agents.task_agent(system, {}) is not first


class TestTaskAgents:
    def test_two_agents_with_the_same_name_are_refused(self) -> None:
        with pytest.raises(ValueError, match="two agents named 'support-bot'"):

            @evaluation.task(agents=[support_bot, FakeAgent(name="support-bot")])
            async def ambiguous(ctx: TaskContext) -> str:
                return ""

    def test_a_deployed_agent_name_is_refused(self) -> None:
        with pytest.raises(TypeError, match="needs no declaration"):

            @evaluation.task(agents=["support-bot"])
            async def by_name(ctx: TaskContext) -> str:
                return ""

    def test_a_sync_task_is_refused_when_declared(self) -> None:
        # So a sync task never reaches run() or optimize(), where it would get no ctx.agent.
        with pytest.raises(WorkflowsException, match="must be async function"):

            @evaluation.task(agents=[support_bot])
            def sync_answer(ctx: TaskContext) -> str:
                return ""


class TestOptimizeSearchSpace:
    def test_an_agent_is_searched_over_its_overrides(self) -> None:
        system = AgentSystem(agent=support_bot, overrides={"instructions": Tunable("Be kind"), "model": "m"})

        fixed, tunables = _search_space(system, answer)

        assert fixed == {"model": "m"}
        assert list(tunables) == ["instructions"]
        candidate = _candidate_system(system, "support-bot-gen1", {"model": "m", "instructions": "Be brief"})
        assert isinstance(candidate, AgentSystem)
        assert candidate.overrides == {"model": "m", "instructions": "Be brief"}
        assert candidate.name == "support-bot-gen1"

    def test_an_undeclared_agent_is_refused_before_the_optimization(self) -> None:
        ghost = FakeAgent(name="ghost-bot")

        with pytest.raises(ValueError, match="Agent 'ghost-bot' is not declared on task 'answer'"):
            _search_space(AgentSystem(agent=ghost, overrides={"instructions": Tunable("Be kind")}), answer)

    @pytest.mark.parametrize(
        ("task", "error"),
        [
            pytest.param(answer_sync, "needs an @evaluation.task task", id="sync function"),
            pytest.param(answer_not_a_task, "needs an @evaluation.task task", id="undecorated function"),
            pytest.param(AgentSystemCodeWorkflow, "needs an @evaluation.task task", id="workflow class"),
            pytest.param("test-agent-system-code", "needs an @evaluation.task task", id="workflow name"),
        ],
    )
    def test_a_task_run_refuses_is_refused_before_the_optimization(self, task: Any, error: str) -> None:
        with pytest.raises(ValueError, match=error):
            _search_space(AgentSystem(agent=support_bot, overrides={"instructions": Tunable("Be kind")}), task)

    def test_a_deployed_agent_needs_no_declaration(self) -> None:
        system = AgentSystem(agent="support-bot", overrides={"instructions": Tunable("Be kind")})

        _, tunables = _search_space(system, answer)

        assert list(tunables) == ["instructions"]

    def test_an_agent_without_tunables_is_refused(self) -> None:
        with pytest.raises(ValueError, match="system.overrides"):
            _search_space(AgentSystem(agent=support_bot, overrides={"model": "m"}), answer)

    def test_a_custom_system_is_searched_over_its_params(self) -> None:
        fixed, tunables = _search_space(TunableSystem(name="s", params={"x": Tunable(1), "y": 2}), answer)

        assert fixed == {"y": 2}
        assert list(tunables) == ["x"]
