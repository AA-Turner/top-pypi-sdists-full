import json

import icechunk
import pytest

from arraylake import AsyncClient
from arraylake.api_utils import ArraylakeHttpClient


async def create_marketplace_listing(token: str, org_name: str, repo_id: str, pricing_model: str = "free"):
    """Create a marketplace listing for a given repo.

    Client does not yet support marketplace listing creation, so we use the lower-level HTTP client here.

    Args:
        pricing_model: "free" or "paid". Use "paid" for listings that need to support filtered subscriptions.
    """
    client = ArraylakeHttpClient("http://localhost:8000", token=token)
    body = {
        "repo_id": str(repo_id),
        "status": "published",
        "repo_readme": f"# Test Marketplace Listing\n\nThis is a test listing for repo {repo_id}",
        "listing_name": f"Test Listing for {repo_id}",
        "pricing_model": pricing_model,
    }
    resp = await client._request("POST", f"/orgs/{org_name}/marketplace/listings", content=json.dumps(body))
    assert resp.is_success, f"Failed to create marketplace listing in org {org_name}: {resp.status_code} {resp.content}"
    return resp.json()


async def create_subscription_repo(token: str, org_name: str, repo_name: str, marketplace_listing_id: str):
    """Create a subscription repo in the specified org that subscribes to the given marketplace listing.

    Client does not yet support subscription repo creation, so we use the lower-level HTTP client here.
    """
    client = ArraylakeHttpClient("http://localhost:8000", token=token)
    body = {
        "name": repo_name,
        "description": "Subscriber repo for subscription tests",
        "marketplace_listing_id": str(marketplace_listing_id),
    }
    resp = await client._request("POST", f"/orgs/{org_name}/marketplace/subscribe", content=json.dumps(body))
    assert resp.is_success, f"Failed to create repo in isolated org {org_name}: {resp.status_code} {resp.content}"
    return resp.json()


async def create_filtered_subscription_repo(
    token: str,
    org_name: str,
    repo_name: str,
    marketplace_listing_id: str,
    bucket_nickname: str,
    target_filter: dict,
):
    """Create a filtered subscription repo in the specified org.

    Filtered subscriptions have their own storage bucket and apply a target_filter
    to select a subset of the provider's data.

    Client does not yet support filtered subscription repo creation, so we use the lower-level HTTP client here.
    """
    client = ArraylakeHttpClient("http://localhost:8000", token=token)
    body = {
        "name": repo_name,
        "description": "Filtered subscriber repo for subscription tests",
        "bucket_nickname": bucket_nickname,
        "marketplace_listing_id": str(marketplace_listing_id),
        "subscription_type": "filtered",
        "target_filter": target_filter,
    }
    resp = await client._request("POST", f"/orgs/{org_name}/marketplace/subscribe", content=json.dumps(body))
    assert resp.is_success, f"Failed to create filtered subscription repo in org {org_name}: {resp.status_code} {resp.content}"
    return resp.json()


async def run_subscription_workflow_test(token: str, parent_org: str, subscriber_org: str):
    """Helper function to test subscription workflow between a parent and subscriber repo.

    Args:
        token: Authentication token
        parent_org: Org name where the parent repo will be created
        subscriber_org: Org name where the subscriber repo will be created
    """
    aclient = AsyncClient(token=token)

    # Create a parent repo
    parent_repo_name = f"{parent_org}/parent-repo"
    parent_ic_repo = await aclient.create_repo(parent_repo_name)
    assert isinstance(parent_ic_repo, icechunk.Repository)

    # Create a new branch in the parent repo
    parent_ic_repo.create_branch("test-branch", parent_ic_repo.lookup_branch("main"))

    # Get parent repo object to get the ID
    parent_repo_obj = await aclient.get_repo_object(parent_repo_name)

    # Create a marketplace listing for the parent repo
    listing = await create_marketplace_listing(token, parent_org, parent_repo_obj.id)

    # Create a subscription repo that subscribes to the parent repo
    repo_name = "subscription-repo"
    await create_subscription_repo(token, subscriber_org, repo_name, listing["id"])

    # Check that the subscription repo has the same branches as the parent repo
    subscription_ic_repo = await aclient.get_repo(f"{subscriber_org}/{repo_name}")
    parent_branches = {branch for branch in parent_ic_repo.list_branches()}
    subscription_branches = {branch for branch in subscription_ic_repo.list_branches()}
    assert parent_branches == subscription_branches

    # Delete the parent repo and check that the subscription repo is now orphaned
    await aclient.delete_repo(parent_repo_name, imsure=True, imreallysure=True)
    orphaned_subscription_repo = await aclient.get_repo_object(f"{subscriber_org}/{repo_name}")
    assert orphaned_subscription_repo.subscription is not None
    assert orphaned_subscription_repo.subscription.status == "orphaned"


@pytest.mark.asyncio
async def test_subscription_repo_creation_same_org(isolated_org, default_bucket, token):
    async with isolated_org(default_bucket()) as (org_name, buckets):
        await run_subscription_workflow_test(token, org_name, org_name)


@pytest.mark.asyncio
async def test_subscription_repo_creation_different_orgs(two_isolated_orgs, default_bucket, token):
    async with two_isolated_orgs((default_bucket(),), (default_bucket(),)) as ((org1_name, buckets1), (org2_name, buckets2)):
        await run_subscription_workflow_test(token, org1_name, org2_name)
