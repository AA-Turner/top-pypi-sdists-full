def version_add(versions: str) -> str:
    separator: str = '.'
    array: list = versions.split('.')
    last_item: int = int(array[2])
    last_item += 1
    array[2]: str = str(last_item)
    versions = separator.join(array)
    return versions


def get_version() -> str:
    with open('VERSION', 'r') as stream:
        versions: str = stream.readline()
    return versions


def set_version(versions: str):
    with open('VERSION', 'w') as stream:
        stream.write(versions)


def main():
    version_old: str = get_version()
    version_new: str = version_add(version_old)
    set_version(version_new)
    version_add(version_new)
    version_new: str = get_version()
    if version_old != version_new:
        print("version changed")
    else:
        print("ERR: version not changed")
