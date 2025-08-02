from metaflow_extensions.outerbounds.plugins import USE_CSPR_ROLE_ARN_IF_SET
from metaflow.metaflow_config import AWS_SECRETS_MANAGER_DEFAULT_REGION
from metaflow_extensions.outerbounds.plugins.s3_proxy.constants import (
    DEFAULT_PROXY_HOST,
    DEFAULT_PROXY_PORT,
)


def get_aws_client_with_s3_proxy(
    module,
    with_error=False,
    role_arn=None,
    session_vars=None,
    client_params=None,
    s3_config=None,
):
    if not client_params:
        client_params = {}

    client_params["region_name"] = client_params.get(
        "region_name", s3_config.get("region")
    )
    client_params["endpoint_url"] = s3_config.get(
        "endpoint_url", f"http://{DEFAULT_PROXY_HOST}:{DEFAULT_PROXY_PORT}"
    )

    import metaflow.plugins.aws.aws_client

    client = metaflow.plugins.aws.aws_client.get_aws_client(
        module,
        with_error=with_error,
        role_arn=role_arn or USE_CSPR_ROLE_ARN_IF_SET,
        session_vars=session_vars,
        client_params=client_params,
    )

    def override_s3_proxy_host_header(request, **kwargs):
        region = kwargs["region_name"]
        request.headers["Host"] = f"s3.{region}.amazonaws.com"
        if "x-ob-write-to" not in request.headers and "write_mode" in s3_config:
            request.headers["x-ob-write-to"] = s3_config.get("write_mode")

    client.meta.events.register("before-sign", override_s3_proxy_host_header)

    return client


def get_S3_with_s3_proxy(s3_config, *args, **kwargs):
    if "region_name" not in kwargs:
        kwargs["region_name"] = s3_config.get(
            "region", AWS_SECRETS_MANAGER_DEFAULT_REGION
        )

    kwargs["endpoint_url"] = s3_config.get(
        "endpoint_url", f"http://{DEFAULT_PROXY_HOST}:{DEFAULT_PROXY_PORT}"
    )

    import metaflow.plugins.datatools.s3

    mf_s3 = metaflow.plugins.datatools.s3.S3(*args, **kwargs)

    # Override reset_client to ensure proxy endpoint is preserved
    original_reset_client = mf_s3._s3_client.reset_client

    def proxy_reset_client():
        original_reset_client()
        import boto3

        proxy_client = boto3.client(
            "s3",
            region_name=kwargs.get("region_name", s3_config.get("region")),
            endpoint_url=s3_config.get("endpoint_url"),
        )
        mf_s3._s3_client._s3_client = proxy_client

    mf_s3._s3_client.reset_client = proxy_reset_client
    mf_s3._s3_client.reset_client()

    def override_s3_proxy_host_header(request, **kwargs):
        region = kwargs["region_name"]
        request.headers["Host"] = f"s3.{region}.amazonaws.com"
        if "x-ob-write-to" not in request.headers and "write_mode" in s3_config:
            request.headers["x-ob-write-to"] = s3_config.get("write_mode")

    mf_s3._s3_client._s3_client.meta.events.register(
        "before-sign", override_s3_proxy_host_header
    )
    return mf_s3
