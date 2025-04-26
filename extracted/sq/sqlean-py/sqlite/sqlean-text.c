// Copyright (c) 2024 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Case conversion functions for utf8 strings.

#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "text/utf8/rune.h"
#include "text/utf8/utf8.h"

// utf8_transform converts the utf8 string s using the transform function.
static bool utf8_transform(char* s, size_t n, uint32_t (*transform)(uint32_t)) {
    utf8_decode_t d = {.state = 0};
    while ((n > 0) & (*s != 0)) {
        size_t i = 0;
        do {
            utf8_decode(&d, (uint8_t)s[i++]);
        } while (d.state);
        uint32_t c = transform(d.codep);
        int len = utf8_encode(s, c);
        if (len == 0) {
            return false;
        }
        s += len;
        n -= len;
    }
    return true;
}

// utf8_tolower converts the utf8 string s to lowercase.
// Returns true if successful, false if an error occurred.
bool utf8_tolower(char* s, size_t n) {
    return utf8_transform(s, n, rune_tolower);
}

// utf8_toupper converts the utf8 string s to uppercase.
bool utf8_toupper(char* s, size_t n) {
    return utf8_transform(s, n, rune_toupper);
}

// utf8_casefold converts the utf8 string s to folded-case.
bool utf8_casefold(char* s, size_t n) {
    return utf8_transform(s, n, rune_casefold);
}

