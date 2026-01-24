#ifndef DS_VARIABLE_HH
#define DS_VARIABLE_HH

#include <cstddef>

#include <ds/config.hh>
#include <ds/string.hh>

namespace ds {
    /// @brief variable_t对象。
    ///
    /// 内存分布:
    /// 1. name : string_t。
    ///
    /// 可能的状态有：
    /// 1. 未初始化name；
    /// 2. 已经设置了name。
    class variable_t {
      public:
        /// @brief 获取variable的name指针。
        /// @return variable的name指针。
        ///
        /// 可以在状态1、2的情况下调用此函数。
        string_t* name();

        /// @brief 获取variable_t对象的大小。
        /// @return variable_t对象的大小。
        length_t data_size();

        /// @brief 获取variable_t对象的头字节指针。
        /// @return variable_t对象的头字节指针。
        std::byte* head();

        /// @brief 获取variable_t对象的尾字节指针。
        /// @return variable_t对象的尾字节指针。
        std::byte* tail();

        /// @brief 将variable_t对象输出至buffer。
        /// @param buffer 待被输出的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输出后的buffer指针，如果尾指针检查失败则返回nullptr。
        char* print(char* buffer, char* check_tail = nullptr);

        /// @brief 从buffer中输入variable_t对象。
        /// @param buffer 待输入的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输入后的buffer指针，如果尾指针检查失败则返回nullptr。
        const char* scan(const char* buffer, std::byte* check_tail = nullptr);
    };
} // namespace ds

#endif
