class Application:
    """
    Class representing an application
    """

    def __init__(self, name: str, opaque_id: str):
        self.name = name
        self.opaque_id = opaque_id

    def __str__(self) -> str:
        return f"Application(name={self.name}, opaque_id={self.opaque_id})"

    def __repr__(self) -> str:
        return self.__str__()
