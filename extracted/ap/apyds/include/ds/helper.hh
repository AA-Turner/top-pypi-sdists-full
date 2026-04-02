#ifndef DS_HELPER_HH
#define DS_HELPER_HH

#include <cstddef>

#include <ds/config.hh>

namespace ds {
    template<typename T1, typename T2>
    bool check_before_fail(T1* check_tail, T2* target_tail, length_t offset = 0) {
        if (check_tail != nullptr) {
            if (reinterpret_cast<std::byte*>(check_tail) < reinterpret_cast<std::byte*>(target_tail) + offset) [[unlikely]] {
                return true;
            }
        }
        return false;
    }

    template<typename T1, typename T2>
    bool check_till_fail(T1* check_tail, T2* target_tail, length_t offset = 0) {
        if (check_tail != nullptr) {
            if (reinterpret_cast<std::byte*>(check_tail) <= reinterpret_cast<std::byte*>(target_tail) + offset) [[unlikely]] {
                return true;
            }
        }
        return false;
    }
} // namespace ds

#endif
