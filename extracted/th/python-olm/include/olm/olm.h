# 1 "../include/olm/olm.h"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "../include/olm/olm.h"
# 19 "../include/olm/olm.h"
# 1 "dummy/stddef.h" 1
# 20 "../include/olm/olm.h" 2
# 1 "dummy/stdint.h" 1
# 21 "../include/olm/olm.h" 2

# 1 "dummy/olm/error.h" 1
# 23 "../include/olm/olm.h" 2
# 1 "../include/olm/inbound_group_session.h" 1
# 18 "../include/olm/inbound_group_session.h"
# 1 "dummy/stddef.h" 1
# 19 "../include/olm/inbound_group_session.h" 2
# 1 "dummy/stdint.h" 1
# 20 "../include/olm/inbound_group_session.h" 2

# 1 "dummy/olm/error.h" 1
# 22 "../include/olm/inbound_group_session.h" 2

# 1 "../include/olm/olm_export.h" 1
# 24 "../include/olm/inbound_group_session.h" 2





typedef struct OlmInboundGroupSession OlmInboundGroupSession;


 size_t olm_inbound_group_session_size(void);






 OlmInboundGroupSession * olm_inbound_group_session(
    void *memory
);




 const char *olm_inbound_group_session_last_error(
    const OlmInboundGroupSession *session
);




 enum OlmErrorCode olm_inbound_group_session_last_error_code(
    const OlmInboundGroupSession *session
);


 size_t olm_clear_inbound_group_session(
    OlmInboundGroupSession *session
);


 size_t olm_pickle_inbound_group_session_length(
    const OlmInboundGroupSession *session
);
# 75 "../include/olm/inbound_group_session.h"
 size_t olm_pickle_inbound_group_session(
    OlmInboundGroupSession *session,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);
# 91 "../include/olm/inbound_group_session.h"
 size_t olm_unpickle_inbound_group_session(
    OlmInboundGroupSession *session,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);
# 108 "../include/olm/inbound_group_session.h"
 size_t olm_init_inbound_group_session(
    OlmInboundGroupSession *session,

    uint8_t const * session_key, size_t session_key_length
);
# 123 "../include/olm/inbound_group_session.h"
 size_t olm_import_inbound_group_session(
    OlmInboundGroupSession *session,


    uint8_t const * session_key, size_t session_key_length
);
# 140 "../include/olm/inbound_group_session.h"
 size_t olm_group_decrypt_max_plaintext_length(
    OlmInboundGroupSession *session,
    uint8_t * message, size_t message_length
);
# 164 "../include/olm/inbound_group_session.h"
 size_t olm_group_decrypt(
    OlmInboundGroupSession *session,



    uint8_t * message, size_t message_length,


    uint8_t * plaintext, size_t max_plaintext_length,
    uint32_t * message_index
);





 size_t olm_inbound_group_session_id_length(
    const OlmInboundGroupSession *session
);
# 192 "../include/olm/inbound_group_session.h"
 size_t olm_inbound_group_session_id(
    OlmInboundGroupSession *session,
    uint8_t * id, size_t id_length
);




 uint32_t olm_inbound_group_session_first_known_index(
    const OlmInboundGroupSession *session
);
# 213 "../include/olm/inbound_group_session.h"
 int olm_inbound_group_session_is_verified(
    const OlmInboundGroupSession *session
);




 size_t olm_export_inbound_group_session_length(
    const OlmInboundGroupSession *session
);
# 236 "../include/olm/inbound_group_session.h"
 size_t olm_export_inbound_group_session(
    OlmInboundGroupSession *session,
    uint8_t * key, size_t key_length, uint32_t message_index
);
# 24 "../include/olm/olm.h" 2
# 1 "../include/olm/outbound_group_session.h" 1
# 18 "../include/olm/outbound_group_session.h"
# 1 "dummy/stddef.h" 1
# 19 "../include/olm/outbound_group_session.h" 2
# 1 "dummy/stdint.h" 1
# 20 "../include/olm/outbound_group_session.h" 2

# 1 "dummy/olm/error.h" 1
# 22 "../include/olm/outbound_group_session.h" 2







