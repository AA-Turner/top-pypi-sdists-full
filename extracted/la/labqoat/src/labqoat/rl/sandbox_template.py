"""The sandbox every episode of a rollout starts in."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from labqoat.rl.sandbox_template_error import SandboxTemplateError
from labqoat.sandbox.sandbox_client import SandboxClient
from labqoat.sandbox.sandbox_image_not_allowed_error import SandboxImageNotAllowedError
from labqoat.sandbox.sandbox_invalid_request_error import SandboxInvalidRequestError
from labqoat.sandbox.sandbox_platform import SandboxPlatform
from labqoat.sandbox.sandbox_too_large_error import SandboxTooLargeError


@dataclass(frozen=True)
class SandboxTemplate:
    """The image, limits, environment, volumes and network each episode's sandbox gets, all of them optional.

    The arguments mean what they mean to ``SandboxClient.create`` and ``Sandbox.create``. A sandbox the
    platform places names its image and mounts no volumes; one on a function's own host may name neither.
    """

    image: str | None = None
    cpu: float = 1
    memory: int = 1024
    env: Mapping[str, str] | None = None
    volumes: Mapping[str, str] | None = None
    network: bool | Sequence[str] = False

    async def start(
        self, client: SandboxClient | SandboxPlatform, sandbox_id: str, wait: float, timeout: float
    ) -> None:
        """Start a sandbox under a chosen identifier that lives ``timeout`` seconds, waiting up to ``wait`` for room.

        A host or the platform refusing the template itself (an image the host was not launched with, a volume
        the function does not mount, more than a host's whole budget) raises ``SandboxTemplateError``.
        """
        try:
            if isinstance(client, SandboxPlatform):
                await self._placed(client, sandbox_id, wait, timeout)
            else:
                await client.create_async(
                    image=self.image,
                    cpu=self.cpu,
                    memory=self.memory,
                    env=self.env,
                    sandbox_id=sandbox_id,
                    timeout=timeout,
                    volumes=self.volumes,
                    network=self.network,
                    wait=wait,
                )
        except (SandboxImageNotAllowedError, SandboxInvalidRequestError, SandboxTooLargeError) as error:
            source = self.image or "the host's image"
            raise SandboxTemplateError(f"no sandbox can start from {source}: {error}") from error

    async def _placed(self, platform: SandboxPlatform, sandbox_id: str, wait: float, timeout: float) -> None:
        """Have the platform place the episode's sandbox, which needs an image and has no volumes to mount."""
        if self.image is None or self.volumes:
            raise SandboxTemplateError("a sandbox the platform places names its image and mounts no volumes")
        await platform.create_async(
            image=self.image,
            cpu=self.cpu,
            memory=self.memory,
            env=self.env,
            network=self.network,
            timeout=timeout,
            sandbox_id=sandbox_id,
            wait=wait,
        )
