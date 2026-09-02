// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Base32 encoding/decoding (RFC 4648)

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static const char base32_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

uint8_t* base32_encode(const uint8_t* src, size_t len, size_t* out_len) {
    *out_len = ((len + 4) / 5) * 8;
    uint8_t* encoded = malloc(*out_len + 1);
    if (encoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    for (size_t i = 0, j = 0; i < len;) {
        uint32_t octet0 = i < len ? src[i++] : 0;
        uint32_t octet1 = i < len ? src[i++] : 0;
        uint32_t octet2 = i < len ? src[i++] : 0;
        uint32_t octet3 = i < len ? src[i++] : 0;
        uint32_t octet4 = i < len ? src[i++] : 0;

        encoded[j++] = base32_chars[octet0 >> 3];
        encoded[j++] = base32_chars[((octet0 & 0x07) << 2) | (octet1 >> 6)];
        encoded[j++] = base32_chars[(octet1 >> 1) & 0x1F];
        encoded[j++] = base32_chars[((octet1 & 0x01) << 4) | (octet2 >> 4)];
        encoded[j++] = base32_chars[((octet2 & 0x0F) << 1) | (octet3 >> 7)];
        encoded[j++] = base32_chars[(octet3 >> 2) & 0x1F];
        encoded[j++] = base32_chars[((octet3 & 0x03) << 3) | (octet4 >> 5)];
        encoded[j++] = base32_chars[octet4 & 0x1F];
    }

    if (len % 5 != 0) {
        size_t padding = 7 - (len % 5) * 8 / 5;
        for (size_t i = 0; i < padding; i++) {
            encoded[*out_len - padding + i] = '=';
        }
    }

    encoded[*out_len] = '\0';
    return encoded;
}

uint8_t* base32_decode(const uint8_t* src, size_t len, size_t* out_len) {
    while (len > 0 && src[len - 1] == '=') {
        len--;
    }
    *out_len = len * 5 / 8;
    uint8_t* decoded = malloc(*out_len);
    if (decoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    size_t bits = 0, value = 0, count = 0;
    for (size_t i = 0; i < len; i++) {
        uint8_t c = src[i];
        if (c >= 'A' && c <= 'Z') {
            c -= 'A';
        } else if (c >= '2' && c <= '7') {
            c -= '2' - 26;
        } else {
            continue;
        }
        value = (value << 5) | c;
        bits += 5;
        if (bits >= 8) {
            decoded[count++] = (uint8_t)(value >> (bits - 8));
            bits -= 8;
        }
    }
    if (bits >= 5 || (value & ((1 << bits) - 1)) != 0) {
        free(decoded);
        return NULL;
    }
    *out_len = count;
    return decoded;
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Base64 encoding/decoding (RFC 4648)

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static const char base64_chars[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

uint8_t* base64_encode(const uint8_t* src, size_t len, size_t* out_len) {
    uint8_t* encoded = NULL;
    size_t i, j;
    uint32_t octets;

    *out_len = ((len + 2) / 3) * 4;
    encoded = malloc(*out_len + 1);
    if (encoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    for (i = 0, j = 0; i < len; i += 3, j += 4) {
        octets =
            (src[i] << 16) | ((i + 1 < len ? src[i + 1] : 0) << 8) | (i + 2 < len ? src[i + 2] : 0);
        encoded[j] = base64_chars[(octets >> 18) & 0x3f];
        encoded[j + 1] = base64_chars[(octets >> 12) & 0x3f];
        encoded[j + 2] = base64_chars[(octets >> 6) & 0x3f];
        encoded[j + 3] = base64_chars[octets & 0x3f];
    }

    if (len % 3 == 1) {
        encoded[*out_len - 1] = '=';
        encoded[*out_len - 2] = '=';
    } else if (len % 3 == 2) {
        encoded[*out_len - 1] = '=';
    }

    encoded[*out_len] = '\0';
    return encoded;
}

static const uint8_t base64_table[] = {
    // Map base64 characters to their corresponding values
    ['A'] = 0,  ['B'] = 1,  ['C'] = 2,  ['D'] = 3,  ['E'] = 4,  ['F'] = 5,  ['G'] = 6,  ['H'] = 7,
    ['I'] = 8,  ['J'] = 9,  ['K'] = 10, ['L'] = 11, ['M'] = 12, ['N'] = 13, ['O'] = 14, ['P'] = 15,
    ['Q'] = 16, ['R'] = 17, ['S'] = 18, ['T'] = 19, ['U'] = 20, ['V'] = 21, ['W'] = 22, ['X'] = 23,
    ['Y'] = 24, ['Z'] = 25, ['a'] = 26, ['b'] = 27, ['c'] = 28, ['d'] = 29, ['e'] = 30, ['f'] = 31,
    ['g'] = 32, ['h'] = 33, ['i'] = 34, ['j'] = 35, ['k'] = 36, ['l'] = 37, ['m'] = 38, ['n'] = 39,
    ['o'] = 40, ['p'] = 41, ['q'] = 42, ['r'] = 43, ['s'] = 44, ['t'] = 45, ['u'] = 46, ['v'] = 47,
    ['w'] = 48, ['x'] = 49, ['y'] = 50, ['z'] = 51, ['0'] = 52, ['1'] = 53, ['2'] = 54, ['3'] = 55,
    ['4'] = 56, ['5'] = 57, ['6'] = 58, ['7'] = 59, ['8'] = 60, ['9'] = 61, ['+'] = 62, ['/'] = 63,
};

uint8_t* base64_decode(const uint8_t* src, size_t len, size_t* out_len) {
    if (len % 4 != 0) {
        return NULL;
    }

    size_t padding = 0;
    if (src[len - 1] == '=') {
        padding++;
    }
    if (src[len - 2] == '=') {
        padding++;
    }

    *out_len = (len / 4) * 3 - padding;
    uint8_t* decoded = malloc(*out_len);
    if (decoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    for (size_t i = 0, j = 0; i < len; i += 4, j += 3) {
        uint32_t block = 0;
        for (size_t k = 0; k < 4; k++) {
            block <<= 6;
            if (src[i + k] == '=') {
                padding--;
            } else {
                uint8_t index = base64_table[src[i + k]];
                if (index == 0 && src[i + k] != 'A') {
                    free(decoded);
                    return NULL;
                }
                block |= index;
            }
        }

        decoded[j] = (block >> 16) & 0xFF;
        if (j + 1 < *out_len) {
            decoded[j + 1] = (block >> 8) & 0xFF;
        }
        if (j + 2 < *out_len) {
            decoded[j + 2] = block & 0xFF;
        }
    }

    return decoded;
}
// Originally by Fränz Friederes, MIT License
// https://github.com/cryptii/cryptii/blob/main/src/Encoder/Ascii85.js

// Modified by Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean/

// Base85 (Ascii85) encoding/decoding

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Maximum value of a tuple (85^5 - 1 does not fit into 32 bits).
#define MAX_TUPLE UINT32_C(0xFFFFFFFF)

uint8_t* base85_encode(const uint8_t* src, size_t len, size_t* out_len) {
    // Each 4-byte group takes at most 5 characters, plus the null terminator.
    uint8_t* encoded = malloc(len * 5 / 4 + 5);
    if (encoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    // Encode each group of 4 bytes
    uint32_t digits[5], tuple;
    size_t pos = 0;
    for (size_t i = 0; i < len; i += 4) {
        // The last group may be partial
        size_t group_len = (len - i < 4) ? len - i : 4;

        // Read 32-bit unsigned integer from bytes following the
        // big-endian convention (most significant byte first),
        // padding a partial group with zero bytes
        tuple = 0;
        for (size_t j = 0; j < group_len; j++) {
            tuple |= (uint32_t)src[i + j] << (24 - 8 * j);
        }

        if (tuple == 0 && group_len == 4) {
            // An all-zero tuple is encoded as a single character.
            // Only full groups qualify: for a partial group the shorthand
            // would decode into more bytes than the source has.
            encoded[pos++] = 'z';
            continue;
        }

        // Calculate 5 digits by repeatedly dividing
        // by 85 and taking the remainder
        for (size_t j = 0; j < 5; j++) {
            digits[4 - j] = tuple % 85;
            tuple = tuple / 85;
        }

        // A group of n bytes is encoded as n+1 characters,
        // so omit the characters added due to zero padding
        for (size_t j = 0; j < group_len + 1; j++) {
            encoded[pos++] = digits[j] + 33;
        }
    }

    *out_len = pos;
    encoded[pos] = '\0';
    return encoded;
}

uint8_t* base85_decode(const uint8_t* src, size_t len, size_t* out_len) {
    // Every 'z' expands into 4 bytes, while the other characters decode
    // in groups of 5 to 4 bytes. Since 'z' is only valid at a group
    // boundary (it is rejected as a digit otherwise), the remaining
    // characters form full groups plus at most one trailing group of
    // n characters, which decodes into n-1 bytes. Both cases are covered
    // by rounding down: (5k + n) * 4 / 5 = 4k + n - 1 for 2 <= n <= 4.
    size_t n_shorthand = 0;
    for (size_t i = 0; i < len; i++) {
        if (src[i] == 'z') {
            n_shorthand++;
        }
    }
    size_t decoded_len = (len - n_shorthand) * 4 / 5 + n_shorthand * 4;

    uint8_t* decoded = malloc(decoded_len > 0 ? decoded_len : 1);
    if (decoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    uint8_t digits[5], tuple_bytes[4];
    uint64_t tuple;
    size_t pos = 0;
    for (size_t i = 0; i < len;) {
        if (src[i] == 'z') {
            // A single character encodes an all-zero tuple
            decoded[pos++] = 0;
            decoded[pos++] = 0;
            decoded[pos++] = 0;
            decoded[pos++] = 0;
            i++;
            continue;
        }

        // The last group may be partial, but a single character
        // encodes no bytes at all, so it is invalid
        size_t group_len = (len - i < 5) ? len - i : 5;
        if (group_len == 1) {
            free(decoded);
            *out_len = 0;
            return NULL;
        }

        // Retrieve radix-85 digits of tuple,
        // padding a partial group with the largest digit ('u')
        for (size_t k = 0; k < 5; k++) {
            if (k >= group_len) {
                digits[k] = 84;
                continue;
            }
            uint8_t digit = src[i + k] - 33;
            if (digit > 84) {
                free(decoded);
                *out_len = 0;
                return NULL;
            }
            digits[k] = digit;
        }

        // Create 32-bit binary number from digits and handle padding
        // tuple = a * 85^4 + b * 85^3 + c * 85^2 + d * 85 + e
        // (calculated as 64-bit, since the digits may overflow 32 bits)
        tuple = (uint64_t)digits[0] * 52200625 + (uint64_t)digits[1] * 614125 +
                (uint64_t)digits[2] * 7225 + (uint64_t)digits[3] * 85 + digits[4];
        if (tuple > MAX_TUPLE) {
            free(decoded);
            *out_len = 0;
            return NULL;
        }

        // Get bytes from tuple
        tuple_bytes[0] = (tuple >> 24) & 0xff;
        tuple_bytes[1] = (tuple >> 16) & 0xff;
        tuple_bytes[2] = (tuple >> 8) & 0xff;
        tuple_bytes[3] = tuple & 0xff;

        // Append bytes to result, dropping the ones
        // that came from the padding digits
        for (size_t k = 0; k + 1 < group_len; k++) {
            decoded[pos++] = tuple_bytes[k];
        }
        i += 5;
    }

    *out_len = pos;
    return decoded;
}
// Created by: Peter Tripp (@notpeter), Public Domain
// blake3 reference implementation, Public Domain
// https://github.com/oconnor663/blake3_reference_impl_c

#include <assert.h>
#include <memory.h>
#include <stdlib.h>
#include <string.h>

#include "crypto/blake3.h"

#define CHUNK_START 1 << 0
#define CHUNK_END 1 << 1
#define PARENT 1 << 2
#define ROOT 1 << 3
#define KEYED_HASH 1 << 4
#define DERIVE_KEY_CONTEXT 1 << 5
#define DERIVE_KEY_MATERIAL 1 << 6

static uint32_t IV[8] = {
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
};

static size_t MSG_PERMUTATION[16] = {2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8};

inline static uint32_t rotate_right(uint32_t x, int n) {
    return (x >> n) | (x << (32 - n));
}

// The mixing function, G, which mixes either a column or a diagonal.
inline static void
g(uint32_t state[16], size_t a, size_t b, size_t c, size_t d, uint32_t mx, uint32_t my) {
    state[a] = state[a] + state[b] + mx;
    state[d] = rotate_right(state[d] ^ state[a], 16);
    state[c] = state[c] + state[d];
    state[b] = rotate_right(state[b] ^ state[c], 12);
    state[a] = state[a] + state[b] + my;
    state[d] = rotate_right(state[d] ^ state[a], 8);
    state[c] = state[c] + state[d];
    state[b] = rotate_right(state[b] ^ state[c], 7);
}

inline static void round_function(uint32_t state[16], uint32_t m[16]) {
    // Mix the columns.
    g(state, 0, 4, 8, 12, m[0], m[1]);
    g(state, 1, 5, 9, 13, m[2], m[3]);
    g(state, 2, 6, 10, 14, m[4], m[5]);
    g(state, 3, 7, 11, 15, m[6], m[7]);
    // Mix the diagonals.
    g(state, 0, 5, 10, 15, m[8], m[9]);
    g(state, 1, 6, 11, 12, m[10], m[11]);
    g(state, 2, 7, 8, 13, m[12], m[13]);
    g(state, 3, 4, 9, 14, m[14], m[15]);
}

inline static void permute(uint32_t m[16]) {
    uint32_t permuted[16];
    for (size_t i = 0; i < 16; i++) {
        permuted[i] = m[MSG_PERMUTATION[i]];
    }
    memcpy(m, permuted, sizeof(permuted));
}

inline static void compress(const uint32_t chaining_value[8],
                            const uint32_t block_words[16],
                            uint64_t counter,
                            uint32_t block_len,
                            uint32_t flags,
                            uint32_t out[16]) {
    uint32_t state[16] = {
        chaining_value[0],
        chaining_value[1],
        chaining_value[2],
        chaining_value[3],
        chaining_value[4],
        chaining_value[5],
        chaining_value[6],
        chaining_value[7],
        IV[0],
        IV[1],
        IV[2],
        IV[3],
        (uint32_t)counter,
        (uint32_t)(counter >> 32),
        block_len,
        flags,
    };
    uint32_t block[16];
    memcpy(block, block_words, sizeof(block));

    round_function(state, block);  // round 1
    permute(block);
    round_function(state, block);  // round 2
    permute(block);
    round_function(state, block);  // round 3
    permute(block);
    round_function(state, block);  // round 4
    permute(block);
    round_function(state, block);  // round 5
    permute(block);
    round_function(state, block);  // round 6
    permute(block);
    round_function(state, block);  // round 7

    for (size_t i = 0; i < 8; i++) {
        state[i] ^= state[i + 8];
        state[i + 8] ^= chaining_value[i];
    }

    memcpy(out, state, sizeof(state));
}

inline static void words_from_little_endian_bytes(const void* bytes,
                                                  size_t bytes_len,
                                                  uint32_t* out) {
    assert(bytes_len % 4 == 0);
    const uint8_t* u8_ptr = (const uint8_t*)bytes;
    for (size_t i = 0; i < (bytes_len / 4); i++) {
        out[i] = ((uint32_t)(*u8_ptr++));
        out[i] += ((uint32_t)(*u8_ptr++)) << 8;
        out[i] += ((uint32_t)(*u8_ptr++)) << 16;
        out[i] += ((uint32_t)(*u8_ptr++)) << 24;
    }
}

// Each chunk or parent node can produce either an 8-word chaining value or, by
// setting the ROOT flag, any number of final output bytes. The Output struct
// captures the state just prior to choosing between those two possibilities.
typedef struct output {
    uint32_t input_chaining_value[8];
    uint32_t block_words[16];
    uint64_t counter;
    uint32_t block_len;
    uint32_t flags;
} output;

inline static void output_chaining_value(const output* self, uint32_t out[8]) {
    uint32_t out16[16];
    compress(self->input_chaining_value, self->block_words, self->counter, self->block_len,
             self->flags, out16);
    memcpy(out, out16, 8 * 4);
}

inline static void output_root_bytes(const output* self, void* out, size_t out_len) {
    uint8_t* out_u8 = (uint8_t*)out;
    uint64_t output_block_counter = 0;
    while (out_len > 0) {
        uint32_t words[16];
        compress(self->input_chaining_value, self->block_words, output_block_counter,
                 self->block_len, self->flags | ROOT, words);
        for (size_t word = 0; word < 16; word++) {
            for (int byte = 0; byte < 4; byte++) {
                if (out_len == 0) {
                    return;
                }
                *out_u8 = (uint8_t)(words[word] >> (8 * byte));
                out_u8++;
                out_len--;
            }
        }
        output_block_counter++;
    }
}

inline static void chunk_state_init(_blake3_chunk_state* self,
                                    const uint32_t key_words[8],
                                    uint64_t chunk_counter,
                                    uint32_t flags) {
    memcpy(self->chaining_value, key_words, sizeof(self->chaining_value));
    self->chunk_counter = chunk_counter;
    memset(self->block, 0, sizeof(self->block));
    self->block_len = 0;
    self->blocks_compressed = 0;
    self->flags = flags;
}

inline static size_t chunk_state_len(const _blake3_chunk_state* self) {
    return BLAKE3_BLOCK_LEN * (size_t)self->blocks_compressed + (size_t)self->block_len;
}

inline static uint32_t chunk_state_start_flag(const _blake3_chunk_state* self) {
    if (self->blocks_compressed == 0) {
        return CHUNK_START;
    } else {
        return 0;
    }
}

inline static void chunk_state_update(_blake3_chunk_state* self,
                                      const void* input,
                                      size_t input_len) {
    const uint8_t* input_u8 = (const uint8_t*)input;
    while (input_len > 0) {
        // If the block buffer is full, compress it and clear it. More input is
        // coming, so this compression is not CHUNK_END.
        if (self->block_len == BLAKE3_BLOCK_LEN) {
            uint32_t block_words[16];
            words_from_little_endian_bytes(self->block, BLAKE3_BLOCK_LEN, block_words);
            uint32_t out16[16];
            compress(self->chaining_value, block_words, self->chunk_counter, BLAKE3_BLOCK_LEN,
                     self->flags | chunk_state_start_flag(self), out16);
            memcpy(self->chaining_value, out16, sizeof(self->chaining_value));
            self->blocks_compressed++;
            memset(self->block, 0, sizeof(self->block));
            self->block_len = 0;
        }

        // Copy input bytes into the block buffer.
        size_t want = BLAKE3_BLOCK_LEN - (size_t)self->block_len;
        size_t take = want;
        if (input_len < want) {
            take = input_len;
        }
        memcpy(&self->block[(size_t)self->block_len], input_u8, take);
        self->block_len += (uint8_t)take;
        input_u8 += take;
        input_len -= take;
    }
}

inline static output chunk_state_output(const _blake3_chunk_state* self) {
    output ret;
    memcpy(ret.input_chaining_value, self->chaining_value, sizeof(ret.input_chaining_value));
    words_from_little_endian_bytes(self->block, sizeof(self->block), ret.block_words);
    ret.counter = self->chunk_counter;
    ret.block_len = (uint32_t)self->block_len;
    ret.flags = self->flags | chunk_state_start_flag(self) | CHUNK_END;
    return ret;
}

inline static output parent_output(const uint32_t left_child_cv[8],
                                   const uint32_t right_child_cv[8],
                                   const uint32_t key_words[8],
                                   uint32_t flags) {
    output ret;
    memcpy(ret.input_chaining_value, key_words, sizeof(ret.input_chaining_value));
    memcpy(&ret.block_words[0], left_child_cv, 8 * 4);
    memcpy(&ret.block_words[8], right_child_cv, 8 * 4);
    ret.counter = 0;                   // Always 0 for parent nodes.
    ret.block_len = BLAKE3_BLOCK_LEN;  // Always BLAKE3_BLOCK_LEN (64) for parent nodes.
    ret.flags = PARENT | flags;
    return ret;
}

inline static void parent_cv(const uint32_t left_child_cv[8],
                             const uint32_t right_child_cv[8],
                             const uint32_t key_words[8],
                             uint32_t flags,
                             uint32_t out[8]) {
    output o = parent_output(left_child_cv, right_child_cv, key_words, flags);
    // We only write to `out` after we've read the inputs. That makes it safe for
    // `out` to alias an input, which we do below.
    output_chaining_value(&o, out);
}

inline static void hasher_init_internal(blake3_hasher* self,
                                        const uint32_t key_words[8],
                                        uint32_t flags) {
    chunk_state_init(&self->chunk_state, key_words, 0, flags);
    memcpy(self->key_words, key_words, sizeof(self->key_words));
    self->cv_stack_len = 0;
    self->flags = flags;
}

// Construct a new `Hasher` for the regular hash function.
static void blake3_hasher_init(blake3_hasher* self) {
    hasher_init_internal(self, IV, 0);
}

inline static void hasher_push_stack(blake3_hasher* self, const uint32_t cv[8]) {
    memcpy(&self->cv_stack[(size_t)self->cv_stack_len * 8], cv, 8 * 4);
    self->cv_stack_len++;
}

// Returns a pointer to the popped CV, which is valid until the next push.
inline static const uint32_t* hasher_pop_stack(blake3_hasher* self) {
    self->cv_stack_len--;
    return &self->cv_stack[(size_t)self->cv_stack_len * 8];
}

// Section 5.1.2 of the BLAKE3 spec explains this algorithm in more detail.
inline static void hasher_add_chunk_cv(blake3_hasher* self,
                                       uint32_t new_cv[8],
                                       uint64_t total_chunks) {
    // This chunk might complete some subtrees. For each completed subtree, its
    // left child will be the current top entry in the CV stack, and its right
    // child will be the current value of `new_cv`. Pop each left child off the
    // stack, merge it with `new_cv`, and overwrite `new_cv` with the result.
    // After all these merges, push the final value of `new_cv` onto the stack.
    // The number of completed subtrees is given by the number of trailing 0-bits
    // in the new total number of chunks.
    while ((total_chunks & 1) == 0) {
        parent_cv(hasher_pop_stack(self), new_cv, self->key_words, self->flags, new_cv);
        total_chunks >>= 1;
    }
    hasher_push_stack(self, new_cv);
}

// Add input to the hash state. This can be called any number of times.
static void blake3_hasher_update(blake3_hasher* self, const void* input, size_t input_len) {
    const uint8_t* input_u8 = (const uint8_t*)input;
    while (input_len > 0) {
        // If the current chunk is complete, finalize it and reset the chunk state.
        // More input is coming, so this chunk is not ROOT.
        if (chunk_state_len(&self->chunk_state) == BLAKE3_CHUNK_LEN) {
            output chunk_output = chunk_state_output(&self->chunk_state);
            uint32_t chunk_cv[8];
            output_chaining_value(&chunk_output, chunk_cv);
            uint64_t total_chunks = self->chunk_state.chunk_counter + 1;
            hasher_add_chunk_cv(self, chunk_cv, total_chunks);
            chunk_state_init(&self->chunk_state, self->key_words, total_chunks, self->flags);
        }

        // Compress input bytes into the current chunk state.
        size_t want = BLAKE3_CHUNK_LEN - chunk_state_len(&self->chunk_state);
        size_t take = want;
        if (input_len < want) {
            take = input_len;
        }
        chunk_state_update(&self->chunk_state, input_u8, take);
        input_u8 += take;
        input_len -= take;
    }
}

// Finalize the hash and write any number of output bytes.
static void blake3_hasher_finalize(const blake3_hasher* self, void* out, size_t out_len) {
    // Starting with the output from the current chunk, compute all the parent
    // chaining values along the right edge of the tree, until we have the root
    // output.
    output current_output = chunk_state_output(&self->chunk_state);
    size_t parent_nodes_remaining = (size_t)self->cv_stack_len;
    while (parent_nodes_remaining > 0) {
        parent_nodes_remaining--;
        uint32_t current_cv[8];
        output_chaining_value(&current_output, current_cv);
        current_output = parent_output(&self->cv_stack[parent_nodes_remaining * 8], current_cv,
                                       self->key_words, self->flags);
    }
    output_root_bytes(&current_output, out, out_len);
}

void* blake3_init() {
    blake3_hasher* context;
    context = malloc(sizeof(blake3_hasher));
    if (!context)
        return NULL;
    blake3_hasher_init(context);
    return context;
}

void blake3_update(blake3_hasher* ctx, const unsigned char* data, size_t len) {
    blake3_hasher_update(ctx, data, len);
}

int blake3_final(blake3_hasher* ctx, unsigned char hash[]) {
    blake3_hasher_finalize(ctx, hash, BLAKE3_OUT_LEN);
    free(ctx);
    return BLAKE3_OUT_LEN;
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// SQLite hash and encode/decode functions.

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT3

#include "crypto/base32.h"
#include "crypto/base64.h"
#include "crypto/base85.h"
#include "crypto/blake3.h"
#include "crypto/hex.h"
#include "crypto/md5.h"
#include "crypto/sha1.h"
#include "crypto/sha2.h"
#include "crypto/url.h"
#include "crypto/xxhash.h"

// encoder/decoder function
typedef uint8_t* (*encdec_fn)(const uint8_t* src, size_t len, size_t* out_len);

// Generic compute hash function. Algorithm is encoded in the user data field.
static void crypto_hash(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);

    if (sqlite3_value_type(argv[0]) == SQLITE_NULL) {
        return;
    }

    void* (*init_func)() = NULL;
    void (*update_func)(void*, void*, size_t) = NULL;
    int (*final_func)(void*, void*) = NULL;
    int algo = (intptr_t)sqlite3_user_data(context);

    switch (algo) {
        case 1: /* Hardened SHA1 */
            init_func = (void*)sha1_init;
            update_func = (void*)sha1_update;
            final_func = (void*)sha1_final;
            algo = 1;
            break;
        case 3: /* Blake3 */
            init_func = (void*)blake3_init;
            update_func = (void*)blake3_update;
            final_func = (void*)blake3_final;
            algo = 3;
            break;
        case 5: /* MD5 */
            init_func = (void*)md5_init;
            update_func = (void*)md5_update;
            final_func = (void*)md5_final;
            algo = 1;
            break;
        case 1032: /* XXH32 */
            init_func = (void*)xxh32_init;
            update_func = (void*)xxh32_update;
            final_func = (void*)xxh32_final;
            algo = 1;
            break;
        case 1064: /* XXH64 */
            init_func = (void*)xxh64_init;
            update_func = (void*)xxh64_update;
            final_func = (void*)xxh64_final;
            algo = 1;
            break;
        case 3064: /* XXH3 64-bit */
            init_func = (void*)xxh3_64_init;
            update_func = (void*)xxh3_64_update;
            final_func = (void*)xxh3_64_final;
            algo = 1;
            break;
        case 3128: /* XXH3 128-bit */
            init_func = (void*)xxh3_128_init;
            update_func = (void*)xxh3_128_update;
            final_func = (void*)xxh3_128_final;
            algo = 1;
            break;
        case 2256: /* SHA2-256 */
            init_func = (void*)sha256_init;
            update_func = (void*)sha256_update;
            final_func = (void*)sha256_final;
            algo = 1;
            break;
        case 2384: /* SHA2-384 */
            init_func = (void*)sha384_init;
            update_func = (void*)sha384_update;
            final_func = (void*)sha384_final;
            algo = 1;
            break;
        case 2512: /* SHA2-512 */
            init_func = (void*)sha512_init;
            update_func = (void*)sha512_update;
            final_func = (void*)sha512_final;
            algo = 1;
            break;
        default:
            sqlite3_result_error(context, "unknown algorithm", -1);
            return;
    }

    void* ctx = NULL;
    if (algo) {
        ctx = init_func();
    }
    if (!ctx) {
        sqlite3_result_error(context, "could not allocate algorithm context", -1);
        return;
    }

    void* data = NULL;
    if (sqlite3_value_type(argv[0]) == SQLITE_BLOB) {
        data = (void*)sqlite3_value_blob(argv[0]);
    } else {
        data = (void*)sqlite3_value_text(argv[0]);
    }

    size_t datalen = sqlite3_value_bytes(argv[0]);
    if (datalen > 0) {
        update_func(ctx, data, datalen);
    }

    unsigned char hash[128] = {0};
    int hashlen = final_func(ctx, hash);
    sqlite3_result_blob(context, hash, hashlen, SQLITE_TRANSIENT);
}

// Encodes binary data into a textual representation using the specified encoder.
static void encode(sqlite3_context* context, int argc, sqlite3_value** argv, encdec_fn encode_fn) {
    assert(argc == 1);
    if (sqlite3_value_type(argv[0]) == SQLITE_NULL) {
        sqlite3_result_null(context);
        return;
    }
    size_t source_len = sqlite3_value_bytes(argv[0]);
    const uint8_t* source = (uint8_t*)sqlite3_value_blob(argv[0]);
    size_t result_len = 0;
    const char* result = (char*)encode_fn(source, source_len, &result_len);
    sqlite3_result_text(context, result, -1, free);
}

// Encodes binary data into a textual representation using the specified algorithm.
// encode('hello', 'base64') = 'aGVsbG8='
static void crypto_encode(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);
    size_t n = sqlite3_value_bytes(argv[1]);
    const char* format = (char*)sqlite3_value_text(argv[1]);
    if (strncmp(format, "base32", n) == 0) {
        encode(context, 1, argv, base32_encode);
        return;
    }
    if (strncmp(format, "base64", n) == 0) {
        encode(context, 1, argv, base64_encode);
        return;
    }
    if (strncmp(format, "base85", n) == 0) {
        encode(context, 1, argv, base85_encode);
        return;
    }
    if (strncmp(format, "hex", n) == 0) {
        encode(context, 1, argv, hex_encode);
        return;
    }
    if (strncmp(format, "url", n) == 0) {
        encode(context, 1, argv, url_encode);
        return;
    }
    sqlite3_result_error(context, "unknown encoding", -1);
}

// Decodes binary data from a textual representation using the specified decoder.
static void decode(sqlite3_context* context, int argc, sqlite3_value** argv, encdec_fn decode_fn) {
    assert(argc == 1);
    if (sqlite3_value_type(argv[0]) == SQLITE_NULL) {
        sqlite3_result_null(context);
        return;
    }

    size_t source_len = sqlite3_value_bytes(argv[0]);
    const uint8_t* source = (uint8_t*)sqlite3_value_text(argv[0]);
    if (source_len == 0) {
        sqlite3_result_zeroblob(context, 0);
        return;
    }

    size_t result_len = 0;
    const uint8_t* result = decode_fn(source, source_len, &result_len);
    if (result == NULL) {
        sqlite3_result_error(context, "invalid input string", -1);
        return;
    }

    sqlite3_result_blob(context, result, result_len, free);
}

// Decodes binary data from a textual representation using the specified algorithm.
// decode('aGVsbG8=', 'base64') = cast('hello' as blob)
static void crypto_decode(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);
    size_t n = sqlite3_value_bytes(argv[1]);
    const char* format = (char*)sqlite3_value_text(argv[1]);
    if (strncmp(format, "base32", n) == 0) {
        decode(context, 1, argv, base32_decode);
        return;
    }
    if (strncmp(format, "base64", n) == 0) {
        decode(context, 1, argv, base64_decode);
        return;
    }
    if (strncmp(format, "base85", n) == 0) {
        decode(context, 1, argv, base85_decode);
        return;
    }
    if (strncmp(format, "hex", n) == 0) {
        decode(context, 1, argv, hex_decode);
        return;
    }
    if (strncmp(format, "url", n) == 0) {
        decode(context, 1, argv, url_decode);
        return;
    }
    sqlite3_result_error(context, "unknown encoding", -1);
}

int crypto_init(sqlite3* db) {
    static const int flags = SQLITE_UTF8 | SQLITE_INNOCUOUS | SQLITE_DETERMINISTIC;
    sqlite3_create_function(db, "crypto_blake3", 1, flags, (void*)3, crypto_hash, 0, 0);
    sqlite3_create_function(db, "blake3", 1, flags, (void*)3, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_md5", 1, flags, (void*)5, crypto_hash, 0, 0);
    sqlite3_create_function(db, "md5", 1, flags, (void*)5, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_sha1", 1, flags, (void*)1, crypto_hash, 0, 0);
    sqlite3_create_function(db, "sha1", 1, flags, (void*)1, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_sha256", 1, flags, (void*)2256, crypto_hash, 0, 0);
    sqlite3_create_function(db, "sha256", 1, flags, (void*)2256, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_sha384", 1, flags, (void*)2384, crypto_hash, 0, 0);
    sqlite3_create_function(db, "sha384", 1, flags, (void*)2384, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_sha512", 1, flags, (void*)2512, crypto_hash, 0, 0);
    sqlite3_create_function(db, "sha512", 1, flags, (void*)2512, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_xxh32", 1, flags, (void*)1032, crypto_hash, 0, 0);
    sqlite3_create_function(db, "xxh32", 1, flags, (void*)1032, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_xxh64", 1, flags, (void*)1064, crypto_hash, 0, 0);
    sqlite3_create_function(db, "xxh64", 1, flags, (void*)1064, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_xxh3_64", 1, flags, (void*)3064, crypto_hash, 0, 0);
    sqlite3_create_function(db, "xxh3_64", 1, flags, (void*)3064, crypto_hash, 0, 0);
    sqlite3_create_function(db, "crypto_xxh3_128", 1, flags, (void*)3128, crypto_hash, 0, 0);
    sqlite3_create_function(db, "xxh3_128", 1, flags, (void*)3128, crypto_hash, 0, 0);

    sqlite3_create_function(db, "crypto_encode", 2, flags, 0, crypto_encode, 0, 0);
    sqlite3_create_function(db, "encode", 2, flags, 0, crypto_encode, 0, 0);
    sqlite3_create_function(db, "crypto_decode", 2, flags, 0, crypto_decode, 0, 0);
    sqlite3_create_function(db, "decode", 2, flags, 0, crypto_decode, 0, 0);
    return SQLITE_OK;
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Hex encoding/decoding

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint8_t* hex_encode(const uint8_t* src, size_t len, size_t* out_len) {
    *out_len = len * 2;
    uint8_t* encoded = malloc(*out_len + 1);
    if (encoded == NULL) {
        *out_len = 0;
        return NULL;
    }
    for (size_t i = 0; i < len; i++) {
        snprintf((char*)encoded + (i * 2), 3, "%02x", src[i]);
    }
    encoded[*out_len] = '\0';
    *out_len = len * 2;
    return encoded;
}

uint8_t* hex_decode(const uint8_t* src, size_t len, size_t* out_len) {
    if (len % 2 != 0) {
        // input length must be even
        return NULL;
    }

    size_t decoded_len = len / 2;
    uint8_t* decoded = malloc(decoded_len);
    if (decoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    for (size_t i = 0; i < decoded_len; i++) {
        uint8_t hi = src[i * 2];
        uint8_t lo = src[i * 2 + 1];

        if (hi >= '0' && hi <= '9') {
            hi -= '0';
        } else if (hi >= 'A' && hi <= 'F') {
            hi -= 'A' - 10;
        } else if (hi >= 'a' && hi <= 'f') {
            hi -= 'a' - 10;
        } else {
            // invalid character
            free(decoded);
            return NULL;
        }

        if (lo >= '0' && lo <= '9') {
            lo -= '0';
        } else if (lo >= 'A' && lo <= 'F') {
            lo -= 'A' - 10;
        } else if (lo >= 'a' && lo <= 'f') {
            lo -= 'a' - 10;
        } else {
            // invalid character
            free(decoded);
            return NULL;
        }

        decoded[i] = (hi << 4) | lo;
    }

    *out_len = decoded_len;
    return decoded;
}
/*********************************************************************
 * Filename:   md5.c
 * Author:     Brad Conte (brad AT bradconte.com)
 * Source:     https://github.com/B-Con/crypto-algorithms
 * License:    Public Domain
 * Details:    Implementation of the MD5 hashing algorithm.
 * Algorithm specification can be found here:
 * http://tools.ietf.org/html/rfc1321
 * This implementation uses little endian byte order.
 *********************************************************************/

/*************************** HEADER FILES ***************************/
#include <memory.h>
#include <stdlib.h>

#include "crypto/md5.h"
/****************************** MACROS ******************************/
#define ROTLEFT(a, b) ((a << b) | (a >> (32 - b)))

#define F(x, y, z) ((x & y) | (~x & z))
#define G(x, y, z) ((x & z) | (y & ~z))
#define H(x, y, z) (x ^ y ^ z)
#define I(x, y, z) (y ^ (x | ~z))

#define FF(a, b, c, d, m, s, t)  \
    {                            \
        a += F(b, c, d) + m + t; \
        a = b + ROTLEFT(a, s);   \
    }
#define GG(a, b, c, d, m, s, t)  \
    {                            \
        a += G(b, c, d) + m + t; \
        a = b + ROTLEFT(a, s);   \
    }
#define HH(a, b, c, d, m, s, t)  \
    {                            \
        a += H(b, c, d) + m + t; \
        a = b + ROTLEFT(a, s);   \
    }
#define II(a, b, c, d, m, s, t)  \
    {                            \
        a += I(b, c, d) + m + t; \
        a = b + ROTLEFT(a, s);   \
    }

/*********************** FUNCTION DEFINITIONS ***********************/
static void md5_transform(MD5_CTX* ctx, const BYTE data[]) {
    WORD a, b, c, d, m[16], i, j;

    // MD5 specifies big endian byte order, but this implementation assumes a little
    // endian byte order CPU. Reverse all the bytes upon input, and re-reverse them
    // on output (in md5_final()).
    for (i = 0, j = 0; i < 16; ++i, j += 4)
        m[i] = (data[j]) + (data[j + 1] << 8) + (data[j + 2] << 16) + ((WORD)data[j + 3] << 24);

    a = ctx->state[0];
    b = ctx->state[1];
    c = ctx->state[2];
    d = ctx->state[3];

    FF(a, b, c, d, m[0], 7, 0xd76aa478);
    FF(d, a, b, c, m[1], 12, 0xe8c7b756);
    FF(c, d, a, b, m[2], 17, 0x242070db);
    FF(b, c, d, a, m[3], 22, 0xc1bdceee);
    FF(a, b, c, d, m[4], 7, 0xf57c0faf);
    FF(d, a, b, c, m[5], 12, 0x4787c62a);
    FF(c, d, a, b, m[6], 17, 0xa8304613);
    FF(b, c, d, a, m[7], 22, 0xfd469501);
    FF(a, b, c, d, m[8], 7, 0x698098d8);
    FF(d, a, b, c, m[9], 12, 0x8b44f7af);
    FF(c, d, a, b, m[10], 17, 0xffff5bb1);
    FF(b, c, d, a, m[11], 22, 0x895cd7be);
    FF(a, b, c, d, m[12], 7, 0x6b901122);
    FF(d, a, b, c, m[13], 12, 0xfd987193);
    FF(c, d, a, b, m[14], 17, 0xa679438e);
    FF(b, c, d, a, m[15], 22, 0x49b40821);

    GG(a, b, c, d, m[1], 5, 0xf61e2562);
    GG(d, a, b, c, m[6], 9, 0xc040b340);
    GG(c, d, a, b, m[11], 14, 0x265e5a51);
    GG(b, c, d, a, m[0], 20, 0xe9b6c7aa);
    GG(a, b, c, d, m[5], 5, 0xd62f105d);
    GG(d, a, b, c, m[10], 9, 0x02441453);
    GG(c, d, a, b, m[15], 14, 0xd8a1e681);
    GG(b, c, d, a, m[4], 20, 0xe7d3fbc8);
    GG(a, b, c, d, m[9], 5, 0x21e1cde6);
    GG(d, a, b, c, m[14], 9, 0xc33707d6);
    GG(c, d, a, b, m[3], 14, 0xf4d50d87);
    GG(b, c, d, a, m[8], 20, 0x455a14ed);
    GG(a, b, c, d, m[13], 5, 0xa9e3e905);
    GG(d, a, b, c, m[2], 9, 0xfcefa3f8);
    GG(c, d, a, b, m[7], 14, 0x676f02d9);
    GG(b, c, d, a, m[12], 20, 0x8d2a4c8a);

    HH(a, b, c, d, m[5], 4, 0xfffa3942);
    HH(d, a, b, c, m[8], 11, 0x8771f681);
    HH(c, d, a, b, m[11], 16, 0x6d9d6122);
    HH(b, c, d, a, m[14], 23, 0xfde5380c);
    HH(a, b, c, d, m[1], 4, 0xa4beea44);
    HH(d, a, b, c, m[4], 11, 0x4bdecfa9);
    HH(c, d, a, b, m[7], 16, 0xf6bb4b60);
    HH(b, c, d, a, m[10], 23, 0xbebfbc70);
    HH(a, b, c, d, m[13], 4, 0x289b7ec6);
    HH(d, a, b, c, m[0], 11, 0xeaa127fa);
    HH(c, d, a, b, m[3], 16, 0xd4ef3085);
    HH(b, c, d, a, m[6], 23, 0x04881d05);
    HH(a, b, c, d, m[9], 4, 0xd9d4d039);
    HH(d, a, b, c, m[12], 11, 0xe6db99e5);
    HH(c, d, a, b, m[15], 16, 0x1fa27cf8);
    HH(b, c, d, a, m[2], 23, 0xc4ac5665);

    II(a, b, c, d, m[0], 6, 0xf4292244);
    II(d, a, b, c, m[7], 10, 0x432aff97);
    II(c, d, a, b, m[14], 15, 0xab9423a7);
    II(b, c, d, a, m[5], 21, 0xfc93a039);
    II(a, b, c, d, m[12], 6, 0x655b59c3);
    II(d, a, b, c, m[3], 10, 0x8f0ccc92);
    II(c, d, a, b, m[10], 15, 0xffeff47d);
    II(b, c, d, a, m[1], 21, 0x85845dd1);
    II(a, b, c, d, m[8], 6, 0x6fa87e4f);
    II(d, a, b, c, m[15], 10, 0xfe2ce6e0);
    II(c, d, a, b, m[6], 15, 0xa3014314);
    II(b, c, d, a, m[13], 21, 0x4e0811a1);
    II(a, b, c, d, m[4], 6, 0xf7537e82);
    II(d, a, b, c, m[11], 10, 0xbd3af235);
    II(c, d, a, b, m[2], 15, 0x2ad7d2bb);
    II(b, c, d, a, m[9], 21, 0xeb86d391);

    ctx->state[0] += a;
    ctx->state[1] += b;
    ctx->state[2] += c;
    ctx->state[3] += d;
}

void* md5_init() {
    MD5_CTX* ctx;
    ctx = malloc(sizeof(MD5_CTX));
    ctx->datalen = 0;
    ctx->bitlen = 0;
    ctx->state[0] = 0x67452301;
    ctx->state[1] = 0xEFCDAB89;
    ctx->state[2] = 0x98BADCFE;
    ctx->state[3] = 0x10325476;
    return ctx;
}

void md5_update(MD5_CTX* ctx, const BYTE data[], size_t len) {
    size_t i;

    for (i = 0; i < len; ++i) {
        ctx->data[ctx->datalen] = data[i];
        ctx->datalen++;
        if (ctx->datalen == 64) {
            md5_transform(ctx, ctx->data);
            ctx->bitlen += 512;
            ctx->datalen = 0;
        }
    }
}

int md5_final(MD5_CTX* ctx, BYTE hash[]) {
    size_t i;

    i = ctx->datalen;

    // Pad whatever data is left in the buffer.
    if (ctx->datalen < 56) {
        ctx->data[i++] = 0x80;
        while (i < 56)
            ctx->data[i++] = 0x00;
    } else if (ctx->datalen >= 56) {
        ctx->data[i++] = 0x80;
        while (i < 64)
            ctx->data[i++] = 0x00;
        md5_transform(ctx, ctx->data);
        memset(ctx->data, 0, 56);
    }

    // Append to the padding the total message's length in bits and transform.
    ctx->bitlen += ctx->datalen * 8;
    ctx->data[56] = ctx->bitlen;
    ctx->data[57] = ctx->bitlen >> 8;
    ctx->data[58] = ctx->bitlen >> 16;
    ctx->data[59] = ctx->bitlen >> 24;
    ctx->data[60] = ctx->bitlen >> 32;
    ctx->data[61] = ctx->bitlen >> 40;
    ctx->data[62] = ctx->bitlen >> 48;
    ctx->data[63] = ctx->bitlen >> 56;
    md5_transform(ctx, ctx->data);

    // Since this implementation uses little endian byte ordering and MD uses big endian,
    // reverse all the bytes when copying the final state to the output hash.
    for (i = 0; i < 4; ++i) {
        hash[i] = (ctx->state[0] >> (i * 8)) & 0x000000ff;
        hash[i + 4] = (ctx->state[1] >> (i * 8)) & 0x000000ff;
        hash[i + 8] = (ctx->state[2] >> (i * 8)) & 0x000000ff;
        hash[i + 12] = (ctx->state[3] >> (i * 8)) & 0x000000ff;
    }
    free(ctx);
    return MD5_BLOCK_SIZE;
}
// Originally from the sha1 SQLite exension, Public Domain
// https://sqlite.org/src/file/ext/misc/sha1.c
// Modified by Anton Zhiyanov, https://github.com/nalgeon/sqlean/, MIT License

#include <assert.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>

#include "crypto/sha1.h"

#define SHA_ROT(x, l, r) ((x) << (l) | (x) >> (r))
#define rol(x, k) SHA_ROT(x, k, 32 - (k))
#define ror(x, k) SHA_ROT(x, 32 - (k), k)

#define blk0le(i) (block[i] = (ror(block[i], 8) & 0xFF00FF00) | (rol(block[i], 8) & 0x00FF00FF))
#define blk0be(i) block[i]
#define blk(i)       \
    (block[i & 15] = \
         rol(block[(i + 13) & 15] ^ block[(i + 8) & 15] ^ block[(i + 2) & 15] ^ block[i & 15], 1))

/*
 * (R0+R1), R2, R3, R4 are the different operations (rounds) used in SHA1
 *
 * Rl0() for little-endian and Rb0() for big-endian.  Endianness is
 * determined at run-time.
 */
#define Rl0(v, w, x, y, z, i)                                      \
    z += ((w & (x ^ y)) ^ y) + blk0le(i) + 0x5A827999 + rol(v, 5); \
    w = ror(w, 2);
#define Rb0(v, w, x, y, z, i)                                      \
    z += ((w & (x ^ y)) ^ y) + blk0be(i) + 0x5A827999 + rol(v, 5); \
    w = ror(w, 2);
#define R1(v, w, x, y, z, i)                                    \
    z += ((w & (x ^ y)) ^ y) + blk(i) + 0x5A827999 + rol(v, 5); \
    w = ror(w, 2);
#define R2(v, w, x, y, z, i)                            \
    z += (w ^ x ^ y) + blk(i) + 0x6ED9EBA1 + rol(v, 5); \
    w = ror(w, 2);
#define R3(v, w, x, y, z, i)                                          \
    z += (((w | x) & y) | (w & x)) + blk(i) + 0x8F1BBCDC + rol(v, 5); \
    w = ror(w, 2);
#define R4(v, w, x, y, z, i)                            \
    z += (w ^ x ^ y) + blk(i) + 0xCA62C1D6 + rol(v, 5); \
    w = ror(w, 2);

/*
 * Hash a single 512-bit block. This is the core of the algorithm.
 */
void SHA1Transform(unsigned int state[5], const unsigned char buffer[64]) {
    unsigned int qq[5]; /* a, b, c, d, e; */
    static int one = 1;
    unsigned int block[16];
    memcpy(block, buffer, 64);
    memcpy(qq, state, 5 * sizeof(unsigned int));

#define a qq[0]
#define b qq[1]
#define c qq[2]
#define d qq[3]
#define e qq[4]

    /* Copy ctx->state[] to working vars */
    /*
  a = state[0];
  b = state[1];
  c = state[2];
  d = state[3];
  e = state[4];
  */

    /* 4 rounds of 20 operations each. Loop unrolled. */
    if (1 == *(unsigned char*)&one) {
        Rl0(a, b, c, d, e, 0);
        Rl0(e, a, b, c, d, 1);
        Rl0(d, e, a, b, c, 2);
        Rl0(c, d, e, a, b, 3);
        Rl0(b, c, d, e, a, 4);
        Rl0(a, b, c, d, e, 5);
        Rl0(e, a, b, c, d, 6);
        Rl0(d, e, a, b, c, 7);
        Rl0(c, d, e, a, b, 8);
        Rl0(b, c, d, e, a, 9);
        Rl0(a, b, c, d, e, 10);
        Rl0(e, a, b, c, d, 11);
        Rl0(d, e, a, b, c, 12);
        Rl0(c, d, e, a, b, 13);
        Rl0(b, c, d, e, a, 14);
        Rl0(a, b, c, d, e, 15);
    } else {
        Rb0(a, b, c, d, e, 0);
        Rb0(e, a, b, c, d, 1);
        Rb0(d, e, a, b, c, 2);
        Rb0(c, d, e, a, b, 3);
        Rb0(b, c, d, e, a, 4);
        Rb0(a, b, c, d, e, 5);
        Rb0(e, a, b, c, d, 6);
        Rb0(d, e, a, b, c, 7);
        Rb0(c, d, e, a, b, 8);
        Rb0(b, c, d, e, a, 9);
        Rb0(a, b, c, d, e, 10);
        Rb0(e, a, b, c, d, 11);
        Rb0(d, e, a, b, c, 12);
        Rb0(c, d, e, a, b, 13);
        Rb0(b, c, d, e, a, 14);
        Rb0(a, b, c, d, e, 15);
    }
    R1(e, a, b, c, d, 16);
    R1(d, e, a, b, c, 17);
    R1(c, d, e, a, b, 18);
    R1(b, c, d, e, a, 19);
    R2(a, b, c, d, e, 20);
    R2(e, a, b, c, d, 21);
    R2(d, e, a, b, c, 22);
    R2(c, d, e, a, b, 23);
    R2(b, c, d, e, a, 24);
    R2(a, b, c, d, e, 25);
    R2(e, a, b, c, d, 26);
    R2(d, e, a, b, c, 27);
    R2(c, d, e, a, b, 28);
    R2(b, c, d, e, a, 29);
    R2(a, b, c, d, e, 30);
    R2(e, a, b, c, d, 31);
    R2(d, e, a, b, c, 32);
    R2(c, d, e, a, b, 33);
    R2(b, c, d, e, a, 34);
    R2(a, b, c, d, e, 35);
    R2(e, a, b, c, d, 36);
    R2(d, e, a, b, c, 37);
    R2(c, d, e, a, b, 38);
    R2(b, c, d, e, a, 39);
    R3(a, b, c, d, e, 40);
    R3(e, a, b, c, d, 41);
    R3(d, e, a, b, c, 42);
    R3(c, d, e, a, b, 43);
    R3(b, c, d, e, a, 44);
    R3(a, b, c, d, e, 45);
    R3(e, a, b, c, d, 46);
    R3(d, e, a, b, c, 47);
    R3(c, d, e, a, b, 48);
    R3(b, c, d, e, a, 49);
    R3(a, b, c, d, e, 50);
    R3(e, a, b, c, d, 51);
    R3(d, e, a, b, c, 52);
    R3(c, d, e, a, b, 53);
    R3(b, c, d, e, a, 54);
    R3(a, b, c, d, e, 55);
    R3(e, a, b, c, d, 56);
    R3(d, e, a, b, c, 57);
    R3(c, d, e, a, b, 58);
    R3(b, c, d, e, a, 59);
    R4(a, b, c, d, e, 60);
    R4(e, a, b, c, d, 61);
    R4(d, e, a, b, c, 62);
    R4(c, d, e, a, b, 63);
    R4(b, c, d, e, a, 64);
    R4(a, b, c, d, e, 65);
    R4(e, a, b, c, d, 66);
    R4(d, e, a, b, c, 67);
    R4(c, d, e, a, b, 68);
    R4(b, c, d, e, a, 69);
    R4(a, b, c, d, e, 70);
    R4(e, a, b, c, d, 71);
    R4(d, e, a, b, c, 72);
    R4(c, d, e, a, b, 73);
    R4(b, c, d, e, a, 74);
    R4(a, b, c, d, e, 75);
    R4(e, a, b, c, d, 76);
    R4(d, e, a, b, c, 77);
    R4(c, d, e, a, b, 78);
    R4(b, c, d, e, a, 79);

    /* Add the working vars back into context.state[] */
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    state[4] += e;

#undef a
#undef b
#undef c
#undef d
#undef e
}

/* Initialize a SHA1 context */
void* sha1_init() {
    /* SHA1 initialization constants */
    SHA1Context* ctx;
    ctx = malloc(sizeof(SHA1Context));
    ctx->state[0] = 0x67452301;
    ctx->state[1] = 0xEFCDAB89;
    ctx->state[2] = 0x98BADCFE;
    ctx->state[3] = 0x10325476;
    ctx->state[4] = 0xC3D2E1F0;
    ctx->count[0] = ctx->count[1] = 0;
    return ctx;
}

/* Add new content to the SHA1 hash */
void sha1_update(SHA1Context* ctx, const unsigned char* data, size_t len) {
    unsigned int i, j;

    j = ctx->count[0];
    if ((ctx->count[0] += len << 3) < j) {
        ctx->count[1] += (len >> 29) + 1;
    }
    j = (j >> 3) & 63;
    if ((j + len) > 63) {
        (void)memcpy(&ctx->buffer[j], data, (i = 64 - j));
        SHA1Transform(ctx->state, ctx->buffer);
        for (; i + 63 < len; i += 64) {
            SHA1Transform(ctx->state, &data[i]);
        }
        j = 0;
    } else {
        i = 0;
    }
    (void)memcpy(&ctx->buffer[j], &data[i], len - i);
}

int sha1_final(SHA1Context* ctx, unsigned char hash[]) {
    unsigned int i;
    unsigned char finalcount[8];

    for (i = 0; i < 8; i++) {
        finalcount[i] = (unsigned char)((ctx->count[(i >= 4 ? 0 : 1)] >> ((3 - (i & 3)) * 8)) &
                                        255); /* Endian independent */
    }
    sha1_update(ctx, (const unsigned char*)"\200", 1);
    while ((ctx->count[0] & 504) != 448) {
        sha1_update(ctx, (const unsigned char*)"\0", 1);
    }
    sha1_update(ctx, finalcount, 8); /* Should cause a SHA1Transform() */
    for (i = 0; i < 20; i++) {
        hash[i] = (unsigned char)((ctx->state[i >> 2] >> ((3 - (i & 3)) * 8)) & 255);
    }
    free(ctx);
    return SHA1_BLOCK_SIZE;
}
/*
 * FIPS 180-2 SHA-224/256/384/512 implementation
 *
 * Copyright (C) 2005-2023 Olivier Gay <olivier.gay@a3.epfl.ch>
 * https://github.com/ogay/sha2, BSD 3-Clause License
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the project nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "crypto/sha2.h"

#define SHFR(x, n) (x >> n)
#define ROTR(x, n) ((x >> n) | (x << ((sizeof(x) << 3) - n)))
#define ROTL(x, n) ((x << n) | (x >> ((sizeof(x) << 3) - n)))
#define CH(x, y, z) ((x & y) ^ (~x & z))
#define MAJ(x, y, z) ((x & y) ^ (x & z) ^ (y & z))

#define SHA256_F1(x) (ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22))
#define SHA256_F2(x) (ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25))
#define SHA256_F3(x) (ROTR(x, 7) ^ ROTR(x, 18) ^ SHFR(x, 3))
#define SHA256_F4(x) (ROTR(x, 17) ^ ROTR(x, 19) ^ SHFR(x, 10))

#define SHA512_F1(x) (ROTR(x, 28) ^ ROTR(x, 34) ^ ROTR(x, 39))
#define SHA512_F2(x) (ROTR(x, 14) ^ ROTR(x, 18) ^ ROTR(x, 41))
#define SHA512_F3(x) (ROTR(x, 1) ^ ROTR(x, 8) ^ SHFR(x, 7))
#define SHA512_F4(x) (ROTR(x, 19) ^ ROTR(x, 61) ^ SHFR(x, 6))

#define UNPACK32(x, str)                   \
    {                                      \
        *((str) + 3) = (uint8)((x));       \
        *((str) + 2) = (uint8)((x) >> 8);  \
        *((str) + 1) = (uint8)((x) >> 16); \
        *((str) + 0) = (uint8)((x) >> 24); \
    }

#define PACK32(str, x)                                                          \
    {                                                                           \
        *(x) = ((uint32) * ((str) + 3)) | ((uint32) * ((str) + 2) << 8) |       \
               ((uint32) * ((str) + 1) << 16) | ((uint32) * ((str) + 0) << 24); \
    }

#define UNPACK64(x, str)                   \
    {                                      \
        *((str) + 7) = (uint8)((x));       \
        *((str) + 6) = (uint8)((x) >> 8);  \
        *((str) + 5) = (uint8)((x) >> 16); \
        *((str) + 4) = (uint8)((x) >> 24); \
        *((str) + 3) = (uint8)((x) >> 32); \
        *((str) + 2) = (uint8)((x) >> 40); \
        *((str) + 1) = (uint8)((x) >> 48); \
        *((str) + 0) = (uint8)((x) >> 56); \
    }

#define PACK64(str, x)                                                           \
    {                                                                            \
        *(x) = ((uint64) * ((str) + 7)) | ((uint64) * ((str) + 6) << 8) |        \
               ((uint64) * ((str) + 5) << 16) | ((uint64) * ((str) + 4) << 24) | \
               ((uint64) * ((str) + 3) << 32) | ((uint64) * ((str) + 2) << 40) | \
               ((uint64) * ((str) + 1) << 48) | ((uint64) * ((str) + 0) << 56);  \
    }

/* Macros used for loops unrolling */

#define SHA256_SCR(i)                                                             \
    {                                                                             \
        w[i] = SHA256_F4(w[i - 2]) + w[i - 7] + SHA256_F3(w[i - 15]) + w[i - 16]; \
    }

#define SHA512_SCR(i)                                                             \
    {                                                                             \
        w[i] = SHA512_F4(w[i - 2]) + w[i - 7] + SHA512_F3(w[i - 15]) + w[i - 16]; \
    }

#define SHA256_EXP(a, b, c, d, e, f, g, h, j)                                         \
    {                                                                                 \
        t1 = wv[h] + SHA256_F2(wv[e]) + CH(wv[e], wv[f], wv[g]) + sha256_k[j] + w[j]; \
        t2 = SHA256_F1(wv[a]) + MAJ(wv[a], wv[b], wv[c]);                             \
        wv[d] += t1;                                                                  \
        wv[h] = t1 + t2;                                                              \
    }

#define SHA512_EXP(a, b, c, d, e, f, g, h, j)                                         \
    {                                                                                 \
        t1 = wv[h] + SHA512_F2(wv[e]) + CH(wv[e], wv[f], wv[g]) + sha512_k[j] + w[j]; \
        t2 = SHA512_F1(wv[a]) + MAJ(wv[a], wv[b], wv[c]);                             \
        wv[d] += t1;                                                                  \
        wv[h] = t1 + t2;                                                              \
    }

static const uint32 sha224_h0[8] = {0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939,
                                    0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4};

static const uint32 sha256_h0[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                                    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19};

static const uint64 sha384_h0[8] = {
    0xcbbb9d5dc1059ed8ULL, 0x629a292a367cd507ULL, 0x9159015a3070dd17ULL, 0x152fecd8f70e5939ULL,
    0x67332667ffc00b31ULL, 0x8eb44a8768581511ULL, 0xdb0c2e0d64f98fa7ULL, 0x47b5481dbefa4fa4ULL};

static const uint64 sha512_h0[8] = {
    0x6a09e667f3bcc908ULL, 0xbb67ae8584caa73bULL, 0x3c6ef372fe94f82bULL, 0xa54ff53a5f1d36f1ULL,
    0x510e527fade682d1ULL, 0x9b05688c2b3e6c1fULL, 0x1f83d9abfb41bd6bULL, 0x5be0cd19137e2179ULL};

static const uint32 sha256_k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};

static const uint64 sha512_k[80] = {
    0x428a2f98d728ae22ULL, 0x7137449123ef65cdULL, 0xb5c0fbcfec4d3b2fULL, 0xe9b5dba58189dbbcULL,
    0x3956c25bf348b538ULL, 0x59f111f1b605d019ULL, 0x923f82a4af194f9bULL, 0xab1c5ed5da6d8118ULL,
    0xd807aa98a3030242ULL, 0x12835b0145706fbeULL, 0x243185be4ee4b28cULL, 0x550c7dc3d5ffb4e2ULL,
    0x72be5d74f27b896fULL, 0x80deb1fe3b1696b1ULL, 0x9bdc06a725c71235ULL, 0xc19bf174cf692694ULL,
    0xe49b69c19ef14ad2ULL, 0xefbe4786384f25e3ULL, 0x0fc19dc68b8cd5b5ULL, 0x240ca1cc77ac9c65ULL,
    0x2de92c6f592b0275ULL, 0x4a7484aa6ea6e483ULL, 0x5cb0a9dcbd41fbd4ULL, 0x76f988da831153b5ULL,
    0x983e5152ee66dfabULL, 0xa831c66d2db43210ULL, 0xb00327c898fb213fULL, 0xbf597fc7beef0ee4ULL,
    0xc6e00bf33da88fc2ULL, 0xd5a79147930aa725ULL, 0x06ca6351e003826fULL, 0x142929670a0e6e70ULL,
    0x27b70a8546d22ffcULL, 0x2e1b21385c26c926ULL, 0x4d2c6dfc5ac42aedULL, 0x53380d139d95b3dfULL,
    0x650a73548baf63deULL, 0x766a0abb3c77b2a8ULL, 0x81c2c92e47edaee6ULL, 0x92722c851482353bULL,
    0xa2bfe8a14cf10364ULL, 0xa81a664bbc423001ULL, 0xc24b8b70d0f89791ULL, 0xc76c51a30654be30ULL,
    0xd192e819d6ef5218ULL, 0xd69906245565a910ULL, 0xf40e35855771202aULL, 0x106aa07032bbd1b8ULL,
    0x19a4c116b8d2d0c8ULL, 0x1e376c085141ab53ULL, 0x2748774cdf8eeb99ULL, 0x34b0bcb5e19b48a8ULL,
    0x391c0cb3c5c95a63ULL, 0x4ed8aa4ae3418acbULL, 0x5b9cca4f7763e373ULL, 0x682e6ff3d6b2b8a3ULL,
    0x748f82ee5defb2fcULL, 0x78a5636f43172f60ULL, 0x84c87814a1f0ab72ULL, 0x8cc702081a6439ecULL,
    0x90befffa23631e28ULL, 0xa4506cebde82bde9ULL, 0xbef9a3f7b2c67915ULL, 0xc67178f2e372532bULL,
    0xca273eceea26619cULL, 0xd186b8c721c0c207ULL, 0xeada7dd6cde0eb1eULL, 0xf57d4f7fee6ed178ULL,
    0x06f067aa72176fbaULL, 0x0a637dc5a2c898a6ULL, 0x113f9804bef90daeULL, 0x1b710b35131c471bULL,
    0x28db77f523047d84ULL, 0x32caab7b40c72493ULL, 0x3c9ebe0a15c9bebcULL, 0x431d67c49c100d4cULL,
    0x4cc5d4becb3e42b6ULL, 0x597f299cfc657e2aULL, 0x5fcb6fab3ad6faecULL, 0x6c44198c4a475817ULL};

/* SHA-2 internal function */

static void sha256_transf(sha256_ctx* ctx, const uint8* message, uint64 block_nb) {
    uint32 w[64];
    uint32 wv[8];
    uint32 t1, t2;
    const uint8* sub_block;
    uint64 i;

    for (i = 0; i < block_nb; i++) {
        sub_block = message + (i << 6);

        PACK32(&sub_block[0], &w[0]);
        PACK32(&sub_block[4], &w[1]);
        PACK32(&sub_block[8], &w[2]);
        PACK32(&sub_block[12], &w[3]);
        PACK32(&sub_block[16], &w[4]);
        PACK32(&sub_block[20], &w[5]);
        PACK32(&sub_block[24], &w[6]);
        PACK32(&sub_block[28], &w[7]);
        PACK32(&sub_block[32], &w[8]);
        PACK32(&sub_block[36], &w[9]);
        PACK32(&sub_block[40], &w[10]);
        PACK32(&sub_block[44], &w[11]);
        PACK32(&sub_block[48], &w[12]);
        PACK32(&sub_block[52], &w[13]);
        PACK32(&sub_block[56], &w[14]);
        PACK32(&sub_block[60], &w[15]);

        SHA256_SCR(16);
        SHA256_SCR(17);
        SHA256_SCR(18);
        SHA256_SCR(19);
        SHA256_SCR(20);
        SHA256_SCR(21);
        SHA256_SCR(22);
        SHA256_SCR(23);
        SHA256_SCR(24);
        SHA256_SCR(25);
        SHA256_SCR(26);
        SHA256_SCR(27);
        SHA256_SCR(28);
        SHA256_SCR(29);
        SHA256_SCR(30);
        SHA256_SCR(31);
        SHA256_SCR(32);
        SHA256_SCR(33);
        SHA256_SCR(34);
        SHA256_SCR(35);
        SHA256_SCR(36);
        SHA256_SCR(37);
        SHA256_SCR(38);
        SHA256_SCR(39);
        SHA256_SCR(40);
        SHA256_SCR(41);
        SHA256_SCR(42);
        SHA256_SCR(43);
        SHA256_SCR(44);
        SHA256_SCR(45);
        SHA256_SCR(46);
        SHA256_SCR(47);
        SHA256_SCR(48);
        SHA256_SCR(49);
        SHA256_SCR(50);
        SHA256_SCR(51);
        SHA256_SCR(52);
        SHA256_SCR(53);
        SHA256_SCR(54);
        SHA256_SCR(55);
        SHA256_SCR(56);
        SHA256_SCR(57);
        SHA256_SCR(58);
        SHA256_SCR(59);
        SHA256_SCR(60);
        SHA256_SCR(61);
        SHA256_SCR(62);
        SHA256_SCR(63);

        wv[0] = ctx->h[0];
        wv[1] = ctx->h[1];
        wv[2] = ctx->h[2];
        wv[3] = ctx->h[3];
        wv[4] = ctx->h[4];
        wv[5] = ctx->h[5];
        wv[6] = ctx->h[6];
        wv[7] = ctx->h[7];

        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 0);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 1);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 2);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 3);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 4);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 5);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 6);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 7);
        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 8);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 9);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 10);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 11);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 12);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 13);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 14);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 15);
        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 16);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 17);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 18);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 19);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 20);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 21);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 22);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 23);
        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 24);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 25);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 26);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 27);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 28);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 29);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 30);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 31);
        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 32);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 33);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 34);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 35);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 36);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 37);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 38);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 39);
        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 40);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 41);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 42);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 43);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 44);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 45);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 46);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 47);
        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 48);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 49);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 50);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 51);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 52);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 53);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 54);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 55);
        SHA256_EXP(0, 1, 2, 3, 4, 5, 6, 7, 56);
        SHA256_EXP(7, 0, 1, 2, 3, 4, 5, 6, 57);
        SHA256_EXP(6, 7, 0, 1, 2, 3, 4, 5, 58);
        SHA256_EXP(5, 6, 7, 0, 1, 2, 3, 4, 59);
        SHA256_EXP(4, 5, 6, 7, 0, 1, 2, 3, 60);
        SHA256_EXP(3, 4, 5, 6, 7, 0, 1, 2, 61);
        SHA256_EXP(2, 3, 4, 5, 6, 7, 0, 1, 62);
        SHA256_EXP(1, 2, 3, 4, 5, 6, 7, 0, 63);

        ctx->h[0] += wv[0];
        ctx->h[1] += wv[1];
        ctx->h[2] += wv[2];
        ctx->h[3] += wv[3];
        ctx->h[4] += wv[4];
        ctx->h[5] += wv[5];
        ctx->h[6] += wv[6];
        ctx->h[7] += wv[7];
    }
}

