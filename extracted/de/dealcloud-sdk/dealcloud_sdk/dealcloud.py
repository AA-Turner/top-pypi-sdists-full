from dealcloud_sdk.constants.auth import AVAILABLE_SCOPES, AvailableScopeTypes
from dealcloud_sdk.data.dealcloud_data import DealCloudData


class DealCloud(DealCloudData):
    def __init__(
        self,
        site_url: str,
        client_id: str,
        client_secret: str,
        scope: AvailableScopeTypes = AVAILABLE_SCOPES,
        refresh_id_maps: bool = True,
    ):
        """
        Init function for DealCloud

        Args:
            site_url(str): the target DealCloud site in the format "{client}.dealcloud.com" - i.e. no https:// or /
            client_id(int): the client id from the user api key
            client_secret(str): the client secret from the user api key
            scope(tuple[str]): the authentication scopes, defaults to ("data", "user_management", "publish")
        """
        super().__init__(site_url, client_id, client_secret, scope, refresh_id_maps)

    pass
