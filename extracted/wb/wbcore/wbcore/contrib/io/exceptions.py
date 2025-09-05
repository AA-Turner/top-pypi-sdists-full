class DeserializationError(Exception):
    """
    Exception excepted when a deserialized error happens during the process object phase in the Handler.

    This exception won't stop the importing process and will only be logged
    """

    pass


class SkipImportError(Exception):
    """
    Exception excepted when a deserialized skip happens during the process object phase in the Handler.

    This exception won't stop the importing process and won't trigger a warning
    """


class ImportError(Exception):
    """
    Exception returns when something wrong happens during the processing of the import source and means that not all data were succesfully imported
    """

    pass