static void sha512_transf(sha512_ctx* ctx, const uint8* message, uint64 block_nb) {
    uint64 w[80];
    uint64 wv[8];
    uint64 t1, t2;
    const uint8* sub_block;
    uint64 i;
    int j;

    for (i = 0; i < block_nb; i++) {
        sub_block = message + (i << 7);

        PACK64(&sub_block[0], &w[0]);
        PACK64(&sub_block[8], &w[1]);
        PACK64(&sub_block[16], &w[2]);
        PACK64(&sub_block[24], &w[3]);
        PACK64(&sub_block[32], &w[4]);
        PACK64(&sub_block[40], &w[5]);
        PACK64(&sub_block[48], &w[6]);
        PACK64(&sub_block[56], &w[7]);
        PACK64(&sub_block[64], &w[8]);
        PACK64(&sub_block[72], &w[9]);
        PACK64(&sub_block[80], &w[10]);
        PACK64(&sub_block[88], &w[11]);
        PACK64(&sub_block[96], &w[12]);
        PACK64(&sub_block[104], &w[13]);
        PACK64(&sub_block[112], &w[14]);
        PACK64(&sub_block[120], &w[15]);

        SHA512_SCR(16);
        SHA512_SCR(17);
        SHA512_SCR(18);
        SHA512_SCR(19);
        SHA512_SCR(20);
        SHA512_SCR(21);
        SHA512_SCR(22);
        SHA512_SCR(23);
        SHA512_SCR(24);
        SHA512_SCR(25);
        SHA512_SCR(26);
        SHA512_SCR(27);
        SHA512_SCR(28);
        SHA512_SCR(29);
        SHA512_SCR(30);
        SHA512_SCR(31);
        SHA512_SCR(32);
        SHA512_SCR(33);
        SHA512_SCR(34);
        SHA512_SCR(35);
        SHA512_SCR(36);
        SHA512_SCR(37);
        SHA512_SCR(38);
        SHA512_SCR(39);
        SHA512_SCR(40);
        SHA512_SCR(41);
        SHA512_SCR(42);
        SHA512_SCR(43);
        SHA512_SCR(44);
        SHA512_SCR(45);
        SHA512_SCR(46);
        SHA512_SCR(47);
        SHA512_SCR(48);
        SHA512_SCR(49);
        SHA512_SCR(50);
        SHA512_SCR(51);
        SHA512_SCR(52);
        SHA512_SCR(53);
        SHA512_SCR(54);
        SHA512_SCR(55);
        SHA512_SCR(56);
        SHA512_SCR(57);
        SHA512_SCR(58);
        SHA512_SCR(59);
        SHA512_SCR(60);
        SHA512_SCR(61);
        SHA512_SCR(62);
        SHA512_SCR(63);
        SHA512_SCR(64);
        SHA512_SCR(65);
        SHA512_SCR(66);
        SHA512_SCR(67);
        SHA512_SCR(68);
        SHA512_SCR(69);
        SHA512_SCR(70);
        SHA512_SCR(71);
        SHA512_SCR(72);
        SHA512_SCR(73);
        SHA512_SCR(74);
        SHA512_SCR(75);
        SHA512_SCR(76);
        SHA512_SCR(77);
        SHA512_SCR(78);
        SHA512_SCR(79);

        wv[0] = ctx->h[0];
        wv[1] = ctx->h[1];
        wv[2] = ctx->h[2];
        wv[3] = ctx->h[3];
        wv[4] = ctx->h[4];
        wv[5] = ctx->h[5];
        wv[6] = ctx->h[6];
        wv[7] = ctx->h[7];

        j = 0;

        do {
            SHA512_EXP(0, 1, 2, 3, 4, 5, 6, 7, j);
            j++;
            SHA512_EXP(7, 0, 1, 2, 3, 4, 5, 6, j);
            j++;
            SHA512_EXP(6, 7, 0, 1, 2, 3, 4, 5, j);
            j++;
            SHA512_EXP(5, 6, 7, 0, 1, 2, 3, 4, j);
            j++;
            SHA512_EXP(4, 5, 6, 7, 0, 1, 2, 3, j);
            j++;
            SHA512_EXP(3, 4, 5, 6, 7, 0, 1, 2, j);
            j++;
            SHA512_EXP(2, 3, 4, 5, 6, 7, 0, 1, j);
            j++;
            SHA512_EXP(1, 2, 3, 4, 5, 6, 7, 0, j);
            j++;
        } while (j < 80);

        ctx->h[0] += wv[0];
        ctx->h[1] += wv[1];
        ctx->h[2] += wv[2];
        ctx->h[3] += wv[3];
        ctx->h[4] += wv[4];
        ctx->h[5] += wv[5];
        ctx->h[6] += wv[6];
        ctx->h[7] += wv[7];
    }
}

