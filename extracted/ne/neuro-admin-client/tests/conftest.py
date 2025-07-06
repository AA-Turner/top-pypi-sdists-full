from __future__ import annotations

import asyncio
import datetime
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass, field, replace
from decimal import Decimal
from typing import Any

import aiohttp
import aiohttp.web
import pytest
from yarl import URL

from neuro_admin_client import (
    Balance,
    Cluster,
    ClusterUser,
    ClusterUserRoleType,
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


@dataclass
class ApiAddress:
    host: str
    port: int


@dataclass(frozen=True)
class Debt:
    cluster_name: str
    org_name: str | None
    user_name: str | None
    credits: Decimal


def _parse_bool(value: str) -> bool:
    value = value.lower()
    return value in ("1", "true", "yes")


@dataclass()
class AdminServer:
    address: ApiAddress | None = None

    users: list[User] = field(default_factory=list)
    clusters: list[Cluster] = field(default_factory=list)
    orgs: list[Org] = field(default_factory=list)
    cluster_users: list[ClusterUser] = field(default_factory=list)
    org_clusters: list[OrgCluster] = field(default_factory=list)
    org_users: list[OrgUser] = field(default_factory=list)
    debts: list[Debt] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    project_users: list[ProjectUser] = field(default_factory=list)

    last_skip_auto_add_to_clusters: bool = False

    @property
    def url(self) -> URL:
        assert self.address
        return URL(f"http://{self.address.host}:{self.address.port}/api/v1/")

    def _serialize_user(self, user: User) -> dict[str, Any]:
        return {
            "name": user.name,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    def _serialize_user_org(self, user: OrgUser) -> dict[str, Any]:
        res = self._serialize_org_user(user, False)
        res.pop("user_name")
        return res

    def _serialize_user_cluster(self, user: ClusterUser) -> dict[str, Any]:
        res = self._serialize_cluster_user(user, False)
        res.pop("user_name")
        res["cluster_name"] = user.cluster_name
        return res

    def _serialize_user_project(self, user: ProjectUser) -> dict[str, Any]:
        res = self._serialize_project_user(user, False)
        res.pop("user_name")
        return res

    async def handle_user_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        payload = await request.json()
        new_user = User(
            name=payload["name"],
            email=payload["email"],
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            created_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.users.append(new_user)
        self.last_skip_auto_add_to_clusters = _parse_bool(
            request.query.get("skip_auto_add_to_clusters", "false")
        )
        return aiohttp.web.json_response(self._serialize_user(new_user))

    async def handle_user_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        user_name = request.match_info["uname"]
        for user in self.users:
            if user.name == user_name:
                payload = self._serialize_user(user)
                if "orgs" in request.query.getall("include", []):
                    payload["orgs"] = [
                        self._serialize_user_org(org_user)
                        for org_user in self.org_users
                        if org_user.user_name == user_name
                    ]
                if "clusters" in request.query.getall("include", []):
                    payload["clusters"] = [
                        self._serialize_user_cluster(cluster_user)
                        for cluster_user in self.cluster_users
                        if cluster_user.user_name == user_name
                    ]
                if "projects" in request.query.getall("include", []):
                    payload["projects"] = [
                        self._serialize_user_project(project_user)
                        for project_user in self.project_users
                        if project_user.user_name == user_name
                    ]
                return aiohttp.web.json_response(payload)
        raise aiohttp.web.HTTPNotFound

    async def handle_user_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        resp = [self._serialize_user(user) for user in self.users]
        return aiohttp.web.json_response(resp)

    def _serialize_org(self, org: Org) -> dict[str, Any]:
        res: dict[str, Any] = {
            "name": org.name,
            "balance": {
                "spent_credits": str(org.balance.spent_credits),
            },
        }
        if org.balance.credits is not None:
            res["balance"]["credits"] = str(org.balance.credits)
        if org.user_default_credits:
            res["user_default_credits"] = str(org.user_default_credits)
        if org.notification_intervals:
            res["notification_intervals"] = asdict(org.notification_intervals)
        return res

    async def handle_org_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        payload = await request.json()
        user_default_credits_raw = payload.get("user_default_credits")
        new_org = Org(
            name=payload["name"],
            user_default_credits=(
                Decimal(user_default_credits_raw) if user_default_credits_raw else None
            ),
        )
        self.orgs.append(new_org)
        self.last_skip_auto_add_to_clusters = _parse_bool(
            request.query.get("skip_auto_add_to_clusters", "false")
        )
        return aiohttp.web.json_response(self._serialize_org(new_org))

    async def handle_org_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        for org in self.orgs:
            if org.name == org_name:
                return aiohttp.web.json_response(self._serialize_org(org))
        raise aiohttp.web.HTTPNotFound

    async def handle_org_delete(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        for idx, org in enumerate(self.orgs):
            if org.name == org_name:
                del self.orgs[idx]
                return aiohttp.web.json_response(self._serialize_org(org))
        raise aiohttp.web.HTTPNotFound

    async def handle_org_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        resp = [self._serialize_org(org) for org in self.orgs]
        return aiohttp.web.json_response(resp)

    async def handle_org_patch_balance(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        payload = await request.json()

        for index, org in enumerate(self.orgs):
            if org.name == org_name:
                balance = org.balance
                if "credits" in payload:
                    credits = (
                        Decimal(payload["credits"]) if payload["credits"] else None
                    )
                    balance = replace(balance, credits=credits)
                if payload.get("additional_credits") and balance.credits is not None:
                    additional_credits = Decimal(payload["additional_credits"])
                    balance = replace(
                        balance, credits=balance.credits + additional_credits
                    )
                org = replace(org, balance=balance)
                self.orgs[index] = org
                return aiohttp.web.json_response(self._serialize_org(org))
        raise aiohttp.web.HTTPNotFound

    async def handle_org_add_spending(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        payload = await request.json()

        for index, org in enumerate(self.orgs):
            if org.name == org_name:
                balance = org.balance
                spending = Decimal(payload["spending"])
                balance = replace(
                    balance, spent_credits=balance.spent_credits + spending
                )
                if balance.credits:
                    balance = replace(balance, credits=balance.credits - spending)
                org = replace(org, balance=balance)
                self.orgs[index] = org
                return aiohttp.web.json_response(self._serialize_org(org))
        raise aiohttp.web.HTTPNotFound

    async def handle_org_patch_defaults(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        payload = await request.json()

        for index, org in enumerate(self.orgs):
            if org.name == org_name:
                user_default_credits_raw = payload.get("credits")
                org = replace(
                    org,
                    user_default_credits=(
                        Decimal(user_default_credits_raw)
                        if user_default_credits_raw
                        else None
                    ),
                )
                notification_intervals = payload.get("notification_intervals")
                if notification_intervals:
                    notification_intervals = OrgNotificationIntervals(
                        **payload["notification_intervals"]
                    )
                    org = replace(
                        org,
                        notification_intervals=notification_intervals,
                    )
                self.orgs[index] = org
                return aiohttp.web.json_response(self._serialize_org(org))
        raise aiohttp.web.HTTPNotFound

    def _serialize_cluster(self, cluster: Cluster) -> dict[str, Any]:
        resp: dict[str, Any] = {
            "name": cluster.name,
            "default_quota": {},
            "default_role": str(cluster.default_role),
            "maintenance": cluster.maintenance,
        }
        if cluster.default_credits:
            resp["default_credits"] = str(cluster.default_credits)
        if cluster.default_quota.total_running_jobs:
            resp["default_quota"][
                "total_running_jobs"
            ] = cluster.default_quota.total_running_jobs
        return resp

    def _int_or_none(self, value: str | None) -> int | None:
        if value:
            return int(value)
        return None

    async def handle_cluster_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        payload = await request.json()
        default_credits_raw = payload.get("default_credits")
        default_quota_raw = payload.get("default_quota", {})
        new_cluster = Cluster(
            name=payload["name"],
            default_credits=(
                Decimal(default_credits_raw) if default_credits_raw else None
            ),
            default_quota=Quota(
                total_running_jobs=self._int_or_none(
                    default_quota_raw.get("total_running_jobs")
                )
            ),
            default_role=ClusterUserRoleType(
                payload.get("default_role", ClusterUserRoleType.USER.value)
            ),
            maintenance=payload.get("maintenance", False),
        )
        self.clusters.append(new_cluster)
        return aiohttp.web.json_response(self._serialize_cluster(new_cluster))

    async def handle_cluster_put(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        payload = await request.json()

        assert cluster_name == payload["name"]

        default_credits_raw = payload.get("default_credits")
        default_quota_raw = payload.get("default_quota", {})
        changed_cluster = Cluster(
            name=payload["name"],
            default_credits=(
                Decimal(default_credits_raw) if default_credits_raw else None
            ),
            default_quota=Quota(
                total_running_jobs=self._int_or_none(
                    default_quota_raw.get("total_running_jobs")
                )
            ),
            default_role=ClusterUserRoleType(
                payload.get("default_role", ClusterUserRoleType.USER.value)
            ),
            maintenance=payload.get("maintenance", False),
        )
        self.clusters = [
            cluster for cluster in self.clusters if cluster.name != changed_cluster.name
        ]
        self.clusters.append(changed_cluster)
        return aiohttp.web.json_response(self._serialize_cluster(changed_cluster))

    async def handle_cluster_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        for cluster in self.clusters:
            if cluster.name == cluster_name:
                return aiohttp.web.json_response(self._serialize_cluster(cluster))
        raise aiohttp.web.HTTPNotFound

    async def handle_cluster_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        resp = [self._serialize_cluster(cluster) for cluster in self.clusters]
        return aiohttp.web.json_response(resp)

    async def handle_cluster_delete(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        for idx, cluster in enumerate(self.clusters):
            if cluster.name == cluster_name:
                del self.clusters[idx]
                return aiohttp.web.json_response(self._serialize_cluster(cluster))
        raise aiohttp.web.HTTPNotFound

    def _serialize_cluster_user(
        self,
        cluster_user: ClusterUser,
        with_info: bool,
        only_usernames: bool = False,
    ) -> dict[str, Any]:
        if only_usernames:
            return {"user_name": cluster_user.user_name}
        res: dict[str, Any] = {
            "user_name": cluster_user.user_name,
            "org_name": cluster_user.org_name,
            "quota": {},
            "balance": {
                "spent_credits": str(cluster_user.balance.spent_credits),
            },
        }
        if cluster_user.role:
            res["role"] = cluster_user.role.value
        if cluster_user.quota.total_running_jobs is not None:
            res["quota"]["total_running_jobs"] = cluster_user.quota.total_running_jobs
        if cluster_user.balance.credits is not None:
            res["balance"]["credits"] = str(cluster_user.balance.credits)
        if with_info:
            user = next(
                user for user in self.users if user.name == cluster_user.user_name
            )
            res["user_info"] = self._serialize_user(user)
            res["user_info"].pop("name")
        return res

    async def handle_cluster_user_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        payload = await request.json()
        new_cluster_user = ClusterUser(
            cluster_name=cluster_name,
            user_name=payload["user_name"],
            role=ClusterUserRoleType(payload["role"]),
            org_name=payload.get("org_name"),
            balance=Balance(),
            quota=Quota(total_running_jobs=payload["quota"].get("total_running_jobs")),
        )
        self.cluster_users.append(new_cluster_user)
        return aiohttp.web.json_response(
            self._serialize_cluster_user(
                new_cluster_user,
                _parse_bool(request.query.get("with_user_info", "false")),
            )
        )

    async def handle_cluster_user_put(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        user_name = request.match_info["uname"]
        org_name = request.match_info.get("oname")
        payload = await request.json()
        credits_raw = payload.get("balance", {}).get("credits")
        spend_credits_raw = payload.get("balance", {}).get("spend_credits_raw")

        assert user_name == payload["user_name"]
        assert org_name == payload.get("org_name")

        new_cluster_user = ClusterUser(
            cluster_name=cluster_name,
            user_name=payload["user_name"],
            role=ClusterUserRoleType(payload["role"]),
            org_name=payload.get("org_name"),
            quota=Quota(total_running_jobs=payload["quota"].get("total_running_jobs")),
            balance=Balance(
                credits=Decimal(credits_raw) if credits_raw else None,
                spent_credits=(
                    Decimal(spend_credits_raw) if spend_credits_raw else Decimal(0)
                ),
            ),
        )
        assert new_cluster_user.user_name == user_name
        self.cluster_users = [
            user
            for user in self.cluster_users
            if user.cluster_name != cluster_name
            or user.user_name != user_name
            or user.org_name != org_name
        ]
        self.cluster_users.append(new_cluster_user)
        return aiohttp.web.json_response(
            self._serialize_cluster_user(
                new_cluster_user,
                _parse_bool(request.query.get("with_user_info", "false")),
            )
        )

    async def handle_cluster_user_patch_quota(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        user_name = request.match_info["uname"]
        org_name = request.match_info.get("oname")
        payload = await request.json()

        for index, user in enumerate(self.cluster_users):
            if (
                user.cluster_name == cluster_name
                and user.user_name == user_name
                and user.org_name == org_name
            ):
                quota = user.quota
                if "quota" in payload:
                    quota = replace(
                        quota,
                        total_running_jobs=payload["quota"].get("total_running_jobs"),
                    )
                if (
                    "additional_quota" in payload
                    and quota.total_running_jobs is not None
                ):
                    quota = replace(
                        quota,
                        total_running_jobs=quota.total_running_jobs
                        + payload["additional_quota"].get("total_running_jobs"),
                    )
                user = replace(user, quota=quota)
                self.cluster_users[index] = user
                return aiohttp.web.json_response(
                    self._serialize_cluster_user(
                        user,
                        _parse_bool(request.query.get("with_user_info", "false")),
                    )
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_org_user_patch_balance(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        user_name = request.match_info["uname"]
        payload = await request.json()

        for index, user in enumerate(self.org_users):
            if user.user_name == user_name and user.org_name == org_name:
                balance = user.balance
                if "credits" in payload:
                    credits = (
                        Decimal(payload["credits"]) if payload["credits"] else None
                    )
                    balance = replace(balance, credits=credits)
                if payload.get("additional_credits") and balance.credits is not None:
                    additional_credits = Decimal(payload["additional_credits"])
                    balance = replace(
                        balance, credits=balance.credits + additional_credits
                    )
                user = replace(user, balance=balance)
                self.org_users[index] = user
                return aiohttp.web.json_response(
                    self._serialize_org_user(
                        user,
                        _parse_bool(request.query.get("with_user_info", "false")),
                    )
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_org_cluster_add_spending(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info["oname"]
        payload = await request.json()

        for index, org_cluster in enumerate(self.org_clusters):
            if (
                org_cluster.cluster_name == cluster_name
                and org_cluster.org_name == org_name
            ):
                balance = org_cluster.balance
                spending = Decimal(payload["spending"])
                balance = replace(
                    balance, spent_credits=balance.spent_credits + spending
                )
                if balance.credits:
                    balance = replace(balance, credits=balance.credits - spending)
                org_cluster = replace(org_cluster, balance=balance)
                self.org_clusters[index] = org_cluster
                return aiohttp.web.json_response(
                    self._serialize_org_cluster(org_cluster)
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_org_user_add_spending(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        user_name = request.match_info["uname"]
        payload = await request.json()

        for index, user in enumerate(self.org_users):
            if user.user_name == user_name and user.org_name == org_name:
                balance = user.balance
                spending = Decimal(payload["spending"])
                balance = replace(
                    balance, spent_credits=balance.spent_credits + spending
                )
                if balance.credits:
                    balance = replace(balance, credits=balance.credits - spending)
                user = replace(user, balance=balance)
                self.org_users[index] = user
                return aiohttp.web.json_response(
                    self._serialize_org_user(
                        user,
                        _parse_bool(request.query.get("with_user_info", "false")),
                    )
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_cluster_user_add_debt(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        payload = await request.json()
        self.debts.append(
            Debt(
                cluster_name=cluster_name,
                org_name=payload.get("org_name"),
                user_name=payload.get("user_name"),
                credits=Decimal(payload["credits"]),
            )
        )
        raise aiohttp.web.HTTPNoContent

    async def handle_cluster_user_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        user_name = request.match_info["uname"]
        org_name = request.match_info.get("oname")
        for cluster_user in self.cluster_users:
            if (
                cluster_user.cluster_name == cluster_name
                and cluster_user.user_name == user_name
                and cluster_user.org_name == org_name
            ):
                return aiohttp.web.json_response(
                    self._serialize_cluster_user(
                        cluster_user,
                        _parse_bool(request.query.get("with_user_info", "false")),
                    )
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_cluster_user_delete(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        user_name = request.match_info["uname"]
        org_name = request.match_info.get("oname")
        for idx, cluster_user in enumerate(self.cluster_users):
            if (
                cluster_user.cluster_name == cluster_name
                and cluster_user.user_name == user_name
                and cluster_user.org_name == org_name
            ):
                del self.cluster_users[idx]
                raise aiohttp.web.HTTPNoContent
        raise aiohttp.web.HTTPNotFound

    async def handle_cluster_user_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        resp = [
            self._serialize_cluster_user(
                cluster_user,
                _parse_bool(request.query.get("with_user_info", "false")),
                _parse_bool(request.query.get("only_usernames", "false")),
            )
            for cluster_user in self.cluster_users
            if cluster_user.cluster_name == cluster_name
            and (org_name is None or cluster_user.org_name == org_name)
        ]
        return aiohttp.web.json_response(resp)

    def _serialize_org_user(self, org_user: OrgUser, with_info: bool) -> dict[str, Any]:
        res: dict[str, Any] = {
            "user_name": org_user.user_name,
            "role": org_user.role.value,
            "org_name": org_user.org_name,
            "balance": {
                "spent_credits": str(org_user.balance.spent_credits),
            },
        }
        if org_user.balance.credits is not None:
            res["balance"]["credits"] = str(org_user.balance.credits)
        if with_info:
            user = next(user for user in self.users if user.name == org_user.user_name)
            res["user_info"] = self._serialize_user(user)
            res["user_info"].pop("name")
        return res

    async def handle_org_user_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        payload = await request.json()
        credits_raw = payload["balance"].get("credits")
        spend_credits_raw = payload["balance"].get("spend_credits_raw")
        new_org_user = OrgUser(
            org_name=org_name,
            user_name=payload["user_name"],
            role=OrgUserRoleType(payload["role"]),
            balance=Balance(
                credits=Decimal(credits_raw) if credits_raw else None,
                spent_credits=(
                    Decimal(spend_credits_raw) if spend_credits_raw else Decimal(0)
                ),
            ),
        )
        self.org_users.append(new_org_user)
        return aiohttp.web.json_response(
            self._serialize_org_user(
                new_org_user,
                _parse_bool(request.query.get("with_user_info", "false")),
            )
        )

    async def handle_org_user_put(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        user_name = request.match_info["uname"]
        payload = await request.json()
        credits_raw = payload["balance"].get("credits")
        spend_credits_raw = payload["balance"].get("spend_credits_raw")
        new_org_user = OrgUser(
            org_name=org_name,
            user_name=payload["user_name"],
            role=OrgUserRoleType(payload["role"]),
            balance=Balance(
                credits=Decimal(credits_raw) if credits_raw else None,
                spent_credits=(
                    Decimal(spend_credits_raw) if spend_credits_raw else Decimal(0)
                ),
            ),
        )
        assert new_org_user.user_name == user_name
        self.org_users = [
            user
            for user in self.org_users
            if user.org_name != org_name or user.user_name != user_name
        ]
        self.org_users.append(new_org_user)
        return aiohttp.web.json_response(
            self._serialize_org_user(
                new_org_user,
                _parse_bool(request.query.get("with_user_info", "false")),
            )
        )

    async def handle_org_user_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        user_name = request.match_info["uname"]
        for org_user in self.org_users:
            if org_user.org_name == org_name and org_user.user_name == user_name:
                return aiohttp.web.json_response(
                    self._serialize_org_user(
                        org_user,
                        _parse_bool(request.query.get("with_user_info", "false")),
                    )
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_org_user_delete(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        user_name = request.match_info["uname"]
        for idx, org_user in enumerate(self.org_users):
            if org_user.org_name == org_name and org_user.user_name == user_name:
                del self.org_users[idx]
                raise aiohttp.web.HTTPNoContent
        raise aiohttp.web.HTTPNotFound

    async def handle_org_user_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        org_name = request.match_info["oname"]
        roles = {OrgUserRoleType(r) for r in request.query.getall("roles", [])}
        resp = [
            self._serialize_org_user(
                org_user, _parse_bool(request.query.get("with_user_info", "false"))
            )
            for org_user in self.org_users
            if org_user.org_name == org_name and (not roles or org_user.role in roles)
        ]
        return aiohttp.web.json_response(resp)

    def _serialize_org_cluster(self, org_cluster: OrgCluster) -> dict[str, Any]:
        res: dict[str, Any] = {
            "org_name": org_cluster.org_name,
            "quota": {},
            "balance": {
                "spent_credits": str(org_cluster.balance.spent_credits),
            },
            "default_quota": {},
            "default_role": str(org_cluster.default_role),
            "maintenance": org_cluster.maintenance,
        }
        if org_cluster.quota.total_running_jobs is not None:
            res["quota"]["total_running_jobs"] = org_cluster.quota.total_running_jobs
        if org_cluster.balance.credits is not None:
            res["balance"]["credits"] = str(org_cluster.balance.credits)
        if org_cluster.default_credits:
            res["default_credits"] = str(org_cluster.default_credits)
        if org_cluster.default_quota.total_running_jobs:
            res["default_quota"][
                "total_running_jobs"
            ] = org_cluster.default_quota.total_running_jobs
        if org_cluster.storage_size is not None:
            res["storage_size"] = org_cluster.storage_size
        return res

    async def handle_org_cluster_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        payload = await request.json()
        credits_raw = payload.get("balance", {}).get("credits")
        default_credits_raw = payload.get("default_credits")
        spend_credits_raw = payload.get("balance", {}).get("spend_credits_raw")
        new_org_cluster = OrgCluster(
            cluster_name=cluster_name,
            org_name=payload["org_name"],
            quota=Quota(
                total_running_jobs=payload.get("quota", {}).get("total_running_jobs")
            ),
            balance=Balance(
                credits=Decimal(credits_raw) if credits_raw else None,
                spent_credits=(
                    Decimal(spend_credits_raw) if spend_credits_raw else Decimal(0)
                ),
            ),
            default_quota=Quota(
                total_running_jobs=payload.get("default_quota", {}).get(
                    "total_running_jobs"
                )
            ),
            default_credits=(
                Decimal(default_credits_raw) if default_credits_raw else None
            ),
            default_role=ClusterUserRoleType(
                payload.get("default_role", ClusterUserRoleType.USER.value)
            ),
            storage_size=payload.get("storage_size"),
            maintenance=payload.get("maintenance", False),
        )
        self.org_clusters.append(new_org_cluster)
        return aiohttp.web.json_response(
            self._serialize_org_cluster(
                new_org_cluster,
            )
        )

    async def handle_org_cluster_put(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info["oname"]
        payload = await request.json()
        credits_raw = payload.get("balance", {}).get("credits")
        default_credits_raw = payload.get("default_credits")
        spend_credits_raw = payload.get("balance", {}).get("spend_credits_raw")
        new_org_cluster = OrgCluster(
            cluster_name=cluster_name,
            org_name=payload["org_name"],
            quota=Quota(
                total_running_jobs=payload.get("quota", {}).get("total_running_jobs")
            ),
            balance=Balance(
                credits=Decimal(credits_raw) if credits_raw else None,
                spent_credits=(
                    Decimal(spend_credits_raw) if spend_credits_raw else Decimal(0)
                ),
            ),
            default_quota=Quota(
                total_running_jobs=payload.get("default_quota", {}).get(
                    "total_running_jobs"
                )
            ),
            default_credits=(
                Decimal(default_credits_raw) if default_credits_raw else None
            ),
            default_role=ClusterUserRoleType(
                payload.get("default_role", ClusterUserRoleType.USER.value)
            ),
            maintenance=payload["maintenance"],
        )
        assert new_org_cluster.org_name == org_name
        self.org_clusters = [
            user
            for user in self.org_clusters
            if user.cluster_name != cluster_name or user.org_name != org_name
        ]
        self.org_clusters.append(new_org_cluster)
        return aiohttp.web.json_response(
            self._serialize_org_cluster(
                new_org_cluster,
            )
        )

    async def handle_org_cluster_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info["oname"]
        for org_cluster in self.org_clusters:
            if (
                org_cluster.cluster_name == cluster_name
                and org_cluster.org_name == org_name
            ):
                return aiohttp.web.json_response(
                    self._serialize_org_cluster(org_cluster)
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_org_cluster_delete(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info["oname"]
        for idx, org_cluster in enumerate(self.org_clusters):
            if (
                org_cluster.cluster_name == cluster_name
                and org_cluster.org_name == org_name
            ):
                del self.org_clusters[idx]
                raise aiohttp.web.HTTPNoContent
        raise aiohttp.web.HTTPNotFound

    async def handle_org_cluster_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        resp = [
            self._serialize_org_cluster(org_cluster)
            for org_cluster in self.org_clusters
            if org_cluster.cluster_name == cluster_name
        ]
        return aiohttp.web.json_response(resp)

    async def handle_org_cluster_patch_defaults(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info["oname"]
        payload = await request.json()

        for index, org_cluster in enumerate(self.org_clusters):
            if (
                org_cluster.cluster_name == cluster_name
                and org_cluster.org_name == org_name
            ):
                default_credits_raw = payload.get("credits")
                org_cluster = replace(
                    org_cluster,
                    default_quota=Quota(
                        total_running_jobs=payload.get("quota", {}).get(
                            "total_running_jobs"
                        )
                    ),
                    default_credits=(
                        Decimal(default_credits_raw) if default_credits_raw else None
                    ),
                    default_role=ClusterUserRoleType(
                        payload.get("default_role", ClusterUserRoleType.USER.value)
                    ),
                )
                self.org_clusters[index] = org_cluster
                return aiohttp.web.json_response(
                    self._serialize_org_cluster(org_cluster)
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_org_cluster_patch_quota(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info["oname"]
        payload = await request.json()

        for index, org_cluster in enumerate(self.org_clusters):
            if (
                org_cluster.cluster_name == cluster_name
                and org_cluster.org_name == org_name
            ):
                quota = org_cluster.quota
                if "quota" in payload:
                    quota = replace(
                        quota,
                        total_running_jobs=payload["quota"].get("total_running_jobs"),
                    )
                if (
                    "additional_quota" in payload
                    and quota.total_running_jobs is not None
                ):
                    quota = replace(
                        quota,
                        total_running_jobs=quota.total_running_jobs
                        + payload["additional_quota"].get("total_running_jobs"),
                    )
                org_cluster = replace(org_cluster, quota=quota)
                self.org_clusters[index] = org_cluster
                return aiohttp.web.json_response(
                    self._serialize_org_cluster(org_cluster)
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_org_cluster_patch_balance(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info["oname"]
        payload = await request.json()

        for index, org_cluster in enumerate(self.org_clusters):
            if (
                org_cluster.cluster_name == cluster_name
                and org_cluster.org_name == org_name
            ):
                balance = org_cluster.balance
                if "credits" in payload:
                    credits = (
                        Decimal(payload["credits"]) if payload["credits"] else None
                    )
                    balance = replace(balance, credits=credits)
                if payload.get("additional_credits") and balance.credits is not None:
                    additional_credits = Decimal(payload["additional_credits"])
                    balance = replace(
                        balance, credits=balance.credits + additional_credits
                    )
                org_cluster = replace(org_cluster, balance=balance)
                self.org_clusters[index] = org_cluster
                return aiohttp.web.json_response(
                    self._serialize_org_cluster(
                        org_cluster,
                    )
                )
        raise aiohttp.web.HTTPNotFound

    def _serialize_project(self, project: Project) -> dict[str, Any]:
        return {
            "name": project.name,
            "cluster_name": project.cluster_name,
            "org_name": project.org_name,
            "is_default": project.is_default,
            "default_role": project.default_role.value,
        }

    async def handle_project_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")

        payload = await request.json()
        new_project = Project(
            name=payload["name"],
            cluster_name=cluster_name,
            org_name=org_name,
            is_default=payload.get("is_default", False),
            default_role=ProjectUserRoleType(
                payload.get("default_role", ProjectUserRoleType.WRITER.value)
            ),
        )
        self.projects.append(new_project)
        return aiohttp.web.json_response(self._serialize_project(new_project))

    async def handle_project_put(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]
        payload = await request.json()

        changed_project = Project(
            name=project_name,
            cluster_name=cluster_name,
            org_name=org_name,
            is_default=payload["is_default"],
            default_role=ProjectUserRoleType(payload["default_role"]),
        )

        self.projects = [
            it
            for it in self.projects
            if it.name != project_name
            or it.cluster_name != cluster_name
            or it.org_name != org_name
        ]
        self.projects.append(changed_project)
        return aiohttp.web.json_response(self._serialize_project(changed_project))

    async def handle_project_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]
        for project in self.projects:
            if (
                project.name == project_name
                and project.cluster_name == cluster_name
                and project.org_name == org_name
            ):
                return aiohttp.web.json_response(self._serialize_project(project))
        raise aiohttp.web.HTTPNotFound

    async def handle_project_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        resp = [
            self._serialize_project(project)
            for project in self.projects
            if project.cluster_name == cluster_name and project.org_name == org_name
        ]
        return aiohttp.web.json_response(resp)

    async def handle_project_delete(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]

        for idx, project in enumerate(self.projects):
            if (
                project.name == project_name
                and project.cluster_name == cluster_name
                and project.org_name == org_name
            ):
                del self.projects[idx]
                return aiohttp.web.json_response(self._serialize_project(project))
        raise aiohttp.web.HTTPNotFound

    def _serialize_project_user(
        self, project_user: ProjectUser, with_info: bool
    ) -> dict[str, Any]:
        res: dict[str, Any] = {
            "user_name": project_user.user_name,
            "role": project_user.role.value,
            "org_name": project_user.org_name,
            "cluster_name": project_user.cluster_name,
            "project_name": project_user.project_name,
        }
        if with_info:
            user = next(
                user for user in self.users if user.name == project_user.user_name
            )
            res["user_info"] = self._serialize_user(user)
            res["user_info"].pop("name")
        return res

    async def handle_project_user_post(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]

        payload = await request.json()
        new_project_user = ProjectUser(
            org_name=org_name,
            cluster_name=cluster_name,
            project_name=project_name,
            user_name=payload["user_name"],
            role=ProjectUserRoleType(payload.get("role", "writer")),
        )
        self.project_users.append(new_project_user)
        return aiohttp.web.json_response(
            self._serialize_project_user(
                new_project_user,
                _parse_bool(request.query.get("with_user_info", "false")),
            )
        )

    async def handle_project_user_put(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]
        user_name = request.match_info["uname"]
        payload = await request.json()
        project_user = ProjectUser(
            org_name=org_name,
            cluster_name=cluster_name,
            project_name=project_name,
            user_name=user_name,
            role=ProjectUserRoleType(payload["role"]),
        )
        self.project_users = [
            it
            for it in self.project_users
            if it.org_name != org_name
            or it.user_name != user_name
            or it.cluster_name != cluster_name
        ]
        self.project_users.append(project_user)
        return aiohttp.web.json_response(
            self._serialize_project_user(
                project_user,
                _parse_bool(request.query.get("with_user_info", "false")),
            )
        )

    async def handle_project_user_get(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]
        user_name = request.match_info["uname"]
        for project_user in self.project_users:
            if (
                project_user.org_name == org_name
                and project_user.user_name == user_name
                and project_user.cluster_name == cluster_name
                and project_user.project_name == project_name
            ):
                return aiohttp.web.json_response(
                    self._serialize_project_user(
                        project_user,
                        _parse_bool(request.query.get("with_user_info", "false")),
                    )
                )
        raise aiohttp.web.HTTPNotFound

    async def handle_project_user_delete(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]
        user_name = request.match_info["uname"]
        for idx, project_user in enumerate(self.project_users):
            if (
                project_user.org_name == org_name
                and project_user.user_name == user_name
                and project_user.cluster_name == cluster_name
                and project_user.project_name == project_name
            ):
                del self.project_users[idx]
                raise aiohttp.web.HTTPNoContent
        raise aiohttp.web.HTTPNotFound

    async def handle_project_user_list(
        self, request: aiohttp.web.Request
    ) -> aiohttp.web.Response:
        cluster_name = request.match_info["cname"]
        org_name = request.match_info.get("oname")
        project_name = request.match_info["pname"]
        resp = [
            self._serialize_project_user(
                project_user, _parse_bool(request.query.get("with_user_info", "false"))
            )
            for project_user in self.project_users
            if project_user.org_name == org_name
            and project_user.cluster_name == cluster_name
            and project_user.project_name == project_name
        ]
        return aiohttp.web.json_response(resp)


@pytest.fixture
async def mock_admin_server() -> AsyncIterator[AdminServer]:
    admin_server = AdminServer()

    def _create_app() -> aiohttp.web.Application:
        app = aiohttp.web.Application()
        app.router.add_routes(
            (
                aiohttp.web.get(
                    "/api/v1/users",
                    admin_server.handle_user_list,
                ),
                aiohttp.web.post(
                    "/api/v1/users",
                    admin_server.handle_user_post,
                ),
                aiohttp.web.get(
                    "/api/v1/users/{uname}",
                    admin_server.handle_user_get,
                ),
                aiohttp.web.get(
                    "/api/v1/orgs",
                    admin_server.handle_org_list,
                ),
                aiohttp.web.post(
                    "/api/v1/orgs",
                    admin_server.handle_org_post,
                ),
                aiohttp.web.get(
                    "/api/v1/orgs/{oname}",
                    admin_server.handle_org_get,
                ),
                aiohttp.web.delete(
                    "/api/v1/orgs/{oname}",
                    admin_server.handle_org_delete,
                ),
                aiohttp.web.patch(
                    "/api/v1/orgs/{oname}/balance",
                    admin_server.handle_org_patch_balance,
                ),
                aiohttp.web.post(
                    "/api/v1/orgs/{oname}/spending",
                    admin_server.handle_org_add_spending,
                ),
                aiohttp.web.patch(
                    "/api/v1/orgs/{oname}",
                    admin_server.handle_org_patch_defaults,
                ),
                aiohttp.web.patch(
                    "/api/v1/orgs/{oname}/defaults",
                    admin_server.handle_org_patch_defaults,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters",
                    admin_server.handle_cluster_list,
                ),
                aiohttp.web.post(
                    "/api/v1/clusters",
                    admin_server.handle_cluster_post,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}",
                    admin_server.handle_cluster_get,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}",
                    admin_server.handle_cluster_put,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}",
                    admin_server.handle_cluster_delete,
                ),
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/users",
                    admin_server.handle_cluster_user_post,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/users",
                    admin_server.handle_cluster_user_list,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/users/{uname}",
                    admin_server.handle_cluster_user_get,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}/users/{uname}",
                    admin_server.handle_cluster_user_put,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}/users/{uname}",
                    admin_server.handle_cluster_user_delete,
                ),
                aiohttp.web.patch(
                    "/api/v1/clusters/{cname}/users/{uname}/quota",
                    admin_server.handle_cluster_user_patch_quota,
                ),
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/debts",
                    admin_server.handle_cluster_user_add_debt,
                ),
                aiohttp.web.post(
                    "/api/v1/orgs/{oname}/users",
                    admin_server.handle_org_user_post,
                ),
                aiohttp.web.get(
                    "/api/v1/orgs/{oname}/users",
                    admin_server.handle_org_user_list,
                ),
                aiohttp.web.get(
                    "/api/v1/orgs/{oname}/users/{uname}",
                    admin_server.handle_org_user_get,
                ),
                aiohttp.web.put(
                    "/api/v1/orgs/{oname}/users/{uname}",
                    admin_server.handle_org_user_put,
                ),
                aiohttp.web.delete(
                    "/api/v1/orgs/{oname}/users/{uname}",
                    admin_server.handle_org_user_delete,
                ),
                aiohttp.web.patch(
                    "/api/v1/orgs/{oname}/users/{uname}/balance",
                    admin_server.handle_org_user_patch_balance,
                ),
                aiohttp.web.post(
                    "/api/v1/orgs/{oname}/users/{uname}/spending",
                    admin_server.handle_org_user_add_spending,
                ),
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/orgs",
                    admin_server.handle_org_cluster_post,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs",
                    admin_server.handle_org_cluster_list,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs/{oname}",
                    admin_server.handle_org_cluster_get,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}/orgs/{oname}",
                    admin_server.handle_org_cluster_put,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}/orgs/{oname}",
                    admin_server.handle_org_cluster_delete,
                ),
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/orgs/{oname}/spending",
                    admin_server.handle_org_cluster_add_spending,
                ),
                # org user endpoints:
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs/{oname}/users",
                    admin_server.handle_cluster_user_list,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs/{oname}/users/{uname}",
                    admin_server.handle_cluster_user_get,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}/orgs/{oname}/users/{uname}",
                    admin_server.handle_cluster_user_put,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}/orgs/{oname}/users/{uname}",
                    admin_server.handle_cluster_user_delete,
                ),
                aiohttp.web.patch(
                    "/api/v1/clusters/{cname}/orgs/{oname}/users/{uname}/quota",
                    admin_server.handle_cluster_user_patch_quota,
                ),
                aiohttp.web.patch(
                    "/api/v1/clusters/{cname}/orgs/{oname}/defaults",
                    admin_server.handle_org_cluster_patch_defaults,
                ),
                # patch org quota endpoints:
                aiohttp.web.patch(
                    "/api/v1/clusters/{cname}/orgs/{oname}/balance",
                    admin_server.handle_org_cluster_patch_balance,
                ),
                aiohttp.web.patch(
                    "/api/v1/clusters/{cname}/orgs/{oname}/quota",
                    admin_server.handle_org_cluster_patch_quota,
                ),
                # projects
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/projects",
                    admin_server.handle_project_post,
                ),
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects",
                    admin_server.handle_project_post,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/projects",
                    admin_server.handle_project_list,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects",
                    admin_server.handle_project_list,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/projects/{pname}",
                    admin_server.handle_project_get,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}",
                    admin_server.handle_project_get,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}/projects/{pname}",
                    admin_server.handle_project_put,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}",
                    admin_server.handle_project_put,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}/projects/{pname}",
                    admin_server.handle_project_delete,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}",
                    admin_server.handle_project_delete,
                ),
                # project users
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/projects/{pname}/users",
                    admin_server.handle_project_user_post,
                ),
                aiohttp.web.post(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}/users",
                    admin_server.handle_project_user_post,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/projects/{pname}/users",
                    admin_server.handle_project_user_list,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}/users",
                    admin_server.handle_project_user_list,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/projects/{pname}/users/{uname}",
                    admin_server.handle_project_user_get,
                ),
                aiohttp.web.get(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}/users/{uname}",
                    admin_server.handle_project_user_get,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}/projects/{pname}/users/{uname}",
                    admin_server.handle_project_user_put,
                ),
                aiohttp.web.put(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}/users/{uname}",
                    admin_server.handle_project_user_put,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}/projects/{pname}/users/{uname}",
                    admin_server.handle_project_user_delete,
                ),
                aiohttp.web.delete(
                    "/api/v1/clusters/{cname}/orgs/{oname}/projects/{pname}/users/{uname}",
                    admin_server.handle_project_user_delete,
                ),
            )
        )
        return app

    app = _create_app()
    runner = ApiRunner(app, port=8085)
    api_address = await runner.run()
    admin_server.address = api_address
    yield admin_server
    await runner.close()


@pytest.fixture
def admin_url(
    mock_admin_server: AdminServer,
) -> URL:
    return mock_admin_server.url


@asynccontextmanager
async def create_local_app_server(
    app: aiohttp.web.Application, port: int = 8080
) -> AsyncIterator[ApiAddress]:
    runner = aiohttp.web.AppRunner(app)
    try:
        await runner.setup()
        api_address = ApiAddress("0.0.0.0", port)
        site = aiohttp.web.TCPSite(runner, api_address.host, api_address.port)
        await site.start()
        yield api_address
    finally:
        await runner.shutdown()
        await runner.cleanup()


class ApiRunner:
    def __init__(self, app: aiohttp.web.Application, port: int) -> None:
        self._app = app
        self._port = port

        self._api_address_future: asyncio.Future[ApiAddress] = asyncio.Future()
        self._cleanup_future: asyncio.Future[None] = asyncio.Future()
        self._task: asyncio.Task[None] | None = None

    async def _run(self) -> None:
        async with create_local_app_server(self._app, port=self._port) as api_address:
            self._api_address_future.set_result(api_address)
            await self._cleanup_future

    async def run(self) -> ApiAddress:
        loop = asyncio.get_running_loop()
        self._task = loop.create_task(self._run())
        return await self._api_address_future

    async def close(self) -> None:
        if self._task:
            task = self._task
            self._task = None
            self._cleanup_future.set_result(None)
            await task

    @property
    def closed(self) -> bool:
        return not self._task
