import os
from pathlib import Path
from dotenv import load_dotenv

from adam.utils import creating_dir, debug, log_exc
from adam.utils_k8s.kube_context import KubeContext

class CredCache:
    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(CredCache, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        if not hasattr(self, 'env_f'):
            self.dir = creating_dir(f'{Path.home()}/.kaqing')
            self.env_f = f'{self.dir}/.credentials'
            # immutable - cannot reload with different file content
            load_dotenv(dotenv_path=self.env_f)

            self.overrides: dict[str, str] = {}

    def get_username(self):
        return self.overrides['IDP_USERNAME'] if 'IDP_USERNAME' in self.overrides else self.get('IDP_USERNAME')

    def get_password(self):
        return self.overrides['IDP_PASSWORD'] if 'IDP_PASSWORD' in self.overrides else self.get('IDP_PASSWORD')

    def get(self, key: str) -> str:
        return os.getenv(key)

    def cache(self, username: str, password: str = None):
        if os.path.exists(self.env_f):
            with open(self.env_f, 'w') as file:
                with log_exc():
                    file.truncate()

        updated = []
        updated.append(f'IDP_USERNAME={username}')
        if not KubeContext.in_cluster() and password:
            # do not store password to the .credentials file when in Kubernetes pod
            updated.append(f'IDP_PASSWORD={password}')

        if updated:
            with open(self.env_f, 'w') as file:
                file.write('\n'.join(updated))

            if username:
                self.overrides['IDP_USERNAME'] = username
            if password:
                self.overrides['IDP_PASSWORD'] = password

            debug(f'Cached username: {username}, password: {password}, try load: {self.get_username()}')