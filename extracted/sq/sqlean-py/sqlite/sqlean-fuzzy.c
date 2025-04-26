// Copyright (c) 2021 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Caverphone phonetic coding algorithm.
// https://en.wikipedia.org/wiki/Caverphone

#include <assert.h>
#include <stdlib.h>
#include <string.h>

// remove_non_letters deletes everything from the source string,
// except lowercased letters a-z
static char* remove_non_letters(const char* src) {
    size_t src_len = strlen(src);
    char* res = malloc((src_len + 1) * sizeof(char));
    const char* src_it;
    char* res_it = res;
    for (size_t idx = 0; idx < src_len; idx++) {
        src_it = src + idx;
        if (*src_it < 97 || *src_it > 122) {
            continue;
        }
        *res_it = *src_it;
        res_it++;
    }
    *res_it = '\0';
    return res;
}

// replace_start replaces the `old` substring with the `new` one
// if it matches at the beginning of the `src` string
static char* replace_start(const char* src, const char* old, const char* new) {
    size_t src_len = strlen(src);
    size_t old_len = strlen(old);
    size_t new_len = strlen(new);
    assert(new_len <= old_len);

    char* res = malloc((src_len + 1) * sizeof(char));

    if (src_len < old_len) {
        // source string is shorter than the substring to replace,
        // so there is definitely no match
        strcpy(res, src);
        return res;
    }

    if (strncmp(src, old, old_len) == 0) {
        strncpy(res, new, new_len);
        strncpy(res + new_len, src + old_len, src_len - old_len);
        *(res + src_len - old_len + new_len) = '\0';
    } else {
        strcpy(res, src);
    }
    return res;
}

// replace_end replaces the `old` substring with the `new` one
// if it matches at the end of the `src` string
static char* replace_end(const char* src, const char* old, const char* new) {
    size_t src_len = strlen(src);
    size_t old_len = strlen(old);
    size_t new_len = strlen(new);
    assert(new_len <= old_len);

    char* res = malloc((src_len + 1) * sizeof(char));

    if (src_len < old_len) {
        // source string is shorter than the substring to replace,
        // so there is definitely no match
        strcpy(res, src);
        return res;
    }

    strncpy(res, src, src_len - old_len);
    if (strncmp(src + src_len - old_len, old, old_len) == 0) {
        strncpy(res + src_len - old_len, new, new_len);
        *(res + src_len - old_len + new_len) = '\0';
    } else {
        strncpy(res + src_len - old_len, src + src_len - old_len, old_len);
        *(res + src_len) = '\0';
    }
    return res;
}

// replace replaces all `old` substrings with `new` ones
// in the the `src` string
static char* replace(const char* src, const char* old, const char* new) {
    size_t src_len = strlen(src);
    size_t old_len = strlen(old);
    size_t new_len = strlen(new);
    assert(new_len <= old_len);

    char* res = malloc((src_len + 1) * sizeof(char));

    if (src_len < old_len) {
        // source string is shorter than the substring to replace,
        // so there is definitely no match
        strcpy(res, src);
        return res;
    }

    const char* src_it;
    char* res_it = res;
    for (size_t idx = 0; idx < src_len;) {
        src_it = src + idx;
        if (strncmp(src_it, old, old_len) == 0) {
            strncpy(res_it, new, new_len);
            res_it += new_len;
            idx += old_len;
        } else {
            *res_it = *src_it;
            res_it++;
            idx++;
        }
    }
    *res_it = '\0';
    return res;
}

// replace_seq replaces all sequences of the `old` character
// with the `new` substring in the the `src` string
static char* replace_seq(const char* src, const char old, const char* new) {
    size_t src_len = strlen(src);
    size_t new_len = strlen(new);
    char* res = malloc((src_len + 1) * sizeof(char));
    const char* src_it;
    char* res_it = res;
    size_t match_len = 0;
    for (size_t idx = 0; idx < src_len;) {
        src_it = src + idx;
        if (*src_it == old) {
            match_len++;
            idx++;
        } else {
            if (match_len > 0) {
                strncpy(res_it, new, new_len);
                res_it += new_len;
                match_len = 0;
            }
            *res_it = *src_it;
            res_it++;
            idx++;
        }
    }
    if (match_len > 0) {
        strncpy(res_it, new, new_len);
        res_it += new_len;
    }
    *res_it = '\0';
    return res;
}

// pad pads `src` string with trailing 1s
// up to the length of 10 characters
static char* pad(const char* src) {
    size_t src_len = strlen(src);
    size_t max_len = 10;

    char* res = malloc((max_len + 1) * sizeof(char));
    strncpy(res, src, max_len);
    if (src_len < max_len) {
        for (size_t idx = src_len; idx < max_len; idx++) {
            *(res + idx) = '1';
        }
    }
    *(res + max_len) = '\0';
    return res;
}

// step frees the source string and returns the result one
static char* step(char* res, char* src) {
    free(src);
    return res;
}

// caverphone implements the Caverphone phonetic hashing algorithm
// as described in https://caversham.otago.ac.nz/files/working/ctp150804.pdf
char* caverphone(const char* src) {
    assert(src != NULL);

    char* res = malloc((strlen(src) + 1) * sizeof(char));

    if (src == 0 || *src == '\0') {
        res[0] = '\0';
        return res;
    }

    strcpy(res, src);

    // Remove anything not in the standard alphabet
    res = step(remove_non_letters((const char*)res), res);

    // Remove final e
    res = step(replace_end((const char*)res, "e", ""), res);

    // If the name starts with *gh make it *2f
    res = step(replace_start((const char*)res, "cough", "cou2f"), res);
    res = step(replace_start((const char*)res, "rough", "rou2f"), res);
    res = step(replace_start((const char*)res, "tough", "tou2f"), res);
    res = step(replace_start((const char*)res, "enough", "enou2f"), res);
    res = step(replace_start((const char*)res, "trough", "trou2f"), res);

    // If the name starts with gn make it 2n
    res = step(replace_start((const char*)res, "gn", "2n"), res);
    // If the name ends with mb make it m2
    res = step(replace_end((const char*)res, "mb", "m2"), res);
    // replace cq with 2q
    res = step(replace((const char*)res, "cq", "2q"), res);

    // replace c[iey] with s[iey]
    res = step(replace((const char*)res, "ci", "si"), res);
    res = step(replace((const char*)res, "ce", "se"), res);
    res = step(replace((const char*)res, "cy", "sy"), res);

    // replace tch with 2ch
    res = step(replace((const char*)res, "tch", "2ch"), res);

    // replace [cqx] with k
    res = step(replace((const char*)res, "c", "k"), res);
    res = step(replace((const char*)res, "q", "k"), res);
    res = step(replace((const char*)res, "x", "k"), res);

    // replace v with f
    res = step(replace((const char*)res, "v", "f"), res);
    // replace dg with 2g
    res = step(replace((const char*)res, "dg", "2g"), res);

    // replace ti[oa] with si[oa]
    res = step(replace((const char*)res, "tio", "sio"), res);
    res = step(replace((const char*)res, "tia", "sia"), res);

    // replace d with t
    res = step(replace((const char*)res, "d", "t"), res);
    // replace ph with fh
    res = step(replace((const char*)res, "ph", "fh"), res);
    // replace b with p
    res = step(replace((const char*)res, "b", "p"), res);
    // replace sh with s2
    res = step(replace((const char*)res, "sh", "s2"), res);
    // replace z with s
    res = step(replace((const char*)res, "z", "s"), res);

    // replace an initial vowel [aeiou] with an A
    res = step(replace_start((const char*)res, "a", "A"), res);
    res = step(replace_start((const char*)res, "e", "A"), res);
    res = step(replace_start((const char*)res, "i", "A"), res);
    res = step(replace_start((const char*)res, "o", "A"), res);
    res = step(replace_start((const char*)res, "u", "A"), res);

    // replace all other vowels with a 3
    res = step(replace((const char*)res, "a", "3"), res);
    res = step(replace((const char*)res, "e", "3"), res);
    res = step(replace((const char*)res, "i", "3"), res);
    res = step(replace((const char*)res, "o", "3"), res);
    res = step(replace((const char*)res, "u", "3"), res);

    // replace j with y
    res = step(replace((const char*)res, "j", "y"), res);

    // replace an initial y3 with Y3
    res = step(replace_start((const char*)res, "y3", "Y3"), res);
    // replace an initial y with A
    res = step(replace_start((const char*)res, "y", "A"), res);
    // replace y with 3
    res = step(replace((const char*)res, "y", "3"), res);

    // replace 3gh3 with 3kh3
    res = step(replace((const char*)res, "3gh3", "3kh3"), res);
    // replace gh with 22
    res = step(replace((const char*)res, "gh", "22"), res);
    // replace g with k
    res = step(replace((const char*)res, "g", "k"), res);

    // replace sequence of the letter [stpkfmn] with an uppercased letter
    res = step(replace_seq((const char*)res, 's', "S"), res);
    res = step(replace_seq((const char*)res, 't', "T"), res);
    res = step(replace_seq((const char*)res, 'p', "P"), res);
    res = step(replace_seq((const char*)res, 'k', "K"), res);
    res = step(replace_seq((const char*)res, 'f', "F"), res);
    res = step(replace_seq((const char*)res, 'm', "M"), res);
    res = step(replace_seq((const char*)res, 'n', "N"), res);

    // replace w3 with W3
    res = step(replace((const char*)res, "w3", "W3"), res);
    // replace wh3 with Wh3
    res = step(replace((const char*)res, "wh3", "Wh3"), res);
    // replace the final w with 3
    res = step(replace_end((const char*)res, "w", "3"), res);
    // replace w with 2
    res = step(replace((const char*)res, "w", "2"), res);

    // replace an initial h with an A
    res = step(replace_start((const char*)res, "h", "A"), res);
    // replace all other occurrences of h with a 2
    res = step(replace((const char*)res, "h", "2"), res);

    // replace r3 with R3
    res = step(replace((const char*)res, "r3", "R3"), res);
    // replace the final r with 3
    res = step(replace_end((const char*)res, "r", "3"), res);
    // replace r with 2
    res = step(replace((const char*)res, "r", "2"), res);

    // replace l3 with L3
    res = step(replace((const char*)res, "l3", "L3"), res);
    // replace the final l with 3
    res = step(replace_end((const char*)res, "l", "3"), res);
    // replace l with 2
    res = step(replace((const char*)res, "l", "2"), res);

    // remove all 2s
    res = step(replace((const char*)res, "2", ""), res);
    // replace the final 3 with A
    res = step(replace_end((const char*)res, "3", "A"), res);
    // remove all 3s
    res = step(replace((const char*)res, "3", ""), res);

    // put ten 1s on the end
    // take the first ten characters as the code
    res = step(pad((const char*)res), res);

    return res;
}
// Originally from the spellfix SQLite exension, Public Domain
// https://www.sqlite.org/src/file/ext/misc/spellfix.c
// Modified by Anton Zhiyanov, https://github.com/nalgeon/sqlean/, MIT License

#include "fuzzy/common.h"

