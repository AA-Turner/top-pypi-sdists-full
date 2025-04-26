#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2020, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from english.casing import Words, iter_words


def test_iter_words_space_precedes_underscore():
    assert list(iter_words("one two_three")) == ["one", "two_three"]


def test_iter_words_space_precedes_hyphen():
    assert list(iter_words("one two-three")) == ["one", "two-three"]


def test_iter_words_underscore_precedes_hyphen():
    assert list(iter_words("one_two-three")) == ["one", "two-three"]


def test_iter_words_hyphenated():
    assert list(iter_words("one-two-three")) == ["one", "two", "three"]


def test_iter_words_no_separators():
    assert list(iter_words("ONE")) == ["ONE"]


def test_iter_words_camel_case():
    assert list(iter_words("oneTwoThree")) == ["one", "Two", "Three"]


def test_lower_case_to_snake_case():
    assert Words("one two three").snake() == "one_two_three"


def test_snake_case_to_upper_case():
    assert Words("one_two_three").upper() == "ONE TWO THREE"


def test_snake_case_to_lower_case():
    assert Words("one_two_three").lower() == "one two three"


def test_snake_case_to_title_case():
    assert Words("one_two_three").title() == "One Two Three"


def test_spaced_to_title_case_with_upper_word():
    assert Words("one Two THREE").title() == "One Two THREE"


def test_snake_case_to_camel_case():
    assert Words("one_two_three").camel() == "oneTwoThree"


def test_snake_case_to_camel_case_with_upper_first():
    assert Words("one_two_three").camel(upper_first=True) == "OneTwoThree"


def test_words_from_tuple():
    assert Words(("one two", "three four")).upper() == "ONE TWO THREE FOUR"
