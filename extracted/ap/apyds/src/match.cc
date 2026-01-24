#include <cstring>

#include <ds/helper.hh>
#include <ds/item.hh>
#include <ds/list.hh>
#include <ds/rule.hh>
#include <ds/string.hh>
#include <ds/term.hh>
#include <ds/variable.hh>

namespace ds {
    // 一般的unification算法中，两侧变量视为同一个变量。
    // 但是我们这里需要区分他们，只有在出现variable: variable的情况下才会将两侧变量视为同一个变量。
    // 这里认为每个term中的变量存在某个scope中。
    namespace {
        struct unify_job_t {
            term_t* term_1;
            term_t* term_2;
            const char* scope_1;
            const char* scope_2;
        };
        struct unify_substitution_t {
            term_t* begin;
            term_t* end;
            length_t count;
            std::byte* check_tail;
        };

        bool term_equal(term_t* term_1, term_t* term_2);
        void unify(unify_job_t* job, unify_substitution_t* substitution);
        void unify_variable(unify_job_t* job, unify_substitution_t* substitution);
        void record_substitution(unify_job_t* job, unify_substitution_t* substitution);
        bool occur_check(unify_job_t* job, unify_substitution_t* substitution);
        term_t* found_in_substitution(variable_t* variable, const char* scope, unify_substitution_t* substitution);

        bool term_equal(term_t* term_1, term_t* term_2) {
            if (term_1->data_size() != term_2->data_size()) {
                return false;
            }
            length_t data_size = term_1->data_size();
            if (memcmp(term_1, term_2, data_size) != 0) {
                return false;
            }
            return true;
        }

        void unify(unify_job_t* job, unify_substitution_t* substitution) {
            if (job->term_1->variable() && job->term_2->variable()) {
                if (strcmp(job->scope_1, job->scope_2) == 0) {
                    if (term_equal(job->term_1, job->term_2)) {
                        return;
                    }
                }
            }

            if (job->term_1->variable()) {
                unify_job_t new_job = {.term_1 = job->term_1, .term_2 = job->term_2, .scope_1 = job->scope_1, .scope_2 = job->scope_2};
                unify_variable(&new_job, substitution);
                return;
            }

            if (job->term_2->variable()) {
                unify_job_t new_job = {.term_1 = job->term_2, .term_2 = job->term_1, .scope_1 = job->scope_2, .scope_2 = job->scope_1};
                unify_variable(&new_job, substitution);
                return;
            }

            if (job->term_1->item() && job->term_2->item()) {
                if (!term_equal(job->term_1, job->term_2)) {
                    substitution->end = nullptr;
                }
                return;
            }

            if (job->term_1->list() && job->term_2->list()) {
                list_t* list_1 = job->term_1->list();
                list_t* list_2 = job->term_2->list();
                if (list_1->get_list_size() != list_2->get_list_size()) {
                    substitution->end = nullptr;
                    return;
                }
                for (length_t index = 0; index < list_1->get_list_size(); ++index) {
                    unify_job_t new_job = {
                        .term_1 = list_1->term(index),
                        .term_2 = list_2->term(index),
                        .scope_1 = job->scope_1,
                        .scope_2 = job->scope_2};
                    unify(&new_job, substitution);
                    if (substitution->end == nullptr) {
                        return;
                    }
                }
                return;
            }

            substitution->end = nullptr;
        }

        void unify_variable(unify_job_t* job, unify_substitution_t* substitution) {
            auto found = found_in_substitution(job->term_1->variable(), job->scope_1, substitution);
            if (found) {
                unify_job_t new_job = {
                    .term_1 = found->list()->term(3),
                    .term_2 = job->term_2,
                    .scope_1 = found->list()->term(1)->item()->name()->get_string(),
                    .scope_2 = job->scope_2};
                unify(&new_job, substitution);
                return;
            }

            if (job->term_2->variable()) {
                auto found = found_in_substitution(job->term_2->variable(), job->scope_2, substitution);
                if (found) {
                    unify_job_t new_job = {
                        .term_1 = job->term_1,
                        .term_2 = found->list()->term(3),
                        .scope_1 = job->scope_1,
                        .scope_2 = found->list()->term(1)->item()->name()->get_string()};
                    unify_variable(&new_job, substitution);
                    return;
                }
            }

            if (occur_check(job, substitution)) {
                substitution->end = nullptr;
                return;
            }

            record_substitution(job, substitution);
        }

