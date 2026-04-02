# 1 "../include/olm/pk.h"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "../include/olm/pk.h"
# 19 "../include/olm/pk.h"
# 1 "dummy/stddef.h" 1
# 20 "../include/olm/pk.h" 2
# 1 "dummy/stdint.h" 1
# 21 "../include/olm/pk.h" 2

# 1 "dummy/olm/error.h" 1
# 23 "../include/olm/pk.h" 2

# 1 "../include/olm/olm_export.h" 1
# 25 "../include/olm/pk.h" 2





typedef struct OlmPkEncryption OlmPkEncryption;


 size_t olm_pk_encryption_size(void);



 OlmPkEncryption *olm_pk_encryption(
    void * memory
);



 const char * olm_pk_encryption_last_error(
    const OlmPkEncryption * encryption
);



 enum OlmErrorCode olm_pk_encryption_last_error_code(
    const OlmPkEncryption * encryption
);


 size_t olm_clear_pk_encryption(
    OlmPkEncryption *encryption
);


 size_t olm_pk_encryption_set_recipient_key(
    OlmPkEncryption *encryption,
    void const *public_key, size_t public_key_length
);



 size_t olm_pk_ciphertext_length(
    const OlmPkEncryption *encryption,
    size_t plaintext_length
);


 size_t olm_pk_mac_length(
    const OlmPkEncryption *encryption
);


 size_t olm_pk_key_length(void);


 size_t olm_pk_encrypt_random_length(
    const OlmPkEncryption *encryption
);
# 94 "../include/olm/pk.h"
 size_t olm_pk_encrypt(
    OlmPkEncryption *encryption,
    void const * plaintext, size_t plaintext_length,
    void * ciphertext, size_t ciphertext_length,
    void * mac, size_t mac_length,
    void * ephemeral_key, size_t ephemeral_key_size,
    const void * random, size_t random_length
);

typedef struct OlmPkDecryption OlmPkDecryption;


 size_t olm_pk_decryption_size(void);



 OlmPkDecryption *olm_pk_decryption(
    void * memory
);



 const char * olm_pk_decryption_last_error(
    const OlmPkDecryption * decryption
);



 enum OlmErrorCode olm_pk_decryption_last_error_code(
    const OlmPkDecryption * decryption
);


 size_t olm_clear_pk_decryption(
    OlmPkDecryption *decryption
);



 size_t olm_pk_private_key_length(void);



 size_t olm_pk_generate_key_random_length(void);
# 149 "../include/olm/pk.h"
 size_t olm_pk_key_from_private(
    OlmPkDecryption * decryption,
    void * pubkey, size_t pubkey_length,
    const void * privkey, size_t privkey_length
);



 size_t olm_pk_generate_key(
    OlmPkDecryption * decryption,
    void * pubkey, size_t pubkey_length,
    const void * privkey, size_t privkey_length
);


 size_t olm_pickle_pk_decryption_length(
    const OlmPkDecryption * decryption
);






 size_t olm_pickle_pk_decryption(
    OlmPkDecryption * decryption,
    void const * key, size_t key_length,
    void *pickled, size_t pickled_length
);
# 186 "../include/olm/pk.h"
 size_t olm_unpickle_pk_decryption(
    OlmPkDecryption * decryption,
    void const * key, size_t key_length,
    void *pickled, size_t pickled_length,
    void *pubkey, size_t pubkey_length
);



 size_t olm_pk_max_plaintext_length(
    const OlmPkDecryption * decryption,
    size_t ciphertext_length
);






 size_t olm_pk_decrypt(
    OlmPkDecryption * decryption,
    void const * ephemeral_key, size_t ephemeral_key_length,
    void const * mac, size_t mac_length,
    void * ciphertext, size_t ciphertext_length,
    void * plaintext, size_t max_plaintext_length
);
# 221 "../include/olm/pk.h"
 size_t olm_pk_get_private_key(
    OlmPkDecryption * decryption,
    void *private_key, size_t private_key_length
);

typedef struct OlmPkSigning OlmPkSigning;


 size_t olm_pk_signing_size(void);



 OlmPkSigning *olm_pk_signing(
    void * memory
);



 const char * olm_pk_signing_last_error(
    const OlmPkSigning * sign
);



 enum OlmErrorCode olm_pk_signing_last_error_code(
    const OlmPkSigning * sign
);


 size_t olm_clear_pk_signing(
    OlmPkSigning *sign
);
# 262 "../include/olm/pk.h"
 size_t olm_pk_signing_key_from_seed(
    OlmPkSigning * sign,
    void * pubkey, size_t pubkey_length,
    const void * seed, size_t seed_length
);




 size_t olm_pk_signing_seed_length(void);




 size_t olm_pk_signing_public_key_length(void);




 size_t olm_pk_signature_length(void);






 size_t olm_pk_sign(
    OlmPkSigning *sign,
    uint8_t const * message, size_t message_length,
    uint8_t * signature, size_t signature_length
);
