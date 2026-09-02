class InvalidUDMFieldError(Exception):
    """
    Exception raised for invalid UDM fields.
    """

    def __init__(self, field: str):
        self.field = field
        self.message = f"Invalid UDM field: {field}"
        super().__init__(self.message)
