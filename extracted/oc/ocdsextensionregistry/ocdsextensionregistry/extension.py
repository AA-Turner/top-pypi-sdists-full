class Extension:
    def __init__(self, data):
        """Accept a row from ``extensions.csv`` and assign values to properties."""
        #: The Id cell.
        self.id = data["Id"]
        #: The Category cell.
        self.category = data["Category"]
        #: The Core cell.
        self.core = data["Core"] == "true"

    def __repr__(self):
        return self.id

    def as_dict(self):
        """
        Return the object's properties as a dictionary.

        This method is defined to match the method in `ExtensionVersion`.
        """
        return self.__dict__
