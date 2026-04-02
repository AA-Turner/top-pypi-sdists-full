#include <cstring>

#include <ds/helper.hh>
#include <ds/item.hh>
#include <ds/list.hh>
#include <ds/rule.hh>
#include <ds/term.hh>
#include <ds/variable.hh>

namespace ds {
    term_t* term_t::ground(term_t* term, term_t* dictionary, const char* scope, std::byte* check_tail) {
        switch (term->get_type()) {
        case term_type_t::variable: {
            char* this_string = term->variable()->name()->get_string();
            list_t* list = dictionary->list();
            for (length_t index = 0; index < list->get_list_size(); ++index) {
                list_t* tuple = list->term(index)->list();
                term_t* key = nullptr;
                term_t* value = nullptr;
                const char* scope_key = nullptr;
                const char* scope_value = nullptr;
                switch (tuple->get_list_size()) {
                case 2:
                    scope_key = scope;
                    scope_value = scope;
                    key = tuple->term(0);
                    value = tuple->term(1);
                    break;
                case 3:
                    scope_key = tuple->term(0)->item()->name()->get_string();
                    scope_value = scope_key;
                    key = tuple->term(1);
                    value = tuple->term(2);
                    break;
                case 4:
                    scope_key = tuple->term(0)->item()->name()->get_string();
                    scope_value = tuple->term(1)->item()->name()->get_string();
                    key = tuple->term(2);
                    value = tuple->term(3);
                    break;
                default:
                    return nullptr;
                }
                if (scope != nullptr && strcmp(scope, scope_key) != 0) {
                    continue;
                }
                if (strcmp(this_string, key->variable()->name()->get_string()) != 0) {
                    continue;
                }
                if (this->ground(value, dictionary, scope_value, check_tail) == nullptr) [[unlikely]] {
                    return nullptr;
                }
                return this;
            }
            if (check_before_fail(check_tail, this, term->data_size())) [[unlikely]] {
                return nullptr;
            };
            memcpy(this, term, term->data_size());
            return this;
        }
        case term_type_t::item: {
            if (check_before_fail(check_tail, this, term->data_size())) [[unlikely]] {
                return nullptr;
            };
            memcpy(this, term, term->data_size());
            return this;
        }
        case term_type_t::list: {
            list_t* src = term->list();
            if (set_list(check_tail) == nullptr) [[unlikely]] {
                return nullptr;
            }
            list_t* dst = list();
            if (dst->set_list_size(src->get_list_size(), check_tail) == nullptr) [[unlikely]] {
                return nullptr;
            }
            for (length_t index = 0; index < dst->get_list_size(); ++index) {
                if (dst->term(index)->ground(src->term(index), dictionary, scope, check_tail) == nullptr) [[unlikely]] {
                    return nullptr;
                }
                dst->update_term_size(index);
            }
            return this;
        }
        default:
            return nullptr;
        }
    }

    rule_t* rule_t::ground(rule_t* rule, term_t* dictionary, const char* scope, std::byte* check_tail) {
        list_t* dst = this;
        list_t* src = rule;
        if (dst->set_list_size(src->get_list_size(), check_tail) == nullptr) [[unlikely]] {
            return nullptr;
        }
        for (length_t index = 0; index < dst->get_list_size(); ++index) {
            if (dst->term(index)->ground(src->term(index), dictionary, scope, check_tail) == nullptr) [[unlikely]] {
                return nullptr;
            }
            dst->update_term_size(index);
        }
        return this;
    }

    rule_t* rule_t::ground(rule_t* rule, rule_t* dictionary, const char* scope, std::byte* check_tail) {
        return ground(rule, dictionary->only_conclusion(), scope, check_tail);
    }
} // namespace ds