/* SHA-224 functions */

sha224_ctx* sha224_init(void) {
    sha224_ctx* ctx;
    ctx = malloc(sizeof(sha224_ctx));
    if (!ctx) {
        return 0;
    }

    ctx->h[0] = sha224_h0[0];
    ctx->h[1] = sha224_h0[1];
    ctx->h[2] = sha224_h0[2];
    ctx->h[3] = sha224_h0[3];
    ctx->h[4] = sha224_h0[4];
    ctx->h[5] = sha224_h0[5];
    ctx->h[6] = sha224_h0[6];
    ctx->h[7] = sha224_h0[7];

    ctx->len = 0;
    ctx->tot_len = 0;
    return ctx;
}

void sha224_update(sha224_ctx* ctx, const uint8* message, uint64 len) {
    uint64 block_nb;
    uint64 new_len, rem_len, tmp_len;
    const uint8* shifted_message;

    tmp_len = SHA224_BLOCK_SIZE - ctx->len;
    rem_len = len < tmp_len ? len : tmp_len;

    memcpy(&ctx->block[ctx->len], message, rem_len);

    if (ctx->len + len < SHA224_BLOCK_SIZE) {
        ctx->len += len;
        return;
    }

    new_len = len - rem_len;
    block_nb = new_len / SHA224_BLOCK_SIZE;

    shifted_message = message + rem_len;

    sha256_transf(ctx, ctx->block, 1);
    sha256_transf(ctx, shifted_message, block_nb);

    rem_len = new_len % SHA224_BLOCK_SIZE;

    memcpy(ctx->block, &shifted_message[block_nb << 6], rem_len);

    ctx->len = rem_len;
    ctx->tot_len += (block_nb + 1) << 6;
}