        void record_substitution(unify_job_t* job, unify_substitution_t* substitution) {
            if (substitution->end->set_list(substitution->check_tail) == nullptr) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            list_t* tuple = substitution->end->list();
            if (tuple->set_list_size(4, substitution->check_tail) == nullptr) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            if (tuple->term(0)->set_item(substitution->check_tail) == nullptr) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            if (tuple->term(0)->item()->name()->set_null_string(job->scope_1, substitution->check_tail) == nullptr) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            tuple->update_term_size(0);
            if (tuple->term(1)->set_item(substitution->check_tail) == nullptr) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            if (tuple->term(1)->item()->name()->set_null_string(job->scope_2, substitution->check_tail) == nullptr) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            tuple->update_term_size(1);
            if (check_before_fail(substitution->check_tail, tuple->term(2), job->term_1->data_size())) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            memcpy(reinterpret_cast<std::byte*>(tuple->term(2)), reinterpret_cast<std::byte*>(job->term_1), job->term_1->data_size());
            tuple->update_term_size(2);
            if (check_before_fail(substitution->check_tail, tuple->term(3), job->term_2->data_size())) [[unlikely]] {
                substitution->end = nullptr;
                return;
            }
            memcpy(reinterpret_cast<std::byte*>(tuple->term(3)), reinterpret_cast<std::byte*>(job->term_2), job->term_2->data_size());
            tuple->update_term_size(3);
            substitution->end = reinterpret_cast<term_t*>(substitution->end->tail());
            substitution->count += 1;
        }

        bool occur_check(unify_job_t* job, unify_substitution_t* substitution) {
            if (job->term_2->variable()) {
                if (strcmp(job->scope_1, job->scope_2) == 0) {
                    if (term_equal(job->term_1, job->term_2)) {
                        return true;
                    }
                }

                auto found = found_in_substitution(job->term_2->variable(), job->scope_2, substitution);
                if (found) {
                    unify_job_t new_job = {
                        .term_1 = job->term_1,
                        .term_2 = found->list()->term(3),
                        .scope_1 = job->scope_1,
                        .scope_2 = found->list()->term(1)->item()->name()->get_string()};
                    return occur_check(&new_job, substitution);
                }
            }

            if (job->term_2->list()) {
                list_t* list = job->term_2->list();
                for (length_t index = 0; index < list->get_list_size(); ++index) {
                    unify_job_t new_job = {.term_1 = job->term_1, .term_2 = list->term(index), .scope_1 = job->scope_1, .scope_2 = job->scope_2};
                    if (occur_check(&new_job, substitution)) {
                        return true;
                    }
                }
            }
            return false;
        }

        term_t* found_in_substitution(variable_t* variable, const char* scope, unify_substitution_t* substitution) {
            const char* variable_name = variable->name()->get_string();
            term_t* current = substitution->begin;
            while (current != substitution->end) {
                list_t* tuple = current->list();
                const char* scope_key = tuple->term(0)->item()->name()->get_string();
                if (strcmp(scope_key, scope) == 0) {
                    const char* key_name = tuple->term(2)->variable()->name()->get_string();
                    if (strcmp(key_name, variable_name) == 0) {
                        return current;
                    }
                }
                current = reinterpret_cast<term_t*>(current->tail());
            }
            return nullptr;
        }
    } // namespace

