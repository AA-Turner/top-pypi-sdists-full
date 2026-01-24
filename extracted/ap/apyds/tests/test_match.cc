#include <ds/rule.hh>
#include <ds/term.hh>
#include <ds/utility.hh>
#include <gtest/gtest.h>

class TestMatch : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 10000;

    TestMatch() { }
    ~TestMatch() override { }
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

    void ground_term_check(const char* term_1_text, const char* term_2_text, const char* expect_text) {
        auto term_1 = ds::text_to_term(term_1_text, buffer_size);
        auto term_2 = ds::text_to_term(term_2_text, buffer_size);
        auto match_result = result_t->match(term_1.get(), term_2.get(), "r", "f", nullptr);
        if (expect_text == nullptr) {
            EXPECT_EQ(match_result, nullptr);
        } else {
            EXPECT_NE(match_result, nullptr);
            auto result = ds::term_to_text(result_t, buffer_size);
            EXPECT_STREQ(result.get(), expect_text);

            auto correct_length = result_t->data_size();
            EXPECT_NE(result_t->match(term_1.get(), term_2.get(), "r", "f", reinterpret_cast<std::byte*>(result_t) + correct_length), nullptr);
            for (ds::length_t i = 0; i < correct_length; ++i) {
                EXPECT_EQ(result_t->match(term_1.get(), term_2.get(), "r", "f", reinterpret_cast<std::byte*>(result_t) + i), nullptr);
            }
        }
    }

    void ground_rule_check(const char* rule_text, const char* dict_text, const char* expect_text) {
        auto rule = ds::text_to_rule(rule_text, buffer_size);
        auto dict = ds::text_to_rule(dict_text, buffer_size);
        auto match_result = result_r->match(rule.get(), dict.get(), nullptr);
        if (expect_text == nullptr) {
            EXPECT_EQ(match_result, nullptr);
        } else {
            EXPECT_NE(match_result, nullptr);
            auto result = ds::rule_to_text(result_r, buffer_size);
            EXPECT_STREQ(result.get(), expect_text);

            auto incorrect_length = result_r->data_size();
            for (ds::length_t i = 0; i < incorrect_length; ++i) {
                EXPECT_EQ(result_r->match(rule.get(), dict.get(), reinterpret_cast<std::byte*>(result_r) + i), nullptr);
            }
        }
    }
};

TEST_F(TestMatch, match_term) {
    ground_term_check("p", "p", "()"); // string match
    ground_term_check("p", "q", nullptr); // difference string data
    ground_term_check("p", "pp", nullptr); // difference string length

    ground_term_check("(`p `p)", "(`q `q)", "((r f `p `q))"); // same scope same variable
    ground_term_check("(`p `p)", "(`p `q)", "((r f `p `p) (f f `p `q))"); // same scope different variable

    ground_term_check("`p", "p", "((r f `p p))"); // left variable match
    ground_term_check("p", "`p", "((f r `p p))"); // right variable match

    ground_term_check("item", "item", "()"); // item match

    ground_term_check("(p q)", "(p q r)", nullptr); // difference list size
    ground_term_check("(p q)", "(p q)", "()"); // matched list
    ground_term_check("(p q)", "q", nullptr); // everything mismatch

    ground_term_check("(p `q)", "(`p `p)", "((f r `p p) (r r `q p))"); // value substituded in unify variable
    ground_term_check("(`p (! `p))", "((! `q) `q)", nullptr); // occur check fail
}

TEST_F(TestMatch, match_rule) {
    ground_rule_check("p r q", "p ", "r\n----\nq\n"); // string match
    ground_rule_check("p x", "q", nullptr); // difference string data
    ground_rule_check("p x", "pp", nullptr); // difference string length

    ground_rule_check("(`p `p) `p", "(`q `q)", "----\n`q\n"); // same scope same variable
    ground_rule_check("(`p `p) (! `p)", "(`p `q)", "----\n(! `q)\n"); // same scope different variable

    ground_rule_check("`p `p", "p", "----\np\n"); // left variable match
    ground_rule_check("p b", "`p", "----\nb\n"); // right variable match

    ground_rule_check("item conclusion", "item", "----\nconclusion\n"); // item match

    ground_rule_check("(p q) x", "(p q r)", nullptr); // difference list size
    ground_rule_check("(p q) (p q)", "(p q)", "----\n(p q)\n"); // matched list
    ground_rule_check("(p q) ops", "q", nullptr); // everything mismatch

    ground_rule_check("(p `q) (`q q)", "(`p `p)", "----\n(p q)\n"); // value substituded in unify variable
    ground_rule_check("(`p (! `p)) fail_premise fail_conclusion", "((! `q) `q)", nullptr); // occur check fail

    ground_rule_check("a", "b", nullptr); // invalid premises count, case 1
    ground_rule_check("a b", "c d", nullptr); // invalid premises count, case 2
    ground_rule_check("a", "b c", nullptr); // invalid premises count, case 3
}
