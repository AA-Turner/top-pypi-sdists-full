#include <cstring>

#include <ds/helper.hh>
#include <ds/list.hh>
#include <ds/term.hh>

namespace ds {
    length_t* list_t::list_size_pointer() {
        return reinterpret_cast<length_t*>(this);
    }

    length_t* list_t::term_size_pointer(length_t index) {
        if (index < 0 || index > get_list_size()) [[unlikely]] {
            return nullptr;
        }
        return reinterpret_cast<length_t*>(reinterpret_cast<std::byte*>(this) + sizeof(length_t) + sizeof(length_t) * index);
    }

    term_t* list_t::term_pointer(length_t index) {
        if (index < 0 || index >= get_list_size()) [[unlikely]] {
            return nullptr;
        }
        return reinterpret_cast<term_t*>(reinterpret_cast<std::byte*>(term_size_pointer(get_list_size())) + term_size(index - 1));
    }

    length_t list_t::get_list_size() {
        return *list_size_pointer();
    }

    list_t* list_t::set_list_size(length_t list_size, std::byte* check_tail) {
        if (check_before_fail(check_tail, this, sizeof(length_t) + sizeof(length_t) * list_size)) [[unlikely]] {
            return nullptr;
        }
        *list_size_pointer() = list_size;
        for (length_t index = 0; index < get_list_size(); ++index) {
            *term_size_pointer(index) = 0;
        }
        return this;
    }

    length_t list_t::term_size(length_t index) {
        if (index == -1) {
            return 0;
        }
        return *term_size_pointer(index);
    }

    term_t* list_t::term(length_t index) {
        return term_pointer(index);
    }

    void list_t::update_term_size(length_t index) {
        *term_size_pointer(index) = term(index)->data_size() + term_size(index - 1);
    }

    length_t list_t::data_size() {
        return sizeof(length_t) + sizeof(length_t) * get_list_size() + term_size(get_list_size() - 1);
    }

    std::byte* list_t::head() {
        return reinterpret_cast<std::byte*>(this);
    }

    std::byte* list_t::tail() {
        return head() + data_size();
    }

    char* list_t::print(char* buffer, char* check_tail) {
        if (check_till_fail(check_tail, buffer)) [[unlikely]] {
            return nullptr;
        }
        *(buffer++) = '(';
        for (length_t index = 0; index < get_list_size(); ++index) {
            if (index != 0) {
                if (check_till_fail(check_tail, buffer)) [[unlikely]] {
                    return nullptr;
                }
                *(buffer++) = ' ';
            }
            buffer = term(index)->print(buffer, check_tail);
            if (buffer == nullptr) [[unlikely]] {
                return nullptr;
            }
        }
        if (check_till_fail(check_tail, buffer)) [[unlikely]] {
            return nullptr;
        }
        *(buffer++) = ')';
        return buffer;
    }

    const char* list_t::scan(const char* buffer, std::byte* check_tail) {
        // 将当前对象的数据暂时作为buffer，以此读取若干个term
        // 在读取的过程中统计list size
        // 在读取完毕后，将当前对象的数据整体向后移动，留出放置list size和各个term size的空间并填写
        ++buffer;
        term_t* term = reinterpret_cast<term_t*>(this);
        length_t list_size = 0;
        while (true) {
            if (*buffer == ')') {
                ++buffer;
                break;
            }
            if (strchr(" \t\r\n", *buffer)) {
                ++buffer;
                continue;
            }
            buffer = term->scan(buffer, check_tail);
            if (buffer == nullptr) [[unlikely]] {
                return nullptr;
            }
            term = reinterpret_cast<term_t*>(term->tail());
            ++list_size;
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
        // 向后移动数据后，不需要检查前面的空间是否足够
        set_list_size(list_size, nullptr);
        for (length_t index = 0; index < list_size; ++index) {
            update_term_size(index);
        }
        return buffer;
    }
} // namespace ds
