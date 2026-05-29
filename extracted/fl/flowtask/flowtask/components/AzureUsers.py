from datetime import datetime, timedelta, timezone

import iso8601
from ..interfaces.azure_component import Azure
from ..exceptions import ComponentError, DataNotFound

class AzureUsers(Azure):
    """
    AzureUsers Component

        Overview

        This component retrieves a list of users from Azure Active Directory (AAD) using the Microsoft Graph API.

            :widths: auto

    | credentials            |   Yes    | Dictionary placeholder for Azure AD application credentials.                                |
    | most_recent (optional) |    No    | ISO 8601-formatted date and time string to filter users created on or after that date/time. |
    | include_modified       |    No    | If True (default), also fetches users modified since `most_recent` via delta query.         |

    **Returns**

        A pandas DataFrame containing the retrieved user information. Each row represents an Azure user, and columns might include properties like:

        - `objectId`: Unique identifier for the user in AAD.
        - `displayName`: User's display name.
        - `userPrincipalName`: User's email address (usually the primary login).
        - ... (other user properties depending on the AAD response)

    **Error Handling**

        - The component raises a `ComponentError` with a detailed message in case of errors during authentication, API calls, or data processing. This error will be surfaced within your Flowtask workflow.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          AzureUsers:
          recent: '2023-10-01'
          include_modified: true
        ```
    """
    _version = "1.1.0"
    accept: str = 'application/json'

    async def _fetch_all_pages(self, url: str) -> list:
        """Fetch all pages from a paginated Graph API response."""
        all_items = []
        while url:
            result, error = await self.async_request(url, self.method)
            if error:
                raise ComponentError(
                    f"{__name__}: Error in AzureUsers: {error}"
                )
            all_items.extend(result.get("value", []))
            url = result.get("@odata.nextLink") or result.get("@odata.deltaLink", None)
            # deltaLink is the token for next delta call, not a next page
            if url and "@odata.deltaLink" in result and "@odata.nextLink" not in result:
                break
        return all_items

    async def get_users(self, most_recent: str = None):
        if most_recent:
            utc_datetime = (
                iso8601.parse_date(most_recent).isoformat().replace("+00:00", "Z")
            )
            url = f"{self.users_info}?$filter=createdDateTime ge {utc_datetime}"
        else:
            url = f"{self.users_info}"
        return await self._fetch_all_pages(url)

    async def get_modified_users(self, since: str) -> list:
        """Fetch users modified/updated since a given date using the delta query.

        Uses the Microsoft Graph /users/delta endpoint to retrieve users
        that have been created or modified since the specified date.

        Note: The /users/delta endpoint does not support date-based $filter
        (only $filter=id eq {value} is allowed). Results are filtered locally
        by createdDateTime after retrieval.
        """
        since_dt = iso8601.parse_date(since)
        delta_url = f"{self.users_info}/delta"
        all_users = await self._fetch_all_pages(delta_url)
        # Filter locally: keep users created or modified on/after the given date
        filtered = []
        for user in all_users:
            created = user.get("createdDateTime")
            if created:
                try:
                    user_dt = iso8601.parse_date(created)
                    if user_dt >= since_dt:
                        filtered.append(user)
                        continue
                except (ValueError, iso8601.ParseError):
                    pass
            # If no createdDateTime, include the user (delta returns it
            # because it was modified, so it's relevant)
            if not created:
                filtered.append(user)
        return filtered

    def _merge_users(self, created: list, modified: list) -> list:
        """Merge created and modified user lists, deduplicating by id."""
        seen = {}
        for user in created:
            uid = user.get("id") or user.get("objectId")
            if uid:
                seen[uid] = user
        for user in modified:
            uid = user.get("id") or user.get("objectId")
            if uid:
                seen[uid] = user  # modified version takes precedence
        return list(seen.values())

    async def run(self):
        """Run Azure Connection for getting Users Info."""
        self._logger.info(
            f"<{__name__}>: Starting Azure Connection for getting Users Info."
        )
        self.app = self.get_msal_app()
        token, self.token_type = self.get_token()
        self.auth["apikey"] = token
        self.headers["Content-Type"] = "application/json"
        self.method = "GET"
        try:
            more_recent = None
            if hasattr(self, "recent"):
                more_recent = self.mask_replacement(self.recent)
            created_users = await self.get_users(more_recent)

            # Also fetch modified/updated users via delta query
            include_modified = getattr(self, "include_modified", True)
            if more_recent and include_modified:
                self._logger.info(
                    f"<{__name__}>: Fetching modified users since {more_recent}"
                )
                modified_users = await self.get_modified_users(more_recent)
                self._logger.info(
                    f"<{__name__}>: Found {len(created_users)} created "
                    f"and {len(modified_users)} modified users"
                )
                result = self._merge_users(created_users, modified_users)
            else:
                result = created_users

            self._logger.info(f"<{__name__}>: Successfully got Users Info.")
            self._result = await self.create_dataframe(result)
            if self._result is None:
                raise DataNotFound(
                    "No data found for Azure Users."
                )
        except Exception as err:
            self._logger.error(err)
            raise ComponentError(f"{__name__}: Error in AzureUsers: {err}") from err
        numrows = len(self._result.index)
        self.add_metric("NUM_USERS", numrows)
        if self._debug is True:
            print(self._result)
            print("::: Printing Column Information === ")
            for column, t in self._result.dtypes.items():
                print(column, "->", t, "->", self._result[column].iloc[0])
        return self._result
