"""Pytest plugin: .eval.py modules export suite and client. No writes during collection."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
import threading
from pathlib import Path
from typing import Any, Coroutine

import pytest

from .client import EvalClient
from .datasets import publish_eval_suite, read_eval_dataset
from .models import EvalDataset, EvalSuite, LocalEvaluator, Selection
from .runner import create_eval_suite_run, run_eval_suite


class Loop:
    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.thread.start()

    def call(self, coroutine: Coroutine[Any, Any, Any]) -> Any:
        return asyncio.run_coroutine_threadsafe(coroutine, self.loop).result()

    def close(self) -> None:
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()


class SuiteState:
    def __init__(self, suite: EvalSuite, client: EvalClient) -> None:
        self.suite, self.client = suite, client
        self.loop = Loop()
        self.session = None
        self.selected: list[str] = []
        self.attempts: dict[str, int] = {}
        self.dataset = None
        self.result = None
        self.started = False
        if isinstance(suite.dataset, EvalDataset):
            self.rows = suite.dataset.rows
        else:
            self.dataset = self.loop.call(
                read_eval_dataset(
                    client, suite.dataset, version_id=suite.dataset_version_id
                )
            )
            self.rows = self.dataset.rows

    async def run_row(self, row_id: str) -> None:
        if self.session is None:
            published = await publish_eval_suite(self.client, self.suite)
            dataset = await read_eval_dataset(
                self.client, published.dataset, version_id=published.dataset_version_id
            )
            if self.dataset and dataset.version.id != self.dataset.version.id:
                raise ValueError(
                    "Dataset changed after pytest collection; rerun collection"
                )
            self.dataset = dataset
            self.session = await create_eval_suite_run(
                self.client,
                published,
                selection=Selection(dataset=dataset, row_ids=self.selected),
            )
            self.started = True
        attempt = self.attempts.get(row_id, 0)
        self.attempts[row_id] = attempt + 1
        result = await self.session.run(
            selection=Selection(dataset=self.dataset, row_ids=[row_id]), attempt=attempt
        )
        row = result.rows[0]
        assert row.status == "done", f"{row.name}: {row.error or row.status}"
        assert len(row.verdicts) == len(self.suite.evaluators), (
            "Missing evaluator verdicts"
        )
        failures = [v for v in row.verdicts if v.state not in ("passed", "measurement")]
        assert not failures, "\n".join(
            f"{v.evaluator}: {v.state} {v.verdict}" for v in failures
        )

    async def run_batch(self) -> None:
        self.started = True
        self.result = await run_eval_suite(self.client, self.suite)
        assert self.result.passed, f"Eval failed/incomplete: {self.result.wire()}"

    def finish(self) -> None:
        try:
            if self.session:
                self.result = self.loop.call(self.session.finish())
        finally:
            self.loop.close()


class EvalFile(pytest.File):
    def collect(self) -> Any:
        directory = self.path.parent
        package = []
        import_root = directory
        while (import_root / "__init__.py").exists():
            package.insert(0, import_root.name)
            import_root = import_root.parent
        if not package:
            # Bare sibling imports share Python's global module namespace. Reject
            # collisions before collection or lazy imports can select another app.
            siblings = getattr(self.config, "_raindrop_eval_siblings", {})
            for child in directory.iterdir():
                if child.suffix == ".py" and child.stem.isidentifier():
                    name = child.stem
                    origin = child.resolve()
                elif child.is_dir() and (child / "__init__.py").exists():
                    name = child.name
                    origin = (child / "__init__.py").resolve()
                else:
                    continue
                if name == "conftest":
                    continue
                cached = getattr(sys.modules.get(name), "__file__", None)
                previous = Path(cached).resolve() if cached else siblings.get(name)
                if previous is not None and previous != origin:
                    raise ValueError(
                        f"Ambiguous eval import {name!r}: {previous} and {origin}. "
                        "Add __init__.py to each eval directory and use relative "
                        "or package-qualified application imports."
                    )
                siblings[name] = origin
            self.config._raindrop_eval_siblings = siblings
        if str(import_root) not in sys.path:
            sys.path.insert(0, str(import_root))
        spec = importlib.util.spec_from_file_location(
            ".".join([*package, f"raindrop_evals_{id(self)}"]), self.path
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        if not isinstance(module.suite, EvalSuite) or not isinstance(
            module.client, EvalClient
        ):
            raise ValueError(
                "Eval module must export suite = define_eval_suite(...) and client = EvalClient(...)"
            )
        state = SuiteState(module.suite, module.client)
        states = getattr(self.config, "_raindrop_eval_states", [])
        states.append(state)
        self.config._raindrop_eval_states = states
        if all(
            isinstance(entry.evaluator, LocalEvaluator)
            for entry in state.suite.evaluators
        ):
            for row in state.rows:
                yield EvalItem.from_parent(
                    self, name=f"{row.id}: {row.name}", state=state, row_id=row.id
                )
        else:
            yield EvalItem.from_parent(
                self, name=state.suite.name, state=state, row_id=None
            )


class EvalItem(pytest.Item):
    def __init__(self, *, state: SuiteState, row_id: str | None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.state, self.row_id = state, row_id

    def runtest(self) -> None:
        self.state.loop.call(
            self.state.run_row(self.row_id) if self.row_id else self.state.run_batch()
        )

    def reportinfo(self) -> tuple[Path, int, str]:
        return self.path, 0, self.name


def pytest_configure(config: Any) -> None:
    # Use pytest's single Python collector, including explicit file arguments.
    config.addinivalue_line("python_files", "*.eval.py")


@pytest.hookimpl(tryfirst=True)
def pytest_pycollect_makemodule(module_path: Path, parent: Any) -> Any:
    if module_path.name.endswith(".eval.py"):
        return EvalFile.from_parent(parent, path=module_path)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(items: list[Any]) -> None:
    for item in items:
        if isinstance(item, EvalItem) and item.row_id:
            item.state.selected.append(item.row_id)


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    errors = []
    for state in getattr(session.config, "_raindrop_eval_states", []):
        try:
            state.finish()
        except Exception as error:
            errors.append(str(error))
    if errors:
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter:
            reporter.write_sep("=", "Raindrop run finalization failed")
            for error in errors:
                reporter.write_line(error)


def pytest_terminal_summary(terminalreporter: Any) -> None:
    for state in getattr(terminalreporter.config, "_raindrop_eval_states", []):
        if state.result:
            terminalreporter.write_line(f"Raindrop run: {state.result.run_id}")
            for evaluator in state.result.evaluators:
                terminalreporter.write_line(evaluator.get("url", ""))
