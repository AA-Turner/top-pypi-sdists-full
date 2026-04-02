#include <cstring>

#include <ds/helper.hh>
#include <ds/string.hh>

namespace ds {
    length_t* string_t::length_pointer() {
        return reinterpret_cast<length_t*>(this);
    }

    char* string_t::string_pointer() {
        return reinterpret_cast<char*>(reinterpret_cast<std::byte*>(this) + sizeof(length_t));
    }

    length_t string_t::get_length() {
        return *length_pointer();
    }

    string_t* string_t::set_length(length_t length, std::byte* check_tail) {
        if (check_before_fail(check_tail, string_pointer(), length)) [[unlikely]] {
            return nullptr;
        }
        *length_pointer() = length;
        return this;
    }

    char* string_t::get_string() {
        return string_pointer();
    }

    string_t* string_t::set_string(const char* buffer) {
        const char* src = buffer;
        char* dst = get_string();
        bool end = false;
        for (length_t index = 0; index < get_length() - 1; ++index) {
            if (end) {
                dst[index] = 0;
            } else {
                dst[index] = src[index];
                if (src[index] == 0) {
                    end = true;
                }
            }
        }
        dst[get_length() - 1] = 0;
        return this;
    }

    string_t* string_t::set_null_string(const char* buffer, std::byte* check_tail) {
        length_t length = strlen(buffer) + 1;
        if (check_before_fail(check_tail, string_pointer(), length)) [[unlikely]] {
            return nullptr;
        }
        set_length(length, nullptr);
        set_string(buffer);
        return this;
    }

    length_t string_t::data_size() {
        return sizeof(length_t) + sizeof(char) * get_length();
    }

    std::byte* string_t::head() {
        return reinterpret_cast<std::byte*>(this);
    }

    std::byte* string_t::tail() {
        return head() + data_size();
    }

    char* string_t::print(char* buffer, char* check_tail) {
        char* src = get_string();
        char* dst = buffer;
        while (*src) {
            if (check_till_fail(check_tail, dst)) [[unlikely]] {
                return nullptr;
            }
            *(dst++) = *(src++);
        }
        return dst;
    }

    const char* string_t::scan(const char* buffer, std::byte* check_tail) {
        const char* src = buffer;
        char* dst = get_string();
        while (true) {
            if (strchr("`() \t\r\n", *src) != nullptr) {
                break;
            }
            if (check_till_fail(check_tail, dst)) [[unlikely]] {
                return nullptr;
            }
            *(dst++) = *(src++);
        }
        if (check_till_fail(check_tail, dst)) [[unlikely]] {
            return nullptr;
        }
        *dst = 0;
        set_length(strlen(get_string()) + 1, nullptr);
        return src;
    }
} // namespace ds
