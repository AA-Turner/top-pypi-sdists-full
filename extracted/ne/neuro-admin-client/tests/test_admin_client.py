import datetime
import typing as t
from contextlib import asynccontextmanager
from dataclasses import replace
from decimal import Decimal

import pytest
from aiohttp import ClientResponseError

from neuro_admin_client import (
    AdminClient,
    Balance,
    Cluster,
    ClusterUser,
    ClusterUserRoleType,
    GetUserResponse,
    Org,
    OrgCluster,
    OrgNotificationIntervals,
    OrgUser,
    OrgUserRoleType,
    Project,
    ProjectUser,
    ProjectUserRoleType,
    Quota,
    User,
)

from .conftest import AdminServer


class TestAdminClient:
    async def test_client_no_url_no_errors(self) -> None:
        async with AdminClient(base_url=None) as client:
            await client.get_user("name")
            await client.get_org("org")
            await client.get_cluster("cluster")
            await client.get_cluster_user("cluster", "name")

    async def test_create_user(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_user(name="name", email="email")

        assert len(mock_admin_server.users) == 1
        created_user = mock_admin_server.users[0]
        assert created_user.name == "name"
        assert created_user.email == "email"

    async def test_create_user_skip_auto_add_to_clusters(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_user(
                name="name", email="email", skip_auto_add_to_clusters=True
            )

            assert mock_admin_server.last_skip_auto_add_to_clusters

            await client.create_user(
                name="name", email="email", skip_auto_add_to_clusters=False
            )

            assert not mock_admin_server.last_skip_auto_add_to_clusters

    async def test_create_user_first_name_last_name(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_user(
                name="name",
                email="email",
                first_name="first_name",
                last_name="last_name",
            )

        assert len(mock_admin_server.users) == 1
        created_user = mock_admin_server.users[0]
        assert created_user.name == "name"
        assert created_user.email == "email"

        assert created_user.first_name == "first_name"
        assert created_user.last_name == "last_name"

    async def test_list_users(self, mock_admin_server: AdminServer) -> None:
        date = datetime.datetime.now(datetime.timezone.utc)

        mock_admin_server.users = [
            User(
                name="name",
                email="email",
            ),
            User(
                name="name2",
                email="email2",
                first_name="first_name",
                last_name="last_name",
                created_at=date,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            users = await client.list_users()

        assert len(users) == 2
        assert set(users) == set(mock_admin_server.users)

    async def test_get_user(self, mock_admin_server: AdminServer) -> None:
        date = datetime.datetime.now(datetime.timezone.utc)

        mock_admin_server.users = [
            User(
                name="name",
                email="email",
            ),
            User(
                name="name2",
                email="email2",
                first_name="first_name",
                last_name="last_name",
                created_at=date,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            user = await client.get_user(name="name")
            assert user == mock_admin_server.users[0]

            user = await client.get_user(name="name2")
            assert user == mock_admin_server.users[1]

    async def test_get_user_with_clusters(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster1",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
            Cluster(
                name="cluster2",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster1",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test1",
                cluster_name="cluster2",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            user, cluster_users = await client.get_user_with_clusters(name="test1")
            assert user == mock_admin_server.users[0]
            assert set(cluster_users) == set(mock_admin_server.cluster_users)

    async def test_get_user_with_additional_info(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.org_users = [
            OrgUser(
                user_name="test1",
                org_name="org1",
                role=OrgUserRoleType.ADMIN,
                balance=Balance(),
            )
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster1",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
            Cluster(
                name="cluster2",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster1",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test1",
                cluster_name="cluster2",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]
        mock_admin_server.project_users = [
            ProjectUser(
                project_name="proj1",
                user_name="test1",
                cluster_name="cluster1",
                org_name=None,
                role=ProjectUserRoleType.WRITER,
            ),
            ProjectUser(
                project_name="proj2",
                user_name="test1",
                cluster_name="cluster2",
                org_name=None,
                role=ProjectUserRoleType.MANAGER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            res1 = await client.get_user(name="test1")
            assert res1 == mock_admin_server.users[0]
            res2 = await client.get_user(name="test1", include_clusters=True)
            assert res2[0] == mock_admin_server.users[0]
            assert set(res2[1]) == set(mock_admin_server.cluster_users)

            res3 = await client.get_user(name="test1", include_projects=True)
            assert res3[0] == mock_admin_server.users[0]
            assert set(res3[1]) == set(mock_admin_server.project_users)

            res4 = await client.get_user(
                name="test1", include_clusters=True, include_projects=True
            )
            assert res4[0] == mock_admin_server.users[0]
            assert set(res4[1]) == set(mock_admin_server.cluster_users)
            assert set(res4[2]) == set(mock_admin_server.project_users)

            res5 = await client.get_user(name="test1", include_orgs=True)
            assert res5 == GetUserResponse(
                user=mock_admin_server.users[0],
                orgs=mock_admin_server.org_users,
            )

    async def test_create_org(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_org(name="name")

        assert len(mock_admin_server.orgs) == 1
        created_org = mock_admin_server.orgs[0]
        assert created_org.name == "name"

    async def test_create_org_skip_auto_add_to_clusters(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_org(name="name", skip_auto_add_to_clusters=True)

            assert mock_admin_server.last_skip_auto_add_to_clusters

            await client.create_org(name="name", skip_auto_add_to_clusters=False)

            assert not mock_admin_server.last_skip_auto_add_to_clusters

    async def test_patch_org(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
                user_default_credits=Decimal(100),
                notification_intervals=OrgNotificationIntervals(
                    balance_projection_seconds=[60 * 60 * 24],
                    balance_amount=None,
                    balance_depletion_seconds=None,
                ),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org = await client.update_org(
                org_name="org",
                user_default_credits=Decimal(200),
                notification_intervals=OrgNotificationIntervals(
                    balance_projection_seconds=[60 * 60 * 24 * 2],
                    balance_amount=[
                        -100,
                    ],
                    balance_depletion_seconds=[
                        60,
                    ],
                ),
            )
            assert org.user_default_credits == Decimal(200)
            assert org == mock_admin_server.orgs[0]
            intervals = t.cast(OrgNotificationIntervals, org.notification_intervals)

            assert intervals.balance_projection_seconds is not None
            assert intervals.balance_projection_seconds[0] == 60 * 60 * 24 * 2

            assert intervals.balance_amount is not None
            assert intervals.balance_amount[0] == -100

            assert intervals.balance_depletion_seconds is not None
            assert intervals.balance_depletion_seconds[0] == 60

    async def test_create_org_with_defaults(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            res_org = await client.create_org(
                name="test_org", user_default_credits=Decimal("100.11")
            )

        assert res_org.name == "test_org"
        assert res_org.user_default_credits == Decimal("100.11")

        assert mock_admin_server.orgs == [res_org]

    async def test_patch_org_defaults(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
                user_default_credits=Decimal(100),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org = await client.update_org_defaults(
                org_name="org",
                user_default_credits=Decimal(200),
            )
            assert org.user_default_credits == Decimal(200)
            assert org == mock_admin_server.orgs[0]

            # set defaults to `None`
            org = await client.update_org_defaults(
                org_name="org",
                user_default_credits=None,
            )
            assert org.user_default_credits is None
            assert org == mock_admin_server.orgs[0]

    async def test_list_orgs(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="name",
            ),
            Org(
                name="name2",
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            orgs = await client.list_orgs()

        assert len(orgs) == 2
        assert set(orgs) == set(mock_admin_server.orgs)

    async def test_get_org(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="name",
            ),
            Org(
                name="name2",
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org = await client.get_org(name="name")
            assert org == mock_admin_server.orgs[0]

            org = await client.get_org(name="name2")
            assert org == mock_admin_server.orgs[1]

    async def test_delete_org(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="name",
            ),
            Org(
                name="name2",
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org = await client.delete_org(name="name")
            assert org.name == "name"

            with pytest.raises(ClientResponseError):
                org = await client.get_org(name="name")

            assert len(mock_admin_server.orgs) == 1

            org = await client.get_org(name="name2")
            assert org == mock_admin_server.orgs[0]

    async def test_create_cluster(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="name")

        assert len(mock_admin_server.clusters) == 1
        created_cluster = mock_admin_server.clusters[0]
        assert created_cluster.name == "name"
        assert not created_cluster.maintenance

    async def test_create_cluster_with_defaults(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(
                name="name",
                default_credits=Decimal(20),
                default_quota=Quota(total_running_jobs=42),
                default_role=ClusterUserRoleType.MANAGER,
            )

        assert len(mock_admin_server.clusters) == 1
        created_cluster = mock_admin_server.clusters[0]
        assert created_cluster.name == "name"
        assert created_cluster.default_credits == Decimal(20)
        assert created_cluster.default_quota == Quota(total_running_jobs=42)
        assert created_cluster.default_role == ClusterUserRoleType.MANAGER

    async def test_create_cluster_with_maintenance(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(
                name="name",
                maintenance=True,
            )

        assert len(mock_admin_server.clusters) == 1
        created_cluster = mock_admin_server.clusters[0]
        assert created_cluster.name == "name"
        assert created_cluster.maintenance

    async def test_update_cluster(self, mock_admin_server: AdminServer) -> None:
        cluster = Cluster(
            name="name",
            default_credits=Decimal(20),
            default_quota=Quota(total_running_jobs=42),
            maintenance=True,
            default_role=ClusterUserRoleType.USER,
        )

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name=cluster.name)
            await client.update_cluster(cluster)

        assert len(mock_admin_server.clusters) == 1
        created_cluster = mock_admin_server.clusters[0]
        assert created_cluster == cluster

    async def test_list_clusters(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.clusters = [
            Cluster(
                name="name",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
            Cluster(
                name="name2",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            clusters = await client.list_clusters()

        assert len(clusters) == 2
        assert set(clusters) == set(mock_admin_server.clusters)

    async def test_get_cluster(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.clusters = [
            Cluster(
                name="name",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
            Cluster(
                name="name2",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster = await client.get_cluster(name="name")
            assert cluster == mock_admin_server.clusters[0]

            cluster = await client.get_cluster(name="name2")
            assert cluster == mock_admin_server.clusters[1]

    async def test_delete_cluster(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.clusters = [
            Cluster(
                name="name",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
            Cluster(
                name="name2",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster = await client.delete_cluster(name="name")
            assert cluster.name == "name"

            with pytest.raises(ClientResponseError):
                cluster = await client.get_cluster(name="name")

            assert len(mock_admin_server.clusters) == 1

            cluster = await client.get_cluster(name="name2")
            assert cluster == mock_admin_server.clusters[0]

    async def test_create_cluster_user(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_user(name="test_user", email="email")
            res_user_with_info = await client.create_cluster_user(
                cluster_name="test",
                user_name="test_user",
                role=ClusterUserRoleType.USER,
                quota=Quota(total_running_jobs=12),
                with_user_info=True,
            )
            res_user = await client.get_cluster_user(
                cluster_name="test", user_name="test_user"
            )

        assert res_user.cluster_name == "test"
        assert res_user.user_name == "test_user"
        assert res_user.role == ClusterUserRoleType.USER
        assert res_user.quota.total_running_jobs == 12
        assert res_user_with_info.user_info.email == "email"

        assert mock_admin_server.cluster_users == [res_user]

    async def test_update_cluster_user(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_user(name="test_user", email="email")
            res_user = await client.create_cluster_user(
                cluster_name="test",
                user_name="test_user",
                role=ClusterUserRoleType.USER,
                quota=Quota(total_running_jobs=12),
            )
            res_user = replace(res_user, role=ClusterUserRoleType.ADMIN)
            res_user = await client.update_cluster_user(res_user)

        assert res_user.role == ClusterUserRoleType.ADMIN
        assert mock_admin_server.cluster_users == [res_user]

    async def test_create_cluster_user_with_org(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_user(name="test_user", email="email")
            res_user_with_info = await client.create_cluster_user(
                cluster_name="test",
                user_name="test_user",
                role=ClusterUserRoleType.USER,
                quota=Quota(total_running_jobs=12),
                with_user_info=True,
                org_name="some_org",
            )
            res_user = await client.get_cluster_user(
                cluster_name="test",
                user_name="test_user",
                org_name="some_org",
            )

        assert res_user.cluster_name == "test"
        assert res_user.user_name == "test_user"
        assert res_user.org_name == "some_org"
        assert res_user.role == ClusterUserRoleType.USER
        assert res_user.quota.total_running_jobs == 12
        assert res_user_with_info.user_info.email == "email"

        assert mock_admin_server.cluster_users == [res_user]

    async def test_update_cluster_user_with_org(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_user(name="test_user", email="email")
            res_user = await client.create_cluster_user(
                cluster_name="test",
                user_name="test_user",
                role=ClusterUserRoleType.USER,
                quota=Quota(total_running_jobs=12),
                org_name="some_org",
            )
            res_user = replace(res_user, role=ClusterUserRoleType.ADMIN)
            res_user = await client.update_cluster_user(res_user)

        assert res_user.role == ClusterUserRoleType.ADMIN
        assert mock_admin_server.cluster_users == [res_user]

    async def test_list_clusters_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test2",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster_users = await client.list_cluster_users("cluster")

        assert len(cluster_users) == 2
        assert set(cluster_users) == set(mock_admin_server.cluster_users)

    async def test_list_clusters_user_can_only_get_usernames(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test2",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]

        class PatchedAdminClient(AdminClient):
            @asynccontextmanager
            async def _request(self, *args, **kwargs) -> t.Any:  # type: ignore
                kwargs["params"]["only_usernames"] = "true"
                async with AdminClient._request(self, *args, **kwargs) as resp:
                    yield resp

        async with PatchedAdminClient(base_url=mock_admin_server.url) as client:
            cluster_users = await client.list_cluster_users("cluster")

        expected = [replace(u, role=None) for u in mock_admin_server.cluster_users]
        assert len(cluster_users) == 2
        assert set(cluster_users) == set(expected)

    async def test_list_clusters_user_with_org(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test2",
                cluster_name="cluster",
                org_name="org1",
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster_users = await client.list_cluster_users("cluster", org_name="org1")

        assert len(cluster_users) == 1
        assert set(cluster_users) == {mock_admin_server.cluster_users[1]}

    async def test_get_cluster_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test2",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster_user = await client.get_cluster_user(
                cluster_name="cluster", user_name="test1"
            )
            assert cluster_user == mock_admin_server.cluster_users[0]

            cluster_user = await client.get_cluster_user(
                cluster_name="cluster", user_name="test2"
            )
            assert cluster_user == mock_admin_server.cluster_users[1]

    async def test_delete_cluster_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test2",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.delete_cluster_user(cluster_name="cluster", user_name="test1")
            assert len(mock_admin_server.cluster_users) == 1
            assert mock_admin_server.cluster_users[0].user_name == "test2"

    async def test_delete_cluster_user_with_org(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name="org",
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.USER,
            ),
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(),
                role=ClusterUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.delete_cluster_user(
                cluster_name="cluster", user_name="test1", org_name="org"
            )
            assert len(mock_admin_server.cluster_users) == 1
            assert mock_admin_server.cluster_users[0].user_name == "test1"
            assert mock_admin_server.cluster_users[0].cluster_name == "cluster"
            assert mock_admin_server.cluster_users[0].org_name is None

    async def test_create_org_user(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_org(name="test")
            await client.create_user(name="test_user", email="email")
            res_user_with_info = await client.create_org_user(
                org_name="test",
                user_name="test_user",
                role=OrgUserRoleType.USER,
                balance=Balance(credits=Decimal(20)),
                with_user_info=True,
            )
            res_user = await client.get_org_user(org_name="test", user_name="test_user")

        assert res_user.org_name == "test"
        assert res_user.user_name == "test_user"
        assert res_user.role == OrgUserRoleType.USER
        assert res_user_with_info.user_info.email == "email"
        assert res_user.balance.credits == Decimal(20)

        assert mock_admin_server.org_users == [res_user]

    async def test_update_org_user(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_org(name="test")
            await client.create_user(name="test_user", email="email")
            res_user_with_info = await client.create_org_user(
                org_name="test",
                user_name="test_user",
                role=OrgUserRoleType.USER,
                balance=Balance(credits=Decimal(20)),
                with_user_info=True,
            )
            res_user = await client.get_org_user(org_name="test", user_name="test_user")
            res_user = replace(res_user, role=OrgUserRoleType.ADMIN)
            res_user = await client.update_org_user(res_user)

        assert res_user.org_name == "test"
        assert res_user.user_name == "test_user"
        assert res_user.role == OrgUserRoleType.ADMIN
        assert res_user_with_info.user_info.email == "email"

        assert mock_admin_server.org_users == [res_user]

    async def test_list_orgs_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.org_users = [
            OrgUser(
                user_name="test1",
                org_name="org",
                role=OrgUserRoleType.USER,
                balance=Balance(),
            ),
            OrgUser(
                user_name="test2",
                org_name="org",
                role=OrgUserRoleType.ADMIN,
                balance=Balance(),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_users = await client.list_org_users("org")

        assert len(org_users) == 2
        assert set(org_users) == set(mock_admin_server.org_users)

    @pytest.mark.parametrize(
        ("roles", "expected_count"),
        [
            ([OrgUserRoleType.USER], 1),
            ([OrgUserRoleType.MANAGER], 1),
            ([OrgUserRoleType.ADMIN], 1),
            ([OrgUserRoleType.USER, OrgUserRoleType.ADMIN], 2),
            ([OrgUserRoleType.USER, OrgUserRoleType.MANAGER], 2),
            ([OrgUserRoleType.MANAGER, OrgUserRoleType.ADMIN], 2),
            ([OrgUserRoleType.USER, OrgUserRoleType.MANAGER, OrgUserRoleType.ADMIN], 3),
        ],
    )
    async def test_list_orgs_user_roles_filter(
        self,
        roles: t.List[OrgUserRoleType],
        expected_count: int,
        mock_admin_server: AdminServer,
    ) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]

        # cleanup of internal data
        mock_admin_server.users, mock_admin_server.org_users = [], []

        # prefill both users and org users
        for user_name, role in (
            ("test1", OrgUserRoleType.USER),
            ("test2", OrgUserRoleType.MANAGER),
            ("test3", OrgUserRoleType.ADMIN),
        ):
            mock_admin_server.users.append(
                User(name=user_name, email=f"{user_name}@email.com")
            )
            mock_admin_server.org_users.append(
                OrgUser(
                    user_name=user_name, org_name="org", role=role, balance=Balance()
                )
            )

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_users = await client.list_org_users("org", roles=roles)

        assert len(org_users) == expected_count
        actual_roles = {ou.role for ou in org_users}
        expected_roles = {r.value for r in roles}
        assert actual_roles == expected_roles

    async def test_get_org_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.org_users = [
            OrgUser(
                user_name="test1",
                org_name="org",
                balance=Balance(),
                role=OrgUserRoleType.USER,
            ),
            OrgUser(
                user_name="test2",
                org_name="org",
                balance=Balance(),
                role=OrgUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_user = await client.get_org_user(org_name="org", user_name="test1")
            assert org_user == mock_admin_server.org_users[0]

            org_user = await client.get_org_user(org_name="org", user_name="test2")
            assert org_user == mock_admin_server.org_users[1]

    async def test_delete_org_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.org_users = [
            OrgUser(
                user_name="test1",
                org_name="org",
                balance=Balance(),
                role=OrgUserRoleType.USER,
            ),
            OrgUser(
                user_name="test2",
                org_name="org",
                balance=Balance(),
                role=OrgUserRoleType.ADMIN,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.delete_org_user(org_name="org", user_name="test1")
            assert len(mock_admin_server.org_users) == 1
            assert mock_admin_server.org_users[0].user_name == "test2"

    async def test_create_org_cluster(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_org(
                name="test_org",
            )
            res_org = await client.create_org_cluster(
                cluster_name="test", org_name="test_org", storage_size=1024
            )

        assert res_org.cluster_name == "test"
        assert res_org.org_name == "test_org"
        assert res_org.storage_size == 1024
        assert not res_org.maintenance

        assert mock_admin_server.org_clusters == [res_org]

    async def test_create_org_cluster_with_defaults(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_org(
                name="test_org",
            )
            res_org = await client.create_org_cluster(
                cluster_name="test",
                org_name="test_org",
                default_credits=Decimal(20),
                default_quota=Quota(total_running_jobs=42),
                default_role=ClusterUserRoleType.MEMBER,
            )

        assert res_org.cluster_name == "test"
        assert res_org.org_name == "test_org"
        assert res_org.default_credits == Decimal(20)
        assert res_org.default_quota == Quota(total_running_jobs=42)
        assert res_org.default_role == ClusterUserRoleType.MEMBER

        assert mock_admin_server.org_clusters == [res_org]

    async def test_create_org_cluster_with_maintenance(
        self, mock_admin_server: AdminServer
    ) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_org(
                name="test_org",
            )
            res_org = await client.create_org_cluster(
                cluster_name="test",
                org_name="test_org",
                maintenance=True,
            )

        assert res_org.cluster_name == "test"
        assert res_org.org_name == "test_org"
        assert res_org.maintenance

        assert mock_admin_server.org_clusters == [res_org]

    async def test_update_org_cluster(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_cluster(name="test")
            await client.create_org(
                name="test_org",
            )
            res_org = await client.create_org_cluster(
                cluster_name="test", org_name="test_org"
            )
            new_org_cluster = replace(
                res_org,
                balance=Balance(credits=Decimal(22)),
                default_credits=Decimal(20),
                default_quota=Quota(total_running_jobs=42),
                maintenance=True,
            )
            await client.update_org_cluster(new_org_cluster)

        assert mock_admin_server.org_clusters == [new_org_cluster]

    async def test_list_org_clusters(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="test1",
            ),
            Org(
                name="test2",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.org_clusters = [
            OrgCluster(
                cluster_name="cluster",
                org_name="test1",
                balance=Balance(),
                quota=Quota(),
            ),
            OrgCluster(
                cluster_name="cluster",
                org_name="test2",
                balance=Balance(credits=Decimal("20")),
                quota=Quota(total_running_jobs=22),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_clusters = await client.list_org_clusters("cluster")

        assert len(org_clusters) == 2
        assert set(org_clusters) == set(mock_admin_server.org_clusters)

    async def test_get_org_cluster(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="test1",
            ),
            Org(
                name="test2",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.org_clusters = [
            OrgCluster(
                cluster_name="cluster",
                org_name="test1",
                balance=Balance(),
                quota=Quota(),
            ),
            OrgCluster(
                cluster_name="cluster",
                org_name="test2",
                balance=Balance(credits=Decimal("20")),
                quota=Quota(total_running_jobs=22),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_cluster = await client.get_org_cluster(
                cluster_name="cluster", org_name="test1"
            )
            assert org_cluster == mock_admin_server.org_clusters[0]

            org_cluster = await client.get_org_cluster(
                cluster_name="cluster", org_name="test2"
            )
            assert org_cluster == mock_admin_server.org_clusters[1]

    async def test_delete_org_cluster(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="test1",
            ),
            Org(
                name="test2",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.org_clusters = [
            OrgCluster(
                cluster_name="cluster",
                org_name="test1",
                balance=Balance(),
                quota=Quota(),
            ),
            OrgCluster(
                cluster_name="cluster",
                org_name="test2",
                balance=Balance(credits=Decimal("20")),
                quota=Quota(total_running_jobs=22),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.delete_org_cluster(cluster_name="cluster", org_name="test1")
            assert len(mock_admin_server.org_clusters) == 1
            assert mock_admin_server.org_clusters[0].org_name == "test2"

    async def test_patch_cluster_user_quota(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name=None,
                balance=Balance(),
                quota=Quota(total_running_jobs=10),
                role=ClusterUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster_user = await client.update_cluster_user_quota(
                cluster_name="cluster",
                user_name="test1",
                quota=Quota(total_running_jobs=15),
            )
            assert cluster_user.quota.total_running_jobs == 15

            cluster_user = await client.update_cluster_user_quota_by_delta(
                cluster_name="cluster",
                user_name="test1",
                delta=Quota(total_running_jobs=10),
            )
            assert cluster_user.quota.total_running_jobs == 25

    async def test_patch_org_user_balance(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [Org(name="org")]
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.org_users = [
            OrgUser(
                org_name="org",
                user_name="test1",
                balance=Balance(),
                role=OrgUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_user = await client.update_org_user_balance(
                org_name="org", user_name="test1", credits=Decimal(15)
            )
            assert org_user.balance.credits == Decimal(15)

            org_user = await client.update_org_user_balance_by_delta(
                org_name="org", user_name="test1", delta=Decimal(10)
            )
            assert org_user.balance.credits == Decimal(25)

    async def test_org_cluster_add_spending(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.org_clusters = [
            OrgCluster(
                cluster_name="cluster",
                org_name="org",
                balance=Balance(credits=Decimal(10)),
                quota=Quota(),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_cluster = await client.charge_org_cluster(
                cluster_name="cluster", org_name="org", amount=Decimal(15)
            )
            assert org_cluster.balance.credits == Decimal(-5)
            assert org_cluster.balance.spent_credits == Decimal(15)

    async def test_org_user_add_spending(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.org_users = [
            OrgUser(
                org_name="org",
                user_name="test1",
                balance=Balance(credits=Decimal(10)),
                role=OrgUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster_user = await client.charge_org_user(
                org_name="org", user_name="test1", amount=Decimal(15)
            )
            assert cluster_user.balance.credits == Decimal(-5)
            assert cluster_user.balance.spent_credits == Decimal(15)

    async def test_org_add_spending(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
                balance=Balance(credits=Decimal(10)),
            )
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org = await client.charge_org(org_name="org", amount=Decimal(15))
            assert org.balance.credits == Decimal(-5)
            assert org.balance.spent_credits == Decimal(15)

    async def test_org_add_balance_delta(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
                balance=Balance(credits=Decimal(10)),
            )
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org = await client.update_org_balance_by_delta(
                org_name="org", delta=Decimal(15)
            )
            assert org.balance.credits == Decimal(25)
            assert org.balance.spent_credits == Decimal(0)

            org = await client.update_org_balance_by_delta(
                org_name="org", delta=Decimal(-30)
            )
            assert org.balance.credits == Decimal(-5)
            assert org.balance.spent_credits == Decimal(0)

    async def test_patch_cluster_user_with_org_quota(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.cluster_users = [
            ClusterUser(
                user_name="test1",
                cluster_name="cluster",
                org_name="org",
                balance=Balance(),
                quota=Quota(total_running_jobs=10),
                role=ClusterUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            cluster_user = await client.update_cluster_user_quota(
                cluster_name="cluster",
                user_name="test1",
                org_name="org",
                quota=Quota(total_running_jobs=15),
            )
            assert cluster_user.quota.total_running_jobs == 15

            cluster_user = await client.update_cluster_user_quota_by_delta(
                cluster_name="cluster",
                user_name="test1",
                org_name="org",
                delta=Quota(total_running_jobs=10),
            )
            assert cluster_user.quota.total_running_jobs == 25

    async def test_patch_org_user_with_org_balance(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
        ]
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.org_users = [
            OrgUser(
                user_name="test1",
                org_name="org",
                balance=Balance(credits=Decimal(10)),
                role=OrgUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_user = await client.update_org_user_balance(
                user_name="test1",
                org_name="org",
                credits=Decimal(15),
            )
            assert org_user.balance.credits == Decimal(15)

            org_user = await client.update_org_user_balance_by_delta(
                user_name="test1",
                org_name="org",
                delta=Decimal(10),
            )
            assert org_user.balance.credits == Decimal(25)

    async def test_cluster_user_add_debt(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.add_debt(
                cluster_name="cluster",
                org_name="org",
                user_name="user",
                credits=Decimal(15),
                idempotency_key="test",
            )

            assert mock_admin_server.debts[0].cluster_name == "cluster"
            assert mock_admin_server.debts[0].org_name == "org"
            assert mock_admin_server.debts[0].user_name == "user"
            assert mock_admin_server.debts[0].credits == Decimal(15)

    async def test_patch_org_cluster_defaults(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.org_clusters = [
            OrgCluster(
                org_name="org",
                cluster_name="cluster",
                balance=Balance(),
                quota=Quota(total_running_jobs=10),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_cluster = await client.update_org_cluster_defaults(
                cluster_name="cluster",
                org_name="org",
                default_quota=Quota(total_running_jobs=20),
                default_credits=Decimal(42),
                default_role=ClusterUserRoleType.MEMBER,
            )
            assert org_cluster.default_quota.total_running_jobs == 20
            assert org_cluster.default_credits == Decimal(42)
            assert org_cluster.default_role == ClusterUserRoleType.MEMBER

            server_org_cluster = mock_admin_server.org_clusters[0]
            assert org_cluster == server_org_cluster

    async def test_patch_org_cluster_quota(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.org_clusters = [
            OrgCluster(
                org_name="org",
                cluster_name="cluster",
                balance=Balance(),
                quota=Quota(total_running_jobs=10),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_cluster = await client.update_org_cluster_quota(
                cluster_name="cluster",
                org_name="org",
                quota=Quota(total_running_jobs=15),
            )
            assert org_cluster.quota.total_running_jobs == 15

            org_cluster = await client.update_org_cluster_quota_by_delta(
                cluster_name="cluster",
                org_name="org",
                delta=Quota(total_running_jobs=10),
            )
            assert org_cluster.quota.total_running_jobs == 25

    async def test_patch_org_cluster_balance(
        self, mock_admin_server: AdminServer
    ) -> None:
        mock_admin_server.orgs = [
            Org(
                name="org",
            ),
        ]
        mock_admin_server.clusters = [
            Cluster(
                name="cluster",
                default_credits=None,
                default_quota=Quota(),
                default_role=ClusterUserRoleType.USER,
            ),
        ]
        mock_admin_server.org_clusters = [
            OrgCluster(
                org_name="org",
                cluster_name="cluster",
                balance=Balance(credits=Decimal(10)),
                quota=Quota(),
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_cluster = await client.update_org_cluster_balance(
                cluster_name="cluster", org_name="org", credits=Decimal(15)
            )
            assert org_cluster.balance.credits == Decimal(15)

            org_cluster = await client.update_org_cluster_balance_by_delta(
                cluster_name="cluster", org_name="org", delta=Decimal(10)
            )
            assert org_cluster.balance.credits == Decimal(25)

    async def test_create_project_minimal(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_project(
                name="name", cluster_name="cluster", org_name=None
            )

        assert len(mock_admin_server.projects) == 1
        project = mock_admin_server.projects[0]
        assert project.name == "name"
        assert project.cluster_name == "cluster"
        assert project.org_name is None
        assert not project.is_default
        assert project.default_role == ProjectUserRoleType.WRITER

    async def test_create_project_full(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_project(
                name="name",
                cluster_name="cluster",
                org_name="org",
                is_default=True,
                default_role=ProjectUserRoleType.READER,
            )

        assert len(mock_admin_server.projects) == 1
        project = mock_admin_server.projects[0]
        assert project.name == "name"
        assert project.cluster_name == "cluster"
        assert project.org_name == "org"
        assert project.is_default
        assert project.default_role == ProjectUserRoleType.READER

    async def test_update_project(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            project = await client.create_project(
                name="name",
                cluster_name="cluster",
                org_name="org",
            )
            project = replace(
                project, is_default=True, default_role=ProjectUserRoleType.READER
            )
            await client.update_project(project)

        assert len(mock_admin_server.projects) == 1
        project = mock_admin_server.projects[0]
        assert project.name == "name"
        assert project.cluster_name == "cluster"
        assert project.org_name == "org"
        assert project.is_default
        assert project.default_role == ProjectUserRoleType.READER

    async def test_list_projects(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.projects = [
            Project(
                name="name",
                cluster_name="cluster",
                org_name=None,
            ),
            Project(
                name="name2",
                cluster_name="cluster",
                org_name="org",
                is_default=True,
                default_role=ProjectUserRoleType.READER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            projects = await client.list_projects(cluster_name="cluster", org_name=None)

            assert len(projects) == 1
            assert set(projects) == {mock_admin_server.projects[0]}

            projects = await client.list_projects(
                cluster_name="cluster", org_name="org"
            )

            assert len(projects) == 1
            assert set(projects) == {mock_admin_server.projects[1]}

    async def test_get_project(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.projects = [
            Project(
                name="name",
                cluster_name="cluster",
                org_name=None,
            ),
            Project(
                name="name2",
                cluster_name="cluster",
                org_name="org",
                is_default=True,
                default_role=ProjectUserRoleType.READER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            project = await client.get_project(
                project_name="name", cluster_name="cluster", org_name=None
            )
            assert project == mock_admin_server.projects[0]

            project = await client.get_project(
                project_name="name2", cluster_name="cluster", org_name="org"
            )
            assert project == mock_admin_server.projects[1]

    async def test_delete_project(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.projects = [
            Project(
                name="name",
                cluster_name="cluster",
                org_name=None,
            ),
            Project(
                name="name2",
                cluster_name="cluster",
                org_name="org",
                is_default=True,
                default_role=ProjectUserRoleType.READER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.delete_project(
                project_name="name", cluster_name="cluster", org_name=None
            )

            with pytest.raises(ClientResponseError):
                await client.get_project(
                    project_name="name", cluster_name="cluster", org_name=None
                )

    async def test_create_project_user(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_user(name="test_user", email="email")
            res_user_with_info = await client.create_project_user(
                project_name="proj",
                cluster_name="cluster",
                org_name="org",
                user_name="test_user",
                role=ProjectUserRoleType.READER,
                with_user_info=True,
            )
            res_user = await client.get_project_user(
                project_name="proj",
                cluster_name="cluster",
                org_name="org",
                user_name="test_user",
            )

        assert res_user.org_name == "org"
        assert res_user.cluster_name == "cluster"
        assert res_user.project_name == "proj"
        assert res_user.user_name == "test_user"
        assert res_user.role == ProjectUserRoleType.READER
        assert res_user_with_info.user_info.email == "email"

        assert mock_admin_server.project_users == [res_user]

    async def test_update_project_user(self, mock_admin_server: AdminServer) -> None:
        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.create_user(name="test_user", email="email")
            res_user = await client.create_project_user(
                project_name="proj",
                cluster_name="cluster",
                org_name="org",
                user_name="test_user",
            )
            res_user = replace(res_user, role=ProjectUserRoleType.MANAGER)
            await client.update_project_user(res_user)
            res_user = await client.get_project_user(
                project_name="proj",
                cluster_name="cluster",
                org_name="org",
                user_name="test_user",
            )

        assert res_user.role == ProjectUserRoleType.MANAGER

        assert mock_admin_server.project_users == [res_user]

    async def test_list_project_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.project_users = [
            ProjectUser(
                project_name="proj",
                cluster_name="cluster",
                user_name="test1",
                org_name="org",
                role=ProjectUserRoleType.READER,
            ),
            ProjectUser(
                project_name="proj",
                cluster_name="cluster",
                user_name="test2",
                org_name=None,
                role=ProjectUserRoleType.READER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            users = await client.list_project_users(
                cluster_name="cluster", org_name="org", project_name="proj"
            )

            assert len(users) == 1
            assert set(users) == {mock_admin_server.project_users[0]}

            users = await client.list_project_users(
                cluster_name="cluster", org_name=None, project_name="proj"
            )

            assert len(users) == 1
            assert set(users) == {mock_admin_server.project_users[1]}

    async def test_get_project_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.project_users = [
            ProjectUser(
                project_name="proj",
                cluster_name="cluster",
                user_name="test1",
                org_name="org",
                role=ProjectUserRoleType.READER,
            ),
            ProjectUser(
                project_name="proj",
                cluster_name="cluster",
                user_name="test2",
                org_name=None,
                role=ProjectUserRoleType.READER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            org_user = await client.get_project_user(
                cluster_name="cluster",
                org_name="org",
                project_name="proj",
                user_name="test1",
            )
            assert org_user == mock_admin_server.project_users[0]

            org_user = await client.get_project_user(
                cluster_name="cluster",
                org_name=None,
                project_name="proj",
                user_name="test2",
            )
            assert org_user == mock_admin_server.project_users[1]

    async def test_delete_project_user(self, mock_admin_server: AdminServer) -> None:
        mock_admin_server.users = [
            User(
                name="test1",
                email="email",
            ),
            User(
                name="test2",
                email="email",
            ),
        ]
        mock_admin_server.project_users = [
            ProjectUser(
                project_name="proj",
                cluster_name="cluster",
                user_name="test1",
                org_name="org",
                role=ProjectUserRoleType.READER,
            ),
            ProjectUser(
                project_name="proj",
                cluster_name="cluster",
                user_name="test2",
                org_name=None,
                role=ProjectUserRoleType.READER,
            ),
        ]

        async with AdminClient(base_url=mock_admin_server.url) as client:
            await client.delete_project_user(
                cluster_name="cluster",
                org_name="org",
                project_name="proj",
                user_name="test1",
            )
            assert len(mock_admin_server.project_users) == 1
            assert mock_admin_server.project_users[0].user_name == "test2"
