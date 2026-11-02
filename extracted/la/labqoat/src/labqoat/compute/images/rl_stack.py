"""The reinforcement-learning packages ``Image.rl`` installs, verified together on Labqoat's GPUs."""

from typing import ClassVar

from labqoat.compute.images.compiler import Compiler


class RlStack:
    """Pins that resolve together and ran asynchronous GRPO on an L40S under the platform's runtime (2026-10-15).

    vLLM fixes torch; Unsloth caps transformers and datasets; TRL's async trainer needs 1.14 or newer. Move them
    together, and only after a run on a GPU.
    """

    SYSTEM: ClassVar[tuple[str, ...]] = Compiler.PACKAGES
    PACKAGES: ClassVar[tuple[str, ...]] = (
        "vllm==0.32.0",
        "torch==2.13.0",
        "trl==1.15.0",
        "unsloth==2026.10.8",
        "unsloth-zoo==2026.10.8",
        "transformers==5.17.0",
        "peft==0.21.2",
        "datasets==4.8.5",
    )
