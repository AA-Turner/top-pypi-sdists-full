//! An I-Regexp parser using [pest].
//!
//! Refer to `iregexp.pest` and the [pest book], or use [crate::check] to check
//! if a pattern conforms to I-Regexp.
//!
//!
//! [pest]: https://pest.rs/
//! [pest book]: https://pest.rs/book/

// Some of the test cases below are derived from https://github.com/f3ath/iregexp.
// Thanks go to @f3ath and the project's license is included here.
//
// MIT License
//
// Copyright (c) 2023 Alexey
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

use pest_derive::Parser;

#[derive(Parser)]
#[grammar = "iregexp.pest"]
pub struct IRegexp;

#[cfg(test)]
mod tests {
    use super::*;
    use pest::Parser;

    macro_rules! assert_valid {
        ($($name:ident: $value:expr,)*) => {
            mod valid {
                use super::*;
                $(
                    #[test]
                    fn $name() {
                        assert!(IRegexp::parse(Rule::pattern, $value).is_ok());
                    }
                )*
            }
        }
    }

    macro_rules! assert_invalid {
        ($($name:ident: $value:expr,)*) => {
            mod invalid {
                use super::*;
                $(
                    #[test]
                    fn $name() {
                        assert!(IRegexp::parse(Rule::pattern, $value).is_err());
                    }
                )*
            }
        }
    }

    assert_valid! {
        dot: r"a.b",
        char_class_expr: r"[0-9]",
        branch: r"foo|bar",
        range_quantifier_exact: r"[ab]{3}",
        range_quantifier: r"[ab]{3,5}",
        range_quantifier_open_ended: r"[ab]{3,}",
        char_class_expr_negation: r"[^ab]",
        unicode_character_category_letter: r"\p{L}",
        unicode_character_category_letter_uppercase: r"\p{Lu}",
        unicode_character_category_letter_lowercase: r"\p{Ll}",
        unicode_character_category_letter_titlecase: r"\p{Lt}",
        unicode_character_category_letter_modifier: r"\p{Lm}",
        unicode_character_category_letter_other: r"\p{Lo}",
        unicode_character_category_mark_nonspcaing: r"\p{Mn}",
        unicode_character_category_mark_spacing_combining: r"\p{Mc}",
        unicode_character_category_mark_enclosing: r"\p{Me}",
        unicode_character_category_number_decimal_digit: r"\p{Nd}",
        unicode_character_category_number_letter: r"\p{Nl}",
        unicode_character_category_number_other: r"\p{No}",
        unicode_character_category_punctuation_connector: r"\p{Pc}",
        unicode_character_category_punctuation_dash: r"\p{Pd}",
        unicode_character_category_punctuation_open: r"\p{Ps}",
        unicode_character_category_punctuation_close: r"\p{Pe}",
        unicode_character_category_punctuation_initial_quote: r"\p{Pi}",
        unicode_character_category_punctuation_final_quote: r"\p{Pf}",
        unicode_character_category_punctuation_other: r"\p{Po}",
        unicode_character_category_symbol_math: r"\p{Sm}",
        unicode_character_category_symbol_currency: r"\p{Sc}",
        unicode_character_category_symbol_modifier: r"\p{Sk}",
        unicode_character_category_symbol_other: r"\p{So}",
        unicode_character_category_separator_space: r"\p{Zs}",
        unicode_character_category_separator_line: r"\p{Zl}",
        unicode_character_category_separator_paragraph: r"\p{Zp}",
        unicode_character_category_other_control: r"\p{Cc}",
        unicode_character_category_other_format: r"\p{Cf}",
        unicode_character_category_other_private_use: r"\p{Co}",
        unicode_character_category_other_not_assigned: r"\p{Cn}",
        unicode_character_category_inverted_letter: r"\P{L}",
        unicode_character_category_inverted_letter_uppercase: r"\P{Lu}",
        unicode_character_category_inverted_letter_lowercase: r"\P{Ll}",
        unicode_character_category_inverted_letter_titlecase: r"\P{Lt}",
        unicode_character_category_inverted_letter_modifier: r"\P{Lm}",
        unicode_character_category_inverted_letter_other: r"\P{Lo}",
        unicode_character_category_inverted_mark_nonspacing: r"\P{Mn}",
        unicode_character_category_inverted_mark_spacing_combining: r"\P{Mc}",
        unicode_character_category_inverted_mark_enclosing: r"\P{Me}",
        unicode_character_category_inverted_number_decimal_digit: r"\P{Nd}",
        unicode_character_category_inverted_number_letter: r"\P{Nl}",
        unicode_character_category_inverted_number_other: r"\P{No}",
        unicode_character_category_inverted_punctuation_connector: r"\P{Pc}",
        unicode_character_category_inverted_punctuation_dash: r"\P{Pd}",
        unicode_character_category_inverted_punctuation_open: r"\P{Ps}",
        unicode_character_category_inverted_punctuation_close: r"\P{Pe}",
        unicode_character_category_inverted_punctuation_initial_quote: r"\P{Pi}",
        unicode_character_category_inverted_punctuation_final_quote: r"\P{Pf}",
        unicode_character_category_inverted_punctuation_other: r"\P{Po}",
        unicode_character_category_inverted_symbol_math: r"\P{Sm}",
        unicode_character_category_inverted_symbol_currency: r"\P{Sc}",
        unicode_character_category_inverted_symbol_modifier: r"\P{Sk}",
        unicode_character_category_inverted_symbol_other: r"\P{So}",
        unicode_character_category_inverted_separator_space: r"\P{Zs}",
        unicode_character_category_inverted_separator_line: r"\P{Zl}",
        unicode_character_category_inverted_separator_paragraph: r"\P{Zp}",
        unicode_character_category_inverted_other_control: r"\P{Cc}",
        unicode_character_category_inverted_other_format: r"\P{Cf}",
        unicode_character_category_inverted_other_private_use: r"\P{Co}",
        unicode_character_category_inverted_other_not_assigned: r"\P{Cn}",
    }

    assert_invalid! {
        named_group: r"(?<group>[a-z]*)",
        multi_char_escape: r"\d",
        multi_char_escape_class_expr: r"[\S ]",
        non_greedy_repetition: r"[0-9]*?",
        back_reference: r"(\w)\1",
        lookahead: r"(?=.*[a-z])(?=.*[A-Z])(?=.*)[a-zA-Z]{8,}",
        lookbehind: r"(?<=[a-z]{4})\[a-z]{2}",
        non_capturing_group: r"(?:[a-z]+)",
        atomic_group: r"(?>[a-z]+)",
        conditional_group: r"(?(1)a|b)",
        comment: r"(?#comment)",
        flag: r"(?i)[a-z]+",
    }
}