int sha224_final(sha224_ctx* ctx, uint8* digest) {
    uint64 block_nb;
    uint64 pm_len;
    uint64 len_b;
    uint64 tot_len;

    block_nb = (1 + ((SHA224_BLOCK_SIZE - 9) < (ctx->len % SHA224_BLOCK_SIZE)));

    tot_len = ctx->tot_len + ctx->len;
    ctx->tot_len = tot_len;

    len_b = tot_len << 3;
    pm_len = block_nb << 6;

    memset(ctx->block + ctx->len, 0, pm_len - ctx->len);
    ctx->block[ctx->len] = 0x80;
    UNPACK64(len_b, ctx->block + pm_len - 8);

    sha256_transf(ctx, ctx->block, block_nb);

    UNPACK32(ctx->h[0], &digest[0]);
    UNPACK32(ctx->h[1], &digest[4]);
    UNPACK32(ctx->h[2], &digest[8]);
    UNPACK32(ctx->h[3], &digest[12]);
    UNPACK32(ctx->h[4], &digest[16]);
    UNPACK32(ctx->h[5], &digest[20]);
    UNPACK32(ctx->h[6], &digest[24]);

    free(ctx);
    return SHA224_DIGEST_SIZE;
}

/* SHA-256 functions */

sha256_ctx* sha256_init(void) {
    sha256_ctx* ctx;
    ctx = malloc(sizeof(sha256_ctx));
    if (!ctx) {
        return 0;
    }

    ctx->h[0] = sha256_h0[0];
    ctx->h[1] = sha256_h0[1];
    ctx->h[2] = sha256_h0[2];
    ctx->h[3] = sha256_h0[3];
    ctx->h[4] = sha256_h0[4];
    ctx->h[5] = sha256_h0[5];
    ctx->h[6] = sha256_h0[6];
    ctx->h[7] = sha256_h0[7];

    ctx->len = 0;
    ctx->tot_len = 0;
    return ctx;
}

