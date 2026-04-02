#include <ds/item.hh>
#include <ds/list.hh>
#include <ds/term.hh>
#include <gtest/gtest.h>

class TestList : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 100;

    TestList() { }
    ~TestList() override { }
    void SetUp() override {
        // The immediate value for p -> q.

        l1 = reinterpret_cast<ds::list_t*>(operator new(buffer_size));
        l2 = reinterpret_cast<ds::list_t*>(operator new(buffer_size));
        l3 = reinterpret_cast<ds::list_t*>(operator new(buffer_size));
        l4 = reinterpret_cast<ds::list_t*>(operator new(buffer_size));
        lf = reinterpret_cast<ds::list_t*>(operator new(buffer_size));
        // state 1

        l2->set_list_size(3, nullptr);
        l3->set_list_size(3, nullptr);
        l4->set_list_size(3, nullptr);
        lf->set_list_size(3, nullptr);
        // state 2

        l3->term(0)->set_item(nullptr)->item()->name()->set_null_string("p", nullptr);
        l4->term(0)->set_item(nullptr)->item()->name()->set_null_string("p", nullptr);
        lf->term(0)->set_item(nullptr)->item()->name()->set_null_string("p", nullptr);
        // state 3.0

        l3->update_term_size(0);
        l4->update_term_size(0);
        lf->update_term_size(0);
        // state 4.0

        l3->term(1)->set_item(nullptr)->item()->name()->set_null_string("->", nullptr);
        lf->term(1)->set_item(nullptr)->item()->name()->set_null_string("->", nullptr);
        // state 3.1

        lf->update_term_size(1);
        // state 4.0

        lf->term(2)->set_item(nullptr)->item()->name()->set_null_string("q", nullptr);
        // state 3.2

        lf->update_term_size(2);
        // state 4.2
    }
    void TearDown() override {
        operator delete(l1);
        operator delete(l2);
        operator delete(l3);
        operator delete(l4);
        operator delete(lf);
    }

    // list size = 3
    ds::list_t* l1; // state 1
    ds::list_t* l2; // state 2
    ds::list_t* l3; // state 3.1
    ds::list_t* l4; // state 4.0
    ds::list_t* lf; // state 4.2
};

TEST_F(TestList, get_list_size) {
    EXPECT_EQ(l2->get_list_size(), 3);
    EXPECT_EQ(l3->get_list_size(), 3);
    EXPECT_EQ(l4->get_list_size(), 3);
    EXPECT_EQ(lf->get_list_size(), 3);
}

TEST_F(TestList, set_list_size) {
    ds::length_t new_size = 5;
    EXPECT_EQ(l1->set_list_size(new_size, nullptr), l1);
    EXPECT_EQ(l1->get_list_size(), new_size);
    EXPECT_EQ(l2->set_list_size(new_size, nullptr), l2);
    EXPECT_EQ(l2->get_list_size(), new_size);
    EXPECT_EQ(l3->set_list_size(new_size, nullptr), l3);
    EXPECT_EQ(l3->get_list_size(), new_size);
    EXPECT_EQ(l4->set_list_size(new_size, nullptr), l4);
    EXPECT_EQ(l4->get_list_size(), new_size);
    EXPECT_EQ(lf->set_list_size(new_size, nullptr), lf);
    EXPECT_EQ(lf->get_list_size(), new_size);

    EXPECT_EQ(l2->set_list_size(new_size, reinterpret_cast<std::byte*>(l2)), nullptr);
    EXPECT_EQ(l2->set_list_size(new_size, reinterpret_cast<std::byte*>(l2) + sizeof(ds::length_t) + sizeof(ds::length_t) * new_size - 1), nullptr);
    EXPECT_NE(l2->set_list_size(new_size, reinterpret_cast<std::byte*>(l2) + sizeof(ds::length_t) + sizeof(ds::length_t) * new_size), nullptr);
}

TEST_F(TestList, term_size) {
    EXPECT_EQ(l3->term_size(0), l3->term(0)->data_size());
    EXPECT_EQ(l4->term_size(0), l4->term(0)->data_size());
    EXPECT_EQ(lf->term_size(0), lf->term(0)->data_size());
    EXPECT_EQ(lf->term_size(1), lf->term(0)->data_size() + lf->term(1)->data_size());
    EXPECT_EQ(lf->term_size(2), lf->term(0)->data_size() + lf->term(1)->data_size() + lf->term(2)->data_size());
}

TEST_F(TestList, term) {
    EXPECT_EQ(
        l3->term(0),
        reinterpret_cast<ds::term_t*>(reinterpret_cast<std::byte*>(l3) + sizeof(ds::length_t) + sizeof(ds::length_t) * l3->get_list_size())
    );
    EXPECT_EQ(
        l3->term(1),
        reinterpret_cast<ds::term_t*>(
            reinterpret_cast<std::byte*>(l3) + sizeof(ds::length_t) + sizeof(ds::length_t) * l3->get_list_size() + l3->term_size(0)
        )
    );
}

TEST_F(TestList, update_term_size) {
    l3->update_term_size(1);
    EXPECT_EQ(l3->term_size(1), l3->term(0)->data_size() + l3->term(1)->data_size());
}

TEST_F(TestList, data_size) {
    ds::length_t head_size = sizeof(ds::length_t) + sizeof(ds::length_t) * lf->get_list_size();
    ds::length_t term_size = lf->term(0)->data_size() + lf->term(1)->data_size() + lf->term(2)->data_size();
    EXPECT_EQ(lf->data_size(), head_size + term_size);
}

TEST_F(TestList, head_tail) {
    EXPECT_EQ(l1->head(), reinterpret_cast<std::byte*>(l1));
    EXPECT_EQ(l2->head(), reinterpret_cast<std::byte*>(l2));
    EXPECT_EQ(l3->head(), reinterpret_cast<std::byte*>(l3));
    EXPECT_EQ(l4->head(), reinterpret_cast<std::byte*>(l4));
    EXPECT_EQ(lf->head(), reinterpret_cast<std::byte*>(lf));
    EXPECT_EQ(lf->tail(), reinterpret_cast<std::byte*>(lf) + lf->data_size());
}

TEST_F(TestList, print) {
    char buffer[100];
    const char* expect = "(p -> q)";
    char* print_result = lf->print(buffer, nullptr);
    EXPECT_NE(print_result, nullptr);
    *print_result = '\0';
    EXPECT_STREQ(buffer, expect);

    EXPECT_NE(lf->print(buffer, buffer + strlen(expect)), nullptr);
    for (ds::length_t i = 0; i < strlen(expect); ++i) {
        EXPECT_EQ(lf->print(buffer, buffer + i), nullptr);
    }
}

TEST_F(TestList, scan) {
    const char* input = "(p -> q)";
    const char* scan_result = lf->scan(input, nullptr);
    EXPECT_NE(scan_result, nullptr);
    EXPECT_EQ(scan_result, input + strlen(input));
    EXPECT_EQ(lf->get_list_size(), 3);
    EXPECT_STREQ(lf->term(0)->item()->name()->get_string(), "p");
    EXPECT_STREQ(lf->term(1)->item()->name()->get_string(), "->");
    EXPECT_STREQ(lf->term(2)->item()->name()->get_string(), "q");

    ds::length_t correct_length = lf->data_size();
    EXPECT_NE(lf->scan(input, reinterpret_cast<std::byte*>(lf) + correct_length), nullptr);
    for (ds::length_t i = 0; i < correct_length; ++i) {
        EXPECT_EQ(lf->scan(input, reinterpret_cast<std::byte*>(lf) + i), nullptr);
    }
}
