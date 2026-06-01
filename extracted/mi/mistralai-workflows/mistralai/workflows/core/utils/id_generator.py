import uuid


def generate_two_part_id(primary_seed: str | None, secondary_seed: str | None = None) -> str:
    """Generates a unique ID composed of two parts derived from seeds.

    Args:
        primary_seed: Optional string seed for the first part of the ID.
                      If not provided, a random UUID will be used.
        secondary_seed: Optional string seed for the second part of the ID.
                        If not provided, a random UUID will be used.

    Returns:
        A unique ID string combining both parts without separators.
    """
    if not primary_seed:
        primary_seed = uuid.uuid4().hex
    if not secondary_seed:
        secondary_seed = uuid.uuid4().hex
    first_part = uuid.uuid5(uuid.NAMESPACE_DNS, primary_seed).hex
    second_part = uuid.uuid5(uuid.NAMESPACE_DNS, secondary_seed).hex
    return f"{first_part}{second_part}".replace("-", "")