void sha256_update(sha256_ctx* ctx, const uint8* message, uint64 len) {
    uint64 block_nb;
    uint64 new_len, rem_len, tmp_len;
    const uint8* shifted_message;

    tmp_len = SHA256_BLOCK_SIZE - ctx->len;
    rem_len = len < tmp_len ? len : tmp_len;

    memcpy(&ctx->block[ctx->len], message, rem_len);

    if (ctx->len + len < SHA256_BLOCK_SIZE) {
        ctx->len += len;
        return;
    }

    new_len = len - rem_len;
    block_nb = new_len / SHA256_BLOCK_SIZE;

    shifted_message = message + rem_len;

    sha256_transf(ctx, ctx->block, 1);
    sha256_transf(ctx, shifted_message, block_nb);

    rem_len = new_len % SHA256_BLOCK_SIZE;

    memcpy(ctx->block, &shifted_message[block_nb << 6], rem_len);

    ctx->len = rem_len;
    ctx->tot_len += (block_nb + 1) << 6;
}

int sha256_final(sha256_ctx* ctx, uint8* digest) {
    uint64 block_nb;
    uint64 pm_len;
    uint64 len_b;
    uint64 tot_len;

    block_nb = (1 + ((SHA256_BLOCK_SIZE - 9) < (ctx->len % SHA256_BLOCK_SIZE)));

    tot_len = ctx->tot_len + ctx->len;
    ctx->tot_len = tot_len;

    len_b = tot_len << 3;
    pm_len = block_nb << 6;

    memset(ctx->block + ctx->len, 0, pm_len - ctx->len);
    ctx->block[ctx->len] = 0x80;
    UNPACK64(len_b, ctx->block + pm_len - 8);

    sha256_transf(ctx, ctx->block, block_nb);

    UNPACK32(ctx->h[0], &digest[0]);
    UNPACK32(ctx->h[1], &digest[4]);
    UNPACK32(ctx->h[2], &digest[8]);
    UNPACK32(ctx->h[3], &digest[12]);
    UNPACK32(ctx->h[4], &digest[16]);
    UNPACK32(ctx->h[5], &digest[20]);
    UNPACK32(ctx->h[6], &digest[24]);
    UNPACK32(ctx->h[7], &digest[28]);

    free(ctx);
    return SHA256_DIGEST_SIZE;
}