/*
** The following table gives the character class for non-initial ASCII
** characters.
*/
const unsigned char midClass[] = {
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_SPACE,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_SPACE,  /*   */ CCLASS_SPACE, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_SPACE,
    /* ! */ CCLASS_OTHER,  /* " */ CCLASS_OTHER, /* # */ CCLASS_OTHER,
    /* $ */ CCLASS_OTHER,  /* % */ CCLASS_OTHER, /* & */ CCLASS_OTHER,
    /* ' */ CCLASS_SILENT, /* ( */ CCLASS_OTHER, /* ) */ CCLASS_OTHER,
    /* * */ CCLASS_OTHER,  /* + */ CCLASS_OTHER, /* , */ CCLASS_OTHER,
    /* - */ CCLASS_OTHER,  /* . */ CCLASS_OTHER, /* / */ CCLASS_OTHER,
    /* 0 */ CCLASS_DIGIT,  /* 1 */ CCLASS_DIGIT, /* 2 */ CCLASS_DIGIT,
    /* 3 */ CCLASS_DIGIT,  /* 4 */ CCLASS_DIGIT, /* 5 */ CCLASS_DIGIT,
    /* 6 */ CCLASS_DIGIT,  /* 7 */ CCLASS_DIGIT, /* 8 */ CCLASS_DIGIT,
    /* 9 */ CCLASS_DIGIT,  /* : */ CCLASS_OTHER, /* ; */ CCLASS_OTHER,
    /* < */ CCLASS_OTHER,  /* = */ CCLASS_OTHER, /* > */ CCLASS_OTHER,
    /* ? */ CCLASS_OTHER,  /* @ */ CCLASS_OTHER, /* A */ CCLASS_VOWEL,
    /* B */ CCLASS_B,      /* C */ CCLASS_C,     /* D */ CCLASS_D,
    /* E */ CCLASS_VOWEL,  /* F */ CCLASS_B,     /* G */ CCLASS_C,
    /* H */ CCLASS_SILENT, /* I */ CCLASS_VOWEL, /* J */ CCLASS_C,
    /* K */ CCLASS_C,      /* L */ CCLASS_L,     /* M */ CCLASS_M,
    /* N */ CCLASS_M,      /* O */ CCLASS_VOWEL, /* P */ CCLASS_B,
    /* Q */ CCLASS_C,      /* R */ CCLASS_R,     /* S */ CCLASS_C,
    /* T */ CCLASS_D,      /* U */ CCLASS_VOWEL, /* V */ CCLASS_B,
    /* W */ CCLASS_B,      /* X */ CCLASS_C,     /* Y */ CCLASS_VOWEL,
    /* Z */ CCLASS_C,      /* [ */ CCLASS_OTHER, /* \ */ CCLASS_OTHER,
    /* ] */ CCLASS_OTHER,  /* ^ */ CCLASS_OTHER, /* _ */ CCLASS_OTHER,
    /* ` */ CCLASS_OTHER,  /* a */ CCLASS_VOWEL, /* b */ CCLASS_B,
    /* c */ CCLASS_C,      /* d */ CCLASS_D,     /* e */ CCLASS_VOWEL,
    /* f */ CCLASS_B,      /* g */ CCLASS_C,     /* h */ CCLASS_SILENT,
    /* i */ CCLASS_VOWEL,  /* j */ CCLASS_C,     /* k */ CCLASS_C,
    /* l */ CCLASS_L,      /* m */ CCLASS_M,     /* n */ CCLASS_M,
    /* o */ CCLASS_VOWEL,  /* p */ CCLASS_B,     /* q */ CCLASS_C,
    /* r */ CCLASS_R,      /* s */ CCLASS_C,     /* t */ CCLASS_D,
    /* u */ CCLASS_VOWEL,  /* v */ CCLASS_B,     /* w */ CCLASS_B,
    /* x */ CCLASS_C,      /* y */ CCLASS_VOWEL, /* z */ CCLASS_C,
    /* { */ CCLASS_OTHER,  /* | */ CCLASS_OTHER, /* } */ CCLASS_OTHER,
    /* ~ */ CCLASS_OTHER,  /*   */ CCLASS_OTHER,
};
/*
** This tables gives the character class for ASCII characters that form the
** initial character of a word.  The only difference from midClass is with
** the letters H, W, and Y.
*/
const unsigned char initClass[] = {
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_SPACE,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_SPACE,  /*   */ CCLASS_SPACE, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_OTHER,
    /*   */ CCLASS_OTHER,  /*   */ CCLASS_OTHER, /*   */ CCLASS_SPACE,
    /* ! */ CCLASS_OTHER,  /* " */ CCLASS_OTHER, /* # */ CCLASS_OTHER,
    /* $ */ CCLASS_OTHER,  /* % */ CCLASS_OTHER, /* & */ CCLASS_OTHER,
    /* ' */ CCLASS_OTHER,  /* ( */ CCLASS_OTHER, /* ) */ CCLASS_OTHER,
    /* * */ CCLASS_OTHER,  /* + */ CCLASS_OTHER, /* , */ CCLASS_OTHER,
    /* - */ CCLASS_OTHER,  /* . */ CCLASS_OTHER, /* / */ CCLASS_OTHER,
    /* 0 */ CCLASS_DIGIT,  /* 1 */ CCLASS_DIGIT, /* 2 */ CCLASS_DIGIT,
    /* 3 */ CCLASS_DIGIT,  /* 4 */ CCLASS_DIGIT, /* 5 */ CCLASS_DIGIT,
    /* 6 */ CCLASS_DIGIT,  /* 7 */ CCLASS_DIGIT, /* 8 */ CCLASS_DIGIT,
    /* 9 */ CCLASS_DIGIT,  /* : */ CCLASS_OTHER, /* ; */ CCLASS_OTHER,
    /* < */ CCLASS_OTHER,  /* = */ CCLASS_OTHER, /* > */ CCLASS_OTHER,
    /* ? */ CCLASS_OTHER,  /* @ */ CCLASS_OTHER, /* A */ CCLASS_VOWEL,
    /* B */ CCLASS_B,      /* C */ CCLASS_C,     /* D */ CCLASS_D,
    /* E */ CCLASS_VOWEL,  /* F */ CCLASS_B,     /* G */ CCLASS_C,
    /* H */ CCLASS_SILENT, /* I */ CCLASS_VOWEL, /* J */ CCLASS_C,
    /* K */ CCLASS_C,      /* L */ CCLASS_L,     /* M */ CCLASS_M,
    /* N */ CCLASS_M,      /* O */ CCLASS_VOWEL, /* P */ CCLASS_B,
    /* Q */ CCLASS_C,      /* R */ CCLASS_R,     /* S */ CCLASS_C,
    /* T */ CCLASS_D,      /* U */ CCLASS_VOWEL, /* V */ CCLASS_B,
    /* W */ CCLASS_B,      /* X */ CCLASS_C,     /* Y */ CCLASS_Y,
    /* Z */ CCLASS_C,      /* [ */ CCLASS_OTHER, /* \ */ CCLASS_OTHER,
    /* ] */ CCLASS_OTHER,  /* ^ */ CCLASS_OTHER, /* _ */ CCLASS_OTHER,
    /* ` */ CCLASS_OTHER,  /* a */ CCLASS_VOWEL, /* b */ CCLASS_B,
    /* c */ CCLASS_C,      /* d */ CCLASS_D,     /* e */ CCLASS_VOWEL,
    /* f */ CCLASS_B,      /* g */ CCLASS_C,     /* h */ CCLASS_SILENT,
    /* i */ CCLASS_VOWEL,  /* j */ CCLASS_C,     /* k */ CCLASS_C,
    /* l */ CCLASS_L,      /* m */ CCLASS_M,     /* n */ CCLASS_M,
    /* o */ CCLASS_VOWEL,  /* p */ CCLASS_B,     /* q */ CCLASS_C,
    /* r */ CCLASS_R,      /* s */ CCLASS_C,     /* t */ CCLASS_D,
    /* u */ CCLASS_VOWEL,  /* v */ CCLASS_B,     /* w */ CCLASS_B,
    /* x */ CCLASS_C,      /* y */ CCLASS_Y,     /* z */ CCLASS_C,
    /* { */ CCLASS_OTHER,  /* | */ CCLASS_OTHER, /* } */ CCLASS_OTHER,
    /* ~ */ CCLASS_OTHER,  /*   */ CCLASS_OTHER,
};

/*
** Mapping from the character class number (0-13) to a symbol for each
** character class.  Note that initClass[] can be used to map the class
** symbol back into the class number.
*/
const unsigned char className[] = ".ABCDHLRMY9 ?";
// Copyright (c) 2014 Ross Bayer, MIT License
// https://github.com/Rostepher/libstrcmp

#include <assert.h>
#include <stdlib.h>
#include <string.h>

#include "fuzzy/common.h"

/// Calculates and returns the Damerau-Levenshtein distance of two non NULL
/// strings. More information about the algorithm can be found here:
///     https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance
///
/// @param str1 first non NULL string
/// @param str2 second non NULL string
///
/// @returns Damerau-Levenshtein distance of str1 and str2
unsigned damerau_levenshtein(const char* str1, const char* str2) {
    // strings cannot be NULL
    assert(str1 != NULL);
    assert(str2 != NULL);

    // size of the alphabet
    const unsigned alpha_size = 255;

    size_t str1_len = strlen(str1);
    size_t str2_len = strlen(str2);

    // handle cases where one or both strings are empty
    if (str1_len == 0) {
        return str2_len;
    }
    if (str2_len == 0) {
        return str1_len;
    }

    // remove common substring
    while (str1_len > 0 && str2_len > 0 && EQ(str1[0], str2[0])) {
        str1++, str2++;
        str1_len--, str2_len--;
    }

    const unsigned INFINITY = str1_len + str2_len;
    unsigned row, col;

    // create "dictionary"
    unsigned* dict = calloc(alpha_size, sizeof(unsigned));

    size_t m_rows = str1_len + 2;  // matrix rows
    size_t m_cols = str2_len + 2;  // matrix cols

    // matrix to hold computed values
    unsigned** matrix = malloc(m_rows * sizeof(unsigned*));
    for (unsigned i = 0; i < m_rows; i++) {
        matrix[i] = calloc(m_cols, sizeof(unsigned));
    }

    // set all the starting values and add all characters to the dict
    matrix[0][0] = INFINITY;
    for (row = 1; row < m_rows; row++) {
        matrix[row][0] = INFINITY;
        matrix[row][1] = row - 1;
    }
    for (col = 1; col < m_cols; col++) {
        matrix[0][col] = INFINITY;
        matrix[1][col] = col - 1;
    }

    unsigned db;
    unsigned i, k;
    unsigned cost;

    // fill in the matrix
    for (row = 1; row <= str1_len; row++) {
        db = 0;

        for (col = 1; col <= str2_len; col++) {
            i = dict[(unsigned)str2[col - 1]];
            k = db;
            cost = EQ(str1[row - 1], str2[col - 1]) ? 0 : 1;

            if (cost == 0) {
                db = col;
            }

            matrix[row + 1][col + 1] =
                MIN4(matrix[row][col] + cost, matrix[row + 1][col] + 1, matrix[row][col + 1] + 1,
                     matrix[i][k] + (row - i - 1) + (col - k - 1) + 1);
        }

        dict[(unsigned)str1[row - 1]] = row;
    }

    unsigned result = matrix[m_rows - 1][m_cols - 1];

    // free allocated memory
    free(dict);
    for (unsigned i = 0; i < m_rows; i++) {
        free(matrix[i]);
    }
    free(matrix);

    return result;
}
// Originally from the spellfix SQLite exension, Public Domain
// https://www.sqlite.org/src/file/ext/misc/spellfix.c
// Modified by Anton Zhiyanov, https://github.com/nalgeon/sqlean/, MIT License

#include <assert.h>
#include <stdlib.h>

#include "fuzzy/common.h"

extern const unsigned char midClass[];
extern const unsigned char initClass[];
extern const unsigned char className[];

/*
** Return the character class number for a character given its
** context.
*/
static char characterClass(char cPrev, char c) {
    return cPrev == 0 ? initClass[c & 0x7f] : midClass[c & 0x7f];
}

/*
** Return the cost of inserting or deleting character c immediately
** following character cPrev.  If cPrev==0, that means c is the first
** character of the word.
*/
static int insertOrDeleteCost(char cPrev, char c, char cNext) {
    char classC = characterClass(cPrev, c);
    char classCprev;

    if (classC == CCLASS_SILENT) {
        /* Insert or delete "silent" characters such as H or W */
        return 1;
    }
    if (cPrev == c) {
        /* Repeated characters, or miss a repeat */
        return 10;
    }
    if (classC == CCLASS_VOWEL && (cPrev == 'r' || cNext == 'r')) {
        return 20; /* Insert a vowel before or after 'r' */
    }
    classCprev = characterClass(cPrev, cPrev);
    if (classC == classCprev) {
        if (classC == CCLASS_VOWEL) {
            /* Remove or add a new vowel to a vowel cluster */
            return 15;
        } else {
            /* Remove or add a consonant not in the same class */
            return 50;
        }
    }

    /* any other character insertion or deletion */
    return 100;
}

/*
** Divide the insertion cost by this factor when appending to the
** end of the word.
*/
#define FINAL_INS_COST_DIV 4

/*
** Return the cost of substituting cTo in place of cFrom assuming
** the previous character is cPrev.  If cPrev==0 then cTo is the first
** character of the word.
*/
static int substituteCost(char cPrev, char cFrom, char cTo) {
    char classFrom, classTo;
    if (cFrom == cTo) {
        /* Exact match */
        return 0;
    }
    if (cFrom == (cTo ^ 0x20) && ((cTo >= 'A' && cTo <= 'Z') || (cTo >= 'a' && cTo <= 'z'))) {
        /* differ only in case */
        return 0;
    }
    classFrom = characterClass(cPrev, cFrom);
    classTo = characterClass(cPrev, cTo);
    if (classFrom == classTo) {
        /* Same character class */
        return 40;
    }
    if (classFrom >= CCLASS_B && classFrom <= CCLASS_Y && classTo >= CCLASS_B &&
        classTo <= CCLASS_Y) {
        /* Convert from one consonant to another, but in a different class */
        return 75;
    }
    /* Any other subsitution */
    return 100;
}

