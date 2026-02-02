import hashlib


class Caching:

    def __init__(self, cache):
        self._cache = cache

    def get(self, secret):
        return self._cache.get(self._hash(secret))

    def set(self, secret, value):
        return self._cache.set(self._hash(secret), value)

    def _hash(self, secret):
        hash_object = hashlib.md5(secret.encode())
        md5_hash = hash_object.hexdigest()
        return md5_hash
