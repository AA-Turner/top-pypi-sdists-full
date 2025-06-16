# -*- coding: utf-8 -*-
###########################################################
#  Copyright (C) Joel B. Mohler <joel@kiwistrawberry.us>
#
#  Distributed under the terms of The MIT License
###########################################################
"""
Date and string matching functions.
"""

def default_match(t,item):
    return t.lower()[:len(item)] == item.lower()

def fuzzy_match(target,item,match_fucn=None):
    """
    This function matches an item to a target list.  It is expected that the
    'item' comes from user input and we want to accept a 'close-enough' match
    to the target list and validate that there is a unique close-enough match.
    
    If there is no suitable match, None is returned.
    
    :param target:  list of possible matches
    :param item:  item to find in the list
    :param match_fucn:  callable function taking 2 parameters (first from the
        target list, second is item) and returning a boolean if match_fucn is
        None then it will default initial lower-case matching of strings

    The default approach to matching is testing against case-insensitive
    prefixes from the target strings.  This is illustrated in the examples
    below.

    Examples:
    >>> fuzzy_match(['aab','bba','abc'],'aa')
    'aab'
    >>> fuzzy_match(['aab','bba','abc'],'a')  # two strings starting with 'a'.
    Traceback (most recent call last):
    ...
    ValueError: ambiguous match for 'a'
    >>> fuzzy_match(['aab','bba','abc'],'b')
    'bba'
    >>> fuzzy_match(['aab','bba','abc'],'sam')  # no match simply returns None
    """

    if match_fucn is None:
        def default_match(t,item):
            return t.lower()[:len(item)] == item.lower()

        match_fucn = default_match

    candidates = [t for t in target if match_fucn(t,item)]
    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) == 0:
        return None
    else:
        raise ValueError("ambiguous match for '{0}'".format(item))
