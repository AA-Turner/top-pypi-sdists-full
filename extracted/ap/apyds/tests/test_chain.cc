#include <ds/chain.hh>
#include <ds/utility.hh>
#include <gtest/gtest.h>

class TestChain : public ::testing::Test {
  protected:
    const ds::length_t limit_size = 100;
    const ds::length_t buffer_size = 1000;

    TestChain() { }
    ~TestChain() override { }
    void SetUp() override {
        chain = new ds::chain_t(limit_size, buffer_size);
    }
    void TearDown() override {
        delete chain;
    }

    ds::chain_t* chain;
};

TEST_F(TestChain, reset_parameters) {
    chain->set_limit_size(50);
    chain->set_buffer_size(500);
    chain->reset();
}

TEST_F(TestChain, add_rule_and_fact) {
    EXPECT_TRUE(chain->add("test rule"));
    EXPECT_TRUE(chain->add("fact"));
}

TEST_F(TestChain, add_fail) {
    chain->set_limit_size(10);
    EXPECT_FALSE(chain->add("a-long-facts-that-exceeds-limit"));
}

TEST_F(TestChain, execute_single_premise) {
    chain->add("p q");
    chain->add("p");
    auto target = ds::text_to_rule("q", limit_size);
    bool success = false;
    auto count = chain->execute([&success, &target](ds::rule_t* rule) {
        if (memcmp(rule, target.get(), rule->data_size()) == 0) {
            success = true;
            return true;
        }
        return false;
    });
    EXPECT_EQ(count, 1);
    EXPECT_TRUE(success);
}

TEST_F(TestChain, execute_multiple_premises_chain) {
    chain->add("p q r");
    chain->add("p");
    chain->add("q");
    auto target = ds::text_to_rule("r", limit_size);
    bool success = false;
    auto count = chain->execute([&success, &target](ds::rule_t* rule) {
        if (memcmp(rule, target.get(), rule->data_size()) == 0) {
            success = true;
        }
        return false;
    });
    EXPECT_EQ(count, 2);
    EXPECT_TRUE(success);
}

TEST_F(TestChain, execute_multiple_premises_partial) {
    chain->add("p q r");
    chain->add("p");
    auto count = chain->execute([](ds::rule_t* rule) { return false; });
    EXPECT_EQ(count, 1);
}

TEST_F(TestChain, execute_three_premises) {
    chain->add("p q r s");
    chain->add("p");
    chain->add("q");
    chain->add("r");
    auto target = ds::text_to_rule("s", limit_size);
    bool success = false;
    auto count = chain->execute([&success, &target](ds::rule_t* rule) {
        if (memcmp(rule, target.get(), rule->data_size()) == 0) {
            success = true;
        }
        return false;
    });
    EXPECT_EQ(count, 3);
    EXPECT_TRUE(success);
}

TEST_F(TestChain, execute_duplicated_fact) {
    chain->add("p r");
    chain->add("q r");
    chain->add("p");
    chain->add("q");
    auto count = chain->execute([](ds::rule_t* rule) { return false; });
    EXPECT_EQ(count, 1);
}

TEST_F(TestChain, execute_exceed) {
    chain->set_limit_size(100);
    EXPECT_TRUE(chain->add("(2 `x) (`x `x`)"));
    EXPECT_TRUE(chain->add("(2 a-very-long-fact-that-exceeds-half-of-the-limit-size)"));
    auto count = chain->execute([](ds::rule_t* rule) { return false; });
    EXPECT_EQ(count, 0);
}

TEST_F(TestChain, dont_generate_duplicated_fact) {
    EXPECT_TRUE(chain->add("aaaaa bbbbb"));
    EXPECT_TRUE(chain->add("aaaaa"));
    EXPECT_EQ(chain->execute([](ds::rule_t* rule) { return false; }), 1);
    EXPECT_EQ(chain->execute([](ds::rule_t* rule) { return false; }), 0);
}

TEST_F(TestChain, execute_exceed_by_too_many_premises) {
    chain->set_limit_size(100);
    chain->set_buffer_size(1000);
    EXPECT_TRUE(chain->add("aaaaa bbbbb ccccc ddddd eeeee fffff"));
    EXPECT_TRUE(chain->add("aaaaa"));
    EXPECT_TRUE(chain->add("bbbbb"));
    EXPECT_TRUE(chain->add("ccccc"));
    EXPECT_TRUE(chain->add("ddddd"));
    EXPECT_TRUE(chain->add("eeeee"));
    EXPECT_EQ(chain->execute([](ds::rule_t* rule) { return false; }), 5);
    chain->reset();
    chain->set_limit_size(100);
    chain->set_buffer_size(1000);
    EXPECT_TRUE(chain->add("aaaaa bbbbb ccccc ddddd eeeee fffff"));
    EXPECT_TRUE(chain->add("aaaaa"));
    EXPECT_TRUE(chain->add("bbbbb"));
    EXPECT_TRUE(chain->add("ccccc"));
    EXPECT_TRUE(chain->add("ddddd"));
    EXPECT_TRUE(chain->add("eeeee"));
    EXPECT_EQ(chain->execute([](ds::rule_t* rule) { return false; }), 5);
    chain->reset();
    chain->set_limit_size(100);
    chain->set_buffer_size(100);
    EXPECT_TRUE(chain->add("aaaaa bbbbb ccccc ddddd eeeee fffff"));
    EXPECT_TRUE(chain->add("aaaaa"));
    EXPECT_TRUE(chain->add("bbbbb"));
    EXPECT_TRUE(chain->add("ccccc"));
    EXPECT_TRUE(chain->add("ddddd"));
    EXPECT_TRUE(chain->add("eeeee"));
    EXPECT_EQ(chain->execute([](ds::rule_t* rule) { return false; }), 1);
}

TEST_F(TestChain, iterator) {
    chain->add("a");
    chain->add("b");
    chain->add("a b c");
    const char* expected[] = {"b\n----\nc\n", "----\nc\n"};
    int count = 0;
    for (auto rule : chain->iterator()) {
        EXPECT_LT(count, 2);
        EXPECT_STREQ(ds::rule_to_text(rule, limit_size).get(), expected[count]);
        ++count;
    }
    EXPECT_EQ(count, 2);
}
