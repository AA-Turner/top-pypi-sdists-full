from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, unique
from typing import List, Optional


class FullNameMixin:
    first_name: Optional[str]
    last_name: Optional[str]

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        return ""


@dataclass(frozen=True)
class UserInfo(FullNameMixin):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass(frozen=True)
class User(FullNameMixin):
    name: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass(frozen=True)
class Balance:
    credits: Optional[Decimal] = None
    spent_credits: Decimal = Decimal(0)

    @property
    def is_non_positive(self) -> bool:
        return self.credits is not None and self.credits <= 0


@dataclass(frozen=True)
class Quota:
    total_running_jobs: Optional[int] = None


@unique
class ClusterUserRoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    USER = "user"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__().__repr__()


@dataclass(frozen=True)
class Cluster:
    name: str
    default_credits: Optional[Decimal]
    default_quota: Quota
    default_role: ClusterUserRoleType
    maintenance: bool = False


@dataclass(frozen=True)
class OrgNotificationIntervals:
    balance_projection_seconds: Optional[List[int]]
    """How many seconds left till the balance reaches zero?
    A list of integers, where each number represents a seconds-based interval,
    at which the organization management team will receive a notification,
    if the projected usage will lead to a reaching of a zero-balance in that
    amount of seconds.
    """
    balance_amount: Optional[List[int]]
    """What exact balance amounts should trigger a notification?
    """
    balance_depletion_seconds: Optional[List[int]]
    """If a balance is negative, when we should send a notification?
    e.g. 86_400 means 1 day after org reaches a zero balance.
    """


@dataclass(frozen=True)
class Org:
    name: str
    balance: Balance = Balance()
    user_default_credits: Optional[Decimal] = None
    notification_intervals: Optional[OrgNotificationIntervals] = None


@unique
class OrgUserRoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__().__repr__()


@dataclass(frozen=True)
class OrgUser:
    org_name: str
    user_name: str
    role: OrgUserRoleType
    balance: Balance

    def add_info(self, user_info: UserInfo) -> "OrgUserWithInfo":
        return OrgUserWithInfo(
            user_name=self.user_name,
            role=self.role,
            org_name=self.org_name,
            balance=self.balance,
            user_info=user_info,
        )


@dataclass(frozen=True)
class OrgUserWithInfo(OrgUser):
    user_info: UserInfo


@dataclass(frozen=True)
class OrgCluster:
    org_name: str
    cluster_name: str
    balance: Balance
    quota: Quota
    default_credits: Optional[Decimal] = None
    default_quota: Quota = Quota()
    default_role: ClusterUserRoleType = ClusterUserRoleType.USER
    storage_size: Optional[int] = None
    maintenance: bool = False


@dataclass(frozen=True)
class ClusterUser:
    cluster_name: str
    user_name: str
    role: Optional[ClusterUserRoleType]
    quota: Quota
    balance: Balance
    org_name: Optional[str]

    def add_info(self, user_info: UserInfo) -> "ClusterUserWithInfo":
        return ClusterUserWithInfo(
            cluster_name=self.cluster_name,
            user_name=self.user_name,
            role=self.role,
            quota=self.quota,
            balance=self.balance,
            org_name=self.org_name,
            user_info=user_info,
        )


@dataclass(frozen=True)
class ClusterUserWithInfo(ClusterUser):
    user_info: UserInfo


@unique
class ProjectUserRoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WRITER = "writer"
    READER = "reader"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__().__repr__()


@dataclass(frozen=True)
class Project:
    name: str
    cluster_name: str
    org_name: Optional[str]
    is_default: bool = False  # Enables auto add new tenant users to thi project
    default_role: ProjectUserRoleType = ProjectUserRoleType.WRITER


@dataclass(frozen=True)
class ProjectUser:
    user_name: str
    cluster_name: str
    org_name: Optional[str]
    project_name: str
    role: ProjectUserRoleType

    def add_info(self, user_info: UserInfo) -> "ProjectUserWithInfo":
        return ProjectUserWithInfo(
            project_name=self.project_name,
            cluster_name=self.cluster_name,
            user_name=self.user_name,
            org_name=self.org_name,
            user_info=user_info,
            role=self.role,
        )


@dataclass(frozen=True)
class ProjectUserWithInfo(ProjectUser):
    user_info: UserInfo
