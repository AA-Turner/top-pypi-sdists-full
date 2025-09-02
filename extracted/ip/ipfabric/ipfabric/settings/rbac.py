import logging
import string
from typing import Any, Optional, Union, Literal

from httpx import HTTPStatusError
from pydantic import BaseModel, Field, PrivateAttr

from ipfabric.models.oas import Endpoint
from ipfabric.models.rbac import Role, Policy
from ipfabric.tools.shared import valid_slug, raise_for_status

logger = logging.getLogger("ipfabric")


class Policies(BaseModel):
    client: Any = Field(exclude=True)
    _policies: Optional[list[Policy]] = PrivateAttr(None)

    def model_post_init(self, __context: Any) -> None:
        self.update()

    def update(self):
        self._policies = self.get_policies()

    @property
    def policies(self):
        return self._policies

    @property
    def policies_by_id(self) -> dict[str, Policy]:
        return {_.policy_id: _ for _ in self.policies}

    @property
    def policies_by_name(self) -> dict[str, Policy]:
        return {_.name: _ for _ in self.policies}

    def get_policies(self, policy_name: str = None) -> Union[list[Policy], Policy, None]:
        """
        Gets all policies or filters on one of the options.
        :param policy_name: str: Case Sensitive Policy Name to filter
        :return: List of policies or single policy if name passed
        """
        filters = {"name": ["eq", policy_name]} if policy_name else None
        policies = list()
        for policy in self.client.fetch_all("tables/policies", filters=filters, snapshot=False):
            p = Policy(**policy)
            p.api_scopes = [self.client.scope_to_api[_] for _ in p.api_scope_ids if _ in self.client.scope_to_api]
            policies.append(p)
        if policy_name:
            return policies.pop() if policies else None
        return policies

    def search_policies_for_endpoint(
        self, api_endpoint: Union[str, Endpoint], method: Literal["POST", "GET", "DELETE", "PATCH", "PUT"] = "POST"
    ) -> list[Policy]:
        """Takes an API endpoint and returns all related policies.
        Args:
            api_endpoint: API table endpoint, SDK Endpoint object, or Policy UUID.
            method: HTTP method if searching by API Table Endpoint.

        Returns: List of Policies matching the endpoint.
        """
        if isinstance(api_endpoint, Endpoint):
            api_scope_id = api_endpoint.api_scope_id
        elif set(api_endpoint).issubset(string.hexdigits) and len(api_endpoint) == 40:
            api_scope_id = api_endpoint
        else:
            endpoint = self.client.oas[self.client._check_url(api_endpoint)]
            if not getattr(endpoint, method.lower()):
                raise ValueError(f"API Endpoint '{endpoint.api_endpoint}' does not have a '{method}' method.")
            api_scope_id = getattr(endpoint, method.lower()).api_scope_id
        return [p for p in self.policies if api_scope_id in p.api_scopes_by_id]

    def _check_policy(self, name=None, description=None, api_scope_ids=None, attribute_filters=None):
        if not (name and description):
            raise SyntaxError("No Policy name or description provided.")
        elif name in self.policies_by_name:
            raise ValueError(f"Duplicate Policy name detected: `{name}`.")
        elif api_scope_ids and attribute_filters:
            raise SyntaxError("Policy must either be API Scoped or Attribute Filter not both.")
        elif not (api_scope_ids or attribute_filters):
            raise SyntaxError("No API Scopes or Attribute Filters provided.")
        if api_scope_ids:
            return self._fmt_api_scopes(api_scope_ids)
        return None

    @staticmethod
    def _fmt_api_scopes(api_scope_ids):
        tmp = set()
        for _ in api_scope_ids:
            if isinstance(_, Endpoint):
                tmp.add(_.api_scope_id)
            elif isinstance(_, str):
                tmp.add(str(_))
            else:
                raise ValueError(f"Invalid Scope: {_}")
        return list(tmp)

    def _create_policy(
        self,
        name: str,
        description: str,
        api_scope_ids: list[Union[int, str, Endpoint]] = None,
        attribute_filters: dict = None,
    ) -> Policy:
        fmt_api_scopes = self._check_policy(name, description, api_scope_ids, attribute_filters)
        payload = {
            "name": valid_slug(name),
            "description": description,
        }
        if api_scope_ids:
            payload["apiScopeIds"] = fmt_api_scopes
        else:
            payload["attributeFilters"] = attribute_filters

        raise_for_status(self.client.post(f"policies/scopes/{'api' if api_scope_ids else 'attributes'}", json=payload))
        return self.get_policies(name)

    def create_policy(
        self,
        name: str,
        description: str,
        api_scope_ids: list[Union[int, str, Endpoint]] = None,
        attribute_filters: dict = None,
    ) -> Policy:
        policy = self._create_policy(name, description, api_scope_ids, attribute_filters)
        self.update()
        return policy

    def create_policies(
        self, policies: list[dict[str, Union[str, dict, list[Union[int, str, Endpoint]]]]]
    ) -> dict[str, Policy]:
        """Create multiple policies.

        Args:
            policies: List of dicts [{name: str, description: str, api_scope_ids: list[Union[int, str, Endpoint]]}
                                    {name: str, description: str, attribute_filters: dict}]

        Returns: Dict of created policies by name.
        """
        created, policy_names = dict(), set()
        for policy in policies:
            self._check_policy(**policy)
            policy_names.add(policy["name"])
        if len(policy_names) != len(policies):
            raise ValueError("Duplicate policy names found.")

        for policy in policies:
            try:
                created[policy["name"]] = self._create_policy(**policy)
            except HTTPStatusError:
                created[policy["name"]] = False
        self.update()
        return created

    def _delete_policy(self, policy: Union[int, str, Policy]) -> bool:
        """Deletes a Role.

        Args:
            policy: Policy ID or Policy object

        Returns: True
        """
        raise_for_status(
            self.client.delete(f"policies/{policy.policy_id if isinstance(policy, Policy) else str(policy)}")
        )
        return True

    def delete_policy(self, policy: Union[int, str, Policy]) -> bool:
        _ = self._delete_policy(policy)
        self.update()
        return _

    def delete_policies(self, policies: list[Union[int, str, Policy]]) -> dict[str, bool]:
        deleted = dict()
        for policy in policies:
            policy_id = policy.policy_id if isinstance(policy, Policy) else str(policy)
            try:
                deleted[policy_id] = self._delete_policy(policy_id)
            except HTTPStatusError:
                deleted[policy_id] = False
        self.update()
        return deleted

    def update_policy(  # noqa: C901
        self,
        policy: Union[int, str, Policy],
        api_scope_ids: list[Union[int, str, Endpoint]] = None,
        attribute_filters: dict = None,
        name: str = None,
        description: str = None,
        replace_api_scopes: bool = False,
    ) -> Policy:
        if not (api_scope_ids or attribute_filters or name or description):
            raise SyntaxError("No updates provided.")
        policy = policy if isinstance(policy, Policy) else self.policies_by_id[str(policy)]
        if policy.scope_type == "attributeScopes" and api_scope_ids:
            raise SyntaxError(f"Policy `{policy.name}` is Attribute Scoped not API Scoped.")
        elif policy.scope_type == "apiScopes" and attribute_filters:
            raise SyntaxError(f"Policy `{policy.name}` is API Scoped not Attribute Scoped.")

        payload = {
            "description": description or policy.description,
            "name": name or policy.name,
        }
        if api_scope_ids:
            api_scope_ids = set(self._fmt_api_scopes(api_scope_ids))
            if not replace_api_scopes:
                api_scope_ids.update(set(policy.api_scope_ids))
            payload["apiScopeIds"] = list(api_scope_ids)
        else:
            payload["attributeFilters"] = attribute_filters

        resp = raise_for_status(
            self.client.patch(
                f"policies/scopes/{'api' if policy.scope_type == 'apiScopes' else 'attributes'}/{policy.policy_id}",
                json=payload,
            )
        )
        self.update()
        return self.policies_by_id[resp.json()["id"]]