// utf8_totitle converts the utf8 string s to title-case.
bool utf8_totitle(char* s, size_t n) {
    utf8_decode_t d = {.state = 0};
    bool upper = true;
    while ((n > 0) & (*s != 0)) {
        size_t i = 0;
        do {
            utf8_decode(&d, (uint8_t)s[i++]);
        } while (d.state);
        uint32_t c = upper ? rune_toupper(d.codep) : rune_tolower(d.codep);
        int len = utf8_encode(s, c);
        if (len == 0) {
            return false;
        }
        upper = !rune_isword(d.codep);
        s += len;
        n -= len;
    }
    return true;
}
/* MIT License
 *
 * Copyright (c) 2023 Tyge Løvset
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

// Rune (utf8 codepoint) handling.

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "text/utf8/rune.h"

#include "text/utf8/groups.h"
#include "text/utf8/tables.h"

#define c_arraylen(a) (size_t)(sizeof(a) / sizeof 0 [a])

// rune_isgroup returns true if c is in the unicode group.
static bool rune_isgroup(int group, uint32_t c) {
    for (int j = 0; j < _utf8_unicode_groups[group].nr16; ++j) {
        if (c < _utf8_unicode_groups[group].r16[j].lo) {
            return false;
        }
        if (c <= _utf8_unicode_groups[group].r16[j].hi) {
            return true;
        }
    }
    return false;
}

// rune_isupper returns true if c is an uppercase letter.
bool rune_isupper(uint32_t c) {
    return rune_tolower(c) != c;
}

// rune_islower returns true if c is a lowercase letter.
bool rune_islower(uint32_t c) {
    return rune_toupper(c) != c;
}

// rune_isdigit returns true if c is a digit character.
bool rune_isdigit(uint32_t c) {
    if (c < 128) {
        return isdigit((int)c) != 0;
    }
    return rune_isgroup(U8G_Nd, c);
}

// rune_isalpha returns true if c is an alphabetic character.
bool rune_isalpha(uint32_t c) {
    static int16_t groups[] = {U8G_Latin, U8G_Nl,         U8G_Greek, U8G_Cyrillic,
                               U8G_Han,   U8G_Devanagari, U8G_Arabic};
    if (c < 128) {
        return isalpha((int)c) != 0;
    }
    for (size_t j = 0; j < c_arraylen(groups); ++j) {
        if (rune_isgroup(groups[j], c)) {
            return true;
        }
    }
    return false;
}

// rune_isalnum returns true if c is an alphanumeric character.
bool rune_isalnum(uint32_t c) {
    if (c < 128) {
        return isalnum((int)c) != 0;
    }
    return rune_isalpha(c) || rune_isgroup(U8G_Nd, c);
}

// rune_isblank returns true if c is a blank character.
bool rune_isblank(uint32_t c) {
    if (c < 128) {
        return (c == ' ') | (c == '\t');
    }
    return rune_isgroup(U8G_Zs, c);
}

// rune_isspace returns true if c is a whitespace character.
bool rune_isspace(uint32_t c) {
    if (c < 128) {
        return isspace((int)c) != 0;
    }
    return ((c == 8232) | (c == 8233)) || rune_isgroup(U8G_Zs, c);
}

// rune_iscased returns true if c is a cased character.
bool rune_iscased(uint32_t c) {
    if (c < 128) {
        return isalpha((int)c) != 0;
    }
    return rune_islower(c) || rune_isupper(c) || rune_isgroup(U8G_Lt, c);
}

// rune_isword returns true if c is a word character.
bool rune_isword(uint32_t c) {
    if (c < 128) {
        return (isalnum((int)c) != 0) | (c == '_');
    }
    return rune_isalpha(c) || rune_isgroup(U8G_Nd, c) || rune_isgroup(U8G_Pc, c);
}

// Character transformation functions.

// rune_casefold returns the unicode casefold of c.
uint32_t rune_casefold(uint32_t c) {
    for (int i = 0; i < casefold_len; ++i) {
        const struct CaseMapping entry = casemappings[i];
        if (c <= entry.c2) {
            if (c < entry.c1) {
                return c;
            }
            int d = entry.m2 - entry.c2;
            if (d == 1) {
                return c + ((entry.c2 & 1) == (c & 1));
            }
            return (uint32_t)((int)c + d);
        }
    }
    return c;
}

// rune_tolower returns the lowercase version of c.
uint32_t rune_tolower(uint32_t c) {
    for (int i = 0; i < (int)(sizeof upcase_ind / sizeof *upcase_ind); ++i) {
        const struct CaseMapping entry = casemappings[upcase_ind[i]];
        if (c <= entry.c2) {
            if (c < entry.c1) {
                return c;
            }
            int d = entry.m2 - entry.c2;
            if (d == 1) {
                return c + ((entry.c2 & 1) == (c & 1));
            }
            return (uint32_t)((int)c + d);
        }
    }
    return c;
}

// rune_toupper returns the uppercase version of c.
uint32_t rune_toupper(uint32_t c) {
    for (int i = 0; i < (int)(sizeof lowcase_ind / sizeof *lowcase_ind); ++i) {
        const struct CaseMapping entry = casemappings[lowcase_ind[i]];
        if (c <= entry.m2) {
            int d = entry.m2 - entry.c2;
            if (c < (uint32_t)(entry.c1 + d)) {
                return c;
            }
            if (d == 1) {
                return c - ((entry.m2 & 1) == (c & 1));
            }
            return (uint32_t)((int)c - d);
        }
    }
    return c;
}
/* MIT License
 *
 * Copyright (c) 2023 Tyge Løvset
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

// UTF-8 string handling.

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "text/utf8/rune.h"
#include "text/utf8/utf8.h"

const uint8_t utf8_dtab[] = {
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  7,
    7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,
    7,  7,  7,  7,  7,  7,  7,  7,  8,  8,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,
    2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  10, 3,  3,  3,  3,  3,
    3,  3,  3,  3,  3,  3,  3,  4,  3,  3,  11, 6,  6,  6,  5,  8,  8,  8,  8,  8,  8,  8,  8,
    8,  8,  8,  0,  12, 24, 36, 60, 96, 84, 12, 12, 12, 48, 72, 12, 12, 12, 12, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 0,  12, 12, 12, 12, 12, 0,  12, 0,  12, 12, 12, 24, 12, 12, 12, 12, 12,
    24, 12, 24, 12, 12, 12, 12, 12, 12, 12, 12, 12, 24, 12, 12, 12, 12, 12, 24, 12, 12, 12, 12,
    12, 12, 12, 24, 12, 12, 12, 12, 12, 12, 12, 12, 12, 36, 12, 36, 12, 12, 12, 36, 12, 12, 12,
    12, 12, 36, 12, 36, 12, 12, 12, 36, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
};

// Encode/decode functions.

// utf8_decode decodes a byte as part of a utf8 codepoint.
uint32_t utf8_decode(utf8_decode_t* d, const uint32_t byte) {
    const uint32_t type = utf8_dtab[byte];
    d->codep = d->state ? (byte & 0x3fu) | (d->codep << 6) : (0xffU >> type) & byte;
    return d->state = utf8_dtab[256 + d->state + type];
}

// utf8_encode encodes the utf8 codepoint c to s
// and returns the number of bytes written.
int utf8_encode(char* out, uint32_t c) {
    if (c < 0x80U) {
        out[0] = (char)c;
        return 1;
    } else if (c < 0x0800U) {
        out[0] = (char)((c >> 6 & 0x1F) | 0xC0);
        out[1] = (char)((c & 0x3F) | 0x80);
        return 2;
    } else if (c < 0x010000U) {
        if ((c < 0xD800U) | (c >= 0xE000U)) {
            out[0] = (char)((c >> 12 & 0x0F) | 0xE0);
            out[1] = (char)((c >> 6 & 0x3F) | 0x80);
            out[2] = (char)((c & 0x3F) | 0x80);
            return 3;
        }
    } else if (c < 0x110000U) {
        out[0] = (char)((c >> 18 & 0x07) | 0xF0);
        out[1] = (char)((c >> 12 & 0x3F) | 0x80);
        out[2] = (char)((c >> 6 & 0x3F) | 0x80);
        out[3] = (char)((c & 0x3F) | 0x80);
        return 4;
    }
    return 0;
}

// String functions.

// utf8_at returns a pointer to the utf8 codepoint at index in s.
const char* utf8_at(const char* s, size_t n, size_t index) {
    while ((index > 0) & (*s != 0) & (n-- != 0)) {
        index -= (*++s & 0xC0) != 0x80;
    }
    return s;
}

// utf8_pos returns the byte position of the utf8 codepoint at index in s.
size_t utf8_pos(const char* s, size_t n, size_t index) {
    return (size_t)(utf8_at(s, n, index) - s);
}

// utf8_len returns the number of utf8 codepoints in s.
size_t utf8_len(const char* s, size_t n) {
    size_t size = 0;
    while ((n-- != 0) & (*s != 0)) {
        size += (*++s & 0xC0) != 0x80;
    }
    return size;
}

// utf8_peek returns the utf8 codepoint at the start of s.
uint32_t utf8_peek(const char* s) {
    utf8_decode_t d = {.state = 0};
    do {
        utf8_decode(&d, (uint8_t)*s++);
    } while (d.state);
    return d.codep;
}

// utf8_peek_at returns the utf8 codepoint at the index pos from s.
uint32_t utf8_peek_at(const char* s, size_t n, size_t pos) {
    return utf8_peek(utf8_at(s, n, pos));
}

// utf8_icmp compares the utf8 strings s1 and s2 case-insensitively.
int utf8_icmp(const char* s1, size_t n1, const char* s2, size_t n2) {
    utf8_decode_t d1 = {.state = 0}, d2 = {.state = 0};
    size_t j1 = 0, j2 = 0;
    while ((j1 < n1) & (j2 < n2)) {
        do {
            utf8_decode(&d1, (uint8_t)s1[j1++]);
        } while (d1.state);
        do {
            utf8_decode(&d2, (uint8_t)s2[j2++]);
        } while (d2.state);
        int32_t c = (int32_t)rune_casefold(d1.codep) - (int32_t)rune_casefold(d2.codep);
        if (c || !s2[j2 - 1])  // OK if n1 and n2 are npos
            return (int)c;
    }
    return (int)(n1 - n2);
}

// utf8_valid returns true if s is a valid utf8 string.
bool utf8_valid(const char* s, size_t n) {
    utf8_decode_t d = {.state = 0};
    while ((n-- != 0) & (*s != 0)) {
        utf8_decode(&d, (uint8_t)*s++);
    }
    return d.state == 0;
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Byte string data structure.

#include <assert.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "text/bstring.h"

// bstring_new creates an empty string.
ByteString bstring_new(void) {
    char* bytes = "\0";
    ByteString str = {.bytes = bytes, .length = 0, .owning = false};
    return str;
}

// bstring_from_cstring creates a new string that wraps an existing C string.
ByteString bstring_from_cstring(const char* const cstring, size_t length) {
    ByteString str = {.bytes = cstring, .length = length, .owning = false};
    return str;
}

// bstring_clone creates a new string by copying an existing C string.
static ByteString bstring_clone(const char* const cstring, size_t length) {
    char* bytes = calloc(length + 1, sizeof(char));
    if (bytes == NULL) {
        ByteString str = {NULL, 0, true};
        return str;
    }
    memcpy(bytes, cstring, length);
    ByteString str = {bytes, length, true};
    return str;
}

// bstring_to_cstring converts the string to a zero-terminated C string.
const char* bstring_to_cstring(ByteString str) {
    if (str.bytes == NULL) {
        return NULL;
    }
    return str.bytes;
}

// bstring_free destroys the string, freeing resources if necessary.
void bstring_free(ByteString str) {
    if (str.owning && str.bytes != NULL) {
        free((void*)str.bytes);
    }
}

// bstring_at returns a character by its index in the string.
char bstring_at(ByteString str, size_t idx) {
    if (str.length == 0) {
        return 0;
    }
    if (idx < 0 || idx >= str.length) {
        return 0;
    };
    return str.bytes[idx];
}

// bstring_slice returns a slice of the string,
// from the `start` index (inclusive) to the `end` index (non-inclusive).
// Negative `start` and `end` values count from the end of the string.
ByteString bstring_slice(ByteString str, int start, int end) {
    if (str.length == 0) {
        return bstring_new();
    }

    // adjusted start index
    start = start < 0 ? (int)str.length + start : start;
    // python-compatible: treat negative start index larger than the length of the string as zero
    start = start < 0 ? 0 : start;
    // adjusted start index should be less the the length of the string
    if (start >= (int)str.length) {
        return bstring_new();
    }

    // adjusted end index
    end = end < 0 ? (int)str.length + end : end;
    // python-compatible: treat end index larger than the length of the string
    // as equal to the length
    end = end > (int)str.length ? (int)str.length : end;
    // adjusted end index should be >= 0
    if (end < 0) {
        return bstring_new();
    }

    // adjusted start index should be less than adjusted end index
    if (start >= end) {
        return bstring_new();
    }

    char* at = (char*)str.bytes + start;
    size_t length = end - start;
    ByteString slice = bstring_clone(at, length);
    return slice;
}

// bstring_substring returns a substring of `length` characters,
// starting from the `start` index.
ByteString bstring_substring(ByteString str, size_t start, size_t length) {
    if (length > str.length - start) {
        length = str.length - start;
    }
    return bstring_slice(str, start, start + length);
}

// bstring_contains_after checks if the other string is a substring of the original string,
// starting at the `start` index.
static bool bstring_contains_after(ByteString str, ByteString other, size_t start) {
    if (start + other.length > str.length) {
        return false;
    }
    for (size_t idx = 0; idx < other.length; idx++) {
        if (str.bytes[start + idx] != other.bytes[idx]) {
            return false;
        }
    }
    return true;
}

// bstring_index_char returns the first index of the character in the string
// after the `start` index, inclusive.
static int bstring_index_char(ByteString str, char chr, size_t start) {
    for (size_t idx = start; idx < str.length; idx++) {
        if (str.bytes[idx] == chr) {
            return idx;
        }
    }
    return -1;
}

// bstring_last_index_char returns the last index of the character in the string
// before the `end` index, inclusive.
static int bstring_last_index_char(ByteString str, char chr, size_t end) {
    if (end >= str.length) {
        return -1;
    }
    for (int idx = end; idx >= 0; idx--) {
        if (str.bytes[idx] == chr) {
            return idx;
        }
    }
    return -1;
}

// bstring_index_after returns the index of the substring in the original string
// after the `start` index, inclusive.
static int bstring_index_after(ByteString str, ByteString other, size_t start) {
    if (other.length == 0) {
        return start;
    }
    if (str.length == 0 || other.length > str.length) {
        return -1;
    }

    size_t cur_idx = start;
    while (cur_idx < str.length) {
        int match_idx = bstring_index_char(str, other.bytes[0], cur_idx);
        if (match_idx == -1) {
            return match_idx;
        }
        if (bstring_contains_after(str, other, match_idx)) {
            return match_idx;
        }
        cur_idx = match_idx + 1;
    }
    return -1;
}

// bstring_index returns the first index of the substring in the original string.
int bstring_index(ByteString str, ByteString other) {
    return bstring_index_after(str, other, 0);
}

// bstring_last_index returns the last index of the substring in the original string.
int bstring_last_index(ByteString str, ByteString other) {
    if (other.length == 0) {
        return str.length - 1;
    }
    if (str.length == 0 || other.length > str.length) {
        return -1;
    }

    int cur_idx = str.length - 1;
    while (cur_idx >= 0) {
        int match_idx = bstring_last_index_char(str, other.bytes[0], cur_idx);
        if (match_idx == -1) {
            return match_idx;
        }
        if (bstring_contains_after(str, other, match_idx)) {
            return match_idx;
        }
        cur_idx = match_idx - 1;
    }

    return -1;
}

// bstring_contains checks if the string contains the substring.
bool bstring_contains(ByteString str, ByteString other) {
    return bstring_index(str, other) != -1;
}

// bstring_equals checks if two strings are equal character by character.
bool bstring_equals(ByteString str, ByteString other) {
    if (str.bytes == NULL && other.bytes == NULL) {
        return true;
    }
    if (str.bytes == NULL || other.bytes == NULL) {
        return false;
    }
    if (str.length != other.length) {
        return false;
    }
    return bstring_contains_after(str, other, 0);
}

// bstring_has_prefix checks if the string starts with the `other` substring.
bool bstring_has_prefix(ByteString str, ByteString other) {
    return bstring_index(str, other) == 0;
}

// bstring_has_suffix checks if the string ends with the `other` substring.
bool bstring_has_suffix(ByteString str, ByteString other) {
    if (other.length == 0) {
        return true;
    }
    int idx = bstring_last_index(str, other);
    return idx < 0 ? false : (size_t)idx == (str.length - other.length);
}

// bstring_count counts how many times the `other` substring is contained in the original string.
size_t bstring_count(ByteString str, ByteString other) {
    if (str.length == 0 || other.length == 0 || other.length > str.length) {
        return 0;
    }

    size_t count = 0;
    size_t char_idx = 0;
    while (char_idx < str.length) {
        int match_idx = bstring_index_after(str, other, char_idx);
        if (match_idx == -1) {
            break;
        }
        count += 1;
        char_idx = match_idx + other.length;
    }

    return count;
}

// bstring_split_part splits the string by the separator and returns the nth part (0-based).
ByteString bstring_split_part(ByteString str, ByteString sep, size_t part) {
    if (str.length == 0 || sep.length > str.length) {
        return bstring_new();
    }
    if (sep.length == 0) {
        if (part == 0) {
            return bstring_slice(str, 0, str.length);
        } else {
            return bstring_new();
        }
    }

    size_t found = 0;
    size_t prev_idx = 0;
    size_t char_idx = 0;
    while (char_idx < str.length) {
        int match_idx = bstring_index_after(str, sep, char_idx);
        if (match_idx == -1) {
            break;
        }
        if (found == part) {
            return bstring_slice(str, prev_idx, match_idx);
        }
        found += 1;
        prev_idx = match_idx + sep.length;
        char_idx = match_idx + sep.length;
    }

    if (found == part) {
        return bstring_slice(str, prev_idx, str.length);
    }

    return bstring_new();
}

// bstring_join joins strings using the separator and returns the resulting string.
ByteString bstring_join(ByteString* strings, size_t count, ByteString sep) {
    // calculate total string length
    size_t total_length = 0;
    for (size_t idx = 0; idx < count; idx++) {
        ByteString str = strings[idx];
        total_length += str.length;
        // no separator after the last one
        if (idx != count - 1) {
            total_length += sep.length;
        }
    }

    // allocate memory for the bytes
    size_t total_size = total_length * sizeof(char);
    char* bytes = malloc(total_size + 1);
    if (bytes == NULL) {
        ByteString str = {NULL, 0, false};
        return str;
    }

    // copy bytes from each string with separator in between
    char* at = bytes;
    for (size_t idx = 0; idx < count; idx++) {
        ByteString str = strings[idx];
        memcpy(at, str.bytes, str.length);
        at += str.length;
        if (idx != count - 1 && sep.length != 0) {
            memcpy(at, sep.bytes, sep.length);
            at += sep.length;
        }
    }

    bytes[total_length] = '\0';
    ByteString str = {bytes, total_length, true};
    return str;
}

// bstring_concat concatenates strings and returns the resulting string.
ByteString bstring_concat(ByteString* strings, size_t count) {
    ByteString sep = bstring_new();
    return bstring_join(strings, count, sep);
}

// bstring_repeat concatenates the string to itself a given number of times
// and returns the resulting string.
ByteString bstring_repeat(ByteString str, size_t count) {
    // calculate total string length
    size_t total_length = str.length * count;

    // allocate memory for the bytes
    size_t total_size = total_length * sizeof(char);
    char* bytes = malloc(total_size + 1);
    if (bytes == NULL) {
        ByteString res = {NULL, 0, false};
        return res;
    }

    // copy bytes
    char* at = bytes;
    for (size_t idx = 0; idx < count; idx++) {
        memcpy(at, str.bytes, str.length);
        at += str.length;
    }

    bytes[total_size] = '\0';
    ByteString res = {bytes, total_length, true};
    return res;
}

// bstring_replace replaces the `old` substring with the `new` substring in the original string,
// but not more than `max_count` times.
ByteString bstring_replace(ByteString str, ByteString old, ByteString new, size_t max_count) {
    // count matches of the old string in the source string
    size_t count = bstring_count(str, old);
    if (count == 0) {
        return bstring_slice(str, 0, str.length);
    }

    // limit the number of replacements
    if (max_count >= 0 && count > max_count) {
        count = max_count;
    }

    // k matches split string into (k+1) parts
    // allocate an array for them
    size_t parts_count = count + 1;
    ByteString* strings = malloc(parts_count * sizeof(ByteString));
    if (strings == NULL) {
        ByteString res = {NULL, 0, false};
        return res;
    }

    // split the source string where it matches the old string
    // and fill the strings array with these parts
    size_t part_idx = 0;
    size_t char_idx = 0;
    while (char_idx < str.length && part_idx < count) {
        int match_idx = bstring_index_after(str, old, char_idx);
        if (match_idx == -1) {
            break;
        }
        // slice from the prevoius match to the current match
        strings[part_idx] = bstring_slice(str, char_idx, match_idx);
        part_idx += 1;
        char_idx = match_idx + old.length;
    }
    // "tail" from the last match to the end of the source string
    strings[part_idx] = bstring_slice(str, char_idx, str.length);

    // join all the parts using new string as a separator
    ByteString res = bstring_join(strings, parts_count, new);
    // free string parts
    for (size_t idx = 0; idx < parts_count; idx++) {
        bstring_free(strings[idx]);
    }
    free(strings);
    return res;
}

// bstring_replace_all replaces all `old` substrings with the `new` substrings
// in the original string.
ByteString bstring_replace_all(ByteString str, ByteString old, ByteString new) {
    return bstring_replace(str, old, new, -1);
}

// bstring_reverse returns the reversed string.
ByteString bstring_reverse(ByteString str) {
    ByteString res = bstring_clone(str.bytes, str.length);
    char* bytes = (char*)res.bytes;
    for (size_t i = 0; i < str.length / 2; i++) {
        char r = bytes[i];
        bytes[i] = bytes[str.length - 1 - i];
        bytes[str.length - 1 - i] = r;
    }
    return res;
}

// bstring_trim_left trims whitespaces from the beginning of the string.
ByteString bstring_trim_left(ByteString str) {
    if (str.length == 0) {
        return bstring_new();
    }
    size_t idx = 0;
    for (; idx < str.length; idx++) {
        if (!isspace(str.bytes[idx])) {
            break;
        }
    }
    return bstring_slice(str, idx, str.length);
}

// bstring_trim_right trims whitespaces from the end of the string.
ByteString bstring_trim_right(ByteString str) {
    if (str.length == 0) {
        return bstring_new();
    }
    size_t idx = str.length - 1;
    for (; idx >= 0; idx--) {
        if (!isspace(str.bytes[idx])) {
            break;
        }
    }
    return bstring_slice(str, 0, idx + 1);
}

// bstring_trim trims whitespaces from the beginning and end of the string.
ByteString bstring_trim(ByteString str) {
    if (str.length == 0) {
        return bstring_new();
    }
    size_t left = 0;
    for (; left < str.length; left++) {
        if (!isspace(str.bytes[left])) {
            break;
        }
    }
    size_t right = str.length - 1;
    for (; right >= 0; right--) {
        if (!isspace(str.bytes[right])) {
            break;
        }
    }
    return bstring_slice(str, left, right + 1);
}

// bstring_print prints the string to stdout.
void bstring_print(ByteString str) {
    if (str.bytes == NULL) {
        printf("<null>\n");
        return;
    }
    printf("'%s' (len=%zu)\n", str.bytes, str.length);
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// SQLite extension for working with text.

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT3

#include "text/bstring.h"
#include "text/rstring.h"
#include "text/utf8/utf8.h"

#pragma region Substrings

// Extracts a substring starting at the `start` position (1-based).
// text_substring(str, start)
// [pg-compatible] substr(string, start)
static void text_substring2(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "start parameter should be integer", -1);
        return;
    }
    int start = sqlite3_value_int(argv[1]);

    // convert to 0-based index
    // postgres-compatible: treat negative index as zero
    start = start > 0 ? start - 1 : 0;

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_res = rstring_slice(s_src, start, s_src.length);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_res);
}

// Extracts a substring of `length` characters starting at the `start` position (1-based).
// text_substring(str, start, length)
// [pg-compatible] substr(string, start, count)
static void text_substring3(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 3);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "start parameter should be integer", -1);
        return;
    }
    int start = sqlite3_value_int(argv[1]);

    if (sqlite3_value_type(argv[2]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "length parameter should be integer", -1);
        return;
    }
    int length = sqlite3_value_int(argv[2]);
    if (length < 0) {
        sqlite3_result_error(context, "length parameter should >= 0", -1);
        return;
    }

    // convert to 0-based index
    start -= 1;
    // postgres-compatible: treat negative start as 0, but shorten the length accordingly
    if (start < 0) {
        length += start;
        start = 0;
    }

    // zero-length substring
    if (length <= 0) {
        sqlite3_result_text(context, "", -1, SQLITE_TRANSIENT);
        return;
    }

    RuneString s_src = rstring_from_cstring(src);

    // postgres-compatible: the substring cannot be longer the the original string
    if ((size_t)length > s_src.length) {
        length = s_src.length;
    }

    RuneString s_res = rstring_substring(s_src, start, length);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_res);
}

// Extracts a substring starting at the `start` position (1-based).
// text_slice(str, start)
static void text_slice2(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "start parameter should be integer", -1);
        return;
    }
    int start = sqlite3_value_int(argv[1]);

    // convert to 0-based index
    start = start > 0 ? start - 1 : start;

    RuneString s_src = rstring_from_cstring(src);

    // python-compatible: treat negative index larger than the length of the string as zero
    // and return the original string
    if (start < -(int)s_src.length) {
        sqlite3_result_text(context, src, -1, SQLITE_TRANSIENT);
        rstring_free(s_src);
        return;
    }

    RuneString s_res = rstring_slice(s_src, start, s_src.length);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_res);
}

// Extracts a substring from `start` position inclusive to `end` position non-inclusive (1-based).
// text_slice(str, start, end)
static void text_slice3(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 3);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "start parameter should be integer", -1);
        return;
    }
    int start = sqlite3_value_int(argv[1]);
    // convert to 0-based index
    start = start > 0 ? start - 1 : start;

    if (sqlite3_value_type(argv[2]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "end parameter should be integer", -1);
        return;
    }
    int end = sqlite3_value_int(argv[2]);
    // convert to 0-based index
    end = end > 0 ? end - 1 : end;

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_res = rstring_slice(s_src, start, end);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_res);
}

// Extracts a substring of `length` characters from the beginning of the string.
// For `length < 0`, extracts all but the last `|length|` characters.
// text_left(str, length)
// [pg-compatible] left(string, n)
static void text_left(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "length parameter should be integer", -1);
        return;
    }
    int length = sqlite3_value_int(argv[1]);

    RuneString s_src = rstring_from_cstring(src);
    if (length < 0) {
        length = s_src.length + length;
        length = length >= 0 ? length : 0;
    }
    RuneString s_res = rstring_substring(s_src, 0, length);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_res);
}

// Extracts a substring of `length` characters from the end of the string.
// For `length < 0`, extracts all but the first `|length|` characters.
// text_right(str, length)
// [pg-compatible] right(string, n)
static void text_right(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "length parameter should be integer", -1);
        return;
    }
    int length = sqlite3_value_int(argv[1]);

    RuneString s_src = rstring_from_cstring(src);

    length = (length < 0) ? (int)s_src.length + length : length;
    int start = (int)s_src.length - length;
    start = start < 0 ? 0 : start;

    RuneString s_res = rstring_substring(s_src, start, length);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_res);
}

#pragma endregion

#pragma region Search and match

// Returns the first index of the substring in the original string.
// text_index(str, other)
// [pg-compatible] strpos(string, substring)
static void text_index(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* other = (char*)sqlite3_value_text(argv[1]);
    if (other == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_other = rstring_from_cstring(other);
    int idx = rstring_index(s_src, s_other);
    sqlite3_result_int64(context, idx + 1);
    rstring_free(s_src);
    rstring_free(s_other);
}

// Returns the last index of the substring in the original string.
// text_last_index(str, other)
static void text_last_index(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* other = (char*)sqlite3_value_text(argv[1]);
    if (other == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_other = rstring_from_cstring(other);
    int idx = rstring_last_index(s_src, s_other);
    sqlite3_result_int64(context, idx + 1);
    rstring_free(s_src);
    rstring_free(s_other);
}

// Checks if the string contains the substring_
// text_contains(str, other)
static void text_contains(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* other = (char*)sqlite3_value_text(argv[1]);
    if (other == NULL) {
        sqlite3_result_null(context);
        return;
    }

    ByteString s_src = bstring_from_cstring(src, sqlite3_value_bytes(argv[0]));
    ByteString s_other = bstring_from_cstring(other, sqlite3_value_bytes(argv[1]));
    bool found = bstring_contains(s_src, s_other);
    sqlite3_result_int(context, found);
    bstring_free(s_src);
    bstring_free(s_other);
}

// Checks if the string starts with the substring_
// text_has_prefix(str, other)
// [pg-compatible] starts_with(string, prefix)
static void text_has_prefix(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* other = (char*)sqlite3_value_text(argv[1]);
    if (other == NULL) {
        sqlite3_result_null(context);
        return;
    }

    ByteString s_src = bstring_from_cstring(src, sqlite3_value_bytes(argv[0]));
    ByteString s_other = bstring_from_cstring(other, sqlite3_value_bytes(argv[1]));
    bool found = bstring_has_prefix(s_src, s_other);
    sqlite3_result_int(context, found);
    bstring_free(s_src);
    bstring_free(s_other);
}

// Checks if the string ends with the substring_
// text_has_suffix(str, other)
static void text_has_suffix(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* other = (char*)sqlite3_value_text(argv[1]);
    if (other == NULL) {
        sqlite3_result_null(context);
        return;
    }

    ByteString s_src = bstring_from_cstring(src, sqlite3_value_bytes(argv[0]));
    ByteString s_other = bstring_from_cstring(other, sqlite3_value_bytes(argv[1]));
    bool found = bstring_has_suffix(s_src, s_other);
    sqlite3_result_int(context, found);
    bstring_free(s_src);
    bstring_free(s_other);
}

// Counts how many times the substring is contained in the original string.
// text_count(str, other)
static void text_count(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* other = (char*)sqlite3_value_text(argv[1]);
    if (other == NULL) {
        sqlite3_result_null(context);
        return;
    }

    ByteString s_src = bstring_from_cstring(src, sqlite3_value_bytes(argv[0]));
    ByteString s_other = bstring_from_cstring(other, sqlite3_value_bytes(argv[1]));
    size_t count = bstring_count(s_src, s_other);
    sqlite3_result_int(context, count);
    bstring_free(s_src);
    bstring_free(s_other);
}

// Checks if the string matches the pattern using the SQL LIKE syntax.
// text_like(pattern, str)
// like(pattern, str)
// str LIKE pattern
static void text_like(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* pattern = (char*)sqlite3_value_text(argv[0]);
    if (pattern == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* str = (char*)sqlite3_value_text(argv[1]);
    if (str == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString s_pattern = rstring_from_cstring(pattern);
    RuneString s_str = rstring_from_cstring(str);
    bool match = rstring_like(s_pattern, s_str);
    sqlite3_result_int(context, match);
    rstring_free(s_pattern);
    rstring_free(s_str);
}

#pragma endregion

#pragma region Split and join

// Splits a string by a separator and returns the n-th part (counting from one).
// When n is negative, returns the |n|'th-from-last part.
// text_split(str, sep, n)
// [pg-compatible] split_part(string, delimiter, n)
static void text_split(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 3);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* sep = (const char*)sqlite3_value_text(argv[1]);
    if (sep == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[2]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "part parameter should be integer", -1);
        return;
    }
    int part = sqlite3_value_int(argv[2]);
    // pg-compatible
    if (part == 0) {
        sqlite3_result_error(context, "part parameter should not be 0", -1);
        return;
    }
    // convert to 0-based index
    part = part > 0 ? part - 1 : part;

    ByteString s_src = bstring_from_cstring(src, strlen(src));
    ByteString s_sep = bstring_from_cstring(sep, strlen(sep));

    // count from the last part backwards
    if (part < 0) {
        int n_parts = bstring_count(s_src, s_sep) + 1;
        part = n_parts + part;
    }

    ByteString s_part = bstring_split_part(s_src, s_sep, part);
    sqlite3_result_text(context, s_part.bytes, -1, SQLITE_TRANSIENT);
    bstring_free(s_src);
    bstring_free(s_sep);
    bstring_free(s_part);
}

// Joins strings using the separator and returns the resulting string. Ignores nulls.
// text_join(sep, str, ...)
// [pg-compatible] concat_ws(sep, val1[, val2 [, ...]])
static void text_join(sqlite3_context* context, int argc, sqlite3_value** argv) {
    if (argc < 2) {
        sqlite3_result_error(context, "expected at least 2 parameters", -1);
        return;
    }

    // separator
    const char* sep = (char*)sqlite3_value_text(argv[0]);
    if (sep == NULL) {
        sqlite3_result_null(context);
        return;
    }
    ByteString s_sep = bstring_from_cstring(sep, sqlite3_value_bytes(argv[0]));

    // parts
    size_t n_parts = argc - 1;
    ByteString* s_parts = malloc(n_parts * sizeof(ByteString));
    if (s_parts == NULL) {
        sqlite3_result_null(context);
        return;
    }
    for (size_t i = 1, part_idx = 0; i < (size_t)argc; i++) {
        if (sqlite3_value_type(argv[i]) == SQLITE_NULL) {
            // ignore nulls
            n_parts--;
            continue;
        }
        const char* part = (char*)sqlite3_value_text(argv[i]);
        int part_len = sqlite3_value_bytes(argv[i]);
        s_parts[part_idx] = bstring_from_cstring(part, part_len);
        part_idx++;
    }

    // join parts with separator
    ByteString s_res = bstring_join(s_parts, n_parts, s_sep);
    const char* res = bstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, SQLITE_TRANSIENT);
    bstring_free(s_sep);
    bstring_free(s_res);
    free(s_parts);
}

// Concatenates strings and returns the resulting string. Ignores nulls.
// text_concat(str, ...)
// [pg-compatible] concat(val1[, val2 [, ...]])
static void text_concat(sqlite3_context* context, int argc, sqlite3_value** argv) {
    if (argc < 1) {
        sqlite3_result_error(context, "expected at least 1 parameter", -1);
        return;
    }

    // parts
    size_t n_parts = argc;
    ByteString* s_parts = malloc(n_parts * sizeof(ByteString));
    if (s_parts == NULL) {
        sqlite3_result_null(context);
        return;
    }
    for (size_t i = 0, part_idx = 0; i < (size_t)argc; i++) {
        if (sqlite3_value_type(argv[i]) == SQLITE_NULL) {
            // ignore nulls
            n_parts--;
            continue;
        }
        const char* part = (char*)sqlite3_value_text(argv[i]);
        int part_len = sqlite3_value_bytes(argv[i]);
        s_parts[part_idx] = bstring_from_cstring(part, part_len);
        part_idx++;
    }

    // join parts
    ByteString s_res = bstring_concat(s_parts, n_parts);
    const char* res = bstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, SQLITE_TRANSIENT);
    bstring_free(s_res);
    free(s_parts);
}

// Concatenates the string to itself a given number of times and returns the resulting string.
// text_repeat(str, count)
// [pg-compatible] repeat(string, number)
static void text_repeat(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "count parameter should be integer", -1);
        return;
    }
    int count = sqlite3_value_int(argv[1]);
    // pg-compatible: treat negative count as zero
    count = count >= 0 ? count : 0;

    ByteString s_src = bstring_from_cstring(src, sqlite3_value_bytes(argv[0]));
    ByteString s_res = bstring_repeat(s_src, count);
    const char* res = bstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, SQLITE_TRANSIENT);
    bstring_free(s_src);
    bstring_free(s_res);
}

#pragma endregion

#pragma region Trim and pad

// Trims certain characters (spaces by default) from the beginning/end of the string.
// text_ltrim(str [,chars])
// text_rtrim(str [,chars])
// text_trim(str [,chars])
// [pg-compatible] ltrim(string [, characters])
// [pg-compatible] rtrim(string [, characters])
// [pg-compatible] btrim(string [, characters])
static void text_trim(sqlite3_context* context, int argc, sqlite3_value** argv) {
    if (argc != 1 && argc != 2) {
        sqlite3_result_error(context, "expected 1 or 2 parameters", -1);
        return;
    }

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* chars = argc == 2 ? (char*)sqlite3_value_text(argv[1]) : " ";
    if (chars == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString (*trim_func)(RuneString, RuneString) = (void*)sqlite3_user_data(context);

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_chars = rstring_from_cstring(chars);
    RuneString s_res = trim_func(s_src, s_chars);
    const char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_chars);
    rstring_free(s_res);
}

// Pads the string to the specified length by prepending/appending certain characters
// (spaces by default).
// text_lpad(str, length [,fill])
// text_rpad(str, length [,fill])
// [pg-compatible] lpad(string, length [, fill])
// [pg-compatible] rpad(string, length [, fill])
// (!) postgres does not support unicode strings in lpad/rpad, while this function does.
static void text_pad(sqlite3_context* context, int argc, sqlite3_value** argv) {
    if (argc != 2 && argc != 3) {
        sqlite3_result_error(context, "expected 2 or 3 parameters", -1);
        return;
    }

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[1]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "length parameter should be integer", -1);
        return;
    }
    int length = sqlite3_value_int(argv[1]);
    // postgres-compatible: treat negative length as zero
    length = length < 0 ? 0 : length;

    const char* fill = argc == 3 ? (char*)sqlite3_value_text(argv[2]) : " ";
    if (fill == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString (*pad_func)(RuneString, size_t, RuneString) = (void*)sqlite3_user_data(context);

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_fill = rstring_from_cstring(fill);
    RuneString s_res = pad_func(s_src, length, s_fill);
    const char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_fill);
    rstring_free(s_res);
}

#pragma endregion

#pragma region Change case

// Changes the case of the string.
// text_upper(str)
// text_lower(str)
// text_title(str)
// text_casefold(str)
static void text_change_case(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);

    const char* src = (const char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }
    size_t n = sqlite3_value_bytes(argv[0]);

    char* res = malloc(n + 1);
    if (res == NULL) {
        sqlite3_result_error_nomem(context);
        return;
    }
    memcpy(res, src, n);
    res[n] = '\0';

    bool (*fn)(char*, size_t) = sqlite3_user_data(context);
    fn(res, n);

    sqlite3_result_text(context, res, n, free);
}

#pragma endregion

#pragma region Other modifications

// Replaces all old substrings with new substrings in the original string.
// text_replace(str, old, new)
// [pg-compatible] replace(string, from, to)
static void text_replace_all(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 3);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* old = (char*)sqlite3_value_text(argv[1]);
    if (old == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* new = (char*)sqlite3_value_text(argv[2]);
    if (new == NULL) {
        sqlite3_result_null(context);
        return;
    }

    ByteString s_src = bstring_from_cstring(src, sqlite3_value_bytes(argv[0]));
    ByteString s_old = bstring_from_cstring(old, sqlite3_value_bytes(argv[1]));
    ByteString s_new = bstring_from_cstring(new, sqlite3_value_bytes(argv[2]));
    ByteString s_res = bstring_replace_all(s_src, s_old, s_new);
    const char* res = bstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, SQLITE_TRANSIENT);
    bstring_free(s_src);
    bstring_free(s_old);
    bstring_free(s_new);
    bstring_free(s_res);
}

// Replaces old substrings with new substrings in the original string,
// but not more than `count` times.
// text_replace(str, old, new, count)
static void text_replace(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 4);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* old = (char*)sqlite3_value_text(argv[1]);
    if (old == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* new = (char*)sqlite3_value_text(argv[2]);
    if (new == NULL) {
        sqlite3_result_null(context);
        return;
    }

    if (sqlite3_value_type(argv[3]) != SQLITE_INTEGER) {
        sqlite3_result_error(context, "count parameter should be integer", -1);
        return;
    }
    int count = sqlite3_value_int(argv[3]);
    // treat negative count as zero
    count = count < 0 ? 0 : count;

    ByteString s_src = bstring_from_cstring(src, sqlite3_value_bytes(argv[0]));
    ByteString s_old = bstring_from_cstring(old, sqlite3_value_bytes(argv[1]));
    ByteString s_new = bstring_from_cstring(new, sqlite3_value_bytes(argv[2]));
    ByteString s_res = bstring_replace(s_src, s_old, s_new, count);
    const char* res = bstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, SQLITE_TRANSIENT);
    bstring_free(s_src);
    bstring_free(s_old);
    bstring_free(s_new);
    bstring_free(s_res);
}

// Replaces each string character that matches a character in the `from` set
// with the corresponding character in the `to` set. If `from` is longer than `to`,
// occurrences of the extra characters in `from` are deleted.
// text_translate(str, from, to)
// [pg-compatible] translate(string, from, to)
// (!) postgres does not support unicode strings in translate, while this function does.
static void text_translate(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 3);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* from = (char*)sqlite3_value_text(argv[1]);
    if (from == NULL) {
        sqlite3_result_null(context);
        return;
    }

    const char* to = (char*)sqlite3_value_text(argv[2]);
    if (to == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_from = rstring_from_cstring(from);
    RuneString s_to = rstring_from_cstring(to);
    RuneString s_res = rstring_translate(s_src, s_from, s_to);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_from);
    rstring_free(s_to);
    rstring_free(s_res);
}

// Reverses the order of the characters in the string.
// text_reverse(str)
// [pg-compatible] reverse(text)
// (!) postgres does not support unicode strings in reverse, while this function does.
static void text_reverse(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString s_src = rstring_from_cstring(src);
    RuneString s_res = rstring_reverse(s_src);
    char* res = rstring_to_cstring(s_res);
    sqlite3_result_text(context, res, -1, free);
    rstring_free(s_src);
    rstring_free(s_res);
}

#pragma endregion

#pragma region Properties

// Returns the number of characters in the string.
// text_length(str)
// [pg-compatible] length(text)
// [pg-compatible] char_length(text)
// [pg-compatible] character_length(text)
static void text_length(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    RuneString s_src = rstring_from_cstring(src);
    sqlite3_result_int64(context, s_src.length);
    rstring_free(s_src);
}

// Returns the number of bytes in the string.
// text_size(str)
// [pg-compatible] octet_length(text)
static void text_size(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    sqlite3_result_int64(context, sqlite3_value_bytes(argv[0]));
}

// Returns the number of bits in the string.
// text_bitsize(str)
// [pg-compatible] bit_length(text)
static void text_bit_size(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);

    const char* src = (char*)sqlite3_value_text(argv[0]);
    if (src == NULL) {
        sqlite3_result_null(context);
        return;
    }

    int size = sqlite3_value_bytes(argv[0]);
    sqlite3_result_int64(context, 8 * size);
}

#pragma endregion

#pragma region Collation

static int collate_nocase(void* unused, int n1, const void* s1, int n2, const void* s2) {
    (void)unused;
    return utf8_icmp((const char*)s1, (size_t)n1, (const char*)s2, (size_t)n2);
}

#pragma endregion

int text_init(sqlite3* db) {
    static const int flags = SQLITE_UTF8 | SQLITE_INNOCUOUS | SQLITE_DETERMINISTIC;

    // substrings
    sqlite3_create_function(db, "text_substring", 2, flags, 0, text_substring2, 0, 0);
    sqlite3_create_function(db, "text_substring", 3, flags, 0, text_substring3, 0, 0);
    sqlite3_create_function(db, "text_slice", 2, flags, 0, text_slice2, 0, 0);
    sqlite3_create_function(db, "text_slice", 3, flags, 0, text_slice3, 0, 0);
    sqlite3_create_function(db, "text_left", 2, flags, 0, text_left, 0, 0);
    sqlite3_create_function(db, "left", 2, flags, 0, text_left, 0, 0);
    sqlite3_create_function(db, "text_right", 2, flags, 0, text_right, 0, 0);
    sqlite3_create_function(db, "right", 2, flags, 0, text_right, 0, 0);

    // search and match
    sqlite3_create_function(db, "text_index", 2, flags, 0, text_index, 0, 0);
    sqlite3_create_function(db, "strpos", 2, flags, 0, text_index, 0, 0);
    sqlite3_create_function(db, "text_last_index", 2, flags, 0, text_last_index, 0, 0);
    sqlite3_create_function(db, "text_contains", 2, flags, 0, text_contains, 0, 0);
    sqlite3_create_function(db, "text_has_prefix", 2, flags, 0, text_has_prefix, 0, 0);
    sqlite3_create_function(db, "starts_with", 2, flags, 0, text_has_prefix, 0, 0);
    sqlite3_create_function(db, "text_has_suffix", 2, flags, 0, text_has_suffix, 0, 0);
    sqlite3_create_function(db, "text_count", 2, flags, 0, text_count, 0, 0);
    sqlite3_create_function(db, "text_like", 2, flags, 0, text_like, 0, 0);

    // split and join
    sqlite3_create_function(db, "text_split", 3, flags, 0, text_split, 0, 0);
    sqlite3_create_function(db, "split_part", 3, flags, 0, text_split, 0, 0);
    sqlite3_create_function(db, "text_join", -1, flags, 0, text_join, 0, 0);
    sqlite3_create_function(db, "concat_ws", -1, flags, 0, text_join, 0, 0);
    sqlite3_create_function(db, "text_concat", -1, flags, 0, text_concat, 0, 0);
    sqlite3_create_function(db, "concat", -1, flags, 0, text_concat, 0, 0);
    sqlite3_create_function(db, "text_repeat", 2, flags, 0, text_repeat, 0, 0);
    sqlite3_create_function(db, "repeat", 2, flags, 0, text_repeat, 0, 0);

    // trim and pad
    sqlite3_create_function(db, "text_ltrim", -1, flags, rstring_trim_left, text_trim, 0, 0);
    sqlite3_create_function(db, "ltrim", -1, flags, rstring_trim_left, text_trim, 0, 0);
    sqlite3_create_function(db, "text_rtrim", -1, flags, rstring_trim_right, text_trim, 0, 0);
    sqlite3_create_function(db, "rtrim", -1, flags, rstring_trim_right, text_trim, 0, 0);
    sqlite3_create_function(db, "text_trim", -1, flags, rstring_trim, text_trim, 0, 0);
    sqlite3_create_function(db, "btrim", -1, flags, rstring_trim, text_trim, 0, 0);
    sqlite3_create_function(db, "text_lpad", -1, flags, rstring_pad_left, text_pad, 0, 0);
    sqlite3_create_function(db, "lpad", -1, flags, rstring_pad_left, text_pad, 0, 0);
    sqlite3_create_function(db, "text_rpad", -1, flags, rstring_pad_right, text_pad, 0, 0);
    sqlite3_create_function(db, "rpad", -1, flags, rstring_pad_right, text_pad, 0, 0);

    // change case
    sqlite3_create_function(db, "text_upper", 1, flags, utf8_toupper, text_change_case, 0, 0);
    sqlite3_create_function(db, "text_lower", 1, flags, utf8_tolower, text_change_case, 0, 0);
    sqlite3_create_function(db, "text_title", 1, flags, utf8_totitle, text_change_case, 0, 0);
    sqlite3_create_function(db, "text_casefold", 1, flags, utf8_casefold, text_change_case, 0, 0);

    // other modifications
    sqlite3_create_function(db, "text_replace", 3, flags, 0, text_replace_all, 0, 0);
    sqlite3_create_function(db, "text_replace", 4, flags, 0, text_replace, 0, 0);
    sqlite3_create_function(db, "text_translate", 3, flags, 0, text_translate, 0, 0);
    sqlite3_create_function(db, "translate", 3, flags, 0, text_translate, 0, 0);
    sqlite3_create_function(db, "text_reverse", 1, flags, 0, text_reverse, 0, 0);
    sqlite3_create_function(db, "reverse", 1, flags, 0, text_reverse, 0, 0);

    // properties
    sqlite3_create_function(db, "text_length", 1, flags, 0, text_length, 0, 0);
    sqlite3_create_function(db, "char_length", 1, flags, 0, text_length, 0, 0);
    sqlite3_create_function(db, "character_length", 1, flags, 0, text_length, 0, 0);
    sqlite3_create_function(db, "text_size", 1, flags, 0, text_size, 0, 0);
    sqlite3_create_function(db, "octet_length", 1, flags, 0, text_size, 0, 0);
    sqlite3_create_function(db, "text_bitsize", 1, flags, 0, text_bit_size, 0, 0);
    sqlite3_create_function(db, "bit_length", 1, flags, 0, text_bit_size, 0, 0);

    // collation
    sqlite3_create_collation(db, "text_nocase", SQLITE_UTF8, NULL, collate_nocase);

    return SQLITE_OK;
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Rune (UTF-8) string data structure.

#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "text/rstring.h"
#include "text/runes.h"
#include "text/utf8/rune.h"

// utf8_length returns the number of utf-8 characters in a string.
static size_t utf8_length(const char* str) {
    size_t length = 0;

    while (*str != '\0') {
        if (0xf0 == (0xf8 & *str)) {
            // 4-byte utf8 code point (began with 0b11110xxx)
            str += 4;
        } else if (0xe0 == (0xf0 & *str)) {
            // 3-byte utf8 code point (began with 0b1110xxxx)
            str += 3;
        } else if (0xc0 == (0xe0 & *str)) {
            // 2-byte utf8 code point (began with 0b110xxxxx)
            str += 2;
        } else {  // if (0x00 == (0x80 & *s)) {
            // 1-byte ascii (began with 0b0xxxxxxx)
            str += 1;
        }

        // no matter the bytes we marched s forward by, it was
        // only 1 utf8 codepoint
        length++;
    }

    return length;
}

// rstring_new creates an empty string.
RuneString rstring_new(void) {
    RuneString str = {.runes = NULL, .length = 0, .size = 0, .owning = true};
    return str;
}

// rstring_from_runes creates a new string from an array of utf-8 characters.
// `owning` indicates whether the string owns the array and should free the memory when destroyed.
static RuneString rstring_from_runes(const int32_t* const runes, size_t length, bool owning) {
    RuneString str = {
        .runes = runes, .length = length, .size = length * sizeof(int32_t), .owning = owning};
    return str;
}

// rstring_from_cstring creates a new string from a zero-terminated C string.
RuneString rstring_from_cstring(const char* const utf8str) {
    size_t length = utf8_length(utf8str);
    int32_t* runes = length > 0 ? runes_from_cstring(utf8str, length) : NULL;
    return rstring_from_runes(runes, length, true);
}

// rstring_to_cstring converts the string to a zero-terminated C string.
char* rstring_to_cstring(RuneString str) {
    return runes_to_cstring(str.runes, str.length);
}

// rstring_free destroys the string, freeing resources if necessary.
void rstring_free(RuneString str) {
    if (str.owning && str.runes != NULL) {
        free((void*)str.runes);
    }
}

// rstring_at returns a character by its index in the string.
int32_t rstring_at(RuneString str, size_t idx) {
    if (str.length == 0) {
        return 0;
    }
    if (idx < 0 || idx >= str.length) {
        return 0;
    };
    return str.runes[idx];
}

// rstring_slice returns a slice of the string,
// from the `start` index (inclusive) to the `end` index (non-inclusive).
// Negative `start` and `end` values count from the end of the string.
RuneString rstring_slice(RuneString str, int start, int end) {
    if (str.length == 0) {
        return rstring_new();
    }

    // adjusted start index
    start = start < 0 ? (int)str.length + start : start;
    // python-compatible: treat negative start index larger than the length of the string as zero
    start = start < 0 ? 0 : start;
    // adjusted start index should be less the the length of the string
    if (start >= (int)str.length) {
        return rstring_new();
    }

    // adjusted end index
    end = end < 0 ? (int)str.length + end : end;
    // python-compatible: treat end index larger than the length of the string
    // as equal to the length
    end = end > (int)str.length ? (int)str.length : end;
    // adjusted end index should be >= 0
    if (end < 0) {
        return rstring_new();
    }

    // adjusted start index should be less than adjusted end index
    if (start >= end) {
        return rstring_new();
    }

    int32_t* at = (int32_t*)str.runes + start;
    size_t length = end - start;
    RuneString slice = rstring_from_runes(at, length, false);
    return slice;
}

// rstring_substring returns a substring of `length` characters,
// starting from the `start` index.
RuneString rstring_substring(RuneString str, size_t start, size_t length) {
    if (length > str.length - start) {
        length = str.length - start;
    }
    return rstring_slice(str, start, start + length);
}

// rstring_contains_after checks if the other string is a substring of the original string,
// starting at the `start` index.
static bool rstring_contains_after(RuneString str, RuneString other, size_t start) {
    if (start + other.length > str.length) {
        return false;
    }
    for (size_t idx = 0; idx < other.length; idx++) {
        if (str.runes[start + idx] != other.runes[idx]) {
            return false;
        }
    }
    return true;
}

// rstring_index_char returns the first index of the character in the string
// after the `start` index, inclusive.
static int rstring_index_char(RuneString str, int32_t rune, size_t start) {
    for (size_t idx = start; idx < str.length; idx++) {
        if (str.runes[idx] == rune) {
            return idx;
        }
    }
    return -1;
}

// rstring_index_char returns the last index of the character in the string
// before the `end` index, inclusive.
static int rstring_last_index_char(RuneString str, int32_t rune, size_t end) {
    if (end >= str.length) {
        return -1;
    }
    for (int idx = end; idx >= 0; idx--) {
        if (str.runes[idx] == rune) {
            return idx;
        }
    }
    return -1;
}

// rstring_index_after returns the index of the substring in the original string
// after the `start` index, inclusive.
static int rstring_index_after(RuneString str, RuneString other, size_t start) {
    if (other.length == 0) {
        return start;
    }
    if (str.length == 0 || other.length > str.length) {
        return -1;
    }

    size_t cur_idx = start;
    while (cur_idx < str.length) {
        int match_idx = rstring_index_char(str, other.runes[0], cur_idx);
        if (match_idx == -1) {
            return match_idx;
        }
        if (rstring_contains_after(str, other, match_idx)) {
            return match_idx;
        }
        cur_idx = match_idx + 1;
    }
    return -1;
}

// rstring_index returns the first index of the substring in the original string.
int rstring_index(RuneString str, RuneString other) {
    return rstring_index_after(str, other, 0);
}

// rstring_last_index returns the last index of the substring in the original string.
int rstring_last_index(RuneString str, RuneString other) {
    if (other.length == 0) {
        return str.length - 1;
    }
    if (str.length == 0 || other.length > str.length) {
        return -1;
    }

    int cur_idx = str.length - 1;
    while (cur_idx >= 0) {
        int match_idx = rstring_last_index_char(str, other.runes[0], cur_idx);
        if (match_idx == -1) {
            return match_idx;
        }
        if (rstring_contains_after(str, other, match_idx)) {
            return match_idx;
        }
        cur_idx = match_idx - 1;
    }

    return -1;
}

// rstring_like returns true if the string matches a LIKE pattern.
bool rstring_like(RuneString pattern, RuneString str) {
    size_t pidx = 0, sidx = 0, star_idx = SIZE_MAX, match = 0;

    while (sidx < str.length) {
        int32_t prune = (pidx < pattern.length) ? pattern.runes[pidx] : 0;
        int32_t srune = str.runes[sidx];

        if (prune == '%') {
            star_idx = ++pidx;
            match = ++sidx;
            if (pidx == pattern.length) {
                return true;
            }
        } else if (prune == '_' || rune_casefold(prune) == rune_casefold(srune)) {
            pidx++;
            sidx++;
        } else if (star_idx != SIZE_MAX) {
            pidx = star_idx;
            sidx = match++;
        } else {
            return false;
        }
    }

    while (pidx < pattern.length && pattern.runes[pidx] == '%') {
        pidx++;
    }
    return pidx == pattern.length;
}

// rstring_translate replaces each string character that matches a character in the `from` set with
// the corresponding character in the `to` set. If `from` is longer than `to`, occurrences of the
// extra characters in `from` are deleted.
RuneString rstring_translate(RuneString str, RuneString from, RuneString to) {
    if (str.length == 0) {
        return rstring_new();
    }

    // empty mapping, return the original string
    if (from.length == 0) {
        return rstring_from_runes(str.runes, str.length, false);
    }

    // resulting string can be no longer than the original one
    int32_t* runes = calloc(str.length, sizeof(int32_t));
    if (runes == NULL) {
        return rstring_new();
    }

    // but it may be shorter, so we should track its length separately
    size_t length = 0;
    // perform the translation
    for (size_t idx = 0; idx < str.length; idx++) {
        size_t k = 0;
        // map idx-th character in str `from` -> `to`
        for (; k < from.length && k < to.length; k++) {
            if (str.runes[idx] == from.runes[k]) {
                runes[length] = to.runes[k];
                length++;
                break;
            }
        }
        // if `from` is longer than `to`, ingore idx-th character found in `from`
        bool ignore = false;
        for (; k < from.length; k++) {
            if (str.runes[idx] == from.runes[k]) {
                ignore = true;
                break;
            }
        }
        // else copy idx-th character as is
        if (!ignore) {
            runes[length] = str.runes[idx];
            length++;
        }
    }

    return rstring_from_runes(runes, length, true);
}

// rstring_reverse returns the reversed string.
RuneString rstring_reverse(RuneString str) {
    int32_t* runes = (int32_t*)str.runes;
    for (size_t i = 0; i < str.length / 2; i++) {
        int32_t r = runes[i];
        runes[i] = runes[str.length - 1 - i];
        runes[str.length - 1 - i] = r;
    }
    RuneString res = rstring_from_runes(runes, str.length, false);
    return res;
}

// rstring_trim_left trims certain characters from the beginning of the string.
RuneString rstring_trim_left(RuneString str, RuneString chars) {
    if (str.length == 0) {
        return rstring_new();
    }
    size_t idx = 0;
    for (; idx < str.length; idx++) {
        if (rstring_index_char(chars, str.runes[idx], 0) == -1) {
            break;
        }
    }
    return rstring_slice(str, idx, str.length);
}

// rstring_trim_right trims certain characters from the end of the string.
RuneString rstring_trim_right(RuneString str, RuneString chars) {
    if (str.length == 0) {
        return rstring_new();
    }
    int idx = str.length - 1;
    for (; idx >= 0; idx--) {
        if (rstring_index_char(chars, str.runes[idx], 0) == -1) {
            break;
        }
    }
    return rstring_slice(str, 0, idx + 1);
}

// rstring_trim trims certain characters from the beginning and end of the string.
RuneString rstring_trim(RuneString str, RuneString chars) {
    if (str.length == 0) {
        return rstring_new();
    }
    size_t left = 0;
    for (; left < str.length; left++) {
        if (rstring_index_char(chars, str.runes[left], 0) == -1) {
            break;
        }
    }
    int right = str.length - 1;
    for (; right >= 0; right--) {
        if (rstring_index_char(chars, str.runes[right], 0) == -1) {
            break;
        }
    }
    return rstring_slice(str, left, right + 1);
}

// rstring_pad_left pads the string to the specified length by prepending `fill` characters.
// If the string is already longer than the specified length, it is truncated on the right.
RuneString rstring_pad_left(RuneString str, size_t length, RuneString fill) {
    if (str.length >= length) {
        // If the string is already longer than length, return a truncated version of the string
        return rstring_substring(str, 0, length);
    }

    if (fill.length == 0) {
        // If the fill string is empty, return the original string
        return rstring_from_runes(str.runes, str.length, false);
    }

    // Calculate the number of characters to pad
    size_t pad_langth = length - str.length;

    // Allocate memory for the padded string
    size_t new_size = (str.length + pad_langth) * sizeof(int32_t);
    int32_t* new_runes = malloc(new_size);
    if (new_runes == NULL) {
        return rstring_new();
    }

    // Copy the fill characters to the beginning of the new string
    for (size_t i = 0; i < pad_langth; i++) {
        new_runes[i] = fill.runes[i % fill.length];
    }

    // Copy the original string to the end of the new string
    memcpy(&new_runes[pad_langth], str.runes, str.size);

    // Return the new string
    RuneString new_str = rstring_from_runes(new_runes, length, true);
    return new_str;
}

// rstring_pad_right pads the string to the specified length by appending `fill` characters.
// If the string is already longer than the specified length, it is truncated on the right.
RuneString rstring_pad_right(RuneString str, size_t length, RuneString fill) {
    if (str.length >= length) {
        // If the string is already longer than length, return a truncated version of the string
        return rstring_substring(str, 0, length);
    }

    if (fill.length == 0) {
        // If the fill string is empty, return the original string
        return rstring_from_runes(str.runes, str.length, false);
    }

    // Calculate the number of characters to pad
    size_t pad_length = length - str.length;

    // Allocate memory for the padded string
    size_t new_size = (str.length + pad_length) * sizeof(int32_t);
    int32_t* new_runes = malloc(new_size);
    if (new_runes == NULL) {
        return rstring_new();
    }

    // Copy the original string to the beginning of the new string
    memcpy(new_runes, str.runes, str.size);

    // Copy the fill characters to the end of the new string
    for (size_t i = str.length; i < length; i++) {
        new_runes[i] = fill.runes[(i - str.length) % fill.length];
    }

    // Return the new string
    RuneString new_str = rstring_from_runes(new_runes, length, true);
    return new_str;
}

// rstring_print prints the string to stdout.
void rstring_print(RuneString str) {
    if (str.length == 0) {
        printf("'' (len=0)\n");
        return;
    }
    printf("'");
    for (size_t i = 0; i < str.length; i++) {
        printf("%08x ", str.runes[i]);
    }
    printf("' (len=%zu)", str.length);
    printf("\n");
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// UTF-8 characters (runes) <-> C string conversions.

#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#include "text/runes.h"
#include "text/utf8/utf8.h"

// runes_from_cstring creates an array of runes from a C string.
int32_t* runes_from_cstring(const char* const str, size_t length) {
    assert(length > 0);
    int32_t* runes = calloc(length, sizeof(int32_t));
    if (runes == NULL) {
        return NULL;
    }

    utf8_decode_t d = {.state = 0};
    const char* s = str;
    size_t idx = 0;
    while (idx < length && *s != 0) {
        do {
            utf8_decode(&d, (uint8_t)*s++);
        } while (d.state);
        runes[idx] = d.codep;
        idx += 1;
    }

    return runes;
}

// runes_to_cstring creates a C string from an array of runes.
char* runes_to_cstring(const int32_t* runes, size_t length) {
    char* str;
    if (length == 0) {
        str = calloc(1, sizeof(char));
        return str;
    }

    size_t maxlen = length * sizeof(int32_t) + 1;
    str = malloc(maxlen);
    if (str == NULL) {
        return NULL;
    }

    char* at = str;
    for (size_t i = 0; i < length; i++) {
        at += utf8_encode(at, runes[i]);
    }
    *at = '\0';
    at += 1;

    if ((size_t)(at - str) < maxlen) {
        // shrink to real size
        size_t size = at - str;
        str = realloc(str, size);
    }
    return str;
}
