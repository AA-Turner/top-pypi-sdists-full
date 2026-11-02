"""Local build + remote publish orchestration.

Split of the monolithic build_and_publish_to_apollo:
- LOCAL: read Chart.yaml, Docker buildx, package chart (pure Python), OCI push
- REMOTE: generate manifest, publish to Apollo (via cube-cloud)

Image builds run locally via `docker buildx` when a daemon is present, or
remotely via cube-cloud/kaniko otherwise (build_mode=auto) — so no local Docker
is required. Everything else is pure Python or proxied to cube-cloud.
"""

from __future__ import annotations

import logging
import os
import tempfile

from cube_common.config import ACR_DOCKER_PREFIX, ACR_HELM_PREFIX, ACR_REGISTRY, APOLLO_GROUP_ID
from cube_common.helm_chart import (
    ChartError,
    bump_version,
    find_chart_yaml,
    helmignore_negation_warning,
    load_helmignore,
    package_chart,
    parse_chart,
    update_chart_version,
)
from cube_common.manifest import generate_manifest
from cube_common.oci_registry import OCIPushError, push_chart

from cube_agent.local.docker_build import (
    DockerBuildError,
    build_and_push,
    docker_available,
    docker_login,
    remote_build_and_push,
)
from cube_agent.remote.client import CloudClient, CloudClientError

logger = logging.getLogger(__name__)


def _use_remote_build(build_mode: str) -> bool:
    """Decide whether to build server-side. 'auto' builds locally when a Docker
    daemon is present, otherwise remotely."""
    if build_mode == "remote":
        return True
    if build_mode == "local":
        return False
    return not docker_available()  # auto