/* SHA-384 functions */

sha384_ctx* sha384_init(void) {
    sha384_ctx* ctx;
    ctx = malloc(sizeof(sha384_ctx));
    if (!ctx) {
        return 0;
    }

    ctx->h[0] = sha384_h0[0];
    ctx->h[1] = sha384_h0[1];
    ctx->h[2] = sha384_h0[2];
    ctx->h[3] = sha384_h0[3];
    ctx->h[4] = sha384_h0[4];
    ctx->h[5] = sha384_h0[5];
    ctx->h[6] = sha384_h0[6];
    ctx->h[7] = sha384_h0[7];

    ctx->len = 0;
    ctx->tot_len = 0;
    return ctx;
}

void sha384_update(sha384_ctx* ctx, const uint8* message, uint64 len) {
    uint64 block_nb;
    uint64 new_len, rem_len, tmp_len;
    const uint8* shifted_message;

    tmp_len = SHA384_BLOCK_SIZE - ctx->len;
    rem_len = len < tmp_len ? len : tmp_len;

    memcpy(&ctx->block[ctx->len], message, rem_len);

    if (ctx->len + len < SHA384_BLOCK_SIZE) {
        ctx->len += len;
        return;
    }

    new_len = len - rem_len;
    block_nb = new_len / SHA384_BLOCK_SIZE;

    shifted_message = message + rem_len;

    sha512_transf(ctx, ctx->block, 1);
    sha512_transf(ctx, shifted_message, block_nb);

    rem_len = new_len % SHA384_BLOCK_SIZE;

    memcpy(ctx->block, &shifted_message[block_nb << 7], rem_len);

    ctx->len = rem_len;
    ctx->tot_len += (block_nb + 1) << 7;
}

