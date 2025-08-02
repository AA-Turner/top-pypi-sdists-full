from typing import Generator, List


def chunk_list(
    input_list: List[str], chunk_size: int
) -> Generator[List[str], None, None]:
    """Splits a list into chunks of specified size."""
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]


def split_list_str(input_str: str, delimiter: str = ",") -> List[str]:
    """Splits a string into a list of strings based on a delimiter. Filters out empty strings."""
    return [s for s in input_str.split(delimiter) if s.strip() != ""]