/*
** Given two strings zA and zB which are pure ASCII, return the cost
** of transforming zA into zB.  If zA ends with '*' assume that it is
** a prefix of zB and give only minimal penalty for extra characters
** on the end of zB.
**
** Smaller numbers mean a closer match.
**
** Negative values indicate an error:
**    -1  One of the inputs is NULL
**    -2  Non-ASCII characters on input
**    -3  Unable to allocate memory
**
** If pnMatch is not NULL, then *pnMatch is set to the number of bytes
** of zB that matched the pattern in zA. If zA does not end with a '*',
** then this value is always the number of bytes in zB (i.e. strlen(zB)).
** If zA does end in a '*', then it is the number of bytes in the prefix
** of zB that was deemed to match zA.
*/
int edit_distance(const char* zA, const char* zB, int* pnMatch) {
    int nA, nB;          /* Number of characters in zA[] and zB[] */
    int xA, xB;          /* Loop counters for zA[] and zB[] */
    char cA = 0, cB;     /* Current character of zA and zB */
    char cAprev, cBprev; /* Previous character of zA and zB */
    char cAnext, cBnext; /* Next character in zA and zB */
    int d;               /* North-west cost value */
    int dc = 0;          /* North-west character value */
    int res;             /* Final result */
    int* m;              /* The cost matrix */
    char* cx;            /* Corresponding character values */
    int* toFree = 0;     /* Malloced space */
    int nMatch = 0;
    int mStack[60 + 15]; /* Stack space to use if not too much is needed */

    /* Early out if either input is NULL */
    if (zA == 0 || zB == 0)
        return -1;

    /* Skip any common prefix */
    while (zA[0] && zA[0] == zB[0]) {
        dc = zA[0];
        zA++;
        zB++;
        nMatch++;
    }
    if (pnMatch)
        *pnMatch = nMatch;
    if (zA[0] == 0 && zB[0] == 0)
        return 0;

#if 0
  printf("A=\"%s\" B=\"%s\" dc=%c\n", zA, zB, dc?dc:' ');
#endif

    /* Verify input strings and measure their lengths */
    for (nA = 0; zA[nA]; nA++) {
        if (zA[nA] & 0x80)
            return -2;
    }
    for (nB = 0; zB[nB]; nB++) {
        if (zB[nB] & 0x80)
            return -2;
    }

    /* Special processing if either string is empty */
    if (nA == 0) {
        cBprev = (char)dc;
        for (xB = res = 0; (cB = zB[xB]) != 0; xB++) {
            res += insertOrDeleteCost(cBprev, cB, zB[xB + 1]) / FINAL_INS_COST_DIV;
            cBprev = cB;
        }
        return res;
    }
    if (nB == 0) {
        cAprev = (char)dc;
        for (xA = res = 0; (cA = zA[xA]) != 0; xA++) {
            res += insertOrDeleteCost(cAprev, cA, zA[xA + 1]);
            cAprev = cA;
        }
        return res;
    }

    /* A is a prefix of B */
    if (zA[0] == '*' && zA[1] == 0)
        return 0;

    /* Allocate and initialize the Wagner matrix */
    if ((size_t)nB < (sizeof(mStack) * 4) / (sizeof(mStack[0]) * 5)) {
        m = mStack;
    } else {
        m = toFree = malloc((nB + 1) * 5 * sizeof(m[0]) / 4);
        if (m == 0)
            return -3;
    }
    cx = (char*)&m[nB + 1];

    /* Compute the Wagner edit distance */
    m[0] = 0;
    cx[0] = (char)dc;
    cBprev = (char)dc;
    for (xB = 1; xB <= nB; xB++) {
        cBnext = zB[xB];
        cB = zB[xB - 1];
        cx[xB] = cB;
        m[xB] = m[xB - 1] + insertOrDeleteCost(cBprev, cB, cBnext);
        cBprev = cB;
    }
    cAprev = (char)dc;
    for (xA = 1; xA <= nA; xA++) {
        int lastA = (xA == nA);
        cA = zA[xA - 1];
        cAnext = zA[xA];
        if (cA == '*' && lastA)
            break;
        d = m[0];
        dc = cx[0];
        m[0] = d + insertOrDeleteCost(cAprev, cA, cAnext);
        cBprev = 0;
        for (xB = 1; xB <= nB; xB++) {
            int totalCost, insCost, delCost, subCost, ncx;
            cB = zB[xB - 1];
            cBnext = zB[xB];

            /* Cost to insert cB */
            insCost = insertOrDeleteCost(cx[xB - 1], cB, cBnext);
            if (lastA)
                insCost /= FINAL_INS_COST_DIV;

            /* Cost to delete cA */
            delCost = insertOrDeleteCost(cx[xB], cA, cBnext);

            /* Cost to substitute cA->cB */
            subCost = substituteCost(cx[xB - 1], cA, cB);

            /* Best cost */
            totalCost = insCost + m[xB - 1];
            ncx = cB;
            if ((delCost + m[xB]) < totalCost) {
                totalCost = delCost + m[xB];
                ncx = cA;
            }
            if ((subCost + d) < totalCost) {
                totalCost = subCost + d;
            }

#if 0
      printf("%d,%d d=%4d u=%4d r=%4d dc=%c cA=%c cB=%c"
             " ins=%4d del=%4d sub=%4d t=%4d ncx=%c\n",
             xA, xB, d, m[xB], m[xB-1], dc?dc:' ', cA, cB,
             insCost, delCost, subCost, totalCost, ncx?ncx:' ');
#endif

            /* Update the matrix */
            d = m[xB];
            dc = cx[xB];
            m[xB] = totalCost;
            cx[xB] = (char)ncx;
            cBprev = cB;
        }
        cAprev = cA;
    }

    /* Free the wagner matrix and return the result */
    if (cA == '*') {
        res = m[1];
        for (xB = 1; xB <= nB; xB++) {
            if (m[xB] < res) {
                res = m[xB];
                if (pnMatch)
                    *pnMatch = xB + nMatch;
            }
        }
    } else {
        res = m[nB];
        /* In the current implementation, pnMatch is always NULL if zA does
        ** not end in "*" */
        assert(pnMatch == 0);
    }
    free(toFree);
    return res;
}
// Copyright (c) 2023 Anton Zhiyanov, MIT License
// https://github.com/nalgeon/sqlean

// Fuzzy string matching and phonetics.

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>

#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT3

#include "fuzzy/fuzzy.h"

// is_ascii checks if the string consists of ASCII symbols only
static bool is_ascii(const unsigned char* str) {
    for (int idx = 0; str[idx]; idx++) {
        if (str[idx] & 0x80) {
            return false;
        }
    }
    return true;
}

// Below are functions extracted from the
// https://github.com/Rostepher/libstrcmp/

// fuzzy_damlev implements Damerau-Levenshtein distance
static void fuzzy_damlev(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);
    const unsigned char* str1 = sqlite3_value_text(argv[0]);
    const unsigned char* str2 = sqlite3_value_text(argv[1]);
    if (str1 == 0 || str2 == 0) {
        sqlite3_result_error(context, "arguments should not be NULL", -1);
        return;
    }
    if (!is_ascii(str1) || !is_ascii(str2)) {
        sqlite3_result_error(context, "arguments should be ASCII strings", -1);
        return;
    }
    unsigned distance = damerau_levenshtein((const char*)str1, (const char*)str2);
    sqlite3_result_int(context, distance);
}

// fuzzy_hamming implements Hamming distance
static void fuzzy_hamming(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);
    const unsigned char* str1 = sqlite3_value_text(argv[0]);
    const unsigned char* str2 = sqlite3_value_text(argv[1]);
    if (str1 == 0 || str2 == 0) {
        sqlite3_result_error(context, "arguments should not be NULL", -1);
        return;
    }
    if (!is_ascii(str1) || !is_ascii(str2)) {
        sqlite3_result_error(context, "arguments should be ASCII strings", -1);
        return;
    }
    int distance = hamming((const char*)str1, (const char*)str2);
    sqlite3_result_int(context, distance);
}

// fuzzy_jarowin implements Jaro-Winkler distance
static void fuzzy_jarowin(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);
    const unsigned char* str1 = sqlite3_value_text(argv[0]);
    const unsigned char* str2 = sqlite3_value_text(argv[1]);
    if (str1 == 0 || str2 == 0) {
        sqlite3_result_error(context, "arguments should not be NULL", -1);
        return;
    }
    if (!is_ascii(str1) || !is_ascii(str2)) {
        sqlite3_result_error(context, "arguments should be ASCII strings", -1);
        return;
    }
    double distance = jaro_winkler((const char*)str1, (const char*)str2);
    sqlite3_result_double(context, distance);
}

// fuzzy_leven implements Levenshtein distance
static void fuzzy_leven(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);
    const unsigned char* str1 = sqlite3_value_text(argv[0]);
    const unsigned char* str2 = sqlite3_value_text(argv[1]);
    if (str1 == 0 || str2 == 0) {
        sqlite3_result_error(context, "arguments should not be NULL", -1);
        return;
    }
    if (!is_ascii(str1) || !is_ascii(str2)) {
        sqlite3_result_error(context, "arguments should be ASCII strings", -1);
        return;
    }
    unsigned distance = levenshtein((const char*)str1, (const char*)str2);
    sqlite3_result_int(context, distance);
}

// fuzzy_osadist implements Optimal String Alignment distance
static void fuzzy_osadist(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 2);
    const unsigned char* str1 = sqlite3_value_text(argv[0]);
    const unsigned char* str2 = sqlite3_value_text(argv[1]);
    if (str1 == 0 || str2 == 0) {
        sqlite3_result_error(context, "arguments should not be NULL", -1);
        return;
    }
    if (!is_ascii(str1) || !is_ascii(str2)) {
        sqlite3_result_error(context, "arguments should be ASCII strings", -1);
        return;
    }
    unsigned distance = optimal_string_alignment((const char*)str1, (const char*)str2);
    sqlite3_result_int(context, distance);
}

// fuzzy_soundex implements Soundex coding
static void fuzzy_soundex(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);
    const unsigned char* source = sqlite3_value_text(argv[0]);
    if (source == 0) {
        return;
    }
    if (!is_ascii(source)) {
        sqlite3_result_error(context, "argument should be ASCII string", -1);
        return;
    }
    char* result = soundex((const char*)source);
    sqlite3_result_text(context, result, -1, free);
}

// fuzzy_rsoundex implements Refined Soundex coding
static void fuzzy_rsoundex(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);
    const unsigned char* source = sqlite3_value_text(argv[0]);
    if (source == 0) {
        return;
    }
    if (!is_ascii(source)) {
        sqlite3_result_error(context, "argument should be ASCII string", -1);
        return;
    }
    char* result = refined_soundex((const char*)source);
    sqlite3_result_text(context, result, -1, free);
}

// Below are functions extracted from the spellfix SQLite exension
// https://www.sqlite.org/src/file/ext/misc/spellfix.c

/*
** fuzzy_phonetic(X)
**
** Generate a "phonetic hash" from a string of ASCII characters in X.
**
**   * Map characters by character class as defined above.
**   * Omit double-letters
**   * Omit vowels beside R and L
**   * Omit T when followed by CH
**   * Omit W when followed by R
**   * Omit D when followed by J or G
**   * Omit K in KN or G in GN at the beginning of a word
**
** Space to hold the result is obtained from sqlite3_malloc()
**
** Return NULL if memory allocation fails.
*/
static void fuzzy_phonetic(sqlite3_context* context, int argc, sqlite3_value** argv) {
    const unsigned char* zIn;
    unsigned char* zOut;

    zIn = sqlite3_value_text(argv[0]);
    if (zIn == 0)
        return;
    zOut = phonetic_hash(zIn, sqlite3_value_bytes(argv[0]));
    if (zOut == 0) {
        sqlite3_result_error_nomem(context);
    } else {
        sqlite3_result_text(context, (char*)zOut, -1, free);
    }
}

/*
** fuzzy_editdist(A,B)
**
** Return the cost of transforming string A into string B.  Both strings
** must be pure ASCII text.  If A ends with '*' then it is assumed to be
** a prefix of B and extra characters on the end of B have minimal additional
** cost.
*/
static void fuzzy_editdist(sqlite3_context* context, int argc, sqlite3_value** argv) {
    int res = edit_distance((const char*)sqlite3_value_text(argv[0]),
                            (const char*)sqlite3_value_text(argv[1]), 0);
    if (res < 0) {
        if (res == (-3)) {
            sqlite3_result_error_nomem(context);
        } else if (res == (-2)) {
            sqlite3_result_error(context, "non-ASCII input to editdist()", -1);
        } else {
            sqlite3_result_error(context, "NULL input to editdist()", -1);
        }
    } else {
        sqlite3_result_int(context, res);
    }
}

/*
** fuzzy_translit(X)
**
** Convert a string that contains non-ASCII Roman characters into
** pure ASCII.
*/
static void fuzzy_translit(sqlite3_context* context, int argc, sqlite3_value** argv) {
    const unsigned char* zIn = sqlite3_value_text(argv[0]);
    int nIn = sqlite3_value_bytes(argv[0]);
    unsigned char* zOut = transliterate(zIn, nIn);
    if (zOut == 0) {
        sqlite3_result_error_nomem(context);
    } else {
        sqlite3_result_text(context, (char*)zOut, -1, free);
    }
}

