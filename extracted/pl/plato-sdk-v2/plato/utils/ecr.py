"""ECR image management utilities."""

from __future__ import annotations

import asyncio
import logging
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

# Keys that litellm (sagemaker handler) injects into os.environ at import time,
# which poison AWS CLI calls.  We strip them so the CLI falls back to
# ~/.aws/credentials or instance profile.
_AWS_ENV_KEYS = ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN")


def _clean_aws_env() -> dict[str, str]:
    """Return a copy of os.environ without injected AWS credential vars.

    In CI (GitHub Actions), credentials come from OIDC via environment variables
    and must be preserved.  Only strip them locally where litellm may pollute
    the environment.
    """
    env = os.environ.copy()
    if not env.get("GITHUB_ACTIONS"):
        for key in _AWS_ENV_KEYS:
            env.pop(key, None)
    return env


# ECR constants
ECR_REGISTRY = "383806609161.dkr.ecr.us-west-1.amazonaws.com"
ECR_REGION = "us-west-1"


def _retag_via_chronos(chronos_url: str, endpoint: str, source_tag: str, target_tag: str, api_key: str) -> bool:
    """POST a retag request to a Chronos retag endpoint. Returns True on success.

    Chronos copies the image manifest using its own ECS task credentials, so the
    caller does not need local AWS credentials.
    """
    chronos_url = chronos_url.rstrip("/")
    try:
        response = httpx.post(
            f"{chronos_url}{endpoint}",
            json={"source_tag": source_tag, "target_tag": target_tag},
            headers={"X-API-Key": api_key},
            timeout=60.0,
        )
    except httpx.HTTPError as e:
        logger.debug("Chronos retag request failed: %s", e)
        return False
    if response.status_code != 200:
        logger.debug("Chronos retag returned HTTP %s: %s", response.status_code, response.text)
        return False
    return True


def retag_image_via_chronos(
    chronos_url: str, package_name: str, source_tag: str, target_tag: str, api_key: str
) -> bool:
    """Retag a world image in ECR through the Chronos API.

    Server-side equivalent of retag_image(): the caller does not need local AWS
    credentials. Returns True on success.
    """
    return _retag_via_chronos(chronos_url, f"/api/worlds/{package_name}/retag-image", source_tag, target_tag, api_key)


def retag_agent_image_via_chronos(
    chronos_url: str, package_name: str, source_tag: str, target_tag: str, api_key: str
) -> bool:
    """Retag an agent image in ECR through the Chronos API.

    Server-side equivalent of retag_image(): the caller does not need local AWS
    credentials. Returns True on success.
    """
    return _retag_via_chronos(chronos_url, f"/api/agents/{package_name}/retag-image", source_tag, target_tag, api_key)


@dataclass
class ECRImage:
    """Parsed ECR image URL."""

    registry: str
    repository: str
    tag: str
    region: str

    @classmethod
    def from_url(cls, url: str) -> ECRImage:
        """Parse an ECR image URL."""
        match = re.match(r"^([^/]+)/(.+):(.+)$", url)
        if not match:
            raise ValueError(f"Invalid ECR URL format: {url}")

        registry = match.group(1)
        repository = match.group(2)
        tag = match.group(3)

        region_match = re.search(r"\.ecr\.([^.]+)\.", registry)
        if not region_match:
            raise ValueError(f"Could not extract region from ECR URL: {url}")

        return cls(registry=registry, repository=repository, tag=tag, region=region_match.group(1))

    @property
    def full_url(self) -> str:
        return f"{self.registry}/{self.repository}:{self.tag}"

    @property
    def short_name(self) -> str:
        repo_name = self.repository.split("/")[-1]
        return f"{repo_name}:{self.tag}"


def ecr_login() -> bool:
    """Login to ECR. Returns True on success."""
    login_cmd = subprocess.run(
        ["aws", "ecr", "get-login-password", "--region", ECR_REGION],
        capture_output=True,
        text=True,
        env=_clean_aws_env(),
    )
    if login_cmd.returncode != 0:
        logger.error(f"ECR login failed: {login_cmd.stderr}")
        return False

    docker_login = subprocess.run(
        ["docker", "login", "--username", "AWS", "--password-stdin", ECR_REGISTRY],
        input=login_cmd.stdout,
        capture_output=True,
        text=True,
    )
    if docker_login.returncode != 0:
        logger.error(f"Docker login failed: {docker_login.stderr}")
        return False

    return True


