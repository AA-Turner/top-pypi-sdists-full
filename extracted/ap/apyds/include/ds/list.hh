#ifndef DS_LIST_HH
#define DS_LIST_HH

#include <cstddef>

#include <ds/config.hh>

namespace ds {
    class term_t;

    /// @brief list_t对象。
    ///
    /// 内存分布:
    /// 1. list_size : length_t；
    /// 2. term_size : length_t[list_size]；
    /// 3. term : term_t[list_size]。
    ///
    /// 可能的状态有：
    /// 1. 完全没有初始化；
    /// 2(4.-1). 仅仅设置了list size；
    /// 3.x 已经设置了list size，term设置到第x个，term size设置到第x-1个；
    /// 4.x 已经设置了list size，term设置到第x个，term size设置到第x个。
    /// 这里的x可以从1取到list size。
    ///
    /// @note 这里的term_size是前若干个term的累计大小。
    /// @note 正常的初始化流程是：
    /// `1 -> 2 -> 3.0 -> 4.0 -> 3.1 -> 4.1 -> ... -> 3.(n-1) -> 4.(n-1)`
    /// 其中n是list size。
    class list_t {
        /// @brief 获取list大小的指针。
        /// @return list大小的指针。
        ///
        /// 可以在1、2、3.x、4.x的状态下调用此函数。
        length_t* list_size_pointer();

        /// @brief 获取前若干个term总大小的指针。
        /// @param index 需要计算的term中最后一个的指标。
        /// @return 前若干个term总大小的指针，溢出则返回nullptr。
        ///
        /// 可以在2、3.x、4.x的状态下调用此函数。
        ///
        /// @note 当index = 0时, 返回的是第0个term的大小的指针;
        /// 当index = list_size - 1时, 返回的是所有term的总大小的指针。
        /// @note 如果index = list_size，此时可以获取溢出的指针，将得到第0个term的指针。
        length_t* term_size_pointer(length_t index);

        /// @brief 获取某个term的指针。
        /// @param index 某个term的指标。
        /// @return 某个term的指针，溢出则返回nullptr。
        ///
        /// index = 0时，可以在2、3.x、4.x的状态下调用此函数；
        /// index > 0时，可以在3.j、4.k的状态下调用此函数，其中j>=index，k>=index - 1。
        term_t* term_pointer(length_t index);

      public:
        /// @brief 获取list大小。
        /// @return list大小。
        ///
        /// 可以在2、3.x、4.x的状态下调用此函数。
        length_t get_list_size();

        /// @brief 设置list大小。
        /// @param list_size 新的list大小。
        /// @param check_tail 可选的尾指针检查。
        /// @return list_t对象的指针，如果尾指针失败则返回nullptr。
        ///
        /// 可以在1、2、3.x、4.x的状态下调用此函数，调用后会将状态变为2。
        /// 也可以在手动放置后续所有的term和term size后调用次函数来到达4.(n-1)的状态，其中n是list size。
        list_t* set_list_size(length_t list_size, std::byte* check_tail = nullptr);

        /// @brief 获取前若干个term总大小。
        /// @param index 需要计算的term中最后一个的指标。
        /// @return 前若干个term总大小。
        ///
        /// 可以在3.j、4.k的状态下调用此函数，其中j>=index + 1，k>=index。
        ///
        /// @note 当index = 0时, 返回的是第0个term的大小;
        /// 当index = list_size - 1时, 返回的是所有term的总大小的。
        /// @note 当index = -1时，返回0。
        /// @note 其他index溢出情况行为未定义。
        length_t term_size(length_t index);

        /// @brief 获取某个term的指针。
        /// @param index 某个term的指标。
        /// @return 某个term的指针，溢出则返回nullptr。
        ///
        /// index = 0时，可以在2、3.x、4.x的状态下调用此函数；
        /// index > 0时，可以在3.j、4.k的状态下调用此函数，其中j>=index，k>=index - 1。
        term_t* term(length_t index);

        /// @brief 更新term_size当中的某个元素。
        /// @param index 某个元素的指标。
        ///
        /// 可以在3.j的状态下调用次函数，其中j>=index，调用后状态变为4.j。
        /// 也可以手动放置所有term后依次调用此函数来到达4.(n-1)的状态，其中n是list size。
        ///
        /// @note 如果index溢出，则行为未定义。
        void update_term_size(length_t index);

        /// @brief 获取list_t对象的大小。
        /// @return list_t对象的大小。
        length_t data_size();

        /// @brief 获取list_t对象的头字节指针。
        /// @return list_t对象的头字节指针。
        std::byte* head();

        /// @brief 获取list_t对象的尾字节指针。
        /// @return list_t对象的尾字节指针。
        std::byte* tail();

        /// @brief 将list_t对象输出至buffer。
        /// @param buffer 待被输出的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输出后的buffer指针，如果尾指针检查失败则返回nullptr。
        char* print(char* buffer, char* check_tail = nullptr);

        /// @brief 从buffer中输入list_t对象。
        /// @param buffer 待输入的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输入后的buffer指针，如果尾指针检查失败则返回nullptr。
        const char* scan(const char* buffer, std::byte* check_tail = nullptr);
    };
} // namespace ds

#endif