/*
** fuzzy_script(X)
**
** Try to determine the dominant script used by the word X and return
** its ISO 15924 numeric code.
**
** The current implementation only understands the following scripts:
**
**    215  (Latin)
**    220  (Cyrillic)
**    200  (Greek)
**
** This routine will return 998 if the input X contains characters from
** two or more of the above scripts or 999 if X contains no characters
** from any of the above scripts.
*/
static void fuzzy_script(sqlite3_context* context, int argc, sqlite3_value** argv) {
    const unsigned char* zIn = sqlite3_value_text(argv[0]);
    int nIn = sqlite3_value_bytes(argv[0]);
    int res = script_code(zIn, nIn);
    sqlite3_result_int(context, res);
}

// Below are custom functions

// fuzzy_caver implements Caverphone coding
static void fuzzy_caver(sqlite3_context* context, int argc, sqlite3_value** argv) {
    assert(argc == 1);
    const unsigned char* source = sqlite3_value_text(argv[0]);
    if (source == 0) {
        return;
    }
    if (!is_ascii(source)) {
        sqlite3_result_error(context, "argument should be ASCII string", -1);
        return;
    }
    char* result = caverphone((const char*)source);
    sqlite3_result_text(context, result, -1, free);
}

int fuzzy_init(sqlite3* db) {
    static const int flags = SQLITE_UTF8 | SQLITE_INNOCUOUS | SQLITE_DETERMINISTIC;
    // libstrcmp
    sqlite3_create_function(db, "fuzzy_damlev", 2, flags, 0, fuzzy_damlev, 0, 0);
    sqlite3_create_function(db, "dlevenshtein", 2, flags, 0, fuzzy_damlev, 0, 0);
    sqlite3_create_function(db, "fuzzy_hamming", 2, flags, 0, fuzzy_hamming, 0, 0);
    sqlite3_create_function(db, "hamming", 2, flags, 0, fuzzy_hamming, 0, 0);
    sqlite3_create_function(db, "fuzzy_jarowin", 2, flags, 0, fuzzy_jarowin, 0, 0);
    sqlite3_create_function(db, "jaro_winkler", 2, flags, 0, fuzzy_jarowin, 0, 0);
    sqlite3_create_function(db, "fuzzy_leven", 2, flags, 0, fuzzy_leven, 0, 0);
    sqlite3_create_function(db, "levenshtein", 2, flags, 0, fuzzy_leven, 0, 0);
    sqlite3_create_function(db, "fuzzy_osadist", 2, flags, 0, fuzzy_osadist, 0, 0);
    sqlite3_create_function(db, "osa_distance", 2, flags, 0, fuzzy_osadist, 0, 0);
    sqlite3_create_function(db, "fuzzy_soundex", 1, flags, 0, fuzzy_soundex, 0, 0);
    sqlite3_create_function(db, "soundex", 1, flags, 0, fuzzy_soundex, 0, 0);
    sqlite3_create_function(db, "fuzzy_rsoundex", 1, flags, 0, fuzzy_rsoundex, 0, 0);
    sqlite3_create_function(db, "rsoundex", 1, flags, 0, fuzzy_rsoundex, 0, 0);
    // spellfix
    sqlite3_create_function(db, "fuzzy_editdist", 2, flags, 0, fuzzy_editdist, 0, 0);
    sqlite3_create_function(db, "edit_distance", 2, flags, 0, fuzzy_editdist, 0, 0);
    sqlite3_create_function(db, "fuzzy_phonetic", 1, flags, 0, fuzzy_phonetic, 0, 0);
    sqlite3_create_function(db, "phonetic_hash", 1, flags, 0, fuzzy_phonetic, 0, 0);
    sqlite3_create_function(db, "fuzzy_script", 1, flags, 0, fuzzy_script, 0, 0);
    sqlite3_create_function(db, "script_code", 1, flags, 0, fuzzy_script, 0, 0);
    sqlite3_create_function(db, "fuzzy_translit", 1, flags, 0, fuzzy_translit, 0, 0);
    sqlite3_create_function(db, "translit", 1, flags, 0, fuzzy_translit, 0, 0);
    // custom
    sqlite3_create_function(db, "fuzzy_caver", 1, flags, 0, fuzzy_caver, 0, 0);
    sqlite3_create_function(db, "caverphone", 1, flags, 0, fuzzy_caver, 0, 0);
    return SQLITE_OK;
}
// Copyright (c) 2014 Ross Bayer, MIT License
// https://github.com/Rostepher/libstrcmp

#include <assert.h>
#include <stddef.h>
#include <string.h>

#include "fuzzy/common.h"

/// Computes and returns the hamming distance between two strings. Both strings
/// must have the same length and not be NULL. More information about the
/// algorithm can be found here:
///     http://en.wikipedia.org/wiki/Hamming_distance
///
/// @param str1 first non NULL string
/// @param str2 second non NULL string
///
/// @returns hamming distance or -1 if str1 and st2 did not have the same
///     length or if one or both str1 and str2 were NULL
int hamming(const char* str1, const char* str2) {
    // strings cannot be NULL
    assert(str1 != NULL);
    assert(str2 != NULL);

    size_t str1_len = strlen(str1);
    size_t str2_len = strlen(str2);

    // handle cases where strings have different lengths
    if (str1_len != str2_len) {
        return -1;
    }

    // return 0 if strings are both empty, but not NULL
    if (str1_len == 0 && str2_len == 0) {
        return 0;
    }

    int dist = 0;
    while (str1_len > 0 && str2_len > 0) {
        dist += (NOT_EQ(*str1, *str2));
        str1++, str2++;
        str1_len--, str2_len--;
    }

    return dist;
}
// Copyright (c) 2014 Ross Bayer, MIT License
// https://github.com/Rostepher/libstrcmp

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "fuzzy/common.h"

/// Calculates and returns the Jaro distance of two non NULL strings.
/// More information about the algorithm can be found here:
///     http://en.wikipedia.org/wiki/Jaro-Winkler_distance
///
/// @param str1 first non NULL string
/// @param str2 second non NULL string
///
/// @returns the jaro distance of str1 and str2
double jaro(const char* str1, const char* str2) {
    // strings cannot be NULL
    assert(str1 != NULL);
    assert(str2 != NULL);

    int str1_len = strlen(str1);
    int str2_len = strlen(str2);

    // if both strings are empty return 1
    // if only one of the strings is empty return 0
    if (str1_len == 0) {
        return (str2_len == 0) ? 1.0 : 0.0;
    }

    // max distance between two chars to be considered matching
    // floor() is ommitted due to integer division rules
    int match_dist = (int)MAX(str1_len, str2_len) / 2 - 1;

    // arrays of bools that signify if that char in the matcing string has a
    // match
    int* str1_matches = calloc(str1_len, sizeof(int));
    int* str2_matches = calloc(str2_len, sizeof(int));

    // number of matches and transpositions
    double matches = 0.0;
    double trans = 0.0;

    // find the matches
    for (int i = 0; i < str1_len; i++) {
        // start and end take into account the match distance
        int start = MAX(0, i - match_dist);
        int end = MIN(i + match_dist + 1, str2_len);

        for (int k = start; k < end; k++) {
            // if str2 already has a match or str1 and str2 are not equal
            // continue
            if (str2_matches[k] || NOT_EQ(str1[i], str2[k])) {
                continue;
            }

            // otherwise assume there is a match
            str1_matches[i] = true;
            str2_matches[k] = true;
            matches++;
            break;
        }
    }

    // if there are no matches return 0
    if (matches == 0) {
        free(str1_matches);
        free(str2_matches);
        return 0.0;
    }

    // count transpositions
    int k = 0;
    for (int i = 0; i < str1_len; i++) {
        // if there are no matches in str1 continue
        if (!str1_matches[i]) {
            continue;
        }

        // while there is no match in str2 increment k
        while (!str2_matches[k]) {
            k++;
        }

        // increment trans
        if (NOT_EQ(str1[i], str2[k])) {
            trans++;
        }

        k++;
    }

    // divide the number of transpositions by two as per the algorithm specs
    // this division is valid because the counted transpositions include both
    // instances of the transposed characters.
    trans /= 2.0;

    // free allocated memory
    free(str1_matches);
    free(str2_matches);

    // return the jaro distance
    return ((matches / str1_len) + (matches / str2_len) + ((matches - trans) / matches)) / 3.0;
}

/// Calculates and returns the Jaro-Winkler distance of two non NULL strings.
/// More information about the algorithm can be found here:
///     http://en.wikipedia.org/wiki/Jaro-Winkler_distance
///
/// @param str1 first non NULL string
/// @param str2 second non NULL string
///
/// @returns the jaro-winkler distance of str1 and str2
double jaro_winkler(const char* str1, const char* str2) {
    // strings cannot be NULL
    assert(str1 != NULL);
    assert(str2 != NULL);

    // compute the jaro distance
    double dist = jaro(str1, str2);

    // finds the number of common terms in the first 3 strings, max 3.
    int prefix_length = 0;
    if (strlen(str1) != 0 && strlen(str2) != 0) {
        while (prefix_length < 3 && EQ(*str1++, *str2++)) {
            prefix_length++;
        }
    }

    // 0.1 is the default scaling factor
    return dist + prefix_length * 0.1 * (1 - dist);
}
// Copyright (c) 2014 Ross Bayer, MIT License
// https://github.com/Rostepher/libstrcmp

#include <assert.h>
#include <stdlib.h>
#include <string.h>

#include "fuzzy/common.h"

/// Calculates and returns the Levenshtein distance of two non NULL strings.
/// More information about the algorithm can be found here:
///     https://en.wikipedia.org/wiki/Levenshtein_distance
///
/// @param str1 first non NULL string
/// @param str2 second non NULL string
///
/// @returns the levenshtein distance of str1 and str2
unsigned levenshtein(const char* str1, const char* str2) {
    // strings cannot be NULL
    assert(str1 != NULL);
    assert(str2 != NULL);

    size_t str1_len = strlen(str1);
    size_t str2_len = strlen(str2);

    // handle cases where one or both strings are empty
    if (str1_len == 0) {
        return str2_len;
    }
    if (str2_len == 0) {
        return str1_len;
    }

    // remove common substring
    while (str1_len > 0 && str2_len > 0 && EQ(str1[0], str2[0])) {
        str1++, str2++;
        str1_len--, str2_len--;
    }

    // declare variables
    unsigned row, col;
    unsigned last_diag = 0, cur, cost;

    // initialize array to hold values
    unsigned* vector = calloc(str1_len + 1, sizeof(unsigned));
    for (col = 1; col <= str1_len; col++) {
        vector[col] = col;
    }

    // itterate through the imagined rows of arrays
    for (row = 1; row <= str2_len + 1; row++) {
        vector[0] = row;
        last_diag = row - 1;  // remember the last first slot

        // itterate throught each member of the vector
        for (col = 1; col <= str1_len; col++) {
            // remember the diagonal before overwriting the array
            cur = vector[col];

            // calculate the cost
            cost = EQ(str1[col - 1], str2[row - 1]) ? 0 : 1;

            // determine min of the possible values
            vector[col] = MIN3(vector[col] + 1, vector[col - 1] + 1, last_diag + cost);

            // remember the new last_diag
            last_diag = cur;
        }
    }

    free(vector);
    return last_diag;
}
// Copyright (c) 2014 Ross Bayer, MIT License
// https://github.com/Rostepher/libstrcmp

#include <assert.h>
#include <stdlib.h>
#include <string.h>

#include "fuzzy/common.h"

