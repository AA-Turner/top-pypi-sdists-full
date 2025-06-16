from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from .exception.internal_exception import DatabaseInitializeFailureException, DatabaseConnectFailureException


class MongoDB:
    def __init__(self, user_name: str, password: str, host: str, port: int, db_name: str, server_selection_timeout: int,
                 connection_timeout: int, auth_source: str, ssl: bool = False, ssl_ca_certs: str = None):
        self.client = None
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.connection_timeout = connection_timeout
        self.server_selection_timeout = server_selection_timeout
        self.ssl = ssl
        self.ssl_ca_certs = ssl_ca_certs
        self.auth_source = auth_source

    async def connect(self):
        try:
            db_settings = dict(username=self.user_name, password=self.password, host=self.host, port=self.port,
                               connectTimeoutMS=self.connection_timeout,
                               serverSelectionTimeoutMS=self.server_selection_timeout, retryWrites=False,
                               authSource=self.auth_source)
            if self.ssl:
                db_settings["ssl"] = self.ssl

            if self.ssl_ca_certs and self.ssl_ca_certs != "":
                db_settings["tlsCAFile"] = self.ssl_ca_certs

            self.client = AsyncIOMotorClient(**db_settings)
        except ServerSelectionTimeoutError:
            raise DatabaseInitializeFailureException()

    async def close(self):
        if self.client:
            self.client.close()

    def get_database(self):
        if not self.client:
            raise DatabaseConnectFailureException()
        return self.client[self.db_name]

    async def get_mongodb_uri(self) -> str:
        if self.user_name and self.password:
            uri = f"mongodb://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        else:
            uri = f"mongodb://{self.host}:{self.port}/{self.db_name}"

        uri += f"?authSource={self.auth_source}&connectTimeoutMS={self.connection_timeout}&serverSelectionTimeoutMS={self.server_selection_timeout}&retryWrites=false"

        if self.ssl:
            uri += "&ssl=true"
        if self.ssl_ca_certs and self.ssl_ca_certs != "":
            uri += f"&tlsCAFile={self.ssl_ca_certs}"

        return uri
