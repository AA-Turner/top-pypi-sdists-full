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


from english.text import first_sentence


def test_first_sentence_of_empty_text():
    assert first_sentence("") == ""


def test_first_sentence_of_complex_text():
    text = ("Bali bombings: U.S. President George W. Bush amongst "
            "many others has condemned the perpetrators of the Bali "
            "car bombing of October 11. The death toll has now risen "
            "to at least 187.")
    assert first_sentence(text) == ("Bali bombings: U.S. President "
                                    "George W. Bush amongst many "
                                    "others has condemned the "
                                    "perpetrators of the Bali car "
                                    "bombing of October 11.")


def test_first_sentence_of_text_with_no_full_stops():
    assert first_sentence("hello") == "hello"
