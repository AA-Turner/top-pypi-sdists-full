import json
import logging
import re
from importlib.resources import files
from typing import Any

from deepdiff import DeepDiff
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr

from ipfabric.models import Policy, Role

logger = logging.getLogger("ipfabric")

EXCLUDE_PATH = re.compile(r"\['(policy_id|role_id)'\]")


class ManagedRBAC(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    ipf: Any = Field(exclude=True)
    _current_policies: dict = PrivateAttr(default_factory=dict)
    _policies: dict = PrivateAttr(default_factory=dict)
    _current_roles: dict = PrivateAttr(default_factory=dict)
    _roles: dict = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        path = files("ipfabric.tools.managed_rbac")
        if not (path.joinpath("policies.json").is_file() and path.joinpath("roles.json").is_file()):
            logger.critical("No managed RBAC found for this version, please contact your SA.")
            exit()

        self._policies = json.loads(path.joinpath("policies.json").read_text())
        self._current_policies = {
            k: {"description": v.description, "paths": v.api_scope_ids, "policy_id": v.policy_id}
            for k, v in self.ipf.settings.policies.policies_by_name.items()
            if k in self._policies
        }
        self._roles = json.loads(path.joinpath("roles.json").read_text())
        self._current_roles = {
            k: {"description": v.description, "policies": [p.name for p in v.policies], "role_id": v.role_id}
            for k, v in self.ipf.settings.roles.roles_by_name.items()
            if k in self._roles
        }

    def _apply_policy(self) -> dict[str, Policy]:
        policies = dict()
        if not self._current_policies:
            logger.warning("No Managed RBAC Policies found, pushing new policies.")
            policies = self.ipf.settings.policies.create_policies(
                [
                    {"name": k, "description": v["description"], "api_scope_ids": v["paths"]}
                    for k, v in self._policies.items()
                ]
            )
            return policies
        missing = {k: v for k, v in self._policies.items() if k not in self._current_policies}
        configured = {k: v for k, v in self._policies.items() if k in self._current_policies}
        if missing:
            logger.warning("Missing Managed RBAC Policies found, pushing new policies.")
            policies.update(
                self.ipf.settings.policies.create_policies(
                    [
                        {"name": k, "description": v["description"], "api_scope_ids": v["paths"]}
                        for k, v in missing.items()
                    ]
                )
            )
        if configured:
            diff = DeepDiff(configured, self._current_policies, exclude_regex_paths=EXCLUDE_PATH, ignore_order=True)
            if diff:
                logger.warning("Policy changes found, pushing updates.")
                for _ in diff.affected_root_keys:
                    logger.warning(f"Updating policy: {_}.")
                    policy = self.ipf.settings.policies.update_policy(
                        policy=self._current_policies[_]["policy_id"],
                        api_scope_ids=self._policies[_]["paths"],
                        name=_,
                        description=self._policies[_]["description"],
                        replace_api_scopes=True,
                    )
                    policies.update({_: policy})
                policies.update(
                    {
                        _: self.ipf.settings.policies.policies_by_name[_]
                        for _ in configured
                        if _ not in diff.affected_root_keys
                    }
                )
            else:
                policies.update({_: self.ipf.settings.policies.policies_by_name[_] for _ in configured})
        return policies

    def _apply_role(self, policies) -> dict[str, Role]:
        roles = dict()
        if not self._roles:
            logger.warning("No Managed RBAC Roles found, pushing new roles.")
            roles = self.ipf.settings.roles.create_roles(
                [
                    {"name": k, "description": v["description"], "policy_ids": [policies[_] for _ in v["policies"]]}
                    for k, v in self._roles.items()
                ]
            )
            return roles
        missing = {k: v for k, v in self._roles.items() if k not in self._current_roles}
        configured = {k: v for k, v in self._roles.items() if k in self._current_roles}
        if missing:
            logger.warning("Missing Managed RBAC Roles found, pushing new roles.")
            roles.update(
                self.ipf.settings.roles.create_roles(
                    [
                        {"name": k, "description": v["description"], "policy_ids": [policies[_] for _ in v["policies"]]}
                        for k, v in missing.items()
                    ]
                )
            )
        if configured:
            diff = DeepDiff(configured, self._current_roles, exclude_regex_paths=EXCLUDE_PATH, ignore_order=True)
            if diff:
                logger.warning("Role changes found, pushing updates.")
                for _ in diff.affected_root_keys:
                    logger.warning(f"Updating role: {_}.")
                    role = self.ipf.settings.roles.update_role(
                        role=self._current_roles[_]["role_id"],
                        policy_ids=[policies[p] for p in self._roles[_]["policies"]],
                        name=_,
                        description=self._roles[_]["description"],
                        replace=True,
                    )
                    roles.update({_: role})
                roles.update(
                    {
                        _: self.ipf.settings.roles.roles_by_name[_]
                        for _ in configured
                        if _ not in diff.affected_root_keys
                    }
                )
            else:
                roles.update({_: self.ipf.settings.roles.roles_by_name[_] for _ in configured})
        return roles

    def apply(self):
        policies = self._apply_policy()
        self.ipf.settings.roles.update()
        roles = self._apply_role(policies)
        return policies, roles
