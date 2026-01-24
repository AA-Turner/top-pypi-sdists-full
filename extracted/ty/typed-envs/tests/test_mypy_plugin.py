from __future__ import annotations

import textwrap
import os
import sys
from pathlib import Path

import pytest

mypy = pytest.importorskip("mypy.api")


def _run_mypy(tmp_path: Path, source: str) -> tuple[str, str, int]:
    repo_root = Path(__file__).resolve().parents[1]
    source_path = tmp_path / "sample.py"
    config_path = tmp_path / "mypy.ini"

    source_path.write_text(textwrap.dedent(source))
    config_path.write_text(
        textwrap.dedent(
            """
            [mypy]
            plugins = typed_envs.mypy_plugin

            [mypy-typed_envs.*]
            ignore_errors = True
            """
        ).lstrip()
    )

    prior_mypy_path = os.environ.get("MYPYPATH")
    prior_python_path = os.environ.get("PYTHONPATH")
    sys_path_snapshot = list(sys.path)
    os.environ["MYPYPATH"] = (
        str(repo_root)
        if not prior_mypy_path
        else f"{repo_root}{os.pathsep}{prior_mypy_path}"
    )
    os.environ["PYTHONPATH"] = (
        str(repo_root)
        if not prior_python_path
        else f"{repo_root}{os.pathsep}{prior_python_path}"
    )
    sys.path.insert(0, str(repo_root))
    try:
        stdout, stderr, exit_status = mypy.run(
            [
                "--config-file",
                str(config_path),
                str(source_path),
            ]
        )
    finally:
        sys.path[:] = sys_path_snapshot
        if prior_mypy_path is None:
            os.environ.pop("MYPYPATH", None)
        else:
            os.environ["MYPYPATH"] = prior_mypy_path
        if prior_python_path is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = prior_python_path
    return stdout, stderr, exit_status


def _assert_mypy_ok(tmp_path: Path, source: str) -> None:
    stdout, stderr, exit_status = _run_mypy(tmp_path, source)
    assert exit_status == 0, stdout
    assert "error:" not in stdout
    assert stderr == ""


