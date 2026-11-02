"""
`seq.Image` — a declarative, immutable image spec (NOT a built image).

WHY every builder method returns a NEW `Image` and nothing is built here: the SDK never builds images; it
accrues a spec that `seq deploy` hands to the gateway, which builds it on the platform. The chain is lazy, so a
new config only adds a field, never a code path.




Two origins, mutually exclusive: a registry base (`from_registry`/`debian_slim`) OR an inline Dockerfile
(`from_dockerfile`). Either is extended by the ordered step chain `uv_pip_install` / `apt_install` / `env`
/ `run_commands`, each a distinct wire `ImageStep` variant. `run_commands` and `from_dockerfile` — which
S1 omitted because the contract had no home for them — are represented natively now the contract carries
`ImageStepRun` and `ImageSpec.dockerfile`.

Nothing here touches the network, a container runtime, or a subprocess: constructing and chaining an
`Image` is a pure in-memory data operation. `from_dockerfile` reads a local file — the source
the user points at — which is the one disk read, never a build.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from sequence_base.contract import (
    AddLocal,
    ImageSpec,
    ImageStep,
    ImageStepAddLocal,
    ImageStepApt,
    ImageStepEnv,
    ImageStepProject,
    ImageStepRun,
    ImageStepTemplateFiles,
    ImageStepUvPip,
    Project,
    SecretRef,
    TemplateFiles,
)
from pydantic import ValidationError

from seq.errors import PolicyDefinitionError




_DEBIAN_SLIM_BASE = "debian:12-slim"



_MAX_DOCKERFILE_BYTES = 1 << 20



PYTHONS = ("3.11", "3.12", "3.13")



_RESERVED_ENV = frozenset({"PYTHONPATH", "PORT"})
_RESERVED_ENV_PREFIX = "SEQ_"





_PLATFORM_ENV = ("SEQ_MANIFEST", "SEQ_EVAL_JOB", "SEQ_BENCH_REF")


def _caller_file(up: int) -> str | None:
    """The __file__ `up` frames above the function that calls this (up=1 is that function's own caller) - the file
    whose code declared a local path. The +1 skips this helper's own frame."""
    try:
        return sys._getframe(up + 1).f_globals.get("__file__")
    except ValueError:
        return None


def _local(local_path, caller: str | None) -> Path:
    """A local path a declaration gave, resolved relative to the file that declared it (`caller`, its __file__), else
    the working directory. The one rule for every local path in seq.Image - from_dockerfile's path and context,
    add_local_file / add_local_dir - so `seq deploy <folder>` finds them from any directory. When the working
    directory is the file's own directory, the result is what it was before this rule."""
    p = Path(local_path)
    if not p.is_absolute():
        p = (Path(caller).resolve().parent if caller else Path.cwd()) / p
    return p.resolve()


def _on_platform() -> bool:
    return any(os.environ.get(name) for name in _PLATFORM_ENV)


def _ships_python(base: str) -> bool:
    """An official `python:*` image: its interpreter sits where an added Python would go."""
    ref = base.split("@", 1)[0]
    last = ref.rsplit("/", 1)[-1]
    repo = ref[: len(ref) - len(last)] + last.split(":", 1)[0]
    return repo in ("python", "library/python", "docker.io/library/python", "index.docker.io/library/python")


def _check_python(python: str | None, base: str | None = None) -> str | None:
    if python is None:
        return None
    if python != "image" and python not in PYTHONS:
        raise PolicyDefinitionError(f"python={python!r}: the worker runs on Python {', '.join(PYTHONS)}, or "
                                    "python='image' to use the one the base image has")
    if base is not None and python != "image" and _ships_python(base):
        raise PolicyDefinitionError(f"{base} already has its own Python; pass python='image' to use it, or start "
                                    "from a base without one")
    return python


class Image:
    """An immutable image declaration: a base (registry ref OR Dockerfile source) plus an ordered list of
    steps. Construct via a class method, chain builder methods (each returns a new `Image`), and let
    `@seq.policy` lower it. A bare `Image()` has no origin — chaining on it is rejected."""

    __slots__ = ("_base", "_dockerfile", "_steps", "_python", "_context", "_locals", "_pysources",
                 "_clear_entrypoint")

    def __init__(
        self,
        base: str | None = None,
        *,
        dockerfile: str | None = None,
        steps: tuple[ImageStep, ...] = (),
        python: str | None = None,
        context: str | None = None,
        locals_: tuple[tuple[str, str], ...] = (),
        pysources: tuple[str, ...] = (),
        clear_entrypoint: bool | None = None,
    ) -> None:
        self._base = base
        self._dockerfile = dockerfile
        self._python = python


        self._clear_entrypoint = clear_entrypoint

        self._context = context


        self._steps = tuple(steps)



        self._locals = tuple(locals_)
        self._pysources = tuple(pysources)


    @classmethod
    def from_registry(cls, ref: str, *, python: str | None = None,
                      clear_entrypoint: bool = False) -> "Image":
        """Start from an explicit registry image (e.g. the CUDA base a GPU policy needs). `ref` is carried
        into the base verbatim, character-for-character; an empty or malformed ref is rejected here.
        `python="3.12"` adds that Python (default 3.11); `python="image"` uses the one the image has.

        `clear_entrypoint=True` drops the base's ENTRYPOINT so the platform's start command runs directly — for a base
        whose entry point would wrap it (e.g. NVIDIA's Isaac Lab runheadless.sh). Off by default, because some images
        set their ENTRYPOINT to prepare the environment and clearing it would break them."""
        if not isinstance(ref, str):
            raise PolicyDefinitionError(
                f"Image.from_registry(ref) needs a string tag, got {type(ref).__name__}"
            )
        if not ref or not ref.strip():
            raise PolicyDefinitionError("Image.from_registry(ref) got an empty registry reference")
        if any(c.isspace() for c in ref):
            raise PolicyDefinitionError(
                f"Image.from_registry({ref!r}) contains whitespace; a registry ref is a single token "
                "like 'nvidia/cuda:12.4.1-runtime-ubuntu22.04'"
            )

        return cls(base=ref, python=_check_python(python, ref),
                   clear_entrypoint=clear_entrypoint or None)

    @classmethod
    def debian_slim(cls, *, python: str | None = None) -> "Image":
        """Start from a small Debian base — the default when a policy declares no image. Resolves to a
        concrete, pullable tag, never the literal token `debian_slim`. `python=` as from_registry."""
        return cls(base=_DEBIAN_SLIM_BASE, python=_check_python(python))

    @classmethod
    def from_project(cls, *, exclude: list[str] | tuple[str, ...] = (), extra: list[str] | tuple[str, ...] = (),
                     python: str | None = None, requirements: str | None = None) -> "Image":
        """Start from the project's own dependency files, which the platform installs for Linux and the worker's
        machine: those `seq deploy` finds from the entry file's folder up to the folder it uploads (a lock - uv.lock,
        poetry.lock, a pinned requirements file - else pyproject.toml's dependencies, requirements.txt or setup.py,
        or a requirements-<name>.txt where a folder has nothing else), with the local packages the code imports and
        the versions this machine has. The chain then goes on as any other (.apt_install(), .run_commands(), ...),
        after them.

        `exclude` leaves packages out by name; `extra` adds requirements after the project's own ("name==1.2", or a
        wheel's URL as "name @ https://..."); a pyproject.toml's [tool.seq] exclude / extra add to both. `python` as
        debian_slim; by default the project's .python-version, else the Python this machine runs. `requirements`
        names the requirements file to install from, by its name in those folders - one of several
        requirements-<name>.txt, which `seq deploy` refuses to pick from: requirements="requirements-05i.txt"; read
        as a requirements.txt is (a .lock as the lock), in the nearest folder that holds it.

        A policy that declares neither image= nor deps= gets this image by default when its project has dependency
        files; `seq deploy --dry-run` prints what it read."""
        for arg, value, example in (("exclude", exclude, '["deepspeed"]'),
                                    ("extra", extra, '["causal-conv1d @ https://.../causal_conv1d-1.4.0-....whl"]')):
            if isinstance(value, str) or not isinstance(value, (list, tuple)) or \
                    not all(isinstance(v, str) for v in value):
                raise PolicyDefinitionError(f"Image.from_project({arg}=...) takes a list of strings, e.g. "
                                            f"{arg}={example}")
        if requirements is not None and (not isinstance(requirements, str) or "/" in requirements
                                         or "\\" in requirements or not requirements.endswith((".txt", ".lock"))):
            raise PolicyDefinitionError(
                'Image.from_project(requirements=...) takes a requirements file\'s name, e.g. '
                'requirements="requirements-05i.txt": seq deploy reads it in the folders it reads the project\'s '
                "files from, the entry file's up to the folder it uploads")
        try:

            project = Project(exclude=list(exclude), extra=list(extra), declared=[requirements] if requirements else [])
        except ValidationError as exc:
            raise PolicyDefinitionError(f"Image.from_project: {exc.errors()[0]['msg']}") from None
        return cls(base=_DEBIAN_SLIM_BASE, python=_check_python(python),
                   steps=(ImageStepProject(project=project),))

    @classmethod
    def from_dockerfile(cls, path: str | Path, *, context: str | Path | None = None,
                        python: str | None = None,
                        clear_entrypoint: bool = False) -> "Image":
        """Start from an inline Dockerfile whose SOURCE is read from `path` now and carried into the image
        spec as its own component (never smuggled into the registry `base`), so the gateway builds from it.
        A missing or unreadable path is rejected at declaration time with a clear error.

        `context` is the directory its COPY / ADD read: it ships with the deploy (within the code bundle's size
        limit). `python="3.12"` adds that Python to the Dockerfile's image; by default it brings its own.
        `clear_entrypoint` is as from_registry — for a base whose ENTRYPOINT would wrap the platform's command
        (e.g. NVIDIA's Isaac Lab); off by default.
        """




        caller = _caller_file(1)
        p = _local(path, caller)
        if _on_platform() and not p.is_file():


            return cls(dockerfile="# built by the platform at deploy\n",
                       python=python if python in (*PYTHONS, "image") else None,
                       clear_entrypoint=clear_entrypoint or None)
        ctx = None
        if context is not None:
            c = _local(context, caller)
            if not c.is_dir():
                raise PolicyDefinitionError(
                    f"Image.from_dockerfile(context={str(context)!r}): not a directory (the context is the "
                    "directory the Dockerfile's COPY / ADD read)")
            ctx = str(c)
        try:
            if not p.is_file():
                raise PolicyDefinitionError(
                    f"Image.from_dockerfile({str(path)!r}): no such file (a Dockerfile path must point "
                    "at a readable file)"
                )
            size = p.stat().st_size
            if size > _MAX_DOCKERFILE_BYTES:
                raise PolicyDefinitionError(
                    f"Image.from_dockerfile({str(path)!r}): file is {size} bytes, over the "
                    f"{_MAX_DOCKERFILE_BYTES}-byte cap for an inline Dockerfile"
                )
            source = p.read_text(encoding="utf-8")
        except PolicyDefinitionError:
            raise
        except OSError as exc:
            raise PolicyDefinitionError(
                f"Image.from_dockerfile({str(path)!r}) could not be read: {exc}"
            ) from exc
        if not source.strip():
            raise PolicyDefinitionError(
                f"Image.from_dockerfile({str(path)!r}) is empty; a Dockerfile needs at least a FROM line"
            )
        return cls(dockerfile=source, python=_check_python(python), context=ctx,
                   clear_entrypoint=clear_entrypoint or None)


    def _extend(self, step: ImageStep) -> "Image":
        """Append one step, returning a new Image; the receiver is never mutated. A
        chaining call before any origin is set (`Image().uv_pip_install(...)`) is rejected — the SDK never
        silently produces a base-less spec."""
        if self._base is None and self._dockerfile is None:
            raise PolicyDefinitionError(
                "Image has no base; start a chain with Image.debian_slim(), Image.from_registry(...), "
                "or Image.from_dockerfile(...) before adding steps"
            )
        return Image(self._base, dockerfile=self._dockerfile, steps=self._steps + (step,), python=self._python,
                     context=self._context, locals_=self._locals, pysources=self._pysources,
                     clear_entrypoint=self._clear_entrypoint)

    def uv_pip_install(self, *packages: str) -> "Image":
        """Add a `uv pip install` step. `*packages` is the ordered install list (order is preserved). Each
        call is its own step — adjacent calls are never coalesced."""
        return self._extend(ImageStepUvPip(uv_pip_install=list(packages)))

    def apt_install(self, *packages: str) -> "Image":
        """Add an `apt-get install` step for system packages. Its own step, never coalesced."""
        return self._extend(ImageStepApt(apt_install=list(packages)))

    def run_commands(self, *commands: str, secrets: list | None = None) -> "Image":
        """Add a `run_commands` step — arbitrary build commands, run in order, preserved verbatim, and
        positioned exactly where called relative to the other steps; never silently dropped.

        `secrets=[seq.Secret.from_name("gh")]` gives these commands alone the secret's variables while they run
        (a private git repo or package index); no other step, no image layer and no worker ever holds them.
        """
        from seq.secret import Secret

        refs: list[SecretRef] = []
        for sec in secrets or []:
            if isinstance(sec, Secret):
                refs.append(sec._ref())
            elif isinstance(sec, SecretRef):
                refs.append(sec)
            else:
                raise PolicyDefinitionError(
                    f"run_commands(secrets=) entries must be seq.Secret.from_name(...), got {type(sec).__name__}")
        return self._extend(ImageStepRun(run_commands=list(commands), secrets=refs or None))

    def template_files(self, template: str, version: int) -> "Image":
        """Let each run_commands step after this one read an official template version's frozen build files, at
        /seq/frozen, while the image builds: the sources at their pinned commits, every Python and system package its
        image installs, the assets it downloads, which the platform keeps - so the image builds the same whether or not
        the sites they came from still serve them. Nothing of them stays in the image unless a step copies or installs
        it. One template version an image; `seq init` writes this step into the templates that have frozen files.

            seq.Image.from_registry("debian:12-slim@sha256:...")
                .template_files("toy-benchmark", version=4)
                .run_commands("pip install --no-index --find-links /seq/frozen/wheels -r /seq/frozen/requirements.lock")

        """
        if any(isinstance(s, ImageStepTemplateFiles) for s in self._steps):
            raise PolicyDefinitionError("template_files: an image takes the files of one template version")
        try:
            files = TemplateFiles(template=template, version=version)
        except ValidationError:
            raise PolicyDefinitionError(f"template_files({template!r}, version={version!r}): name a template as `seq "
                                        "init` takes it (e.g. 'pi05-droid') and a version from 1") from None
        return self._extend(ImageStepTemplateFiles(template_files=files))







    def _add_local(self, local_path: str | os.PathLike, remote_path: str, *, want_dir: bool, depth: int) -> "Image":
        path = _local(local_path, _caller_file(depth))




        if not isinstance(remote_path, str) or not remote_path.startswith("/"):
            raise PolicyDefinitionError(f"add_local_{'dir' if want_dir else 'file'}: remote_path {remote_path!r} must "
                                        "be an absolute path in the image")
        src = f"_seq_local/{len(self._locals)}/{path.name}"
        step = ImageStepAddLocal(add_local=AddLocal(src=src, dst=remote_path))
        new = self._extend(step)
        new._locals = self._locals + ((src, str(path)),)
        return new

    def add_local_file(self, local_path: str | os.PathLike, remote_path: str) -> "Image":
        """Ship one local file with the deploy and place it at `remote_path` in the image (e.g. a config the policy
        reads at load)."""
        return self._add_local(local_path, remote_path, want_dir=False, depth=2)

    def add_local_dir(self, local_path: str | os.PathLike, remote_path: str) -> "Image":
        """Ship one local directory with the deploy and place it at `remote_path` in the image."""
        return self._add_local(local_path, remote_path, want_dir=True, depth=2)

    def add_local_python_source(self, *modules: str) -> "Image":
        """Ship Python modules or packages from outside the folder at the top of its upload, importable by name on the
        worker (a helper module the policy imports from elsewhere on this machine). Each is found where `import` would
        find it here and is never run here, so what it imports needs to be in the image alone; a dotted name ships the
        whole package it is in."""
        for name in modules:
            if not isinstance(name, str) or not all(part.isidentifier() for part in name.split(".")):
                raise PolicyDefinitionError(f"add_local_python_source: {name!r} is not a module name")
        if self._base is None and self._dockerfile is None:
            raise PolicyDefinitionError("Image has no base; start a chain before add_local_python_source(...)")
        return Image(self._base, dockerfile=self._dockerfile, steps=self._steps, python=self._python,
                     context=self._context, locals_=self._locals, pysources=self._pysources + tuple(modules),
                     clear_entrypoint=self._clear_entrypoint)

    def env(self, variables: dict[str, str]) -> "Image":
        """Add an environment-variable step (build-time env baked into the image). Each `env()` call is its
        own ordered step (calls are not merged into one dict), so a key set again later wins under build
        order by both steps being preserved.

        Keys are sorted within the step for a canonical, byte-stable serialization regardless of the
        caller's dict order. `env` carries ORDINARY build-time variables only — a `seq.Secret`
        (or any non-string value) is rejected so the image spec cannot become a credential side-channel
        : secret values travel only through `secrets=[seq.Secret.from_name(...)]`.
        """

        from seq.secret import Secret

        if not isinstance(variables, dict):
            raise PolicyDefinitionError(
                f"Image.env(variables) needs a dict[str, str], got {type(variables).__name__}"
            )
        clean: dict[str, str] = {}
        for key in sorted(variables):
            value = variables[key]
            if not isinstance(key, str):
                raise PolicyDefinitionError(f"env key must be a str, got {type(key).__name__}")
            if key in _RESERVED_ENV or key.startswith(_RESERVED_ENV_PREFIX):
                raise PolicyDefinitionError(
                    f"env[{key!r}] is set by the platform on every worker (PYTHONPATH, PORT and SEQ_* are "
                    "reserved); choose another name")
            if isinstance(value, Secret):
                raise PolicyDefinitionError(
                    f"env[{key!r}] is a seq.Secret; a secret value must not travel through the image "
                    "env (it would be baked into the build). Declare it in secrets=[seq.Secret.from_name"
                    "(...)] instead — the value is injected into the policy subprocess at bootstrap."
                )
            if not isinstance(value, str):
                raise PolicyDefinitionError(
                    f"env[{key!r}] must be a str (a build-time environment value), got "
                    f"{type(value).__name__}"
                )
            clean[key] = value
        return self._extend(ImageStepEnv(env=clean))


    @property
    def context(self) -> str | None:
        """The Dockerfile's build context directory, when one was given."""
        return self._context

    @property
    def steps(self) -> tuple[ImageStep, ...]:
        """The ordered step chain (read-only view). Exposed so a caller / verifier can inspect fork
        isolation and step order without reaching into a private attribute."""
        return self._steps

    @property
    def local_files(self) -> tuple[tuple[str, str], ...]:
        """(path in the code bundle, absolute local path) of each declared local file or directory."""
        return self._locals

    @property
    def python_sources(self) -> tuple[str, ...]:
        """Local Python modules declared with add_local_python_source."""
        return self._pysources

    def _spec(self) -> ImageSpec:
        """Lower to the wire `ImageSpec`; `steps` order is the chain order, exactly as written. A registry
        base lowers to `base=`; a Dockerfile lowers to `dockerfile=` (its own component). An origin-less
        Image is rejected — the SDK never produces a base-less spec."""
        if self._dockerfile is not None:
            return ImageSpec(dockerfile=self._dockerfile, steps=list(self._steps), python=self._python,
                             clear_entrypoint=self._clear_entrypoint)
        if self._base is not None:
            return ImageSpec(base=self._base, steps=list(self._steps), python=self._python,
                             clear_entrypoint=self._clear_entrypoint)
        raise PolicyDefinitionError(
            "Image has no base; declare one with Image.debian_slim(), Image.from_registry(...), or "
            "Image.from_dockerfile(...)"
        )

    def __repr__(self) -> str:
        origin = f"dockerfile:{len(self._dockerfile)}B" if self._dockerfile is not None else repr(self._base)
        return f"Image(base={origin}, steps={len(self._steps)})"
