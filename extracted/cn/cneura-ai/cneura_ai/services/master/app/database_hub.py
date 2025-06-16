import base64
import hashlib
import asyncpg
import aiohttp
import motor.motor_asyncio
import redis.asyncio as redis
from cryptography.fernet import Fernet
import aiosqlite
import aio_pika
from chromadb import HttpClient as ChromaClient
import logging

class DatabaseHub:
    def __init__(self, sqlite_path: str, secret_key:str, verbose: bool = False):
        self.sqlite_path = sqlite_path
        self.sqlite_conn = None
        self.config = {}
        self.postgres_pool = None
        self.mongo_client = None
        self.redis_client = None
        self.chroma_client = None
        self.rabbitmq_connection = None
        self.rabbitmq_http_auth = None 
        self.rabbitmq_http_url = None 

        
        hash_digest = hashlib.sha256(secret_key.encode()).digest()
        self.fernet = Fernet(base64.urlsafe_b64encode(hash_digest))

        if verbose:
            logging.basicConfig(level=logging.DEBUG)

    async def connect_sqlite(self):
        if not self.sqlite_conn:
            try:
                self.sqlite_conn = await aiosqlite.connect(self.sqlite_path)
                logging.debug("Connected to SQLite.")
            except Exception as e:
                logging.error(f"Failed to connect to SQLite: {e}")
                raise RuntimeError(e)

    def _encrypt(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def _decrypt(self, ciphertext: str) -> str:
        try:
            return self.fernet.decrypt(ciphertext.encode()).decode()
        except Exception:
            return None  # Or raise an exception if needed

    async def load_config(self):
        await self.connect_sqlite()
        self.config.clear()
        try:
            async with self.sqlite_conn.execute("SELECT key, value FROM config") as cursor:
                async for key, value in cursor:
                    self.config[key] = self._decrypt(value)
            self.config["SQLITE_PATH"] = self.sqlite_path

            # Load RabbitMQ HTTP auth config
            if all(k in self.config for k in (
                "RABBITMQ_HTTP_USER", "RABBITMQ_HTTP_PASSWORD", 
                "RABBITMQ_HTTP_HOST", "RABBITMQ_HTTP_PORT")):
                
                user = self.config["RABBITMQ_HTTP_USER"]
                password = self.config["RABBITMQ_HTTP_PASSWORD"]
                host = self.config["RABBITMQ_HTTP_HOST"]
                port = int(self.config["RABBITMQ_HTTP_PORT"])
                
                self.rabbitmq_http_url = f"http://{host}:{port}/api"
                auth_str = f"{user}:{password}"
                self.rabbitmq_http_auth = base64.b64encode(auth_str.encode()).decode()
            
            logging.debug("Configuration loaded.")
        except Exception as e:
            logging.error(f"Failed to load configuration from SQLite: {e}")
            raise RuntimeError(e)

    async def set_config_items(self, items: list[dict]):
        """
        Expects a list of dicts with 'key' and 'value'.
        Encrypts and inserts or updates the database.
        """
        await self.connect_sqlite()
        try:
            async with self.sqlite_conn.execute("BEGIN"):
                for item in items:
                    encrypted_value = self._encrypt(item["value"])
                    await self.sqlite_conn.execute(
                        """
                        INSERT INTO config (key, value) VALUES (?, ?)
                        ON CONFLICT(key) DO UPDATE SET value = excluded.value
                        """,
                        (item["key"], encrypted_value)
                    )
                await self.sqlite_conn.commit()
        except Exception as e:
            await self.sqlite_conn.execute("ROLLBACK")
            logging.error(f"Failed to save config items: {e}")
            raise RuntimeError(e)


    async def connect_postgres(self):
        if not self.config:
            await self.load_config()
        if not self.postgres_pool:
            try:
                required = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_HOST", "POSTGRES_PORT"]
                self._validate_config_keys(required)
                self.postgres_pool = await asyncpg.create_pool(
                    user=self.config["POSTGRES_USER"],
                    password=self.config["POSTGRES_PASSWORD"],
                    database=self.config["POSTGRES_DB"],
                    host=self.config["POSTGRES_HOST"],
                    port=int(self.config["POSTGRES_PORT"]),
                )
                logging.debug("Connected to PostgreSQL.")
            except Exception as e:
                logging.error(f"Failed to connect to PostgreSQL: {e}")
                raise RuntimeError(e)

    async def connect_mongodb(self):
        if not self.config:
            await self.load_config()
        if not self.mongo_client:
            try:
                required = ["MONGO_USER", "MONGO_PASSWORD", "MONGO_HOST", "MONGO_PORT"]
                self._validate_config_keys(required)
                port = int(self.config['MONGO_PORT'])
                uri = f"mongodb://{self.config['MONGO_USER']}:{self.config['MONGO_PASSWORD']}@{self.config['MONGO_HOST']}:{port}"
                self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(uri)
                logging.debug("Connected to MongoDB.")
            except Exception as e:
                logging.error(f"Failed to connect to MongoDB: {e}")
                raise RuntimeError(e)

    async def connect_redis(self):
        if not self.config:
            await self.load_config()
        if not self.redis_client:
            try:
                required = ["REDIS_HOST", "REDIS_PORT"]
                self._validate_config_keys(required)
                self.redis_client = redis.Redis(
                    host=self.config["REDIS_HOST"],
                    port=int(self.config["REDIS_PORT"]),
                    decode_responses=True
                )
                await self.redis_client.ping()
                logging.debug("Connected to Redis.")
            except Exception as e:
                logging.error(f"Failed to connect to Redis: {e}")
                raise RuntimeError(e)

    async def connect_chromadb(self):
        if not self.config:
            await self.load_config()
        if not self.chroma_client:
            try:
                required = ["CHROMADB_HOST", "CHROMADB_PORT", "CHROMADB_API_KEY"]
                self._validate_config_keys(required)
                self.chroma_client = ChromaClient(
                    host=self.config["CHROMADB_HOST"],
                    port=int(self.config["CHROMADB_PORT"]),
                    headers={"Authorization": f"Bearer {self.config['CHROMADB_API_KEY']}"}
                )
                logging.debug("Connected to ChromaDB.")
            except Exception as e:
                logging.error(f"Failed to connect to ChromaDB: {e}")
                raise RuntimeError(e)

    async def connect_rabbitmq(self):
        if not self.config:
            await self.load_config()
        if not self.rabbitmq_connection:
            try:
                required = ["RABBITMQ_USER", "RABBITMQ_PASSWORD", "RABBITMQ_HOST", "RABBITMQ_PORT"]
                self._validate_config_keys(required)
                url = (
                    f"amqp://{self.config['RABBITMQ_USER']}:"
                    f"{self.config['RABBITMQ_PASSWORD']}@"
                    f"{self.config['RABBITMQ_HOST']}:"
                    f"{int(self.config['RABBITMQ_PORT'])}/"
                )
                self.rabbitmq_connection = await aio_pika.connect_robust(url)
                logging.debug("Connected to RabbitMQ.")
            except Exception as e:
                logging.error(f"Failed to connect to RabbitMQ: {e}")
                raise RuntimeError(e)

    async def list_rabbitmq_queues(self):
        """
        Calls RabbitMQ Management HTTP API /api/queues to get queue info
        """
        logging.debug(f"{self.rabbitmq_http_url, self.rabbitmq_http_auth}")
        if not self.rabbitmq_http_url or not self.rabbitmq_http_auth:
            raise RuntimeError("RabbitMQ HTTP API config missing")

        url = f"{self.rabbitmq_http_url}/queues"
        headers = {
            "Authorization": f"Basic {self.rabbitmq_http_auth}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise RuntimeError(f"RabbitMQ HTTP API error: {response.status}")
                data = await response.json()
                return [queue["name"] for queue in data]

    async def disconnect_all(self):
        try:
            if self.sqlite_conn:
                await self.sqlite_conn.close()
                logging.debug("Disconnected SQLite.")
        except Exception as e:
            logging.warning(f"Failed to disconnect SQLite: {e}")

        try:
            if self.postgres_pool:
                await self.postgres_pool.close()
                logging.debug("Disconnected PostgreSQL.")
        except Exception as e:
            logging.warning(f"Failed to disconnect PostgreSQL: {e}")

        try:
            if self.mongo_client:
                self.mongo_client.close()
                logging.debug("Disconnected MongoDB.")
        except Exception as e:
            logging.warning(f"Failed to disconnect MongoDB: {e}")

        try:
            if self.redis_client:
                await self.redis_client.close()
                logging.debug("Disconnected Redis.")
        except Exception as e:
            logging.warning(f"Failed to disconnect Redis: {e}")

        try:
            if self.chroma_client and hasattr(self.chroma_client, "close"):
                await self.chroma_client.close()
                logging.debug("Disconnected ChromaDB.")
        except Exception as e:
            logging.warning(f"Failed to disconnect ChromaDB: {e}")

        try:
            if self.rabbitmq_connection:
                await self.rabbitmq_connection.close()
                logging.debug("Disconnected RabbitMQ.")
        except Exception as e:
            logging.warning(f"Failed to disconnect RabbitMQ: {e}")

    def _validate_config_keys(self, keys):
        for key in keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")
