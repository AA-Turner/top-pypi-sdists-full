import asyncio
from collections.abc import Callable
import pandas as pd
from flowtask.components.Azure import Azure
from flowtask.exceptions import ComponentError


class MS365Usage(Azure):
    """
    MS365Usage

    Overview

        The MS365Usage class is a component for retrieving Microsoft 365 usage reports via the Microsoft Graph API.
        It extends the Azure class and supports various report types such as M365, Teams, SharePoint, OneDrive, and Yammer.

    :widths: auto

        | report_type      |   No     | The type of report to retrieve, defaults to "M365".                                              |
        | usage_method     |   No     | The usage method for the report, defaults to "UserDetail".                                       |
        | _report          |   Yes    | The specific report endpoint to use based on the report type and usage method.                   |
        | period           |   No     | The period for the report, defaults to "D7".                                                     |
        | format           |   No     | The format of the report, defaults to "text/csv".                                                |
        | method           |   Yes    | The HTTP method to use for the API request, set to "GET".                                        |
        | download         |   Yes    | Flag indicating if a file download is required, set to False.                                    |
        | url              |   Yes    | The formatted URL for the API request.                                                           |
        | app              |   Yes    | The MSAL app instance for authentication.                                                        |
        | token_type       |   Yes    | The type of authentication token.                                                                |
        | auth             |   Yes    | Dictionary containing the authentication details.                                                |

        Return

        The methods in this class manage the retrieval and processing of Microsoft 365 usage reports, including initialization,
        API request execution, and result handling.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          MS365Usage:
          period: D7
          report_type: Yammer
          usage_method: UserDetail
          credentials:
          client_id: OFFICE_365_REPORT_ID
          client_secret: OFFICE_365_REPORT_SECRET
          tenant_id: AZURE_ADFS_TENANT_ID
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.report_type = kwargs.pop("report_type", "M365")
        self.usage_method = kwargs.pop("usage_method", "UserDetail")
        if self.report_type == 'M365':
            self._report = 'getM365App'
        elif self.report_type == 'Teams':
            self._report = 'getTeamsUserActivity'
            if self.usage_method == 'DeviceUserDetails':
                self._report = 'getTeamsDeviceUsage'
                self.usage_method = 'UserDetail'
            elif self.usage_method == 'DeviceUserCounts':
                self._report = 'getTeamsDeviceUsage'
            elif self.usage_method == 'DeviceDistributionUserCounts':
                self._report = 'getTeamsDeviceUsage'
                self.usage_method = 'DistributionUserCounts'
        elif self.report_type == 'SharePoint':
            self._report = 'getSharePointActivity'
        elif self.report_type == 'OneDrive':
            self._report = 'getOneDriveActivity'
        elif self.report_type == 'Yammer':
            self._report = 'getYammerActivity'
            if self.usage_method == 'DeviceUserDetails':
                self._report = 'getYammerDeviceUsage'
                self.usage_method = 'UserDetail'
            elif self.usage_method == 'DeviceUserCounts':
                self._report = 'getYammerDeviceUsage'
            elif self.usage_method == 'DeviceDistributionUserCounts':
                self._report = 'getYammerDeviceUsage'
                self.usage_method = 'DistributionUserCounts'
        else:
            self._report = 'getM365App'
        self.period = kwargs.pop("period", "D7")
        self.format = kwargs.pop("format", "text/csv")
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.as_dataframe: bool = True  # Forcing return a Dataframe

    async def start(self, **kwargs):
        await super().start(**kwargs)

        self.method = "GET"
        self.download = False
        self.as_binary = False
        self.accept = 'application/octet-stream'

        _base_url = "https://graph.microsoft.com/v1.0/reports/{report}{usage_method}(period='{period}')?$format={format}"  # noqa: E501
        self.url = _base_url.format(
            report=self._report,
            usage_method=self.usage_method,
            period=self.period,
            format=self.format
        )
        return True

    async def run(self):
        """Run Azure Connection for getting Users Info."""
        self._logger.info(f"<{__name__}>:")
        self.set_apikey()

        try:
            result, error = await self.async_request(self.url, self.method)
            if error:
                raise ComponentError(
                    f"Error getting {self.usage_method} from API: {error}"
                )
        except Exception as ex:
            raise ComponentError(
                f"Error getting {self.usage_method} from API: {ex}"
            ) from ex
        if self.as_dataframe is True:
            df = await self.from_csv(result, sep=',', header=0)
            print(df)
            self._result = df
        else:
            # returned as text
            self._result = result
        return self._result

    async def close(self):
        pass

    def set_apikey(self):
        self.app = self.get_msal_app()
        token, self.token_type = self.get_token()
        self.auth["apikey"] = token
