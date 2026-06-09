from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
import getpass
import json
import os
from pathlib import Path
import subprocess
from threading import Lock
from typing import TYPE_CHECKING, Any

from anyio import NamedTemporaryFile, Path as AsyncPath

from drydock.core.session.session_loader import (
    MESSAGES_FILENAME,
    METADATA_FILENAME,
    SessionLoader,
)
from drydock.core.types import AgentStats, LLMMessage, Role, SessionMetadata
from drydock.core.utils import is_windows, utc_now

if TYPE_CHECKING:
    from drydock.core.agents.models import AgentProfile
    from drydock.core.config import SessionLoggingConfig, DrydockConfig
    from drydock.core.tools.manager import ToolManager


TMP_CLEANUP_INTERVAL = timedelta(seconds=5)


class SessionLogger:
    def __init__(self, session_config: SessionLoggingConfig, session_id: str) -> None:
        self.session_config = session_config
        self.enabled = session_config.enabled
        self._last_tmp_cleanup_at: datetime | None = None
        self._tmp_cleanup_lock = Lock()

        if not self.enabled:
            self.save_dir: Path | None = None
            self.session_prefix: str | None = None
            self.session_id: str = "disabled"
            self.session_start_time: str = "N/A"
            self.session_dir: Path | None = None
            self.session_metadata: SessionMetadata | None = None
            return

        self.save_dir = Path(session_config.save_dir)
        self.session_prefix = session_config.session_prefix
        self.session_id = session_id
        self.session_start_time = utc_now().isoformat()

        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir = self.save_folder
        # Eagerly materialize session_dir on disk BEFORE publishing the
        # marker. Previously the dir was created lazily on the first
        # log_event call, which could be 60+ seconds after spawn for
        # slow startups. External watchers (tui_capture, test_harness
        # runner) checked target.is_dir() before attaching and saw
        # FALSE until the first event landed — so they timed out
        # waiting on a session that drydock had already published but
        # hadn't yet realized on disk. Observed 2026-05-21 across 10
        # consecutive test_harness cases per iter (~20% of attempts):
        # msgs+=1, no LLM call, runner SIGINT'd waiting for activity
        # that never came.
        try:
            self.session_dir.mkdir(parents=True, exist_ok=True)
        except Exception:  # noqa: BLE001 — never block init
            pass
        self.session_metadata = self._initialize_session_metadata()
        # Publish current session dir at init too (not just on reset)
        # so external watchers can find the very first session.
        try:
            self._publish_current_session()
        except Exception:  # noqa: BLE001
            pass

    @property
    def save_folder(self) -> Path:
        if self.save_dir is None or self.session_prefix is None:
            raise RuntimeError(
                "Cannot get session save folder when logging is disabled"
            )

        timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{self.session_prefix}_{timestamp}_{self.session_id[:8]}"
        return self.save_dir / folder_name

    @property
    def metadata_filepath(self) -> Path:
        if self.session_dir is None:
            raise RuntimeError(
                "Cannot get session metadata filepath when logging is disabled"
            )
        return self.session_dir / METADATA_FILENAME

    @property
    def messages_filepath(self) -> Path:
        if self.session_dir is None:
            raise RuntimeError(
                "Cannot get session messages filepath when logging is disabled"
            )
        return self.session_dir / MESSAGES_FILENAME

    def log_event(self, event: dict) -> None:
        """Append a structured event to <session_dir>/events.jsonl.

        Used for things that aren't conversation messages but ARE
        worth recording for replay/debugging — e.g.
        user_injection_queued (typed during agent run), tool_recycled,
        modal_opened, etc. Fail-silent: never raise.

        Creates session_dir on first call if it doesn't exist yet
        (early-session events can fire before persist_messages
        materialises the dir).
        """
        if self.session_dir is None:
            return
        try:
            import json as _json
            import time as _time
            event_with_ts = {"ts": _time.time(), **event}
            self.session_dir.mkdir(parents=True, exist_ok=True)
            with (self.session_dir / "events.jsonl").open("a") as f:
                f.write(_json.dumps(event_with_ts) + "\n")
        except Exception:  # noqa: BLE001 — never block on logging
            pass

    @property
    def git_commit(self) -> str | None:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                stdin=subprocess.DEVNULL if is_windows() else None,
                text=True,
                timeout=5.0,
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
        except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
            pass
        return None

    @property
    def git_branch(self) -> str | None:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                stdin=subprocess.DEVNULL if is_windows() else None,
                text=True,
                timeout=5.0,
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
        except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
            pass
        return None

    @property
    def username(self) -> str:
        try:
            return getpass.getuser()
        except Exception:
            return "unknown"

    def _initialize_session_metadata(self) -> SessionMetadata:
        git_commit = self.git_commit
        git_branch = self.git_branch
        user_name = self.username

        return SessionMetadata(
            session_id=self.session_id,
            start_time=self.session_start_time,
            end_time=None,
            git_commit=git_commit,
            git_branch=git_branch,
            username=user_name,
            environment={"working_directory": str(Path.cwd())},
        )

    def _get_title(self, messages: Sequence[LLMMessage]) -> str:
        first_user_message = None
        for message in messages:
            if message.role == Role.user:
                first_user_message = message
                break

        if first_user_message is None:
            title = "Untitled session"
        else:
            MAX_TITLE_LENGTH = 50
            text = str(first_user_message.content)
            title = text[:MAX_TITLE_LENGTH]
            if len(text) > MAX_TITLE_LENGTH:
                title += "…"

        return title

    @staticmethod
    async def persist_metadata(metadata: Any, session_dir: Path) -> None:
        temp_metadata_filepath = None
        metadata_filepath = session_dir / METADATA_FILENAME
        try:
            async with NamedTemporaryFile(
                mode="w",
                suffix=".json.tmp",
                dir=str(session_dir),
                delete=False,
                encoding="utf-8",
            ) as f:
                temp_metadata_filepath = Path(str(f.name))
                await f.write(json.dumps(metadata, indent=2, ensure_ascii=False))
                await f.flush()
                os.fsync(f.wrapped.fileno())

            os.replace(temp_metadata_filepath, str(metadata_filepath))
        except Exception as e:
            raise RuntimeError(
                f"Failed to persist session metadata to {metadata_filepath}: {e}"
            ) from e
        finally:
            if (
                temp_metadata_filepath
                and temp_metadata_filepath.exists()
                and temp_metadata_filepath.is_file()
            ):
                temp_metadata_filepath.unlink()

    @staticmethod
    async def persist_messages(messages: list[dict], session_dir: Path) -> None:
        messages_filepath = session_dir / "messages.jsonl"
        try:
            if not messages_filepath.exists():
                messages_filepath.touch()

            async with await AsyncPath(messages_filepath).open(
                "a", encoding="utf-8"
            ) as f:
                for message in messages:
                    await f.write(json.dumps(message, ensure_ascii=False) + "\n")
                    await f.flush()
                    os.fsync(f.wrapped.fileno())
        except Exception as e:
            raise RuntimeError(
                f"Failed to persist session messages to {messages_filepath}: {e}"
            ) from e

    async def save_interaction(
        self,
        messages: Sequence[LLMMessage],
        stats: AgentStats,
        base_config: DrydockConfig,
        tool_manager: ToolManager,
        agent_profile: AgentProfile,
    ) -> None:
        if not self.enabled or self.session_dir is None:
            return

        if self.session_metadata is None:
            return

        if not any(msg.role != Role.system for msg in messages):
            return

        # If the session directory does not exist, create it
        try:
            self.session_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise RuntimeError(
                f"Failed to create session directory at {self.session_dir}: {type(e).__name__}: {e}"
            ) from e

        # Read old metadata and get total_messages
        try:
            if self.metadata_filepath.exists():
                async with await AsyncPath(self.metadata_filepath).open(
                    encoding="utf-8", errors="ignore"
                ) as f:
                    old_metadata = json.loads(await f.read())
                    old_total_messages = old_metadata["total_messages"]
            else:
                old_total_messages = 0
        except Exception as e:
            raise RuntimeError(
                f"Failed to read session metadata at {self.metadata_filepath}: {e}"
            ) from e

        try:
            non_system_messages = [m for m in messages if m.role != Role.system]
            # Append new messages
            new_messages = non_system_messages[old_total_messages:]

            if len(new_messages) == 0:
                return

            messages_data = [m.model_dump(exclude_none=True) for m in new_messages]
            await SessionLogger.persist_messages(messages_data, self.session_dir)

            # If message update succeeded, write metadata.
            # 2026-06-08: per-tool isolation — same defensive pattern as
            # format.get_available_tools. A single tool with a broken
            # run() annotation used to crash session save (and through
            # save_interaction's re-raise, the whole TUI session). Skip
            # broken tools with a logged warning; the session metadata
            # just lacks those entries.
            tools_available = []
            for tool_class in tool_manager.available_tools.values():
                try:
                    tools_available.append({
                        "type": "function",
                        "function": {
                            "name": tool_class.get_name(),
                            "description": tool_class.description,
                            "parameters": tool_class.get_parameters(),
                        },
                    })
                except Exception as tool_err:
                    from drydock.core.logger import logger
                    logger.error(
                        "[session_logger] skipping broken tool %r: %s",
                        getattr(tool_class, "__name__", tool_class),
                        tool_err,
                    )

            title = self._get_title(messages)
            system_prompt = (
                messages[0].model_dump()
                if len(messages) > 0 and messages[0].role == Role.system
                else None
            )
            total_messages = len(non_system_messages)

            metadata_dump = {
                **self.session_metadata.model_dump(),
                "end_time": utc_now().isoformat(),
                "stats": stats.model_dump(),
                "title": title,
                "total_messages": total_messages,
                "tools_available": tools_available,
                "config": base_config.model_dump(mode="json"),
                "agent_profile": {
                    "name": agent_profile.name,
                    "overrides": agent_profile.overrides,
                },
                "system_prompt": system_prompt,
            }

            await SessionLogger.persist_metadata(metadata_dump, self.session_dir)
        except Exception as e:
            raise RuntimeError(
                f"Failed to save session to {self.session_dir}: {e}"
            ) from e
        finally:
            self.maybe_cleanup_tmp_files()

    def reset_session(self, session_id: str) -> None:
        """Clear existing session info and setup a new session.

        Materializes the new session_dir on disk immediately so external
        watchers (drydock-using tools, dashboards, the stress harness)
        can discover the new session BEFORE the first message gets
        persisted.

        Also publishes the new session_dir path to
        ~/.drydock/current_session.txt — any external tool that wants to
        know "which drydock session is active right now" can read this
        single file instead of doing a heuristic mtime-sorted search of
        all ~3k+ historical session dirs. Solves the post-/clear race
        where a watcher polling between reset_session and the OS
        filesystem flush would cache the OLD dir as "newest".
        """
        if not self.enabled:
            return

        self.session_id = session_id
        self.session_start_time = utc_now().isoformat()
        self.session_dir = self.save_folder
        self.session_metadata = self._initialize_session_metadata()
        try:
            self.session_dir.mkdir(parents=True, exist_ok=True)
            # Touch the messages.jsonl marker so watchers see this as a
            # discoverable session dir immediately, not after the first
            # message lands.
            (self.session_dir / MESSAGES_FILENAME).touch(exist_ok=True)
            # Publish the active session_dir for external watchers.
            self._publish_current_session()
            self.log_event({
                "event": "session_reset",
                "session_id": session_id,
            })
        except Exception:  # noqa: BLE001 — never block on disk
            pass

    def _publish_current_session(self) -> None:
        """Write the active session_dir path to per-project AND per-pid
        marker files so external watchers can find the right drydock.

        Three write targets:
          1. `<cwd>/.drydock/current_session.txt` — per-project. A watcher
             that knows the cwd it's targeting reads this. Concurrent
             drydocks in different folders don't clobber each other.
          2. `~/.drydock/sessions_by_pid/<pid>.txt` — per-process. Lets a
             watcher addressing a specific drydock PID find its session
             without depending on cwd state.
          3. `~/.drydock/current_session.txt` — last-writer-wins legacy
             marker. Kept for back-compat with watchers that don't know
             the cwd yet; future code should prefer #1 or #2.

        Atomic via write-then-rename. Fail-silent — publishing is an
        observability convenience, never block the session on it.
        """
        if self.session_dir is None:
            return
        contents = str(self.session_dir) + "\n"
        # (1) per-project
        try:
            cwd = Path.cwd()
            project_pub = cwd / ".drydock" / "current_session.txt"
            project_pub.parent.mkdir(parents=True, exist_ok=True)
            tmp = project_pub.with_suffix(".txt.tmp")
            tmp.write_text(contents)
            tmp.replace(project_pub)
        except Exception:  # noqa: BLE001
            pass
        # (2) per-pid
        try:
            import os as _os
            pid_dir = Path.home() / ".drydock" / "sessions_by_pid"
            pid_dir.mkdir(parents=True, exist_ok=True)
            pid_pub = pid_dir / f"{_os.getpid()}.txt"
            tmp = pid_pub.with_suffix(".txt.tmp")
            tmp.write_text(contents)
            tmp.replace(pid_pub)
        except Exception:  # noqa: BLE001
            pass
        # (3) legacy global — last writer wins. Kept ONLY for watchers
        # that haven't been updated to look at the per-project path yet.
        try:
            pub_path = Path.home() / ".drydock" / "current_session.txt"
            pub_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = pub_path.with_suffix(".txt.tmp")
            tmp_path.write_text(contents)
            tmp_path.replace(pub_path)
        except Exception:  # noqa: BLE001
            pass

    def resume_existing_session(self, session_id: str, session_dir: Path) -> None:
        if not self.enabled:
            return

        self.session_id = session_id
        self.session_dir = session_dir
        self.session_metadata = SessionLoader.load_metadata(session_dir)

        if self.session_metadata.start_time:
            self.session_start_time = self.session_metadata.start_time

        # 2026-05-18: also publish on resume. Without this, drydocks
        # that auto-resume an existing session (the common path when
        # the user re-launches in a directory with a recent session)
        # never write per-pid or per-project markers — and external
        # watchers (tui_capture, shakedown SessionWatcher) couldn't
        # bind to those drydocks. Both running drydocks observed in
        # the operator's session were resumed and missing markers.
        try:
            self._publish_current_session()
        except Exception:  # noqa: BLE001
            pass

    def cleanup_tmp_files(self) -> None:
        """Delete temporary files created more than 5 minutes ago"""
        if not self.enabled or not self.save_dir:
            return

        now = utc_now()
        ago = now - timedelta(minutes=5)

        tmp_files = self.save_dir.glob("**/*.json.tmp")  # Recursive search

        for file_path in tmp_files:
            if file_path.is_file():
                try:
                    file_mtime = datetime.fromtimestamp(
                        file_path.stat().st_mtime, tz=UTC
                    )
                    if file_mtime < ago:
                        file_path.unlink()
                except Exception:
                    continue

    def maybe_cleanup_tmp_files(self) -> None:
        if not self.enabled or not self.save_dir:
            return

        if not self._tmp_cleanup_lock.acquire(blocking=False):
            return
        try:
            now = utc_now()
            if (
                self._last_tmp_cleanup_at is not None
                and now - self._last_tmp_cleanup_at < TMP_CLEANUP_INTERVAL
            ):
                return

            self.cleanup_tmp_files()
            self._last_tmp_cleanup_at = now
        finally:
            self._tmp_cleanup_lock.release()
