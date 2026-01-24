#ifndef DS_STRING_HH
#define DS_STRING_HH

#include <cstddef>

#include <ds/config.hh>

namespace ds {
    /// @brief string_t对象。
    ///
    /// 内存分布：
    /// 1. length : length_t；
    /// 2. string : char[length]。
    ///
    /// 可能的状态有：
    /// 1. 未初始化状态，length不正确，string不正确；
    /// 2. 已经设置了长度，但是字符串没有设置，length正确，string不正确；
    /// 3. 已经设置了长度和字符串，length和string都是正确的。
    class string_t {
        /// @brief 获取字符串长度的指针。
        /// @return 字符串长度的指针。
        ///
        /// 可以在状态1、2、3的情况下调用此函数。
        length_t* length_pointer();

        /// @brief 获取字符串本身的指针。
        /// @return 字符串本身的指针。
        ///
        /// 可以在状态1、2、3的情况下调用此函数。
        char* string_pointer();

      public:
        /// @brief 获取字符串的长度。
        /// @return 字符串的长度。
        ///
        /// 可以在状态2、3的情况下调用此函数。
        length_t get_length();

        /// @brief 设置字符串的长度。
        /// @param length 字符串的新长度。
        /// @param check_tail 可选的尾指针检查。
        /// @return string_t对象的指针，如果尾指针失败则返回nullptr。
        ///
        /// 可以在1、2、3的状态下调用此函数，调用后会将状态变为2，除非设置的长度是通过字符串长度得到的，那样回到状态3。
        string_t* set_length(length_t length, std::byte* check_tail = nullptr);

        /// @brief 获取字符串本身。
        /// @return 字符串本身。
        ///
        /// 可以在状态1、2、3的情况下调用此函数。
        char* get_string();

        /// @brief 设置字符串本身。
        /// @param buffer 新的字符串。
        /// @return string_t对象的指针。
        ///
        /// 可以在状态2、3的情况下调用此函数，调用后会将状态变为3。
        ///
        /// @note 超出长度的部分将被截断。
        /// @note 因为已经设置了长度才可以调用此函数，因此此函数不需要做尾指针检查。
        string_t* set_string(const char* buffer);

        /// @brief 设置字符串本身。
        /// @param buffer null结尾的新的字符串。
        /// @param check_tail 可选的尾指针检查。
        /// @return string_t对象的指针，如果尾指针失败则返回nullptr。
        ///
        /// 可以在状态1、2、3的情况下调用此函数，调用后会将状态变为3。
        string_t* set_null_string(const char* buffer, std::byte* check_tail = nullptr);

        /// @brief 获取string_t对象的大小。
        /// @return string_t对象的大小。
        length_t data_size();

        /// @brief 获取string_t对象的头字节指针。
        /// @return string_t对象的头字节指针。
        std::byte* head();

        /// @brief 获取string_t对象的尾字节指针。
        /// @return string_t对象的尾字节指针。
        std::byte* tail();

        /// @brief 将string_t对象输出至buffer。
        /// @param buffer 待被输出的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输出后的buffer指针，如果尾指针检查失败则返回nullptr。
        char* print(char* buffer, char* check_tail = nullptr);

        /// @brief 从buffer中输入string_t对象。
        /// @param buffer 待输入的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输入后的buffer指针，如果尾指针检查失败则返回nullptr。
        const char* scan(const char* buffer, std::byte* check_tail = nullptr);
    };
} // namespace ds

#endif
