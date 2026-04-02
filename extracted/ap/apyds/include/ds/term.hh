#ifndef DS_TERM_HH
#define DS_TERM_HH

#include <cstddef>

#include <ds/config.hh>

namespace ds {
    class variable_t;
    class item_t;
    class list_t;

    /// @brief term_t的类型enum。
    enum class term_type_t : min_uint_t {
        null = 0,
        variable = 1,
        item = 2,
        list = 3
    };

    /// @brief term_t对象。
    ///
    /// 内存分布:
    /// 1. type : term_type_t；
    /// 2.data : variable | item | list。
    ///
    /// 可能的状态有：
    /// 1. 未初始化状态，type不正确，data不正确；
    /// 2. 已经设置了type，但是data没有设置，type正确，data不正确；
    /// 3. 已经设置了type和data，type和data都是正确的。
    class term_t {
        /// @brief 获取term type的指针。
        /// @return term type的指针。
        ///
        /// 可以在1、2、3的状态下调用此函数。
        term_type_t* type_pointer();

      public:
        /// @brief 获取term type。
        /// @return term type。
        ///
        /// 可以在2、3的状态下调用此函数。
        term_type_t get_type();

        /// @brief 设置term type。
        /// @param type 新的term type。
        /// @param check_tail 可选的尾指针检查。
        /// @return term_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// 可以在1、2、3的状态下调用此函数，调用后会将状态变为2。
        term_t* set_type(term_type_t type, std::byte* check_tail = nullptr);

        /// @brief 设置term type为null, 表示一个空的term。
        /// @param check_tail 可选的尾指针检查。
        /// @return term_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// 可以在1、2、3的状态下调用此函数，调用后会将状态变为2。
        term_t* set_null(std::byte* check_tail = nullptr);

        /// @brief 设置term type为variable。
        /// @param check_tail 可选的尾指针检查。
        /// @return term_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// 可以在1、2、3的状态下调用此函数，调用后会将状态变为2。
        term_t* set_variable(std::byte* check_tail = nullptr);

        /// @brief 设置term type为item。
        /// @param check_tail 可选的尾指针检查。
        /// @return term_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// 可以在1、2、3的状态下调用此函数，调用后会将状态变为2。
        term_t* set_item(std::byte* check_tail = nullptr);

        /// @brief 设置term type为list。
        /// @param check_tail 可选的尾指针检查。
        /// @return term_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// 可以在1、2、3的状态下调用此函数，调用后会将状态变为2。
        term_t* set_list(std::byte* check_tail = nullptr);

        /// @brief 检查term_t对象是否为null。
        /// @return 如果term_t对象是null，则返回true，否则返回false。
        ///
        /// 可以在2、3的状态下调用此函数。
        bool is_null();

        /// @brief 获取variable_t对象。
        /// @return variable_t对象的指针。
        ///
        /// 可以在2、3的状态下调用此函数。
        ///
        /// @note 如果term中并不是variable则返回nullptr。
        variable_t* variable();

        /// @brief 获取item_t对象。
        /// @return item_t对象的指针。
        ///
        /// 可以在2、3的状态下调用此函数。
        ///
        /// @note 如果term中并不是item则返回nullptr。
        item_t* item();

        /// @brief 获取list_t对象。
        /// @return list_t对象的指针。
        ///
        /// 可以在2、3的状态下调用此函数。
        ///
        /// @note 如果term中并不是list则返回nullptr。
        list_t* list();

        /// @brief 获取term_t对象的大小。
        /// @return term_t对象的大小。
        length_t data_size();

        /// @brief 获取term_t对象的头字节指针。
        /// @return term_t对象的头字节指针。
        std::byte* head();

        /// @brief 获取term_t对象的尾字节指针。
        /// @return term_t对象的尾字节指针。
        std::byte* tail();

        /// @brief 将term_t对象输出至buffer。
        /// @param buffer 待被输出的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输出后的buffer指针，如果term类型为空或者尾指针检查失败则返回nullptr。
        char* print(char* buffer, char* check_tail = nullptr);

        /// @brief 从buffer中输入term_t对象。
        /// @param buffer 待输入的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输入后的buffer指针，如果尾指针检查失败则返回nullptr。
        const char* scan(const char* buffer, std::byte* check_tail = nullptr);

        /// @brief 将term使用dictionary进行ground, 结果更新至本对象。
        /// @param term 待被ground的term。
        /// @param dictionary 含有list of tuple的term作为的dictionary。
        /// @param scope 给定的term所在的scope，如果为nullptr则无视scope判断，且要求dictionary内无scope。
        /// @param check_tail 可选的尾指针检查。
        /// @return 自身，是一个term_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// @note dictionary中每个tuple可以是下面的形式：
        /// 1. key, value (视为对所有scope有效)；
        /// 2. scope, key, value (key和value的scope相同)；
        /// 3. scope_key, scope_value, key, value。
        /// @note 如果dictionary格式不正确，则行为未定义。
        term_t* ground(term_t* term, term_t* dictionary, const char* scope, std::byte* check_tail = nullptr);

        /// @brief 将term_1和term_2相互匹配，结果作为一个用于ground的dictionary被更新至本对象。
        /// @param term_1 第一个term。
        /// @param term_2 第二个term。
        /// @param scope_1 结果中用于标记给term_1使用的scope。
        /// @param scope_2 结果中用于标记给term_2使用的scope。
        /// @param check_tail 可选的尾指针检查。
        /// @return 自身，如果匹配失败则返回nullptr，如果尾指针检查失败则返回nullptr，在尾指针检查正常时，匹配失败会将本对象设置为null。
        term_t* match(term_t* term_1, term_t* term_2, const char* scope_1, const char* scope_2, std::byte* check_tail = nullptr);

        /// @brief 将term中的所有variable添加prefix和suffix, 结果更新至本对象。
        /// @param term 待被重命名的term。
        /// @param prefix_and_suffix 含有两个list的list，每个内部list包含0或1个item，分别表示prefix和suffix。
        /// @param check_tail 可选的尾指针检查。
        /// @return 自身，是一个term_t对象的指针，如果尾指针检查失败则返回nullptr。
        term_t* rename(term_t* term, term_t* prefix_and_suffix, std::byte* check_tail = nullptr);
    };
} // namespace ds

#endif
