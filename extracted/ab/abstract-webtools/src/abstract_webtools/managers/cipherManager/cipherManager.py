# ssl_manager.py
from ..imports import *

class CipherManager:
    @staticmethod
    def get_default_ciphers() -> list:
        return ['ECDHE-ECDSA-AES128-SHA256',
                'ECDHE-RSA-AES256-SHA',
                'ECDHE-RSA-AES256-SHA384',
                'ECDHE-RSA-CHACHA20-POLY1305',
                'ECDHE-ECDSA-CHACHA20-POLY1305',
                'ECDHE-ECDSA-AES256-SHA384',
                'ECDHE-ECDSA-AES128-GCM-SHA256',
                'ECDHE-RSA-AES128-GCM-SHA256',
                'AES256-SHA',
                'AES128-SHA',
                'ECDHE-RSA-AES128-SHA256',
                'ECDHE-ECDSA-AES256-SHA',
                'ECDHE-RSA-AES256-GCM-SHA384',
                'ECDHE-ECDSA-AES256-GCM-SHA384']

    def __init__(self, cipher_list=None):
        self.cipher_list = cipher_list or self.get_default_ciphers()
        if isinstance(self.cipher_list, str):
            self.cipher_list = [c.strip() for c in self.cipher_list.split(',') if c.strip()]
        self.ciphers_string = ','.join(self.cipher_list) if self.cipher_list else ''
    def add_string_list(self):
        if len(self.cipher_list)==0:
            return ''
        return','.join(self.cipher_list)
    def create_list(self):
        if self.cipher_list == None:
            self.cipher_list= []
        elif isinstance(self.cipher_list, str):
            self.cipher_list=self.cipher_list.split(',')
        if isinstance(self.cipher_list, str):
            self.cipher_list=[self.cipher_list]
class CipherManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance(cipher_list=None):
        if CipherManagerSingleton._instance is None:
            CipherManagerSingleton._instance = CipherManager(cipher_list=cipher_list)
        elif CipherManagerSingleton._instance.cipher_list != cipher_list:
            CipherManagerSingleton._instance = CipherManager(cipher_list=cipher_list)
        return CipherManagerSingleton._instance
