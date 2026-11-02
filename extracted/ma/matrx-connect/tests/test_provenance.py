from matrx_connect import AppContext, derive_http_origin_class, reconcile_origin
from matrx_connect.emitters.console_emitter import ConsoleEmitter


def _ctx(**overrides) -> AppContext:
    return AppContext(emitter=ConsoleEmitter("test", accumulate=False), **overrides)


def test_http_derivation_requires_route():
    assert derive_http_origin_class(route=None, auth_type="token", initiation="user") == ""
    assert derive_http_origin_class(route="/ai/chat", auth_type="token", initiation="user") == "human"
    assert derive_http_origin_class(route="/ai/chat", auth_type="fingerprint", initiation="user") == "human"
    assert derive_http_origin_class(route="/ai/chat", auth_type="token", initiation="auto") == "client_auto"
    assert derive_http_origin_class(route="/ai/chat", auth_type="token", initiation=None) == "api"
    assert derive_http_origin_class(route="/ai/chat", auth_type="anonymous", initiation="user") == "api"


def test_reconcile_overrules_human_claim_without_http_witness():
    ctx = _ctx(origin_class="human", auth_type="token", is_internal_agent=True)
    final, witness = reconcile_origin(ctx)
    assert final == "system"
    assert witness["declared_class"] == "human"
    assert witness["contradictions"]


def test_reconcile_accepts_witnessed_human():
    ctx = _ctx(origin_class="human", auth_type="token", route="/ai/chat")
    final, witness = reconcile_origin(ctx)
    assert final == "human"
    assert "contradictions" not in witness


def test_machine_classes_are_trusted():
    for klass in ("workflow", "scheduled", "system", "child_agent"):
        final, witness = reconcile_origin(
            _ctx(origin_class=klass, parent_conversation_id="10101010-1010-1010-1010-101010101010")
        )
        assert final == klass
        assert "contradictions" not in witness
    # A child_agent with no parent conversation was started by no agent: it records its root.
    assert reconcile_origin(_ctx(origin_class="child_agent"))[0] == "system"


def test_blank_context_derives_honestly():
    # Background work with no class minted: never a UI identity.
    assert reconcile_origin(_ctx())[0] == "system"
    # HTTP request with no attestation: api, not human.
    assert reconcile_origin(_ctx(route="/ai/chat", auth_type="token"))[0] == "api"
    # Child fork lineage.
    child = _ctx(conversation_id="10101010-1010-1010-1010-101010101010").fork_for_child_agent(
        "11111111-1111-1111-1111-111111111111"
    )
    assert reconcile_origin(child)[0] == "child_agent"
    # A root fork of blank background work is that background work (no agent started it).
    root = _ctx().fork_for_child_agent("11111111-1111-1111-1111-111111111112")
    assert reconcile_origin(root)[0] == "system"
    # Workflow fork lineage.
    step = _ctx().fork_for_workflow_step("22222222-2222-2222-2222-222222222222")
    assert reconcile_origin(step)[0] == "workflow"


def test_no_context_is_system_with_evidence():
    final, witness = reconcile_origin(None)
    assert final == "system"
    assert witness["contradictions"]


def test_unregistered_class_is_overruled():
    final, witness = reconcile_origin(_ctx(origin_class="totally-legit-human"))
    assert final == "system"
    assert witness["contradictions"]


def test_workflow_run_correlation_is_not_a_conversation_parent():
    run_id = "11111111-1111-1111-1111-111111111111"
    child_id = "22222222-2222-2222-2222-222222222222"
    parent = _ctx(conversation_id=run_id, execution_kind="workflow_run", execution_id=run_id)
    child = parent.fork_for_child_agent(child_id)
    assert child.parent_conversation_id is None
    assert child.execution_id == run_id
    assert child.execution_kind == "workflow_run"
    assert child.fork_for_child_agent("33333333-3333-3333-3333-333333333333").parent_conversation_id == child_id


def test_real_conversation_lineage_is_preserved_inside_workflow():
    run_id = "11111111-1111-1111-1111-111111111111"
    conversation_id = "22222222-2222-2222-2222-222222222222"
    for execution_kind, source_id in (("workflow_run", conversation_id), ("conversation", run_id)):
        parent = _ctx(conversation_id=source_id, execution_kind=execution_kind, execution_id=run_id)
        assert parent.fork_for_child_agent("33333333-3333-3333-3333-333333333333").parent_conversation_id == source_id


# ── Root forks carry their caller's class (2026-10-08) ────────────────────────
# A person running an agent from Claude Code through the MCP ``agent_run`` tool
# was recorded as ``child_agent`` — automated sub-agent traffic — because every
# fork hard-coded that class, even when the parent ran no conversation at all.


def test_mcp_agent_run_root_fork_is_api_not_child_agent():
    mcp = _ctx(
        route="mcp:agent_run",
        auth_type="token",
        is_authenticated=True,
        source_app="mcp-agent-service",
        source_feature="agent-service",
    )
    root = mcp.fork_for_child_agent("44444444-4444-4444-4444-444444444444")
    assert root.origin_class == "api"
    final, witness = reconcile_origin(root)
    assert final == "api"
    assert "contradictions" not in witness


def test_fork_inside_a_running_conversation_is_still_child_agent():
    parent = _ctx(
        route="mcp:agent_run",
        auth_type="token",
        conversation_id="55555555-5555-5555-5555-555555555555",
    )
    child = parent.fork_for_child_agent("66666666-6666-6666-6666-666666666666")
    assert child.origin_class == "child_agent"


def test_root_fork_from_machine_context_stays_child_agent():
    # The usage gate leaves system/scheduled ungated: a machine fork must never
    # inherit those classes and slip out of a person's plan limit.
    for klass in ("scheduled", "system", "workflow"):
        root = _ctx(origin_class=klass, route="mcp:agent_run", auth_type="token").fork_for_child_agent(
            "77777777-7777-7777-7777-777777777777"
        )
        assert root.origin_class == "child_agent"


def test_root_fork_never_claims_attested_class_without_http_witness():
    root = _ctx(origin_class="human", auth_type="token").fork_for_child_agent(
        "88888888-8888-8888-8888-888888888888"
    )
    assert root.origin_class not in ("human", "client_auto", "api")


def test_labeler_style_helper_with_parent_is_child_agent_not_human():
    # Mandate helper: person's route + token (witnessed 'human'), but typed subagent with a parent.
    helper = _ctx(
        origin_class="human",
        auth_type="token",
        route="/ai/mandates/chat.default_new_chat",
        conversation_type="subagent",
        parent_conversation_id="88a134af-9db2-407e-8a1f-5c300da9657f",
    )
    final, witness = reconcile_origin(helper)
    assert final == "child_agent"
    assert witness["lineage_class"]["from"] == "human"


def test_person_started_standard_child_stays_human():
    session = _ctx(
        origin_class="human",
        auth_type="token",
        route="/ai/sessions/offers/x/start",
        conversation_type="standard",
        parent_conversation_id="88a134af-9db2-407e-8a1f-5c300da9657f",
    )
    assert reconcile_origin(session)[0] == "human"