    term_t* term_t::match(term_t* term_1, term_t* term_2, const char* scope_1, const char* scope_2, std::byte* check_tail) {
        // 检查是否能存下非法结果，存不下直接返回nullptr
        // 在此之后，所有非法结果在返回前都会调用set_null(nullptr)
        if (check_before_fail(check_tail, this, sizeof(term_type_t))) [[unlikely]] {
            return nullptr;
        }
        // 将自己作为暂时的buffer用于存储一群tuple形式的term
        // 公用的部分都放在substitution中
        unify_job_t job = {.term_1 = term_1, .term_2 = term_2, .scope_1 = scope_1, .scope_2 = scope_2};
        unify_substitution_t substitution = {.begin = this, .end = this, .count = 0, .check_tail = check_tail};
        unify(&job, &substitution);
        if (substitution.end == nullptr) [[unlikely]] {
            set_null(nullptr);
            return nullptr;
        }
        length_t offset = sizeof(term_type_t) + sizeof(length_t) + sizeof(length_t) * substitution.count;
        if (check_before_fail(check_tail, substitution.end, offset)) [[unlikely]] {
            return nullptr;
        }
        memmove(
            reinterpret_cast<std::byte*>(substitution.begin) + offset,
            reinterpret_cast<std::byte*>(substitution.begin),
            reinterpret_cast<std::byte*>(substitution.end) - reinterpret_cast<std::byte*>(substitution.begin)
        );
        // 前面的元信息不需要检查尾指针
        set_list(nullptr)->list()->set_list_size(substitution.count, nullptr);
        for (length_t index = 0; index < substitution.count; ++index) {
            list()->update_term_size(index);
        }
        return this;
    }

    rule_t* rule_t::match(rule_t* rule_1, rule_t* rule_2, std::byte* check_tail) {
        // 检查是否能存下非法结果，存不下直接返回nullptr
        // 在此之后，所有非法结果在返回前都会调用set_null(nullptr)
        if (check_before_fail(check_tail, this, sizeof(length_t))) [[unlikely]] {
            return nullptr;
        }
        // 前者不是真rule，后者不是真fact，则直接报告非法
        if (rule_1->premises_count() == 0 || rule_2->premises_count() != 0) [[unlikely]] {
            set_null(nullptr);
            return nullptr;
        }
        // 拿自己当buffer存dict
        term_t* dict = reinterpret_cast<term_t*>(this);
        if (dict->match(rule_1->premises(0), rule_2->only_conclusion(), "r", "f", check_tail) == nullptr) [[unlikely]] {
            set_null(nullptr);
            return nullptr;
        }
        // 那自己继续当buffer存ground的结果
        rule_t* candidate_1 = reinterpret_cast<rule_t*>(dict->tail());
        if (candidate_1->ground(rule_1, dict, "r", check_tail) == nullptr) [[unlikely]] {
            set_null(nullptr);
            return nullptr;
        }
        rule_t* candidate_2 = reinterpret_cast<rule_t*>(candidate_1->tail());
        if (candidate_2->ground(rule_2, dict, "f", check_tail) == nullptr) [[unlikely]] {
            set_null(nullptr);
            return nullptr;
        }
        // 检查两个candidate的对应位置是否相同
        term_t* term_1 = candidate_1->premises(0);
        term_t* term_2 = candidate_2->conclusion();
        if (!term_equal(term_1, term_2)) [[unlikely]] {
            set_null(nullptr);
            return nullptr;
        }
        // 进行向前位移
        length_t list_size = rule_1->get_list_size() - 1;
        length_t offset = sizeof(length_t) + sizeof(length_t) * list_size;
        memmove(
            reinterpret_cast<std::byte*>(this) + offset,
            reinterpret_cast<std::byte*>(candidate_1->premises(0)->tail()),
            reinterpret_cast<std::byte*>(candidate_1->tail()) - reinterpret_cast<std::byte*>(candidate_1->premises(0)->tail())
        );
        set_list_size(list_size, nullptr);
        for (length_t index = 0; index < list_size; ++index) {
            update_term_size(index);
        }
        return this;
    }
} // namespace ds
