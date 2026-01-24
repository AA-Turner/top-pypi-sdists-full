#include <ds/term.hh>
#include <ds/utility.hh>
#include <gtest/gtest.h>

class TestGround : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 100;

    TestGround() { }
    ~TestGround() override { }
    void SetUp() override {
        result_t = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        result_r = reinterpret_cast<ds::rule_t*>(operator new(buffer_size));
    }
    void TearDown() override {
        operator delete(result_t);
        operator delete(result_r);
    }

    ds::term_t* result_t;
    ds::rule_t* result_r;

    void ground_term_term_check(const char* term_text, const char* dict_text, const char* scope, const char* expect_text) {
        auto term = ds::text_to_term(term_text, buffer_size);
        auto dict = ds::text_to_term(dict_text, buffer_size);
        EXPECT_NE(result_t->ground(term.get(), dict.get(), scope, nullptr), nullptr);
        auto result = ds::term_to_text(result_t, buffer_size);
        EXPECT_STREQ(result.get(), expect_text);
        auto correct_length = result_t->data_size();
        EXPECT_NE(result_t->ground(term.get(), dict.get(), scope, reinterpret_cast<std::byte*>(result_t) + correct_length), nullptr);
        for (auto i = 0; i < correct_length; ++i) {
            EXPECT_EQ(result_t->ground(term.get(), dict.get(), scope, reinterpret_cast<std::byte*>(result_t) + i), nullptr);
        }
    }

    void ground_rule_term_check(const char* term_text, const char* dict_text, const char* scope, const char* expect_text) {
        auto rule = ds::text_to_rule(term_text, buffer_size);
        auto dict = ds::text_to_term(dict_text, buffer_size);
        EXPECT_NE(result_r->ground(rule.get(), dict.get(), scope, nullptr), nullptr);
        auto result = ds::rule_to_text(result_r, buffer_size);
        EXPECT_STREQ(result.get(), expect_text);
        auto correct_length = result_r->data_size();
        EXPECT_NE(result_r->ground(rule.get(), dict.get(), scope, reinterpret_cast<std::byte*>(result_r) + correct_length), nullptr);
        for (auto i = 0; i < correct_length; ++i) {
            EXPECT_EQ(result_r->ground(rule.get(), dict.get(), scope, reinterpret_cast<std::byte*>(result_r) + i), nullptr);
        }
    }

    void ground_rule_rule_check(const char* term_text, const char* dict_text, const char* scope, const char* expect_text) {
        auto rule = ds::text_to_rule(term_text, buffer_size);
        auto dict = ds::text_to_rule(dict_text, buffer_size);
        EXPECT_NE(result_r->ground(rule.get(), dict.get(), scope, nullptr), nullptr);
        auto result = ds::rule_to_text(result_r, buffer_size);
        EXPECT_STREQ(result.get(), expect_text);
        auto correct_length = result_r->data_size();
        EXPECT_NE(result_r->ground(rule.get(), dict.get(), scope, reinterpret_cast<std::byte*>(result_r) + correct_length), nullptr);
        for (auto i = 0; i < correct_length; ++i) {
            EXPECT_EQ(result_r->ground(rule.get(), dict.get(), scope, reinterpret_cast<std::byte*>(result_r) + i), nullptr);
        }
    }
};

TEST_F(TestGround, ground_term_term) {
    ground_term_term_check("`x", "((`x X))", nullptr, "X");
    ground_term_term_check("`x", "((`x `X))", nullptr, "`X");
    ground_term_term_check("`x", "((`x ()))", nullptr, "()");
    ground_term_term_check("(`x `y)", "((`x (`y)) (`y ?))", nullptr, "((?) ?)");
    ground_term_term_check("`x", "((`x x))", "a", "x");
    ground_term_term_check("`x", "((a `x x))", nullptr, "x");
    ground_term_term_check("`x", "((a `x a) (b `x b))", "a", "a");
    ground_term_term_check("`x", "((a `x a) (b `x b))", "b", "b");
    ground_term_term_check("`x", "((a b `x `x) (b a `x y))", "a", "y");

    ds::term_t* null_term = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
    null_term->set_null(nullptr);
    auto dict = ds::text_to_term("()", buffer_size);
    EXPECT_EQ(result_t->ground(null_term, dict.get(), nullptr, nullptr), nullptr);
    operator delete(null_term);

    auto some_term = ds::text_to_term("((`a b c d e))", buffer_size);
    EXPECT_EQ(result_t->ground(some_term.get(), some_term.get(), nullptr, nullptr), nullptr);
}

TEST_F(TestGround, ground_rule_term) {
    ground_rule_term_check("`x", "((`x X))", nullptr, "----\nX\n");
    ground_rule_term_check("`x", "((`x `X))", nullptr, "----\n`X\n");
    ground_rule_term_check("`x", "((`x ()))", nullptr, "----\n()\n");
    ground_rule_term_check("(`x `y)", "((`x (`y)) (`y ?))", nullptr, "----\n((?) ?)\n");
    ground_rule_term_check("`x", "((`x x))", "a", "----\nx\n");
    ground_rule_term_check("`x", "((a `x x))", nullptr, "----\nx\n");
    ground_rule_term_check("`x", "((a `x a) (b `x b))", "a", "----\na\n");
    ground_rule_term_check("`x", "((a `x a) (b `x b))", "b", "----\nb\n");
    ground_rule_term_check("`x", "((a b `x `x) (b a `x y))", "a", "----\ny\n");

    ground_rule_term_check(
        "(`p -> `q)\n"
        "`p\n"
        "----------\n"
        "`q\n",
        "((a `p P) (b `q Q))",
        "a",
        "(P -> `q)\n"
        "P\n"
        "---------\n"
        "`q\n"
    );
}

TEST_F(TestGround, ground_rule_rule) {
    ground_rule_rule_check("`x", "((`x X))", nullptr, "----\nX\n");
    ground_rule_rule_check("`x", "((`x `X))", nullptr, "----\n`X\n");
    ground_rule_rule_check("`x", "((`x ()))", nullptr, "----\n()\n");
    ground_rule_rule_check("(`x `y)", "((`x (`y)) (`y ?))", nullptr, "----\n((?) ?)\n");
    ground_rule_rule_check("`x", "((`x x))", "a", "----\nx\n");
    ground_rule_rule_check("`x", "((a `x x))", nullptr, "----\nx\n");
    ground_rule_rule_check("`x", "((a `x a) (b `x b))", "a", "----\na\n");
    ground_rule_rule_check("`x", "((a `x a) (b `x b))", "b", "----\nb\n");
    ground_rule_rule_check("`x", "((a b `x `x) (b a `x y))", "a", "----\ny\n");

    ground_rule_rule_check(
        "(`p -> `q)\n"
        "`p\n"
        "----------\n"
        "`q\n",
        "((a `p P) (b `q Q))",
        "a",
        "(P -> `q)\n"
        "P\n"
        "---------\n"
        "`q\n"
    );
}
