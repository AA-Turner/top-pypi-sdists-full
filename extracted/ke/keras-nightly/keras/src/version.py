from keras.src.api_export import keras_export

# Unique source of truth for the version number.
__version__ = "3.15.0.dev2026061005"


@keras_export("keras.version")
def version():
    return __version__
