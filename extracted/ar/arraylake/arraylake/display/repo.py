from textwrap import indent

from arraylake.types import Repo


def reporepr(repo: Repo) -> str:
    header = ["<arraylake.Repo>"]
    contents = []

    # Basic info section
    contents.append(f"Repository: {repo.org}/{repo.name}")
    if repo.description:
        contents.append(f"Description: {repo.description}")

    # Metadata section
    if repo.metadata:
        contents.append("Metadata:")
        for key, value in repo.metadata.items():
            contents.append(f"  {key}: {value}")

    # Configuration section
    contents.append(f"Kind: {repo.kind.value}")
    contents.append(f"Visibility: {repo.visibility.value}")
    if repo.prefix:
        contents.append(f"Prefix: {repo.prefix}")

    # Status section
    contents.append(f"Status: {repo.status.mode.value}")
    if repo.status.message:
        contents.append(f"Status message: {repo.status.message}")

    # Bucket section
    if repo.bucket:
        contents.append(f"Bucket: {repo.bucket.nickname} ({repo.bucket.platform})")
        contents.append(f"Bucket name: {repo.bucket.name}")
        if repo.bucket.prefix:
            contents.append(f"Bucket prefix: {repo.bucket.prefix}")

    # Optimization config section
    if repo.optimization_config and (repo.optimization_config.gc_config or repo.optimization_config.expiration_config):
        contents.append("Optimization:")
        if repo.optimization_config.gc_config and repo.optimization_config.gc_config.enabled:
            contents.append("  GC: enabled")
        if repo.optimization_config.expiration_config and repo.optimization_config.expiration_config.enabled:
            contents.append("  Expiration: enabled")

    # Timestamps section
    contents.append(f"Created: {repo.created.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    contents.append(f"Updated: {repo.updated.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    if repo.created_by:
        contents.append(f"Created by: {repo.created_by}")

    return "\n".join(header + [indent(line, "  ") for line in contents])