def test_mypy_plugin_exhaustive_cases(tmp_path: Path) -> None:
    source = """
        import typed_envs
        from dataclasses import dataclass
        from enum import Enum
        from typing import (
            Any,
            Annotated,
            Final,
            Generator,
            Iterator,
            Literal,
            Mapping,
            NewType,
            Optional,
            Protocol,
            TypeVar,
            TypedDict,
            Union,
            cast,
        )

        from typed_envs import EnvVarFactory, EnvironmentVariable

        some_var = typed_envs.create_env("SOME_VAR", int, 10)
        factory = EnvVarFactory()
        other_var = factory.create_env("OTHER_VAR", str, "hi")
        explicit: EnvironmentVariable[int] = some_var

        def takes_int(x: int) -> None:
            print(x)

        def takes_str(x: str) -> None:
            print(x)

        def takes_union(x: Union[int, str]) -> None:
            print(x)

        explicit.bit_length()
        explicit._env_name

        takes_int(some_var)
        takes_int(explicit)
        takes_str(other_var)

        class HasEnvName:
            _env_name: int

            def __init__(self, value: int) -> None:
                self._env_name = value

            def ping(self) -> int:
                return self._env_name

        class Counter:
            def __init__(self, n: int) -> None:
                self.n = n

            def __len__(self) -> int:
                return self.n

            def __iter__(self) -> Iterator[int]:
                return iter(range(self.n))

            def __getitem__(self, idx: int) -> int:
                return idx

            def __call__(self, value: int) -> int:
                return self.n + value

        class AwaitableThing:
            def __init__(self, value: int) -> None:
                self.value = value

            def __await__(self) -> Generator[Any, None, int]:
                async def _inner() -> int:
                    return self.value
                return _inner().__await__()

        conflict_env = typed_envs.create_env("CONFLICT", HasEnvName, HasEnvName(1))
        counter_env = typed_envs.create_env("COUNTER", Counter, Counter(3))
        await_env = typed_envs.create_env("AWAIT", AwaitableThing, AwaitableThing(5))
        int_env = typed_envs.create_env("NUM", int, 5)

        takes_str(conflict_env._env_name)
        takes_int(conflict_env.ping())

        takes_int(len(counter_env))
        for item in counter_env:
            takes_int(item)
        takes_int(counter_env[1])
        takes_int(counter_env(2))

        takes_int(int_env + 1)
        takes_int(1 + int_env)
        int_comparison = int_env > 1

        async def uses_await(x: AwaitableThing) -> int:
            return await x

        async def uses_env() -> int:
            return await await_env

        flag = True
        env_type: Union[type[int], type[str]] = int if flag else str
        default: Union[int, str] = 0 if flag else "ok"
        env_union = typed_envs.create_env("UNION", env_type, default)

        takes_union(env_union)
        if isinstance(env_union, int):
            env_union.bit_length()
        else:
            env_union.upper()

        opt_env = cast(
            Optional[EnvironmentVariable[int]],
            typed_envs.create_env("OPT", int, 1),
        )
        if opt_env is not None:
            opt_env.bit_length()

        UserId = NewType("UserId", int)

        class HasShout(Protocol):
            def shout(self) -> str: ...

        @dataclass
        class Greeter:
            name: str

            def shout(self) -> str:
                return self.name.upper()

        TBound = TypeVar("TBound", bound=HasShout)
        TCons = TypeVar("TCons", int, str)

        def use_bound(x: EnvironmentVariable[TBound]) -> str:
            return x.shout()

        def use_constrained(x: EnvironmentVariable[TCons]) -> None:
            if isinstance(x, int):
                x.bit_length()
            else:
                x.upper()

        annot_env: EnvironmentVariable[Annotated[int, "meta"]] = typed_envs.create_env(
            "ANN", int, 1
        )
        lit_env: EnvironmentVariable[Literal[3]] = cast(
            EnvironmentVariable[Literal[3]],
            typed_envs.create_env("LIT", int, 3),
        )

        user_type = cast(type[UserId], UserId)
        user_env = typed_envs.create_env("USER_ID", user_type, UserId(1))
        greeter_env = typed_envs.create_env("GREET", Greeter, Greeter("hello"))

        final_env: Final[EnvironmentVariable[int]] = typed_envs.create_env(
            "FINAL", int, 2
        )
        any_env: EnvironmentVariable[Any] = typed_envs.create_env("ANY", object, object())

        def takes_user(x: UserId) -> None:
            print(x)

        takes_int(annot_env)
        takes_int(lit_env + 1)
        annot_env.bit_length()
        lit_env.bit_length()
        final_env.bit_length()
        any_env.any_attr.any_other_attr

        takes_user(user_env)
        use_constrained(typed_envs.create_env("CONS_INT", int, 4))
        use_constrained(typed_envs.create_env("CONS_STR", str, "yo"))

        class Config(TypedDict):
            host: str
            port: int

        list_env: EnvironmentVariable[list[int]] = cast(
            EnvironmentVariable[list[int]],
            typed_envs.create_env("LIST", list, [1, 2]),
        )
        dict_env: EnvironmentVariable[dict[str, int]] = cast(
            EnvironmentVariable[dict[str, int]],
            typed_envs.create_env("DICT", dict, {"a": 1}),
        )
        tuple_env: EnvironmentVariable[tuple[int, str]] = cast(
            EnvironmentVariable[tuple[int, str]],
            typed_envs.create_env("TUP", tuple, (1, "a")),
        )
        td_env: EnvironmentVariable[Config] = cast(
            EnvironmentVariable[Config],
            typed_envs.create_env("CFG", dict, {"host": "localhost", "port": 8080}),
        )

        list_env.append(3)
        list_item = list_env[0]
        for item in list_env:
            print(item)

        dict_env["a"]
        dict_env.get("a", 0)

        tuple_first = tuple_env[0]
        tuple_second = tuple_env[1]

        def takes_mapping(x: Mapping[str, object]) -> None:
            print(x)

        takes_mapping(td_env)
        host_value = td_env["host"]

        class Color(Enum):
            RED = "red"
            BLUE = "blue"

        color_env = typed_envs.create_env("COLOR", Color, Color.RED)

        def takes_color(x: Color) -> None:
            print(x)

        takes_color(color_env)
        takes_str(color_env.name)
        color_value = color_env.value

        set_env: EnvironmentVariable[set[str]] = cast(
            EnvironmentVariable[set[str]],
            typed_envs.create_env("SET", set, {"a"}),
        )
        set_env.add("b")
        for set_item in set_env:
            takes_str(set_item)

        int_type: type[int] = int
        int_type_env = typed_envs.create_env("INT_TYPE", int_type, 1)
        takes_int(int_type_env)

        any_type: type[Any] = object
        any_env2 = typed_envs.create_env("ANY2", any_type, object())
        any_env2.any_attr.any_other_attr

        maybe_env: EnvironmentVariable[Optional[int]] = cast(
            EnvironmentVariable[Optional[int]],
            typed_envs.create_env("MAYBE", int, 5),
        )
        if isinstance(maybe_env, int):
            maybe_env.bit_length()
        """
    _assert_mypy_ok(tmp_path, source)
