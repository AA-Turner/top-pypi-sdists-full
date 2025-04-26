import json


class PersistentFieldLogger:
    """
    Wrapper for logging.logger or equivalent, will track useful metrics defined in persistent_fields in a specified
    Dictionary.

    Useful when processing specific files, create a logger with a persistent field of the filename, pass the filename
    and then all subsequent messages against that logger will contain the filename.

    """
    def __init__(self, logger, persistent_fields, sep=" ", message_key="message"):
        """
        :param logger: logger object
        :param persistent_fields: dictionary with key value pairs for to be logged out with every call to the logger
        :param sep: separator used
        :param message_key: key to use for the message in the logger
        """
        self.logger = logger
        self.persistent_fields = persistent_fields
        self.sep = sep
        self._message_key = message_key

    def set_field_value(self, field, value):
        """
        Add or override a field which is persistently logged - will raise if object is not JSON serializable
        :param field: name of field
        :param value: value to assign - must be JSON serializable
        :return: None
        """
        json.dumps({field: value})  # This will raise if it will not serialize
        self.persistent_fields = {**self.persistent_fields, field: value}

    def set_multiple_values(self, fields_and_values):
        """
        Allows multiple keys and values to be added or overridden in a PersistentFieldLogger object
        :param fields_and_values: dictionary with keys and values to add/override, must be JSON serializable
        :return: None
        """
        json.dumps(fields_and_values)   # This will raise if it will not serialize
        self.persistent_fields = {**self.persistent_fields, **fields_and_values}

    def _get_args(self, *args, **kwargs):

        all_args = self.persistent_fields.copy()
        for arg in kwargs:
            if arg in self.persistent_fields:
                self.persistent_fields[arg] = kwargs[arg]
            all_args[arg] = kwargs[arg]
        for message in args:
            if not isinstance(message, str):
                raise ValueError("Logging methods only accepts string values as args, or keyword arguments")
            if self._message_key in all_args:
                all_args[self._message_key] += self.sep + message
            else:
                all_args[self._message_key] = message

        return all_args

    def debug(self, *args, **kwargs):
        self.logger.debug(json.dumps(self._get_args(*args, **kwargs)))

    def info(self, *args, **kwargs):
        self.logger.info(json.dumps(self._get_args(*args, **kwargs)))

    def warning(self, *args, **kwargs):
        self.logger.warning(json.dumps(self._get_args(*args, **kwargs)))

    def error(self, *args, **kwargs):
        self.logger.error(json.dumps(self._get_args(*args, **kwargs)))
