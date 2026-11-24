"""Exercise the public custody edges in isolated, network-denied processes."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("scenario", ["standalone", "unbound", "immutable", "adopt_head_before", "adopt_stream", "adopt_head_after", "adopt_publication", "read_stream", "read_publication", "replay_denied", "publication_exit", "success", "retry_serialization", "retry_unique", "unrelated_unique", "drift_cause", "descriptor_mismatch"])
def test_external_object_runtime_isolated(scenario: str) -> None:
    env = {"PATH": os.environ.get("PATH", ""), "PYTHONPATH": os.pathsep.join(sys.path), "CASE": scenario, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), "child"], env=env, text=True, capture_output=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr


async def _exercise() -> None:
    from contextlib import asynccontextmanager
    import test_external_objects as fixture
    import matrx_files.external_objects as ext
    from matrx_files.external_object_runtime import declare_external_object_runtime, bind_external_object_guard
    from matrx_files.retention import VOICE_RECORDING_RETENTION_POLICY

    case = os.environ["CASE"]
    engine = fixture._Engine()  # deliberately created before host declaration
    def classifier(uri):
        return uri.startswith("s3://recordings/")
    calls = []
    @asynccontextmanager
    async def transaction(*, database):
        rows, events = dict(engine.db.rows), list(engine.db.events)
        try:
            yield
        except BaseException:
            engine.db.rows, engine.db.events = rows, events
            raise
    ext.transaction = transaction
    class Guard:
        async def admit_remote(self, eng, uri, *, operation, unit, file_id=None, descriptor=None):
            assert eng is engine and uri == fixture.STORAGE_URI and operation is token
            if unit.startswith("adopt_"):
                from matrx_files.external_object_runtime import adoption_descriptor
                assert descriptor == adoption_descriptor(fixture._request(), VOICE_RECORDING_RETENTION_POLICY)
            calls.append(unit)
            if case == unit:
                raise PermissionError(unit)
        @asynccontextmanager
        async def publication_scope(self, eng, uri, *, operation, unit, file_id=None, descriptor=None):
            assert eng is engine and uri == fixture.STORAGE_URI and operation is token
            if unit.startswith("adopt_"):
                from matrx_files.external_object_runtime import adoption_descriptor
                assert descriptor == adoption_descriptor(fixture._request(), VOICE_RECORDING_RETENTION_POLICY)
            calls.append(unit)
            if case == unit:
                raise PermissionError(unit)
            rows, events = dict(engine.db.rows), list(engine.db.events)
            try:
                yield
                if case == "publication_exit" and unit == "adopt_publication":
                    raise PermissionError("publication commit denied")
            except BaseException:
                engine.db.rows, engine.db.events = rows, events
                raise
    guard = Guard()
    token = object()
    if case == "standalone":
        declare_external_object_runtime(mode="standalone_trusted", namespace_classifier=classifier)
    else:
        declare_external_object_runtime(mode="host_required", namespace_classifier=classifier)
        declare_external_object_runtime(mode="host_required", namespace_classifier=classifier)
        if case != "unbound":
            bind_external_object_guard(guard)
            bind_external_object_guard(guard)
        if case == "immutable":
            for mutation in (lambda: bind_external_object_guard(Guard()), lambda: declare_external_object_runtime(mode="standalone_trusted", namespace_classifier=classifier), lambda: declare_external_object_runtime(mode="host_required", namespace_classifier=lambda _: True, guard=guard)):
                try:
                    mutation()
                except RuntimeError:
                    pass
                else:
                    raise AssertionError("runtime changed")
    heads, gets = [], []
    original_head, original_get = engine.router.s3.get_metadata_async, engine.router.download_to_path_async
    async def head(path):
        heads.append(path)
        return await original_head(path)
    async def get(uri, path):
        gets.append(uri)
        return await original_get(uri, path)
    engine.router.s3.get_metadata_async = head
    engine.router.download_to_path_async = get
    from matrx_files.external_object_runtime import adoption_descriptor
    desc = adoption_descriptor(fixture._request(), VOICE_RECORDING_RETENTION_POLICY)
    if case == "descriptor_mismatch":
        from dataclasses import replace, FrozenInstanceError
        try:
            desc.owner_id = "changed"
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError("descriptor is mutable")
        try:
            await ext.adopt_external_object(engine, fixture._request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY, operation=token, descriptor=replace(desc, owner_id="wrong"))
        except ext.ExternalObjectMismatchError:
            assert not heads and not gets
            return
        raise AssertionError("mismatch admitted")
    phase = ext._adopt_database_phase
    phase_calls = 0
    class DBError(Exception):
        sqlstate = "40001" if case == "retry_serialization" else "23505"
        constraint_name = "cld_files_owner_id_file_path_key" if case == "retry_unique" else "unrelated_key"
    async def flaky(*args):
        nonlocal phase_calls
        phase_calls += 1
        if phase_calls == 1:
            if case in {"retry_serialization", "retry_unique", "unrelated_unique"}:
                raise DBError("first phase")
            if case == "drift_cause":
                raise ext.ExternalObjectDriftError("refused") from DBError("collision")
        return await phase(*args)
    if case in {"retry_serialization", "retry_unique", "unrelated_unique", "drift_cause"}:
        ext._adopt_database_phase = flaky
    try:
        adopted = await ext.adopt_external_object(engine, fixture._request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY, operation=token)
    except (DBError, ext.ExternalObjectDriftError):
        assert case in {"unrelated_unique", "drift_cause"} and phase_calls == 1
        assert calls.count("adopt_publication") == 1 and len(heads) == 2 and len(gets) == 1
        return
    except PermissionError:
        assert case in {"unbound", "adopt_head_before", "adopt_stream", "adopt_head_after", "adopt_publication", "publication_exit"}
        assert not engine.db.rows and not engine.db.events
        expected = {"unbound": (0, 0), "adopt_head_before": (0, 0), "adopt_stream": (1, 0), "adopt_head_after": (1, 1), "adopt_publication": (2, 1), "publication_exit": (2, 1)}
        assert (len(heads), len(gets)) == expected[case]
        return
    if case in {"retry_serialization", "retry_unique"}:
        assert phase_calls == 2 and calls.count("adopt_publication") == 2
        assert len(heads) == 2 and len(gets) == 1 and len(engine.db.events) == 1
        return
    assert case not in {"unbound", "adopt_head_before", "adopt_stream", "adopt_head_after", "adopt_publication"}
    events_before = len(engine.db.events)
    reads = []
    original_read = engine.router.read_async
    async def read(uri):
        reads.append(uri)
        return await original_read(uri)
    engine.router.read_async = read
    try:
        result = await ext.read_external_object_with_receipt(engine, file_id=adopted.file_id, user_id=fixture.OWNER_ID, operation=token)
    except PermissionError:
        assert case in {"read_stream", "read_publication"}
        assert len(reads) == (0 if case == "read_stream" else 1)
        assert len(engine.db.events) == events_before
        return
    assert result.content == fixture.CONTENT
    if case == "replay_denied":
        @asynccontextmanager
        async def deny_replay(*args, **kwargs):
            raise PermissionError("replay denied")
            yield
        guard.publication_scope = deny_replay
        before = list(engine.db.events)
        try:
            await ext.adopt_external_object(engine, fixture._request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY, operation=token)
        except PermissionError:
            assert engine.db.events == before and len(engine.db.rows) == 1
            return
        raise AssertionError("replay was admitted")
    replay = await ext.adopt_external_object(engine, fixture._request(), retention_policy=VOICE_RECORDING_RETENTION_POLICY, operation=token)
    assert replay.replayed and replay.file_id == adopted.file_id
    if case != "standalone":
        assert calls[:6] == ["adopt_head_before", "adopt_stream", "adopt_head_after", "adopt_publication", "read_stream", "read_publication"]


if __name__ == "__main__":
    import socket
    def deny(*args, **kwargs):
        raise AssertionError("network is disabled")
    socket.socket.connect = deny
    socket.create_connection = deny
    socket.getaddrinfo = deny
    import dotenv
    dotenv.load_dotenv = lambda *a, **k: False
    dotenv.dotenv_values = lambda *a, **k: {}
    import asyncio
    asyncio.run(_exercise())