/// Computes and returns the Optimal String Alignment distance for two non NULL
/// strings. More information about the algorithm can be found here:
///     https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance
///
/// @param str1 first non NULL string
/// @param str2 second non NULL string
///
/// @returns optimal string alignment distance for str1 and str2
unsigned optimal_string_alignment(const char* str1, const char* str2) {
    // strings cannot be NULL
    assert(str1 != NULL);
    assert(str2 != NULL);

    size_t str1_len = strlen(str1);
    size_t str2_len = strlen(str2);

    // handle cases where one or both strings are empty
    if (str1_len == 0) {
        return str2_len;
    }
    if (str2_len == 0) {
        return str1_len;
    }

    // remove common substring
    while (str1_len > 0 && str2_len > 0 && EQ(str1[0], str2[0])) {
        str1++, str2++;
        str1_len--, str2_len--;
    }

    unsigned row, col, cost, result;

    // initialize matrix to hold distance values
    unsigned** matrix = malloc((str1_len + 1) * sizeof(unsigned*));
    for (unsigned i = 0; i <= str1_len; i++) {
        matrix[i] = calloc((str2_len + 1), sizeof(unsigned));
    }

    // set all the starting values
    matrix[0][0] = 0;
    for (row = 1; row <= str1_len; row++) {
        matrix[row][0] = row;
    }
    for (col = 1; col <= str2_len; col++) {
        matrix[0][col] = col;
    }

    // itterate through and fill in the matrix
    for (row = 1; row <= str1_len; row++) {
        for (col = 1; col <= str2_len; col++) {
            cost = EQ(str1[row - 1], str2[col - 1]) ? 0 : 1;

            matrix[row][col] = MIN3(matrix[row - 1][col] + 1,        // deletion
                                    matrix[row][col - 1] + 1,        // insertion
                                    matrix[row - 1][col - 1] + cost  // substitution
            );

            // transpositions
            if (row > 1 && col > 1 && EQ(str1[row], str2[col - 1]) &&
                EQ(str1[row - 1], str2[col])) {
                matrix[row][col] = MIN(matrix[row][col], matrix[row - 2][col - 2] + cost);
            }
        }
    }

    result = matrix[str1_len][str2_len];

    // free allocated memory
    for (unsigned i = 0; i < str1_len + 1; i++) {
        free(matrix[i]);
    }
    free(matrix);

    return result;
}
// Ooriginally from the spellfix SQLite exension, Public Domain
// https://www.sqlite.org/src/file/ext/misc/spellfix.c
// Modified by Anton Zhiyanov, https://github.com/nalgeon/sqlean/, MIT License

#include <assert.h>
#include <stdlib.h>

#include "fuzzy/common.h"

extern const unsigned char midClass[];
extern const unsigned char initClass[];
extern const unsigned char className[];

/*
** Generate a "phonetic hash" from a string of ASCII characters
** in zIn[0..nIn-1].
**
**   * Map characters by character class as defined above.
**   * Omit double-letters
**   * Omit vowels beside R and L
**   * Omit T when followed by CH
**   * Omit W when followed by R
**   * Omit D when followed by J or G
**   * Omit K in KN or G in GN at the beginning of a word
**
** Space to hold the result is obtained from sqlite3_malloc()
**
** Return NULL if memory allocation fails.
*/
unsigned char* phonetic_hash(const unsigned char* zIn, int nIn) {
    unsigned char* zOut = malloc(nIn + 1);
    int i;
    int nOut = 0;
    char cPrev = 0x77;
    char cPrevX = 0x77;
    const unsigned char* aClass = initClass;

    if (zOut == 0)
        return 0;
    if (nIn > 2) {
        switch (zIn[0]) {
            case 'g':
            case 'k': {
                if (zIn[1] == 'n') {
                    zIn++;
                    nIn--;
                }
                break;
            }
        }
    }
    for (i = 0; i < nIn; i++) {
        unsigned char c = zIn[i];
        if (i + 1 < nIn) {
            if (c == 'w' && zIn[i + 1] == 'r')
                continue;
            if (c == 'd' && (zIn[i + 1] == 'j' || zIn[i + 1] == 'g'))
                continue;
            if (i + 2 < nIn) {
                if (c == 't' && zIn[i + 1] == 'c' && zIn[i + 2] == 'h')
                    continue;
            }
        }
        c = aClass[c & 0x7f];
        if (c == CCLASS_SPACE)
            continue;
        if (c == CCLASS_OTHER && cPrev != CCLASS_DIGIT)
            continue;
        aClass = midClass;
        if (c == CCLASS_VOWEL && (cPrevX == CCLASS_R || cPrevX == CCLASS_L)) {
            continue; /* No vowels beside L or R */
        }
        if ((c == CCLASS_R || c == CCLASS_L) && cPrevX == CCLASS_VOWEL) {
            nOut--; /* No vowels beside L or R */
        }
        cPrev = c;
        if (c == CCLASS_SILENT)
            continue;
        cPrevX = c;
        c = className[c];
        assert(nOut >= 0);
        if (nOut == 0 || c != zOut[nOut - 1])
            zOut[nOut++] = c;
    }
    zOut[nOut] = 0;
    return zOut;
}
// Copyright (c) 2014 Ross Bayer, MIT License
// https://github.com/Rostepher/libstrcmp

#include <assert.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#include "fuzzy/common.h"

/// Helper function that returns the numeric code for a given char as specified
/// by the refined soundex algorithm.
///
/// @param c char to encode
///
/// @returns char representation of the number associated with the given char
static char rsoundex_encode(const char c) {
    switch (tolower(c)) {
        case 'b':
        case 'p':
            return '1';

        case 'f':
        case 'v':
            return '2';

        case 'c':
        case 'k':
        case 's':
            return '3';

        case 'g':
        case 'j':
            return '4';

        case 'q':
        case 'x':
        case 'z':
            return '5';

        case 'd':
        case 't':
            return '6';

        case 'l':
            return '7';

        case 'm':
        case 'n':
            return '8';

        case 'r':
            return '9';

        default:
            break;
    }

    return '0';
}

/// Computes and returns the soundex representation of a given non NULL string.
/// More information about the algorithm can be found here:
///     http://ntz-develop.blogspot.com/2011/03/phonetic-algorithms.html
///
/// @param str non NULL string to encode
///
/// @returns soundex representation of str
char* refined_soundex(const char* str) {
    // string cannot be NULL
    assert(str != NULL);

    size_t str_len = strlen(str);

    // final code buffer
    char* code = malloc((str_len + 1) * sizeof(char));

    // temporary buffer to encode string
    char* buf = malloc((str_len + 1) * sizeof(char));

    // set first value to first char in str
    code[0] = toupper(str[0]);

    // number of digits in code
    unsigned d = 1;

    // encode all chars in str
    for (unsigned i = 0; i < str_len; i++)
        buf[i] = rsoundex_encode(str[i]);

    // add all viable chars to code
    char prev = '\0';
    for (unsigned i = 0; i < str_len; i++) {
        // check if current char in buf is not the same as previous char
        if (NOT_EQ(buf[i], prev)) {
            // add digit to the code
            code[d] = buf[i];

            // increment digit counter
            d++;

            // set prev to current char
            prev = buf[i];
        }
    }

    // allocate space for final code
    // d will be length of the code + 1
    char* result = malloc((d + 1) * sizeof(char));

    // copy final code into result and null terminate
    for (unsigned i = 0; i < d; i++) {
        result[i] = code[i];
    }
    result[d] = '\0';

    free(code);
    free(buf);

    return result;
}
// Copyright (c) 2014 Ross Bayer, MIT License
// https://github.com/Rostepher/libstrcmp

#include <assert.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#include "fuzzy/common.h"

/// Helper function that returns the numeric code for a given char as specified
/// by the soundex algorithm.
///
/// @param c char to encode
///
/// @returns char representation of the number associated with the given char
static char soundex_encode(const char c) {
    switch (tolower(c)) {
        case 'b':
        case 'f':
        case 'p':
        case 'v':
            return '1';

        case 'c':
        case 'g':
        case 'j':
        case 'k':
        case 'q':
        case 's':
        case 'x':
        case 'z':
            return '2';

        case 'd':
        case 't':
            return '3';

        case 'l':
            return '4';

        case 'm':
        case 'n':
            return '5';

        case 'r':
            return '6';

        default:
            break;
    }

    return '0';
}

/// Computes and returns the soundex representation of a given non NULL string.
/// More information about the algorithm can be found here:
///     https://en.wikipedia.org/wiki/Soundex
///
/// @param str non NULL string to encode
///
/// @returns soundex representation of str
char* soundex(const char* str) {
    // string cannot be NULL
    assert(str != NULL);

    size_t str_len = strlen(str);

    // allocate space for final code and null terminator
    char* code = malloc(5 * sizeof(char));

    // temporary buffer to encode string
    char* buf = malloc((str_len + 1) * sizeof(char));

    // set first value to first char in str
    code[0] = toupper(str[0]);

    // number of digits in code
    unsigned d = 1;

    // encode all chars in str
    for (unsigned i = 0; i < str_len; i++) {
        buf[i] = soundex_encode(str[i]);
    }

    // add all viable chars to code
    for (unsigned i = 1; i < str_len && d < 4; i++) {
        // check if current char in buf is not the same as previous char
        // and that the current char is not '0'
        if (NOT_EQ(buf[i], buf[i - 1]) && NOT_EQ(buf[i], '0')) {
            // if digits separated by an 'h' or 'w' are the same, skip them
            if (i > 1 && EQ(buf[i], buf[i - 2]) && strchr("hw", str[i - 1])) {
                continue;
            }

            // add digit to the code
            code[d] = buf[i];

            // increment digit counter
            d++;
        }
    }

    // pad the end of code with '0' if too short
    while (d < 4) {
        code[d] = '0';
        d++;
    }

    // null terminate string
    code[d] = '\0';
    free(buf);

    return code;
}
// Originally from the spellfix SQLite exension, Public Domain
// https://www.sqlite.org/src/file/ext/misc/spellfix.c
// Modified by Anton Zhiyanov, https://github.com/nalgeon/sqlean/, MIT License

#include <stdlib.h>

#include "fuzzy/common.h"

extern const unsigned char midClass[];
extern const unsigned char initClass[];
extern const unsigned char className[];

/*
** This lookup table is used to help decode the first byte of
** a multi-byte UTF8 character.
*/
static const unsigned char translit_utf8_lookup[] = {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x00, 0x01, 0x02, 0x03, 0x00, 0x01, 0x00, 0x00,
};

/*
** Return the value of the first UTF-8 character in the string.
*/
static int utf8Read(const unsigned char* z, int n, int* pSize) {
    int c, i;

    /* All callers to this routine (in the current implementation)
    ** always have n>0. */
    if (NEVER(n == 0)) {
        c = i = 0;
    } else {
        c = z[0];
        i = 1;
        if (c >= 0xc0) {
            c = translit_utf8_lookup[c - 0xc0];
            while (i < n && (z[i] & 0xc0) == 0x80) {
                c = (c << 6) + (0x3f & z[i++]);
            }
        }
    }
    *pSize = i;
    return c;
}

typedef struct Transliteration Transliteration;
struct Transliteration {
    unsigned short int cFrom;
    unsigned char cTo0, cTo1, cTo2, cTo3;
};

