#include "type_resolver.h"
#include <algorithm>
#include <cctype>
#include <sstream>

namespace includecpp {
namespace generator {

// ============================================================================
// TypeResolver Implementation
// ============================================================================

TypeResolver::ParsedType TypeResolver::parse_type(const std::string& type_str) {
    ParsedType result;
    std::string working_str = type_str;

    // Remove leading/trailing whitespace
    working_str.erase(0, working_str.find_first_not_of(" \t\n\r"));
    working_str.erase(working_str.find_last_not_of(" \t\n\r") + 1);

    // Check for const qualifier
    if (working_str.find("const") == 0) {
        result.is_const = true;
        working_str = working_str.substr(5);
        working_str.erase(0, working_str.find_first_not_of(" \t"));
    }

    // Check for reference (&) or pointer (*)
    if (!working_str.empty() && working_str.back() == '&') {
        result.is_reference = true;
        working_str.pop_back();
        working_str.erase(working_str.find_last_not_of(" \t") + 1);
    } else if (!working_str.empty() && working_str.back() == '*') {
        result.is_pointer = true;
        working_str.pop_back();
        working_str.erase(working_str.find_last_not_of(" \t") + 1);
    }

    // Check if template type
    size_t template_start = working_str.find('<');
    if (template_start != std::string::npos) {
        result.is_template = true;
        result.base_name = working_str.substr(0, template_start);

        // Extract template arguments
        std::string template_content = extract_template_content(working_str);
        auto args = split_template_args(template_content);

        for (const auto& arg : args) {
            result.template_args.push_back(parse_type(arg));
        }
    } else {
        result.base_name = working_str;
    }

    return result;
}

std::string TypeResolver::ParsedType::to_cpp_string() const {
    std::ostringstream oss;

    if (is_const) oss << "const ";

    oss << base_name;

    if (is_template && !template_args.empty()) {
        oss << "<";
        for (size_t i = 0; i < template_args.size(); ++i) {
            if (i > 0) oss << ", ";
            oss << template_args[i].to_cpp_string();
        }
        oss << ">";
    }

    if (is_pointer) oss << "*";
    if (is_reference) oss << "&";

    return oss.str();
}

std::string TypeResolver::ParsedType::to_python_hint() const {
    // Convert C++ types to Python type hints
    static const std::map<std::string, std::string> type_map = {
        {"int", "int"}, {"long", "int"}, {"short", "int"},
        {"float", "float"}, {"double", "float"},
        {"bool", "bool"},
        {"string", "str"}, {"std::string", "str"},
        {"void", "None"}
    };

    if (type_map.count(base_name)) {
        return type_map.at(base_name);
    }

    // Handle containers
    if (base_name == "vector" || base_name == "std::vector") {
        if (!template_args.empty()) {
            return "List[" + template_args[0].to_python_hint() + "]";
        }
        return "List[Any]";
    }

    if (base_name == "map" || base_name == "std::map") {
        if (template_args.size() >= 2) {
            return "Dict[" + template_args[0].to_python_hint() + ", " +
                   template_args[1].to_python_hint() + "]";
        }
        return "Dict[Any, Any]";
    }

    // Custom type (struct/class)
    if (is_template && !template_args.empty()) {
        std::string result = base_name + "_";
        for (size_t i = 0; i < template_args.size(); ++i) {
            if (i > 0) result += "_";
            result += template_args[i].base_name;
        }
        return result;
    }

    return base_name;
}

std::string TypeResolver::to_python_hint(const ParsedType& type) {
    return type.to_python_hint();
}

std::string TypeResolver::to_pybind11_signature(const ParsedType& type) {
    return type.to_cpp_string();
}

std::string TypeResolver::strip_qualifiers(const std::string& type) {
    std::string result = type;

    // Remove const
    size_t const_pos = result.find("const");
    while (const_pos != std::string::npos) {
        result.erase(const_pos, 5);
        const_pos = result.find("const");
    }

    // Remove &, *
    result.erase(std::remove(result.begin(), result.end(), '&'), result.end());
    result.erase(std::remove(result.begin(), result.end(), '*'), result.end());

    // Remove leading/trailing whitespace
    result.erase(0, result.find_first_not_of(" \t\n\r"));
    result.erase(result.find_last_not_of(" \t\n\r") + 1);

    return result;
}

std::string TypeResolver::normalize_type(const std::string& type) {
    std::string normalized = strip_qualifiers(type);

    // Normalize common types
    if (normalized == "string") return "std::string";
    if (normalized == "vector") return "std::vector";
    if (normalized == "map") return "std::map";

    return normalized;
}

bool TypeResolver::is_container_type(const std::string& type) {
    std::string lower = to_lower(type);
    return lower.find("vector") != std::string::npos ||
           lower.find("map") != std::string::npos ||
           lower.find("set") != std::string::npos ||
           lower.find("array") != std::string::npos ||
           lower.find("list") != std::string::npos;
}

bool TypeResolver::is_primitive_type(const std::string& type) {
    static const std::set<std::string> primitives = {
        "int", "long", "short", "char",
        "float", "double",
        "bool",
        "void",
        "unsigned", "signed"
    };

    std::string clean_type = strip_qualifiers(type);
    return primitives.count(clean_type) > 0;
}

bool TypeResolver::is_numeric_type(const std::string& type) {
    static const std::set<std::string> numerics = {
        "int", "long", "short", "char",
        "float", "double",
        "unsigned", "signed",
        "int8_t", "int16_t", "int32_t", "int64_t",
        "uint8_t", "uint16_t", "uint32_t", "uint64_t",
        "size_t"
    };

    std::string clean_type = strip_qualifiers(type);
    return numerics.count(clean_type) > 0;
}

bool TypeResolver::requires_custom_converter(const ParsedType& type) {
    return is_container_type(type.base_name) ||
           (!is_primitive_type(type.base_name) && !is_container_type(type.base_name));
}

std::vector<std::string> TypeResolver::split_template_args(const std::string& args) {
    std::vector<std::string> result;
    std::string current;
    int depth = 0;

    for (char c : args) {
        if (c == '<') {
            depth++;
            current += c;
        } else if (c == '>') {
            depth--;
            current += c;
        } else if (c == ',' && depth == 0) {
            // Remove leading/trailing whitespace
            current.erase(0, current.find_first_not_of(" \t"));
            current.erase(current.find_last_not_of(" \t") + 1);
            if (!current.empty()) {
                result.push_back(current);
            }
            current.clear();
        } else {
            current += c;
        }
    }

    // Add last argument
    current.erase(0, current.find_first_not_of(" \t"));
    current.erase(current.find_last_not_of(" \t") + 1);
    if (!current.empty()) {
        result.push_back(current);
    }

    return result;
}

std::string TypeResolver::extract_template_content(const std::string& type_str) {
    size_t start = type_str.find('<');
    if (start == std::string::npos) return "";

    size_t end = type_str.rfind('>');
    if (end == std::string::npos || end <= start) return "";

    return type_str.substr(start + 1, end - start - 1);
}

std::string TypeResolver::to_lower(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
                  [](unsigned char c) { return std::tolower(c); });
    return result;
}

// ============================================================================
// ContainerBindings Implementation
// ============================================================================

std::string ContainerBindings::generate_vector_binding(const std::string& element_type,
                                                       const std::string& module_var) {
    std::ostringstream code;
    std::string sanitized = sanitize_type_name(element_type);

    code << "    // Vector binding for " << element_type << "\n";
    code << "    py::bind_vector<std::vector<" << element_type << ">>(";
    code << module_var << ", \"vector_" << sanitized << "\");\n\n";

    return code.str();
}

std::string ContainerBindings::generate_map_binding(const std::string& key_type,
                                                    const std::string& value_type,
                                                    const std::string& module_var) {
    std::ostringstream code;
    std::string sanitized_key = sanitize_type_name(key_type);
    std::string sanitized_val = sanitize_type_name(value_type);

    code << "    // Map binding for " << key_type << " -> " << value_type << "\n";
    code << "    py::bind_map<std::map<" << key_type << ", " << value_type << ">>(";
    code << module_var << ", \"map_" << sanitized_key << "_" << sanitized_val << "\");\n\n";

    return code.str();
}

std::string ContainerBindings::generate_nested_container_binding(const TypeMetadata& type,
                                                                 const std::string& module_var) {
    std::ostringstream code;

    // For nested containers, we need to bind inner containers first
    if (type.category == TypeMetadata::VECTOR_TYPE && !type.template_args.empty()) {
        const auto& element = type.template_args[0];

        // If element is also a container, bind it first
        if (element.is_container()) {
            code << generate_nested_container_binding(element, module_var);
        }

        code << generate_vector_binding(element.base_type, module_var);
    }

    return code.str();
}

std::set<std::string> ContainerBindings::find_used_containers(const ModuleDescriptor& module) {
    std::set<std::string> containers;

    // Check function parameters and return types
    for (const auto& func : module.functions) {
        for (const auto& [type, name] : func.params) {
            if (TypeResolver::is_container_type(type)) {
                containers.insert(type);
            }
        }
    }

    // Check class fields
    for (const auto& cls : module.classes) {
        for (const auto& [type, name] : cls.params) {
            if (TypeResolver::is_container_type(type)) {
                containers.insert(type);
            }
        }
    }

    // Check struct fields
    for (const auto& st : module.structs) {
        for (const auto& [type, name] : st.fields) {
            if (TypeResolver::is_container_type(type)) {
                containers.insert(type);
            }
        }
    }

    return containers;
}

std::string ContainerBindings::sanitize_type_name(const std::string& type) {
    std::string result = type;

    // Replace problematic characters
    std::replace(result.begin(), result.end(), ':', '_');
    std::replace(result.begin(), result.end(), '<', '_');
    std::replace(result.begin(), result.end(), '>', '_');
    std::replace(result.begin(), result.end(), ',', '_');
    std::replace(result.begin(), result.end(), ' ', '_');
    std::replace(result.begin(), result.end(), '*', '_');
    std::replace(result.begin(), result.end(), '&', '_');

    // Remove consecutive underscores
    auto new_end = std::unique(result.begin(), result.end(),
                               [](char a, char b) { return a == '_' && b == '_'; });
    result.erase(new_end, result.end());

    // Remove leading/trailing underscores
    while (!result.empty() && result.front() == '_') result.erase(0, 1);
    while (!result.empty() && result.back() == '_') result.pop_back();

    return result;
}

}} // namespace includecpp::generator
