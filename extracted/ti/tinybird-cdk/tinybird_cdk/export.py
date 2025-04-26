import os
import logging
from abc import ABC


class Export(ABC):
    def cleanup(self):
        pass

class Data(Export):
    def __init__(self, data):
        self.data = data

class URL(Export):
    def __init__(self, url):
        self.url = url

class LocalFile(Export):
    def __init__(self, path):
        self.path = path

    def cleanup(self):
        try:
            os.remove(self.path)
        except Exception as err:
            logging.exception(f'Error on cleanup (LocalFile): {err}')

class CloudFile(Export):
    def __init__(self, client, bucket, key):
        self.client = client
        self.bucket = bucket
        self.key = key

    def cleanup(self):
        try:
            self.client.rm(self.bucket, self.key)
        except Exception as err:
            logging.exception(f'Error on cleanup (CloudFile): {err}')

class CloudDir(Export):
    def __init__(self, client, bucket, directory):
        self.client = client
        self.bucket = bucket
        self.directory = directory

    def cleanup(self):
        try:
            self.client.rmtree(self.bucket, self.directory)
        except Exception as err:
            logging.exception(f'Error on cleanup (CloudDir): {err}')