def ensure_repository(repository: str) -> bool:
    """Ensure ECR repository exists, create if not."""
    clean_env = _clean_aws_env()
    result = subprocess.run(
        [
            "aws",
            "ecr",
            "describe-repositories",
            "--repository-names",
            repository,
            "--region",
            ECR_REGION,
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        env=clean_env,
    )
    if result.returncode == 0:
        return True

    logger.info(f"Creating ECR repository: {repository}")
    result = subprocess.run(
        [
            "aws",
            "ecr",
            "create-repository",
            "--repository-name",
            repository,
            "--region",
            ECR_REGION,
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        env=clean_env,
    )
    if result.returncode != 0:
        # If another process created the repository first, treat it as success.
        if "RepositoryAlreadyExistsException" in (result.stderr or ""):
            return True
        logger.error(f"Failed to create repository: {result.stderr}")
        return False

    return True


BUILDX_BUILDER_NAME = "plato-builder"


def _builder_base_marker(builder_name: str = BUILDX_BUILDER_NAME) -> Path:
    """File recording the base-image digest this builder last built against."""
    cache_root = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
    return cache_root / "plato" / f"{builder_name}.base-digest"


def _dockerfile_base_ref(build_path: str) -> str | None:
    """Return the image reference of the first ``FROM`` in build_path/Dockerfile.

    This is the base image whose staleness can poison a long-lived builder.
    Returns None if there's no Dockerfile or the FROM can't be parsed.
    """
    dockerfile = Path(build_path) / "Dockerfile"
    if not dockerfile.exists():
        return None
    for raw in dockerfile.read_text().splitlines():
        line = raw.strip()
        if not line.upper().startswith("FROM "):
            continue
        # FROM [--platform=...] <image>[:tag|@digest] [AS <stage>]
        tokens = [t for t in line.split()[1:] if not t.startswith("--")]
        if tokens:
            return tokens[0]
    return None


def _resolve_registry_digest(image_ref: str) -> str | None:
    """Resolve image_ref to its current registry manifest digest.

    Used to detect when the base image moved so we can refresh the builder
    instead of reusing a stale cached base snapshot. Returns None on any error
    (e.g. a non-registry stage ref), in which case callers fall back to ``--pull``.
    """
    result = subprocess.run(
        ["docker", "buildx", "imagetools", "inspect", image_ref, "--format", "{{.Manifest.Digest}}"],
        capture_output=True,
        text=True,
        env=_clean_aws_env(),
    )
    if result.returncode != 0:
        return None
    digest = result.stdout.strip()
    return digest or None


def _ensure_buildx_builder(base_digest: str | None = None) -> str:
    """Ensure a docker-container buildx builder exists. Returns its name.

    When ``base_digest`` is provided and differs from the digest this builder
    last built against, the builder is recreated. A long-lived docker-container
    builder caches *unpacked* base layers, and ``--pull`` re-resolves the base
    manifest but still reuses that cached snapshot — so a moved base (e.g. a
    rebuilt ``plato-agent-base:latest``) would otherwise keep shipping the old
    base into images. Recreating only on a base-digest change keeps the build
    cache for the common case where the base is unchanged.
    """
    builder_name = BUILDX_BUILDER_NAME
    exists = (
        subprocess.run(
            ["docker", "buildx", "inspect", builder_name],
            capture_output=True,
            text=True,
        ).returncode
        == 0
    )

    marker = _builder_base_marker(builder_name)
    if exists and base_digest is not None:
        previous = marker.read_text().strip() if marker.exists() else None
        if previous != base_digest:
            logger.info(
                "Base image digest changed (%s -> %s); recreating buildx builder "
                "'%s' to avoid reusing a stale base snapshot",
                previous or "<none>",
                base_digest,
                builder_name,
            )
            subprocess.run(
                ["docker", "buildx", "rm", builder_name],
                capture_output=True,
                text=True,
            )
            exists = False

    if not exists:
        subprocess.run(
            ["docker", "buildx", "create", "--name", builder_name, "--driver", "docker-container"],
            capture_output=True,
            text=True,
        )

    if base_digest is not None:
        try:
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text(base_digest)
        except OSError as e:
            logger.warning("Could not persist builder base-digest marker: %s", e)

    return builder_name


def build_and_push(
    local_image: str,
    ecr_image: str,
    build_path: str,
    repository: str,
    no_cache: bool = False,
) -> bool:
    """Build Docker image and push to ECR."""
    # Ensure repo exists and login before build (buildx --push needs auth)
    if not ensure_repository(repository):
        return False
    if not ecr_login():
        return False

    cache_image = f"{ECR_REGISTRY}/{repository}:cache"
    builder = _ensure_buildx_builder()
    build_cmd = [
        "docker",
        "buildx",
        "build",
        "--builder",
        builder,
        "--provenance=false",
        "-t",
        ecr_image,
        "--build-arg",
        "SOURCE_DATE_EPOCH=0",
        "--push",
    ]
    if no_cache:
        build_cmd.append("--no-cache")
    else:
        build_cmd.extend(["--cache-from", f"type=registry,ref={cache_image}"])
        build_cmd.extend(["--cache-to", f"type=registry,ref={cache_image},mode=max"])
    build_cmd.append(".")
    result = subprocess.run(build_cmd, cwd=build_path)
    return result.returncode == 0


def get_image_digest(repository: str, tag: str) -> str | None:
    """Get the digest of an image tag in ECR. Returns None if not found."""
    import json

    result = subprocess.run(
        [
            "aws",
            "ecr",
            "describe-images",
            "--repository-name",
            repository,
            "--image-ids",
            f"imageTag={tag}",
            "--region",
            ECR_REGION,
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        env=_clean_aws_env(),
    )
    if result.returncode != 0:
        return None

    try:
        data = json.loads(result.stdout)
        images = data.get("imageDetails", [])
        if images:
            return images[0].get("imageDigest")
    except Exception:
        pass
    return None


def retag_image(repository: str, source_tag: str, target_tag: str) -> bool:
    """Retag an existing ECR image without rebuilding.

    Copies the image manifest from source_tag to target_tag in the same repository.
    Returns True on success.
    """
    import json

    # Get the manifest for the source tag
    result = subprocess.run(
        [
            "aws",
            "ecr",
            "batch-get-image",
            "--repository-name",
            repository,
            "--image-ids",
            f"imageTag={source_tag}",
            "--region",
            ECR_REGION,
            "--output",
            "json",
            "--query",
            "images[].imageManifest",
        ],
        capture_output=True,
        text=True,
        env=_clean_aws_env(),
    )
    if result.returncode != 0:
        return False

    try:
        manifests = json.loads(result.stdout)
        if not manifests:
            return False
        manifest = manifests[0]
    except (json.JSONDecodeError, IndexError):
        return False

    # Put the manifest with the new tag
    result = subprocess.run(
        [
            "aws",
            "ecr",
            "put-image",
            "--repository-name",
            repository,
            "--image-tag",
            target_tag,
            "--image-manifest",
            manifest,
            "--region",
            ECR_REGION,
        ],
        capture_output=True,
        text=True,
        env=_clean_aws_env(),
    )
    # ImageAlreadyExistsException is fine — means the tag already points to the same digest
    return result.returncode == 0 or "ImageAlreadyExistsException" in result.stderr


@dataclass
class DockerPublishResult:
    """Result of a Docker publish operation."""

    success: bool
    ecr_image: str
    latest_image: str
    error: str | None = None


def publish_docker_image(
    name: str,
    version: str,
    build_path: str,
    repo_prefix: str,
    target: str | None = None,
    build_args: dict[str, str] | None = None,
    disable_provenance: bool = True,
    no_cache: bool = False,
) -> DockerPublishResult:
    """Build and publish a Docker image to ECR.

    Args:
        name: Short name for the image (e.g., 'my-agent')
        version: Version tag (e.g., '1.0.0')
        build_path: Path to directory containing Dockerfile
        repo_prefix: ECR repository prefix (e.g., 'vm/rootfs/plato-agents')
        target: Optional Docker build target (e.g., 'prod')
        build_args: Optional build arguments
        disable_provenance: Disable BuildKit provenance attestations by default
            so unchanged image content yields stable digests.

    Returns:
        DockerPublishResult with success status and image URIs
    """
    repository = f"{repo_prefix}/{name}"
    ecr_image = f"{ECR_REGISTRY}/{repository}:{version}"
    latest_image = f"{ECR_REGISTRY}/{repository}:latest"
    cache_image = f"{ECR_REGISTRY}/{repository}:cache"

    # Ensure repo exists and login before build (buildx --push needs auth)
    if not ensure_repository(repository):
        return DockerPublishResult(
            success=False, ecr_image=ecr_image, latest_image=latest_image, error="Failed to create ECR repository"
        )
    if not ecr_login():
        return DockerPublishResult(
            success=False, ecr_image=ecr_image, latest_image=latest_image, error="ECR login failed"
        )

    # Use buildx with docker-container driver for registry cache support.
    # Registry cache stores cache metadata in a separate :cache tag so the
    # actual image digest stays stable when layers don't change.
    #
    # Resolve the Dockerfile's base image to its current registry digest and
    # pass it to the builder, which recreates itself if the base moved — this
    # prevents a long-lived builder from reusing a stale unpacked base snapshot
    # (which `--pull` does not bust). Falls back to plain `--pull` if the base
    # can't be resolved (e.g. a local-only or multi-stage ref).
    base_ref = _dockerfile_base_ref(build_path)
    base_digest = _resolve_registry_digest(base_ref) if base_ref else None
    builder = _ensure_buildx_builder(base_digest)
    docker_cmd = [
        "docker",
        "buildx",
        "build",
        "--builder",
        builder,
        # Always re-resolve `FROM ...:latest` base images against the registry.
        # Without this, buildx reuses whatever base image is cached locally / in
        # the builder, so a stale `plato-agent-base:latest` (e.g. an old build
        # that left /root owned by a non-root uid, which breaks sshd into the
        # VM) silently ships into the agent image. `--no-cache` does NOT cover
        # this — it only busts build-layer cache, not the FROM base.
        "--pull",
    ]
    if disable_provenance:
        docker_cmd.append("--provenance=false")

    # Tag with both versioned and latest
    docker_cmd.extend(["-t", ecr_image, "-t", latest_image])

    # Reproducible builds
    docker_cmd.extend(["--build-arg", "SOURCE_DATE_EPOCH=0"])

    # Registry cache
    if no_cache:
        docker_cmd.append("--no-cache")
    else:
        docker_cmd.extend(["--cache-from", f"type=registry,ref={cache_image}"])
    docker_cmd.extend(["--cache-to", f"type=registry,ref={cache_image},mode=max"])

    # Add --target if specified, or auto-detect from Dockerfile
    dockerfile_path = Path(build_path) / "Dockerfile"
    if target:
        docker_cmd.extend(["--target", target])
    elif dockerfile_path.exists():
        dockerfile_content = dockerfile_path.read_text()
        if "FROM" in dockerfile_content and "AS prod" in dockerfile_content:
            docker_cmd.extend(["--target", "prod"])

    # Add build args
    if build_args:
        for key, value in build_args.items():
            docker_cmd.extend(["--build-arg", f"{key}={value}"])

    # Build and push in one step
    docker_cmd.extend(["--push", build_path])

    result = subprocess.run(docker_cmd)
    if result.returncode != 0:
        return DockerPublishResult(
            success=False, ecr_image=ecr_image, latest_image=latest_image, error="Docker build failed"
        )

    return DockerPublishResult(success=True, ecr_image=ecr_image, latest_image=latest_image)


# Async versions for chronos dev
async def check_image_exists_async(image: ECRImage) -> bool:
    """Check if an image exists in ECR (async)."""
    cmd = [
        "aws",
        "ecr",
        "describe-images",
        "--repository-name",
        image.repository,
        "--image-ids",
        f"imageTag={image.tag}",
        "--region",
        image.region,
        "--output",
        "json",
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=_clean_aws_env(),
        )
        _, stderr = await proc.communicate()

        if proc.returncode == 0:
            return True

        stderr_str = stderr.decode()
        if "ImageNotFoundException" in stderr_str or "RepositoryNotFoundException" in stderr_str:
            return False

        logger.warning(f"ECR check failed: {stderr_str}")
        return False

    except FileNotFoundError:
        logger.warning("AWS CLI not found")
        return False


async def ensure_image_exists_async(image_url: str) -> bool:
    """Ensure an image exists in ECR (async)."""
    try:
        image = ECRImage.from_url(image_url)
    except ValueError as e:
        logger.error(f"Invalid ECR URL: {e}")
        raise

    logger.info(f"Checking if image exists: {image.short_name}")
    if await check_image_exists_async(image):
        logger.info(f"Image found: {image.short_name}")
        return True

    raise RuntimeError(
        f"Image not found in ECR: {image.full_url}\n\n"
        f"Push the image first with: plato world publish <path> or plato agent publish <path>"
    )
