#include <ds/helper.hh>
#include <ds/variable.hh>

namespace ds {
    string_t* variable_t::name() {
        return reinterpret_cast<string_t*>(this);
    }

    length_t variable_t::data_size() {
        return name()->data_size();
    }

    std::byte* variable_t::head() {
        return reinterpret_cast<std::byte*>(this);
    }

    std::byte* variable_t::tail() {
        return head() + data_size();
    }

    char* variable_t::print(char* buffer, char* check_tail) {
        if (check_till_fail(check_tail, buffer)) [[unlikely]] {
            return nullptr;
        }
        *(buffer++) = '`';
        return name()->print(buffer, check_tail);
    }

    const char* variable_t::scan(const char* buffer, std::byte* check_tail) {
        return name()->scan(buffer + 1, check_tail);
    }
} // namespace ds
