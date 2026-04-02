# 1 "../include/olm/error.h"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "../include/olm/error.h"
# 18 "../include/olm/error.h"
# 1 "../include/olm/olm_export.h" 1
# 19 "../include/olm/error.h" 2





enum OlmErrorCode {
    OLM_SUCCESS = 0,
    OLM_NOT_ENOUGH_RANDOM = 1,
    OLM_OUTPUT_BUFFER_TOO_SMALL = 2,
    OLM_BAD_MESSAGE_VERSION = 3,
    OLM_BAD_MESSAGE_FORMAT = 4,
    OLM_BAD_MESSAGE_MAC = 5,
    OLM_BAD_MESSAGE_KEY_ID = 6,
    OLM_INVALID_BASE64 = 7,
    OLM_BAD_ACCOUNT_KEY = 8,
    OLM_UNKNOWN_PICKLE_VERSION = 9,
    OLM_CORRUPTED_PICKLE = 10,

    OLM_BAD_SESSION_KEY = 11,

    OLM_UNKNOWN_MESSAGE_INDEX = 12,
# 49 "../include/olm/error.h"
    OLM_BAD_LEGACY_ACCOUNT_PICKLE = 13,




    OLM_BAD_SIGNATURE = 14,

    OLM_INPUT_BUFFER_TOO_SMALL = 15,




    OLM_SAS_THEIR_KEY_NOT_SET = 16,





    OLM_PICKLE_EXTRA_DATA = 17,



};


 const char * _olm_error_to_string(enum OlmErrorCode error);
