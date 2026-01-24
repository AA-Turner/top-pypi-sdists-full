from pyspark.errors.exceptions.base import (
    AnalysisException,
    ArithmeticException,
    ArrayIndexOutOfBoundsException,
    DateTimeException,
    IllegalArgumentException,
    NumberFormatException,
    ParseException,
    PySparkException,
    PySparkTypeError,
    PySparkValueError,
    PythonException,
    SparkRuntimeException,
)

# We change the module so that these exceptions are shown as pyspark exceptions in the client
AnalysisException.__module__ = ArithmeticException.__module__ = ArrayIndexOutOfBoundsException.__module__ = \
    DateTimeException.__module__ = IllegalArgumentException.__module__ = NumberFormatException.__module__ = \
    ParseException.__module__ = PySparkException.__module__ = PySparkTypeError.__module__ = \
    PySparkValueError.__module__ = PythonException.__module__ = \
    SparkRuntimeException.__module__ = "pyspark.errors.exceptions.base"