class Roles(BaseModel):
    client: Any
    _roles: Optional[list[Role]] = None
    _policies: Optional[Policies] = PrivateAttr(None)

    def model_post_init(self, __context: Any) -> None:
        self._policies = self.client.settings.policies
        self._roles = self.get_roles()

    def update(self):
        self._policies.update()
        self._roles = self.get_roles()

    @property
    def roles(self):
        return self._roles

    @property
    def roles_by_id(self):
        return {r.role_id: r for r in self.roles}

    @property
    def roles_by_name(self):
        return {r.name: r for r in self.roles}

    def get_roles(self, role_name: str = None) -> [list[Role], Role, None]:
        """
        Gets all roles or filters on one of the options.
        :param role_name: str: Case Sensitive Role Name to filter
        :return: List of roles or single role if filtered
        """
        filters = {"name": ["ieq", role_name]} if role_name else None
        roles = list()
        for role in self.client.fetch_all("tables/roles", filters=filters, snapshot=False):
            roles.append(
                Role(**role, policies=[self._policies.policies_by_id[_] for _ in role["policyIds"]])
                if self._policies
                else Role(**role)
            )
        if role_name:
            return roles.pop() if roles else None
        return roles

    def search_roles_for_policy(self, policy_name: str = None, policy_id: Union[str, int] = None) -> list[Role]:
        if policy_name and not self._policies:
            raise ValueError(self.client._api_insuf_rights + 'on POST "/tables/policies".')
        if policy_name:
            return [r for r in self.roles if policy_name in r.policies_by_name]
        elif policy_id:
            return [r for r in self.roles if str(policy_id) in r.policies_by_id]
        else:
            raise SyntaxError("No Policy Name or ID provided.")

    def search_roles_for_endpoint(
        self, api_endpoint: Union[str, Endpoint], method: Literal["POST", "GET", "DELETE", "PATCH", "PUT"] = "POST"
    ) -> list[Role]:
        """Takes an API endpoint and returns all related roles.
        Args:
            api_endpoint: API table endpoint, SDK Endpoint object, or Policy UUID.
            method: HTTP method if searching by API Table Endpoint.

        Returns: List of Roles matching the endpoint.
        """
        policies = self._policies.search_policies_for_endpoint(api_endpoint, method)
        if not policies:
            logger.warning(f"No policies found for API Scope ID {api_endpoint}.")
            return list()
        roles = set()
        for p in policies:
            roles.update(set(self.search_roles_for_policy(policy_id=p.policy_id)))
        return list(roles)

    def _create_role(self, name: str, description: str, policy_ids: list[Union[int, str, Policy]]) -> Role:
        payload = {
            "name": valid_slug(name),
            "description": description,
            "policyIds": [_.policy_id if isinstance(_, Policy) else str(_) for _ in policy_ids],
        }
        raise_for_status(self.client.post("roles", json=payload))
        return self.get_roles(name)

    def create_role(self, name: str, description: str, policy_ids: list[Union[int, str, Policy]]) -> Role:
        role = self._create_role(name, description, policy_ids)
        self.update()
        return role

    def create_roles(self, roles: list[dict[str, Union[str, list[Union[int, str, Policy]]]]]) -> dict[str, Role]:
        """Create multiple roles.

        Args:
            roles: List of dicts [{name: str, description: str, policy_ids: list[Union[int, str, Policy]]}]

        Returns: Dict of created roles by name.
        """
        created, role_names = dict(), set()
        for role in roles:
            if set(role.keys()) != {"name", "description", "policy_ids"} or not (
                isinstance(role["name"], str)
                and isinstance(role["description"], str)
                and isinstance(role["policy_ids"], list)
            ):
                raise SyntaxError(f"Invalid role `{str(role)}`.")
            elif role["name"] in self.roles_by_name:
                raise ValueError(f"Duplicate Role name detected: `{role['name']}`.")
            role_names.add(role["name"])
        if len(role_names) != len(roles):
            raise ValueError("Duplicate role names found.")

        for role in roles:
            try:
                created[role["name"]] = self.create_role(**role)
            except HTTPStatusError:
                created[role["name"]] = False
        return created

    def _delete_role(self, role: Union[int, str, Role]) -> bool:
        """Deletes a Role.

        Args:
            role: Role ID or Role object

        Returns: True
        """
        raise_for_status(self.client.delete(f"roles/{role.role_id if isinstance(role, Role) else str(role)}"))
        return True

    def delete_role(self, role: Union[int, str, Role]) -> bool:
        _ = self._delete_role(role)
        self.update()
        return _

    def delete_roles(self, roles: list[Union[int, str, Role]]) -> dict[str, bool]:
        deleted = dict()
        for role in roles:
            role_id = role.role_id if isinstance(role, Role) else str(role)
            try:
                deleted[role_id] = self._delete_role(role_id)
            except HTTPStatusError:
                deleted[role_id] = False
        return deleted

    def update_role(
        self,
        role: Union[int, str, Role],
        policy_ids: list[Union[int, str, Policy]] = None,
        name: str = None,
        description: str = None,
        replace: bool = False,
    ) -> Role:
        """Updates a Role.

        Args:
            role: Role ID or Role object
            policy_ids: List of Policy IDs or Policy Objects
            name: New name for role, if None then do not update
            description: New description, if None then do not update
            replace: True to replace all policies, defaults to false to append policies

        Returns: Role object
        """
        if not (policy_ids or name or description):
            raise SyntaxError("No updates provided.")
        role = role if isinstance(role, Role) else self.roles_by_id[str(role)]
        policies = set(role.policy_ids)
        if replace and policy_ids:
            policies = {_.policy_id if isinstance(_, Policy) else str(_) for _ in policy_ids}
        elif policy_ids:
            policies.update({_.policy_id if isinstance(_, Policy) else str(_) for _ in policy_ids})
        payload = {
            "description": description or role.description,
            "name": name or role.name,
            "policyIds": list(policies),
        }
        resp = raise_for_status(self.client.put(f"roles/{role.role_id}", json=payload))
        self.update()
        return self.roles_by_id[resp.json()["id"]]
