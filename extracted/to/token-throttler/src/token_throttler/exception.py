class TokenThrottlerException(Exception):
    """Exception raised once there are no more tokens inside TokenThrottler's bucket(s)"""

    def __init__(self):
        self.message = "Tokens exceeded"
        super().__init__(self.message)
