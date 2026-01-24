#pragma once
#include <string>
#include <vector>
#include <map>
#include <set>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <filesystem>

/*
This Api is made for Python <-> C++ communication via pybind11.
This Api Provides several API calls that can be extenden in other c++ modules or directly be imported as function in python.
For Adding External C++ Modules (simply plugins). Add a Announcer file '<modulename>.cp' in the folder 'src/plugins/'.
This file connects the external C++ module with the main application via this API. Allowing to also use the external C++ module functions in python via pybind11.
This API Manager will automatically load all plugins in the folder 'src/plugins/' on startup.
*/

/*  Basic ShowOff of .cp

SOURCE(<here_your_path_to_module.cpp>) && HEADER(<here_your_path_to_module.h>) <name_your_module>

~oder nur cpp ohne header~
SOURCE(<here_your_path_to_module.cpp>) <name_your_module>


PUBLIC(
    <name_your_module> FUNC(<funcname>)
    <name_your_module> FUNC2(<funcname>>)
    <name_your_module> CLASS(<ClassName>)
    <name_your_module> VAR(<VariableName>)
)
~ wenn alle dann~
PUBLIC(
    ALL
)
*/

/* The Best is, you also can give and Take params! Here another Example based on real usecase:
fast_list.cp:

SOURCE(/src/include/fast_list.cpp) && HEADER(/src/include/fast_list.h) fast_list
PUBLIC(
    fast_list CLASS(FastList) && PY_PARAM(list, "List to convert") && PY_PARAM(int, "Pointer count")
    fast_list FUNC(fast_sort)
)
PY_PARAM ist rein optional und sollte nicht genutzt werden da Parameter auch von Pybind11 automatisch erkannt werden.
*/

// v2.3.5: Parameter metadata structure for IntelliSense
struct ParameterInfo {
    std::string name;
    std::string type;
    std::string default_value;  // Empty if no default
    bool is_const = false;
    bool is_reference = false;
    bool is_pointer = false;
};

struct FunctionBinding {
    std::string module_name;
    std::string function_name;
    std::vector<std::pair<std::string, std::string>> params;
    std::string documentation;  // Function documentation from DOC()

    // v2.3.5: Enhanced signature metadata for IntelliSense
    std::string return_type = "void";
    std::vector<ParameterInfo> parameters;  // Enhanced parameter info
    bool is_const = false;
    bool is_static = false;
    bool is_inline = false;
    std::string full_signature;  // Full C++ signature for reference

    // v3.1.5: Template function support
    bool is_template = false;
    std::vector<std::string> template_types;  // For TEMPLATE_FUNC(name) TYPES(int, float)
};

// v2.3.5: Method signature metadata
// v2.4.13: Extended with param_types for overload resolution
struct MethodSignature {
    std::string name;
    std::string return_type;
    std::vector<ParameterInfo> parameters;
    std::vector<std::string> param_types;  // v2.4.13: ["const Circle&", "const Rect&"] for overload_cast
    bool is_const = false;
    bool is_static = false;
    bool is_virtual = false;
    bool is_override = false;
    std::string documentation;
};

// v2.3.5: Field metadata
// v4.6.6: Added array support
struct FieldInfo {
    std::string name;
    std::string type;
    bool is_static = false;
    bool is_const = false;
    bool is_array = false;        // v4.6.6: Is this a C-style array?
    int array_size = 0;           // v4.6.6: Size of array (0 if not array)
    std::string documentation;
};

// v2.4.3: Constructor parameter types
struct ConstructorInfo {
    std::vector<std::string> param_types;  // e.g., ["double", "double"] for Vector2D(double, double)
};

struct ClassBinding {
    std::string module_name;
    std::string class_name;
    std::vector<std::pair<std::string, std::string>> params;
    std::vector<std::string> methods;    // Method names to bind
    std::vector<std::string> fields;     // Field names to bind
    std::vector<ConstructorInfo> constructors;  // v2.4.3: Constructor overloads
    bool auto_bind_all;                  // Bind all methods automatically
    std::string documentation;           // Class documentation from DOC()
    std::map<std::string, std::string> method_docs;  // Method-specific docs: method_name -> doc

    // v2.3.5: Enhanced method and field signatures
    std::vector<MethodSignature> method_signatures;
    std::vector<FieldInfo> field_infos;
};

struct VariableBinding {
    std::string module_name;
    std::string variable_name;
    std::string documentation;  // Variable documentation from DOC()
};

// v4.6.5: ENUM() Bindings for C++ enums
struct EnumBinding {
    std::string module_name;
    std::string enum_name;
    std::vector<std::string> values;  // Enum values to expose
    bool export_values = true;        // Call .export_values() to export to module scope
    bool is_class_enum = false;       // enum class vs plain enum
    std::string documentation;
};

// v2.0: STRUCT() Bindings for Plain-Old-Data types
// v4.1.1: Added CONSTRUCTOR and METHOD support (same as CLASS)
struct StructBinding {
    std::string module_name;
    std::string struct_name;
    std::vector<FieldInfo> fields;  // v4.6.6: Changed from pair to FieldInfo for array support
    std::vector<std::string> template_types;  // For STRUCT(Point) TYPES(int, float)
    bool is_template = false;
    std::string documentation;

    // v4.1.1: CONSTRUCTOR and METHOD support for STRUCT (same as CLASS)
    std::vector<ConstructorInfo> constructors;
    std::vector<MethodSignature> method_signatures;
    std::vector<std::string> methods;  // Simple method names for backward compatibility

