"""
Implementation of Porter Stemming Algorithm from
https://tartarus.org/martin/PorterStemmer/python.txt

Note: The Python implementation returns different results than the JS
version:
- Stemming "lay" returns "lai" in Python, but "lay" in JS
- Stemming "try" returns "try" in Python, but "tri" in JS


Porter Stemming Algorithm
This is the Porter stemming algorithm, ported to Python from the
version coded up in ANSI C by the author. It may be regarded
as canonical, in that it follows the algorithm presented in

Porter, 1980, An algorithm for suffix stripping, Program, Vol. 14,
no. 3, pp 130-137,

only differing from it at the points marked --DEPARTURE-- below.

The implementation is a flat, stateless translation of the original:
it keeps `j` (the suffix offset) and `k` (end of the stem) as locals
instead of storing them on an instance, which both removes attribute
lookups from the hot path and makes the stemmer thread-safe. Results
are memoized, as stemming the same word repeatedly is common when
 indexing documents and performing searches.

--DEPARTURE-- points preserved from the original:
- "bli" -> "ble" in step2 instead of "abli" -> "able"
- adding "logi" -> "log" in step2

Release 1: January 2001 (Vivake Gupta, v@nano.com)
Further adjustments by Santiago Bruno (bananabruno@gmail.com)
Release 2: July 2008
"""

from lunr.pipeline import Pipeline

_VOWELS = "aeiou"
_S_FINALS = "lsz"
_MISS = object()

_memo = {}


def _cons(word, i):
    """True when word[i] is a consonant."""
    ch = word[i]
    if ch in _VOWELS:
        return False
    if ch != "y":
        return True
    if i == 0:
        return True
    return not _cons(word, i - 1)


def _m(word, j):
    """Number of consonant sequences between 0 and j.

    if c is a consonant sequence and v a vowel sequence, and <..>
    indicates arbitrary presence,

       <c><v>       gives 0
       <c>vc<v>     gives 1
       <c>vcvc<v>   gives 2
       <c>vcvcvc<v> gives 3
       ....
    """
    n = 0
    cons = _cons(word, 0)
    for i in range(1, j + 1):
        is_cons = _cons(word, i)
        if is_cons and not cons:
            n += 1
        cons = is_cons
    return n


def _has_vowel(word, j):
    """True when 0..j contains a vowel."""
    for i in range(j + 1):
        if not _cons(word, i):
            return True
    return False


def _double_consonant(word, j):
    """True when j,(j-1) contain a double consonant."""
    if j < 1 or word[j] != word[j - 1]:
        return False
    return _cons(word, j)


def _cvc(word, i):
    """True when i-2,i-1,i has the form consonant-vowel-consonant and
    the second c is not w, x or y. Used when trying to restore an e at
    the end of a short word, e.g. cav(e), lov(e), hop(e), crim(e), but
    snow, box, tray.
    """
    if i < 2 or not _cons(word, i) or _cons(word, i - 1) or not _cons(word, i - 2):
        return False
    return word[i] not in "wxy"


def _ends(word, s, k):
    """Index of the last character before s if word ends with s (ending
    at k), None otherwise."""
    n = len(s)
    if word[k] != s[n - 1]:
        return None
    if n > k + 1:
        return None
    if word[k - n + 1 : k + 1] != s:
        return None
    return k - n


def _replace_suffix(word, j, s):
    """Replaces the suffix after j (the characters j+1..k) by s and
    returns the new word and k."""
    return word[: j + 1] + s + word[j + len(s) + 1 :], j + len(s)


