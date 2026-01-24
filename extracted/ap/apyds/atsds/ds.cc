#include <ds/ds.hh>
#include <ds/search.hh>
#include <emscripten/bind.h>

namespace em = emscripten;

// 由于embind的限制，这里无法使用string_view。
// 为了保持一致性，一律使用复制。
template<typename T>
auto from_string(const std::string& string, int buffer_size) -> std::unique_ptr<T> {
    auto result = reinterpret_cast<T*>(operator new(buffer_size));
    auto scan_result = result->scan(string.data(), reinterpret_cast<std::byte*>(result) + buffer_size);
    if (scan_result == nullptr) [[unlikely]] {
        operator delete(result);
        return std::unique_ptr<T>(nullptr);
    }
    return std::unique_ptr<T>(result);
}

template<typename T>
auto to_string(T* value, int buffer_size) -> std::string {
    auto result = reinterpret_cast<char*>(operator new(buffer_size));
    auto print_result = value->print(result, reinterpret_cast<char*>(result) + buffer_size);
    if (print_result == nullptr || print_result - result == buffer_size) [[unlikely]] {
        operator delete(result);
        return std::string();
    }
    *print_result = '\0';
    auto string = std::string(result);
    operator delete(result);
    return string;
}

template<typename T>
auto from_binary(const std::vector<std::uint8_t>& binary) -> std::unique_ptr<T> {
    auto dst = std::unique_ptr<T>(reinterpret_cast<T*>(operator new(binary.size())));
    memcpy(dst.get(), binary.data(), binary.size());
    return dst;
}

template<typename T>
auto to_binary(T* value) -> std::vector<std::uint8_t> {
    std::vector<std::uint8_t> result;
    result.resize(value->data_size());
    memcpy(result.data(), value, value->data_size());
    return result;
}

template<typename T>
auto clone(T* value) -> std::unique_ptr<T> {
    auto result = std::unique_ptr<T>(reinterpret_cast<T*>(operator new(value->data_size())));
    memcpy(result.get(), value, value->data_size());
    return result;
}

template<typename T>
auto data_size(T* value) -> int {
    return value->data_size();
}

template<typename T>
auto common_declaration(em::class_<T>& t) {
    t.class_function("from_string", from_string<T>);
    t.class_function("to_string", to_string<T>, em::allow_raw_pointers());
    t.class_function("from_binary", from_binary<T>);
    t.class_function("to_binary", to_binary<T>, em::allow_raw_pointers());
    t.function("clone", clone<T>, em::allow_raw_pointers());
    t.function("data_size", data_size<T>, em::allow_raw_pointers());
}

auto term_ground(ds::term_t* term, ds::term_t* dictionary, const std::string& scope, int length) -> std::unique_ptr<ds::term_t> {
    const char* scope_ptr = scope.size() != 0 ? scope.data() : nullptr;
    auto result = reinterpret_cast<ds::term_t*>(operator new(length));
    if (result->ground(term, dictionary, scope_ptr, reinterpret_cast<std::byte*>(result) + length) == nullptr) [[unlikely]] {
        operator delete(result);
        return std::unique_ptr<ds::term_t>(nullptr);
    }
    return std::unique_ptr<ds::term_t>(result);
}

auto rule_ground(ds::rule_t* rule, ds::rule_t* dictionary, const std::string& scope, int length) -> std::unique_ptr<ds::rule_t> {
    const char* scope_ptr = scope.size() != 0 ? scope.data() : nullptr;
    auto result = reinterpret_cast<ds::rule_t*>(operator new(length));
    if (result->ground(rule, dictionary, scope_ptr, reinterpret_cast<std::byte*>(result) + length) == nullptr) [[unlikely]] {
        operator delete(result);
        return std::unique_ptr<ds::rule_t>(nullptr);
    }
    return std::unique_ptr<ds::rule_t>(result);
}

auto term_match(ds::term_t* term_1, ds::term_t* term_2, const std::string& scope_1, const std::string& scope_2, int length)
    -> std::unique_ptr<ds::term_t> {
    auto result = reinterpret_cast<ds::term_t*>(operator new(length));
    if (result->match(term_1, term_2, scope_1.data(), scope_2.data(), reinterpret_cast<std::byte*>(result) + length) == nullptr) [[unlikely]] {
        operator delete(result);
        return std::unique_ptr<ds::term_t>(nullptr);
    }
    return std::unique_ptr<ds::term_t>(result);
}

