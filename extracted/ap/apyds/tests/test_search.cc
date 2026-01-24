#include <ds/search.hh>
#include <ds/utility.hh>
#include <gtest/gtest.h>

class TestSearch : public ::testing::Test {
  protected:
    const ds::length_t limit_size = 100;
    const ds::length_t buffer_size = 1000;

    TestSearch() { }
    ~TestSearch() override { }
    void SetUp() override {
        search = new ds::search_t(limit_size, buffer_size);
    }
    void TearDown() override {
        delete search;
    }

    ds::search_t* search;
};

TEST_F(TestSearch, reset_parameters) {
    search->set_limit_size(50);
    search->set_buffer_size(500);
    search->reset();
}

TEST_F(TestSearch, add_rule_and_fact) {
    EXPECT_TRUE(search->add("test rule"));
    EXPECT_TRUE(search->add("fact"));
}

TEST_F(TestSearch, add_fail) {
    search->set_limit_size(10);
    EXPECT_FALSE(search->add("a-long-facts-that-exceeds-limit"));
}

TEST_F(TestSearch, execute_single) {
    search->add("p q");
    search->add("p");
    auto target = ds::text_to_rule("q", limit_size);
    bool success = false;
    auto count = search->execute([&success, &target](ds::rule_t* rule) {
        if (memcmp(rule, target.get(), rule->data_size()) == 0) {
            success = true;
            return true;
        }
        return false;
    });
    EXPECT_EQ(count, 1);
    EXPECT_TRUE(success);
}

TEST_F(TestSearch, execute_long) {
    search->add("p q r");
    search->add("p");
    search->add("q");
    auto target1 = ds::text_to_rule("q r", limit_size);
    auto target2 = ds::text_to_rule("r", limit_size);
    bool success1 = false;
    bool success2 = false;
    auto count1 = search->execute([&success1, &target1](ds::rule_t* rule) {
        if (memcmp(rule, target1.get(), rule->data_size()) == 0) {
            success1 = true;
        }
        return false;
    });
    auto count2 = search->execute([&success2, &target2](ds::rule_t* rule) {
        if (memcmp(rule, target2.get(), rule->data_size()) == 0) {
            success2 = true;
        }
        return false;
    });
    EXPECT_EQ(count1, 1);
    EXPECT_TRUE(success1);
    EXPECT_EQ(count2, 1);
    EXPECT_TRUE(success2);
}

TEST_F(TestSearch, execute_duplicated_fact) {
    search->add("p r");
    search->add("q r");
    search->add("p");
    search->add("q");
    auto count = search->execute([](ds::rule_t* rule) { return false; });
    EXPECT_EQ(count, 1);
}

TEST_F(TestSearch, execute_duplicated_rule) {
    search->add("p r s");
    search->add("q r s");
    search->add("p");
    search->add("q");
    auto count = search->execute([](ds::rule_t* rule) { return false; });
    EXPECT_EQ(count, 1);
}

TEST_F(TestSearch, execute_exceed) {
    search->set_limit_size(100);
    EXPECT_TRUE(search->add("(2 `x) (`x `x`)"));
    EXPECT_TRUE(search->add("(2 a-very-long-fact-that-exceeds-half-of-the-limit-size)"));
    auto count = search->execute([](ds::rule_t* rule) { return false; });
    EXPECT_EQ(count, 0);
}
