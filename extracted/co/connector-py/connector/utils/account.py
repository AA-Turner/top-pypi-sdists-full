"""Account related utility functions."""


def full_name(given_name: str | None, family_name: str | None) -> str:
    """Get full name."""
    return " ".join(filter(None, (given_name, family_name))).strip()


def split_name(name: str | None) -> tuple[str | None, str | None]:
    """Split name into given and family name.

    This is meant to be used when transforming a full name from APIs to our FoundAccountData.

    Example usage in a user model DTO:
    ```
    def to_account(self) -> FoundAccountData:
        given_name, family_name = split_name(self.name)
        return FoundAccountData(
            given_name=given_name,
            family_name=family_name,
            ...
        )
    ```
    """
    if name is None:
        return None, None

    try:
        given_name, family_name = name.split(" ", maxsplit=1)
    except ValueError:
        given_name = name
        family_name = None

    return given_name, family_name
