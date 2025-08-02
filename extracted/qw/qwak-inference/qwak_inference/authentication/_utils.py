from requests.auth import AuthBase


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

    def __eq__(self, other):
        if not isinstance(other, BearerAuth):
            return False
        return self.token == other.token


class EmptyAuth(AuthBase):
    def __call__(self, r):
        return r
