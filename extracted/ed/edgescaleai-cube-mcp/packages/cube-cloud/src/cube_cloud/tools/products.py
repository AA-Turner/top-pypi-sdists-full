"""Product and release channel management tools."""

from __future__ import annotations

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_common import apollo_queries as Q


def _version_from_coordinate(coordinate: str) -> str:
    """Extract version from a maven coordinate (group:name:version)."""
    parts = coordinate.split(":")
    return parts[2] if len(parts) >= 3 else coordinate


async def list_products(
    client: ApolloClient, search: str | None = None, page_size: int = 50
) -> str:
    page_size = min(max(page_size, 1), 200)
    products: list[dict] = []
    page_token: str | None = None

    # Paginate through all results to ensure search doesn't miss products
    while True:
        variables: dict = {"pageSize": page_size}
        if page_token:
            variables["pageToken"] = page_token

        data = await client.graphql(Q.LIST_PRODUCTS, variables)
        page_data = data.get("apollo", {}).get("products", {})
        products.extend(page_data.get("products", []))

        page_token = page_data.get("nextPageToken")
        if not page_token:
            break

    if search:
        search_lower = search.lower()
        products = [
            p for p in products if search_lower in p.get("productId", "").lower()
        ]

    if not products:
        suffix = f' matching "{search}"' if search else ""
        return f"No products found{suffix}."

    lines = [f"Apollo Products ({len(products)})", "=" * 60]
    for p in sorted(products, key=lambda x: x.get("productId", "")):
        pid = p.get("productId", "?")
        labels = p.get("labels", [])
        lines.append(f"  {pid}")
        for lbl in labels:
            lines.append(f"    {lbl['labelId']}: {lbl['labelValue']}")
    return "\n".join(lines)


async def compare_product_versions(
    client: ApolloClient, product_id: str, environments: str
) -> str:
    from cube_cloud.tools.environments import _resolve_environment

    env_names = [e.strip() for e in environments.split(",") if e.strip()]
    if not env_names:
        return "Error: no environments specified."

    lines = [f"Product Version Comparison: {product_id}", "=" * 60]

    for env_name in env_names:
        try:
            env_info = await _resolve_environment(client, env_name)
        except ApolloError as e:
            lines.append(f"  {env_name}: {e}")
            continue

        data = await client.graphql(Q.ENTITY_BY_NAME, {"id": env_info["id"]})
        entities = (
            data.get("apollo", {})
            .get("environmentById", {})
            .get("entities", {})
            .get("entities", [])
        )

        matched = [
            e for e in entities
            if (e.get("product") or {}).get("productId", "") == product_id
        ]

        if not matched:
            lines.append(f"  {env_info.get('name', env_name)}: not installed")
        else:
            for e in matched:
                ename = (e.get("entityLocator") or {}).get("entityName", "?")
                # Use entity health data if available
                lines.append(f"  {env_info.get('name', env_name)}: entity={ename}")

    return "\n".join(lines)


async def get_product_releases(
    client: ApolloClient, product_id: str, page_size: int = 10
) -> str:
    page_size = min(max(page_size, 1), 50)
    data = await client.graphql(
        Q.GET_PRODUCT_RELEASES, {"productId": product_id, "pageSize": page_size}
    )
    product = data.get("apollo", {}).get("productByProductIdV2")
    if not product:
        return f"Product not found: {product_id}"

    releases = product.get("productReleases", {}).get("productReleases", [])

    if not releases:
        return f"No releases found for product: {product_id}"

    lines = [f"Releases for {product_id} ({len(releases)})", "=" * 60]
    for r in releases:
        version = _version_from_coordinate(r.get("mavenCoordinate", "?"))
        rid = r.get("rid", "")
        channels = [
            ch.get("name", "?")
            for ch in r.get("releaseChannels", [])
        ]
        ch_str = ", ".join(channels) if channels else "(no channels)"
        lines.append(f"  {version}")
        lines.append(f"    RID:      {rid}")
        lines.append(f"    Channels: {ch_str}")

    return "\n".join(lines)


async def list_release_channels(
    client: ApolloClient,
    search: str | None = None,
    include_env_specific: bool = False,
) -> str:
    data = await client.graphql(Q.LIST_RELEASE_CHANNELS)
    # Collect unique channels from product releases
    seen: dict[str, dict] = {}
    releases = (
        data.get("apollo", {})
        .get("productReleases", {})
        .get("productReleases", [])
    )
    for rel in releases:
        for ch in rel.get("releaseChannels", []):
            name = ch.get("name", "")
            if name and name not in seen:
                metadata = ch.get("metadata", {})
                seen[name] = {
                    "name": name,
                    "rid": ch.get("rid", ""),
                    "description": metadata.get("description", ""),
                    "type": metadata.get("type", ""),
                }

    channels = list(seen.values())

    if not include_env_specific:
        channels = [
            ch for ch in channels
            if ch.get("type", "") != "ENVIRONMENT_SPECIFIC"
        ]

    if search:
        search_lower = search.lower()
        channels = [
            ch for ch in channels
            if search_lower in ch.get("name", "").lower()
        ]

    if not channels:
        suffix = f' matching "{search}"' if search else ""
        return f"No release channels found{suffix}."

    lines = [f"Release Channels ({len(channels)})", "=" * 60]
    for ch in sorted(channels, key=lambda x: x.get("name", "")):
        name = ch.get("name", "?")
        rid = ch.get("rid", "")
        desc = ch.get("description", "")
        ch_type = ch.get("type", "")
        lines.append(f"  {name}")
        lines.append(f"    RID:  {rid}")
        if desc:
            lines.append(f"    Desc: {desc}")
        if ch_type:
            lines.append(f"    Type: {ch_type}")

    return "\n".join(lines)
