import typing


def to_nested_dict(
    data: typing.Mapping[str, typing.Mapping | typing.Any], keysep: str
) -> dict[str, dict | typing.Any]:
    """
    Converts a dictionary with composite keys separated by
    a specified separator into a nested dictionary.
    The function handles nested dictionaries recursively.

    Example:
    ```
    init_dict = {
        'a/b/c': 1,
        'a/b/d': {'e': 1},
        'a/b/f': {'g/h': 1}
    }
    to_nested_dict(init_dict, sep='/')
    >>> {'a': {'b': {'c': 1, 'd': {'e': 1}, 'f': {'g': {'h': 1}}}}}
    ```

    Args:
        data (typing.Mapping[str, typing.Mapping | typing.Any]):
        Dictionary to be converted. Keys are strings with a separator.
        sep (str): Separator used in the keys of the dictionary.

    Returns:
        dict[str, dict | typing.Any]: Nested dictionary where
        the structure is defined by the composite keys.
    """

    def recursive_convert(data: dict | typing.Any) -> dict | typing.Any:
        if not isinstance(data, dict):
            return data
        return {
            key: recursive_convert(value)
            for key, value in to_nested_dict(data, keysep).items()
            }

    nested_dict: dict[str, dict | typing.Any] = {}
    for key, value in data.items():
        keys = key.split(keysep)
        sub_dict = nested_dict
        for sub_key in keys[:-1]:
            sub_dict = sub_dict.setdefault(sub_key, {})
        sub_dict[keys[-1]] = recursive_convert(value)
    return nested_dict
