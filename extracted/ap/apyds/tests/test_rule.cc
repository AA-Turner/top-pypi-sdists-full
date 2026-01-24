#include <ds/item.hh>
#include <ds/list.hh>
#include <ds/rule.hh>
#include <ds/term.hh>
#include <gtest/gtest.h>

class TestRule : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 100;

    TestRule() { }
    ~TestRule() override { }
    void SetUp() override {
        r1 = reinterpret_cast<ds::rule_t*>(operator new(buffer_size));
        r2 = reinterpret_cast<ds::rule_t*>(operator new(buffer_size));
        rf = reinterpret_cast<ds::rule_t*>(operator new(buffer_size));
        rc = reinterpret_cast<ds::rule_t*>(operator new(buffer_size));
        rl = reinterpret_cast<ds::rule_t*>(operator new(buffer_size));

        r2->set_null(nullptr);

        ds::list_t* lf = reinterpret_cast<ds::list_t*>(rf);
        lf->set_list_size(2, nullptr);
        lf->term(0)->set_item(nullptr)->item()->name()->set_null_string("p", nullptr);
        lf->update_term_size(0);
        lf->term(1)->set_item(nullptr)->item()->name()->set_null_string("q", nullptr);
        lf->update_term_size(1);

        ds::list_t* lc = reinterpret_cast<ds::list_t*>(rc);
        lc->set_list_size(1, nullptr);
        lc->term(0)->set_item(nullptr)->item()->name()->set_null_string("x", nullptr);
        lc->update_term_size(0);

        ds::list_t* ll = reinterpret_cast<ds::list_t*>(rl);
        ll->set_list_size(2, nullptr);
        ll->term(0)->set_item(nullptr)->item()->name()->set_null_string("a-very-long-premise", nullptr);
        ll->update_term_size(0);
        ll->term(1)->set_item(nullptr)->item()->name()->set_null_string("q", nullptr);
        ll->update_term_size(1);
    }
    void TearDown() override {
        operator delete(r1);
        operator delete(r2);
        operator delete(rf);
        operator delete(rc);
        operator delete(rl);
    }

    ds::rule_t* r1;
    ds::rule_t* r2;
    ds::rule_t* rf;
    ds::rule_t* rc;
    ds::rule_t* rl;
};

TEST_F(TestRule, conclusion) {
    EXPECT_EQ(r2->conclusion(), nullptr);
    EXPECT_STREQ(rf->conclusion()->item()->name()->get_string(), "q");
    EXPECT_STREQ(rc->conclusion()->item()->name()->get_string(), "x");
}

TEST_F(TestRule, only_conclusion) {
    EXPECT_EQ(r2->only_conclusion(), nullptr);
    EXPECT_EQ(rf->only_conclusion(), nullptr);
    EXPECT_STREQ(rc->only_conclusion()->item()->name()->get_string(), "x");
}

TEST_F(TestRule, premises) {
    EXPECT_EQ(r2->premises(-1), nullptr);
    EXPECT_EQ(r2->premises(0), nullptr);
    EXPECT_EQ(rf->premises(-1), nullptr);
    EXPECT_STREQ(rf->premises(0)->item()->name()->get_string(), "p");
    EXPECT_EQ(rf->premises(1), nullptr);
    EXPECT_EQ(rc->premises(-1), nullptr);
    EXPECT_EQ(rc->premises(0), nullptr);
}

TEST_F(TestRule, premises_count) {
    EXPECT_EQ(rf->premises_count(), 1);
    EXPECT_EQ(rc->premises_count(), 0);
}

TEST_F(TestRule, valid) {
    EXPECT_FALSE(r2->valid());
    EXPECT_TRUE(rf->valid());
    EXPECT_TRUE(rc->valid());
}

TEST_F(TestRule, set_null) {
    EXPECT_EQ(r1->set_null(nullptr), r1);
    EXPECT_FALSE(r1->valid());

    EXPECT_NE(r1->set_null(reinterpret_cast<std::byte*>(r1) + sizeof(ds::length_t)), nullptr);
    EXPECT_EQ(r1->set_null(reinterpret_cast<std::byte*>(r1) + sizeof(ds::length_t) - 1), nullptr);
}

TEST_F(TestRule, data_size) {
    EXPECT_EQ(r2->data_size(), sizeof(ds::length_t));
    EXPECT_EQ(rf->data_size(), sizeof(ds::length_t) + sizeof(ds::length_t) * 2 + rf->premises(0)->data_size() + rf->conclusion()->data_size());
    EXPECT_EQ(rc->data_size(), sizeof(ds::length_t) + sizeof(ds::length_t) * 1 + rf->conclusion()->data_size());
}