def stem(word, metadata=None):
    """Stems a word with the Porter stemming algorithm. Words of length
    1 or 2 don't go through the stemming process, although no mention is
    made of this in the published algorithm.
    """
    result = _memo.get(word, _MISS)
    if result is not _MISS:
        return result

    k = len(word) - 1
    j = 0

    if k <= 1:
        result = word
        _memo[word] = result
        return result

    # step1ab: plurals and -ed or -ing. e.g.
    #
    # caresses  ->  caress
    # ponies    ->  poni
    # ties      ->  ti
    # caress    ->  caress
    # cats      ->  cat
    #
    # feed      ->  feed
    # agreed    ->  agree
    # disabled  ->  disable
    #
    # matting   ->  mat
    # mating    ->  mate
    # meeting   ->  meet
    # milling   ->  mill
    # messing   ->  mess
    #
    # meetings  ->  meet
    if word[k] == "s":
        jj = _ends(word, "sses", k)
        if jj is not None:
            j = jj
            k -= 2
        else:
            jj = _ends(word, "ies", k)
            if jj is not None:
                j = jj
                word, k = _replace_suffix(word, j, "i")
            elif word[k - 1] != "s":
                k -= 1

    jj = _ends(word, "eed", k)
    if jj is not None:
        j = jj
        if _m(word, j) > 0:
            k -= 1
    else:
        jj = _ends(word, "ed", k)
        if jj is None:
            jj = _ends(word, "ing", k)
        if jj is not None:
            j = jj
            if _has_vowel(word, j):
                k = j
                jj = _ends(word, "at", k)
                if jj is not None:
                    j = jj
                    word, k = _replace_suffix(word, j, "ate")
                else:
                    jj = _ends(word, "bl", k)
                    if jj is not None:
                        j = jj
                        word, k = _replace_suffix(word, j, "ble")
                    else:
                        jj = _ends(word, "iz", k)
                        if jj is not None:
                            j = jj
                            word, k = _replace_suffix(word, j, "ize")
                        elif _double_consonant(word, k):
                            k -= 1
                            if word[k] in _S_FINALS:
                                k += 1
                        elif _m(word, j) == 1 and _cvc(word, k):
                            word, k = _replace_suffix(word, j, "e")

    # step1c: turns terminal y to i when there is another vowel in the stem
    jj = _ends(word, "y", k)
    if jj is not None:
        j = jj
        if _has_vowel(word, j):
            word = word[:k] + "i" + word[k + 1 :]

    # step2: maps double suffices to single ones, so -ization (= -ize
    # plus -ation) maps to -ize etc., when the string before the suffix
    # gives m() > 0
    ch = word[k - 1]
    if ch == "a":
        jj = _ends(word, "ational", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ate")
        else:
            jj = _ends(word, "tional", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "tion")
    elif ch == "c":
        jj = _ends(word, "enci", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ence")
        else:
            jj = _ends(word, "anci", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "ance")
    elif ch == "e":
        jj = _ends(word, "izer", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ize")
    elif ch == "l":
        jj = _ends(word, "bli", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ble")
        else:
            jj = _ends(word, "alli", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "al")
            else:
                jj = _ends(word, "entli", k)
                if jj is not None:
                    j = jj
                    if _m(word, j) > 0:
                        word, k = _replace_suffix(word, j, "ent")
                else:
                    jj = _ends(word, "eli", k)
                    if jj is not None:
                        j = jj
                        if _m(word, j) > 0:
                            word, k = _replace_suffix(word, j, "e")
                    else:
                        jj = _ends(word, "ousli", k)
                        if jj is not None:
                            j = jj
                            if _m(word, j) > 0:
                                word, k = _replace_suffix(word, j, "ous")
    elif ch == "o":
        jj = _ends(word, "ization", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ize")
        else:
            jj = _ends(word, "ation", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "ate")
            else:
                jj = _ends(word, "ator", k)
                if jj is not None:
                    j = jj
                    if _m(word, j) > 0:
                        word, k = _replace_suffix(word, j, "ate")
    elif ch == "s":
        jj = _ends(word, "alism", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "al")
        else:
            jj = _ends(word, "iveness", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "ive")
            else:
                jj = _ends(word, "fulness", k)
                if jj is not None:
                    j = jj
                    if _m(word, j) > 0:
                        word, k = _replace_suffix(word, j, "ful")
                else:
                    jj = _ends(word, "ousness", k)
                    if jj is not None:
                        j = jj
                        if _m(word, j) > 0:
                            word, k = _replace_suffix(word, j, "ous")
    elif ch == "t":
        jj = _ends(word, "aliti", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "al")
        else:
            jj = _ends(word, "iviti", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "ive")
            else:
                jj = _ends(word, "biliti", k)
                if jj is not None:
                    j = jj
                    if _m(word, j) > 0:
                        word, k = _replace_suffix(word, j, "ble")
    elif ch == "g":
        jj = _ends(word, "logi", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "log")

    # step3: deals with -ic-, -ful, -ness etc., similar strategy to step2
    ch = word[k]
    if ch == "e":
        jj = _ends(word, "icate", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ic")
        else:
            jj = _ends(word, "ative", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "")
            else:
                jj = _ends(word, "alize", k)
                if jj is not None:
                    j = jj
                    if _m(word, j) > 0:
                        word, k = _replace_suffix(word, j, "al")
    elif ch == "i":
        jj = _ends(word, "iciti", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ic")
    elif ch == "l":
        jj = _ends(word, "ical", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "ic")
        else:
            jj = _ends(word, "ful", k)
            if jj is not None:
                j = jj
                if _m(word, j) > 0:
                    word, k = _replace_suffix(word, j, "")
    elif ch == "s":
        jj = _ends(word, "ness", k)
        if jj is not None:
            j = jj
            if _m(word, j) > 0:
                word, k = _replace_suffix(word, j, "")

    # step4: takes off -ant, -ence etc., in context <c>vcvc<v>
    ok = False
    ch = word[k - 1]
    if ch == "a":
        jj = _ends(word, "al", k)
        if jj is not None:
            j = jj
            ok = True
    elif ch == "c":
        jj = _ends(word, "ance", k)
        if jj is not None:
            j = jj
            ok = True
        else:
            jj = _ends(word, "ence", k)
            if jj is not None:
                j = jj
                ok = True
    elif ch == "e":
        jj = _ends(word, "er", k)
        if jj is not None:
            j = jj
            ok = True
    elif ch == "i":
        jj = _ends(word, "ic", k)
        if jj is not None:
            j = jj
            ok = True
    elif ch == "l":
        jj = _ends(word, "able", k)
        if jj is not None:
            j = jj
            ok = True
        else:
            jj = _ends(word, "ible", k)
            if jj is not None:
                j = jj
                ok = True
    elif ch == "n":
        jj = _ends(word, "ant", k)
        if jj is not None:
            j = jj
            ok = True
        else:
            jj = _ends(word, "ement", k)
            if jj is not None:
                j = jj
                ok = True
            else:
                jj = _ends(word, "ment", k)
                if jj is not None:
                    j = jj
                    ok = True
                else:
                    jj = _ends(word, "ent", k)
                    if jj is not None:
                        j = jj
                        ok = True
    elif ch == "o":
        jj = _ends(word, "ion", k)
        if jj is not None:
            j = jj
            if word[j] == "s" or word[j] == "t":
                ok = True
        if not ok:
            jj = _ends(word, "ou", k)
            if jj is not None:
                j = jj
                ok = True
    elif ch == "s":
        jj = _ends(word, "ism", k)
        if jj is not None:
            j = jj
            ok = True
    elif ch == "t":
        jj = _ends(word, "ate", k)
        if jj is not None:
            j = jj
            ok = True
        else:
            jj = _ends(word, "iti", k)
            if jj is not None:
                j = jj
                ok = True
    elif ch == "u":
        jj = _ends(word, "ous", k)
        if jj is not None:
            j = jj
            ok = True
    elif ch == "v":
        jj = _ends(word, "ive", k)
        if jj is not None:
            j = jj
            ok = True
    elif ch == "z":
        jj = _ends(word, "ize", k)
        if jj is not None:
            j = jj
            ok = True
    if ok and _m(word, j) > 1:
        k = j

    # step5: removes a final -e if m() > 1, and changes -ll to -l if m() > 1
    j = k
    if word[k] == "e":
        a = _m(word, j)
        if a > 1 or (a == 1 and not _cvc(word, k - 1)):
            k -= 1
    if word[k] == "l" and _double_consonant(word, k) and _m(word, j) > 1:
        k -= 1

    result = word[: k + 1]
    _memo[word] = result
    return result


class PorterStemmer:
    def stem(self, word, metadata=None):
        return stem(word, metadata)


porter_stemmer = PorterStemmer()


def stemmer(token, i=None, tokens=None):
    """Wrapper around the PorterStemmer for inclusion in pipeline.

    Args:
        language (str): ISO-639-1 code of the language.
        token (lunr.Token): The token to stem.
        i (int): The index of the token in a set.
        tokens (list): A list of tokens representing the set.
    """
    return token.update(porter_stemmer.stem)


Pipeline.register_function(stemmer, "stemmer")
