#ifndef DS_RULE_HH
#define DS_RULE_HH

#include <ds/list.hh>
#include <ds/term.hh>

namespace ds {
    /// @brief rule_t对象。
    ///
    /// 可能的状态有：
    /// 1. 没有初始化；
    /// 2. 初始化完毕。
    ///
    /// @note 含有若干term，直接使用list_t作为基类实现。
    /// list中最后一个term被视为conclusion，其他的term被视为premises。
    /// 因为使用方式完全不同，所以是private继承的。
    /// @note 存在空态，即基态list的长度为0。
    class rule_t : private list_t {
      public:
        /// @brief 获取rule的conclusion。
        /// @return rule的conclusion，如果rule为空态则返回nullptr。
        ///
        /// 可以在2的状态下调用此函数。
        term_t* conclusion();

        /// @brief 获取rule仅有的conclusion。
        /// @return rule仅有的conclusion, 否则返回nullptr。
        ///
        /// 可以在2的状态下调用此函数。
        term_t* only_conclusion();

        /// @brief 获取rule的某个premises。
        /// @param index 某个preimises的指标。
        /// @return rule的某个premises，如果index溢出则返回nullptr。
        ///
        /// 可以在2的状态下调用此函数。
        term_t* premises(length_t index);

        /// @brief 获取rule的premises数目。
        /// @return rule的premises数目。
        ///
        /// 可以在2的状态下调用此函数。
        ///
        /// @note 如果rule的状态为空，则行为未定义。
        length_t premises_count();

        /// @brief 判断rule的合法性。
        /// @return rule的合法性。
        ///
        /// 可以在2的状态下调用此函数。
        bool valid();

        /// @brief 设置状态为非法。
        /// @param check_tail 可选的尾指针检查。
        /// @return rule_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// 可以在1、2的状态下调用此函数。
        rule_t* set_null(std::byte* check_tail = nullptr);

        /// @brief 获取rule_t对象的大小。
        /// @return rule_t对象的大小。
        length_t data_size();

        /// @brief 获取rule_t对象的头字节指针。
        /// @return rule_t对象的头字节指针。
        std::byte* head();

        /// @brief 获取rule_t对象的尾字节指针。
        /// @return rule_t对象的尾字节指针。
        std::byte* tail();

        /// @brief 将rule_t对象输出至buffer。
        /// @param buffer 待被输出的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输出后的buffer指针，如果rule状态为空或者尾指针检查失败则返回nullptr。
        char* print(char* buffer, char* check_tail = nullptr);

        /// @brief 从buffer中输入rule_t对象。
        /// @param buffer 待输入的buffer指针。
        /// @param check_tail 可选的尾指针检查。
        /// @return 被输入后的buffer指针，如果尾指针检查失败则返回nullptr。
        const char* scan(const char* buffer, std::byte* check_tail = nullptr);

        /// @brief 将rule使用dictionary进行ground, 结果更新至本对象。
        /// @param rule 待被ground的rule。
        /// @param dictionary 含有list of tuple的term作为的dictionary。
        /// @param scope 给定的rule所在的scope，如果为nullptr则无视scope判断，且要求dictionary内无scope。
        /// @param check_tail 可选的尾指针检查。
        /// @return 自身，是一个rule_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// @note dictionary中每个tuple可以是下面的形式：
        /// 1. key, value (视为对所有scope有效)；
        /// 2. scope, key, value (key和value的scope相同)；
        /// 2. scope_key, scope_value, key, value。
        /// @note 如果dictionary格式不正确，则行为未定义。
        rule_t* ground(rule_t* rule, term_t* dictionary, const char* scope, std::byte* check_tail = nullptr);

        /// @brief 将rule使用dictionary进行ground, 结果更新至本对象。
        /// @param rule 待被ground的rule。
        /// @param dictionary 含有list of tuple的rule作为的dictionary。
        /// @param scope 给定的rule所在的scope，如果为nullptr则无视scope判断，且要求dictionary内无scope。
        /// @param check_tail 可选的尾指针检查。
        /// @return 自身，是一个rule_t对象的指针，如果尾指针检查失败则返回nullptr。
        ///
        /// @note dictionary中每个tuple可以是下面的形式：
        /// 1. key, value (视为对所有scope有效)；
        /// 2. scope, key, value (key和value的scope相同)；
        /// 3. scope_key, scope_value, key, value。
        /// @note 如果dictionary格式不正确，则行为未定义。
        rule_t* ground(rule_t* rule, rule_t* dictionary, const char* scope, std::byte* check_tail = nullptr);

        /// @brief 将两个rule尽可能相互提示并ground, 随后进行apply, 结果更新至本对象。
        /// @param rule_1 待被apply的rule。
        /// @param rule_2 待作为fact的rule。
        /// @param check_tail 可选的尾指针检查。
        /// @return 自身，如果匹配失败则返回nullptr，如果尾指针检查失败则返回nullptr，在尾指针检查正常时，匹配失败会将本对象设置为null。
        rule_t* match(rule_t* rule_1, rule_t* rule_2, std::byte* check_tail = nullptr);

        /// @brief 将rule中的所有variable添加prefix和suffix, 结果更新至本对象。
        /// @param rule 待被重命名的rule。
        /// @param prefix_and_suffix 只有一个conclusion的rule，conclusion是含有两个list的list，每个内部list包含0或1个item，分别表示prefix和suffix。
        /// @param check_tail 可选的尾指针检查。
        /// @return 自身，是一个rule_t对象的指针，如果尾指针检查失败则返回nullptr。
        rule_t* rename(rule_t* rule, rule_t* prefix_and_suffix, std::byte* check_tail = nullptr);
    };
} // namespace ds

#endif
