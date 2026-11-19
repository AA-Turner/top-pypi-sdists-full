"""A bucket config as the icechunk `ObjectStoreConfig` that reaches it, in icechunk's serde shape.

zax takes a store as plain data (`zax.StoreLocator`) rather than an `icechunk.Storage`, which
cannot be serialized, so no icechunk object crosses into zax and the two need not agree on
an icechunk version. The mapping mirrors `_get_icechunk_storage_obj` in `storage.py`.

Shared by the server, the openEO worker and booth.
"""

from functools import lru_cache
from typing import Any, TypeVar

from arraylake.types import BucketModel

TBucket = TypeVar("TBucket", bound=BucketModel)

_TIGRIS_ENDPOINTS = ("fly.storage.tigris.dev", "t3.storage.dev")


def _str_or_none(value: object) -> str | None:
    return None if value is None else str(value)


def s3_options(region: str | None, endpoint_url: str | None, allow_http: bool, force_path_style: bool) -> dict[str, Any]:
    """icechunk's `S3Options`, for a bucket or a virtual chunk container."""
    return {
        "region": region,
        "endpoint_url": endpoint_url,
        "anonymous": False,
        "allow_http": allow_http,
        "force_path_style": force_path_style,
    }


def bucket_store_config(bucket: BucketModel, azure_account: str | None = None) -> dict[str, Any]:
    """The icechunk `ObjectStoreConfig` that reaches `bucket`.

    `azure_account` is the storage account an Azure bucket lives in. It defaults to the one
    on the bucket's auth config, which bucket responses carry and the base model doesn't.
    """
    extra = bucket.extra_config
    match bucket.platform:
        case "s3" | "s3-compatible" | "minio":
            endpoint_url = _str_or_none(extra.get("endpoint_url"))
            region = _str_or_none(extra.get("region_name"))
            use_ssl = bool(extra.get("use_ssl", True))
            force_path_style = bool(extra.get("force_path_style", not use_ssl))
            if endpoint_url and any(host in endpoint_url for host in _TIGRIS_ENDPOINTS):
                if region is None or region == "auto":
                    raise ValueError(f"Tigris bucket {bucket.nickname!r} needs a specific region, not {region!r}.")
                return {"tigris": s3_options(region, endpoint_url, not use_ssl, force_path_style)}
            if endpoint_url and ".r2." in endpoint_url:
                # What icechunk's R2 constructor fills in over plain S3 options.
                return {"s3_compatible": s3_options(region or "auto", endpoint_url, not use_ssl, True)}
            return {"s3": s3_options(region, endpoint_url, not use_ssl, force_path_style)}
        case "gs":
            return {"gcs": {}}
        case "azure":
            account = azure_account or getattr(getattr(bucket, "auth_config", None), "storage_account", None)
            if not account:
                raise ValueError(f"Could not determine the Azure storage account for bucket {bucket.nickname!r}.")
            return {"azure": {"account": account}}
    raise ValueError(f"Unsupported bucket platform: {bucket.platform!r}")


@lru_cache
def dualstack_endpoint(region: str) -> str:
    """S3's dualstack endpoint for `region`. Needs botocore, which the client does not depend on."""
    import botocore.session
    from botocore import UNSIGNED
    from botocore.config import Config

    client = botocore.session.get_session().create_client(
        "s3",
        region_name=region,
        config=Config(signature_version=UNSIGNED, s3={"use_dualstack_endpoint": True}),
    )
    return str(client.meta.endpoint_url)


def with_dualstack_endpoint(bucket: TBucket) -> TBucket:
    """Return ``bucket`` with the S3 dualstack endpoint injected.

    Applies only to genuine S3 buckets without their own endpoint: pulls then
    resolve AAAA endpoints and ride the IPv6/egress-only-gateway path instead
    of the NAT gateway (same-region transfer is free on either path). The
    endpoint is injected per bucket, into a copy, because a process-wide
    AWS_USE_DUALSTACK_ENDPOINT makes icechunk's aws-sdk-s3 fail for buckets
    that carry their own endpoint_url (R2, Tigris, RustFS): "Cannot set
    dual-stack in combination with a custom endpoint".
    """
    if bucket.platform != "s3" or bucket.extra_config.get("endpoint_url"):
        return bucket
    region = bucket.extra_config.get("region_name")
    if not region:
        return bucket
    return bucket.model_copy(update={"extra_config": {**bucket.extra_config, "endpoint_url": dualstack_endpoint(str(region))}})
