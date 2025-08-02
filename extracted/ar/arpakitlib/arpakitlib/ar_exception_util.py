import traceback

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def exception_to_traceback_str(exception: BaseException) -> str:
    return "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))


def __example():
    try:
        raise Exception()
    except Exception as exception:
        print(exception_to_traceback_str(exception))


if __name__ == '__main__':
    __example()
