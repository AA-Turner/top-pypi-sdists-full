import requests
import os
import json


class BitbucketConfig:
    def __init__(
            self,
            bitbucket_key=None,
            bitbucket_secret=None,
            bitbucket_workspace=None,
            bitbucket_repo_slug=None,
            auth_header=None
    ):
        self.url = 'https://api.bitbucket.org'
        self.auth_url: str = 'https://bitbucket.org'

        self.bitbucket_key: str = bitbucket_key or os.getenv('BITBUCKET_KEY')
        self.bitbucket_secret: str = bitbucket_secret or os.getenv('BITBUCKET_SECRET')
        self.bitbucket_workspace: str = bitbucket_workspace or os.getenv('BITBUCKET_WORKSPACE')
        self.bitbucket_repo_slug: str = bitbucket_repo_slug or os.getenv('BITBUCKET_REPO_SLUG')
        self.token = self.__get_bitbucket_token(self.bitbucket_key, self.bitbucket_secret)
        self.auth_header = auth_header or ''

    def __get_bitbucket_token(self, key: str, secret: str) -> object:
        """get bitbucket oauth token

        :param key: bitbucket key
        :param secret: bitbucket secret
        :return: token: bitbucket oauth token
        """
        token = ''
        if key and secret:
            data = {'grant_type': 'client_credentials'}
            response = requests.post(
                f'{self.auth_url}/site/oauth2/access_token',
                data=data,
                auth=(key, secret)
            )

            if response.status_code == 200:
                token = json.loads(response.text)['access_token']

        return token
