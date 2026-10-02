# flake8: noqa: I003

from fabric.functions.user_data_functions import UserDataFunctions
from azure.cosmos import CosmosClient
from .cosmos_client_provider import CosmosClientProvider


def use_cosmosdb(udf: UserDataFunctions):
    udf.register_provider(CosmosClient, CosmosClientProvider)
    pass
