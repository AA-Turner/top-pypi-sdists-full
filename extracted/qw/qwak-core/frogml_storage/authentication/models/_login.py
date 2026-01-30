from typing import Optional


class LoginArguments(object):
    isAnonymous: bool = False
    server_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    access_token: Optional[str] = None
    artifactory_url: Optional[str] = None

    def __eq__(self, other):
        if not isinstance(other, LoginArguments):
            return False
        return (
            self.isAnonymous == other.isAnonymous
            and self.server_id == other.server_id
            and self.username == other.username
            and self.password == other.password
            and self.access_token == other.access_token
            and self.artifactory_url == other.artifactory_url
        )
