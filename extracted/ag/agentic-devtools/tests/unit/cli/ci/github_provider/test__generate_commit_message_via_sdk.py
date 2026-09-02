"""Tests for GitHubActionsProvider._generate_commit_message_via_sdk.

The SDK now supplies structured content and the final message is rendered through
the commit template via ``_render_squash_message_from_sdk``.  These tests exercise
the SDK *plumbing* (token, events, errors, timeout, the github_token fallback)
with the renderer mocked; rendering itself is covered by
``test__render_squash_message_from_sdk``.
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_RENDER = "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider._render_squash_message_from_sdk"


def _make_event(event_type: str, content: str | None = None) -> MagicMock:
    """Build a minimal mock SDK event object."""
    event = MagicMock()
    type_mock = MagicMock()
    type_mock.value = event_type
    event.type = type_mock
    if content is not None:
        data_mock = MagicMock()
        data_mock.content = content
        data_mock.message = content
        event.data = data_mock
    else:
        event.data = MagicMock(content="", message=None)
    return event


def _build_sdk_mocks(
    create_session_side_effect: Exception | None = None,
    create_session_fallback: bool = False,
) -> tuple[MagicMock, MagicMock, MagicMock]:
    """Return (mock_copilot_module, mock_session_module, mock_session).

    ``mock_session.send`` is left as a plain MagicMock so callers can replace it
    with an async function that fires events into the captured on_event callback.
    """
    mock_session = MagicMock()
    mock_session.disconnect = AsyncMock()
    mock_session.on = MagicMock()

    mock_client = MagicMock()
    mock_client.start = AsyncMock()
    mock_client.stop = AsyncMock()

    if create_session_side_effect is not None and not create_session_fallback:
        mock_client.create_session = AsyncMock(side_effect=create_session_side_effect)
    elif create_session_fallback:
        # First call raises the expected TypeError; second call succeeds.
        mock_client.create_session = AsyncMock(
            side_effect=[
                TypeError("unexpected keyword argument 'github_token'"),
                mock_session,
            ]
        )
    else:
        mock_client.create_session = AsyncMock(return_value=mock_session)

    mock_copilot = MagicMock()
    mock_copilot.CopilotClient.return_value = mock_client

    mock_session_module = MagicMock()
    mock_session_module.PermissionHandler = MagicMock()

    return mock_copilot, mock_session_module, mock_session


class TestGenerateCommitMessageViaSdk:
    """Tests for the Copilot-SDK-backed squash commit message generator."""

    # ── No token ─────────────────────────────────────────────────────────────

    def test_no_token_returns_none(self, monkeypatch: object) -> None:
        monkeypatch.delenv("COPILOT_GITHUB_TOKEN", raising=False)  # type: ignore[attr-defined]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider._generate_commit_message_via_sdk(
            head_sha="abc123",
            commit_subjects=["feat: test"],
        )
        assert result is None

    def test_empty_token_returns_none(self, monkeypatch: object) -> None:
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "")  # type: ignore[attr-defined]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider._generate_commit_message_via_sdk(
            head_sha="abc123",
            commit_subjects=["feat: test"],
        )
        assert result is None

    # ── git_root fallback ────────────────────────────────────────────────────

    def test_rev_parse_failure_falls_back_to_cwd(self, monkeypatch: object) -> None:
        """When rev-parse --show-toplevel fails, cwd fallback is used and rendering still proceeds."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_events_and_return(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "fix: something"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_events_and_return

        with patch.dict(sys.modules, {"copilot": mock_copilot, "copilot.session": mock_session_module}):
            with patch(
                "agentic_devtools.cli.ci.github_provider.GitHubActionsProvider._run_git",
                side_effect=RuntimeError("not a git repo"),
            ):
                with patch(_RENDER, return_value="fix: something") as mock_render:
                    provider = GitHubActionsProvider(repo="owner/repo")
                    result = provider._generate_commit_message_via_sdk(
                        head_sha="abc123",
                        commit_subjects=["fix: something"],
                    )

        assert result == "fix: something"
        call_kwargs = mock_render.call_args.kwargs
        assert isinstance(call_kwargs["git_root"], Path)

    # ── Happy path ───────────────────────────────────────────────────────────

    def test_sdk_happy_path_returns_message(self, monkeypatch: object) -> None:
        """SDK fires assistant.message then session.idle; the rendered template message is returned."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_events_and_return(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "add squash feature\n\n- did things"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_events_and_return

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            with patch(_RENDER, return_value="fix(#42): add squash feature\n\n- did things\n\n#42") as mock_render:
                provider = GitHubActionsProvider(repo="owner/repo")
                result = provider._generate_commit_message_via_sdk(
                    head_sha="abc123",
                    commit_subjects=["original subject"],
                    head_branch="fix/42/squash",
                )

        assert result == "fix(#42): add squash feature\n\n- did things\n\n#42"
        # Renderer received the raw SDK content, the branch-resolved key/type, and git_root.
        assert mock_render.call_args.args[0] == "add squash feature\n\n- did things"
        call_kwargs = mock_render.call_args.kwargs
        assert call_kwargs["issue_key"] == "42"
        assert call_kwargs["issue_type"] == "fix"
        assert isinstance(call_kwargs["git_root"], Path)

    def test_sdk_empty_content_returns_none(self, monkeypatch: object) -> None:
        """SDK fires session.idle without any assistant.message; returns None."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_idle_only(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("session.idle"))

        mock_session.send = fire_idle_only

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            provider = GitHubActionsProvider(repo="owner/repo")
            result = provider._generate_commit_message_via_sdk(
                head_sha="abc123",
                commit_subjects=["feat: test"],
            )

        assert result is None

    # ── Error event ──────────────────────────────────────────────────────────

    def test_sdk_error_event_returns_none(self, monkeypatch: object) -> None:
        """SDK fires an error event; returns None and logs a warning."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_error_event(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("session.error", "SDK internal error"))

        mock_session.send = fire_error_event

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            provider = GitHubActionsProvider(repo="owner/repo")
            result = provider._generate_commit_message_via_sdk(
                head_sha="abc123",
                commit_subjects=["feat: test"],
            )

        assert result is None

    # ── Timeout ──────────────────────────────────────────────────────────────

    def test_sdk_timeout_returns_none(self, monkeypatch: object) -> None:
        """asyncio.wait_for times out inside _run(); returns None and logs a warning."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def send_without_events(prompt: str) -> None:  # noqa: ARG001
            pass  # never fires events; wait_for will be patched to time out

        mock_session.send = send_without_events

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            with patch("asyncio.wait_for", side_effect=TimeoutError()):
                provider = GitHubActionsProvider(repo="owner/repo")
                result = provider._generate_commit_message_via_sdk(
                    head_sha="abc123",
                    commit_subjects=["feat: test"],
                    timeout_seconds=1,
                )

        assert result is None

    def test_sdk_timeout_covers_client_start(self, monkeypatch: object) -> None:
        """Timeout also covers SDK startup before a session is created."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, _ = _build_sdk_mocks()

        async def hang_on_start() -> None:
            await asyncio.Future()

        mock_copilot.CopilotClient.return_value.start = hang_on_start
        original_wait_for = asyncio.wait_for

        async def bounded_wait_for(awaitable, timeout):
            return await original_wait_for(awaitable, timeout=0.01)

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            with patch("asyncio.wait_for", side_effect=bounded_wait_for):
                provider = GitHubActionsProvider(repo="owner/repo")
                result = provider._generate_commit_message_via_sdk(
                    head_sha="abc123",
                    commit_subjects=["feat: test"],
                    timeout_seconds=1,
                )

        assert result is None

    # ── create_session github_token TypeError fallback ───────────────────────

    def test_sdk_github_token_type_error_falls_back(self, monkeypatch: object) -> None:
        """Older SDK that doesn't accept github_token kwarg; fallback create_session used."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks(
            create_session_fallback=True,
        )

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_events_and_return(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "chore: squash post-repair updates"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_events_and_return

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            with patch(_RENDER, return_value="chore(#42): squash post-repair updates\n\n#42"):
                provider = GitHubActionsProvider(repo="owner/repo")
                result = provider._generate_commit_message_via_sdk(
                    head_sha="abc123",
                    commit_subjects=["chore: squash post-repair updates"],
                    head_branch="chore/42/x",
                )

        assert result == "chore(#42): squash post-repair updates\n\n#42"
        # Ensure create_session was called twice (with then without github_token).
        assert mock_copilot.CopilotClient.return_value.create_session.call_count == 2

    # ── Renderer integration ─────────────────────────────────────────────────

    def test_sdk_blank_subjects_use_placeholder(self, monkeypatch: object) -> None:
        """Empty commit_subjects still build a prompt (with a placeholder) and render."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_message(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "add feature"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_message

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            with patch(_RENDER, return_value="chore: add feature") as mock_render:
                provider = GitHubActionsProvider(repo="owner/repo")
                result = provider._generate_commit_message_via_sdk(
                    head_sha="abc123",
                    commit_subjects=[],
                )

        assert result == "chore: add feature"
        mock_render.assert_called_once()

    def test_sdk_render_returns_none_propagates_none(self, monkeypatch: object) -> None:
        """When the renderer cannot produce a usable message, the generator returns None."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_message(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "add feature"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_message

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            with patch(_RENDER, return_value=None):
                provider = GitHubActionsProvider(repo="owner/repo")
                result = provider._generate_commit_message_via_sdk(
                    head_sha="abc123",
                    commit_subjects=["feat: add feature"],
                    head_branch="fix/42/x",
                )

        assert result is None

    def test_sdk_conversational_message_returns_none(self, monkeypatch: object) -> None:
        """Conversational SDK output is rejected; returns None for deterministic fallback."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_conversational_message(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "Here is the commit message: feat: add feature"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_conversational_message

        with patch.dict(
            sys.modules,
            {"copilot": mock_copilot, "copilot.session": mock_session_module},
        ):
            provider = GitHubActionsProvider(repo="owner/repo")
            result = provider._generate_commit_message_via_sdk(
                head_sha="abc123",
                commit_subjects=["feat: add feature"],
            )

        assert result is None

    # ── Explicit issue_key propagation (regression for GitHub adapter) ────────

    def test_explicit_issue_key_passed_to_renderer(self, monkeypatch: object) -> None:
        """Pre-resolved issue_key bypasses internal re-resolution and reaches the renderer."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_events_and_return(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "make coding-agent assignment reliable"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_events_and_return

        with patch.dict(sys.modules, {"copilot": mock_copilot, "copilot.session": mock_session_module}):
            with patch(
                _RENDER,
                return_value="fix(#2262): make coding-agent assignment reliable\n\n#2262",
            ) as mock_render:
                provider = GitHubActionsProvider(repo="owner/repo")
                result = provider._generate_commit_message_via_sdk(
                    head_sha="abc123",
                    commit_subjects=["fix(#2262): make coding-agent assignment reliable", "Initial plan"],
                    head_branch="fix/2262/make-coding-agent-assignment-reliable",
                    issue_key="2262",
                )

        assert result == "fix(#2262): make coding-agent assignment reliable\n\n#2262"
        call_kwargs = mock_render.call_args.kwargs
        # The pre-resolved key must reach the renderer — not re-derived internally.
        assert call_kwargs["issue_key"] == "2262"
        assert call_kwargs["issue_type"] == "fix"

    def test_explicit_issue_key_skips_internal_resolution(self, monkeypatch: object) -> None:
        """When issue_key is provided, _resolve_issue_key_adapter_aware is never called."""
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_events(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "fix: something"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_events

        with patch.dict(sys.modules, {"copilot": mock_copilot, "copilot.session": mock_session_module}):
            with patch(_RENDER, return_value="fix(#2262): something\n\n#2262"):
                with patch.object(
                    GitHubActionsProvider,
                    "_resolve_issue_key_adapter_aware",
                    wraps=GitHubActionsProvider._resolve_issue_key_adapter_aware,
                ) as mock_resolve:
                    provider = GitHubActionsProvider(repo="owner/repo")
                    provider._generate_commit_message_via_sdk(
                        head_sha="abc123",
                        commit_subjects=["fix(#2262): something"],
                        head_branch="fix/2262/something",
                        issue_key="2262",
                    )

        # Adapter-aware resolution must NOT be called when a key is already provided.
        mock_resolve.assert_not_called()

    def test_github_adapter_non_numeric_branch_segment_uses_subject_key(self, monkeypatch: object) -> None:
        """Regression: branch with non-numeric segment + github adapter resolves key from subjects.

        Scenario: branch ``fix/non-numeric-segment/description`` on a github-adapter repo.
        The subjects contain ``fix(#2262): ...``.  Without the fix, ``issueKey`` was
        ``None`` in the template context → warning fired and fallback message had no scope.
        With the fix, the adapter-aware resolution finds ``2262`` in subjects and both the
        SDK path and the deterministic fallback message carry ``(#2262)`` / ``#2262``.
        """
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "test-token")  # type: ignore[attr-defined]
        mock_copilot, mock_session_module, mock_session = _build_sdk_mocks()

        captured_callback: list = []

        def capture_on(cb: object) -> None:
            captured_callback.append(cb)

        mock_session.on = MagicMock(side_effect=capture_on)

        async def fire_events(prompt: str) -> None:  # noqa: ARG001
            cb = captured_callback[0]
            cb(_make_event("assistant.message", "make coding-agent assignment reliable"))
            cb(_make_event("session.idle"))

        mock_session.send = fire_events

        subjects = [
            "fix(#2262): make coding-agent assignment reliable",
            "Initial plan",
        ]

        with patch.dict(sys.modules, {"copilot": mock_copilot, "copilot.session": mock_session_module}):
            with patch(
                "agentic_devtools.cli.ci.github_provider.load_platform_config",
                return_value={"issue_adapter": "github"},
            ):
                with patch(
                    _RENDER,
                    return_value="fix(#2262): make coding-agent assignment reliable\n\n#2262",
                ) as mock_render:
                    provider = GitHubActionsProvider(repo="owner/repo")
                    result = provider._generate_commit_message_via_sdk(
                        head_sha="6e70896e",
                        commit_subjects=subjects,
                        head_branch="fix/non-numeric-segment/description",
                        issue_key="2262",  # Pre-resolved by _squash_and_force_push
                    )

        assert result == "fix(#2262): make coding-agent assignment reliable\n\n#2262"
        # issueKey must reach the renderer — no unresolved-variable warning.
        call_kwargs = mock_render.call_args.kwargs
        assert call_kwargs["issue_key"] == "2262"
