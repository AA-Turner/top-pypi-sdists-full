#ifndef DS_UTILITY_HH
#define DS_UTILITY_HH

#include <memory>

#include <ds/rule.hh>
#include <ds/term.hh>

namespace ds {
    /// @brief 将文本形式的term转化为二进制形式的term。
    /// @param text 文本形式的term。
    /// @param length 二进制形式的term的数据最大长度。
    /// @return 二进制的term，如果长度超过限制，则返回nullptr。
    std::unique_ptr<term_t> text_to_term(const char* text, length_t length);

    /// @brief 将二进制形式的term转化为文本形式的term。
    /// @param term 二进制形式的term。
    /// @param length 文本形式的term的文本最大长度。
    /// @return 文本形式的term，如果长度超过限制，则返回nullptr。
    std::unique_ptr<char> term_to_text(term_t* term, length_t length);

    /// @brief 将文本形式的rule转化为二进制形式的rule。
    /// @param text 文本形式的rule。
    /// @param length 二进制形式的rule的数据最大长度。
    /// @return 二进制的rule，如果长度超过限制，则返回nullptr。
    std::unique_ptr<rule_t> text_to_rule(const char* text, length_t length);

    /// @brief 将二进制形式的rule转化为文本形式的rule。
    /// @param rule 二进制形式的rule。
    /// @param length 文本形式的rule的文本最大长度。
    /// @return 文本形式的rule，如果长度超过限制，则返回nullptr。
    std::unique_ptr<char> rule_to_text(rule_t* rule, length_t length);
} // namespace ds

#endif
