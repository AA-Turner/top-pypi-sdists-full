import os
import base64
import json
import datetime
from cryptography.fernet import Fernet
from pymongo import MongoClient
from hashlib import sha256

class CredentialStorage:
    def __init__(self, mongo_uri, db_name="credential_db", collection_name="credentials", secret_key=None):
        if secret_key is None:
            raise ValueError("Secret key must be provided for encryption.")

        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]
        self.fernet = Fernet(self._generate_fernet_key(secret_key))

    def _generate_fernet_key(self, secret_key):
        key = sha256(secret_key.encode()).digest()
        return base64.urlsafe_b64encode(key[:32])

    def save(self, credential_id, data):
        try:
            encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
            document = {
                "_id": credential_id,
                "data": encrypted_data,
                "created_at": datetime.datetime.now(datetime.timezone.utc) 
            }
            self.collection.replace_one({"_id": credential_id}, document, upsert=True)
        except Exception as e:
            raise CredentialStorageError(str(e))

    def load(self, credential_id):
        try:
            record = self.collection.find_one({"_id": credential_id})
            if record is None:
                raise FileNotFoundError(f"Credential '{credential_id}' not found.")
            encrypted_data = record["data"]
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except FileNotFoundError:
            raise
        except Exception as e:
            raise CredentialStorageError(str(e))

    def delete(self, credential_id):
        self.collection.delete_one({"_id": credential_id})

    def list_ids(self):
        return [doc["_id"] for doc in self.collection.find({}, {"_id": 1})]

class CredentialManager:
    def __init__(self, secret_key, mongo_uri, db_name="credential_db", collection_name="credentials"):
        self.storage = CredentialStorage(
            mongo_uri=mongo_uri,
            db_name=db_name,
            collection_name=collection_name,
            secret_key=secret_key
        )

    def register(self, credential_id, credential_data):
        self.storage.save(credential_id, credential_data)

    def get_credentials(self, credential_id):
        try:
            return self.storage.load(credential_id)
        except FileNotFoundError:
            raise CredentialNotFound(f"Credential '{credential_id}' not found.")

    def delete(self, credential_id):
        self.storage.delete(credential_id)

    def list_credentials(self):
        return self.storage.list_ids()

class SecureCredential:
    def __init__(self, credential_data: dict):
        self._credential_data = credential_data
        self._consumed = False

    def __enter__(self):
        return self._credential_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._wipe()

    def _wipe(self):
        if not self._consumed:
            for key in list(self._credential_data.keys()):
                random_data = os.urandom(len(str(self._credential_data[key])))
                self._credential_data[key] = random_data.hex()
            self._credential_data.clear()
            self._consumed = True

class CredentialStorageError(Exception):
    pass

class CredentialNotFound(Exception):
    pass
