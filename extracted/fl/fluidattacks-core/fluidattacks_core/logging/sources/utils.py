import os


def get_env_var(key: str) -> str | None:
    return os.environ.get(key)


def get_environment() -> str:
    product_environment = os.environ.get("PRODUCT_ENVIRONMENT")
    branch = os.environ.get("CI_COMMIT_REF_NAME", "default")
    return product_environment or ("production" if branch == "trunk" else "development")


def get_version() -> str:
    product_version = os.environ.get("PRODUCT_VERSION")
    short_commit_sha = os.environ["CI_COMMIT_SHA"][:8] if os.environ.get("CI_COMMIT_SHA") else None
    return product_version or short_commit_sha or "00000000"


def set_product_id(product_id: str) -> None:
    os.environ["PRODUCT_ID"] = product_id


def set_product_environment(product_environment: str) -> None:
    os.environ["PRODUCT_ENVIRONMENT"] = product_environment


def set_product_version(product_version: str) -> None:
    os.environ["PRODUCT_VERSION"] = product_version


def set_commit_sha(commit_sha: str) -> None:
    os.environ["CI_COMMIT_SHA"] = commit_sha


def set_commit_ref_name(commit_ref_name: str) -> None:
    os.environ["CI_COMMIT_REF_NAME"] = commit_ref_name
