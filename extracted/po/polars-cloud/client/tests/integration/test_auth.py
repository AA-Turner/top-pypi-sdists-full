# mypy: disable-error-code="return-value,no-untyped-def,no-any-return,no-untyped-call"
import polars as pl
import pytest
from polars.lazyframe.opt_flags import DEFAULT_QUERY_OPT_FLAGS
from polars_cloud import ComputeContext, Workspace
from polars_cloud.constants import API_CLIENT
from polars_cloud.query._utils import prepare_query
from polars_cloud.query.dst import TmpDst

from .conftest import ComputeContextSpecsInput  # noqa: TID252

pytestmark = pytest.mark.auth


@pytest.mark.parametrize(
    "direct_compute",
    [ComputeContextSpecsInput(instance_type="t3.micro")],
    indirect=True,
)
def test_invalid_token(direct_compute: ComputeContext, workspace: Workspace) -> None:
    # Scenario 1: invalid token client side check
    direct_compute._compute_token = "INVALID123"
    lf = pl.LazyFrame({})
    with pytest.raises(ValueError, match="Failed to parse JWT Token"):
        lf.remote(direct_compute).show()

    plan, settings = prepare_query(
        lf=lf,
        dst=TmpDst(),
        engine="auto",
        plan_type="dot",
        shuffle_compression="auto",
        shuffle_format="auto",
        n_retries=0,
        distributed_settings=None,
        sink_to_single_file=None,
        optimizations=DEFAULT_QUERY_OPT_FLAGS,
    )

    client = direct_compute._get_direct_client()
    # Scenario 2: Invalid token server side check
    with pytest.raises(
        RuntimeError, match="The request does not have valid authentication credentials"
    ):
        client.do_query(plan=plan, settings=settings, token="INVALID123")  # type:ignore[union-attr]

    # Scenario 3: No token at all
    with pytest.raises(
        RuntimeError, match="The request does not have valid authentication credentials"
    ):
        client.do_query(plan=plan, settings=settings, token=None)  # type:ignore[union-attr]

    # Scenario 4: Token of another cluster
    ctx = ComputeContext(workspace=workspace, cpus=1, memory=1)
    ctx.start()
    ctx._get_token()  # Init the token
    direct_compute._compute_token = ctx._compute_token
    with pytest.raises(
        RuntimeError, match="The request does not have valid authentication credentials"
    ):
        lf.remote(direct_compute).show()

    # Scenario 4: Refresh token should work
    direct_compute._compute_token = None
    lf.remote(direct_compute).show()


@pytest.mark.parametrize(
    "direct_compute",
    [ComputeContextSpecsInput(instance_type="t3.micro")],
    indirect=True,
)
def test_service_account(direct_compute: ComputeContext, workspace: Workspace) -> None:
    # Force clear any possible cache
    direct_compute._compute_token = None
    direct_compute._direct_client = None

    # A service account in the same workspace should be able to access the cluster
    service_account = API_CLIENT.create_service_account(
        workspace.id, "ServiceAccount", None
    )
    API_CLIENT.authenticate(
        client_id=str(service_account.username),
        client_secret=service_account.api_secret,
        interactive=False,
    )

    # Check we are logged in with service account
    user = API_CLIENT.get_user()
    assert user.email == str(service_account.username) + "@sa.cloud.pola.rs"

    lf = pl.LazyFrame({})
    lf.remote(direct_compute).show()

    # Force clear cached client & token
    direct_compute._compute_token = None
    direct_compute._direct_client = None

    # Delete the service account
    API_CLIENT.delete_service_account(
        workspace_id=workspace.id, user_id=service_account.id
    )

    # This is quirky as the access token is still valid, but can't be exchanged by
    # keycloak anymore, it returns a 401 in that case
    with pytest.raises(ValueError, match="Status 401 Unauthorized with body"):
        lf.remote(direct_compute).show()


@pytest.mark.parametrize(
    "proxy_compute",
    [ComputeContextSpecsInput(instance_type="t3.micro")],
    indirect=True,
)
def test_query_owner(proxy_compute: ComputeContext, workspace: Workspace) -> None:
    proxy_compute._compute_token = None
    proxy_compute._direct_client = None

    # A service account in the same workspace should be able to access the cluster
    service_account = API_CLIENT.create_service_account(
        workspace.id, "ServiceAccount", None
    )
    API_CLIENT.authenticate(
        client_id=str(service_account.username),
        client_secret=service_account.api_secret,
        interactive=False,
    )

    # Check we are logged in with service account
    user = API_CLIENT.get_user()
    assert user.email == str(service_account.username) + "@sa.cloud.pola.rs"

    lf = pl.LazyFrame({})
    query = lf.remote(proxy_compute).execute()

    # Check if the query logged the SA as owner
    query_api = API_CLIENT.get_query(workspace.id, query._query_id)
    assert query_api.query.user_id == user.id, "Query was logged under different user"
