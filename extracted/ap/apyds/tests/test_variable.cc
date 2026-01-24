#include <ds/variable.hh>
#include <gtest/gtest.h>

class TestVariable : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 100;
    const char* v2_name = "Hello";

    TestVariable() { }
    ~TestVariable() override { }
    void SetUp() override {
        v1 = reinterpret_cast<ds::variable_t*>(operator new(buffer_size));
        v2 = reinterpret_cast<ds::variable_t*>(operator new(buffer_size));

        v2->name()->set_null_string(v2_name, nullptr);
    }
    void TearDown() override {
        operator delete(v1);
        operator delete(v2);
    }

    ds::variable_t* v1;
    ds::variable_t* v2;
};

TEST_F(TestVariable, name) {
    EXPECT_EQ(v1->name(), reinterpret_cast<ds::string_t*>(v1));
    EXPECT_EQ(v2->name(), reinterpret_cast<ds::string_t*>(v2));
}

TEST_F(TestVariable, data_size) {
    EXPECT_EQ(v2->data_size(), sizeof(ds::length_t) + strlen(v2_name) + 1);
}

TEST_F(TestVariable, head_tail) {
    EXPECT_EQ(v1->head(), reinterpret_cast<std::byte*>(v1));
    EXPECT_EQ(v2->head(), reinterpret_cast<std::byte*>(v2));
    EXPECT_EQ(v2->tail(), reinterpret_cast<std::byte*>(v2) + v2->data_size());
}

TEST_F(TestVariable, print) {
    char long_buffer[100];
    const char* expect = "`Hello";
    char* print_result = v2->print(long_buffer, long_buffer + sizeof(long_buffer));
    EXPECT_EQ(print_result, long_buffer + strlen(v2_name) + 1);
    for (ds::length_t i = 0; i < strlen(v2_name) + 1; ++i) {
        EXPECT_EQ(long_buffer[i], expect[i]);
    }

    EXPECT_EQ(v2->print(long_buffer, long_buffer), nullptr);
    EXPECT_NE(v2->print(long_buffer, long_buffer + strlen(v2_name) + 1), nullptr);
    EXPECT_EQ(v2->print(long_buffer, long_buffer + strlen(v2_name)), nullptr);
}

TEST_F(TestVariable, scan) {
    const char* input = "`World World";
    const char* expect = "World";
    const char* scan_result = v2->scan(input, nullptr);
    EXPECT_EQ(scan_result, input + strlen(expect) + 1);
    EXPECT_STREQ(v2->name()->get_string(), expect);
    EXPECT_EQ(v2->name()->get_length(), strlen(expect) + 1);

    EXPECT_NE(v2->scan(input, reinterpret_cast<std::byte*>(v2) + sizeof(ds::length_t) + strlen(expect) + 1), nullptr);
    EXPECT_EQ(v2->scan(input, reinterpret_cast<std::byte*>(v2) + sizeof(ds::length_t) + strlen(expect)), nullptr);
}
