"""Side-effect-free authored image declarations."""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path

from labqoat.compute.images.base_catalog import BaseCatalog
from labqoat.compute.images.compiler import Compiler
from labqoat.compute.images.rl_stack import RlStack
from labqoat.compute.images.command_step import CommandStep
from labqoat.compute.images.dependency_command_step import DependencyCommandStep
from labqoat.compute.images.copy_step import CopyStep
from labqoat.compute.images.env_step import EnvStep
from labqoat.compute.images.image_validation import ImageValidation
from labqoat.compute.images.hugging_face_snapshot import HuggingFaceSnapshot
from labqoat.compute.images.local_path import LocalPath
from labqoat.compute.images.operation import Operation
from labqoat.compute.images.workdir_step import WorkdirStep
from labqoat.compute.images.pip_step import PipStep
from labqoat.compute.images.sync_step import SyncStep
from labqoat.compute.images.apt_step import AptStep
from labqoat.compute.images.stage_step import StageStep
from labqoat.compute.images.fragment_steps import FragmentSteps
from labqoat.compute.images.dependency_validation import DependencyValidation


@dataclass(frozen=True)
class Image:
    """Branch immutable ordered recipes without performing build or publication work."""

    base: str
    operations: tuple[Operation, ...] = ()
    python_version: str = "3.13"

    @classmethod
    def debian_slim(cls, *, python_version: str = "3.13") -> "Image":
        """Declare the catalog's pinned Python, Debian and uv base."""
        return cls(base=BaseCatalog.resolve(python_version), python_version=python_version)

    @classmethod
    def rl(cls) -> "Image":
        """Python 3.12 with vLLM, TRL, Unsloth, PyTorch and a C compiler, at versions verified on Labqoat's GPUs.

        Load a model with Unsloth's ``FastLanguageModel.from_pretrained(..., fast_inference=True)`` and train it with
        TRL's ``AsyncGRPOTrainer``: generation and training share one GPU and only the LoRA adapter moves between
        them. Add packages with ``.uv_pip_install(...)``.
        """
        return (
            cls.debian_slim(python_version="3.12")
            .apt_install(*RlStack.SYSTEM)
            .uv_pip_install(*RlStack.PACKAGES)
            # FlashInfer's sampler compiles with nvcc at engine start-up, and the image has no CUDA toolkit.
            .env({"TOKENIZERS_PARALLELISM": "false", "VLLM_USE_FLASHINFER_SAMPLER": "0"})
        )

    @classmethod
    def from_registry(cls, reference: str, *, python_version: str = "3.13") -> "Image":
        """Declare a digest-pinned OCI image whose `python` is the given 3.11, 3.12 or 3.13 minor."""
        return cls(base=ImageValidation.reference(reference), python_version=BaseCatalog.supported(python_version))

    def run_commands(self, *commands: str) -> "Image":
        """Append ordered build-time shell commands with failure propagation."""
        return self._append(CommandStep(ImageValidation.commands(commands)))

    def huggingface_model(self, repository: str, *, revision: str, allow_patterns: tuple[str, ...] = ()) -> "Image":
        """Bake a pinned public model into the image; install locked huggingface-hub dependencies first."""
        command = HuggingFaceSnapshot.command(repository, revision, allow_patterns)
        return self.env({"HF_HUB_CACHE": HuggingFaceSnapshot.cache}).run_dependency_commands(command)

    def run_dependency_commands(self, *commands: str) -> "Image":
        """Build source-independent dependencies before workspace copies; commands must not read authored source."""
        return self._append(DependencyCommandStep(ImageValidation.commands(commands)))

    def env(self, values: Mapping[str, str]) -> "Image":
        """Capture literal environment values for subsequent steps and execution."""
        if not 1 <= len(values) <= 128:
            raise ValueError("Image environment operations require 1..128 entries")
        entries = tuple(sorted(ImageValidation.environment(key, value) for key, value in values.items()))
        return self._append(EnvStep(entries))

    def workdir(self, path: str) -> "Image":
        """Set the absolute directory used by subsequent commands and execution."""
        return self._append(WorkdirStep(ImageValidation.path(path)))

    def add_local_file(self, path: Path | str, remote_path: str) -> "Image":
        """Declare a caller-relative file copied into the immutable image."""
        return self._append(CopyStep(LocalPath.capture(path), ImageValidation.path(remote_path), False))

    def add_local_dir(self, path: Path | str, remote_path: str, *, ignore: tuple[str, ...] = ()) -> "Image":
        """Declare a caller-relative directory with ordered inline ignore patterns."""
        patterns = tuple(ImageValidation.text(pattern) for pattern in ignore)
        return self._append(CopyStep(LocalPath.capture(path), ImageValidation.path(remote_path), True, patterns))

    def _compiled(self, names: tuple[str, ...]) -> "Image":
        """Add Debian's C compiler before installing torch, whose `torch.compile` builds kernels at run time."""
        if self.base not in BaseCatalog.bases.values() or not Compiler.required(names):
            return self
        return self if Compiler.present(self.operations) else self.apt_install(*Compiler.PACKAGES)

    def _append(self, operation: Operation) -> "Image":
        """Bound recipes while preserving previously declared image branches."""
        if not self.base or len(self.operations) >= 128:
            raise ValueError("Image recipes require a registry base and at most 128 operations")
        return replace(self, operations=(*self.operations, operation))

    def uv_pip_install(
        self, *packages: str, requirements: Path | str | None = None, index_url: str | None = None
    ) -> "Image":
        """Install exact package requirements or one captured hash-locked requirements file."""
        if bool(packages) == (requirements is not None):
            raise ValueError("Choose exact packages or a hash-locked requirements file")
        pins = DependencyValidation.python(packages) if packages else ()
        path = None if requirements is None else LocalPath.capture(requirements)
        names = tuple(Compiler.name(pin) for pin in pins) if path is None else Compiler.listed(path)
        return self._compiled(names)._append(PipStep(pins, path, DependencyValidation.index(index_url)))

    def uv_sync(
        self,
        project_dir: Path | str,
        *,
        package: str | None = None,
        groups: tuple[str, ...] = (),
        extras: tuple[str, ...] = (),
    ) -> "Image":
        """Install frozen uv dependencies and capture selected workspace sources separately."""
        if package is not None:
            DependencyValidation.names((package,))
        project = LocalPath.capture(project_dir)
        step = SyncStep(project, package, DependencyValidation.names(groups), DependencyValidation.names(extras))
        return self._compiled(Compiler.locked(project))._append(step)

    def apt_install(self, *packages: str) -> "Image":
        """Install exact system package versions from the pinned Debian repository snapshot."""
        return self._append(AptStep(DependencyValidation.apt(packages)))

    def dockerfile_commands(self, *commands: str) -> "Image":
        """Append validated single-stage RUN, ENV or WORKDIR instruction fragments."""
        image = self
        for command in ImageValidation.commands(commands):
            image = image._append(FragmentSteps.parse(command))
        return image

    def copy_from(self, image: "Image", source: str, destination: str) -> "Image":
        """Copy a native output from an explicitly retained immutable dependency stage."""
        return self._append(StageStep(image, ImageValidation.path(source), ImageValidation.path(destination)))
