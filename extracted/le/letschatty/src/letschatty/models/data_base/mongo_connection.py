from ..base_models.singleton import SingletonMeta
from pymongo import MongoClient
from typing import Optional
import os
import atexit

class MongoConnection(metaclass=SingletonMeta):
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        uri_base: Optional[str] = None,
        instance: Optional[str] = None
    ):
        self.username = username or os.getenv('MONGO_USERNAME')
        self.password = password or os.getenv('MONGO_PASSWORD')
        self.uri_base = uri_base or os.getenv('MONGO_URI_BASE')
        self.instance = instance or os.getenv('MONGO_INSTANCE_COMPONENT')
        
        if not all([self.username, self.password, self.uri_base, self.instance]):
            raise ValueError("Missing required MongoDB connection parameters")
            
        uri = f"{self.uri_base}://{self.username}:{self.password}@{self.instance}.mongodb.net"
        self.client = MongoClient(uri)
        try:
            self.client.admin.command('ping')
        except Exception as e:
            self.client.close()
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

        atexit.register(self.close)
    
    def close(self) -> None:
        if hasattr(self, 'client'):
            self.client.close()