typedef struct OlmOutboundGroupSession OlmOutboundGroupSession;


 size_t olm_outbound_group_session_size(void);






 OlmOutboundGroupSession * olm_outbound_group_session(
    void *memory
);




 const char *olm_outbound_group_session_last_error(
    const OlmOutboundGroupSession *session
);




 enum OlmErrorCode olm_outbound_group_session_last_error_code(
    const OlmOutboundGroupSession *session
);


 size_t olm_clear_outbound_group_session(
    OlmOutboundGroupSession *session
);


 size_t olm_pickle_outbound_group_session_length(
    const OlmOutboundGroupSession *session
);
# 75 "../include/olm/outbound_group_session.h"
 size_t olm_pickle_outbound_group_session(
    OlmOutboundGroupSession *session,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);
# 91 "../include/olm/outbound_group_session.h"
 size_t olm_unpickle_outbound_group_session(
    OlmOutboundGroupSession *session,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);



 size_t olm_init_outbound_group_session_random_length(
    const OlmOutboundGroupSession *session
);






 size_t olm_init_outbound_group_session(
    OlmOutboundGroupSession *session,
    uint8_t *random, size_t random_length
);




 size_t olm_group_encrypt_message_length(
    OlmOutboundGroupSession *session,
    size_t plaintext_length
);







 size_t olm_group_encrypt(
    OlmOutboundGroupSession *session,
    uint8_t const * plaintext, size_t plaintext_length,
    uint8_t * message, size_t message_length
);





 size_t olm_outbound_group_session_id_length(
    const OlmOutboundGroupSession *session
);
# 149 "../include/olm/outbound_group_session.h"
 size_t olm_outbound_group_session_id(
    OlmOutboundGroupSession *session,
    uint8_t * id, size_t id_length
);







 uint32_t olm_outbound_group_session_message_index(
    OlmOutboundGroupSession *session
);




 size_t olm_outbound_group_session_key_length(
    const OlmOutboundGroupSession *session
);
# 181 "../include/olm/outbound_group_session.h"
 size_t olm_outbound_group_session_key(
    OlmOutboundGroupSession *session,
    uint8_t * key, size_t key_length
);
# 25 "../include/olm/olm.h" 2







static const size_t OLM_MESSAGE_TYPE_PRE_KEY = 0;
static const size_t OLM_MESSAGE_TYPE_MESSAGE = 1;

