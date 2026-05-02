class SpotifyError(Exception):
    pass

class StatusCodeError(SpotifyError):
    def __init__(self, status_code):
        super().__init__('Error! API returned error code ' + status_code)
        self.status_code = status_code
