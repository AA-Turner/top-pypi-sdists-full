#include <cstring>
#include <set>

#include <ds/search.hh>
#include <ds/utility.hh>

namespace ds {
    bool search_t::less_t::operator()(const std::unique_ptr<rule_t>& lhs, const std::unique_ptr<rule_t>& rhs) const {
        const length_t lhs_size = lhs->data_size();
        const length_t rhs_size = rhs->data_size();
        if (lhs_size < rhs_size) {
            return true;
        }
        if (lhs_size > rhs_size) {
            return false;
        }
        if (std::memcmp(lhs->head(), rhs->head(), lhs_size) < 0) {
            return true;
        }
        return false;
    }

    search_t::search_t(length_t _limit_size, length_t _buffer_size) {
        set_limit_size(_limit_size);
        set_buffer_size(_buffer_size);
        reset();
    }

    void search_t::set_limit_size(length_t _limit_size) {
        limit_size = _limit_size;
        done_cycle = 0;
    }

    void search_t::set_buffer_size(length_t _buffer_size) {
        buffer_size = _buffer_size;
        buffer = std::unique_ptr<rule_t>(reinterpret_cast<rule_t*>(operator new(buffer_size)));
        done_cycle = 0;
    }

    void search_t::reset() {
        done_cycle = 0;
        current_cycle = 0;
        rules.clear();
        facts.clear();
    }

    bool search_t::add(std::string_view text) {
        auto candidate = text_to_rule(text.data(), limit_size);
        if (candidate) {
            if (done_cycle == current_cycle) {
                ++current_cycle;
            }
            if (candidate->premises_count() != 0) {
                rules.emplace(std::move(candidate), current_cycle);
            } else {
                facts.emplace(std::move(candidate), current_cycle);
            }
            return true;
        } else {
            return false;
        }
    }

    length_t search_t::execute(const std::function<bool(rule_t*)>& callback) {
        std::set<std::unique_ptr<rule_t>, less_t> temp_rules;
        std::set<std::unique_ptr<rule_t>, less_t> temp_facts;

        bool break_all = false;
        for (auto& [rule, rules_cycle] : rules) {
            for (auto& [fact, facts_cycle] : facts) {
                if (rules_cycle <= done_cycle && facts_cycle <= done_cycle) {
                    continue;
                }
                buffer->match(rule.get(), fact.get(), reinterpret_cast<std::byte*>(buffer.get()) + buffer_size);
                if (!buffer->valid()) {
                    continue;
                }
                if (buffer->data_size() > limit_size) {
                    continue;
                }
                if (buffer->premises_count() != 0) {
                    // rule
                    if (rules.find(buffer) != rules.end() || temp_rules.find(buffer) != temp_rules.end()) {
                        continue;
                    }
                    auto new_rule = std::unique_ptr<rule_t>(reinterpret_cast<rule_t*>(operator new(buffer->data_size())));
                    memcpy(new_rule.get(), buffer.get(), buffer->data_size());
                    temp_rules.emplace(std::move(new_rule));
                } else {
                    // fact
                    if (facts.find(buffer) != facts.end() || temp_facts.find(buffer) != temp_facts.end()) {
                        continue;
                    }
                    auto new_fact = std::unique_ptr<rule_t>(reinterpret_cast<rule_t*>(operator new(buffer->data_size())));
                    memcpy(new_fact.get(), buffer.get(), buffer->data_size());
                    temp_facts.emplace(std::move(new_fact));
                }
                if (callback(buffer.get())) {
                    break_all = true;
                    break;
                }
            }
            if (break_all) {
                break;
            }
        }

        if (!break_all) {
            done_cycle = current_cycle;
        }
        ++current_cycle;
        length_t count = temp_rules.size() + temp_facts.size();
        for (auto it = temp_rules.begin(); it != temp_rules.end();) {
            auto node = temp_rules.extract(it++);
            rules.emplace(std::move(node.value()), current_cycle);
        }
        for (auto it = temp_facts.begin(); it != temp_facts.end();) {
            auto node = temp_facts.extract(it++);
            facts.emplace(std::move(node.value()), current_cycle);
        }
        return count;
    }
} // namespace ds