int sha384_final(sha384_ctx* ctx, uint8* digest) {
    uint64 block_nb;
    uint64 pm_len;
    uint64 len_b;
    uint64 tot_len;

    block_nb = (1 + ((SHA384_BLOCK_SIZE - 17) < (ctx->len % SHA384_BLOCK_SIZE)));

    tot_len = ctx->tot_len + ctx->len;
    ctx->tot_len = tot_len;

    len_b = tot_len << 3;
    pm_len = block_nb << 7;

    memset(ctx->block + ctx->len, 0, pm_len - ctx->len);
    ctx->block[ctx->len] = 0x80;
    UNPACK64(len_b, ctx->block + pm_len - 8);

    sha512_transf(ctx, ctx->block, block_nb);

    UNPACK64(ctx->h[0], &digest[0]);
    UNPACK64(ctx->h[1], &digest[8]);
    UNPACK64(ctx->h[2], &digest[16]);
    UNPACK64(ctx->h[3], &digest[24]);
    UNPACK64(ctx->h[4], &digest[32]);
    UNPACK64(ctx->h[5], &digest[40]);

    free(ctx);
    return SHA384_DIGEST_SIZE;
}

/* SHA-512 functions */

sha512_ctx* sha512_init(void) {
    sha512_ctx* ctx;
    ctx = malloc(sizeof(sha512_ctx));
    if (!ctx) {
        return 0;
    }

    ctx->h[0] = sha512_h0[0];
    ctx->h[1] = sha512_h0[1];
    ctx->h[2] = sha512_h0[2];
    ctx->h[3] = sha512_h0[3];
    ctx->h[4] = sha512_h0[4];
    ctx->h[5] = sha512_h0[5];
    ctx->h[6] = sha512_h0[6];
    ctx->h[7] = sha512_h0[7];

    ctx->len = 0;
    ctx->tot_len = 0;
    return ctx;
}

