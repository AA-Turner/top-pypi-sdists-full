class TokenData(object):
    def __init__(self, subject, role, server, customer_id=None):
        self.subject = subject or ""
        self.customerId = customer_id or self.subject.split("@")[0]
        self.role = role
        self.server = server
        self.validation_errors = []

    def is_valid(self):
        return not self.validation_errors