/*
** Table of translations from unicode characters into ASCII.
*/
static const Transliteration translit[] = {
    {0x00A0, 0x20, 0x00, 0x00, 0x00}, /*   to   */
    {0x00B5, 0x75, 0x00, 0x00, 0x00}, /* µ to u */
    {0x00C0, 0x41, 0x00, 0x00, 0x00}, /* À to A */
    {0x00C1, 0x41, 0x00, 0x00, 0x00}, /* Á to A */
    {0x00C2, 0x41, 0x00, 0x00, 0x00}, /* Â to A */
    {0x00C3, 0x41, 0x00, 0x00, 0x00}, /* Ã to A */
    {0x00C4, 0x41, 0x65, 0x00, 0x00}, /* Ä to Ae */
    {0x00C5, 0x41, 0x61, 0x00, 0x00}, /* Å to Aa */
    {0x00C6, 0x41, 0x45, 0x00, 0x00}, /* Æ to AE */
    {0x00C7, 0x43, 0x00, 0x00, 0x00}, /* Ç to C */
    {0x00C8, 0x45, 0x00, 0x00, 0x00}, /* È to E */
    {0x00C9, 0x45, 0x00, 0x00, 0x00}, /* É to E */
    {0x00CA, 0x45, 0x00, 0x00, 0x00}, /* Ê to E */
    {0x00CB, 0x45, 0x00, 0x00, 0x00}, /* Ë to E */
    {0x00CC, 0x49, 0x00, 0x00, 0x00}, /* Ì to I */
    {0x00CD, 0x49, 0x00, 0x00, 0x00}, /* Í to I */
    {0x00CE, 0x49, 0x00, 0x00, 0x00}, /* Î to I */
    {0x00CF, 0x49, 0x00, 0x00, 0x00}, /* Ï to I */
    {0x00D0, 0x44, 0x00, 0x00, 0x00}, /* Ð to D */
    {0x00D1, 0x4E, 0x00, 0x00, 0x00}, /* Ñ to N */
    {0x00D2, 0x4F, 0x00, 0x00, 0x00}, /* Ò to O */
    {0x00D3, 0x4F, 0x00, 0x00, 0x00}, /* Ó to O */
    {0x00D4, 0x4F, 0x00, 0x00, 0x00}, /* Ô to O */
    {0x00D5, 0x4F, 0x00, 0x00, 0x00}, /* Õ to O */
    {0x00D6, 0x4F, 0x65, 0x00, 0x00}, /* Ö to Oe */
    {0x00D7, 0x78, 0x00, 0x00, 0x00}, /* × to x */
    {0x00D8, 0x4F, 0x00, 0x00, 0x00}, /* Ø to O */
    {0x00D9, 0x55, 0x00, 0x00, 0x00}, /* Ù to U */
    {0x00DA, 0x55, 0x00, 0x00, 0x00}, /* Ú to U */
    {0x00DB, 0x55, 0x00, 0x00, 0x00}, /* Û to U */
    {0x00DC, 0x55, 0x65, 0x00, 0x00}, /* Ü to Ue */
    {0x00DD, 0x59, 0x00, 0x00, 0x00}, /* Ý to Y */
    {0x00DE, 0x54, 0x68, 0x00, 0x00}, /* Þ to Th */
    {0x00DF, 0x73, 0x73, 0x00, 0x00}, /* ß to ss */
    {0x00E0, 0x61, 0x00, 0x00, 0x00}, /* à to a */
    {0x00E1, 0x61, 0x00, 0x00, 0x00}, /* á to a */
    {0x00E2, 0x61, 0x00, 0x00, 0x00}, /* â to a */
    {0x00E3, 0x61, 0x00, 0x00, 0x00}, /* ã to a */
    {0x00E4, 0x61, 0x65, 0x00, 0x00}, /* ä to ae */
    {0x00E5, 0x61, 0x61, 0x00, 0x00}, /* å to aa */
    {0x00E6, 0x61, 0x65, 0x00, 0x00}, /* æ to ae */
    {0x00E7, 0x63, 0x00, 0x00, 0x00}, /* ç to c */
    {0x00E8, 0x65, 0x00, 0x00, 0x00}, /* è to e */
    {0x00E9, 0x65, 0x00, 0x00, 0x00}, /* é to e */
    {0x00EA, 0x65, 0x00, 0x00, 0x00}, /* ê to e */
    {0x00EB, 0x65, 0x00, 0x00, 0x00}, /* ë to e */
    {0x00EC, 0x69, 0x00, 0x00, 0x00}, /* ì to i */
    {0x00ED, 0x69, 0x00, 0x00, 0x00}, /* í to i */
    {0x00EE, 0x69, 0x00, 0x00, 0x00}, /* î to i */
    {0x00EF, 0x69, 0x00, 0x00, 0x00}, /* ï to i */
    {0x00F0, 0x64, 0x00, 0x00, 0x00}, /* ð to d */
    {0x00F1, 0x6E, 0x00, 0x00, 0x00}, /* ñ to n */
    {0x00F2, 0x6F, 0x00, 0x00, 0x00}, /* ò to o */
    {0x00F3, 0x6F, 0x00, 0x00, 0x00}, /* ó to o */
    {0x00F4, 0x6F, 0x00, 0x00, 0x00}, /* ô to o */
    {0x00F5, 0x6F, 0x00, 0x00, 0x00}, /* õ to o */
    {0x00F6, 0x6F, 0x65, 0x00, 0x00}, /* ö to oe */
    {0x00F7, 0x3A, 0x00, 0x00, 0x00}, /* ÷ to : */
    {0x00F8, 0x6F, 0x00, 0x00, 0x00}, /* ø to o */
    {0x00F9, 0x75, 0x00, 0x00, 0x00}, /* ù to u */
    {0x00FA, 0x75, 0x00, 0x00, 0x00}, /* ú to u */
    {0x00FB, 0x75, 0x00, 0x00, 0x00}, /* û to u */
    {0x00FC, 0x75, 0x65, 0x00, 0x00}, /* ü to ue */
    {0x00FD, 0x79, 0x00, 0x00, 0x00}, /* ý to y */
    {0x00FE, 0x74, 0x68, 0x00, 0x00}, /* þ to th */
    {0x00FF, 0x79, 0x00, 0x00, 0x00}, /* ÿ to y */
    {0x0100, 0x41, 0x00, 0x00, 0x00}, /* Ā to A */
    {0x0101, 0x61, 0x00, 0x00, 0x00}, /* ā to a */
    {0x0102, 0x41, 0x00, 0x00, 0x00}, /* Ă to A */
    {0x0103, 0x61, 0x00, 0x00, 0x00}, /* ă to a */
    {0x0104, 0x41, 0x00, 0x00, 0x00}, /* Ą to A */
    {0x0105, 0x61, 0x00, 0x00, 0x00}, /* ą to a */
    {0x0106, 0x43, 0x00, 0x00, 0x00}, /* Ć to C */
    {0x0107, 0x63, 0x00, 0x00, 0x00}, /* ć to c */
    {0x0108, 0x43, 0x68, 0x00, 0x00}, /* Ĉ to Ch */
    {0x0109, 0x63, 0x68, 0x00, 0x00}, /* ĉ to ch */
    {0x010A, 0x43, 0x00, 0x00, 0x00}, /* Ċ to C */
    {0x010B, 0x63, 0x00, 0x00, 0x00}, /* ċ to c */
    {0x010C, 0x43, 0x00, 0x00, 0x00}, /* Č to C */
    {0x010D, 0x63, 0x00, 0x00, 0x00}, /* č to c */
    {0x010E, 0x44, 0x00, 0x00, 0x00}, /* Ď to D */
    {0x010F, 0x64, 0x00, 0x00, 0x00}, /* ď to d */
    {0x0110, 0x44, 0x00, 0x00, 0x00}, /* Đ to D */
    {0x0111, 0x64, 0x00, 0x00, 0x00}, /* đ to d */
    {0x0112, 0x45, 0x00, 0x00, 0x00}, /* Ē to E */
    {0x0113, 0x65, 0x00, 0x00, 0x00}, /* ē to e */
    {0x0114, 0x45, 0x00, 0x00, 0x00}, /* Ĕ to E */
    {0x0115, 0x65, 0x00, 0x00, 0x00}, /* ĕ to e */
    {0x0116, 0x45, 0x00, 0x00, 0x00}, /* Ė to E */
    {0x0117, 0x65, 0x00, 0x00, 0x00}, /* ė to e */
    {0x0118, 0x45, 0x00, 0x00, 0x00}, /* Ę to E */
    {0x0119, 0x65, 0x00, 0x00, 0x00}, /* ę to e */
    {0x011A, 0x45, 0x00, 0x00, 0x00}, /* Ě to E */
    {0x011B, 0x65, 0x00, 0x00, 0x00}, /* ě to e */
    {0x011C, 0x47, 0x68, 0x00, 0x00}, /* Ĝ to Gh */
    {0x011D, 0x67, 0x68, 0x00, 0x00}, /* ĝ to gh */
    {0x011E, 0x47, 0x00, 0x00, 0x00}, /* Ğ to G */
    {0x011F, 0x67, 0x00, 0x00, 0x00}, /* ğ to g */
    {0x0120, 0x47, 0x00, 0x00, 0x00}, /* Ġ to G */
    {0x0121, 0x67, 0x00, 0x00, 0x00}, /* ġ to g */
    {0x0122, 0x47, 0x00, 0x00, 0x00}, /* Ģ to G */
    {0x0123, 0x67, 0x00, 0x00, 0x00}, /* ģ to g */
    {0x0124, 0x48, 0x68, 0x00, 0x00}, /* Ĥ to Hh */
    {0x0125, 0x68, 0x68, 0x00, 0x00}, /* ĥ to hh */
    {0x0126, 0x48, 0x00, 0x00, 0x00}, /* Ħ to H */
    {0x0127, 0x68, 0x00, 0x00, 0x00}, /* ħ to h */
    {0x0128, 0x49, 0x00, 0x00, 0x00}, /* Ĩ to I */
    {0x0129, 0x69, 0x00, 0x00, 0x00}, /* ĩ to i */
    {0x012A, 0x49, 0x00, 0x00, 0x00}, /* Ī to I */
    {0x012B, 0x69, 0x00, 0x00, 0x00}, /* ī to i */
    {0x012C, 0x49, 0x00, 0x00, 0x00}, /* Ĭ to I */
    {0x012D, 0x69, 0x00, 0x00, 0x00}, /* ĭ to i */
    {0x012E, 0x49, 0x00, 0x00, 0x00}, /* Į to I */
    {0x012F, 0x69, 0x00, 0x00, 0x00}, /* į to i */
    {0x0130, 0x49, 0x00, 0x00, 0x00}, /* İ to I */
    {0x0131, 0x69, 0x00, 0x00, 0x00}, /* ı to i */
    {0x0132, 0x49, 0x4A, 0x00, 0x00}, /* Ĳ to IJ */
    {0x0133, 0x69, 0x6A, 0x00, 0x00}, /* ĳ to ij */
    {0x0134, 0x4A, 0x68, 0x00, 0x00}, /* Ĵ to Jh */
    {0x0135, 0x6A, 0x68, 0x00, 0x00}, /* ĵ to jh */
    {0x0136, 0x4B, 0x00, 0x00, 0x00}, /* Ķ to K */
    {0x0137, 0x6B, 0x00, 0x00, 0x00}, /* ķ to k */
    {0x0138, 0x6B, 0x00, 0x00, 0x00}, /* ĸ to k */
    {0x0139, 0x4C, 0x00, 0x00, 0x00}, /* Ĺ to L */
    {0x013A, 0x6C, 0x00, 0x00, 0x00}, /* ĺ to l */
    {0x013B, 0x4C, 0x00, 0x00, 0x00}, /* Ļ to L */
    {0x013C, 0x6C, 0x00, 0x00, 0x00}, /* ļ to l */
    {0x013D, 0x4C, 0x00, 0x00, 0x00}, /* Ľ to L */
    {0x013E, 0x6C, 0x00, 0x00, 0x00}, /* ľ to l */
    {0x013F, 0x4C, 0x2E, 0x00, 0x00}, /* Ŀ to L. */
    {0x0140, 0x6C, 0x2E, 0x00, 0x00}, /* ŀ to l. */
    {0x0141, 0x4C, 0x00, 0x00, 0x00}, /* Ł to L */
    {0x0142, 0x6C, 0x00, 0x00, 0x00}, /* ł to l */
    {0x0143, 0x4E, 0x00, 0x00, 0x00}, /* Ń to N */
    {0x0144, 0x6E, 0x00, 0x00, 0x00}, /* ń to n */
    {0x0145, 0x4E, 0x00, 0x00, 0x00}, /* Ņ to N */
    {0x0146, 0x6E, 0x00, 0x00, 0x00}, /* ņ to n */
    {0x0147, 0x4E, 0x00, 0x00, 0x00}, /* Ň to N */
    {0x0148, 0x6E, 0x00, 0x00, 0x00}, /* ň to n */
    {0x0149, 0x27, 0x6E, 0x00, 0x00}, /* ŉ to 'n */
    {0x014A, 0x4E, 0x47, 0x00, 0x00}, /* Ŋ to NG */
    {0x014B, 0x6E, 0x67, 0x00, 0x00}, /* ŋ to ng */
    {0x014C, 0x4F, 0x00, 0x00, 0x00}, /* Ō to O */
    {0x014D, 0x6F, 0x00, 0x00, 0x00}, /* ō to o */
    {0x014E, 0x4F, 0x00, 0x00, 0x00}, /* Ŏ to O */
    {0x014F, 0x6F, 0x00, 0x00, 0x00}, /* ŏ to o */
    {0x0150, 0x4F, 0x00, 0x00, 0x00}, /* Ő to O */
    {0x0151, 0x6F, 0x00, 0x00, 0x00}, /* ő to o */
    {0x0152, 0x4F, 0x45, 0x00, 0x00}, /* Œ to OE */
    {0x0153, 0x6F, 0x65, 0x00, 0x00}, /* œ to oe */
    {0x0154, 0x52, 0x00, 0x00, 0x00}, /* Ŕ to R */
    {0x0155, 0x72, 0x00, 0x00, 0x00}, /* ŕ to r */
    {0x0156, 0x52, 0x00, 0x00, 0x00}, /* Ŗ to R */
    {0x0157, 0x72, 0x00, 0x00, 0x00}, /* ŗ to r */
    {0x0158, 0x52, 0x00, 0x00, 0x00}, /* Ř to R */
    {0x0159, 0x72, 0x00, 0x00, 0x00}, /* ř to r */
    {0x015A, 0x53, 0x00, 0x00, 0x00}, /* Ś to S */
    {0x015B, 0x73, 0x00, 0x00, 0x00}, /* ś to s */
    {0x015C, 0x53, 0x68, 0x00, 0x00}, /* Ŝ to Sh */
    {0x015D, 0x73, 0x68, 0x00, 0x00}, /* ŝ to sh */
    {0x015E, 0x53, 0x00, 0x00, 0x00}, /* Ş to S */
    {0x015F, 0x73, 0x00, 0x00, 0x00}, /* ş to s */
    {0x0160, 0x53, 0x00, 0x00, 0x00}, /* Š to S */
    {0x0161, 0x73, 0x00, 0x00, 0x00}, /* š to s */
    {0x0162, 0x54, 0x00, 0x00, 0x00}, /* Ţ to T */
    {0x0163, 0x74, 0x00, 0x00, 0x00}, /* ţ to t */
    {0x0164, 0x54, 0x00, 0x00, 0x00}, /* Ť to T */
    {0x0165, 0x74, 0x00, 0x00, 0x00}, /* ť to t */
    {0x0166, 0x54, 0x00, 0x00, 0x00}, /* Ŧ to T */
    {0x0167, 0x74, 0x00, 0x00, 0x00}, /* ŧ to t */
    {0x0168, 0x55, 0x00, 0x00, 0x00}, /* Ũ to U */
    {0x0169, 0x75, 0x00, 0x00, 0x00}, /* ũ to u */
    {0x016A, 0x55, 0x00, 0x00, 0x00}, /* Ū to U */
    {0x016B, 0x75, 0x00, 0x00, 0x00}, /* ū to u */
    {0x016C, 0x55, 0x00, 0x00, 0x00}, /* Ŭ to U */
    {0x016D, 0x75, 0x00, 0x00, 0x00}, /* ŭ to u */
    {0x016E, 0x55, 0x00, 0x00, 0x00}, /* Ů to U */
    {0x016F, 0x75, 0x00, 0x00, 0x00}, /* ů to u */
    {0x0170, 0x55, 0x00, 0x00, 0x00}, /* Ű to U */
    {0x0171, 0x75, 0x00, 0x00, 0x00}, /* ű to u */
    {0x0172, 0x55, 0x00, 0x00, 0x00}, /* Ų to U */
    {0x0173, 0x75, 0x00, 0x00, 0x00}, /* ų to u */
    {0x0174, 0x57, 0x00, 0x00, 0x00}, /* Ŵ to W */
    {0x0175, 0x77, 0x00, 0x00, 0x00}, /* ŵ to w */
    {0x0176, 0x59, 0x00, 0x00, 0x00}, /* Ŷ to Y */
    {0x0177, 0x79, 0x00, 0x00, 0x00}, /* ŷ to y */
    {0x0178, 0x59, 0x00, 0x00, 0x00}, /* Ÿ to Y */
    {0x0179, 0x5A, 0x00, 0x00, 0x00}, /* Ź to Z */
    {0x017A, 0x7A, 0x00, 0x00, 0x00}, /* ź to z */
    {0x017B, 0x5A, 0x00, 0x00, 0x00}, /* Ż to Z */
    {0x017C, 0x7A, 0x00, 0x00, 0x00}, /* ż to z */
    {0x017D, 0x5A, 0x00, 0x00, 0x00}, /* Ž to Z */
    {0x017E, 0x7A, 0x00, 0x00, 0x00}, /* ž to z */
    {0x017F, 0x73, 0x00, 0x00, 0x00}, /* ſ to s */
    {0x0192, 0x66, 0x00, 0x00, 0x00}, /* ƒ to f */
    {0x0218, 0x53, 0x00, 0x00, 0x00}, /* Ș to S */
    {0x0219, 0x73, 0x00, 0x00, 0x00}, /* ș to s */
    {0x021A, 0x54, 0x00, 0x00, 0x00}, /* Ț to T */
    {0x021B, 0x74, 0x00, 0x00, 0x00}, /* ț to t */
    {0x0386, 0x41, 0x00, 0x00, 0x00}, /* Ά to A */
    {0x0388, 0x45, 0x00, 0x00, 0x00}, /* Έ to E */
    {0x0389, 0x49, 0x00, 0x00, 0x00}, /* Ή to I */
    {0x038A, 0x49, 0x00, 0x00, 0x00}, /* Ί to I */
    {0x038C, 0x4f, 0x00, 0x00, 0x00}, /* Ό to O */
    {0x038E, 0x59, 0x00, 0x00, 0x00}, /* Ύ to Y */
    {0x038F, 0x4f, 0x00, 0x00, 0x00}, /* Ώ to O */
    {0x0390, 0x69, 0x00, 0x00, 0x00}, /* ΐ to i */
    {0x0391, 0x41, 0x00, 0x00, 0x00}, /* Α to A */
    {0x0392, 0x42, 0x00, 0x00, 0x00}, /* Β to B */
    {0x0393, 0x47, 0x00, 0x00, 0x00}, /* Γ to G */
    {0x0394, 0x44, 0x00, 0x00, 0x00}, /* Δ to D */
    {0x0395, 0x45, 0x00, 0x00, 0x00}, /* Ε to E */
    {0x0396, 0x5a, 0x00, 0x00, 0x00}, /* Ζ to Z */
    {0x0397, 0x49, 0x00, 0x00, 0x00}, /* Η to I */
    {0x0398, 0x54, 0x68, 0x00, 0x00}, /* Θ to Th */
    {0x0399, 0x49, 0x00, 0x00, 0x00}, /* Ι to I */
    {0x039A, 0x4b, 0x00, 0x00, 0x00}, /* Κ to K */
    {0x039B, 0x4c, 0x00, 0x00, 0x00}, /* Λ to L */
    {0x039C, 0x4d, 0x00, 0x00, 0x00}, /* Μ to M */
    {0x039D, 0x4e, 0x00, 0x00, 0x00}, /* Ν to N */
    {0x039E, 0x58, 0x00, 0x00, 0x00}, /* Ξ to X */
    {0x039F, 0x4f, 0x00, 0x00, 0x00}, /* Ο to O */
    {0x03A0, 0x50, 0x00, 0x00, 0x00}, /* Π to P */
    {0x03A1, 0x52, 0x00, 0x00, 0x00}, /* Ρ to R */
    {0x03A3, 0x53, 0x00, 0x00, 0x00}, /* Σ to S */
    {0x03A4, 0x54, 0x00, 0x00, 0x00}, /* Τ to T */
    {0x03A5, 0x59, 0x00, 0x00, 0x00}, /* Υ to Y */
    {0x03A6, 0x46, 0x00, 0x00, 0x00}, /* Φ to F */
    {0x03A7, 0x43, 0x68, 0x00, 0x00}, /* Χ to Ch */
    {0x03A8, 0x50, 0x73, 0x00, 0x00}, /* Ψ to Ps */
    {0x03A9, 0x4f, 0x00, 0x00, 0x00}, /* Ω to O */
    {0x03AA, 0x49, 0x00, 0x00, 0x00}, /* Ϊ to I */
    {0x03AB, 0x59, 0x00, 0x00, 0x00}, /* Ϋ to Y */
    {0x03AC, 0x61, 0x00, 0x00, 0x00}, /* ά to a */
    {0x03AD, 0x65, 0x00, 0x00, 0x00}, /* έ to e */
    {0x03AE, 0x69, 0x00, 0x00, 0x00}, /* ή to i */
    {0x03AF, 0x69, 0x00, 0x00, 0x00}, /* ί to i */
    {0x03B1, 0x61, 0x00, 0x00, 0x00}, /* α to a */
    {0x03B2, 0x62, 0x00, 0x00, 0x00}, /* β to b */
    {0x03B3, 0x67, 0x00, 0x00, 0x00}, /* γ to g */
    {0x03B4, 0x64, 0x00, 0x00, 0x00}, /* δ to d */
    {0x03B5, 0x65, 0x00, 0x00, 0x00}, /* ε to e */
    {0x03B6, 0x7a, 0x00, 0x00, 0x00}, /* ζ to z */
    {0x03B7, 0x69, 0x00, 0x00, 0x00}, /* η to i */
    {0x03B8, 0x74, 0x68, 0x00, 0x00}, /* θ to th */
    {0x03B9, 0x69, 0x00, 0x00, 0x00}, /* ι to i */
    {0x03BA, 0x6b, 0x00, 0x00, 0x00}, /* κ to k */
    {0x03BB, 0x6c, 0x00, 0x00, 0x00}, /* λ to l */
    {0x03BC, 0x6d, 0x00, 0x00, 0x00}, /* μ to m */
    {0x03BD, 0x6e, 0x00, 0x00, 0x00}, /* ν to n */
    {0x03BE, 0x78, 0x00, 0x00, 0x00}, /* ξ to x */
    {0x03BF, 0x6f, 0x00, 0x00, 0x00}, /* ο to o */
    {0x03C0, 0x70, 0x00, 0x00, 0x00}, /* π to p */
    {0x03C1, 0x72, 0x00, 0x00, 0x00}, /* ρ to r */
    {0x03C3, 0x73, 0x00, 0x00, 0x00}, /* σ to s */
    {0x03C4, 0x74, 0x00, 0x00, 0x00}, /* τ to t */
    {0x03C5, 0x79, 0x00, 0x00, 0x00}, /* υ to y */
    {0x03C6, 0x66, 0x00, 0x00, 0x00}, /* φ to f */
    {0x03C7, 0x63, 0x68, 0x00, 0x00}, /* χ to ch */
    {0x03C8, 0x70, 0x73, 0x00, 0x00}, /* ψ to ps */
    {0x03C9, 0x6f, 0x00, 0x00, 0x00}, /* ω to o */
    {0x03CA, 0x69, 0x00, 0x00, 0x00}, /* ϊ to i */
    {0x03CB, 0x79, 0x00, 0x00, 0x00}, /* ϋ to y */
    {0x03CC, 0x6f, 0x00, 0x00, 0x00}, /* ό to o */
    {0x03CD, 0x79, 0x00, 0x00, 0x00}, /* ύ to y */
    {0x03CE, 0x69, 0x00, 0x00, 0x00}, /* ώ to i */
    {0x0400, 0x45, 0x00, 0x00, 0x00}, /* Ѐ to E */
    {0x0401, 0x45, 0x00, 0x00, 0x00}, /* Ё to E */
    {0x0402, 0x44, 0x00, 0x00, 0x00}, /* Ђ to D */
    {0x0403, 0x47, 0x00, 0x00, 0x00}, /* Ѓ to G */
    {0x0404, 0x45, 0x00, 0x00, 0x00}, /* Є to E */
    {0x0405, 0x5a, 0x00, 0x00, 0x00}, /* Ѕ to Z */
    {0x0406, 0x49, 0x00, 0x00, 0x00}, /* І to I */
    {0x0407, 0x49, 0x00, 0x00, 0x00}, /* Ї to I */
    {0x0408, 0x4a, 0x00, 0x00, 0x00}, /* Ј to J */
    {0x0409, 0x49, 0x00, 0x00, 0x00}, /* Љ to I */
    {0x040A, 0x4e, 0x00, 0x00, 0x00}, /* Њ to N */
    {0x040B, 0x44, 0x00, 0x00, 0x00}, /* Ћ to D */
    {0x040C, 0x4b, 0x00, 0x00, 0x00}, /* Ќ to K */
    {0x040D, 0x49, 0x00, 0x00, 0x00}, /* Ѝ to I */
    {0x040E, 0x55, 0x00, 0x00, 0x00}, /* Ў to U */
    {0x040F, 0x44, 0x00, 0x00, 0x00}, /* Џ to D */
    {0x0410, 0x41, 0x00, 0x00, 0x00}, /* А to A */
    {0x0411, 0x42, 0x00, 0x00, 0x00}, /* Б to B */
    {0x0412, 0x56, 0x00, 0x00, 0x00}, /* В to V */
    {0x0413, 0x47, 0x00, 0x00, 0x00}, /* Г to G */
    {0x0414, 0x44, 0x00, 0x00, 0x00}, /* Д to D */
    {0x0415, 0x45, 0x00, 0x00, 0x00}, /* Е to E */
    {0x0416, 0x5a, 0x68, 0x00, 0x00}, /* Ж to Zh */
    {0x0417, 0x5a, 0x00, 0x00, 0x00}, /* З to Z */
    {0x0418, 0x49, 0x00, 0x00, 0x00}, /* И to I */
    {0x0419, 0x49, 0x00, 0x00, 0x00}, /* Й to I */
    {0x041A, 0x4b, 0x00, 0x00, 0x00}, /* К to K */
    {0x041B, 0x4c, 0x00, 0x00, 0x00}, /* Л to L */
    {0x041C, 0x4d, 0x00, 0x00, 0x00}, /* М to M */
    {0x041D, 0x4e, 0x00, 0x00, 0x00}, /* Н to N */
    {0x041E, 0x4f, 0x00, 0x00, 0x00}, /* О to O */
    {0x041F, 0x50, 0x00, 0x00, 0x00}, /* П to P */
    {0x0420, 0x52, 0x00, 0x00, 0x00}, /* Р to R */
    {0x0421, 0x53, 0x00, 0x00, 0x00}, /* С to S */
    {0x0422, 0x54, 0x00, 0x00, 0x00}, /* Т to T */
    {0x0423, 0x55, 0x00, 0x00, 0x00}, /* У to U */
    {0x0424, 0x46, 0x00, 0x00, 0x00}, /* Ф to F */
    {0x0425, 0x4b, 0x68, 0x00, 0x00}, /* Х to Kh */
    {0x0426, 0x54, 0x63, 0x00, 0x00}, /* Ц to Tc */
    {0x0427, 0x43, 0x68, 0x00, 0x00}, /* Ч to Ch */
    {0x0428, 0x53, 0x68, 0x00, 0x00}, /* Ш to Sh */
    {0x0429, 0x53, 0x68, 0x63, 0x68}, /* Щ to Shch */
    {0x042A, 0x61, 0x00, 0x00, 0x00}, /*  to A */
    {0x042B, 0x59, 0x00, 0x00, 0x00}, /* Ы to Y */
    {0x042C, 0x59, 0x00, 0x00, 0x00}, /*  to Y */
    {0x042D, 0x45, 0x00, 0x00, 0x00}, /* Э to E */
    {0x042E, 0x49, 0x75, 0x00, 0x00}, /* Ю to Iu */
    {0x042F, 0x49, 0x61, 0x00, 0x00}, /* Я to Ia */
    {0x0430, 0x61, 0x00, 0x00, 0x00}, /* а to a */
    {0x0431, 0x62, 0x00, 0x00, 0x00}, /* б to b */
    {0x0432, 0x76, 0x00, 0x00, 0x00}, /* в to v */
    {0x0433, 0x67, 0x00, 0x00, 0x00}, /* г to g */
    {0x0434, 0x64, 0x00, 0x00, 0x00}, /* д to d */
    {0x0435, 0x65, 0x00, 0x00, 0x00}, /* е to e */
    {0x0436, 0x7a, 0x68, 0x00, 0x00}, /* ж to zh */
    {0x0437, 0x7a, 0x00, 0x00, 0x00}, /* з to z */
    {0x0438, 0x69, 0x00, 0x00, 0x00}, /* и to i */
    {0x0439, 0x69, 0x00, 0x00, 0x00}, /* й to i */
    {0x043A, 0x6b, 0x00, 0x00, 0x00}, /* к to k */
    {0x043B, 0x6c, 0x00, 0x00, 0x00}, /* л to l */
    {0x043C, 0x6d, 0x00, 0x00, 0x00}, /* м to m */
    {0x043D, 0x6e, 0x00, 0x00, 0x00}, /* н to n */
    {0x043E, 0x6f, 0x00, 0x00, 0x00}, /* о to o */
    {0x043F, 0x70, 0x00, 0x00, 0x00}, /* п to p */
    {0x0440, 0x72, 0x00, 0x00, 0x00}, /* р to r */
    {0x0441, 0x73, 0x00, 0x00, 0x00}, /* с to s */
    {0x0442, 0x74, 0x00, 0x00, 0x00}, /* т to t */
    {0x0443, 0x75, 0x00, 0x00, 0x00}, /* у to u */
    {0x0444, 0x66, 0x00, 0x00, 0x00}, /* ф to f */
    {0x0445, 0x6b, 0x68, 0x00, 0x00}, /* х to kh */
    {0x0446, 0x74, 0x63, 0x00, 0x00}, /* ц to tc */
    {0x0447, 0x63, 0x68, 0x00, 0x00}, /* ч to ch */
    {0x0448, 0x73, 0x68, 0x00, 0x00}, /* ш to sh */
    {0x0449, 0x73, 0x68, 0x63, 0x68}, /* щ to shch */
    {0x044A, 0x61, 0x00, 0x00, 0x00}, /*  to a */
    {0x044B, 0x79, 0x00, 0x00, 0x00}, /* ы to y */
    {0x044C, 0x79, 0x00, 0x00, 0x00}, /*  to y */
    {0x044D, 0x65, 0x00, 0x00, 0x00}, /* э to e */
    {0x044E, 0x69, 0x75, 0x00, 0x00}, /* ю to iu */
    {0x044F, 0x69, 0x61, 0x00, 0x00}, /* я to ia */
    {0x0450, 0x65, 0x00, 0x00, 0x00}, /* ѐ to e */
    {0x0451, 0x65, 0x00, 0x00, 0x00}, /* ё to e */
    {0x0452, 0x64, 0x00, 0x00, 0x00}, /* ђ to d */
    {0x0453, 0x67, 0x00, 0x00, 0x00}, /* ѓ to g */
    {0x0454, 0x65, 0x00, 0x00, 0x00}, /* є to e */
    {0x0455, 0x7a, 0x00, 0x00, 0x00}, /* ѕ to z */
    {0x0456, 0x69, 0x00, 0x00, 0x00}, /* і to i */
    {0x0457, 0x69, 0x00, 0x00, 0x00}, /* ї to i */
    {0x0458, 0x6a, 0x00, 0x00, 0x00}, /* ј to j */
    {0x0459, 0x69, 0x00, 0x00, 0x00}, /* љ to i */
    {0x045A, 0x6e, 0x00, 0x00, 0x00}, /* њ to n */
    {0x045B, 0x64, 0x00, 0x00, 0x00}, /* ћ to d */
    {0x045C, 0x6b, 0x00, 0x00, 0x00}, /* ќ to k */
    {0x045D, 0x69, 0x00, 0x00, 0x00}, /* ѝ to i */
    {0x045E, 0x75, 0x00, 0x00, 0x00}, /* ў to u */
    {0x045F, 0x64, 0x00, 0x00, 0x00}, /* џ to d */
    {0x1E02, 0x42, 0x00, 0x00, 0x00}, /* Ḃ to B */
    {0x1E03, 0x62, 0x00, 0x00, 0x00}, /* ḃ to b */
    {0x1E0A, 0x44, 0x00, 0x00, 0x00}, /* Ḋ to D */
    {0x1E0B, 0x64, 0x00, 0x00, 0x00}, /* ḋ to d */
    {0x1E1E, 0x46, 0x00, 0x00, 0x00}, /* Ḟ to F */
    {0x1E1F, 0x66, 0x00, 0x00, 0x00}, /* ḟ to f */
    {0x1E40, 0x4D, 0x00, 0x00, 0x00}, /* Ṁ to M */
    {0x1E41, 0x6D, 0x00, 0x00, 0x00}, /* ṁ to m */
    {0x1E56, 0x50, 0x00, 0x00, 0x00}, /* Ṗ to P */
    {0x1E57, 0x70, 0x00, 0x00, 0x00}, /* ṗ to p */
    {0x1E60, 0x53, 0x00, 0x00, 0x00}, /* Ṡ to S */
    {0x1E61, 0x73, 0x00, 0x00, 0x00}, /* ṡ to s */
    {0x1E6A, 0x54, 0x00, 0x00, 0x00}, /* Ṫ to T */
    {0x1E6B, 0x74, 0x00, 0x00, 0x00}, /* ṫ to t */
    {0x1E80, 0x57, 0x00, 0x00, 0x00}, /* Ẁ to W */
    {0x1E81, 0x77, 0x00, 0x00, 0x00}, /* ẁ to w */
    {0x1E82, 0x57, 0x00, 0x00, 0x00}, /* Ẃ to W */
    {0x1E83, 0x77, 0x00, 0x00, 0x00}, /* ẃ to w */
    {0x1E84, 0x57, 0x00, 0x00, 0x00}, /* Ẅ to W */
    {0x1E85, 0x77, 0x00, 0x00, 0x00}, /* ẅ to w */
    {0x1EF2, 0x59, 0x00, 0x00, 0x00}, /* Ỳ to Y */
    {0x1EF3, 0x79, 0x00, 0x00, 0x00}, /* ỳ to y */
    {0xFB00, 0x66, 0x66, 0x00, 0x00}, /* ﬀ to ff */
    {0xFB01, 0x66, 0x69, 0x00, 0x00}, /* ﬁ to fi */
    {0xFB02, 0x66, 0x6C, 0x00, 0x00}, /* ﬂ to fl */
    {0xFB05, 0x73, 0x74, 0x00, 0x00}, /* ﬅ to st */
    {0xFB06, 0x73, 0x74, 0x00, 0x00}, /* ﬆ to st */
};