void sha512_update(sha512_ctx* ctx, const uint8* message, uint64 len) {
    uint64 block_nb;
    uint64 new_len, rem_len, tmp_len;
    const uint8* shifted_message;

    tmp_len = SHA512_BLOCK_SIZE - ctx->len;
    rem_len = len < tmp_len ? len : tmp_len;

    memcpy(&ctx->block[ctx->len], message, rem_len);

    if (ctx->len + len < SHA512_BLOCK_SIZE) {
        ctx->len += len;
        return;
    }

    new_len = len - rem_len;
    block_nb = new_len / SHA512_BLOCK_SIZE;

    shifted_message = message + rem_len;

    sha512_transf(ctx, ctx->block, 1);
    sha512_transf(ctx, shifted_message, block_nb);

    rem_len = new_len % SHA512_BLOCK_SIZE;

    memcpy(ctx->block, &shifted_message[block_nb << 7], rem_len);

    ctx->len = rem_len;
    ctx->tot_len += (block_nb + 1) << 7;
}

int sha512_final(sha512_ctx* ctx, uint8* digest) {
    uint64 block_nb;
    uint64 pm_len;
    uint64 len_b;
    uint64 tot_len;

    block_nb = 1 + ((SHA512_BLOCK_SIZE - 17) < (ctx->len % SHA512_BLOCK_SIZE));

    tot_len = ctx->tot_len + ctx->len;
    ctx->tot_len = tot_len;

    len_b = tot_len << 3;
    pm_len = block_nb << 7;

    memset(ctx->block + ctx->len, 0, pm_len - ctx->len);
    ctx->block[ctx->len] = 0x80;
    UNPACK64(len_b, ctx->block + pm_len - 8);

    sha512_transf(ctx, ctx->block, block_nb);

    UNPACK64(ctx->h[0], &digest[0]);
    UNPACK64(ctx->h[1], &digest[8]);
    UNPACK64(ctx->h[2], &digest[16]);
    UNPACK64(ctx->h[3], &digest[24]);
    UNPACK64(ctx->h[4], &digest[32]);
    UNPACK64(ctx->h[5], &digest[40]);
    UNPACK64(ctx->h[6], &digest[48]);
    UNPACK64(ctx->h[7], &digest[56]);

    free(ctx);
    return SHA512_DIGEST_SIZE;
}
// Originally by Fränz Friederes, MIT License
// https://github.com/cryptii/cryptii/blob/main/src/Encoder/URL.js

// Modified by Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean/

// URL-escape encoding/decoding

#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

const char* url_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~";

uint8_t hex_to_ascii(char c) {
    if (isdigit(c)) {
        return c - '0';
    } else {
        return tolower(c) - 'a' + 10;
    }
}

uint8_t* url_encode(const uint8_t* src, size_t len, size_t* out_len) {
    size_t encoded_len = 0;
    for (size_t i = 0; i < len; i++) {
        if (strchr(url_chars, src[i]) == NULL) {
            encoded_len += 3;
        } else {
            encoded_len += 1;
        }
    }

    uint8_t* encoded = malloc(encoded_len + 1);
    if (encoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    size_t pos = 0;
    for (size_t i = 0; i < len; i++) {
        if (strchr(url_chars, src[i]) == NULL) {
            encoded[pos++] = '%';
            encoded[pos++] = "0123456789ABCDEF"[src[i] >> 4];
            encoded[pos++] = "0123456789ABCDEF"[src[i] & 0x0F];
        } else {
            encoded[pos++] = src[i];
        }
    }
    encoded[pos] = '\0';

    *out_len = pos;
    return encoded;
}

uint8_t* url_decode(const uint8_t* src, size_t len, size_t* out_len) {
    uint8_t* decoded = malloc(len);
    if (decoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    size_t pos = 0;
    for (size_t i = 0; i < len; i++) {
        if (src[i] == '%') {
            if (i + 2 >= len || !isxdigit(src[i + 1]) || !isxdigit(src[i + 2])) {
                free(decoded);
                return NULL;
            }
            decoded[pos++] = (hex_to_ascii(src[i + 1]) << 4) | hex_to_ascii(src[i + 2]);
            i += 2;
        } else if (src[i] == '+') {
            decoded[pos++] = ' ';
        } else {
            decoded[pos++] = src[i];
        }
    }

    *out_len = pos;
    return decoded;
}
// Copyright (c) 2025 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

#include <stddef.h>
#include <stdint.h>
#include <string.h>

#define XXH_STATIC_LINKING_ONLY
#define XXH_IMPLEMENTATION
#include "crypto/xxhash.h"
#include "crypto/xxhash.impl.h"

#define XXH32_DIGEST_LENGTH 4
#define XXH64_DIGEST_LENGTH 8
#define XXH128_DIGEST_LENGTH 16

// XXH32.

void* xxh32_init() {
    XXH32_state_t* ctx = XXH32_createState();
    if (!ctx) {
        return NULL;
    }
    XXH32_reset(ctx, 0);
    return ctx;
}

void xxh32_update(XXH32_state_t* ctx, const void* data, size_t len) {
    XXH32_update(ctx, data, len);
}

int xxh32_final(XXH32_state_t* ctx, uint8_t* hash) {
    XXH32_hash_t digest = XXH32_digest(ctx);
    XXH32_canonical_t cano;
    XXH32_canonicalFromHash(&cano, digest);
    memcpy(hash, cano.digest, XXH32_DIGEST_LENGTH);
    XXH32_freeState(ctx);
    return XXH32_DIGEST_LENGTH;
}

// XXH64.

void* xxh64_init() {
    XXH64_state_t* ctx = XXH64_createState();
    if (!ctx) {
        return NULL;
    }
    XXH64_reset(ctx, 0);
    return ctx;
}

void xxh64_update(XXH64_state_t* ctx, const void* data, size_t len) {
    XXH64_update(ctx, data, len);
}

int xxh64_final(XXH64_state_t* ctx, uint8_t* hash) {
    XXH64_hash_t digest = XXH64_digest(ctx);
    XXH64_canonical_t cano;
    XXH64_canonicalFromHash(&cano, digest);
    memcpy(hash, cano.digest, XXH64_DIGEST_LENGTH);
    XXH64_freeState(ctx);
    return XXH64_DIGEST_LENGTH;
}

// XXH3 64-bit.

void* xxh3_64_init() {
    XXH3_state_t* ctx = XXH3_createState();
    if (!ctx) {
        return NULL;
    }
    XXH3_64bits_reset(ctx);
    return ctx;
}

void xxh3_64_update(XXH3_state_t* ctx, const void* data, size_t len) {
    XXH3_64bits_update(ctx, data, len);
}

int xxh3_64_final(XXH3_state_t* ctx, uint8_t* hash) {
    uint64_t digest = XXH3_64bits_digest(ctx);
    XXH64_canonical_t cano;
    XXH64_canonicalFromHash(&cano, digest);
    memcpy(hash, cano.digest, XXH64_DIGEST_LENGTH);
    XXH3_freeState(ctx);
    return XXH64_DIGEST_LENGTH;
}

// XXH3 128-bit.

void* xxh3_128_init() {
    XXH3_state_t* ctx = XXH3_createState();
    if (!ctx) {
        return NULL;
    }
    XXH3_128bits_reset(ctx);
    return ctx;
}

void xxh3_128_update(XXH3_state_t* ctx, const void* data, size_t len) {
    XXH3_128bits_update(ctx, data, len);
}

int xxh3_128_final(XXH3_state_t* ctx, uint8_t* hash) {
    XXH128_hash_t digest = XXH3_128bits_digest(ctx);
    XXH128_canonical_t cano;
    XXH128_canonicalFromHash(&cano, digest);
    memcpy(hash, cano.digest, XXH128_DIGEST_LENGTH);
    XXH3_freeState(ctx);
    return XXH128_DIGEST_LENGTH;
}
