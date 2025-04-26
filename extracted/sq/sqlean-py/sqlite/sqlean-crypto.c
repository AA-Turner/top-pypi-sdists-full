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

uint8_t* base85_encode(const uint8_t* src, size_t len, size_t* out_len) {
    uint8_t* encoded = malloc(len * 5 / 4 + 5);
    if (encoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    // Encode each tuple of 4 bytes
    uint32_t digits[5], tuple;
    size_t pos = 0;
    for (size_t i = 0; i < len; i += 4) {
        // Read 32-bit unsigned integer from bytes following the
        // big-endian convention (most significant byte first)
        tuple = (((src[i]) << 24) + ((src[i + 1] << 16) & 0xFF0000) + ((src[i + 2] << 8) & 0xFF00) +
                 ((src[i + 3]) & 0xFF));

        if (tuple > 0) {
            // Calculate 5 digits by repeatedly dividing
            // by 85 and taking the remainder
            for (size_t j = 0; j < 5; j++) {
                digits[4 - j] = tuple % 85;
                tuple = tuple / 85;
            }

            // Omit final characters added due to bytes of padding
            size_t num_padding = 0;
            if (len < i + 4) {
                num_padding = (i + 4) - len;
            }
            for (size_t j = 0; j < 5 - num_padding; j++) {
                encoded[pos++] = digits[j] + 33;
            }
        } else {
            // An all-zero tuple is encoded as a single character
            encoded[pos++] = 'z';
        }
    }

    *out_len = len * 5 / 4 + (len % 4 ? 1 : 0);
    encoded[*out_len] = '\0';
    return encoded;
}

uint8_t* base85_decode(const uint8_t* src, size_t len, size_t* out_len) {
    uint8_t* decoded = malloc(len * 4 / 5);
    if (decoded == NULL) {
        *out_len = 0;
        return NULL;
    }

    uint8_t digits[5], tupleBytes[4];
    uint32_t tuple;
    size_t pos = 0;
    for (size_t i = 0; i < len;) {
        if (src[i] == 'z') {
            // A single character encodes an all-zero tuple
            decoded[pos++] = 0;
            decoded[pos++] = 0;
            decoded[pos++] = 0;
            decoded[pos++] = 0;
            i++;
        } else {
            // Retrieve radix-85 digits of tuple
            for (int k = 0; k < 5; k++) {
                if (i + k < len) {
                    uint8_t digit = src[i + k] - 33;
                    if (digit < 0 || digit > 84) {
                        *out_len = 0;
                        free(decoded);
                        return NULL;
                    }
                    digits[k] = digit;
                } else {
                    digits[k] = 84;  // Pad with 'u'
                }
            }

            // Create 32-bit binary number from digits and handle padding
            // tuple = a * 85^4 + b * 85^3 + c * 85^2 + d * 85 + e
            tuple = digits[0] * 52200625 + digits[1] * 614125 + digits[2] * 7225 + digits[3] * 85 +
                    digits[4];

            // Get bytes from tuple
            tupleBytes[0] = (tuple >> 24) & 0xff;
            tupleBytes[1] = (tuple >> 16) & 0xff;
            tupleBytes[2] = (tuple >> 8) & 0xff;
            tupleBytes[3] = tuple & 0xff;

            // Remove bytes of padding
            int padding = 0;
            if (i + 4 >= len) {
                padding = i + 4 - len;
            }

            // Append bytes to result
            for (int k = 0; k < 4 - padding; k++) {
                decoded[pos++] = tupleBytes[k];
            }
            i += 5;
        }
    }

    *out_len = len * 4 / 5;
    return decoded;
}
// Created by: Peter Tripp (@notpeter)
// Public Domain

#include <stdlib.h>
#include <memory.h>
#include "crypto/blake3.h"

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
// Originally from blake3 reference implementation, Public Domain
// https://github.com/oconnor663/blake3_reference_impl_c

#include <assert.h>
#include <string.h>

#include "crypto/blake3_reference_impl.h"

#define CHUNK_START 1 << 0
#define CHUNK_END 1 << 1
#define PARENT 1 << 2
#define ROOT 1 << 3
#define KEYED_HASH 1 << 4
#define DERIVE_KEY_CONTEXT 1 << 5
#define DERIVE_KEY_MATERIAL 1 << 6

static uint32_t IV[8] = {
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
};

static size_t MSG_PERMUTATION[16] = {2, 6,  3,  10, 7, 0,  4,  13,
                                     1, 11, 12, 5,  9, 14, 15, 8};

inline static uint32_t rotate_right(uint32_t x, int n) {
  return (x >> n) | (x << (32 - n));
}

// The mixing function, G, which mixes either a column or a diagonal.
inline static void g(uint32_t state[16], size_t a, size_t b, size_t c, size_t d,
                     uint32_t mx, uint32_t my) {
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
                            const uint32_t block_words[16], uint64_t counter,
                            uint32_t block_len, uint32_t flags,
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

  round_function(state, block); // round 1
  permute(block);
  round_function(state, block); // round 2
  permute(block);
  round_function(state, block); // round 3
  permute(block);
  round_function(state, block); // round 4
  permute(block);
  round_function(state, block); // round 5
  permute(block);
  round_function(state, block); // round 6
  permute(block);
  round_function(state, block); // round 7

  for (size_t i = 0; i < 8; i++) {
    state[i] ^= state[i + 8];
    state[i + 8] ^= chaining_value[i];
  }

  memcpy(out, state, sizeof(state));
}

inline static void words_from_little_endian_bytes(const void *bytes,
                                                  size_t bytes_len,
                                                  uint32_t *out) {
  assert(bytes_len % 4 == 0);
  const uint8_t *u8_ptr = (const uint8_t *)bytes;
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

inline static void output_chaining_value(const output *self, uint32_t out[8]) {
  uint32_t out16[16];
  compress(self->input_chaining_value, self->block_words, self->counter,
           self->block_len, self->flags, out16);
  memcpy(out, out16, 8 * 4);
}

inline static void output_root_bytes(const output *self, void *out,
                                     size_t out_len) {
  uint8_t *out_u8 = (uint8_t *)out;
  uint64_t output_block_counter = 0;
  while (out_len > 0) {
    uint32_t words[16];
    compress(self->input_chaining_value, self->block_words,
             output_block_counter, self->block_len, self->flags | ROOT, words);
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

inline static void chunk_state_init(_blake3_chunk_state *self,
                                    const uint32_t key_words[8],
                                    uint64_t chunk_counter, uint32_t flags) {
  memcpy(self->chaining_value, key_words, sizeof(self->chaining_value));
  self->chunk_counter = chunk_counter;
  memset(self->block, 0, sizeof(self->block));
  self->block_len = 0;
  self->blocks_compressed = 0;
  self->flags = flags;
}

inline static size_t chunk_state_len(const _blake3_chunk_state *self) {
  return BLAKE3_BLOCK_LEN * (size_t)self->blocks_compressed +
         (size_t)self->block_len;
}

inline static uint32_t chunk_state_start_flag(const _blake3_chunk_state *self) {
  if (self->blocks_compressed == 0) {
    return CHUNK_START;
  } else {
    return 0;
  }
}

inline static void chunk_state_update(_blake3_chunk_state *self,
                                      const void *input, size_t input_len) {
  const uint8_t *input_u8 = (const uint8_t *)input;
  while (input_len > 0) {
    // If the block buffer is full, compress it and clear it. More input is
    // coming, so this compression is not CHUNK_END.
    if (self->block_len == BLAKE3_BLOCK_LEN) {
      uint32_t block_words[16];
      words_from_little_endian_bytes(self->block, BLAKE3_BLOCK_LEN,
                                     block_words);
      uint32_t out16[16];
      compress(self->chaining_value, block_words, self->chunk_counter,
               BLAKE3_BLOCK_LEN, self->flags | chunk_state_start_flag(self),
               out16);
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

inline static output chunk_state_output(const _blake3_chunk_state *self) {
  output ret;
  memcpy(ret.input_chaining_value, self->chaining_value,
         sizeof(ret.input_chaining_value));
  words_from_little_endian_bytes(self->block, sizeof(self->block),
                                 ret.block_words);
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
  ret.counter = 0; // Always 0 for parent nodes.
  ret.block_len =
      BLAKE3_BLOCK_LEN; // Always BLAKE3_BLOCK_LEN (64) for parent nodes.
  ret.flags = PARENT | flags;
  return ret;
}

inline static void parent_cv(const uint32_t left_child_cv[8],
                             const uint32_t right_child_cv[8],
                             const uint32_t key_words[8], uint32_t flags,
                             uint32_t out[8]) {
  output o = parent_output(left_child_cv, right_child_cv, key_words, flags);
  // We only write to `out` after we've read the inputs. That makes it safe for
  // `out` to alias an input, which we do below.
  output_chaining_value(&o, out);
}

inline static void hasher_init_internal(blake3_hasher *self,
                                        const uint32_t key_words[8],
                                        uint32_t flags) {
  chunk_state_init(&self->chunk_state, key_words, 0, flags);
  memcpy(self->key_words, key_words, sizeof(self->key_words));
  self->cv_stack_len = 0;
  self->flags = flags;
}

// Construct a new `Hasher` for the regular hash function.
void blake3_hasher_init(blake3_hasher *self) {
  hasher_init_internal(self, IV, 0);
}

// Construct a new `Hasher` for the keyed hash function.
void blake3_hasher_init_keyed(blake3_hasher *self,
                              const uint8_t key[BLAKE3_KEY_LEN]) {
  uint32_t key_words[8];
  words_from_little_endian_bytes(key, BLAKE3_KEY_LEN, key_words);
  hasher_init_internal(self, key_words, KEYED_HASH);
}

// Construct a new `Hasher` for the key derivation function. The context
// string should be hardcoded, globally unique, and application-specific.
void blake3_hasher_init_derive_key(blake3_hasher *self, const char *context) {
  blake3_hasher context_hasher;
  hasher_init_internal(&context_hasher, IV, DERIVE_KEY_CONTEXT);
  blake3_hasher_update(&context_hasher, context, strlen(context));
  uint8_t context_key[BLAKE3_KEY_LEN];
  blake3_hasher_finalize(&context_hasher, context_key, BLAKE3_KEY_LEN);
  uint32_t context_key_words[8];
  words_from_little_endian_bytes(context_key, BLAKE3_KEY_LEN,
                                 context_key_words);
  hasher_init_internal(self, context_key_words, DERIVE_KEY_MATERIAL);
}

inline static void hasher_push_stack(blake3_hasher *self,
                                     const uint32_t cv[8]) {
  memcpy(&self->cv_stack[(size_t)self->cv_stack_len * 8], cv, 8 * 4);
  self->cv_stack_len++;
}

// Returns a pointer to the popped CV, which is valid until the next push.
inline static const uint32_t *hasher_pop_stack(blake3_hasher *self) {
  self->cv_stack_len--;
  return &self->cv_stack[(size_t)self->cv_stack_len * 8];
}

// Section 5.1.2 of the BLAKE3 spec explains this algorithm in more detail.
inline static void hasher_add_chunk_cv(blake3_hasher *self, uint32_t new_cv[8],
                                       uint64_t total_chunks) {
  // This chunk might complete some subtrees. For each completed subtree, its
  // left child will be the current top entry in the CV stack, and its right
  // child will be the current value of `new_cv`. Pop each left child off the
  // stack, merge it with `new_cv`, and overwrite `new_cv` with the result.
  // After all these merges, push the final value of `new_cv` onto the stack.
  // The number of completed subtrees is given by the number of trailing 0-bits
  // in the new total number of chunks.
  while ((total_chunks & 1) == 0) {
    parent_cv(hasher_pop_stack(self), new_cv, self->key_words, self->flags,
              new_cv);
    total_chunks >>= 1;
  }
  hasher_push_stack(self, new_cv);
}

// Add input to the hash state. This can be called any number of times.
void blake3_hasher_update(blake3_hasher *self, const void *input,
                          size_t input_len) {
  const uint8_t *input_u8 = (const uint8_t *)input;
  while (input_len > 0) {
    // If the current chunk is complete, finalize it and reset the chunk state.
    // More input is coming, so this chunk is not ROOT.
    if (chunk_state_len(&self->chunk_state) == BLAKE3_CHUNK_LEN) {
      output chunk_output = chunk_state_output(&self->chunk_state);
      uint32_t chunk_cv[8];
      output_chaining_value(&chunk_output, chunk_cv);
      uint64_t total_chunks = self->chunk_state.chunk_counter + 1;
      hasher_add_chunk_cv(self, chunk_cv, total_chunks);
      chunk_state_init(&self->chunk_state, self->key_words, total_chunks,
                       self->flags);
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
void blake3_hasher_finalize(const blake3_hasher *self, void *out,
                            size_t out_len) {
  // Starting with the output from the current chunk, compute all the parent
  // chaining values along the right edge of the tree, until we have the root
  // output.
  output current_output = chunk_state_output(&self->chunk_state);
  size_t parent_nodes_remaining = (size_t)self->cv_stack_len;
  while (parent_nodes_remaining > 0) {
    parent_nodes_remaining--;
    uint32_t current_cv[8];
    output_chaining_value(&current_output, current_cv);
    current_output = parent_output(&self->cv_stack[parent_nodes_remaining * 8],
                                   current_cv, self->key_words, self->flags);
  }
  output_root_bytes(&current_output, out, out_len);
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
        sprintf((char*)encoded + (i * 2), "%02x", src[i]);
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
 * FILE:    sha2.c
 * AUTHOR:  Aaron D. Gifford - http://www.aarongifford.com/
 *
 * Copyright (c) 2000-2001, Aaron D. Gifford
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
 * 3. Neither the name of the copyright holder nor the names of contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTOR(S) ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTOR(S) BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * $Id: sha2.c,v 1.1 2001/11/08 00:01:51 adg Exp adg $
 */

#include <assert.h> /* assert() */
#include <stdlib.h>
#include <string.h> /* memcpy()/memset() or bcopy()/bzero() */

#include "crypto/sha2.h"

/*
 * ASSERT NOTE:
 * Some sanity checking code is included using assert().  On my FreeBSD
 * system, this additional code can be removed by compiling with NDEBUG
 * defined.  Check your own systems manpage on assert() to see how to
 * compile WITHOUT the sanity checking code on your system.
 *
 * UNROLLED TRANSFORM LOOP NOTE:
 * You can define SHA2_UNROLL_TRANSFORM to use the unrolled transform
 * loop version for the hash transform rounds (defined using macros
 * later in this file).  Either define on the command line, for example:
 *
 *   cc -DSHA2_UNROLL_TRANSFORM -o sha2 sha2.c sha2prog.c
 *
 * or define below:
 *
 *   #define SHA2_UNROLL_TRANSFORM
 *
 */

/*** SHA-256/384/512 Machine Architecture Definitions *****************/
/*
 * BYTE_ORDER NOTE:
 *
 * Please make sure that your system defines BYTE_ORDER.  If your
 * architecture is little-endian, make sure it also defines
 * LITTLE_ENDIAN and that the two (BYTE_ORDER and LITTLE_ENDIAN) are
 * equivilent.
 *
 * If your system does not define the above, then you can do so by
 * hand like this:
 *
 *   #define LITTLE_ENDIAN 1234
 *   #define BIG_ENDIAN    4321
 *
 * And for little-endian machines, add:
 *
 *   #define BYTE_ORDER LITTLE_ENDIAN
 *
 * Or for big-endian machines:
 *
 *   #define BYTE_ORDER BIG_ENDIAN
 *
 * The FreeBSD machine this was written on defines BYTE_ORDER
 * appropriately by including <sys/types.h> (which in turn includes
 * <machine/endian.h> where the appropriate definitions are actually
 * made).
 */

#ifdef __BYTE_ORDER__
#ifndef BYTE_ORDER
#define BYTE_ORDER __BYTE_ORDER__
#endif
#ifndef BIG_ENDIAN
#define BIG_ENDIAN __ORDER_BIG_ENDIAN__
#endif
#ifndef LITTLE_ENDIAN
#define LITTLE_ENDIAN __ORDER_LITTLE_ENDIAN__
#endif
#endif

#ifndef BYTE_ORDER
#if defined(i386) || defined(__i386__) || defined(_M_IX86) || defined(__x86_64) ||    \
    defined(__x86_64__) || defined(_M_X64) || defined(_M_AMD64) || defined(_M_ARM) || \
    defined(__x86) || defined(__arm__)
#define BYTE_ORDER 1234
#elif defined(sparc) || defined(__ppc__)
#define BYTE_ORDER 4321
#else
#define BYTE_ORDER 0
#endif
#endif

#if !defined(BYTE_ORDER) || (BYTE_ORDER != LITTLE_ENDIAN && BYTE_ORDER != BIG_ENDIAN)
#error Define BYTE_ORDER to be equal to either LITTLE_ENDIAN or BIG_ENDIAN
#endif

/*
 * Define the followingsha2_* types to types of the correct length on
 * the native archtecture.   Most BSD systems and Linux define u_intXX_t
 * types.  Machines with very recent ANSI C headers, can use the
 * uintXX_t definintions from inttypes.h by defining SHA2_USE_INTTYPES_H
 * during compile or in the sha.h header file.
 *
 * Machines that support neither u_intXX_t nor inttypes.h's uintXX_t
 * will need to define these three typedefs below (and the appropriate
 * ones in sha.h too) by hand according to their system architecture.
 *
 * Thank you, Jun-ichiro itojun Hagino, for suggesting using u_intXX_t
 * types and pointing out recent ANSI C support for uintXX_t in inttypes.h.
 */
#ifdef SHA2_USE_INTTYPES_H

typedef uint8_t sha2_byte;    /* Exactly 1 byte */
typedef uint32_t sha2_word32; /* Exactly 4 bytes */
typedef uint64_t sha2_word64; /* Exactly 8 bytes */

#else /* SHA2_USE_INTTYPES_H */

typedef u_int8_t sha2_byte;    /* Exactly 1 byte */
typedef u_int32_t sha2_word32; /* Exactly 4 bytes */
typedef u_int64_t sha2_word64; /* Exactly 8 bytes */

#endif /* SHA2_USE_INTTYPES_H */

/*** SHA-256/384/512 Various Length Definitions ***********************/
/* NOTE: Most of these are in sha2.h */
#define SHA256_SHORT_BLOCK_LENGTH (SHA256_BLOCK_LENGTH - 8)
#define SHA384_SHORT_BLOCK_LENGTH (SHA384_BLOCK_LENGTH - 16)
#define SHA512_SHORT_BLOCK_LENGTH (SHA512_BLOCK_LENGTH - 16)

/*** ENDIAN REVERSAL MACROS *******************************************/
#if BYTE_ORDER == LITTLE_ENDIAN
#define REVERSE32(w, x)                                                  \
    {                                                                    \
        sha2_word32 tmp = (w);                                           \
        tmp = (tmp >> 16) | (tmp << 16);                                 \
        (x) = ((tmp & 0xff00ff00UL) >> 8) | ((tmp & 0x00ff00ffUL) << 8); \
    }
#define REVERSE64(w, x)                                                                      \
    {                                                                                        \
        sha2_word64 tmp = (w);                                                               \
        tmp = (tmp >> 32) | (tmp << 32);                                                     \
        tmp = ((tmp & 0xff00ff00ff00ff00ULL) >> 8) | ((tmp & 0x00ff00ff00ff00ffULL) << 8);   \
        (x) = ((tmp & 0xffff0000ffff0000ULL) >> 16) | ((tmp & 0x0000ffff0000ffffULL) << 16); \
    }
#endif /* BYTE_ORDER == LITTLE_ENDIAN */

/*
 * Macro for incrementally adding the unsigned 64-bit integer n to the
 * unsigned 128-bit integer (represented using a two-element array of
 * 64-bit words):
 */
#define ADDINC128(w, n)             \
    {                               \
        (w)[0] += (sha2_word64)(n); \
        if ((w)[0] < (n)) {         \
            (w)[1]++;               \
        }                           \
    }

/*
 * Macros for copying blocks of memory and for zeroing out ranges
 * of memory.  Using these macros makes it easy to switch from
 * using memset()/memcpy() and using bzero()/bcopy().
 *
 * Please define either SHA2_USE_MEMSET_MEMCPY or define
 * SHA2_USE_BZERO_BCOPY depending on which function set you
 * choose to use:
 */
#if !defined(SHA2_USE_MEMSET_MEMCPY) && !defined(SHA2_USE_BZERO_BCOPY)
/* Default to memset()/memcpy() if no option is specified */
#define SHA2_USE_MEMSET_MEMCPY 1
#endif
#if defined(SHA2_USE_MEMSET_MEMCPY) && defined(SHA2_USE_BZERO_BCOPY)
/* Abort with an error if BOTH options are defined */
#error Define either SHA2_USE_MEMSET_MEMCPY or SHA2_USE_BZERO_BCOPY, not both!
#endif

#ifdef SHA2_USE_MEMSET_MEMCPY
#define MEMSET_BZERO(p, l) memset((p), 0, (l))
#define MEMCPY_BCOPY(d, s, l) memcpy((d), (s), (l))
#endif
#ifdef SHA2_USE_BZERO_BCOPY
#define MEMSET_BZERO(p, l) bzero((p), (l))
#define MEMCPY_BCOPY(d, s, l) bcopy((s), (d), (l))
#endif

/*** THE SIX LOGICAL FUNCTIONS ****************************************/
/*
 * Bit shifting and rotation (used by the six SHA-XYZ logical functions:
 *
 *   NOTE:  The naming of R and S appears backwards here (R is a SHIFT and
 *   S is a ROTATION) because the SHA-256/384/512 description document
 *   (see http://csrc.nist.gov/cryptval/shs/sha256-384-512.pdf) uses this
 *   same "backwards" definition.
 */
/* Shift-right (used in SHA-256, SHA-384, and SHA-512): */
#define R(b, x) ((x) >> (b))
/* 32-bit Rotate-right (used in SHA-256): */
#define S32(b, x) (((x) >> (b)) | ((x) << (32 - (b))))
/* 64-bit Rotate-right (used in SHA-384 and SHA-512): */
#define S64(b, x) (((x) >> (b)) | ((x) << (64 - (b))))

/* Two of six logical functions used in SHA-256, SHA-384, and SHA-512: */
#define Ch(x, y, z) (((x) & (y)) ^ ((~(x)) & (z)))
#define Maj(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))

/* Four of six logical functions used in SHA-256: */
#define Sigma0_256(x) (S32(2, (x)) ^ S32(13, (x)) ^ S32(22, (x)))
#define Sigma1_256(x) (S32(6, (x)) ^ S32(11, (x)) ^ S32(25, (x)))
#define sigma0_256(x) (S32(7, (x)) ^ S32(18, (x)) ^ R(3, (x)))
#define sigma1_256(x) (S32(17, (x)) ^ S32(19, (x)) ^ R(10, (x)))

/* Four of six logical functions used in SHA-384 and SHA-512: */
#define Sigma0_512(x) (S64(28, (x)) ^ S64(34, (x)) ^ S64(39, (x)))
#define Sigma1_512(x) (S64(14, (x)) ^ S64(18, (x)) ^ S64(41, (x)))
#define sigma0_512(x) (S64(1, (x)) ^ S64(8, (x)) ^ R(7, (x)))
#define sigma1_512(x) (S64(19, (x)) ^ S64(61, (x)) ^ R(6, (x)))

/*** INTERNAL FUNCTION PROTOTYPES *************************************/
/* NOTE: These should not be accessed directly from outside this
 * library -- they are intended for private internal visibility/use
 * only.
 */
// void SHA512_Last(SHA512_CTX*);
// void SHA256_Transform(SHA256_CTX*, const sha2_word32*);
// void SHA512_Transform(SHA512_CTX*, const sha2_word64*);

/*** SHA-XYZ INITIAL HASH VALUES AND CONSTANTS ************************/
/* Hash constant words K for SHA-256: */
const static sha2_word32 K256[64] = {
    0x428a2f98UL, 0x71374491UL, 0xb5c0fbcfUL, 0xe9b5dba5UL, 0x3956c25bUL, 0x59f111f1UL,
    0x923f82a4UL, 0xab1c5ed5UL, 0xd807aa98UL, 0x12835b01UL, 0x243185beUL, 0x550c7dc3UL,
    0x72be5d74UL, 0x80deb1feUL, 0x9bdc06a7UL, 0xc19bf174UL, 0xe49b69c1UL, 0xefbe4786UL,
    0x0fc19dc6UL, 0x240ca1ccUL, 0x2de92c6fUL, 0x4a7484aaUL, 0x5cb0a9dcUL, 0x76f988daUL,
    0x983e5152UL, 0xa831c66dUL, 0xb00327c8UL, 0xbf597fc7UL, 0xc6e00bf3UL, 0xd5a79147UL,
    0x06ca6351UL, 0x14292967UL, 0x27b70a85UL, 0x2e1b2138UL, 0x4d2c6dfcUL, 0x53380d13UL,
    0x650a7354UL, 0x766a0abbUL, 0x81c2c92eUL, 0x92722c85UL, 0xa2bfe8a1UL, 0xa81a664bUL,
    0xc24b8b70UL, 0xc76c51a3UL, 0xd192e819UL, 0xd6990624UL, 0xf40e3585UL, 0x106aa070UL,
    0x19a4c116UL, 0x1e376c08UL, 0x2748774cUL, 0x34b0bcb5UL, 0x391c0cb3UL, 0x4ed8aa4aUL,
    0x5b9cca4fUL, 0x682e6ff3UL, 0x748f82eeUL, 0x78a5636fUL, 0x84c87814UL, 0x8cc70208UL,
    0x90befffaUL, 0xa4506cebUL, 0xbef9a3f7UL, 0xc67178f2UL};

/* Initial hash value H for SHA-256: */
const static sha2_word32 sha256_initial_hash_value[8] = {0x6a09e667UL, 0xbb67ae85UL, 0x3c6ef372UL,
                                                         0xa54ff53aUL, 0x510e527fUL, 0x9b05688cUL,
                                                         0x1f83d9abUL, 0x5be0cd19UL};

/* Hash constant words K for SHA-384 and SHA-512: */
const static sha2_word64 K512[80] = {
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

/* Initial hash value H for SHA-384 */
const static sha2_word64 sha384_initial_hash_value[8] = {
    0xcbbb9d5dc1059ed8ULL, 0x629a292a367cd507ULL, 0x9159015a3070dd17ULL, 0x152fecd8f70e5939ULL,
    0x67332667ffc00b31ULL, 0x8eb44a8768581511ULL, 0xdb0c2e0d64f98fa7ULL, 0x47b5481dbefa4fa4ULL};

/* Initial hash value H for SHA-512 */
const static sha2_word64 sha512_initial_hash_value[8] = {
    0x6a09e667f3bcc908ULL, 0xbb67ae8584caa73bULL, 0x3c6ef372fe94f82bULL, 0xa54ff53a5f1d36f1ULL,
    0x510e527fade682d1ULL, 0x9b05688c2b3e6c1fULL, 0x1f83d9abfb41bd6bULL, 0x5be0cd19137e2179ULL};

/*** SHA-256: *********************************************************/
void* sha256_init() {
    SHA256_CTX* context;
    context = malloc(sizeof(SHA256_CTX));
    if (!context)
        return NULL;
    MEMCPY_BCOPY(context->state, sha256_initial_hash_value, SHA256_DIGEST_LENGTH);
    MEMSET_BZERO(context->buffer, SHA256_BLOCK_LENGTH);
    context->bitcount = 0;
    return context;
}

#ifdef SHA2_UNROLL_TRANSFORM

/* Unrolled SHA-256 round macros: */

#if BYTE_ORDER == LITTLE_ENDIAN

#define ROUND256_0_TO_15(a, b, c, d, e, f, g, h)                      \
    REVERSE32(*data++, W256[j]);                                      \
    T1 = (h) + Sigma1_256(e) + Ch((e), (f), (g)) + K256[j] + W256[j]; \
    (d) += T1;                                                        \
    (h) = T1 + Sigma0_256(a) + Maj((a), (b), (c));                    \
    j++

#else /* BYTE_ORDER == LITTLE_ENDIAN */

#define ROUND256_0_TO_15(a, b, c, d, e, f, g, h)                                  \
    T1 = (h) + Sigma1_256(e) + Ch((e), (f), (g)) + K256[j] + (W256[j] = *data++); \
    (d) += T1;                                                                    \
    (h) = T1 + Sigma0_256(a) + Maj((a), (b), (c));                                \
    j++

#endif /* BYTE_ORDER == LITTLE_ENDIAN */

#define ROUND256(a, b, c, d, e, f, g, h)                     \
    s0 = W256[(j + 1) & 0x0f];                               \
    s0 = sigma0_256(s0);                                     \
    s1 = W256[(j + 14) & 0x0f];                              \
    s1 = sigma1_256(s1);                                     \
    T1 = (h) + Sigma1_256(e) + Ch((e), (f), (g)) + K256[j] + \
         (W256[j & 0x0f] += s1 + W256[(j + 9) & 0x0f] + s0); \
    (d) += T1;                                               \
    (h) = T1 + Sigma0_256(a) + Maj((a), (b), (c));           \
    j++

static void SHA256_Transform(SHA256_CTX* context, const sha2_word32* data) {
    sha2_word32 a, b, c, d, e, f, g, h, s0, s1;
    sha2_word32 T1, *W256;
    int j;

    W256 = (sha2_word32*)context->buffer;

    /* Initialize registers with the prev. intermediate value */
    a = context->state[0];
    b = context->state[1];
    c = context->state[2];
    d = context->state[3];
    e = context->state[4];
    f = context->state[5];
    g = context->state[6];
    h = context->state[7];

    j = 0;
    do {
        /* Rounds 0 to 15 (unrolled): */
        ROUND256_0_TO_15(a, b, c, d, e, f, g, h);
        ROUND256_0_TO_15(h, a, b, c, d, e, f, g);
        ROUND256_0_TO_15(g, h, a, b, c, d, e, f);
        ROUND256_0_TO_15(f, g, h, a, b, c, d, e);
        ROUND256_0_TO_15(e, f, g, h, a, b, c, d);
        ROUND256_0_TO_15(d, e, f, g, h, a, b, c);
        ROUND256_0_TO_15(c, d, e, f, g, h, a, b);
        ROUND256_0_TO_15(b, c, d, e, f, g, h, a);
    } while (j < 16);

    /* Now for the remaining rounds to 64: */
    do {
        ROUND256(a, b, c, d, e, f, g, h);
        ROUND256(h, a, b, c, d, e, f, g);
        ROUND256(g, h, a, b, c, d, e, f);
        ROUND256(f, g, h, a, b, c, d, e);
        ROUND256(e, f, g, h, a, b, c, d);
        ROUND256(d, e, f, g, h, a, b, c);
        ROUND256(c, d, e, f, g, h, a, b);
        ROUND256(b, c, d, e, f, g, h, a);
    } while (j < 64);

    /* Compute the current intermediate hash value */
    context->state[0] += a;
    context->state[1] += b;
    context->state[2] += c;
    context->state[3] += d;
    context->state[4] += e;
    context->state[5] += f;
    context->state[6] += g;
    context->state[7] += h;

    /* Clean up */
    a = b = c = d = e = f = g = h = T1 = 0;
}

#else /* SHA2_UNROLL_TRANSFORM */

static void SHA256_Transform(SHA256_CTX* context, const sha2_word32* data) {
    sha2_word32 a, b, c, d, e, f, g, h, s0, s1;
    sha2_word32 T1, T2, *W256;
    int j;

    W256 = (sha2_word32*)context->buffer;

    /* Initialize registers with the prev. intermediate value */
    a = context->state[0];
    b = context->state[1];
    c = context->state[2];
    d = context->state[3];
    e = context->state[4];
    f = context->state[5];
    g = context->state[6];
    h = context->state[7];

    j = 0;
    do {
#if BYTE_ORDER == LITTLE_ENDIAN
        /* Copy data while converting to host byte order */
        REVERSE32(*data++, W256[j]);
        /* Apply the SHA-256 compression function to update a..h */
        T1 = h + Sigma1_256(e) + Ch(e, f, g) + K256[j] + W256[j];
#else  /* BYTE_ORDER == LITTLE_ENDIAN */
        /* Apply the SHA-256 compression function to update a..h with copy */
        T1 = h + Sigma1_256(e) + Ch(e, f, g) + K256[j] + (W256[j] = *data++);
#endif /* BYTE_ORDER == LITTLE_ENDIAN */
        T2 = Sigma0_256(a) + Maj(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + T1;
        d = c;
        c = b;
        b = a;
        a = T1 + T2;

        j++;
    } while (j < 16);

    do {
        /* Part of the message block expansion: */
        s0 = W256[(j + 1) & 0x0f];
        s0 = sigma0_256(s0);
        s1 = W256[(j + 14) & 0x0f];
        s1 = sigma1_256(s1);

        /* Apply the SHA-256 compression function to update a..h */
        T1 = h + Sigma1_256(e) + Ch(e, f, g) + K256[j] +
             (W256[j & 0x0f] += s1 + W256[(j + 9) & 0x0f] + s0);
        T2 = Sigma0_256(a) + Maj(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + T1;
        d = c;
        c = b;
        b = a;
        a = T1 + T2;

        j++;
    } while (j < 64);

    /* Compute the current intermediate hash value */
    context->state[0] += a;
    context->state[1] += b;
    context->state[2] += c;
    context->state[3] += d;
    context->state[4] += e;
    context->state[5] += f;
    context->state[6] += g;
    context->state[7] += h;

    /* Clean up */
    a = b = c = d = e = f = g = h = T1 = T2 = 0;
}

#endif /* SHA2_UNROLL_TRANSFORM */

void sha256_update(SHA256_CTX* context, const sha2_byte* data, size_t len) {
    unsigned int freespace, usedspace;

    if (len == 0) {
        /* Calling with no data is valid - we do nothing */
        return;
    }

    /* Sanity check: */
    assert(context != (SHA256_CTX*)0 && data != (sha2_byte*)0);

    usedspace = (context->bitcount >> 3) % SHA256_BLOCK_LENGTH;
    if (usedspace > 0) {
        /* Calculate how much free space is available in the buffer */
        freespace = SHA256_BLOCK_LENGTH - usedspace;

        if (len >= freespace) {
            /* Fill the buffer completely and process it */
            MEMCPY_BCOPY(&context->buffer[usedspace], data, freespace);
            context->bitcount += freespace << 3;
            len -= freespace;
            data += freespace;
            SHA256_Transform(context, (sha2_word32*)context->buffer);
        } else {
            /* The buffer is not yet full */
            MEMCPY_BCOPY(&context->buffer[usedspace], data, len);
            context->bitcount += len << 3;
            /* Clean up: */
            usedspace = freespace = 0;
            return;
        }
    }
    while (len >= SHA256_BLOCK_LENGTH) {
        /* Process as many complete blocks as we can */
        SHA256_Transform(context, (sha2_word32*)data);
        context->bitcount += SHA256_BLOCK_LENGTH << 3;
        len -= SHA256_BLOCK_LENGTH;
        data += SHA256_BLOCK_LENGTH;
    }
    if (len > 0) {
        /* There's left-overs, so save 'em */
        MEMCPY_BCOPY(context->buffer, data, len);
        context->bitcount += len << 3;
    }
    /* Clean up: */
    usedspace = freespace = 0;
}

int sha256_final(SHA256_CTX* context, sha2_byte digest[SHA256_DIGEST_LENGTH]) {
    sha2_word32* d = (sha2_word32*)digest;
    unsigned int usedspace;

    /* Sanity check: */
    assert(context != (SHA256_CTX*)0);

    /* If no digest buffer is passed, we don't bother doing this: */
    if (digest != (sha2_byte*)0) {
        usedspace = (context->bitcount >> 3) % SHA256_BLOCK_LENGTH;
#if BYTE_ORDER == LITTLE_ENDIAN
        /* Convert FROM host byte order */
        REVERSE64(context->bitcount, context->bitcount);
#endif
        if (usedspace > 0) {
            /* Begin padding with a 1 bit: */
            context->buffer[usedspace++] = 0x80;

            if (usedspace <= SHA256_SHORT_BLOCK_LENGTH) {
                /* Set-up for the last transform: */
                MEMSET_BZERO(&context->buffer[usedspace], SHA256_SHORT_BLOCK_LENGTH - usedspace);
            } else {
                if (usedspace < SHA256_BLOCK_LENGTH) {
                    MEMSET_BZERO(&context->buffer[usedspace], SHA256_BLOCK_LENGTH - usedspace);
                }
                /* Do second-to-last transform: */
                SHA256_Transform(context, (sha2_word32*)context->buffer);

                /* And set-up for the last transform: */
                MEMSET_BZERO(context->buffer, SHA256_SHORT_BLOCK_LENGTH);
            }
        } else {
            /* Set-up for the last transform: */
            MEMSET_BZERO(context->buffer, SHA256_SHORT_BLOCK_LENGTH);

            /* Begin padding with a 1 bit: */
            *context->buffer = 0x80;
        }
        /* Set the bit count: */
        *(sha2_word64*)&context->buffer[SHA256_SHORT_BLOCK_LENGTH] = context->bitcount;

        /* Final transform: */
        SHA256_Transform(context, (sha2_word32*)context->buffer);

#if BYTE_ORDER == LITTLE_ENDIAN
        {
            /* Convert TO host byte order */
            int j;
            for (j = 0; j < 8; j++) {
                REVERSE32(context->state[j], context->state[j]);
                *d++ = context->state[j];
            }
        }
#else
        MEMCPY_BCOPY(d, context->state, SHA256_DIGEST_LENGTH);
#endif
    }

    /* Clean up state data: */
    free(context);
    usedspace = 0;
    return SHA256_DIGEST_LENGTH;
}

/*** SHA-512: *********************************************************/
void* sha512_init() {
    SHA512_CTX* context;
    context = malloc(sizeof(SHA512_CTX));
    if (!context)
        return NULL;
    MEMCPY_BCOPY(context->state, sha512_initial_hash_value, SHA512_DIGEST_LENGTH);
    MEMSET_BZERO(context->buffer, SHA512_BLOCK_LENGTH);
    context->bitcount[0] = context->bitcount[1] = 0;
    return context;
}

#ifdef SHA2_UNROLL_TRANSFORM

/* Unrolled SHA-512 round macros: */
#if BYTE_ORDER == LITTLE_ENDIAN

#define ROUND512_0_TO_15(a, b, c, d, e, f, g, h)                      \
    REVERSE64(*data++, W512[j]);                                      \
    T1 = (h) + Sigma1_512(e) + Ch((e), (f), (g)) + K512[j] + W512[j]; \
    (d) += T1, (h) = T1 + Sigma0_512(a) + Maj((a), (b), (c)), j++

#else /* BYTE_ORDER == LITTLE_ENDIAN */

#define ROUND512_0_TO_15(a, b, c, d, e, f, g, h)                                  \
    T1 = (h) + Sigma1_512(e) + Ch((e), (f), (g)) + K512[j] + (W512[j] = *data++); \
    (d) += T1;                                                                    \
    (h) = T1 + Sigma0_512(a) + Maj((a), (b), (c));                                \
    j++

#endif /* BYTE_ORDER == LITTLE_ENDIAN */

#define ROUND512(a, b, c, d, e, f, g, h)                     \
    s0 = W512[(j + 1) & 0x0f];                               \
    s0 = sigma0_512(s0);                                     \
    s1 = W512[(j + 14) & 0x0f];                              \
    s1 = sigma1_512(s1);                                     \
    T1 = (h) + Sigma1_512(e) + Ch((e), (f), (g)) + K512[j] + \
         (W512[j & 0x0f] += s1 + W512[(j + 9) & 0x0f] + s0); \
    (d) += T1;                                               \
    (h) = T1 + Sigma0_512(a) + Maj((a), (b), (c));           \
    j++

static void SHA512_Transform(SHA512_CTX* context, const sha2_word64* data) {
    sha2_word64 a, b, c, d, e, f, g, h, s0, s1;
    sha2_word64 T1, *W512 = (sha2_word64*)context->buffer;
    int j;

    /* Initialize registers with the prev. intermediate value */
    a = context->state[0];
    b = context->state[1];
    c = context->state[2];
    d = context->state[3];
    e = context->state[4];
    f = context->state[5];
    g = context->state[6];
    h = context->state[7];

    j = 0;
    do {
        ROUND512_0_TO_15(a, b, c, d, e, f, g, h);
        ROUND512_0_TO_15(h, a, b, c, d, e, f, g);
        ROUND512_0_TO_15(g, h, a, b, c, d, e, f);
        ROUND512_0_TO_15(f, g, h, a, b, c, d, e);
        ROUND512_0_TO_15(e, f, g, h, a, b, c, d);
        ROUND512_0_TO_15(d, e, f, g, h, a, b, c);
        ROUND512_0_TO_15(c, d, e, f, g, h, a, b);
        ROUND512_0_TO_15(b, c, d, e, f, g, h, a);
    } while (j < 16);

    /* Now for the remaining rounds up to 79: */
    do {
        ROUND512(a, b, c, d, e, f, g, h);
        ROUND512(h, a, b, c, d, e, f, g);
        ROUND512(g, h, a, b, c, d, e, f);
        ROUND512(f, g, h, a, b, c, d, e);
        ROUND512(e, f, g, h, a, b, c, d);
        ROUND512(d, e, f, g, h, a, b, c);
        ROUND512(c, d, e, f, g, h, a, b);
        ROUND512(b, c, d, e, f, g, h, a);
    } while (j < 80);

    /* Compute the current intermediate hash value */
    context->state[0] += a;
    context->state[1] += b;
    context->state[2] += c;
    context->state[3] += d;
    context->state[4] += e;
    context->state[5] += f;
    context->state[6] += g;
    context->state[7] += h;

    /* Clean up */
    a = b = c = d = e = f = g = h = T1 = 0;
}

#else /* SHA2_UNROLL_TRANSFORM */

static void SHA512_Transform(SHA512_CTX* context, const sha2_word64* data) {
    sha2_word64 a, b, c, d, e, f, g, h, s0, s1;
    sha2_word64 T1, T2, *W512 = (sha2_word64*)context->buffer;
    int j;

    /* Initialize registers with the prev. intermediate value */
    a = context->state[0];
    b = context->state[1];
    c = context->state[2];
    d = context->state[3];
    e = context->state[4];
    f = context->state[5];
    g = context->state[6];
    h = context->state[7];

    j = 0;
    do {
#if BYTE_ORDER == LITTLE_ENDIAN
        /* Convert TO host byte order */
        REVERSE64(*data++, W512[j]);
        /* Apply the SHA-512 compression function to update a..h */
        T1 = h + Sigma1_512(e) + Ch(e, f, g) + K512[j] + W512[j];
#else  /* BYTE_ORDER == LITTLE_ENDIAN */
        /* Apply the SHA-512 compression function to update a..h with copy */
        T1 = h + Sigma1_512(e) + Ch(e, f, g) + K512[j] + (W512[j] = *data++);
#endif /* BYTE_ORDER == LITTLE_ENDIAN */
        T2 = Sigma0_512(a) + Maj(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + T1;
        d = c;
        c = b;
        b = a;
        a = T1 + T2;

        j++;
    } while (j < 16);

    do {
        /* Part of the message block expansion: */
        s0 = W512[(j + 1) & 0x0f];
        s0 = sigma0_512(s0);
        s1 = W512[(j + 14) & 0x0f];
        s1 = sigma1_512(s1);

        /* Apply the SHA-512 compression function to update a..h */
        T1 = h + Sigma1_512(e) + Ch(e, f, g) + K512[j] +
             (W512[j & 0x0f] += s1 + W512[(j + 9) & 0x0f] + s0);
        T2 = Sigma0_512(a) + Maj(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + T1;
        d = c;
        c = b;
        b = a;
        a = T1 + T2;

        j++;
    } while (j < 80);

    /* Compute the current intermediate hash value */
    context->state[0] += a;
    context->state[1] += b;
    context->state[2] += c;
    context->state[3] += d;
    context->state[4] += e;
    context->state[5] += f;
    context->state[6] += g;
    context->state[7] += h;

    /* Clean up */
    a = b = c = d = e = f = g = h = T1 = T2 = 0;
}

#endif /* SHA2_UNROLL_TRANSFORM */

void sha512_update(SHA512_CTX* context, const sha2_byte* data, size_t len) {
    unsigned int freespace, usedspace;

    if (len == 0) {
        /* Calling with no data is valid - we do nothing */
        return;
    }

    /* Sanity check: */
    assert(context != (SHA512_CTX*)0 && data != (sha2_byte*)0);

    usedspace = (context->bitcount[0] >> 3) % SHA512_BLOCK_LENGTH;
    if (usedspace > 0) {
        /* Calculate how much free space is available in the buffer */
        freespace = SHA512_BLOCK_LENGTH - usedspace;

        if (len >= freespace) {
            /* Fill the buffer completely and process it */
            MEMCPY_BCOPY(&context->buffer[usedspace], data, freespace);
            ADDINC128(context->bitcount, freespace << 3);
            len -= freespace;
            data += freespace;
            SHA512_Transform(context, (sha2_word64*)context->buffer);
        } else {
            /* The buffer is not yet full */
            MEMCPY_BCOPY(&context->buffer[usedspace], data, len);
            ADDINC128(context->bitcount, len << 3);
            /* Clean up: */
            usedspace = freespace = 0;
            return;
        }
    }
    while (len >= SHA512_BLOCK_LENGTH) {
        /* Process as many complete blocks as we can */
        SHA512_Transform(context, (sha2_word64*)data);
        ADDINC128(context->bitcount, SHA512_BLOCK_LENGTH << 3);
        len -= SHA512_BLOCK_LENGTH;
        data += SHA512_BLOCK_LENGTH;
    }
    if (len > 0) {
        /* There's left-overs, so save 'em */
        MEMCPY_BCOPY(context->buffer, data, len);
        ADDINC128(context->bitcount, len << 3);
    }
    /* Clean up: */
    usedspace = freespace = 0;
}

static void SHA512_Last(SHA512_CTX* context) {
    unsigned int usedspace;

    usedspace = (context->bitcount[0] >> 3) % SHA512_BLOCK_LENGTH;
#if BYTE_ORDER == LITTLE_ENDIAN
    /* Convert FROM host byte order */
    REVERSE64(context->bitcount[0], context->bitcount[0]);
    REVERSE64(context->bitcount[1], context->bitcount[1]);
#endif
    if (usedspace > 0) {
        /* Begin padding with a 1 bit: */
        context->buffer[usedspace++] = 0x80;

        if (usedspace <= SHA512_SHORT_BLOCK_LENGTH) {
            /* Set-up for the last transform: */
            MEMSET_BZERO(&context->buffer[usedspace], SHA512_SHORT_BLOCK_LENGTH - usedspace);
        } else {
            if (usedspace < SHA512_BLOCK_LENGTH) {
                MEMSET_BZERO(&context->buffer[usedspace], SHA512_BLOCK_LENGTH - usedspace);
            }
            /* Do second-to-last transform: */
            SHA512_Transform(context, (sha2_word64*)context->buffer);

            /* And set-up for the last transform: */
            MEMSET_BZERO(context->buffer, SHA512_BLOCK_LENGTH - 2);
        }
    } else {
        /* Prepare for final transform: */
        MEMSET_BZERO(context->buffer, SHA512_SHORT_BLOCK_LENGTH);

        /* Begin padding with a 1 bit: */
        *context->buffer = 0x80;
    }
    /* Store the length of input data (in bits): */
    *(sha2_word64*)&context->buffer[SHA512_SHORT_BLOCK_LENGTH] = context->bitcount[1];
    *(sha2_word64*)&context->buffer[SHA512_SHORT_BLOCK_LENGTH + 8] = context->bitcount[0];

    /* Final transform: */
    SHA512_Transform(context, (sha2_word64*)context->buffer);
}

int sha512_final(SHA512_CTX* context, sha2_byte digest[SHA512_DIGEST_LENGTH]) {
    sha2_word64* d = (sha2_word64*)digest;

    /* Sanity check: */
    assert(context != (SHA512_CTX*)0);

    /* If no digest buffer is passed, we don't bother doing this: */
    if (digest != (sha2_byte*)0) {
        SHA512_Last(context);

        /* Save the hash data for output: */
#if BYTE_ORDER == LITTLE_ENDIAN
        {
            /* Convert TO host byte order */
            int j;
            for (j = 0; j < 8; j++) {
                REVERSE64(context->state[j], context->state[j]);
                *d++ = context->state[j];
            }
        }
#else
        MEMCPY_BCOPY(d, context->state, SHA512_DIGEST_LENGTH);
#endif
    }

    /* Zero out state data */
    free(context);
    return SHA512_DIGEST_LENGTH;
}

/*** SHA-384: *********************************************************/
void* sha384_init() {
    SHA384_CTX* context;
    context = malloc(sizeof(SHA384_CTX));
    if (!context)
        return NULL;
    MEMCPY_BCOPY(context->state, sha384_initial_hash_value, SHA512_DIGEST_LENGTH);
    MEMSET_BZERO(context->buffer, SHA384_BLOCK_LENGTH);
    context->bitcount[0] = context->bitcount[1] = 0;
    return context;
}

void sha384_update(SHA384_CTX* context, const sha2_byte* data, size_t len) {
    sha512_update((SHA512_CTX*)context, data, len);
}

int sha384_final(SHA384_CTX* context, sha2_byte digest[SHA384_DIGEST_LENGTH]) {
    sha2_word64* d = (sha2_word64*)digest;

    /* Sanity check: */
    assert(context != (SHA384_CTX*)0);

    /* If no digest buffer is passed, we don't bother doing this: */
    if (digest != (sha2_byte*)0) {
        SHA512_Last((SHA512_CTX*)context);

        /* Save the hash data for output: */
#if BYTE_ORDER == LITTLE_ENDIAN
        {
            /* Convert TO host byte order */
            int j;
            for (j = 0; j < 6; j++) {
                REVERSE64(context->state[j], context->state[j]);
                *d++ = context->state[j];
            }
        }
#else
        MEMCPY_BCOPY(d, context->state, SHA384_DIGEST_LENGTH);
#endif
    }

    /* Zero out state data */
    free(context);
    return SHA384_DIGEST_LENGTH;
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
