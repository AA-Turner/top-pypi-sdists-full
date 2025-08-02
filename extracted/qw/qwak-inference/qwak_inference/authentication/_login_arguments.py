from typing import Optional


class LoginArguments:
    is_anonymous: bool = False
    server_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    access_token: Optional[str] = None
    artifactory_url: Optional[str] = None

    def __eq__(self, __value):
        if not isinstance(__value, LoginArguments):
            return False
        return (
            self.is_anonymous == __value.is_anonymous
            and self.server_id == __value.server_id
            and self.username == __value.username
            and self.password == __value.password
            and self.access_token == __value.access_token
            and self.artifactory_url == __value.artifactory_url
        )
