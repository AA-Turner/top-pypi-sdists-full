#include <ds/item.hh>
#include <ds/list.hh>
#include <ds/term.hh>
#include <ds/variable.hh>
#include <gtest/gtest.h>

class TestTerm : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 100;

    TestTerm() { }
    ~TestTerm() override { }
    void SetUp() override {
        t1 = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        t2n = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        t2v = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        t2i = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        t2l = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        t3v = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        t3i = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        t3l = reinterpret_cast<ds::term_t*>(operator new(buffer_size));
        // state 1

        t2n->set_null(nullptr);
        t2v->set_variable(nullptr);
        t2i->set_item(nullptr);
        t2l->set_list(nullptr);
        t3v->set_variable(nullptr);
        t3i->set_item(nullptr);
        t3l->set_list(nullptr);
        // state 2

        t3v->variable()->name()->set_null_string("v", nullptr);
        t3i->item()->name()->set_null_string("i", nullptr);
        t3l->list()->set_list_size(0, nullptr);
        // state 3
    }
    void TearDown() override {
        operator delete(t1);
        operator delete(t2n);
        operator delete(t2v);
        operator delete(t2i);
        operator delete(t2l);
        operator delete(t3v);
        operator delete(t3i);
        operator delete(t3l);
    }

    ds::term_t* t1;
    ds::term_t* t2n;
    ds::term_t* t2v;
    ds::term_t* t2i;
    ds::term_t* t2l;
    ds::term_t* t3v;
    ds::term_t* t3i;
    ds::term_t* t3l;
};

TEST_F(TestTerm, get_type) {
    EXPECT_EQ(t2n->get_type(), ds::term_type_t::null);
    EXPECT_EQ(t2v->get_type(), ds::term_type_t::variable);
    EXPECT_EQ(t2i->get_type(), ds::term_type_t::item);
    EXPECT_EQ(t2l->get_type(), ds::term_type_t::list);
    EXPECT_EQ(t3v->get_type(), ds::term_type_t::variable);
    EXPECT_EQ(t3i->get_type(), ds::term_type_t::item);
    EXPECT_EQ(t3l->get_type(), ds::term_type_t::list);
}

TEST_F(TestTerm, set_type) {
    EXPECT_NE(t2n->set_type(ds::term_type_t::null, nullptr), nullptr);
    EXPECT_NE(t2v->set_type(ds::term_type_t::null, nullptr), nullptr);
    EXPECT_NE(t2i->set_type(ds::term_type_t::null, nullptr), nullptr);
    EXPECT_NE(t2l->set_type(ds::term_type_t::null, nullptr), nullptr);
    EXPECT_NE(t3v->set_type(ds::term_type_t::null, nullptr), nullptr);
    EXPECT_NE(t3i->set_type(ds::term_type_t::null, nullptr), nullptr);
    EXPECT_NE(t3l->set_type(ds::term_type_t::null, nullptr), nullptr);

    EXPECT_NE(t1->set_null(nullptr), nullptr);
    EXPECT_EQ(t1->get_type(), ds::term_type_t::null);
    EXPECT_NE(t1->set_variable(nullptr), nullptr);
    EXPECT_EQ(t1->get_type(), ds::term_type_t::variable);
    EXPECT_NE(t1->set_item(nullptr), nullptr);
    EXPECT_EQ(t1->get_type(), ds::term_type_t::item);
    EXPECT_NE(t1->set_list(nullptr), nullptr);
    EXPECT_EQ(t1->get_type(), ds::term_type_t::list);

    EXPECT_EQ(t1->set_type(ds::term_type_t::list, reinterpret_cast<std::byte*>(t1)), nullptr);
    EXPECT_EQ(t1->set_type(ds::term_type_t::list, reinterpret_cast<std::byte*>(t1) + sizeof(ds::term_type_t) - 1), nullptr);
    EXPECT_NE(t1->set_type(ds::term_type_t::list, reinterpret_cast<std::byte*>(t1) + sizeof(ds::term_type_t)), nullptr);
}

TEST_F(TestTerm, get_term) {
    EXPECT_TRUE(t2n->is_null());
    EXPECT_FALSE(t2v->is_null());
    EXPECT_FALSE(t2i->is_null());
    EXPECT_FALSE(t2l->is_null());

    EXPECT_EQ(t2n->variable(), nullptr);
    EXPECT_NE(t2v->variable(), nullptr);
    EXPECT_EQ(t2i->variable(), nullptr);
    EXPECT_EQ(t2l->variable(), nullptr);

    EXPECT_EQ(t2n->item(), nullptr);
    EXPECT_EQ(t2v->item(), nullptr);
    EXPECT_NE(t2i->item(), nullptr);
    EXPECT_EQ(t2l->item(), nullptr);

    EXPECT_EQ(t2n->list(), nullptr);
    EXPECT_EQ(t2v->list(), nullptr);
    EXPECT_EQ(t2i->list(), nullptr);
    EXPECT_NE(t2l->list(), nullptr);
}

TEST_F(TestTerm, data_size) {
    EXPECT_EQ(t3v->data_size(), sizeof(ds::term_type_t) + t3v->variable()->data_size());
    EXPECT_EQ(t3i->data_size(), sizeof(ds::term_type_t) + t3i->item()->data_size());
    EXPECT_EQ(t3l->data_size(), sizeof(ds::term_type_t) + t3l->list()->data_size());
    EXPECT_EQ(t2n->data_size(), sizeof(ds::term_type_t));
}