    // Helper methods
    std::string get_full_name() const {
        return struct_name;
    }

    std::string get_template_suffix(const std::string& type) const {
        return "_" + type;
    }
};

// v2.0: Enhanced Type Metadata for type resolution
struct TypeMetadata {
    enum TypeCategory {
        PRIMITIVE,      // int, float, double, string, bool
        STRUCT_TYPE,    // User-defined struct
        VECTOR_TYPE,    // std::vector<T>
        MAP_TYPE,       // std::map<K,V>
        CLASS_TYPE,     // Full C++ class with methods
        UNKNOWN
    };

    TypeCategory category = UNKNOWN;
    std::string base_type;              // "vector", "map", "Point"
    std::string full_signature;         // "std::vector<Point>", "std::map<string, int>"
    std::vector<TypeMetadata> template_args;  // Recursive for nested types
    bool is_const = false;
    bool is_reference = false;
    bool is_pointer = false;

    // Conversion methods
    std::string to_python_type_hint() const;
    std::string to_pybind11_type() const;
    std::string to_cpp_type() const;
    bool is_container() const {
        return category == VECTOR_TYPE || category == MAP_TYPE;
    }
    bool requires_custom_converter() const {
        return is_container() || category == STRUCT_TYPE;
    }
};

// v2.0: Module Dependencies (DEPENDS keyword)
struct ModuleDependency {
    std::string target_module;              // Dependent module
    std::vector<std::string> required_types;  // Required Structs/Classes
    bool is_optional = false;               // Optional dependency
};

// v2.0: Enhanced ModuleDescriptor with structs and dependencies
struct ModuleDescriptor {
    std::string module_name;
    std::string source_path;
    std::string header_path;
    bool has_header;
    bool expose_all;

    // Bindings Collections
    std::vector<FunctionBinding> functions;
    std::vector<ClassBinding> classes;
    std::vector<StructBinding> structs;           // v2.0: NEW
    std::vector<VariableBinding> variables;
    std::vector<EnumBinding> enums;               // v4.6.5: NEW

    // Dependencies & Multi-Source (v2.0)
    std::vector<ModuleDependency> dependencies;   // v2.0: NEW
    std::vector<std::string> additional_sources;  // v2.0: NEW - SOURCES(a.cpp, b.cpp)

    // Metadata
    std::string version;
    std::map<std::string, std::string> metadata;
};

// v2.0: Type Registry for Cross-Module Type Resolution
class TypeRegistry {
public:
    // Type Registration
    void register_struct(const std::string& module, const StructBinding& s);
    void register_class(const std::string& module, const ClassBinding& c);
    void register_dependency(const std::string& from_module, const ModuleDependency& dep);

    // Type Resolution
    TypeMetadata resolve_type(const std::string& type_string) const;
    bool is_struct(const std::string& type_name) const;
    bool is_class(const std::string& type_name) const;
    bool type_exists(const std::string& type_name) const;

    // Dependency Management
    std::vector<std::string> get_dependencies(const std::string& module) const;
    std::vector<std::string> get_dependency_order() const;  // Topological sort
    bool has_circular_dependency() const;
    std::vector<std::string> get_circular_path() const;

    // Module Info
    std::string get_module_for_type(const std::string& type_name) const;
    std::vector<std::string> get_all_modules() const;

private:
    std::map<std::string, StructBinding> structs_;
    std::map<std::string, ClassBinding> classes_;
    std::map<std::string, std::string> type_to_module_;
    std::map<std::string, std::vector<ModuleDependency>> dependencies_;

    // Helper methods
    std::vector<std::string> topological_sort() const;
    bool has_cycle_dfs(const std::string& module,
                       std::set<std::string>& visited,
                       std::set<std::string>& rec_stack,
                       std::vector<std::string>& path) const;
};

class API
{
public:
    static int main(int argc, char* argv[]);
    static std::vector<ModuleDescriptor> parse_all_cp_files(const std::string& plugins_dir);
    static ModuleDescriptor parse_cp_file(const std::string& filepath);
    static std::string generate_pybind11_code(const std::vector<ModuleDescriptor>& modules);
    static std::string generate_class_bindings(const ClassBinding& cls, const ModuleDescriptor& mod);
    static bool validate_bindings_code(const std::string& code);
    static void validate_module_name(const std::string& name, int line_num);
    static void validate_namespace_includecpp(const std::string& source_path, const std::string& module_name);
    static bool write_files(const std::vector<ModuleDescriptor>& modules,
                           const std::string& bindings_path,
                           const std::string& sources_path);
    static std::string compute_file_hash(const std::string& filepath);
    static std::string generate_registry_json(const std::vector<ModuleDescriptor>& modules, const std::string& plugins_dir);

    // v2.3.5: Signature extraction for IntelliSense
    static std::vector<FunctionBinding> parse_cpp_function_signatures(const std::string& cpp_file_path);
    static std::vector<ParameterInfo> parse_parameter_list(const std::string& params_str);

private:
    static std::string trim(const std::string& str);
    static std::vector<std::string> split(const std::string& str, char delimiter);
    static std::string extract_between(const std::string& str, char open, char close);
    static std::string safe_extract_between(const std::string& str,
                                           size_t start_pos,
                                           size_t end_pos,
                                           const std::string& context);
    static bool starts_with(const std::string& str, const std::string& prefix);
    static std::string normalize_path(const std::string& path);
    static std::string replace_all(std::string str, const std::string& from, const std::string& to);
    static std::string extract_doc_string(const std::string& str);
    static std::map<std::string, std::string> parse_doc_statements(const std::string& content);
};