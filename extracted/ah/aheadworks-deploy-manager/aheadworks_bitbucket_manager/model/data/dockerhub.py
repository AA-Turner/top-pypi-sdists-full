import requests
import json
import datetime


class DockerHubConfig:
    def __init__(
            self,
            dockerhub_user,
            dockerhub_password,
            pull_expire_date=None,
            push_expire_date=None
    ):
        self.url = 'https://hub.docker.com'
        self.auth_url = 'https://hub.docker.com/v2/users/login'
        self.dockerhub_user = dockerhub_user
        self.dockerhub_password = dockerhub_password
        self.token = self.__get_token(self.dockerhub_user, self.dockerhub_password)
        self.auth_headder = {'Authorization': f'JWT {self.token}'}
        self.pull_expire_date = pull_expire_date or datetime.datetime.now() - datetime.timedelta(days=10, )
        self.push_expire_date = push_expire_date or datetime.datetime.now() - datetime.timedelta(days=10, )

    def __get_token(self, username: str, password: str):
        token = ''
        if username and password:
            headers = {'Content-Type': 'application/json', }
            data = '{"username": ' + f'"{username}"' + f', "password": "{password}"' + '}'
            response = requests.post(self.auth_url, data=data, headers=headers)
            if response.status_code == 200:
                token = json.loads(response.text)['token']

        return token