auto rule_match(ds::rule_t* rule_1, ds::rule_t* rule_2, int length) -> std::unique_ptr<ds::rule_t> {
    auto result = reinterpret_cast<ds::rule_t*>(operator new(length));
    if (result->match(rule_1, rule_2, reinterpret_cast<std::byte*>(result) + length) == nullptr) [[unlikely]] {
        operator delete(result);
        return std::unique_ptr<ds::rule_t>(nullptr);
    }
    return std::unique_ptr<ds::rule_t>(result);
}

auto term_rename(ds::term_t* term, ds::term_t* prefix_and_suffix, int length) -> std::unique_ptr<ds::term_t> {
    auto result = reinterpret_cast<ds::term_t*>(operator new(length));
    if (result->rename(term, prefix_and_suffix, reinterpret_cast<std::byte*>(result) + length) == nullptr) [[unlikely]] {
        operator delete(result);
        return std::unique_ptr<ds::term_t>(nullptr);
    }
    return std::unique_ptr<ds::term_t>(result);
}

auto rule_rename(ds::rule_t* rule, ds::rule_t* prefix_and_suffix, int length) -> std::unique_ptr<ds::rule_t> {
    auto result = reinterpret_cast<ds::rule_t*>(operator new(length));
    if (result->rename(rule, prefix_and_suffix, reinterpret_cast<std::byte*>(result) + length) == nullptr) [[unlikely]] {
        operator delete(result);
        return std::unique_ptr<ds::rule_t>(nullptr);
    }
    return std::unique_ptr<ds::rule_t>(result);
}

auto search_add(ds::search_t* search, const std::string& text) -> bool {
    return search->add(text);
}

auto search_execute(ds::search_t* search, const em::val& callback) -> ds::length_t {
    return search->execute([&callback](ds::rule_t* candidate) -> bool { return callback(candidate, em::allow_raw_pointers()).as<bool>(); });
}

EMSCRIPTEN_BINDINGS(ds) {
    em::register_vector<std::uint8_t>("Buffer");

    auto string_t = em::class_<ds::string_t>("String");
    auto item_t = em::class_<ds::item_t>("Item");
    auto variable_t = em::class_<ds::variable_t>("Variable");
    auto list_t = em::class_<ds::list_t>("List");
    auto term_t = em::class_<ds::term_t>("Term");
    auto rule_t = em::class_<ds::rule_t>("Rule");

    common_declaration(string_t);
    common_declaration(item_t);
    common_declaration(variable_t);
    common_declaration(list_t);
    common_declaration(term_t);
    common_declaration(rule_t);

    item_t.function("name", &ds::item_t::name, em::return_value_policy::reference());

    variable_t.function("name", &ds::variable_t::name, em::return_value_policy::reference());

    list_t.function("length", &ds::list_t::get_list_size);
    list_t.function("getitem", &ds::list_t::term, em::return_value_policy::reference());

    em::enum_<ds::term_type_t>("TermType")
        .value("Variable", ds::term_type_t::variable)
        .value("Item", ds::term_type_t::item)
        .value("List", ds::term_type_t::list)
        .value("Null", ds::term_type_t::null);
    term_t.function("get_type", &ds::term_t::get_type);
    term_t.function("variable", &ds::term_t::variable, em::return_value_policy::reference());
    term_t.function("item", &ds::term_t::item, em::return_value_policy::reference());
    term_t.function("list", &ds::term_t::list, em::return_value_policy::reference());

    rule_t.function("length", &ds::rule_t::premises_count);
    rule_t.function("conclusion", &ds::rule_t::conclusion, em::return_value_policy::reference());
    rule_t.function("getitem", &ds::rule_t::premises, em::return_value_policy::reference());

    term_t.class_function("ground", term_ground, em::return_value_policy::take_ownership());
    rule_t.class_function("ground", rule_ground, em::return_value_policy::take_ownership());
    term_t.class_function("match", term_match, em::return_value_policy::take_ownership());
    rule_t.class_function("match", rule_match, em::return_value_policy::take_ownership());
    term_t.class_function("rename", term_rename, em::return_value_policy::take_ownership());
    rule_t.class_function("rename", rule_rename, em::return_value_policy::take_ownership());

    auto search_t = em::class_<ds::search_t>("Search");
    search_t.constructor<ds::length_t, ds::length_t>();
    search_t.function("set_limit_size", &ds::search_t::set_limit_size);
    search_t.function("set_buffer_size", &ds::search_t::set_buffer_size);
    search_t.function("reset", &ds::search_t::reset);
    // 因为embind的限制，这里无法使用string_view和function。
    search_t.function("add", &search_add, em::allow_raw_pointers());
    search_t.function("execute", &search_execute, em::allow_raw_pointers());
}