static const Transliteration* spellfixFindTranslit(int c, int* pxTop) {
    *pxTop = (sizeof(translit) / sizeof(translit[0])) - 1;
    return translit;
}

/*
** Convert the input string from UTF-8 into pure ASCII by converting
** all non-ASCII characters to some combination of characters in the
** ASCII subset.
**
** The returned string might contain more characters than the input.
**
** Space to hold the returned string comes from sqlite3_malloc() and
** should be freed by the caller.
*/
unsigned char* transliterate(const unsigned char* zIn, int nIn) {
    unsigned char* zOut = malloc(nIn * 4 + 1);
    int c, sz, nOut;
    if (zOut == 0)
        return 0;
    nOut = 0;
    while (nIn > 0) {
        c = utf8Read(zIn, nIn, &sz);
        zIn += sz;
        nIn -= sz;
        if (c <= 127) {
            zOut[nOut++] = (unsigned char)c;
        } else {
            int xTop, xBtm, x;
            const Transliteration* tbl = spellfixFindTranslit(c, &xTop);
            xBtm = 0;
            while (xTop >= xBtm) {
                x = (xTop + xBtm) / 2;
                if (tbl[x].cFrom == c) {
                    zOut[nOut++] = tbl[x].cTo0;
                    if (tbl[x].cTo1) {
                        zOut[nOut++] = tbl[x].cTo1;
                        if (tbl[x].cTo2) {
                            zOut[nOut++] = tbl[x].cTo2;
                            if (tbl[x].cTo3) {
                                zOut[nOut++] = tbl[x].cTo3;
                            }
                        }
                    }
                    c = 0;
                    break;
                } else if (tbl[x].cFrom > c) {
                    xTop = x - 1;
                } else {
                    xBtm = x + 1;
                }
            }
            if (c)
                zOut[nOut++] = '?';
        }
    }
    zOut[nOut] = 0;
    return zOut;
}

