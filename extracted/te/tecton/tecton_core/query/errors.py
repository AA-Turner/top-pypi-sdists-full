class UserDefinedTransformationError(Exception):
    """Exception that represents a user-caused error occurred during Query Tree evaluation.

    The error is usually caused by a mistake in user configuration or code and
    should be recoverable by user.
    This exception is expected to have a more comprehensive context (in message)
    to be as clear as possible.
    We will most probably drop the traceback of this exception to reduce noise.
    """

    can_drop_traceback = True

    def __init__(self, error_msg):
        self.error_msg = error_msg
        self.context_msg = None

    def with_context(self, context_msg):
        self.context_msg = context_msg
        return self

    def __str__(self):
        msg = ""
        if self.context_msg:
            msg += f"During {self.context_msg} "

        msg += "error caused by user configuration has occurred:\n"
        msg += f"{self.error_msg}\n"
        return msg


class SQLCompilationError(UserDefinedTransformationError):
    def __init__(self, error_msg, sql_query):
        super().__init__(error_msg)
        self.sql_query = sql_query

    def __str__(self):
        return super().__str__() + "Query:\n" + self._query_with_line_numbers()

    def _query_with_line_numbers(self):
        lines = self.sql_query.split("\n")
        return "\n".join(f"{line_no + 1:>3} {line}" for line_no, line in enumerate(lines))


class UserCodeError(UserDefinedTransformationError):
    def __str__(self):
        return super().__str__() + str(self.__cause__)
