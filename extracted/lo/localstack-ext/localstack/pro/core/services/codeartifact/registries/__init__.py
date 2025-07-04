from localstack.http import Router
from localstack.http.dispatcher import Handler
from localstack.pro.core.services.codeartifact.registries.npm import register as register_npm


def register_registries(router: Router[Handler]):
    register_npm(router)
