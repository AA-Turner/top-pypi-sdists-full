class IdToken:
    def __init__(self, data: dict[str, any], email: str, username: str, groups: list[str] = [], iat: int = 0, nbf: int = 0, exp: int = 0):
        self.data = data
        self.email = email
        self.username = username
        self.groups = groups
        self.iat = iat
        self.nbf = nbf
        self.exp = exp

    def from_dict(j: dict[str, any]):
        return IdToken(
            j['data'],
            j['email'],
            j['username'],
            groups=j['groups'] if 'groups' in j else None,
            iat=j['iat'] if 'iat' in j else None,
            nbf=j['nbf'] if 'nbf' in j else None,
            exp=j['exp'] if 'exp' in j else None
        )

    def to_dict(self):
        return self.__dict__