from esi.http_utils import pascal_case_string  # noqa: F401 re-exported for backwards compatibility
from esi.models import Token


def get_token(character_id: int, scopes: list) -> Token:
    """Helper method to get a valid token for a specific character with specific scopes.

    Args:
        character_id: Character to filter on.
        scopes: array of ESI scope strings to search for.

    Returns:
        Matching Token
    """
    qs = (
        Token.objects
        .filter(character_id=character_id)
        .require_scopes(scopes)
        .require_valid()
    )
    token = qs.first()
    if token is None:
        raise Token.DoesNotExist(
            f"No valid token found for character_id={character_id} with required scopes."
        )
    return token
