def read_file(file_path: str) -> str:
    """
    Reads the text of a file.

    :param file_path: The path to the file
    :return:          Text contents of file
    """
    with open(file_path, "r") as f:
        contents = f.read()
    return contents