TEST_F(TestRule, head_tail) {
    EXPECT_EQ(r1->head(), reinterpret_cast<std::byte*>(r1));
    EXPECT_EQ(r2->head(), reinterpret_cast<std::byte*>(r2));
    EXPECT_EQ(rf->head(), reinterpret_cast<std::byte*>(rf));
    EXPECT_EQ(rc->head(), reinterpret_cast<std::byte*>(rc));
    EXPECT_EQ(r2->tail(), reinterpret_cast<std::byte*>(r2) + r2->data_size());
    EXPECT_EQ(rf->tail(), reinterpret_cast<std::byte*>(rf) + rf->data_size());
    EXPECT_EQ(rc->tail(), reinterpret_cast<std::byte*>(rc) + rc->data_size());
}

TEST_F(TestRule, print) {
    char buffer[100];

    EXPECT_EQ(r2->print(buffer, nullptr), nullptr);

    const char* expect_f = "p\n"
                           "----\n"
                           "q\n";
    char* print_result_f = rf->print(buffer, nullptr);
    EXPECT_NE(print_result_f, nullptr);
    *print_result_f = '\0';
    EXPECT_STREQ(buffer, expect_f);
    EXPECT_NE(rf->print(buffer, buffer + strlen(expect_f)), nullptr);
    for (ds::length_t i = 0; i < strlen(expect_f); ++i) {
        EXPECT_EQ(rf->print(buffer, buffer + i), nullptr);
    }

    const char* expect_c = "----\n"
                           "x\n";
    char* print_result_c = rc->print(buffer, nullptr);
    EXPECT_NE(print_result_c, nullptr);
    *print_result_c = '\0';
    EXPECT_STREQ(buffer, expect_c);
    for (ds::length_t i = 0; i < strlen(expect_c); ++i) {
        EXPECT_EQ(rc->print(buffer, buffer + i), nullptr);
    }

    const char* expect_l = "a-very-long-premise\n"
                           "-------------------\n"
                           "q\n";
    char* print_result_l = rl->print(buffer, nullptr);
    EXPECT_NE(print_result_l, nullptr);
    *print_result_l = '\0';
    EXPECT_STREQ(buffer, expect_l);
    EXPECT_NE(rl->print(buffer, buffer + strlen(expect_l)), nullptr);
    for (ds::length_t i = 0; i < strlen(expect_l); ++i) {
        EXPECT_EQ(rl->print(buffer, buffer + i), nullptr);
    }
}

TEST_F(TestRule, scan) {
    const char* input_1 = "-a-premise-start-with-'-'\n"
                          "q\n"
                          "-------------------------\n"
                          "r\n";
    const char* scan_result_f = r1->scan(input_1, nullptr);
    EXPECT_EQ(scan_result_f, input_1 + strlen(input_1) - 1); // 被"----"终止，最后一个 \n 并没有读入
    EXPECT_EQ(r1->premises_count(), 2);
    EXPECT_STREQ(r1->premises(0)->item()->name()->get_string(), "-a-premise-start-with-'-'");
    EXPECT_STREQ(r1->premises(1)->item()->name()->get_string(), "q");
    EXPECT_STREQ(r1->conclusion()->item()->name()->get_string(), "r");

    ds::length_t correct_length_1 = r1->data_size();
    EXPECT_NE(r1->scan(input_1, reinterpret_cast<std::byte*>(r1) + correct_length_1), nullptr);
    for (ds::length_t i = 0; i < correct_length_1; ++i) {
        EXPECT_EQ(r1->scan(input_1, reinterpret_cast<std::byte*>(r1) + i), nullptr);
    }

    const char* input_2 = "x\n";
    const char* scan_result_c = r2->scan(input_2, nullptr);
    EXPECT_EQ(scan_result_c, input_2 + strlen(input_2)); // 被 \0 终止，最后一个 \n 被读入
    EXPECT_EQ(r2->premises_count(), 0);
    EXPECT_STREQ(r2->only_conclusion()->item()->name()->get_string(), "x");

    ds::length_t correct_length_2 = r2->data_size();
    EXPECT_NE(r2->scan(input_2, reinterpret_cast<std::byte*>(r2) + correct_length_2), nullptr);
    for (ds::length_t i = 0; i < correct_length_2; ++i) {
        EXPECT_EQ(r2->scan(input_2, reinterpret_cast<std::byte*>(r2) + i), nullptr);
    }
}