async def build_and_publish(
    chart_path: str | None = None,
    version: str | None = None,
    bump: str = "patch",
    app_version: str | None = None,
    skip_docker: bool = False,
    dry_run: bool = False,
    build_args: dict[str, str] | None = None,
    dockerfile: str | None = None,
    target: str | None = None,
    build_mode: str = "auto",
    platform: str = "linux/amd64",
    show_build_log: bool = False,
) -> str:
    """Build and publish an app to Apollo.

    Pipeline:
    1. Find and parse Chart.yaml (local, pure Python)
    2. Get ACR token (remote, via cube-cloud)
    3. Docker login + build + push (local, only if Dockerfile exists)
    4. Update Chart.yaml version (local, pure Python)
    5. Package chart (local, pure Python tarfile)
    6. Push chart to OCI registry (local, pure Python httpx)
    7. Publish manifest to Apollo (remote, via cube-cloud)

    Apollo automatically adds newly published releases to the DEV release
    channel on publish, so no explicit promotion step is needed.
    """
    steps: list[str] = []
    errors: list[str] = []

    # Step 1: Find and parse Chart.yaml
    try:
        chart_yaml = find_chart_yaml(chart_path)
        info = parse_chart(chart_yaml)
        # Parse .helmignore now, not at packaging: a bad one (e.g. '**') would
        # otherwise fail after the image is pushed and Chart.yaml rewritten.
        load_helmignore(info["dir"])
    except ChartError as e:
        return f"Error: {e}"

    chart_dir = info["dir"]
    chart_name = info["name"]
    current_version = info["version"]

    new_version = version or bump_version(current_version, bump)
    new_app_version = app_version or new_version

    # Check for Dockerfile
    dockerfile_not_found = False
    if dockerfile:
        # Resolve relative to chart_dir, matching the auto-detect branch below —
        # otherwise a relative path is checked against the process cwd instead
        # of the chart directory the user actually meant.
        dockerfile_path = dockerfile if os.path.isabs(dockerfile) else os.path.join(chart_dir, dockerfile)
        dockerfile_not_found = not os.path.isfile(dockerfile_path)
    else:
        dockerfile_path = os.path.join(chart_dir, "Dockerfile")
        if not os.path.isfile(dockerfile_path):
            dockerfile_path = os.path.join(os.path.dirname(chart_dir), "Dockerfile")
    has_dockerfile = os.path.isfile(dockerfile_path) and not skip_docker
    remote_build = has_dockerfile and _use_remote_build(build_mode)

    # appVersion is the image tag the chart deploys. Write it when this run
    # pushes that tag, or when the caller names one (a chart-only publish for an
    # image built separately). Otherwise leave it alone: it still points at an
    # image that exists, whereas the default (the new chart version) was never
    # pushed. The summary reports exactly this value — it used to print the
    # default even when nothing was written, and the chart that shipped pointed
    # at an image tag that did not exist (ImagePullBackOff).
    # A named Dockerfile that is missing is not a chart-only publish: the caller
    # asked for a build that will not happen, so app_version names a tag nothing
    # pushed. Writing it would ship that ImagePullBackOff one branch over.
    build_missing = dockerfile_not_found and not skip_docker
    current_app_version = info.get("appVersion")
    app_version_to_write = (
        new_app_version if (has_dockerfile or (app_version and not build_missing)) else None
    )
    if app_version_to_write:
        app_version_line = f"{current_app_version or 'N/A'} -> {app_version_to_write}"
    elif build_missing:
        app_version_line = (
            f"{current_app_version or 'N/A'} (unchanged: the specified dockerfile was "
            "not found, so no image is built"
            + (" and app_version is not written" if app_version else "")
            + "; fix the dockerfile path, or pass skip_docker=true if the image was built separately)"
        )
    else:
        app_version_line = (
            f"{current_app_version or 'N/A'} (unchanged: no image is built; "
            "pass app_version to point the chart at a different image tag)"
        )

    if skip_docker:
        docker_status = "No (skip_docker)"
    elif dockerfile_not_found:
        docker_status = f"No (specified dockerfile not found: {dockerfile_path})"
    elif has_dockerfile:
        docker_status = f"Yes ({'remote (cube-cloud/kaniko)' if remote_build else 'local (docker buildx)'})"
    else:
        docker_status = "No (no Dockerfile)"

    summary = f"""
Helm Deploy Summary
{'=' * 42}
Chart:        {chart_name}
Path:         {chart_yaml}
Version:      {current_version} -> {new_version}
App Version:  {app_version_line}
Docker Build: {docker_status}
Channels:     DEV (added automatically by Apollo on publish)
{'=' * 42}

Pipeline:
1. Get ACR token (remote)
2. {('Build & push Docker image (' + ('remote/kaniko' if remote_build else 'local buildx') + ')') if has_dockerfile else '(skip Docker)'}
3. Update Chart.yaml version (local)
4. Package Helm chart (local, pure Python)
5. Push to OCI registry (local, pure Python)
6. Publish to Apollo (remote)
"""

    if dry_run:
        return summary + "\nDRY RUN - No changes made."

    steps.append(summary)

    # Step 2: Get ACR token from cube-cloud
    async with CloudClient() as cloud:
        try:
            token_text = await cloud.call_tool("acr_get_token", {})
            # Extract the token from the response text
            token = _extract_token(token_text)
        except CloudClientError as e:
            return f"Error getting ACR token: {e}"

    # Step 3: Docker build + push (local buildx, or remote kaniko via cube-cloud)
    docker_image_uri: str | None = None
    if has_dockerfile:
        docker_tag = f"{ACR_DOCKER_PREFIX}/{chart_name}:{new_app_version}"
        context_dir = os.path.dirname(dockerfile_path) or "."
        steps.append(
            f"{'Remotely building' if remote_build else 'Building'} Docker image: {docker_tag}"
        )

        try:
            if remote_build:
                async with CloudClient() as cloud:
                    docker_image_uri = await remote_build_and_push(
                        cloud,
                        context_dir=context_dir,
                        image_name=chart_name,
                        tag=new_app_version,
                        dockerfile_rel=os.path.basename(dockerfile_path),
                        target=target,
                        build_args=build_args,
                        platform=platform,
                        show_build_log=show_build_log,
                        log=lambda m: steps.append(f"  {m}"),
                    )
                steps.append(f"[ok] Image pushed: {docker_image_uri}")
            else:
                await docker_login(ACR_REGISTRY, token)
                result = await build_and_push(
                    context_dir,
                    docker_tag,
                    platforms=platform,
                    build_args=build_args,
                    dockerfile=dockerfile_path if dockerfile else None,
                    target=target,
                )
                steps.append(f"[ok] {result}")
                docker_image_uri = docker_tag
        except DockerBuildError as e:
            # Reached only when a Dockerfile was present and its build was
            # requested (this block is under `if has_dockerfile`). A failed build
            # means the release would reference an image that was never pushed, so
            # abort before publishing rather than ship a broken release that
            # ImagePullBackOffs on deploy. For a deliberate chart-only publish,
            # pass skip_docker=true (which takes the no-Dockerfile path instead).
            steps.append(f"[error] Image build failed — aborting before publish: {e}")
            if remote_build:
                # Already built server-side; remote isn't a recovery option, and
                # the failure is almost certainly a real Dockerfile/build error.
                hint = (
                    "Fix the build (check the failure above; pass show_build_log=true "
                    "for the build log) and retry, or pass skip_docker=true to publish "
                    "the chart without an image on purpose."
                )
            else:
                hint = (
                    "Fix the build and retry, pass build_mode=remote to build "
                    "server-side (no local Docker needed), or pass skip_docker=true "
                    "to publish the chart without an image on purpose."
                )
            return "\n".join(steps) + (
                "\n\nAborted: the image build failed, so nothing was published. "
                "Publishing would have created a release referencing an image that "
                f"was never pushed to the registry. {hint}"
            )

    # Step 4: Update Chart.yaml version
    try:
        update_chart_version(chart_yaml, new_version, app_version_to_write)
        steps.append(
            f"[ok] Updated Chart.yaml to version {new_version}"
            + (f", appVersion {app_version_to_write}" if app_version_to_write else "")
        )
    except ChartError as e:
        return f"Error updating Chart.yaml: {e}"

    # Step 5: Package chart (pure Python)
    try:
        tgz_path = package_chart(chart_dir, new_version)
        size_mb = os.path.getsize(tgz_path) / (1024 * 1024)
        steps.append(f"[ok] Packaged: {os.path.basename(tgz_path)} ({size_mb:.1f} MB)")
        negation_warning = helmignore_negation_warning(chart_dir)
        if negation_warning:
            steps.append(f"[warn] {negation_warning}")
    except ChartError as e:
        return f"Error packaging chart: {e}"

    # Step 6: Push to OCI registry (pure Python httpx)
    repo_path = f"charts/{APOLLO_GROUP_ID}/{chart_name}"
    try:
        digest = await push_chart(
            tgz_path=tgz_path,
            registry=ACR_REGISTRY,
            repository=repo_path,
            tag=new_version,
            token=token,
        )
        steps.append(f"[ok] Pushed to {ACR_HELM_PREFIX}/{chart_name}:{new_version}")
    except OCIPushError as e:
        return f"Error pushing chart: {e}"
    finally:
        # Clean up .tgz
        try:
            os.remove(tgz_path)
        except OSError:
            pass

    # Step 7: Publish manifest to Apollo (via cube-cloud)
    oci_url = f"{ACR_HELM_PREFIX}/{chart_name}"
    manifest_content = generate_manifest(
        chart_name,
        new_version,
        APOLLO_GROUP_ID,
        oci_url,
        docker_image_uri=docker_image_uri,
    )

    publish_ok = False
    async with CloudClient() as cloud:
        try:
            publish_result = await cloud.call_tool(
                "apollo_publish_manifest",
                {"manifest_yaml": manifest_content},
            )
            steps.append(f"[ok] Published to Apollo: {publish_result}")
            publish_ok = True
        except CloudClientError as e:
            errors.append(f"Apollo publish: {e}")
            steps.append(f"[warn] Apollo publish failed: {e}")

    # Apollo automatically adds the newly published release to the DEV release
    # channel, so there is no explicit promotion step here.
    if publish_ok:
        steps.append("[ok] Release added to DEV channel automatically by Apollo")

    # Final summary
    result = "\n".join(steps)
    status = "complete" if not errors else "completed with warnings"
    result += f"\n\nDeployment {status}!"
    result += f"\n\nChart: {chart_name}:{new_version}"
    result += f"\nHelm:  {ACR_HELM_PREFIX}/{chart_name}"

    if errors:
        result += "\n\nWarnings:\n" + "\n".join(f"  - {e}" for e in errors)

    return result


def _extract_token(token_text: str) -> str:
    """Extract the raw token from the acr_get_token response text."""
    # The acr_get_token tool returns the token as the text content
    # It may be wrapped in status text, try to find the raw token
    for line in token_text.strip().splitlines():
        line = line.strip()
        # ACR tokens are base64-ish JWT strings, typically long
        if len(line) > 100 and " " not in line:
            return line
    # Fallback: return the whole text stripped
    return token_text.strip()
