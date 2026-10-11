"""
User Management API operations for DealCloud.

The User Management API provides user and group administration:
- Create, update, delete users
- Manage user groups
- User proxies
- Invitations
- User activity tracking

See: https://api.docs.dealcloud.com/docs - User Management API
"""

from datetime import datetime
from typing import Optional, Union, List
from urllib.parse import urlencode

from intapp_rest_client.exceptions import HttpError  # type: ignore[import-untyped]

from ..constants import user_activity as user_activity_constants
from ..files.dealcloud_files import DealCloudFiles


class DealCloudUserManagement(DealCloudFiles):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    User Management API operations.
    
    Provides user and group administration.
    """
    
    @property
    def usermanagement_url(self) -> str:
        """
        Get the User Management API base URL.
        
        Use this for custom user management API calls not covered by SDK methods.
        
        Returns:
            str: User Management API URL (e.g., "https://site.dealcloud.com/api/rest/v1/management/user")
        
        Example:
            >>> # Custom user management endpoint call
            >>> url = f"{dc.usermanagement_url}/users/bulk"
            >>> response = dc.client.post(url, json=payload)
        """
        return self._usermgmt_url
    
    # =========================================================================
    # User CRUD Operations
    # =========================================================================
    
    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: Optional[str] = None,
        federation_id: Optional[str] = None,
        groups: Optional[Union[List[int], List[str]]] = None,
        two_factor_enabled: Optional[bool] = None,
        ip_restrictions_enabled: Optional[bool] = None,
        is_active: bool = True,
    ) -> dict:
        """
        Create a new user.
        
        API: POST /api/rest/v1/management/user
        See: https://api.docs.dealcloud.com/docs/management/create_user
        
        Args:
            email: User's email address
            first_name: User's first name
            last_name: User's last name
            password: Assign password; if blank, a password reset email is sent (no email if IDM enabled)
            federation_id: For SSO users (e.g. federated identity)
            groups: User group IDs (list of int) or group names (list of str); names are resolved via resolve_group_names_to_ids
            two_factor_enabled: Enable 2FA (cannot be disabled via API once set)
            ip_restrictions_enabled: Toggle IP restrictions
            is_active: Create as active (True) or inactive (False)
        
        Returns:
            Created user object with ID
        """
        url = self._usermgmt_url
        payload = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "isActive": is_active,
        }
        if password is not None:
            payload["password"] = password
        if federation_id is not None:
            payload["federationId"] = federation_id
        if groups:
            if any(isinstance(x, str) for x in groups):
                payload["groups"] = self.resolve_group_names_to_ids(groups)
            else:
                payload["groups"] = groups
        if two_factor_enabled is not None:
            payload["twoFactorEnabled"] = two_factor_enabled
        if ip_restrictions_enabled is not None:
            payload["ipRestrictionsEnabled"] = ip_restrictions_enabled
        return self._client.post(url, json=payload)
    
    def create_users(self, users: List[dict]) -> List[dict]:
        """
        Create multiple users. Convenience helper that calls create_user for each item.
        
        Args:
            users: List of user specs. Each dict must have email, first_name, last_name
                   and may include password, federation_id, groups, two_factor_enabled,
                   ip_restrictions_enabled, is_active (same as create_user).
        
        Returns:
            List of created user objects (one per item).
        """
        results = []
        for u in users:
            result = self.create_user(
                email=u["email"],
                first_name=u["first_name"],
                last_name=u["last_name"],
                password=u.get("password"),
                federation_id=u.get("federation_id"),
                groups=u.get("groups"),
                two_factor_enabled=u.get("two_factor_enabled"),
                ip_restrictions_enabled=u.get("ip_restrictions_enabled"),
                is_active=u.get("is_active", True),
            )
            results.append(result)
        return results
    
    def resolve_group_names_to_ids(self, names: Union[str, List[str]]) -> List[int]:
        """
        Resolve group name(s) to group ID(s) via get_all_user_groups().
        Names are matched case-insensitively. Raises ValueError for unknown names.
        """
        names_list = [names] if isinstance(names, str) else names
        groups = self.get_all_user_groups(page_size=1000)
        name_to_id = {}
        for g in groups:
            n = g.get("name")
            if n is not None:
                name_to_id[n.strip().lower()] = g.get("id") or g.get("Id")
        ids = []
        for n in names_list:
            key = n.strip().lower()
            if key not in name_to_id:
                raise ValueError(f"Unknown user group name: {n!r}")
            ids.append(name_to_id[key])
        return ids

    def get_users(
        self,
        user_ids: Optional[List[int]] = None,
        emails: Optional[Union[str, List[str]]] = None,
        user_group_ids: Optional[Union[int, List[int], str, List[str]]] = None,
        modified_since: Optional[Union[datetime, str]] = None,
        page_number: int = 1,
        page_size: int = 10,
    ) -> List[dict]:
        """
        Get users: by IDs (POST) or by filters (GET).
        - If user_ids is provided: POST /api/rest/v1/management/user with body [id, ...].
        - Otherwise: GET with exactly one filter. API requires one of: email, userGroupID,
          or modifiedSince (mutually exclusive). If emails or user_group_ids is a list, one GET
          per item and results are combined (deduplicated by id).
        - user_group_ids may be int, list of int, group name (str), or list of group names (str).
          Names are resolved to IDs via get_user_groups() then get_users is called with those IDs.
        See: https://api.docs.dealcloud.com/docs/management/get_user, get_users_by_id
        
        Args:
            user_ids: If set, fetch these user IDs (POST); GET filters are ignored
            emails: Filter by one email (str) or many (list of str); mutually exclusive with other GET filters
            user_group_ids: Filter by group ID (int), list of IDs (list of int), group name (str), or list of names (list of str)
            modified_since: Filter by recently modified; mutually exclusive with emails, user_group_ids
            page_number: Page number for GET (default 1)
            page_size: Page size for GET, max 1000 (default 10)
        
        Returns:
            List of user objects
        """
        _has_emails = emails is not None and (not isinstance(emails, list) or len(emails) > 0)
        _has_group_ids = user_group_ids is not None and (not isinstance(user_group_ids, list) or len(user_group_ids) > 0)
        _has_modified = modified_since is not None
        _has_filter = _has_emails or _has_group_ids or _has_modified

        # Mutually exclusive: user_ids (POST) vs GET filters
        if user_ids is not None and _has_filter:
            raise ValueError(
                "Use either user_ids (POST) or one of emails, user_group_ids, modified_since (GET); not both."
            )
        # GET path requires at least one filter
        if user_ids is None and not _has_filter:
            raise ValueError(
                "Provide either modified_since, emails or user_group_ids filter."
            )

        # By IDs: POST /api/rest/v1/management/users with body [id, ...] (Get Users by ID; plural path per API)
        if user_ids is not None:
            url = f"{self._usermgmt_url}s"
            return self._client.post(url, json=user_ids)

        # By filter: GET /api/rest/v1/management/user?email=...|userGroupID=...|modifiedSince=...
        if isinstance(emails, list):
            seen_ids = set()
            combined = []
            for e in emails:
                batch = self.get_users(
                    emails=e,
                    page_number=page_number,
                    page_size=page_size,
                )
                for u in batch:
                    uid = u.get("id") or u.get("Id")
                    if uid is not None and uid not in seen_ids:
                        seen_ids.add(uid)
                        combined.append(u)
            return combined

        if user_group_ids is not None and (
            isinstance(user_group_ids, str) or (
                isinstance(user_group_ids, list) and user_group_ids and isinstance(user_group_ids[0], str)
            )
        ):
            group_ids = self.resolve_group_names_to_ids(user_group_ids)
            return self.get_users(
                user_group_ids=group_ids,
                page_number=page_number,
                page_size=page_size,
            )

        if isinstance(user_group_ids, list):
            seen_ids = set()
            combined = []
            for g in user_group_ids:
                batch = self.get_users(
                    user_group_ids=g,
                    page_number=page_number,
                    page_size=page_size,
                )
                for u in batch:
                    uid = u.get("id") or u.get("Id")
                    if uid is not None and uid not in seen_ids:
                        seen_ids.add(uid)
                        combined.append(u)
            return combined

        # GET: API allows only one of email, userGroupID, or modifiedSince
        has_emails = emails is not None
        has_group_ids = user_group_ids is not None
        has_modified = modified_since is not None
        if sum([has_emails, has_group_ids, has_modified]) > 1:
            raise ValueError(
                "Provide either modified_since, emails or user_group_ids; only one filter is allowed."
            )
        params = {
            "pageNumber": page_number,
            "pageSize": min(page_size, 1000),
        }
        if has_emails:
            params["email"] = emails
        elif has_group_ids:
            params["userGroupID"] = user_group_ids
        else:
            params["modifiedSince"] = (
                modified_since.isoformat()
                if isinstance(modified_since, datetime)
                else modified_since
            )
        url = f"{self._usermgmt_url}?{urlencode(params)}"
        return self._client.get(url)

    def get_all_users(self, page_size: int = 1000) -> List[dict]:
        """
        Fetch all users by paginating with modified_since (epoch).
        Used when a full user list is needed (e.g. building email->id map).
        API requires at least one filter; we use modified_since to get all users.
        """
        all_users: List[dict] = []
        page = 1
        since = datetime(1970, 1, 1)
        while True:
            batch = self.get_users(
                modified_since=since,
                page_number=page,
                page_size=page_size,
            )
            if not batch:
                break
            all_users.extend(batch)
            # Stop only when API returns empty; a partial page may not be the end
            page += 1
        return all_users

    def get_users_by_ids(self, user_ids: List[int]) -> List[dict]:
        """
        Get multiple users by IDs. Convenience wrapper for get_users(user_ids=...).
        API: POST /api/rest/v1/management/users with body [id1, id2, ...].
        """
        return self.get_users(user_ids=user_ids)

    def get_user(self, user_id_or_email: Union[int, str]) -> Optional[dict]:
        """
        Get a single user by ID or by email.
        - If int: uses get_users(user_ids=[id]).
        - If str: uses get_users(emails=...).
        Returns None if the user does not exist (e.g. API returns 400/404).
        
        Args:
            user_id_or_email: User ID (int) or email address (str)
        
        Returns:
            User object, or None if not found
        """
        try:
            if isinstance(user_id_or_email, int):
                result = self.get_users(user_ids=[user_id_or_email])
                return (result[0] if result else None) if isinstance(result, list) else None
            result = self.get_users(emails=user_id_or_email, page_size=1)
            return result[0] if result else None
        except HttpError as e:
            msg = getattr(e, "message", None) or getattr(e, "response_body", None) or str(e)
            if getattr(e, "status_code", None) in (400, 404) or "does not exist" in str(msg).lower():
                return None
            raise
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """
        Find user by email address. Convenience wrapper for get_user(email).
        
        Args:
            email: Email address to search
        
        Returns:
            User object if found, None otherwise
        """
        return self.get_user(email)
    
    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password: Optional[str] = None,
        federation_id: Optional[str] = None,
        groups: Optional[Union[List[int], List[str]]] = None,
        two_factor_enabled: Optional[bool] = None,
        ip_restrictions_enabled: Optional[bool] = None,
        is_active: Optional[bool] = None,
    ) -> dict:
        """
        Update user properties. Same optional params as create_user; uses PUT.
        API: PUT /api/rest/v1/management/user with body { id, ... }.
        
        Args:
            user_id: User ID to update
            email: New email address (optional)
            first_name: New first name (optional)
            last_name: New last name (optional)
            password: New password (optional)
            federation_id: For SSO users (optional)
            groups: User group IDs (list of int) or group names (list of str); names resolved via resolve_group_names_to_ids
            two_factor_enabled: Enable 2FA (optional; cannot be disabled via API once set)
            ip_restrictions_enabled: Toggle IP restrictions (optional)
            is_active: Update active status (optional)
        
        Returns:
            Updated user object. If user does not exist, API returns 400 and ValueError is raised.
        """
        url = self._usermgmt_url
        payload = {"id": user_id}
        # API requires email, firstName, lastName in update body; fill from current user if not provided
        existing = None
        if email is None or first_name is None or last_name is None:
            existing = self.get_user(user_id)
        # Swagger UserInfo: request body uses camelCase (email, firstName, lastName)
        if email is not None:
            payload["email"] = email
        else:
            payload["email"] = (existing.get("email") or "") if existing else ""
        if first_name is not None:
            payload["firstName"] = first_name
        else:
            payload["firstName"] = (existing.get("firstName") or "") if existing else ""
        if last_name is not None:
            payload["lastName"] = last_name
        else:
            payload["lastName"] = (existing.get("lastName") or "") if existing else ""
        if password is not None:
            payload["password"] = password
        if federation_id is not None:
            payload["federationId"] = federation_id
        if groups is not None:
            if any(isinstance(x, str) for x in groups):
                payload["groups"] = self.resolve_group_names_to_ids(groups)
            else:
                payload["groups"] = groups
        if two_factor_enabled is not None:
            payload["twoFactorEnabled"] = two_factor_enabled
        if ip_restrictions_enabled is not None:
            payload["ipRestrictionsEnabled"] = ip_restrictions_enabled
        if is_active is not None:
            payload["isActive"] = is_active
        try:
            return self._client.put(url, json=payload)
        except HttpError as e:
            msg = getattr(e, "response_body", None) or getattr(e, "message", None) or str(e)
            if getattr(e, "status_code", None) == 400 and "does not exist" in str(msg).lower():
                raise ValueError("User with given id does not exist.") from None
            raise
    
    def update_users(self, users: List[dict]) -> List[dict]:
        """
        Update multiple users. Convenience helper that calls update_user for each item.
        
        Args:
            users: List of update specs per swagger (camelCase). Each dict must have "id" (user id)
                   and may include email, firstName, lastName, password, federationId, groups,
                   twoFactorEnabled, ipRestrictionsEnabled, isActive.
        
        Returns:
            List of updated user objects (one per item).
        """
        results = []
        for u in users:
            # Swagger UserInfo: id, firstName, lastName, email, etc. (camelCase only)
            user_id = u.get("id")
            if user_id is None:
                raise ValueError("Each update spec must have 'id' (user id per swagger).")
            result = self.update_user(
                user_id=int(user_id),
                email=u.get("email"),
                first_name=u.get("firstName"),
                last_name=u.get("lastName"),
                password=u.get("password"),
                federation_id=u.get("federationId"),
                groups=u.get("groups"),
                two_factor_enabled=u.get("twoFactorEnabled"),
                ip_restrictions_enabled=u.get("ipRestrictionsEnabled"),
                is_active=u.get("isActive"),
            )
            results.append(result)
        return results
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.
        API: DELETE /api/rest/v1/management/user/{{userId}}
        
        Args:
            user_id: User ID to delete
        
        Returns:
            True if successful
        
        Note:
            Deleted users cannot be restored. Consider deactivating instead.
        """
        url = f"{self._usermgmt_url}/{user_id}"
        self._client.delete(url)
        return True
    
    def deactivate_user(self, user_id_or_email: Union[int, str]) -> dict:
        """
        Deactivate a user (set isActive=False).
        
        This is preferred over delete_user for most cases.
        Fetches user by ID or email via get_user, then updates with isActive=False.
        API requires email, firstName, lastName in the update body (taken from fetched user; swagger UserInfo).
        
        Args:
            user_id_or_email: User ID (int) or email address (str)
        
        Returns:
            Updated user object
        
        Raises:
            ValueError: If user is not found
        """
        user = self.get_user(user_id_or_email)
        if user is None:
            raise ValueError("User not found.")
        user_id = user.get("id") or user.get("Id")
        first_name = user.get("firstName") or ""
        last_name = user.get("lastName") or ""
        email = user.get("email") or ""
        return self.update_user(user_id, email=email, first_name=first_name, last_name=last_name, is_active=False)

    def activate_user(self, user_id_or_email: Union[int, str]) -> dict:
        """
        Activate a user (set isActive=True).
        
        Fetches user by ID or email via get_user, then updates with isActive=True.
        API requires email, firstName, lastName in the update body (taken from fetched user; swagger UserInfo).
        
        Args:
            user_id_or_email: User ID (int) or email address (str)
        
        Returns:
            Updated user object
        
        Raises:
            ValueError: If user is not found
        """
        user = self.get_user(user_id_or_email)
        if user is None:
            raise ValueError("User not found.")
        user_id = user.get("id") or user.get("Id")
        first_name = user.get("firstName") or ""
        last_name = user.get("lastName") or ""
        email = user.get("email") or ""
        return self.update_user(user_id, email=email, first_name=first_name, last_name=last_name, is_active=True)
    
    # =========================================================================
    # User Groups
    # =========================================================================
    
    def get_all_user_groups(
        self, page_number: int = 1, page_size: int = 1000
    ) -> List[dict]:
        """
        Get all user groups.
        API: GET /api/rest/v1/management/user/group?pageNumber=&pageSize=
        
        Returns:
            List of user group objects
        """
        url = f"{self._usermgmt_url}/group?pageNumber={page_number}&pageSize={page_size}"
        return self._client.get(url)
    
    def get_user_groups(
        self, group_id: Union[int, str, List[Union[int, str]]]
    ) -> Union[dict, List[dict]]:
        """
        Get one or more user groups by ID or name.
        API: GET /api/rest/v1/management/user/group/{{groupId}}
        String names are resolved via resolve_group_names_to_ids.
        
        Args:
            group_id: Group ID (int), group name (str), or list of IDs and/or names
        
        Returns:
            Single group dict if group_id is int or str; list of group dicts if list
        """
        if isinstance(group_id, int):
            ids = [group_id]
        elif isinstance(group_id, str):
            ids = self.resolve_group_names_to_ids(group_id)
        else:
            ids = []
            for x in group_id:
                if isinstance(x, int):
                    ids.append(x)
                else:
                    ids.extend(self.resolve_group_names_to_ids(x))
        if len(ids) == 1:
            url = f"{self._usermgmt_url}/group/{ids[0]}"
            return self._client.get(url)
        return [self._client.get(f"{self._usermgmt_url}/group/{i}") for i in ids]
    
    def update_user_group(
        self,
        group_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        member_ids: Optional[List[int]] = None,
    ) -> dict:
        """
        Update a user group.
        
        Args:
            group_id: Group ID to update
            name: New name (optional)
            description: New description (optional)
            member_ids: New member list (replaces existing)
        
        Returns:
            Updated group object
        """
        url = f"{self._usermgmt_url}/group/{group_id}"
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if member_ids is not None:
            payload["memberIds"] = member_ids
        
        return self._client.put(url, json=payload)
    
    def delete_user_group(
        self, group_id: Union[int, str, List[Union[int, str]]]
    ) -> bool:
        """
        Delete one or more user groups by ID or name.
        String names are resolved via resolve_group_names_to_ids.
        
        Args:
            group_id: Group ID (int), group name (str), or list of IDs and/or names
        
        Returns:
            True if successful
        """
        if isinstance(group_id, int):
            ids = [group_id]
        elif isinstance(group_id, str):
            ids = self.resolve_group_names_to_ids(group_id)
        else:
            ids = []
            for x in group_id:
                if isinstance(x, int):
                    ids.append(x)
                else:
                    ids.extend(self.resolve_group_names_to_ids(x))
        for i in ids:
            url = f"{self._usermgmt_url}/group/{i}"
            self._client.delete(url)
        return True
    
    def add_user_to_group(self, user_id: int, group_id: int) -> dict:
        """
        Add a user to a group.
        
        Args:
            user_id: User ID to add
            group_id: Group ID to add to
        
        Returns:
            Updated group object
        """
        group = self.get_user_groups(group_id)
        current_members = group.get("users", group.get("memberIds", []))
        if user_id not in current_members:
            current_members.append(user_id)
            return self.update_user_group(group_id, member_ids=current_members)
        return group
    
    def remove_user_from_group(self, user_id: int, group_id: int) -> dict:
        """
        Remove a user from a group.
        
        Args:
            user_id: User ID to remove
            group_id: Group ID to remove from
        
        Returns:
            Updated group object
        """
        group = self.get_user_groups(group_id)
        current_members = group.get("users", group.get("memberIds", []))
        if user_id in current_members:
            current_members.remove(user_id)
            return self.update_user_group(group_id, member_ids=current_members)
        return group
    
    def add_users_to_groups(self, assignments: List[dict]):
        """
        Bulk add users to user groups. API: PUT /api/rest/v1/management/user/group.
        Swagger: array of UsersToUserGroupRequestVm { userIds: number[], groupIds: number[] }.
        
        Args:
            assignments: List of dicts with userIds (list of int) and groupIds (list of int).
                        Also accepts user_ids / group_ids (snake_case). Group names in list
                        are resolved via resolve_group_names_to_ids.
        
        Returns:
            API response (200 Success or 204 No content)
        """
        payload = []
        for a in assignments:
            user_ids = a.get("userIds") or a.get("user_ids") or []
            group_ids = a.get("groupIds") or a.get("group_ids") or []
            if not user_ids or not group_ids:
                continue
            group_ids = list(group_ids)
            if any(isinstance(g, str) for g in group_ids):
                group_ids = self.resolve_group_names_to_ids(group_ids)
            payload.append({"userIds": list(user_ids), "groupIds": group_ids})
        if not payload:
            return None
        url = f"{self._usermgmt_url}/group"
        return self._client.put(url, json=payload)
    
    def remove_users_from_groups(self, assignments: List[dict]):
        """
        Bulk remove users from user groups. API: DELETE /api/rest/v1/management/user/group.
        Swagger: same body as add — array of { userIds: number[], groupIds: number[] }.
        
        Args:
            assignments: List of dicts with userIds and groupIds (or user_ids / group_ids).
                        Group names resolved via resolve_group_names_to_ids.
        
        Returns:
            API response (200 Success or 204 No content)
        """
        payload = []
        for a in assignments:
            user_ids = a.get("userIds") or a.get("user_ids") or []
            group_ids = a.get("groupIds") or a.get("group_ids") or []
            if not user_ids or not group_ids:
                continue
            group_ids = list(group_ids)
            if any(isinstance(g, str) for g in group_ids):
                group_ids = self.resolve_group_names_to_ids(group_ids)
            payload.append({"userIds": list(user_ids), "groupIds": group_ids})
        if not payload:
            return None
        url = f"{self._usermgmt_url}/group"
        return self._client.delete(url, json=payload)
    
    # =========================================================================
    # User Licenses
    # =========================================================================
    
    def get_user_licenses(
        self,
        user_ids: Optional[Union[int, List[int]]] = None,
        is_billable: Optional[bool] = None,
        page_number: int = 1,
        page_size: int = 10,
    ) -> Union[dict, List[dict]]:
        """
        Get user license info by user ID(s) or all licenses with pagination.
        When user_ids is None, uses GET .../userLicenses (paginated).
        When user_ids is set, uses GET .../userLicense/{{userId}} per ID.
        
        Returns licenseType, isBillable (True when LicenseType 1 or 2), userId, description.
        LicenseType: 1 Standard, 2 Limited, 3 Free/Complimentary, 4 No License.
        
        Args:
            user_ids: User ID (int), list of user IDs, or None to get all via pagination
            is_billable: When user_ids is None: filter by billable (True = Standard/Limited, False = Free/No License)
            page_number: When user_ids is None: page number (default 1)
            page_size: When user_ids is None: page size (default 10)
        
        Returns:
            Single license dict if one ID; list of license dicts if list or paginated (user_ids=None)
        """
        if user_ids is not None:
            ids = [user_ids] if isinstance(user_ids, int) else list(user_ids)
            if len(ids) == 1:
                url = f"{self._url_root_v1}/management/userLicense/{ids[0]}"
                return self._client.get(url)
            return [
                self._client.get(f"{self._url_root_v1}/management/userLicense/{i}")
                for i in ids
            ]
        params = {"pageNumber": page_number, "pageSize": page_size}
        if is_billable is not None:
            params["isBillable"] = "true" if is_billable else "false"
        url = f"{self._url_root_v1}/management/userLicenses?{urlencode(params)}"
        return self._client.get(url)
    
    def update_user_license(
        self,
        user_id: int,
        license_type: int,
        description: Optional[str] = None,
    ):
        """
        Update existing user license for the current client.
        API: PUT /api/rest/v1/management/userLicense
        
        LicenseType: 1 Standard, 2 Limited, 3 Free/Complimentary, 4 No License.
        
        Args:
            user_id: User ID to update
            license_type: License type ID (1–4)
            description: Optional description
        
        Returns:
            Response from the API
        """
        url = f"{self._url_root_v1}/management/userLicense"
        payload = {"userId": user_id, "licenseType": license_type}
        if description is not None:
            payload["description"] = description
        return self._client.put(url, json=payload)
    
    def update_user_licenses(
        self,
        updates: List[dict],
    ) -> List:
        """
        Update user licenses for multiple users. Calls update_user_license for each item.
        
        Args:
            updates: List of dicts with userId (int), licenseType (int), and optional description (str).
                     e.g. [{"userId": 1, "licenseType": 2}, {"userId": 2, "licenseType": 3, "description": "Free"}]
        
        Returns:
            List of API responses (one per update)
        """
        results = []
        for u in updates:
            user_id = u.get("userId") or u.get("user_id")
            license_type = u.get("licenseType") or u.get("license_type")
            description = u.get("description")
            results.append(
                self.update_user_license(
                    user_id=user_id,
                    license_type=license_type,
                    description=description,
                )
            )
        return results
    
    # =========================================================================
    # User Proxy
    # =========================================================================
    
    def create_user_proxy(
        self,
        proxy_user_id: int,
        principal_user_ids: Union[int, List[int]],
    ) -> dict:
        """
        Create user proxy assignments. Proxy user can act on behalf of the principal user(s).
        API: POST /api/rest/v1/management/user/proxy.
        See: https://api.docs.dealcloud.com/docs/management/create_user_proxy.
        Calls replace existing proxy assignments for the proxy user.
        
        Args:
            proxy_user_id: User who receives proxy access (ProxyUserId).
            principal_user_ids: User ID or list of user IDs on whose behalf the proxy can act (Users).
        
        Returns:
            Response from the API
        """
        url = f"{self._usermgmt_url}/proxy"
        users = [principal_user_ids] if isinstance(principal_user_ids, int) else list(principal_user_ids)
        payload = {
            "proxyUserId": proxy_user_id,
            "users": users,
        }
        return self._client.post(url, json=payload)
    
    def get_user_proxy(
        self,
        user_id: Optional[int] = None,
        proxy_query: Optional[str] = None,
        user_query: Optional[str] = None,
        search_by_name: Optional[bool] = None,
        page_number: int = 1,
        page_size: int = 100,
    ) -> List[dict]:
        """
        Get user proxy assignments.
        API: GET /api/rest/v1/management/user/proxy.
        See: https://api.docs.dealcloud.com/docs/management/get_user_proxy.
        If user_id is given, results are filtered client-side for that principal.
        
        Args:
            user_id: Optional principal user ID to filter by (client-side filter)
            proxy_query: Search by proxy user (email or full name)
            user_query: Search by principal user (email or full name)
            search_by_name: Toggle search by name (optional; API default when omitted)
            page_number: Page number (default 1)
            page_size: Page size, max 1000 (default 100)
        
        Returns:
            List of proxy relationships
        """
        url = f"{self._usermgmt_url}/proxy?pageNumber={page_number}&pageSize={page_size}"
        if proxy_query:
            url += f"&proxyQuery={proxy_query}"
        if user_query:
            url += f"&userQuery={user_query}"
        if search_by_name is not None:
            url += f"&searchByName={'true' if search_by_name else 'false'}"
        result = self._client.get(url)
        if user_id is not None and result:
            result = [r for r in result if r.get("userId") == user_id]
        return result
    
    def delete_user_proxy(self, user_id: int, proxy_user_id: int) -> bool:
        """
        Delete a user proxy relationship.
        API path not documented; uses .../proxy/{userId}/{proxyUserId}.
        
        Args:
            user_id: User who granted proxy
            proxy_user_id: User who had proxy access
        
        Returns:
            True if successful
        """
        url = f"{self._usermgmt_url}/proxy/{user_id}/{proxy_user_id}"
        self._client.delete(url)
        return True
    
    def delete_user_proxies_from_current(
        self,
        user_id: Optional[int] = None,
        proxy_user_id: Optional[int] = None,
        **kwargs,
    ) -> List[bool]:
        """
        Retrieve current proxy assignments (via get_user_proxy), then delete each one.
        Uses DELETE .../proxy/{userId}/{proxyUserId} per assignment (Swagger does not document this path).
        
        Args:
            user_id: If set, only fetch assignments for this principal user (client-side filter)
            proxy_user_id: If set, only delete assignments involving this proxy user
            **kwargs: Passed to get_user_proxy (e.g. proxy_query, user_query, search_by_name, page_number, page_size)
        
        Returns:
            List of True per successful delete
        """
        assignments = self.get_user_proxy(user_id=user_id, **kwargs)
        pairs: List[tuple] = []
        for item in assignments:
            pid = (
                item.get("proxyUserId")
                or (item.get("proxyUser") or {}).get("id")
                or (item.get("proxyUser") or {}).get("Id")
            )
            if pid is None:
                continue
            users = item.get("users") or []
            if users:
                for u in users:
                    uid = u.get("id") or u.get("Id")
                    if uid is not None:
                        pairs.append((uid, pid))
            else:
                uid = item.get("userId") or item.get("UserId")
                if uid is not None:
                    pairs.append((uid, pid))
        if proxy_user_id is not None:
            pairs = [(u, p) for u, p in pairs if p == proxy_user_id]
        return [self.delete_user_proxy(uid, pid) for uid, pid in pairs]
    
    # =========================================================================
    # User Invitations
    # =========================================================================
    
    def invite_user(
        self,
        email: str,
        duration: Optional[int] = None,
        groups: Optional[Union[List[int], List[str]]] = None,
        auto_create_or_link_contact: Optional[bool] = None,
        mapped_contact_id: Optional[int] = None,
    ) -> dict:
        """
        Invite or shadow-add a user to the site.
        API: POST /api/rest/v1/management/user/invite (single email per request).
        Invites an existing DealCloud Universe user; sends invitation email.
        
        Args:
            email: Email address to invite
            duration: If temporary, duration in days
            groups: Group IDs (list of int) or group names (list of str); names resolved via resolve_group_names_to_ids
            auto_create_or_link_contact: Link invited user to contact
            mapped_contact_id: Contact ID when auto_create_or_link_contact is True
        
        Returns:
            Response dict from the invite API
        """
        url = f"{self._usermgmt_url}/invite"
        payload = {"email": email}
        if duration is not None:
            payload["duration"] = duration
        if groups is not None:
            if any(isinstance(x, str) for x in groups):
                payload["groups"] = self.resolve_group_names_to_ids(groups)
            else:
                payload["groups"] = groups
        if auto_create_or_link_contact is not None:
            payload["autoCreateOrLinkContact"] = auto_create_or_link_contact
        if mapped_contact_id is not None:
            payload["mappedContactId"] = mapped_contact_id
        return self._client.post(url, json=payload)

    def add_existing_user(
        self,
        email: str,
        duration: Optional[int] = None,
        groups: Optional[Union[List[int], List[str]]] = None,
        is_active: Optional[bool] = None,
        auto_create_or_link_contact: Optional[bool] = None,
        mapped_contact_id: Optional[int] = None,
    ) -> dict:
        """
        Shadow-add an existing user to the site (no invitation email or user acceptance).
        API: POST /api/rest/v1/management/user/addExisting (AddExistingUserRequestVm).
        Only users with an email domain that matches the site's dedicated domain are eligible.
        Same params as invite_user; see https://api.docs.dealcloud.com/docs/management/invite_user.
        
        Args:
            email: Email address of existing DealCloud Universe user
            duration: If temporary, duration in days
            groups: Group IDs (list of int) or group names (list of str); names resolved via resolve_group_names_to_ids
            is_active: Whether the user is active (Swagger: isActive)
            auto_create_or_link_contact: Link added user to contact
            mapped_contact_id: Contact ID when auto_create_or_link_contact is True (creates new if omitted)
        
        Returns:
            Response dict from the add-existing-user API
        """
        url = f"{self._usermgmt_url}/addExisting"
        payload = {"email": email}
        if duration is not None:
            payload["duration"] = duration
        if groups is not None:
            if any(isinstance(x, str) for x in groups):
                payload["groups"] = self.resolve_group_names_to_ids(groups)
            else:
                payload["groups"] = groups
        if is_active is not None:
            payload["isActive"] = is_active
        if auto_create_or_link_contact is not None:
            payload["autoCreateOrLinkContact"] = auto_create_or_link_contact
        if mapped_contact_id is not None:
            payload["mappedContactId"] = mapped_contact_id
        return self._client.post(url, json=payload)

    def add_existing_users(self, users: List[dict]) -> List[dict]:
        """
        Shadow-add multiple existing users. Convenience helper that calls add_existing_user for each item.
        
        Args:
            users: List of specs. Each dict must have email and may include
                   duration, groups, is_active, auto_create_or_link_contact, mapped_contact_id
                   (same as add_existing_user).
        
        Returns:
            List of response dicts (one per item).
        """
        results = []
        for u in users:
            email = u.get("email")
            if email is None:
                raise ValueError("Each add-existing spec must have 'email'.")
            # Swagger AddExistingUserRequestVm: camelCase only
            result = self.add_existing_user(
                email=email,
                duration=u.get("duration"),
                groups=u.get("groups"),
                is_active=u.get("isActive"),
                auto_create_or_link_contact=u.get("autoCreateOrLinkContact"),
                mapped_contact_id=u.get("mappedContactId"),
            )
            results.append(result)
        return results

    def invite_users(self, invites: List[dict]) -> List[dict]:
        """
        Invite multiple users. Convenience helper that calls invite_user for each item.
        
        Args:
            invites: List of invite specs. Each dict must have email and may include
                     duration, groups, auto_create_or_link_contact, mapped_contact_id
                     (same as invite_user).
        
        Returns:
            List of response dicts (one per item).
        """
        results = []
        for inv in invites:
            email = inv.get("email")
            if email is None:
                raise ValueError("Each invite spec must have 'email'.")
            # Swagger InviteExistingUserRequestVm: camelCase only
            result = self.invite_user(
                email=email,
                duration=inv.get("duration"),
                groups=inv.get("groups"),
                auto_create_or_link_contact=inv.get("autoCreateOrLinkContact"),
                mapped_contact_id=inv.get("mappedContactId"),
            )
            results.append(result)
        return results
    
    # =========================================================================
    # User Activity
    # =========================================================================

    @staticmethod
    def get_activity_types() -> dict:
        """Return Activity Types mapping (id -> name). See dealcloud_sdk.constants.user_activity."""
        return user_activity_constants.get_activity_types()

    @staticmethod
    def get_activity_type_name(activity_id: int) -> str:
        """Return display name for an activity type ID."""
        return user_activity_constants.get_activity_type_name(activity_id)

    @staticmethod
    def get_source_types() -> dict:
        """Return Source Types mapping (id -> name). See dealcloud_sdk.constants.user_activity."""
        return user_activity_constants.get_source_types()

    @staticmethod
    def get_source_type_name(source_id: int) -> str:
        """Return display name for a source type ID."""
        return user_activity_constants.get_source_type_name(source_id)

    @staticmethod
    def get_export_data_types() -> dict:
        """Return Export Data Type mapping (id -> name); used when activity=8. See dealcloud_sdk.constants.user_activity."""
        return user_activity_constants.get_export_data_types()

    @staticmethod
    def get_export_data_type_name(export_data_type_id: int) -> str:
        """Return display name for an export data type ID."""
        return user_activity_constants.get_export_data_type_name(export_data_type_id)

    def get_user_activity(
        self,
        user_ids: Optional[List[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        activity: Optional[Union[int, str]] = None,
        source: Optional[Union[int, str]] = None,
        export_data_type: Optional[Union[int, str]] = None,
        page_number: int = 1,
        page_size: int = 1000,
    ) -> dict:
        """
        Get user activity audit log.
        API: POST /api/rest/v1/management/user/activity.
        See: https://api.docs.dealcloud.com/docs/management/user_activity.
        All parameters are optional; the API requires a request body (sending {} returns all activity).
        activity, source, and export_data_type accept int IDs or exact string names (see get_activity_types(), etc.).
        
        Args:
            user_ids: Filter by user IDs (optional; omit for all users)
            date_from: Start date (optional; default 90 days ago)
            date_to: End date, must be > date_from (optional; default today)
            activity: Activity type ID or exact name (e.g. 8 or "Export Data")
            source: Source type ID or exact name (e.g. 1 or "Web UI")
            export_data_type: For activity=8 only; ID or exact name (e.g. 0 or "Export Data")
            page_number: Page number (default 1)
            page_size: Page size (default 1000, max 1000)
        
        Returns:
            Response with totalRecords and rows
        
        Raises:
            ValueError: If a string value for activity/source/export_data_type does not match an exact name
        """
        # Resolve string names to IDs (exact match required)
        _activity = activity
        if isinstance(_activity, str):
            _activity = user_activity_constants.get_activity_type_id(_activity)
        _source = source
        if isinstance(_source, str):
            _source = user_activity_constants.get_source_type_id(_source)
        _export_data_type = export_data_type
        if isinstance(_export_data_type, str):
            _export_data_type = user_activity_constants.get_export_data_type_id(_export_data_type)

        url = f"{self._usermgmt_url}/activity"
        payload = {}
        if user_ids is not None:
            payload["userIds"] = user_ids
        if date_from is not None:
            payload["dateFrom"] = date_from.isoformat()
        if date_to is not None:
            payload["dateTo"] = date_to.isoformat()
        if _activity is not None:
            payload["activity"] = _activity
        if _source is not None:
            payload["source"] = _source
        if _export_data_type is not None:
            payload["exportDataType"] = _export_data_type
        # API requires a request body; send {} when no filters (returns all activity)
        body = payload if payload else {}
        _page_size = min(page_size, 1000)  # API: pageSize cannot be greater than 1000
        params = f"pageNumber={page_number}&pageSize={_page_size}"
        return self._client.post(f"{url}?{params}", json=body)

    def get_all_user_activity(
        self,
        date_from: datetime,
        date_to: datetime,
        user_ids: Optional[List[int]] = None,
        activity: Optional[Union[int, str]] = None,
        source: Optional[Union[int, str]] = None,
        export_data_type: Optional[Union[int, str]] = None,
        page_size: int = 1000,
    ) -> dict:
        """
        Get all user activity for a date range; pagination is handled internally.
        Date range is mandatory. API requires dateTo > dateFrom (at least 1 day greater).
        
        Args:
            date_from: Start date (required)
            date_to: End date (required; must be > date_from)
            user_ids: Filter by user IDs (optional)
            activity: Activity type ID or exact name (optional)
            source: Source type ID or exact name (optional)
            export_data_type: For activity=8 only; ID or exact name (optional)
            page_size: Page size per request (default 1000, max 1000)
        
        Returns:
            {"totalRecords": N, "rows": [ ... ]} with all rows in the range
        
        Raises:
            ValueError: If date_to is not greater than date_from, or if a string filter does not match an exact name
        """
        if date_to <= date_from:
            raise ValueError("date_to must be greater than date_from.")
        _page_size = min(page_size, 1000)  # API: pageSize cannot be greater than 1000
        all_rows: List[dict] = []
        total_records: Optional[int] = None
        page_number = 1
        while True:
            response = self.get_user_activity(
                user_ids=user_ids,
                date_from=date_from,
                date_to=date_to,
                activity=activity,
                source=source,
                export_data_type=export_data_type,
                page_number=page_number,
                page_size=_page_size,
            )
            rows = response.get("rows") or []
            all_rows.extend(rows)
            if total_records is None:
                total_records = response.get("totalRecords")
            if total_records is not None and len(all_rows) >= total_records:
                break
            if len(rows) < _page_size:
                break
            page_number += 1
        return {"totalRecords": total_records if total_records is not None else len(all_rows), "rows": all_rows}
    
    # Roles: The DealCloud User Management API does not expose role endpoints.
    # See https://api.docs.dealcloud.com/docs/management for documented endpoints.

