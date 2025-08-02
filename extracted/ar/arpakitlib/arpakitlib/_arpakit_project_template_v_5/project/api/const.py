from arpakitlib.ar_enumeration_util import Enumeration


class APIErrorCodes(Enumeration):
    cannot_authorize = "CANNOT_AUTHORIZE"
    unknown_error = "UNKNOWN_ERROR"
    error_in_request = "ERROR_IN_REQUEST"
    not_found = "NOT_FOUND"


class APIErrorSpecificationCodes(Enumeration):
    pass


if __name__ == '__main__':
    print(APIErrorCodes.str_for_print())
    print()
    print(APIErrorSpecificationCodes.str_for_print())
