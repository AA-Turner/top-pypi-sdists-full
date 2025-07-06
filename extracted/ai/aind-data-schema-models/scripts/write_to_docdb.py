"""Module to publish models to docdb"""

import os
import csv
from typing import Iterator
from aind_data_access_api.document_db_ssh import (
    DocumentDbSSHClient,
    DocumentDbSSHCredentials,
)

DB_NAME = os.getenv("DB_NAME")
PATH_TO_MODELS = os.getenv("PATH_TO_MODELS")
DOCDB_READWRITE_SECRET = os.getenv("DOCDB_READWRITE_SECRET")
DOCDB_SSH_TUNNEL_SECRET = os.getenv("DOCDB_SSH_TUNNEL_SECRET")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")


def csv_to_json(csv_file_path: str) -> Iterator:
    """
    Returns Iterator of dict
    """
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            yield row


def publish_to_docdb(folder_path: str, credentials: DocumentDbSSHCredentials) -> None:
    """
    Writes models to docdb
    """
    with DocumentDbSSHClient(credentials=credentials) as doc_db_client:
        database = doc_db_client._client[doc_db_client.database_name]
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                collection_name = file_name[:-4]
                collection = database[collection_name]
                csv_file_path = os.path.join(folder_path, file_name)
                json_data = csv_to_json(csv_file_path)
                for records in json_data:
                    filter = {"name": records["name"]}
                    response = collection.update_one(filter=filter, update={"$set": records}, upsert=True)
                    print(response.raw_result)


if __name__ == "__main__":
    folder_path = PATH_TO_MODELS
    credentials = DocumentDbSSHCredentials.from_secrets_manager(
        doc_db_secret_name=DOCDB_READWRITE_SECRET,
        ssh_secret_name=DOCDB_SSH_TUNNEL_SECRET
    )
    credentials.database = DB_NAME
    publish_to_docdb(folder_path, credentials)
