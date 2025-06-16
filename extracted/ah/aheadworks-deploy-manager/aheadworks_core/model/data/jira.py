
class JiraConfig:
    def __init__(self, user, token, url=None):
        if url is None:
            self.url = 'https://aheadworks.atlassian.net'

        self.auth_type = 'auth'
        self.user = user
        self.token = token
