/**
 * CSSL Lexer - High-performance tokenizer for CSSL language
 *
 * Part of IncludeCPP's self-hosting optimization strategy.
 * This C++ implementation provides 10-20x speedup over Python.
 *
 * Copyright (c) 2024-2026 Lilias Hatterscheidt
 * Licensed under MIT License
 */

#pragma once

#include <string>
#include <string_view>
#include <vector>
#include <variant>
#include <unordered_set>
#include <cstdint>
#include <stdexcept>

namespace cssl {

/**
 * Token types matching Python cssl_parser.py TokenType enum
 */
enum class TokenType {
    // Basic types
    KEYWORD,
    IDENTIFIER,
    STRING,
    STRING_INTERP,      // <variable> in strings
    NUMBER,
    BOOLEAN,
    NULL_T,
    TYPE_LITERAL,       // list, dict as type literals
    TYPE_GENERIC,       // datastruct<T>, shuffled<T>, etc.

    // Injection operators
    INJECT_LEFT,        // <==
    INJECT_RIGHT,       // ==>
    INJECT_PLUS_LEFT,   // +<==
    INJECT_PLUS_RIGHT,  // ==>+
    INJECT_MINUS_LEFT,  // -<==
    INJECT_MINUS_RIGHT, // ===>-

    // Code Infusion operators
    INFUSE_LEFT,        // <<==
    INFUSE_RIGHT,       // ==>>
    INFUSE_PLUS_LEFT,   // +<<==
    INFUSE_PLUS_RIGHT,  // ==>>+
    INFUSE_MINUS_LEFT,  // -<<==
    INFUSE_MINUS_RIGHT, // ==>>-

    // Flow operators
    FLOW_RIGHT,         // ->
    FLOW_LEFT,          // <-

    // Assignment and comparison
    EQUALS,             // =
    COMPARE_EQ,         // ==
    COMPARE_NE,         // !=
    COMPARE_LT,         // <
    COMPARE_GT,         // >
    COMPARE_LE,         // <=
    COMPARE_GE,         // >=

    // Arithmetic
    PLUS,               // +
    MINUS,              // -
    MULTIPLY,           // *
    DIVIDE,             // /
    MODULO,             // %

    // Logical
    AND,                // && or 'and'
    OR,                 // || or 'or'
    NOT,                // ! or 'not'
    AMPERSAND,          // & (reference/bitwise)

    // Delimiters
    BLOCK_START,        // {
    BLOCK_END,          // }
    PAREN_START,        // (
    PAREN_END,          // )
    BRACKET_START,      // [
    BRACKET_END,        // ]
    SEMICOLON,          // ;
    COLON,              // :
    DOUBLE_COLON,       // ::
    COMMA,              // ,
    DOT,                // .

    // References
    AT,                 // @
    GLOBAL_REF,         // r@name
    SELF_REF,           // s@name
    SHARED_REF,         // $name
    CAPTURED_REF,       // %name
    THIS_REF,           // this->

    // Package/module
    PACKAGE,
    PACKAGE_INCLUDES,
    AS,

    // Special
    COMMENT,
    NEWLINE,
    EOF_T,

    // Super-functions (payload files)
    SUPER_FUNC,         // #$run(), #$exec(), etc.

    // Append/extension operators
    PLUS_PLUS,          // ++ (constructor/function extension)
    MINUS_MINUS,        // --

    // Multi-language support
    LANG_INSTANCE_REF   // cpp$InstanceName, py$Object
};

/**
 * Token value - can hold string, number, or boolean
 */
using TokenValue = std::variant<std::monostate, std::string, double, bool>;

/**
 * Token structure
 */
struct Token {
    TokenType type;
    TokenValue value;
    uint32_t line;
    uint32_t column;

    // Convenience getters
    bool has_string() const { return std::holds_alternative<std::string>(value); }
    bool has_number() const { return std::holds_alternative<double>(value); }
    bool has_bool() const { return std::holds_alternative<bool>(value); }

    const std::string& as_string() const { return std::get<std::string>(value); }
    double as_number() const { return std::get<double>(value); }
    bool as_bool() const { return std::get<bool>(value); }
};

/**
 * Lexer error with source location
 */
class LexerError : public std::runtime_error {
public:
    LexerError(const std::string& message, uint32_t line, uint32_t column,
               const std::string& source_line = "")
        : std::runtime_error(build_message(message, line, column, source_line)),
          line_(line), column_(column) {}

    uint32_t line() const { return line_; }
    uint32_t column() const { return column_; }

private:
    uint32_t line_;
    uint32_t column_;

    static std::string build_message(const std::string& msg, uint32_t line, uint32_t col,
                                     const std::string& src_line) {
        std::string result = "CSSL Lexer Error at line " + std::to_string(line) +
                            ", column " + std::to_string(col) + ": " + msg;
        if (!src_line.empty()) {
            result += "\n  " + src_line;
            if (col > 0) {
                result += "\n  " + std::string(col - 1, ' ') + "^";
            }
        }
        return result;
    }
};

/**
 * High-performance CSSL Lexer
 *
 * Converts CSSL source code into a vector of tokens.
 * Optimized for speed with minimal allocations.
 */
class Lexer {
public:
    /**
     * Construct lexer with source code
     * @param source CSSL source code (must remain valid during tokenization)
     */
    explicit Lexer(std::string_view source);

    /**
     * Tokenize entire source and return all tokens
     * @return Vector of tokens including EOF token at end
     */
    std::vector<Token> tokenize();

    /**
     * Get next token (streaming mode)
     * @return Next token, EOF_T when done
     */
    Token next_token();

    /**
     * Check if more tokens available
     */
    bool has_more() const { return pos_ < source_.size(); }

    /**
     * Reset lexer to beginning
     */
    void reset();

private:
    std::string_view source_;
    size_t pos_ = 0;
    uint32_t line_ = 1;
    uint32_t column_ = 1;

    // Current character helpers
    char current() const;
    char peek(size_t offset = 1) const;
    void advance(size_t count = 1);
    bool at_end() const { return pos_ >= source_.size(); }

    // Whitespace and comment handling
    void skip_whitespace();
    void skip_comment();
    void skip_block_comment();

    // Token readers
    Token read_string(char quote);
    Token read_raw_string();
    Token read_number();
    Token read_identifier();
    Token read_operator();

    // Special token readers
    Token read_super_function();
    Token read_global_ref();
    Token read_self_ref();
    Token read_shared_ref();
    Token read_captured_ref();

    // Operator readers
    Token read_less_than();
    Token read_greater_than();
    Token read_equals();
    Token read_not();
    Token read_minus();
    Token read_plus();

    // Token creation helpers
    Token make_token(TokenType type, TokenValue value = {}) const;

    // Error helper
    [[noreturn]] void error(const std::string& message) const;

    // Static keyword sets (initialized once)
    static const std::unordered_set<std::string> keywords_;
    static const std::unordered_set<std::string> type_literals_;
    static const std::unordered_set<std::string> type_generics_;
    static const std::unordered_set<std::string> language_ids_;
};

/**
 * Utility function: Tokenize source code
 * @param source CSSL source code
 * @return Vector of tokens
 */
inline std::vector<Token> tokenize(const std::string& source) {
    Lexer lexer(source);
    return lexer.tokenize();
}

/**
 * Get string representation of token type
 */
const char* token_type_name(TokenType type);

} // namespace cssl
