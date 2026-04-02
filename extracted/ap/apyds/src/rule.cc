#include <cstring>

#include <ds/helper.hh>
#include <ds/rule.hh>

namespace ds {
    term_t* rule_t::conclusion() {
        if (get_list_size() > 0) [[likely]] {
            return term(get_list_size() - 1);
        } else {
            return nullptr;
        }
    }

    term_t* rule_t::only_conclusion() {
        if (get_list_size() == 1) [[likely]] {
            return term(0);
        } else {
            return nullptr;
        }
    }

    term_t* rule_t::premises(length_t index) {
        if (index < 0 || index >= get_list_size() - 1) [[unlikely]] {
            return nullptr;
        }
        return term(index);
    }

    length_t rule_t::premises_count() {
        return get_list_size() - 1;
    }

    bool rule_t::valid() {
        return get_list_size() != 0;
    }

    rule_t* rule_t::set_null(std::byte* check_tail) {
        if (set_list_size(0, check_tail) == nullptr) [[unlikely]] {
            return nullptr;
        }
        return this;
    }

    length_t rule_t::data_size() {
        return list_t::data_size();
    }

    std::byte* rule_t::head() {
        return reinterpret_cast<std::byte*>(this);
    }

    std::byte* rule_t::tail() {
        return head() + data_size();
    }

    char* rule_t::print(char* buffer, char* check_tail) {
        if (!valid()) [[unlikely]] {
            return nullptr;
        }
        // 记录premises的最大长度用于分割符的长度
        length_t max_length = 4;
        // 打印当前term之前的buffer位置
        char* last_buffer = buffer;
        for (length_t index = 0; index < premises_count(); ++index) {
            buffer = premises(index)->print(buffer, check_tail);
            if (buffer == nullptr) [[unlikely]] {
                return nullptr;
            }
            length_t this_length = buffer - last_buffer;
            max_length = this_length > max_length ? this_length : max_length;
            if (check_till_fail(check_tail, buffer)) [[unlikely]] {
                return nullptr;
            }
            *(buffer++) = '\n';
            last_buffer = buffer;
        }
        if (check_till_fail(check_tail, buffer, max_length)) [[unlikely]] {
            return nullptr;
        }
        for (length_t length = 0; length < max_length; ++length) {
            *(buffer++) = '-';
        }
        *(buffer++) = '\n';
        buffer = conclusion()->print(buffer, check_tail);
        if (buffer == nullptr) [[unlikely]] {
            return nullptr;
        }
        if (check_till_fail(check_tail, buffer)) [[unlikely]] {
            return nullptr;
        }
        *(buffer++) = '\n';
        return buffer;
    }

    const char* rule_t::scan(const char* buffer, std::byte* check_tail) {
        // 先将当前对象的数据暂时作为buffer，以此读取若干个term
        // 在读取的过程中统计conclusion和premises的总数目
        // 在读取完毕后，将当前对象的数据整体向后移动，留出放置元信息的位置并填写
        term_t* term = reinterpret_cast<term_t*>(this);
        length_t list_size = 0;
        bool last_one = false;
        while (true) {
            if (*buffer == '\0') {
                break;
            }
            if (strchr(" \t\r\n", *buffer)) {
                ++buffer;
                continue;
            }
            if (buffer[0] == '-' && buffer[1] == '-') {
                while (*(buffer++) == '-') {
                }
                last_one = true;
                continue;
            }
            buffer = term->scan(buffer, check_tail);
            if (buffer == nullptr) [[unlikely]] {
                return nullptr;
            }
            term = reinterpret_cast<term_t*>(term->tail());
            ++list_size;
            if (last_one) {
                break;
            }
        }
        length_t offset = sizeof(length_t) + sizeof(length_t) * list_size;
        if (check_before_fail(check_tail, term, offset)) [[unlikely]] {
            return nullptr;
        }
        memmove(
            reinterpret_cast<std::byte*>(this) + offset,
            reinterpret_cast<std::byte*>(this),
            reinterpret_cast<std::byte*>(term) - reinterpret_cast<std::byte*>(this)
        );
        set_list_size(list_size, nullptr);
        for (length_t index = 0; index < list_size; ++index) {
            update_term_size(index);
        }
        return buffer;
    }
} // namespace ds
