#include <ds/item.hh>
#include <gtest/gtest.h>

class TestItem : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 100;
    const char* i2_name = "Hello";

    TestItem() { }
    ~TestItem() override { }
    void SetUp() override {
        i1 = reinterpret_cast<ds::item_t*>(operator new(buffer_size));
        i2 = reinterpret_cast<ds::item_t*>(operator new(buffer_size));

        i2->name()->set_null_string(i2_name, nullptr);
    }
    void TearDown() override {
        operator delete(i1);
        operator delete(i2);
    }

    ds::item_t* i1;
    ds::item_t* i2;
};

TEST_F(TestItem, name) {
    EXPECT_EQ(i1->name(), reinterpret_cast<ds::string_t*>(i1));
    EXPECT_EQ(i2->name(), reinterpret_cast<ds::string_t*>(i2));
}

TEST_F(TestItem, data_size) {
    EXPECT_EQ(i2->data_size(), sizeof(ds::length_t) + strlen(i2_name) + 1);
}

TEST_F(TestItem, head_tail) {
    EXPECT_EQ(i1->head(), reinterpret_cast<std::byte*>(i1));
    EXPECT_EQ(i2->head(), reinterpret_cast<std::byte*>(i2));
    EXPECT_EQ(i2->tail(), reinterpret_cast<std::byte*>(i2) + i2->data_size());
}

TEST_F(TestItem, print) {
    char long_buffer[100];
    const char* expect = "Hello";
    char* print_result = i2->print(long_buffer, long_buffer + sizeof(long_buffer));
    EXPECT_EQ(print_result, long_buffer + strlen(i2_name));
    for (ds::length_t i = 0; i < strlen(i2_name); ++i) {
        EXPECT_EQ(long_buffer[i], expect[i]);
    }

    EXPECT_EQ(i2->print(long_buffer, long_buffer), nullptr);
    EXPECT_NE(i2->print(long_buffer, long_buffer + strlen(i2_name)), nullptr);
    EXPECT_EQ(i2->print(long_buffer, long_buffer + strlen(i2_name) - 1), nullptr);
}

TEST_F(TestItem, scan) {
    const char* input = "World World";
    const char* expect = "World";
    const char* scan_result = i2->scan(input, nullptr);
    EXPECT_EQ(scan_result, input + strlen(expect));
    EXPECT_STREQ(i2->name()->get_string(), expect);
    EXPECT_EQ(i2->name()->get_length(), strlen(expect) + 1);

    EXPECT_NE(i2->scan(input, reinterpret_cast<std::byte*>(i2) + sizeof(ds::length_t) + strlen(expect) + 1), nullptr);
    EXPECT_EQ(i2->scan(input, reinterpret_cast<std::byte*>(i2) + sizeof(ds::length_t) + strlen(expect)), nullptr);
}
