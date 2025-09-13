from arpakitlib.ar_enumeration_util import Enumeration


class APIErrorCodes(Enumeration):
    class Common(Enumeration):
        cannot_authorize = "COMMON_CANNOT_AUTHORIZE".upper()
        unknown_error = "COMMON_UNKNOWN_ERROR".upper()
        error_in_request = "COMMON_ERROR_IN_REQUEST".upper()
        not_found = "COMMON_NOT_FOUND".upper()
        content_length_is_too_big = "content_length_is_too_big".upper()

    cannot_authorize = Common.cannot_authorize
    unknown_error = Common.unknown_error
    error_in_request = Common.error_in_request
    not_found = Common.not_found

    class Global(Enumeration):
        pass

    class General(Enumeration):
        pass

    class Client(Enumeration):
        error_use_referral_code = "client_error_use_referral_code"

    class Admin(Enumeration):
        error_raise_api_exception_1 = "error_admin_error_raise_api_exception_1".upper()
        error_raise_api_exception_2 = "error_admin_error_raise_api_exception_2".upper()
        error_raise_api_exception_3 = "error_admin_error_raise_api_exception_3".upper()
        error_raise_fake_error = "error_admin_raise_fake_error".upper()
        error_update_user = "error_admin_error_update_user".upper()
        error_create_user = "error_create_user"


if __name__ == '__main__':
    print(APIErrorCodes.str_for_print())