typedef struct OlmAccount OlmAccount;
typedef struct OlmSession OlmSession;
typedef struct OlmUtility OlmUtility;




 void olm_get_library_version(uint8_t *major, uint8_t *minor, uint8_t *patch);


 size_t olm_account_size(void);


 size_t olm_session_size(void);


 size_t olm_utility_size(void);



 OlmAccount * olm_account(
    void * memory
);



 OlmSession * olm_session(
    void * memory
);



 OlmUtility * olm_utility(
    void * memory
);


 size_t olm_error(void);



 const char * olm_account_last_error(
    OlmAccount const * account
);


 enum OlmErrorCode olm_account_last_error_code(
    OlmAccount const * account
);



 const char * olm_session_last_error(
    OlmSession const * session
);


 enum OlmErrorCode olm_session_last_error_code(
    OlmSession const * session
);



 const char * olm_utility_last_error(
    OlmUtility const * utility
);


 enum OlmErrorCode olm_utility_last_error_code(
    OlmUtility const * utility
);


 size_t olm_clear_account(
    OlmAccount * account
);


 size_t olm_clear_session(
    OlmSession * session
);


 size_t olm_clear_utility(
    OlmUtility * utility
);


 size_t olm_pickle_account_length(
    OlmAccount const * account
);


 size_t olm_pickle_session_length(
    OlmSession const * session
);






 size_t olm_pickle_account(
    OlmAccount * account,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);






 size_t olm_pickle_session(
    OlmSession * session,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);







 size_t olm_unpickle_account(
    OlmAccount * account,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);







 size_t olm_unpickle_session(
    OlmSession * session,
    void const * key, size_t key_length,
    void * pickled, size_t pickled_length
);


 size_t olm_create_account_random_length(
    OlmAccount const * account
);




 size_t olm_create_account(
    OlmAccount * account,
    void * random, size_t random_length
);


 size_t olm_account_identity_keys_length(
    OlmAccount const * account
);





 size_t olm_account_identity_keys(
    OlmAccount * account,
    void * identity_keys, size_t identity_key_length
);



 size_t olm_account_signature_length(
    OlmAccount const * account
);




 size_t olm_account_sign(
    OlmAccount * account,
    void const * message, size_t message_length,
    void * signature, size_t signature_length
);


 size_t olm_account_one_time_keys_length(
    OlmAccount const * account
);
# 243 "../include/olm/olm.h"
 size_t olm_account_one_time_keys(
    OlmAccount * account,
    void * one_time_keys, size_t one_time_keys_length
);
# 255 "../include/olm/olm.h"
 size_t olm_account_mark_keys_as_published(
    OlmAccount * account
);


 size_t olm_account_max_number_of_one_time_keys(
    OlmAccount const * account
);



 size_t olm_account_generate_one_time_keys_random_length(
    OlmAccount const * account,
    size_t number_of_keys
);





 size_t olm_account_generate_one_time_keys(
    OlmAccount * account,
    size_t number_of_keys,
    void * random, size_t random_length
);


 size_t olm_account_generate_fallback_key_random_length(
    OlmAccount const * account
);




 size_t olm_account_generate_fallback_key(
    OlmAccount * account,
    void * random, size_t random_length
);



 size_t olm_account_fallback_key_length(
    OlmAccount const * account
);


 size_t olm_account_fallback_key(
    OlmAccount * account,
    void * fallback_key, size_t fallback_key_size
);



 size_t olm_account_unpublished_fallback_key_length(
    OlmAccount const * account
);



 size_t olm_account_unpublished_fallback_key(
    OlmAccount * account,
    void * fallback_key, size_t fallback_key_size
);






 void olm_account_forget_old_fallback_key(
    OlmAccount * account
);



 size_t olm_create_outbound_session_random_length(
    OlmSession const * session
);






 size_t olm_create_outbound_session(
    OlmSession * session,
    OlmAccount const * account,
    void const * their_identity_key, size_t their_identity_key_length,
    void const * their_one_time_key, size_t their_one_time_key_length,
    void * random, size_t random_length
);
# 355 "../include/olm/olm.h"
 size_t olm_create_inbound_session(
    OlmSession * session,
    OlmAccount * account,
    void * one_time_key_message, size_t message_length
);




 size_t olm_create_inbound_session_from(
    OlmSession * session,
    OlmAccount * account,
    void const * their_identity_key, size_t their_identity_key_length,
    void * one_time_key_message, size_t message_length
);


 size_t olm_session_id_length(
    OlmSession const * session
);




 size_t olm_session_id(
    OlmSession * session,
    void * id, size_t id_length
);

 int olm_session_has_received_message(
    OlmSession const *session
);
# 395 "../include/olm/olm.h"
 void olm_session_describe(OlmSession * session, char *buf, size_t buflen);
# 406 "../include/olm/olm.h"
 size_t olm_matches_inbound_session(
    OlmSession * session,
    void * one_time_key_message, size_t message_length
);
# 420 "../include/olm/olm.h"
 size_t olm_matches_inbound_session_from(
    OlmSession * session,
    void const * their_identity_key, size_t their_identity_key_length,
    void * one_time_key_message, size_t message_length
);




 size_t olm_remove_one_time_keys(
    OlmAccount * account,
    OlmSession * session
);





 size_t olm_encrypt_message_type(
    OlmSession const * session
);


 size_t olm_encrypt_random_length(
    OlmSession const * session
);



 size_t olm_encrypt_message_length(
    OlmSession const * session,
    size_t plaintext_length
);







 size_t olm_encrypt(
    OlmSession * session,
    void const * plaintext, size_t plaintext_length,
    void * random, size_t random_length,
    void * message, size_t message_length
);
# 475 "../include/olm/olm.h"
 size_t olm_decrypt_max_plaintext_length(
    OlmSession * session,
    size_t message_type,
    void * message, size_t message_length
);
# 492 "../include/olm/olm.h"
 size_t olm_decrypt(
    OlmSession * session,
    size_t message_type,
    void * message, size_t message_length,
    void * plaintext, size_t max_plaintext_length
);


 size_t olm_sha256_length(
   OlmUtility const * utility
);




 size_t olm_sha256(
    OlmUtility * utility,
    void const * input, size_t input_length,
    void * output, size_t output_length
);




 size_t olm_ed25519_verify(
    OlmUtility * utility,
    void const * key, size_t key_length,
    void const * message, size_t message_length,
    void * signature, size_t signature_length
);
void *memset(void *s, int c, size_t n);
