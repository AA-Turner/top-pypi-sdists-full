#include <algorithm>
#include <optional>
#include <stdint.h>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>


#include <catch2/catch_all.hpp>
#include <catch2/catch_test_macros.hpp>


#include "cdfpp/cdf-io/loading/records-loading.hpp"
#include <cpp_utils/serde/serde.hpp>

using cdf::io::cdf_record_endianness;
using cpp_utils::reflexion::count_members;
using cpp_utils::serde::bounded_string;
using cpp_utils::serde::dynamic_array;
using cpp_utils::serde::unused;

SCENARIO("record loading", "[CDF]")
{
    GIVEN("a simple two char fields record")
    {
        struct two_chars
        {
            char a;
            char b;
        };
        two_chars s { 'a', 'b' };
        THEN("we can load it from a buffer")
        {
            std::string buffer { "cd" };
            cdf::io::load_record(s, buffer, 0);
            REQUIRE(s.a == 'c');
            REQUIRE(s.b == 'd');
        }
    }
    GIVEN("a simple two char fields record with an unused field")
    {
        struct two_chars
        {
            char a;
            unused<char> b;
        };
        two_chars s { 'a', { 'b' } };
        THEN("we can load it from a buffer")
        {
            std::string buffer { "cd" };
            cdf::io::load_record(s, buffer, 0);
            REQUIRE(s.a == 'c');
            REQUIRE(s.b.value == 'b');
        }
    }
    GIVEN("a more complex record")
    {
        struct complex_record
        {
            using endianness = cdf_record_endianness;
            char a;
            double b;
            uint32_t c;
            uint64_t d;
        };
        THEN("we can load it from a buffer")
        {
            complex_record s { 0, 0., 0, 0 };
            std::array<char, 21> buffer { 0x2A, 0x40, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2A };
            cdf::io::load_record(s, buffer, 0);
            REQUIRE(s.a == 42);
            REQUIRE(s.b == 42.);
            REQUIRE(s.c == 42);
            REQUIRE(s.d == 42);
        }
        THEN("we can load it from a buffer with an offset")
        {
            complex_record s { 0, 0., 0, 0 };
            std::array<char, 22> buffer { 0x11, 0x2A, 0x40, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2A };
            cdf::io::load_record(s, buffer, 1);
            REQUIRE(s.a == 42);
            REQUIRE(s.b == 42.);
            REQUIRE(s.c == 42);
            REQUIRE(s.d == 42);
        }
    }
    GIVEN("a record with nested record")
    {
        struct inner_record
        {
            using endianness = cdf_record_endianness;
            uint16_t a;
            uint16_t b;
        };
        struct outer_record
        {
            char a;
            inner_record b;
            char c;
        };
        THEN("we can load it from a buffer")
        {
            outer_record s { 0, { 0, 0 }, 0 };
            std::array<char, 6> buffer { 0x2A, 0x0, 0x2A, 0x0, 0x2A, 0x2A };
            cdf::io::load_record(s, buffer, 0);
            REQUIRE(s.a == 42);
            REQUIRE(s.b.a == 42);
            REQUIRE(s.b.b == 42);
            REQUIRE(s.c == 42);
        }
    }
    GIVEN("a record with string fields")
    {
        struct record_with_string
        {
            using endianness = cdf_record_endianness;
            char a;
            double b;
            bounded_string<8> c;
            uint64_t d;
        };
        THEN("we can load it from a buffer")
        {
            record_with_string s { 0, 0., { "" }, 0 };
            std::array<char, 25> buffer { 0x2A, 0x40, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 'h',
                'e', 'l', 'l', 'o', 0, 0, 0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2A };
            cdf::io::load_record(s, buffer, 0);
            REQUIRE(s.a == 42);
            REQUIRE(s.b == 42.);
            REQUIRE(s.c.value == "hello");
            REQUIRE(s.d == 42);
        }
    }
    GIVEN("a record with table fields")
    {
        struct record_table_fields
        {
            using endianness = cdf_record_endianness;
            char a;
            double b;
            dynamic_array<0, uint16_t> c;
            uint64_t d;
            dynamic_array<1, uint32_t> e;

            std::size_t field_size(const dynamic_array<0, uint16_t>&) const { return this->a; }
            std::size_t field_size(const dynamic_array<1, uint32_t>&) const { return 2; }
        };
        THEN("we can load it from a buffer")
        {
            record_table_fields s {};
            std::array<char, 33> buffer { 0x4, 0x40, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0,
                0x01, 0x0, 0x2, 0x0, 0x3, 0x0, 0x4, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2A,
                0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02 };
            cdf::io::load_record(s, buffer, 0);
            REQUIRE(s.a == 4);
            REQUIRE(s.b == 42.);
            REQUIRE(std::vector<uint16_t>(s.c.begin(), s.c.end())
                == std::vector<uint16_t> { 1, 2, 3, 4 });
            REQUIRE(s.d == 42);
            REQUIRE(
                std::vector<uint32_t>(s.e.begin(), s.e.end()) == std::vector<uint32_t> { 1, 2 });
            static_assert(count_members<decltype(s)> == 5);
        }
    }
}