TEST_F(TestTerm, head_tail) {
    EXPECT_EQ(t1->head(), reinterpret_cast<std::byte*>(t1));
    EXPECT_EQ(t2n->head(), reinterpret_cast<std::byte*>(t2n));
    EXPECT_EQ(t2v->head(), reinterpret_cast<std::byte*>(t2v));
    EXPECT_EQ(t2i->head(), reinterpret_cast<std::byte*>(t2i));
    EXPECT_EQ(t2l->head(), reinterpret_cast<std::byte*>(t2l));
    EXPECT_EQ(t3v->head(), reinterpret_cast<std::byte*>(t3v));
    EXPECT_EQ(t3i->head(), reinterpret_cast<std::byte*>(t3i));
    EXPECT_EQ(t3l->head(), reinterpret_cast<std::byte*>(t3l));

    EXPECT_EQ(t2n->tail(), reinterpret_cast<std::byte*>(t2n) + t2n->data_size());
    EXPECT_EQ(t3v->tail(), reinterpret_cast<std::byte*>(t3v) + t3v->data_size());
    EXPECT_EQ(t3i->tail(), reinterpret_cast<std::byte*>(t3i) + t3i->data_size());
    EXPECT_EQ(t3l->tail(), reinterpret_cast<std::byte*>(t3l) + t3l->data_size());
}

TEST_F(TestTerm, print) {
    char buffer[100];
    EXPECT_EQ(t2n->print(buffer, nullptr), nullptr);

    const char* expect_v = "`v";
    char* print_result_v = t3v->print(buffer, buffer + sizeof(buffer));
    EXPECT_NE(print_result_v, nullptr);
    *print_result_v = '\0';
    EXPECT_STREQ(buffer, expect_v);
    EXPECT_NE(t3v->print(buffer, buffer + strlen(expect_v)), nullptr);
    for (ds::length_t i = 0; i < strlen(expect_v); ++i) {
        EXPECT_EQ(t3v->print(buffer, buffer + i), nullptr);
    }

    const char* expect_i = "i";
    char* print_result_i = t3i->print(buffer, buffer + sizeof(buffer));
    EXPECT_NE(print_result_i, nullptr);
    *print_result_i = '\0';
    EXPECT_STREQ(buffer, expect_i);
    EXPECT_NE(t3i->print(buffer, buffer + strlen(expect_i)), nullptr);
    for (ds::length_t i = 0; i < strlen(expect_i); ++i) {
        EXPECT_EQ(t3i->print(buffer, buffer + i), nullptr);
    }

    const char* expect_l = "()";
    char* print_result_l = t3l->print(buffer, buffer + sizeof(buffer));
    EXPECT_NE(print_result_l, nullptr);
    *print_result_l = '\0';
    EXPECT_STREQ(buffer, expect_l);
    EXPECT_NE(t3l->print(buffer, buffer + strlen(expect_l)), nullptr);
    for (ds::length_t i = 0; i < strlen(expect_l); ++i) {
        EXPECT_EQ(t3l->print(buffer, buffer + i), nullptr);
    }
}

TEST_F(TestTerm, scan) {
    const char* input_v = "`v";
    const char* expect_v = "v";
    const char* scan_result_v = t3v->scan(input_v, nullptr);
    EXPECT_EQ(scan_result_v, input_v + strlen(input_v));
    EXPECT_STREQ(t3v->variable()->name()->get_string(), expect_v);
    EXPECT_EQ(t3v->variable()->name()->get_length(), strlen(expect_v) + 1);

    EXPECT_NE(t3v->scan(input_v, reinterpret_cast<std::byte*>(t3v) + sizeof(ds::term_type_t) + sizeof(ds::length_t) + strlen(expect_v) + 1), nullptr);
    EXPECT_EQ(t3v->scan(input_v, reinterpret_cast<std::byte*>(t3v) + sizeof(ds::term_type_t) + sizeof(ds::length_t) + strlen(expect_v)), nullptr);
    EXPECT_EQ(t3v->scan(input_v, reinterpret_cast<std::byte*>(t3v)), nullptr);

    const char* input_i = "i";
    const char* expect_i = "i";
    const char* scan_result_i = t3i->scan(input_i, nullptr);
    EXPECT_EQ(scan_result_i, input_i + strlen(input_i));
    EXPECT_STREQ(t3i->item()->name()->get_string(), expect_i);
    EXPECT_EQ(t3i->item()->name()->get_length(), strlen(expect_i) + 1);
    EXPECT_NE(t3i->scan(input_i, reinterpret_cast<std::byte*>(t3i) + sizeof(ds::term_type_t) + sizeof(ds::length_t) + strlen(expect_i) + 1), nullptr);
    EXPECT_EQ(t3i->scan(input_i, reinterpret_cast<std::byte*>(t3i) + sizeof(ds::term_type_t) + sizeof(ds::length_t) + strlen(expect_i)), nullptr);
    EXPECT_EQ(t3i->scan(input_i, reinterpret_cast<std::byte*>(t3i)), nullptr);

    const char* input_l = "()";
    const char* scan_result_l = t3l->scan(input_l, nullptr);
    EXPECT_EQ(scan_result_l, input_l + strlen(input_l));
    EXPECT_EQ(t3l->list()->get_list_size(), 0);
    EXPECT_NE(t3l->scan(input_l, reinterpret_cast<std::byte*>(t3l) + sizeof(ds::term_type_t) + sizeof(ds::length_t)), nullptr);
    EXPECT_EQ(t3l->scan(input_l, reinterpret_cast<std::byte*>(t3l) + sizeof(ds::term_type_t) + sizeof(ds::length_t) - 1), nullptr);
    EXPECT_EQ(t3l->scan(input_l, reinterpret_cast<std::byte*>(t3l)), nullptr);
}
