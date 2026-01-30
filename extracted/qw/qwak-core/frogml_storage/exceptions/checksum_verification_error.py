class ChecksumVerificationError(Exception):
    def __init__(self, filename):
        super().__init__(f"Checksum verification failed for file: '{filename}'")
