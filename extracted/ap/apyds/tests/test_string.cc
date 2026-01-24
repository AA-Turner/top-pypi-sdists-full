#include <ds/string.hh>
#include <gtest/gtest.h>

class TestString : public ::testing::Test {
  protected:
    const ds::length_t buffer_size = 100;
    const ds::length_t s2_length = 10;
    const char* s3_string = "Hello";

    TestString() { }
    ~TestString() override { }
    void SetUp() override {
        s1 = reinterpret_cast<ds::string_t*>(operator new(buffer_size));
        s2 = reinterpret_cast<ds::string_t*>(operator new(buffer_size));
        s3 = reinterpret_cast<ds::string_t*>(operator new(buffer_size));

        s2->set_length(s2_length, nullptr);

        s3->set_null_string(s3_string, nullptr);
    }
    void TearDown() override {
        operator delete(s1);
        operator delete(s2);
        operator delete(s3);
    }

    ds::string_t* s1;
    ds::string_t* s2;
    ds::string_t* s3;
};

TEST_F(TestString, get_length) {
    EXPECT_EQ(s2->get_length(), s2_length);
    EXPECT_EQ(s3->get_length(), strlen(s3_string) + 1);
}

TEST_F(TestString, set_length) {
    ds::length_t new_length = 20;
    EXPECT_EQ(s1->set_length(new_length, nullptr), s1);
    EXPECT_EQ(s1->get_length(), new_length);
    EXPECT_EQ(s2->set_length(new_length, nullptr), s2);
    EXPECT_EQ(s2->get_length(), new_length);
    EXPECT_EQ(s3->set_length(new_length, nullptr), s3);
    EXPECT_EQ(s3->get_length(), new_length);

    EXPECT_EQ(s2->set_length(buffer_size - sizeof(ds::length_t) + 1, reinterpret_cast<std::byte*>(s2) + buffer_size), nullptr);
    EXPECT_NE(s2->set_length(buffer_size - sizeof(ds::length_t), reinterpret_cast<std::byte*>(s2) + buffer_size), nullptr);
}

TEST_F(TestString, get_string) {
    EXPECT_EQ(s1->get_string(), reinterpret_cast<char*>(s1) + sizeof(ds::length_t));
    EXPECT_EQ(s2->get_string(), reinterpret_cast<char*>(s2) + sizeof(ds::length_t));
    EXPECT_EQ(s3->get_string(), reinterpret_cast<char*>(s3) + sizeof(ds::length_t));
}

TEST_F(TestString, set_string) {
    char* str = s2->get_string();

    const char* short_string = "World";
    EXPECT_EQ(s2->set_string(short_string), s2);
    EXPECT_STREQ(s2->get_string(), short_string);
    for (ds::length_t i = 0; i < s2->get_length(); ++i) {
        if (i < strlen(short_string)) {
            EXPECT_EQ(str[i], short_string[i]);
        } else {
            EXPECT_EQ(str[i], '\0');
        }
    }

    const char* long_string = "This is a very long string that exceeds the original length.";
    EXPECT_EQ(s2->set_string(long_string), s2);
    EXPECT_STRNE(s2->get_string(), long_string);
    for (ds::length_t i = 0; i < s2->get_length() - 1; ++i) {
        EXPECT_EQ(str[i], long_string[i]);
    }
    EXPECT_EQ(str[s2->get_length() - 1], '\0');
}

TEST_F(TestString, set_null_string) {
    char* str = s2->get_string();

    const char* short_string = "World";
    EXPECT_EQ(s2->set_null_string(short_string, nullptr), s2);
    EXPECT_STREQ(s2->get_string(), short_string);
    EXPECT_EQ(s2->get_length(), strlen(short_string) + 1);

    const char* empty_string = "";
    EXPECT_EQ(s2->set_null_string(empty_string, nullptr), s2);
    EXPECT_STREQ(s2->get_string(), empty_string);
    EXPECT_EQ(s2->get_length(), 1);

    const char* long_string = "This is a very long string that exceeds the original length.";
    EXPECT_EQ(s2->set_null_string(long_string, reinterpret_cast<std::byte*>(s2) + 10), nullptr);

    EXPECT_EQ(s2->set_null_string(short_string, reinterpret_cast<std::byte*>(s2) + strlen(short_string) + sizeof(ds::length_t)), nullptr);
    EXPECT_EQ(s2->set_null_string(short_string, reinterpret_cast<std::byte*>(s2) + strlen(short_string) + sizeof(ds::length_t) + 1), s2);
}

TEST_F(TestString, data_size) {
    EXPECT_EQ(s2->data_size(), sizeof(ds::length_t) + sizeof(char) * s2->get_length());
    EXPECT_EQ(s3->data_size(), sizeof(ds::length_t) + sizeof(char) * s3->get_length());
}

TEST_F(TestString, head_tail) {
    EXPECT_EQ(s1->head(), reinterpret_cast<std::byte*>(s1));
    EXPECT_EQ(s2->head(), reinterpret_cast<std::byte*>(s2));
    EXPECT_EQ(s3->head(), reinterpret_cast<std::byte*>(s3));
    EXPECT_EQ(s2->tail(), reinterpret_cast<std::byte*>(s2) + s2->data_size());
    EXPECT_EQ(s3->tail(), reinterpret_cast<std::byte*>(s3) + s3->data_size());
}

TEST_F(TestString, print) {
    char long_buffer[100];
    char* print_result = s3->print(long_buffer, long_buffer + sizeof(long_buffer));
    EXPECT_NE(print_result, nullptr);
    for (ds::length_t i = 0; i < s3->get_length() - 1; ++i) {
        EXPECT_EQ(long_buffer[i], s3->get_string()[i]);
    }
    EXPECT_EQ(print_result, long_buffer + s3->get_length() - 1);

    EXPECT_EQ(s3->print(long_buffer, long_buffer + strlen(s3->get_string() - 1)), nullptr);
    EXPECT_NE(s3->print(long_buffer, long_buffer + strlen(s3->get_string())), nullptr);
}

TEST_F(TestString, scan) {
    const char* input = "Hello World";
    const char* expect = "Hello";
    const char* scan_result = s3->scan(input, nullptr);
    EXPECT_EQ(scan_result, input + strlen(expect));
    EXPECT_STREQ(s3->get_string(), expect);
    EXPECT_EQ(s3->get_length(), strlen(expect) + 1);

    EXPECT_NE(s3->scan(input, reinterpret_cast<std::byte*>(s3) + sizeof(ds::length_t) + strlen(expect) + 1), nullptr);
    EXPECT_EQ(s3->scan(input, reinterpret_cast<std::byte*>(s3) + sizeof(ds::length_t) + strlen(expect)), nullptr);
    EXPECT_EQ(s3->scan(input, reinterpret_cast<std::byte*>(s3) + sizeof(ds::length_t) + strlen(expect) - 1), nullptr);
}
