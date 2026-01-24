#pragma once
#include <string>
#include <vector>
#include <set>
#include <regex>
#include "parser.h"

namespace includecpp {
namespace generator {

// Type String Parser - Parses C++ type strings into structured metadata
class TypeResolver {
public:
    struct ParsedType {
        std::string base_name;          // "vector", "map", "Point"
        bool is_template = false;
        std::vector<ParsedType> template_args;
        bool is_const = false;
        bool is_reference = false;
        bool is_pointer = false;

        std::string to_cpp_string() const;
        std::string to_python_hint() const;
    };

    // Parse type string: "const vector<Point<int>>&" → ParsedType
    static ParsedType parse_type(const std::string& type_str);

    // Type conversions
    static std::string to_python_hint(const ParsedType& type);
    static std::string to_pybind11_signature(const ParsedType& type);
    static std::string strip_qualifiers(const std::string& type);
    static std::string normalize_type(const std::string& type);

    // Type queries
    static bool is_container_type(const std::string& type);
    static bool is_primitive_type(const std::string& type);
    static bool is_numeric_type(const std::string& type);
    static bool requires_custom_converter(const ParsedType& type);

private:
    static std::vector<std::string> split_template_args(const std::string& args);
    static std::string extract_template_content(const std::string& type_str);
    static std::string to_lower(const std::string& str);
};

// Container Bindings Generator - Generates pybind11 bindings for STL containers
class ContainerBindings {
public:
    // Generate pybind11 bindings for containers
    static std::string generate_vector_binding(const std::string& element_type,
                                               const std::string& module_var);

    static std::string generate_map_binding(const std::string& key_type,
                                            const std::string& value_type,
                                            const std::string& module_var);

    static std::string generate_nested_container_binding(const TypeMetadata& type,
                                                         const std::string& module_var);

    // Helper: Detect which containers are used in module
    static std::set<std::string> find_used_containers(const ModuleDescriptor& module);

private:
    static std::string sanitize_type_name(const std::string& type);
};

}} // namespace includecpp::generator
