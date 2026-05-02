import loguru
import requests
from requests import Response
from lgt_jobs.lgt_common.discord_client.methods import DiscordMethods


class DiscordClient:
    base_url = 'https://discord.com/api/'
    discord_api_version = 'v9/'
    token: str
    headers: dict

    def __init__(self, token: str = None):
        self.token = token
        self.headers = {"Authorization": self.token}

    def login(self, login: str, password: str, captcha_key: str = None, rqtoken: str = None,
              user_agent: str = None) -> dict:
        payload = {
            'login': login,
            'password': password,
            "undelete": False,
            "login_source": None,
            "gift_code_sku_id": None
        }
        cookies = {
            'User-Agent': user_agent
        }
        if captcha_key:
            cookies = cookies | {'X-Captcha-Key': captcha_key,'X-Captcha-Rqtoken': rqtoken}
        response = requests.post(f"{self.base_url}{self.discord_api_version}{DiscordMethods.LOGIN.value}", json=payload, cookies=cookies)
        if response.status_code == 400 or response.status_code == 200:
            return response.json()
        return {}

    def get_servers(self) -> list | dict:
        response = requests.get(f"{self.base_url}{DiscordMethods.USER_GUILDS.value}?with_counts=true",
                                headers=self.headers)
        return self.__response(response).json()

    def get_dms(self) -> list | dict:
        response = requests.get(f"{self.base_url}{DiscordMethods.USER_DMS.value}", headers=self.headers)
        return self.__response(response).json()

    def get_current_user(self) -> dict:
        response = requests.get(f"{self.base_url}{DiscordMethods.USER.value}", headers=self.headers)
        if response.status_code != 200:
            self.__log_error(response)
        return response.json()

    def patch_current_user(self, username: str, avatar: str = None) -> dict:
        payload = {'username': username, 'avatar': avatar}
        response = requests.patch(f"{self.base_url}{DiscordMethods.USER.value}", headers=self.headers, json=payload)
        if response.status_code != 200:
            self.__log_error(response)
        return response.json()

    def patch_current_user_in_guild(self, guild_id: str, username: str, avatar: str = None) -> dict:
        payload = {'username': username, 'avatar': avatar}
        response = requests.patch(f"{self.base_url}{DiscordMethods.guild_user(guild_id)}",
                                  headers=self.headers, json=payload)
        if response.status_code != 200:
            self.__log_error(response)
        return response.json()

    def patch_current_user_bio(self, bio: str) -> dict:
        payload = {'bio': bio}
        response = requests.patch(f"{self.base_url}{DiscordMethods.USER_PROFILE.value}", headers=self.headers,
                                  json=payload)
        if response.status_code != 200:
            self.__log_error(response)
        return response.json()

    def patch_user_bio_in_guild(self, guild_id: str, bio: str) -> dict:
        payload = {'bio': bio}
        response = requests.patch(f"{self.base_url}{DiscordMethods.guild_bio(guild_id)}",
                                  headers=self.headers, json=payload)
        if response.status_code != 200:
            self.__log_error(response)
        return response.json()

    def get_channels(self, guild_id: str) -> list | dict:
        response = requests.get(f"{self.base_url}{DiscordMethods.guild_channels(guild_id)}?with_counts=true",
                                headers=self.headers)
        return self.__response(response).json()

    def get_invite_link(self, channel_id: str) -> Response:
        response = requests.post(f'{self.base_url}{self.discord_api_version}'
                                 f'{DiscordMethods.channels_invites(channel_id)}', headers=self.headers)
        return self.__response(response)

    @staticmethod
    def __log_error(response: Response):
        loguru.logger.warning(f"[DiscordClient WARNING]: {response.url}, {response.status_code}, {response.content}")

    @staticmethod
    def __response(response: Response):
        if response.status_code != 200:
            DiscordClient.__log_error(response)
        return response