/*
** Return the number of characters in the shortest prefix of the input
** string that transliterates to an ASCII string nTrans bytes or longer.
** Or, if the transliteration of the input string is less than nTrans
** bytes in size, return the number of characters in the input string.
*/
int translen_to_charlen(const char* zIn, int nIn, int nTrans) {
    int i, c, sz, nOut;
    int nChar;

    i = nOut = 0;
    for (nChar = 0; i < nIn && nOut < nTrans; nChar++) {
        c = utf8Read((const unsigned char*)&zIn[i], nIn - i, &sz);
        i += sz;

        nOut++;
        if (c >= 128) {
            int xTop, xBtm, x;
            const Transliteration* tbl = spellfixFindTranslit(c, &xTop);
            xBtm = 0;
            while (xTop >= xBtm) {
                x = (xTop + xBtm) / 2;
                if (tbl[x].cFrom == c) {
                    if (tbl[x].cTo1) {
                        nOut++;
                        if (tbl[x].cTo2) {
                            nOut++;
                            if (tbl[x].cTo3) {
                                nOut++;
                            }
                        }
                    }
                    break;
                } else if (tbl[x].cFrom > c) {
                    xTop = x - 1;
                } else {
                    xBtm = x + 1;
                }
            }
        }
    }

    return nChar;
}

/*
 * Try to determine the dominant script used by the word zIn of length nIn
 * and return its ISO 15924 numeric code.
 */
int script_code(const unsigned char* zIn, int nIn) {
    int c, sz;
    int scriptMask = 0;
    int res;
    int seenDigit = 0;

    while (nIn > 0) {
        c = utf8Read(zIn, nIn, &sz);
        zIn += sz;
        nIn -= sz;
        if (c < 0x02af) {
            if (c >= 0x80 || midClass[c & 0x7f] < CCLASS_DIGIT) {
                scriptMask |= SCRIPT_LATIN;
            } else if (c >= '0' && c <= '9') {
                seenDigit = 1;
            }
        } else if (c >= 0x0400 && c <= 0x04ff) {
            scriptMask |= SCRIPT_CYRILLIC;
        } else if (c >= 0x0386 && c <= 0x03ce) {
            scriptMask |= SCRIPT_GREEK;
        } else if (c >= 0x0590 && c <= 0x05ff) {
            scriptMask |= SCRIPT_HEBREW;
        } else if (c >= 0x0600 && c <= 0x06ff) {
            scriptMask |= SCRIPT_ARABIC;
        }
    }
    if (scriptMask == 0 && seenDigit)
        scriptMask = SCRIPT_LATIN;
    switch (scriptMask) {
        case 0:
            res = 999;
            break;
        case SCRIPT_LATIN:
            res = 215;
            break;
        case SCRIPT_CYRILLIC:
            res = 220;
            break;
        case SCRIPT_GREEK:
            res = 200;
            break;
        case SCRIPT_HEBREW:
            res = 125;
            break;
        case SCRIPT_ARABIC:
            res = 160;
            break;
        default:
            res = 998;
            break;
    }
    return res;
}
