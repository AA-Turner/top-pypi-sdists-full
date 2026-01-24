#include "parser.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <regex>
#include <ctime>
#include <iomanip>
#include <functional>
#include <filesystem>
#include <iterator>
#include <set>

int API::main(int argc, char* argv[]) {
    if (argc < 5) {
        std::cerr << "Usage: plugin_gen <plugins_dir> <bindings_output> <sources_output> <registry_output>" << std::endl;
        return 1;
    }

    std::string plugins_dir = argv[1];
    std::string bindings_output = argv[2];
    std::string sources_output = argv[3];
    std::string registry_output = argv[4];

    std::cout << "Plugin Generator starting..." << std::endl;
    std::cout << "Plugins directory: " << plugins_dir << std::endl;
    std::cout << "Output: " << bindings_output << std::endl;

    auto modules = parse_all_cp_files(plugins_dir);
    if (modules.empty()) {
        std::cerr << "ERROR: No modules found or parsed successfully in " << plugins_dir << std::endl;
        std::cerr << "Please ensure:" << std::endl;
        std::cerr << "  1. The plugins directory exists" << std::endl;
        std::cerr << "  2. There are .cp files in the directory" << std::endl;
        std::cerr << "  3. The .cp files have valid syntax" << std::endl;
        return 1;  // Exit with error if no modules found
    }

    if (!write_files(modules, bindings_output, sources_output)) {
        std::cerr << "ERROR: Failed to write output files!" << std::endl;
        return 1;
    }

    std::string registry_json = generate_registry_json(modules, plugins_dir);
    std::ofstream registry_file(registry_output);
    if (!registry_file.is_open()) {
        std::cerr << "ERROR: Cannot open registry file for writing: " << registry_output << std::endl;
        return 1;
    }

    registry_file << registry_json;

    if (registry_file.fail() || registry_file.bad()) {
        std::cerr << "ERROR: Failed to write to registry file: " << registry_output << std::endl;
        registry_file.close();
        return 1;
    }
    registry_file.close();

    std::cout << "SUCCESS: Generated bindings for " << modules.size() << " module(s)" << std::endl;
    return 0;
}

std::vector<ModuleDescriptor> API::parse_all_cp_files(const std::string& plugins_dir) {
    std::vector<ModuleDescriptor> modules;

    if (!std::filesystem::exists(plugins_dir)) {
        std::cerr << "ERROR: Plugins directory does not exist: " << plugins_dir << std::endl;
        std::cerr << "Current working directory: " << std::filesystem::current_path() << std::endl;
        return modules;
    }

    std::cout << "Scanning for .cp files in: " << plugins_dir << std::endl;

    int cp_file_count = 0;
    for (const auto& entry : std::filesystem::directory_iterator(plugins_dir)) {
        if (entry.path().extension() == ".cp") {
            cp_file_count++;
            std::cout << "Found .cp file: " << entry.path().filename() << std::endl;
            try {
                modules.push_back(parse_cp_file(entry.path().string()));
                std::cout << "  [OK] Successfully parsed: " << entry.path().filename() << std::endl;
            } catch (const std::exception& e) {
                std::cerr << "  [ERROR] Parsing " << entry.path().filename() << ": " << e.what() << std::endl;
            }
        }
    }

    if (cp_file_count == 0) {
        std::cerr << "ERROR: No .cp files found in directory" << std::endl;
    } else {
        std::cout << "Total: " << cp_file_count << " .cp file(s) found, "
                  << modules.size() << " successfully parsed" << std::endl;
    }

    return modules;
}

void API::validate_module_name(const std::string& name, int line_num) {
    if (name.empty()) {
        throw std::runtime_error("Line " + std::to_string(line_num) +
                                ": Empty module name");
    }

    if (!std::isalpha(static_cast<unsigned char>(name[0])) && name[0] != '_') {
        throw std::runtime_error("Line " + std::to_string(line_num) +
                                ": Invalid module name '" + name +
                                "' (must start with letter or underscore)");
    }

    for (char c : name) {
        if (!std::isalnum(static_cast<unsigned char>(c)) && c != '_') {
            throw std::runtime_error("Line " + std::to_string(line_num) +
                                    ": Invalid character '" + std::string(1, c) +
                                    "' in module name");
        }
    }
}

bool API::validate_bindings_code(const std::string& code) {
    int brace_count = 0;
    for (char c : code) {
        if (c == '{') brace_count++;
        if (c == '}') brace_count--;
        if (brace_count < 0) {
            std::cerr << "ERROR: Unbalanced braces (too many closing braces)" << std::endl;
            return false;
        }
    }

    if (brace_count != 0) {
        std::cerr << "ERROR: Unbalanced braces (missing " << brace_count << " closing braces)" << std::endl;
        return false;
    }

    if (code.find("#include <pybind11/pybind11.h>") == std::string::npos) {
        std::cerr << "ERROR: Missing required include: pybind11/pybind11.h" << std::endl;
        return false;
    }

    if (code.find("PYBIND11_MODULE(api, m)") == std::string::npos) {
        std::cerr << "ERROR: Missing PYBIND11_MODULE(api, m) definition" << std::endl;
        return false;
    }

    if (code.find(";;") != std::string::npos) {
        std::cerr << "WARNING: Double semicolon detected (possible syntax error)" << std::endl;
    }

    return true;
}

void API::validate_namespace_includecpp(const std::string& source_path, const std::string& module_name) {
    // Check if the source file contains "namespace includecpp"
    std::ifstream file(source_path);
    if (!file.is_open()) {
        // File doesn't exist yet or can't be opened - skip validation
        return;
    }

    std::string content((std::istreambuf_iterator<char>(file)),
                        std::istreambuf_iterator<char>());
    file.close();

    // Look for "namespace includecpp" with optional whitespace
    std::regex ns_regex(R"(\bnamespace\s+includecpp\s*\{)");
    if (!std::regex_search(content, ns_regex)) {
        std::string error_msg =
            "\n"
            "+============================================================================+\n"
            "|  NAMESPACE ERROR                                                           |\n"
            "+============================================================================+\n"
            "\n"
            "Module: " + module_name + "\n"
            "Source: " + source_path + "\n"
            "\n"
            "ERROR: Source file must contain 'namespace includecpp { ... }'\n"
            "\n"
            "All IncludeCPP code must be wrapped in the 'includecpp' namespace.\n"
            "This is required for proper Python binding generation.\n"
            "\n"
            "Example:\n"
            "\n"
            "  #include <string>\n"
            "  \n"
            "  namespace includecpp {\n"
            "      \n"
            "      int add(int a, int b) {\n"
            "          return a + b;\n"
            "      }\n"
            "      \n"
            "      class MyClass {\n"
            "      public:\n"
            "          void hello() { ... }\n"
            "      };\n"
            "      \n"
            "  } // namespace includecpp\n"
            "\n";
        throw std::runtime_error(error_msg);
    }
}

ModuleDescriptor API::parse_cp_file(const std::string& filepath) {
    ModuleDescriptor desc;
    desc.has_header = false;
    desc.expose_all = false;

    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filepath);
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();

    auto lines = split(content, '\n');

    bool in_public_block = false;
    std::string public_content;
    int line_num = 0;

    for (const auto& line_raw : lines) {
        line_num++;
        std::string line = trim(line_raw);
        if (line.empty() || line[0] == '#') continue;

#ifdef VSRAM_DEBUG
        std::cout << "DEBUG: Processing line " << line_num << ": " << line << std::endl;
#endif

        if (!in_public_block) {
            if (starts_with(line, "SOURCE")) {
                // v4.6.5: Support multiple SOURCE() and HEADER() declarations
                // Format: SOURCE(file1) && SOURCE(file2) && HEADER(h) module_name

                // Find ALL SOURCE(...) declarations
                std::regex source_regex(R"(SOURCE\s*\(\s*([^)]+)\s*\))");
                std::sregex_iterator source_it(line.begin(), line.end(), source_regex);
                std::sregex_iterator end_it;
                bool first_source = true;
                while (source_it != end_it) {
                    std::string src_content = trim((*source_it)[1].str());
                    // Handle space/comma-separated files within one SOURCE()
                    std::istringstream iss(src_content);
                    std::string single_src;
                    while (iss >> single_src) {
                        // Remove trailing comma if present
                        if (!single_src.empty() && single_src.back() == ',') {
                            single_src.pop_back();
                        }
                        if (!single_src.empty()) {
                            if (first_source && desc.source_path.empty()) {
                                desc.source_path = single_src;
                                first_source = false;
                            } else {
                                desc.additional_sources.push_back(single_src);
                            }
                        }
                    }
                    ++source_it;
                }

                // Find ALL HEADER(...) declarations
                std::regex header_regex(R"(HEADER\s*\(\s*([^)]+)\s*\))");
                std::sregex_iterator header_it(line.begin(), line.end(), header_regex);
                bool first_header = true;
                while (header_it != end_it) {
                    std::string hdr_content = trim((*header_it)[1].str());
                    // Handle space/comma-separated headers within one HEADER()
                    std::istringstream hss(hdr_content);
                    std::string single_hdr;
                    while (hss >> single_hdr) {
                        if (!single_hdr.empty() && single_hdr.back() == ',') {
                            single_hdr.pop_back();
                        }
                        if (!single_hdr.empty()) {
                            if (first_header) {
                                desc.header_path = single_hdr;
                                desc.has_header = true;
                                first_header = false;
                            }
                            // Additional headers can be stored if needed in future
                        }
                    }
                    ++header_it;
                }

                // Module name is at the end after all declarations
                size_t last_space = line.rfind(' ');
                if (last_space != std::string::npos) {
                    desc.module_name = trim(line.substr(last_space + 1));
                    validate_module_name(desc.module_name, line_num);
                }
            }
            // v2.0: Parse SOURCES() for multi-file modules
            else if (starts_with(line, "SOURCES")) {
                size_t sources_start = line.find('(');
                size_t sources_end = line.find(')');
                if (sources_start != std::string::npos && sources_end != std::string::npos) {
                    std::string sources_str = line.substr(sources_start + 1, sources_end - sources_start - 1);
                    auto source_files = split(sources_str, ',');
                    for (auto& src : source_files) {
                        desc.additional_sources.push_back(trim(src));
                    }
                }
            }
            // v2.0: Parse DEPENDS() for module dependencies
            else if (starts_with(line, "DEPENDS")) {
                size_t depends_start = line.find('(');
                size_t depends_end = line.find(')');
                if (depends_start != std::string::npos && depends_end != std::string::npos) {
                    std::string depends_str = line.substr(depends_start + 1, depends_end - depends_start - 1);
                    auto modules = split(depends_str, ',');

                    for (const auto& mod : modules) {
                        std::string trimmed = trim(mod);
                        ModuleDependency dep;

                        // Check for type list: module[Type1, Type2]
                        size_t bracket_start = trimmed.find('[');
                        if (bracket_start != std::string::npos) {
                            dep.target_module = trimmed.substr(0, bracket_start);
                            size_t bracket_end = trimmed.find(']');
                            if (bracket_end != std::string::npos) {
                                std::string types_str = trimmed.substr(bracket_start + 1, bracket_end - bracket_start - 1);
                                auto types = split(types_str, ',');
                                for (auto& t : types) {
                                    dep.required_types.push_back(trim(t));
                                }
                            }
                        } else {
                            dep.target_module = trimmed;
                        }

                        desc.dependencies.push_back(dep);
                    }
                }
            }
            else if (starts_with(line, "PUBLIC")) {
                in_public_block = true;
                size_t paren = line.find('(');
                if (paren != std::string::npos) {
                    public_content += line.substr(paren + 1);
                }
            }
        }
        else {
            public_content += "\n" + line;
        }
    }

    size_t last_paren = public_content.rfind(')');
    if (last_paren != std::string::npos) {
        public_content = public_content.substr(0, last_paren);
    }

    public_content = trim(public_content);

#ifdef VSRAM_DEBUG
    std::cout << "DEBUG: public_content = [" << public_content << "]" << std::endl;
#endif

    if (trim(public_content) == "ALL") {
        desc.expose_all = true;
    }
    else {
        auto public_lines = split(public_content, '\n');
#ifdef VSRAM_DEBUG
        std::cout << "DEBUG: Found " << public_lines.size() << " lines in PUBLIC block" << std::endl;
#endif

        for (size_t i = 0; i < public_lines.size(); ++i) {
            std::string cleaned = trim(public_lines[i]);
            if (cleaned.empty()) continue;

            size_t and_pos = cleaned.find("&&");
            if (and_pos != std::string::npos) {
                cleaned = trim(cleaned.substr(0, and_pos));
            }

            if (cleaned.find("TEMPLATE_FUNC") != std::string::npos) {
                FunctionBinding fb;
                fb.is_template = true;
                auto parts = split(cleaned, ' ');
                if (parts.size() >= 2) {
                    fb.module_name = parts[0];

                    size_t tfunc_pos = cleaned.find("TEMPLATE_FUNC(");
                    if (tfunc_pos != std::string::npos) {
                        size_t func_start = tfunc_pos + 13;
                        size_t func_end = cleaned.find(')', func_start);
                        fb.function_name = safe_extract_between(cleaned, func_start, func_end, "TEMPLATE_FUNC");
                    }

                    size_t types_pos = cleaned.find("TYPES(");
                    if (types_pos != std::string::npos) {
                        size_t types_start = types_pos + 6;
                        size_t types_end = cleaned.find(')', types_start);
                        if (types_end != std::string::npos) {
                            std::string types_str = cleaned.substr(types_start, types_end - types_start);
                            auto types = split(types_str, ',');
                            for (auto& t : types) {
                                fb.template_types.push_back(trim(t));
                            }
                        }
                    }

                    desc.functions.push_back(fb);
                }
            }
            else if (cleaned.find("FUNC") != std::string::npos) {
                FunctionBinding fb;
                auto parts = split(cleaned, ' ');
                if (parts.size() >= 2) {
                    fb.module_name = parts[0];

                    size_t func_start = cleaned.find('(');
                    size_t func_end = cleaned.find(')');
                    fb.function_name = safe_extract_between(cleaned, func_start, func_end, "FUNC");
                    desc.functions.push_back(fb);
                }
            }
            // v4.6.5: Check ENUM before CLASS (ENUM lines may contain "CLASS" keyword)
            else if (cleaned.find("ENUM(") != std::string::npos) {
                EnumBinding eb;
                auto parts = split(cleaned, ' ');
                if (parts.size() >= 2) {
                    eb.module_name = parts[0];

                    size_t enum_start = cleaned.find("ENUM(");
                    size_t enum_end = cleaned.find(')', enum_start);
                    size_t enum_paren = enum_start + 4;  // Position of '(' in "ENUM("
                    eb.enum_name = safe_extract_between(cleaned, enum_paren, enum_end, "ENUM");

                    // Check for CLASS keyword (enum class vs plain enum)
                    if (cleaned.find(" CLASS") != std::string::npos) {
                        eb.is_class_enum = true;
                    }

                    // Check for NOEXPORT keyword
                    if (cleaned.find("NOEXPORT") != std::string::npos) {
                        eb.export_values = false;
                    }

                    // Check for VALUES block: ENUM(Name) { VALUE1 VALUE2 ... }
                    size_t brace_open = cleaned.find('{');
                    if (brace_open != std::string::npos) {
                        std::string values_block;
                        size_t brace_close = cleaned.find('}', brace_open);
                        if (brace_close != std::string::npos) {
                            values_block = cleaned.substr(brace_open + 1, brace_close - brace_open - 1);
                        } else {
                            // Multi-line - collect from next lines
                            for (size_t j = i + 1; j < public_lines.size(); ++j) {
                                std::string next_line = trim(public_lines[j]);
                                size_t close_pos = next_line.find('}');
                                if (close_pos != std::string::npos) {
                                    values_block += next_line.substr(0, close_pos);
                                    i = j;
                                    break;
                                } else {
                                    values_block += next_line + " ";
                                }
                            }
                        }

                        // Parse enum values
                        std::istringstream vss(values_block);
                        std::string value;
                        while (vss >> value) {
                            if (!value.empty() && value.back() == ',') {
                                value.pop_back();
                            }
                            if (!value.empty()) {
                                eb.values.push_back(value);
                            }
                        }
                    }

                    desc.enums.push_back(eb);
                }
            }
            else if (cleaned.find("CLASS") != std::string::npos) {
                ClassBinding cb;
                cb.auto_bind_all = false;
                auto parts = split(cleaned, ' ');
                if (parts.size() >= 2) {
                    cb.module_name = parts[0];

                    size_t class_start = cleaned.find('(');
                    size_t class_end = cleaned.find(')');
                    cb.class_name = safe_extract_between(cleaned, class_start, class_end, "CLASS");

                    // Check for METHOD/FIELD block: CLASS(Name) { ... }
                    size_t brace_open = cleaned.find('{');
                    if (brace_open != std::string::npos) {
                        // Collect all lines until closing brace
                        std::string method_block;
                        bool found_close = false;

                        // Check if closing brace on same line
                        size_t brace_close = cleaned.find('}', brace_open);
                        if (brace_close != std::string::npos) {
                            method_block = cleaned.substr(brace_open + 1, brace_close - brace_open - 1);
                            found_close = true;
                        } else {
                            // Collect from next lines
                            for (size_t j = i + 1; j < public_lines.size(); ++j) {
                                std::string next_line = trim(public_lines[j]);
                                size_t close_pos = next_line.find('}');

                                if (close_pos != std::string::npos) {
                                    method_block += next_line.substr(0, close_pos);
                                    i = j;  // Skip these lines in main loop
                                    found_close = true;
                                    break;
                                } else {
                                    method_block += next_line + "\n";
                                }
                            }
                        }

                        // Parse METHOD(...) and FIELD(...) entries
                        auto method_lines = split(method_block, '\n');
                        for (const auto& mline : method_lines) {
                            std::string mtrim = trim(mline);
                            if (mtrim.empty()) continue;

                            // v2.4.3: Parse CONSTRUCTOR(type1, type2, ...) for parametrized constructors
                            if (mtrim.find("CONSTRUCTOR") != std::string::npos) {
                                size_t c_start = mtrim.find('(');
                                size_t c_end = mtrim.rfind(')');
                                if (c_start != std::string::npos && c_end != std::string::npos) {
                                    std::string params_str = mtrim.substr(c_start + 1, c_end - c_start - 1);
                                    ConstructorInfo ctor;
                                    if (!params_str.empty()) {
                                        auto params = split(params_str, ',');
                                        for (auto& p : params) {
                                            std::string param_type = trim(p);
                                            if (!param_type.empty()) {
                                                ctor.param_types.push_back(param_type);
                                            }
                                        }
                                    }
                                    cb.constructors.push_back(ctor);
                                }
                            }
                            // v2.4.13: Extended METHOD parsing with overload support
                            // Supports: METHOD(name), METHOD(name, type1, type2), METHOD_CONST(name, type1)
                            else if (mtrim.find("METHOD") != std::string::npos) {
                                MethodSignature sig;
                                bool is_const_method = mtrim.find("METHOD_CONST") != std::string::npos;

                                size_t m_start = mtrim.find('(');
                                size_t m_end = mtrim.rfind(')');  // Use rfind to handle nested templates

                                if (m_start != std::string::npos && m_end != std::string::npos) {
                                    std::string content = mtrim.substr(m_start + 1, m_end - m_start - 1);

                                    // Parse method name and optional parameter types
                                    // Format: "methodName" or "methodName, const Circle&, const Rect&"
                                    std::vector<std::string> parts;
                                    int template_depth = 0;
                                    std::string current_part;

                                    for (char c : content) {
                                        if (c == '<') {
                                            template_depth++;
                                            current_part += c;
                                        } else if (c == '>') {
                                            template_depth--;
                                            current_part += c;
                                        } else if (c == ',' && template_depth == 0) {
                                            parts.push_back(trim(current_part));
                                            current_part.clear();
                                        } else {
                                            current_part += c;
                                        }
                                    }
                                    if (!current_part.empty()) {
                                        parts.push_back(trim(current_part));
                                    }

                                    if (!parts.empty()) {
                                        sig.name = parts[0];
                                        sig.is_const = is_const_method;

                                        // Remaining parts are parameter types for overload resolution
                                        for (size_t i = 1; i < parts.size(); ++i) {
                                            sig.param_types.push_back(parts[i]);
                                        }

                                        // v3.3.22: Also populate parameters for display in get command
                                        for (size_t i = 0; i < sig.param_types.size(); ++i) {
                                            ParameterInfo param;
                                            std::string type_str = sig.param_types[i];
                                            param.type = type_str;
                                            param.name = "arg" + std::to_string(i + 1);
                                            // Check for const
                                            if (type_str.find("const ") != std::string::npos) {
                                                param.is_const = true;
                                            }
                                            // Check for reference
                                            if (!type_str.empty() && type_str.back() == '&') {
                                                param.is_reference = true;
                                            }
                                            // Check for pointer
                                            if (!type_str.empty() && type_str.back() == '*') {
                                                param.is_pointer = true;
                                            }
                                            sig.parameters.push_back(param);
                                        }

                                        cb.method_signatures.push_back(sig);
                                        // Also add to legacy methods list for backward compatibility
                                        cb.methods.push_back(sig.name);
                                    }
                                }
                            }
                            else if (mtrim.find("FIELD") != std::string::npos) {
                                size_t f_start = mtrim.find('(');
                                size_t f_end = mtrim.find(')');
                                if (f_start != std::string::npos && f_end != std::string::npos) {
                                    std::string field_name = safe_extract_between(mtrim, f_start, f_end, "FIELD");
                                    cb.fields.push_back(field_name);
                                }
                            }
                        }
                    }

                    desc.classes.push_back(cb);
                }
            }
            else if (cleaned.find("VAR") != std::string::npos) {
                VariableBinding vb;
                auto parts = split(cleaned, ' ');
                if (parts.size() >= 2) {
                    vb.module_name = parts[0];

                    size_t var_start = cleaned.find('(');
                    size_t var_end = cleaned.find(')');
                    vb.variable_name = safe_extract_between(cleaned, var_start, var_end, "VAR");
                    desc.variables.push_back(vb);
                }
            }
            // v2.0: Parse STRUCT() for Plain-Old-Data types
            else if (cleaned.find("STRUCT") != std::string::npos) {
                StructBinding sb;
                auto parts = split(cleaned, ' ');
                if (parts.size() >= 2) {
                    sb.module_name = parts[0];

                    size_t struct_start = cleaned.find("STRUCT(");
                    size_t struct_end = cleaned.find(')', struct_start);
                    // safe_extract_between adds +1 to start_pos, so pass position of '(' not after it
                    size_t struct_paren = struct_start + 6;  // Position of '(' in "STRUCT("
                    sb.struct_name = safe_extract_between(cleaned, struct_paren, struct_end, "STRUCT");

                    // Check for TYPES() clause for template structs
                    size_t types_pos = cleaned.find("TYPES(");
                    if (types_pos != std::string::npos) {
                        sb.is_template = true;
                        size_t types_start = types_pos + 6;
                        size_t types_end = cleaned.find(')', types_start);
                        if (types_end != std::string::npos) {
                            std::string types_str = cleaned.substr(types_start, types_end - types_start);
                            auto types = split(types_str, ',');
                            for (auto& t : types) {
                                sb.template_types.push_back(trim(t));
                            }
                        }
                    }

                    // Check for FIELD block: STRUCT(Name) { FIELD(type, name) ... }
                    size_t brace_open = cleaned.find('{');
                    if (brace_open != std::string::npos) {
                        std::string field_block;
                        bool found_close = false;

                        // Check if closing brace on same line
                        size_t brace_close = cleaned.find('}', brace_open);
                        if (brace_close != std::string::npos) {
                            field_block = cleaned.substr(brace_open + 1, brace_close - brace_open - 1);
                            found_close = true;
                        } else {
                            // Collect from next lines
                            for (size_t j = i + 1; j < public_lines.size(); ++j) {
                                std::string next_line = trim(public_lines[j]);
                                size_t close_pos = next_line.find('}');

                                if (close_pos != std::string::npos) {
                                    field_block += next_line.substr(0, close_pos);
                                    i = j;  // Skip these lines in main loop
                                    found_close = true;
                                    break;
                                } else {
                                    field_block += next_line + "\n";
                                }
                            }
                        }

                        // v4.1.1: Parse CONSTRUCTOR, METHOD, and FIELD entries for STRUCT
                        auto field_lines = split(field_block, '\n');
                        for (const auto& fline : field_lines) {
                            std::string ftrim = trim(fline);
                            if (ftrim.empty()) continue;

                            // v4.1.1: Parse CONSTRUCTOR(type1, type2, ...) for parametrized constructors
                            if (ftrim.find("CONSTRUCTOR") != std::string::npos) {
                                size_t c_start = ftrim.find('(');
                                size_t c_end = ftrim.rfind(')');
                                if (c_start != std::string::npos && c_end != std::string::npos) {
                                    std::string params_str = ftrim.substr(c_start + 1, c_end - c_start - 1);
                                    ConstructorInfo ctor;
                                    if (!params_str.empty()) {
                                        auto params = split(params_str, ',');
                                        for (auto& p : params) {
                                            std::string param_type = trim(p);
                                            if (!param_type.empty()) {
                                                ctor.param_types.push_back(param_type);
                                            }
                                        }
                                    }
                                    sb.constructors.push_back(ctor);
                                }
                            }
                            // v4.1.1: Parse METHOD and METHOD_CONST for STRUCT
                            else if (ftrim.find("METHOD") != std::string::npos) {
                                MethodSignature sig;
                                bool is_const_method = ftrim.find("METHOD_CONST") != std::string::npos;

                                size_t m_start = ftrim.find('(');
                                size_t m_end = ftrim.rfind(')');

                                if (m_start != std::string::npos && m_end != std::string::npos) {
                                    std::string content = ftrim.substr(m_start + 1, m_end - m_start - 1);

                                    // Parse method name and optional parameter types
                                    std::vector<std::string> parts;
                                    int template_depth = 0;
                                    std::string current_part;

                                    for (char c : content) {
                                        if (c == '<') {
                                            template_depth++;
                                            current_part += c;
                                        } else if (c == '>') {
                                            template_depth--;
                                            current_part += c;
                                        } else if (c == ',' && template_depth == 0) {
                                            parts.push_back(trim(current_part));
                                            current_part.clear();
                                        } else {
                                            current_part += c;
                                        }
                                    }
                                    if (!current_part.empty()) {
                                        parts.push_back(trim(current_part));
                                    }

                                    if (!parts.empty()) {
                                        sig.name = parts[0];
                                        sig.is_const = is_const_method;

                                        // Remaining parts are parameter types
                                        for (size_t k = 1; k < parts.size(); ++k) {
                                            sig.param_types.push_back(parts[k]);
                                        }

                                        sb.method_signatures.push_back(sig);
                                        sb.methods.push_back(sig.name);
                                    }
                                }
                            }
                            // v4.6.6: Parse FIELD_ARRAY(name, type, size) for C-style arrays
                            else if (ftrim.find("FIELD_ARRAY(") != std::string::npos) {
                                size_t f_start = ftrim.find('(');
                                size_t f_end = ftrim.find(')');
                                if (f_start != std::string::npos && f_end != std::string::npos) {
                                    std::string field_content = ftrim.substr(f_start + 1, f_end - f_start - 1);
                                    auto field_parts = split(field_content, ',');
                                    if (field_parts.size() >= 3) {
                                        FieldInfo fi;
                                        fi.name = trim(field_parts[0]);
                                        fi.type = trim(field_parts[1]);
                                        fi.is_array = true;
                                        fi.array_size = std::stoi(trim(field_parts[2]));
                                        sb.fields.push_back(fi);
                                    }
                                }
                            }
                            // Parse FIELD(name) or FIELD(type, name)
                            else if (ftrim.find("FIELD(") != std::string::npos) {
                                size_t f_start = ftrim.find('(');
                                size_t f_end = ftrim.find(')');
                                if (f_start != std::string::npos && f_end != std::string::npos) {
                                    std::string field_content = ftrim.substr(f_start + 1, f_end - f_start - 1);
                                    auto field_parts = split(field_content, ',');

                                    FieldInfo fi;
                                    if (field_parts.size() >= 2) {
                                        fi.type = trim(field_parts[0]);
                                        fi.name = trim(field_parts[1]);
                                    } else if (field_parts.size() == 1) {
                                        // Simple FIELD(name) - type will be inferred
                                        fi.type = "auto";
                                        fi.name = trim(field_parts[0]);
                                    }
                                    fi.is_array = false;
                                    fi.array_size = 0;
                                    sb.fields.push_back(fi);
                                }
                            }
                        }
                    }

                    desc.structs.push_back(sb);
                }
            }
        }
    }

    // Parse DOC() statements from entire file content
    auto doc_map = parse_doc_statements(content);

    // Apply documentation to functions
    for (auto& func : desc.functions) {
        std::string key = "FUNC(" + func.function_name + ")";
        if (doc_map.count(key)) {
            func.documentation = doc_map[key];
        }
    }

    // Apply documentation to classes and methods
    for (auto& cls : desc.classes) {
        std::string class_key = "CLASS(" + cls.class_name + ")";
        if (doc_map.count(class_key)) {
            cls.documentation = doc_map[class_key];
        }

        // Apply method documentation
        for (const auto& method : cls.methods) {
            std::string method_key = "METHOD(" + method + ")";
            if (doc_map.count(method_key)) {
                cls.method_docs[method] = doc_map[method_key];
            }
        }
    }

    // Apply documentation to variables
    for (auto& var : desc.variables) {
        std::string key = "VAR(" + var.variable_name + ")";
        if (doc_map.count(key)) {
            var.documentation = doc_map[key];
        }
    }

    // v2.0: Apply documentation to structs
    for (auto& st : desc.structs) {
        std::string key = "STRUCT(" + st.struct_name + ")";
        if (doc_map.count(key)) {
            st.documentation = doc_map[key];
        }
    }

    // v2.3.5: Extract function signatures from C++ source file for IntelliSense
    if (!desc.source_path.empty() && std::filesystem::exists(desc.source_path)) {
        auto cpp_signatures = parse_cpp_function_signatures(desc.source_path);

        // Match extracted signatures with declared functions
        for (auto& func : desc.functions) {
            for (const auto& sig : cpp_signatures) {
                if (sig.function_name == func.function_name) {
                    func.return_type = sig.return_type;
                    func.parameters = sig.parameters;
                    func.is_const = sig.is_const;
                    func.is_static = sig.is_static;
                    func.is_inline = sig.is_inline;
                    func.full_signature = sig.full_signature;
                    break;
                }
            }
        }

        // TODO v2.3.5: Extract class method signatures (future enhancement)
        // This would require more complex parsing to associate methods with classes
        // For now, classes use basic method names without signatures
    }

    // v2.4.1: Validate that source file uses namespace includecpp
    if (!desc.source_path.empty()) {
        validate_namespace_includecpp(desc.source_path, desc.module_name);
    }

    // v3.4.1: Auto-detect header from #include directives in source file
    if (!desc.has_header && !desc.source_path.empty()) {
        std::ifstream source_file(desc.source_path);
        if (source_file.is_open()) {
            std::string line;
            std::regex include_regex(R"re(^\s*#include\s*"([^"]+\.h(?:pp)?)")re");
            std::smatch match;

            while (std::getline(source_file, line)) {
                if (std::regex_search(line, match, include_regex)) {
                    std::string header_name = match[1].str();
                    // Skip standard headers and pybind11 headers
                    if (header_name.find("pybind11") == std::string::npos &&
                        header_name.find("std") == std::string::npos) {
                        // Found a local header - construct the path
                        std::filesystem::path source_path(desc.source_path);
                        std::filesystem::path header_path = source_path.parent_path() / header_name;

                        // Check if the header file exists
                        if (std::filesystem::exists(header_path)) {
                            desc.header_path = header_path.string();
                            desc.has_header = true;
                            std::cout << "NOTE: Auto-detected header for '" << desc.module_name
                                      << "': " << desc.header_path << std::endl;
                            break;
                        }
                        // Also try in include/ subdirectory
                        header_path = source_path.parent_path().parent_path() / "include" / header_name;
                        if (std::filesystem::exists(header_path)) {
                            desc.header_path = header_path.string();
                            desc.has_header = true;
                            std::cout << "NOTE: Auto-detected header for '" << desc.module_name
                                      << "': " << desc.header_path << std::endl;
                            break;
                        }
                    }
                }
            }
        }
    }

    return desc;
}

std::string API::generate_class_bindings(const ClassBinding& cls, const ModuleDescriptor& mod) {
    std::ostringstream code;

    code << "    py::class_<" << cls.class_name << ">("
         << mod.module_name << "_module, \"" << cls.class_name << "\")\n";

    // v2.4.3: Generate all constructor overloads from CONSTRUCTOR() entries
    if (cls.constructors.empty()) {
        // Backward compatibility: default constructor if none specified
        code << "        .def(py::init<>())";
    } else {
        bool first = true;
        for (const auto& ctor : cls.constructors) {
            if (!first) code << "\n";
            first = false;

            code << "        .def(py::init<";
            for (size_t i = 0; i < ctor.param_types.size(); ++i) {
                if (i > 0) code << ", ";
                code << ctor.param_types[i];
            }
            code << ">())";
        }
    }

    // Bind Initialize static method only if there's a default constructor
    bool has_default_ctor = cls.constructors.empty();  // backward compatibility
    if (!has_default_ctor) {
        for (const auto& ctor : cls.constructors) {
            if (ctor.param_types.empty()) {
                has_default_ctor = true;
                break;
            }
        }
    }
    if (has_default_ctor) {
        code << "\n        .def_static(\"Initialize\", []() { return " << cls.class_name << "(); })";
    }

    // v2.4.13: Group methods by name to detect overloads
    std::map<std::string, std::vector<MethodSignature>> method_groups;
    for (const auto& sig : cls.method_signatures) {
        method_groups[sig.name].push_back(sig);
    }

    // v2.4.13: Handle methods with overload detection
    if (!cls.method_signatures.empty()) {
        // Use new signature-based bindings with overload support
        for (const auto& [method_name, signatures] : method_groups) {
            if (signatures.size() == 1 && signatures[0].param_types.empty()) {
                // Single method without explicit signature - use simple binding
                const auto& sig = signatures[0];
                code << "\n        .def(\"" << method_name << "\", &"
                     << cls.class_name << "::" << method_name << ")";
            } else if (signatures.size() == 1) {
                // Single method with explicit signature - still use overload_cast for safety
                const auto& sig = signatures[0];
                code << "\n        .def(\"" << method_name << "\", "
                     << "py::overload_cast<";

                for (size_t i = 0; i < sig.param_types.size(); ++i) {
                    if (i > 0) code << ", ";
                    code << sig.param_types[i];
                }

                code << ">(&" << cls.class_name << "::" << method_name;

                if (sig.is_const) {
                    code << ", py::const_";
                }
                code << "))";
            } else {
                // Multiple overloads - generate py::overload_cast for each
                for (const auto& sig : signatures) {
                    code << "\n        .def(\"" << method_name << "\", "
                         << "py::overload_cast<";

                    for (size_t i = 0; i < sig.param_types.size(); ++i) {
                        if (i > 0) code << ", ";
                        code << sig.param_types[i];
                    }

                    code << ">(&" << cls.class_name << "::" << method_name;

                    if (sig.is_const) {
                        code << ", py::const_";
                    }
                    code << "))";
                }
            }
        }
    } else {
        // Fallback: Legacy method binding (no signature info)
        for (const auto& method : cls.methods) {
            code << "\n        .def(\"" << method << "\", &"
                 << cls.class_name << "::" << method << ")";
        }
    }

    // Bind fields (read-write access)
    for (const auto& field : cls.fields) {
        code << "\n        .def_readwrite(\"" << field
             << "\", &" << cls.class_name << "::" << field << ")";
    }

    // v2.8: Add __repr__ for better debugging output
    code << "\n        .def(\"__repr__\", [](" << cls.class_name << "& self) {\n";
    code << "            return \"<" << cls.class_name << " object>\";\n";
    code << "        })";

    code << ";\n\n";
    return code.str();
}

// v2.0: Generate bindings for STRUCT (Plain-Old-Data types)
std::string generate_struct_bindings(const StructBinding& sb, const ModuleDescriptor& mod) {
    std::ostringstream code;

    if (sb.is_template) {
        // Generate bindings for each template type
        for (const auto& ttype : sb.template_types) {
            std::string struct_full_name = sb.struct_name + "_" + ttype;
            std::string cpp_type = sb.struct_name + "<" + ttype + ">";

            code << "    py::class_<" << cpp_type << ">(";
            code << mod.module_name << "_module, \"" << struct_full_name << "\")\n";

            // v4.1.1: Generate all constructor overloads from CONSTRUCTOR() entries
            if (sb.constructors.empty()) {
                // Backward compatibility: default constructor if none specified
                code << "        .def(py::init<>())\n";
            } else {
                for (const auto& ctor : sb.constructors) {
                    code << "        .def(py::init<";
                    for (size_t i = 0; i < ctor.param_types.size(); ++i) {
                        if (i > 0) code << ", ";
                        // Replace T with actual template type
                        std::string ptype = ctor.param_types[i];
                        if (ptype == "T") ptype = ttype;
                        code << ptype;
                    }
                    code << ">())\n";
                }
            }

            // Fields - readwrite access
            // v4.6.6: Handle array fields with def_property
            for (const auto& fi : sb.fields) {
                std::string actual_type = fi.type;
                // Replace template parameter T with actual type
                if (actual_type == "T") {
                    actual_type = ttype;
                }

                if (fi.is_array) {
                    // Array field: use def_property with lambda getter returning py::bytes
                    code << "        .def_property_readonly(\"" << fi.name << "\", [](" << cpp_type << "& self) {\n";
                    code << "            return py::bytes(reinterpret_cast<const char*>(self." << fi.name << "), " << fi.array_size << ");\n";
                    code << "        })\n";
                } else {
                    code << "        .def_readwrite(\"" << fi.name << "\", &"
                         << cpp_type << "::" << fi.name << ")\n";
                }
            }

            // v4.1.1: Generate method bindings
            for (const auto& sig : sb.method_signatures) {
                if (sig.is_const) {
                    code << "        .def(\"" << sig.name << "\", &" << cpp_type << "::" << sig.name << ")\n";
                } else {
                    code << "        .def(\"" << sig.name << "\", &" << cpp_type << "::" << sig.name << ")\n";
                }
            }

            // Auto-generate to_dict() method
            code << "        .def(\"to_dict\", [](" << cpp_type << "& self) {\n";
            code << "            py::dict d;\n";
            for (const auto& fi : sb.fields) {
                if (!fi.is_array) {
                    code << "            d[\"" << fi.name << "\"] = self." << fi.name << ";\n";
                }
            }
            code << "            return d;\n";
            code << "        })\n";

            // Auto-generate from_dict() static method
            // v4.3.2: Check if all fields have known types (not "auto")
            bool template_all_types_known = true;
            for (const auto& fi : sb.fields) {
                if (fi.is_array) continue;
                std::string actual_type = fi.type;
                if (actual_type == "T") actual_type = ttype;
                if (actual_type == "auto" || actual_type.empty()) {
                    template_all_types_known = false;
                    break;
                }
            }

            if (template_all_types_known && !sb.fields.empty()) {
                code << "        .def_static(\"from_dict\", [](py::dict d) {\n";
                code << "            " << cpp_type << " obj;\n";
                for (const auto& fi : sb.fields) {
                    if (fi.is_array) continue;
                    std::string actual_type = fi.type;
                    if (actual_type == "T") {
                        actual_type = ttype;
                    }

                    code << "            obj." << fi.name << " = d[\"" << fi.name
                         << "\"].cast<" << actual_type << ">();\n";
                }
                code << "            return obj;\n";
                code << "        })\n";
            }

            // v2.8: Add __repr__ for better debugging output
            code << "        .def(\"__repr__\", [](" << cpp_type << "& self) {\n";
            code << "            return \"<" << struct_full_name << " object>\";\n";
            code << "        });\n\n";
        }
    } else {
        // Non-template struct
        code << "    py::class_<" << sb.struct_name << ">(";
        code << mod.module_name << "_module, \"" << sb.struct_name << "\")\n";

        // v4.1.1: Generate all constructor overloads from CONSTRUCTOR() entries
        if (sb.constructors.empty()) {
            // Backward compatibility: default constructor if none specified
            code << "        .def(py::init<>())\n";
        } else {
            for (const auto& ctor : sb.constructors) {
                code << "        .def(py::init<";
                for (size_t i = 0; i < ctor.param_types.size(); ++i) {
                    if (i > 0) code << ", ";
                    code << ctor.param_types[i];
                }
                code << ">())\n";
            }
        }

        // Fields
        // v4.6.6: Handle array fields with def_property
        for (const auto& fi : sb.fields) {
            if (fi.is_array) {
                // Array field: use def_property_readonly with lambda getter returning py::bytes
                code << "        .def_property_readonly(\"" << fi.name << "\", [](" << sb.struct_name << "& self) {\n";
                code << "            return py::bytes(reinterpret_cast<const char*>(self." << fi.name << "), " << fi.array_size << ");\n";
                code << "        })\n";
            } else {
                code << "        .def_readwrite(\"" << fi.name << "\", &"
                     << sb.struct_name << "::" << fi.name << ")\n";
            }
        }

        // v4.1.1: Generate method bindings
        for (const auto& sig : sb.method_signatures) {
            code << "        .def(\"" << sig.name << "\", &" << sb.struct_name << "::" << sig.name << ")\n";
        }

        // Auto-generate to_dict() method
        code << "        .def(\"to_dict\", [](" << sb.struct_name << "& self) {\n";
        code << "            py::dict d;\n";
        for (const auto& fi : sb.fields) {
            if (!fi.is_array) {
                code << "            d[\"" << fi.name << "\"] = self." << fi.name << ";\n";
            }
        }
        code << "            return d;\n";
        code << "        })\n";

        // Auto-generate from_dict() static method
        // v4.3.2: Check if all fields have known types (not "auto")
        bool all_types_known = true;
        for (const auto& fi : sb.fields) {
            if (fi.is_array) continue;
            if (fi.type == "auto" || fi.type.empty()) {
                all_types_known = false;
                break;
            }
        }

        if (all_types_known && !sb.fields.empty()) {
            code << "        .def_static(\"from_dict\", [](py::dict d) {\n";
            code << "            " << sb.struct_name << " obj;\n";
            for (const auto& fi : sb.fields) {
                if (fi.is_array) continue;
                code << "            obj." << fi.name << " = d[\"" << fi.name
                     << "\"].cast<" << fi.type << ">();\n";
            }
            code << "            return obj;\n";
            code << "        })\n";
        }

        // v2.8: Add __repr__ for better debugging output
        code << "        .def(\"__repr__\", [](" << sb.struct_name << "& self) {\n";
        code << "            return \"<" << sb.struct_name << " object>\";\n";
        code << "        });\n\n";
    }

    return code.str();
}

std::string API::generate_pybind11_code(const std::vector<ModuleDescriptor>& modules) {
    std::ostringstream code;

    code << "#include <pybind11/pybind11.h>\n";
    code << "#include <pybind11/stl.h>\n";
    code << "#include <pybind11/stl_bind.h>\n";
    code << "#include <pybind11/operators.h>\n";
    code << "#include <pybind11/functional.h>\n";
    code << "#include <pybind11/complex.h>\n";
    code << "#include <pybind11/chrono.h>\n\n";

    // v3.3.22: Track included headers to prevent duplicates
    std::set<std::string> included_headers;
    std::vector<std::string> ordered_includes;

    // First pass: collect all headers and detect dependencies
    for (const auto& mod : modules) {
        std::string include_path;
        if (mod.has_header) {
            include_path = replace_all(mod.header_path, "\\", "/");
        } else {
            // Fallback: Include source file directly (header-only in .cpp)
            include_path = replace_all(mod.source_path, "\\", "/");
            std::cout << "NOTE: Module '" << mod.module_name
                      << "' has no separate header, including source file: "
                      << include_path << std::endl;
        }

        // Skip if already included
        if (included_headers.find(include_path) != included_headers.end()) {
            std::cout << "NOTE: Skipping duplicate include: " << include_path << std::endl;
            continue;
        }

        included_headers.insert(include_path);
        ordered_includes.push_back(include_path);
    }

    // Generate includes (duplicates already filtered)
    for (const auto& include_path : ordered_includes) {
        code << "#include \"" << include_path << "\"\n";
    }

    code << "\nusing namespace includecpp;\n";
    code << "namespace py = pybind11;\n\n";
    code << "PYBIND11_MODULE(api, m) {\n";
    code << "    m.doc() = \"Auto-generated C++ API bindings\";\n\n";

    for (const auto& mod : modules) {
        code << "    py::module_ " << mod.module_name << "_module = ";
        code << "m.def_submodule(\"" << mod.module_name << "\", \"";
        code << mod.module_name << " module\");\n\n";

        for (const auto& cls : mod.classes) {
            code << generate_class_bindings(cls, mod);
        }

        // v2.0: Generate struct bindings
        for (const auto& st : mod.structs) {
            code << generate_struct_bindings(st, mod);
        }

        // v4.6.5: Generate enum bindings
        for (const auto& en : mod.enums) {
            code << "    py::enum_<" << en.enum_name << ">(";
            code << mod.module_name << "_module, \"" << en.enum_name << "\")\n";

            for (const auto& val : en.values) {
                code << "        .value(\"" << val << "\", " << en.enum_name << "::" << val << ")\n";
            }

            if (en.export_values) {
                code << "        .export_values();\n\n";
            } else {
                code << "        ;\n\n";
            }
        }

        for (const auto& func : mod.functions) {
            if (func.is_template && !func.template_types.empty()) {
                for (const auto& ttype : func.template_types) {
                    code << "    " << mod.module_name << "_module.def(\"";
                    code << func.function_name << "_" << ttype << "\", &"
                         << func.function_name << "<" << ttype << ">);\n";
                }
            } else {
                code << "    " << mod.module_name << "_module.def(\"";
                code << func.function_name << "\", &" << func.function_name << ");\n";
            }
        }

        for (const auto& var : mod.variables) {
            code << "    " << mod.module_name << "_module.attr(\"";
            code << var.variable_name << "\") = " << var.variable_name << ";\n";
        }

        code << "\n";
    }

    code << "}\n";

    return code.str();
}

bool API::write_files(const std::vector<ModuleDescriptor>& modules,
                     const std::string& bindings_path,
                     const std::string& sources_path) {

    std::string bindings_code = generate_pybind11_code(modules);

    // Validate generated code
    if (!validate_bindings_code(bindings_code)) {
        std::cerr << "ERROR: Generated bindings code validation failed!" << std::endl;
        return false;
    }

    std::ofstream bindings_file(bindings_path);
    if (!bindings_file.is_open()) {
        std::cerr << "ERROR: Cannot open file for writing: " << bindings_path << std::endl;
        return false;
    }

    bindings_file << bindings_code;

    if (bindings_file.fail() || bindings_file.bad()) {
        std::cerr << "ERROR: Failed to write to file: " << bindings_path << std::endl;
        bindings_file.close();
        return false;
    }
    bindings_file.close();

    std::ofstream sources_file(sources_path);
    if (!sources_file.is_open()) {
        std::cerr << "ERROR: Cannot open file for writing: " << sources_path << std::endl;
        return false;
    }

    for (const auto& mod : modules) {
        // Only add to sources if module has a separate header
        // If no header, source is already included in bindings.cpp
        if (mod.has_header) {
            std::string source_path = replace_all(mod.source_path, "\\", "/");
            sources_file << source_path << "\n";
        } else {
            std::cout << "NOTE: Skipping '" << mod.source_path
                      << "' from compilation (already included as header)" << std::endl;
        }
    }

    if (sources_file.fail() || sources_file.bad()) {
        std::cerr << "ERROR: Failed to write to file: " << sources_path << std::endl;
        sources_file.close();
        return false;
    }
    sources_file.close();

    return true;
}

std::string API::compute_file_hash(const std::string& filepath) {
    if (!std::filesystem::exists(filepath)) {
        return "0";
    }

    std::ifstream file(filepath, std::ios::binary);
    if (!file.is_open()) {
        return "0";
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();

    std::hash<std::string> hasher;
    size_t hash_value = hasher(content);

    std::ostringstream hash_str;
    hash_str << std::hex << hash_value;
    return hash_str.str();
}

// v2.3.5: Helper function to trim whitespace
static std::string trim_whitespace(const std::string& str) {
    size_t start = str.find_first_not_of(" \t\n\r");
    if (start == std::string::npos) return "";
    size_t end = str.find_last_not_of(" \t\n\r");
    return str.substr(start, end - start + 1);
}

// v2.3.5: Parse parameter list from C++ function signature
std::vector<ParameterInfo> API::parse_parameter_list(const std::string& params_str) {
    std::vector<ParameterInfo> parameters;

    if (params_str.empty() || params_str == "void") {
        return parameters;
    }

    // Split by comma (respecting template brackets)
    std::vector<std::string> param_tokens;
    int bracket_depth = 0;
    int paren_depth = 0;
    std::string current_param;

    for (char c : params_str) {
        if (c == '<') bracket_depth++;
        else if (c == '>') bracket_depth--;
        else if (c == '(') paren_depth++;
        else if (c == ')') paren_depth--;
        else if (c == ',' && bracket_depth == 0 && paren_depth == 0) {
            param_tokens.push_back(trim_whitespace(current_param));
            current_param.clear();
            continue;
        }
        current_param += c;
    }
    if (!current_param.empty()) {
        param_tokens.push_back(trim_whitespace(current_param));
    }

    // Parse each parameter
    for (const auto& param_str : param_tokens) {
        ParameterInfo param;
        std::string clean_param = trim_whitespace(param_str);

        // Check for default value
        size_t eq_pos = clean_param.find('=');
        if (eq_pos != std::string::npos) {
            param.default_value = trim_whitespace(clean_param.substr(eq_pos + 1));
            clean_param = trim_whitespace(clean_param.substr(0, eq_pos));
        }

        // Parse type and name using regex
        // Pattern: [const] type [&|*] name
        std::regex param_regex(R"(^(const\s+)?(.+?)\s*([&*])?\s*([a-zA-Z_]\w*)$)");
        std::smatch param_match;

        if (std::regex_match(clean_param, param_match, param_regex)) {
            if (param_match[1].matched) {
                param.is_const = true;
            }
            param.type = trim_whitespace(param_match[2].str());
            if (param_match[3].matched) {
                std::string ref_or_ptr = param_match[3].str();
                if (ref_or_ptr == "&") param.is_reference = true;
                if (ref_or_ptr == "*") param.is_pointer = true;
            }
            param.name = param_match[4].str();
        } else {
            // Fallback: assume entire thing is type, no name
            param.type = clean_param;
            param.name = "";
        }

        parameters.push_back(param);
    }

    return parameters;
}

// v2.3.5: Parse C++ function signatures from source file
std::vector<FunctionBinding> API::parse_cpp_function_signatures(const std::string& cpp_file_path) {
    std::vector<FunctionBinding> signatures;

    std::ifstream file(cpp_file_path);
    if (!file.is_open()) {
        return signatures;
    }

    std::string content((std::istreambuf_iterator<char>(file)),
                        std::istreambuf_iterator<char>());
    file.close();

    // Regex pattern for function declarations/definitions
    // Matches: [qualifiers] return_type function_name(params) [const]
    std::regex func_regex(
        R"((?:^|\n)\s*(?:(static|inline|virtual|constexpr)\s+)?)"
        R"(([a-zA-Z_][\w:<>]*(?:\s*\*|\s*&)?)\s+)"
        R"(([a-zA-Z_]\w*)\s*\()"
        R"(([^)]*)\))"
        R"(\s*(const)?\s*(?:[{;]|\n))"
    );

    auto search_begin = std::sregex_iterator(content.begin(), content.end(), func_regex);
    auto search_end = std::sregex_iterator();

    for (std::sregex_iterator i = search_begin; i != search_end; ++i) {
        std::smatch match = *i;

        FunctionBinding sig;

        // Extract leading qualifier
        if (match[1].matched) {
            std::string qualifier = match[1].str();
            if (qualifier == "static") sig.is_static = true;
            if (qualifier == "inline") sig.is_inline = true;
        }

        // Extract return type
        sig.return_type = trim_whitespace(match[2].str());

        // Extract function name
        sig.function_name = trim_whitespace(match[3].str());

        // Extract parameters
        std::string params_str = trim_whitespace(match[4].str());
        if (!params_str.empty() && params_str != "void") {
            sig.parameters = parse_parameter_list(params_str);
        }

        // Extract trailing const
        if (match[5].matched) {
            sig.is_const = true;
        }

        // Build full signature string
        sig.full_signature = match[0].str();

        signatures.push_back(sig);
    }

    return signatures;
}

std::string API::generate_registry_json(const std::vector<ModuleDescriptor>& modules, const std::string& plugins_dir) {
    std::ostringstream json;
    json << "{\n";
    json << "  \"schema_version\": \"2.0\",\n";
    json << "  \"modules\": {\n";

    for (size_t i = 0; i < modules.size(); ++i) {
        const auto& mod = modules[i];

        json << "    \"" << mod.module_name << "\": {\n";
        json << "      \"sources\": [";

        std::string source_path = replace_all(mod.source_path, "\\", "/");
        json << "\"" << source_path << "\"";

        // v2.0: Add additional sources
        for (const auto& add_src : mod.additional_sources) {
            std::string add_src_path = replace_all(add_src, "\\", "/");
            json << ", \"" << add_src_path << "\"";
        }

        json << "],\n";

        if (mod.has_header) {
            std::string header_path = replace_all(mod.header_path, "\\", "/");
            json << "      \"header\": \"" << header_path << "\",\n";
        } else {
            json << "      \"header\": null,\n";
        }

        std::filesystem::path cp_path = std::filesystem::path(plugins_dir) / (mod.module_name + ".cp");
        std::string cp_file = cp_path.string();
        cp_file = replace_all(cp_file, "\\", "/");
        json << "      \"cp_file\": \"" << cp_file << "\",\n";

        // v2.0: Add dependencies
        json << "      \"dependencies\": [\n";
        for (size_t j = 0; j < mod.dependencies.size(); ++j) {
            const auto& dep = mod.dependencies[j];
            json << "        {\n";
            json << "          \"target\": \"" << dep.target_module << "\"";
            if (!dep.required_types.empty()) {
                json << ",\n          \"types\": [";
                for (size_t k = 0; k < dep.required_types.size(); ++k) {
                    json << "\"" << dep.required_types[k] << "\"";
                    if (k < dep.required_types.size() - 1) json << ", ";
                }
                json << "]";
            }
            if (dep.is_optional) {
                json << ",\n          \"optional\": true";
            } else {
                json << ",\n          \"optional\": false";
            }
            json << "\n        }";
            if (j < mod.dependencies.size() - 1) json << ",";
            json << "\n";
        }
        json << "      ],\n";

        // v2.3.5: Use source_hashes with full path keys for compatibility
        json << "      \"source_hashes\": {\n";

        // Hash main source with full relative path as key
        json << "        \"" << source_path << "\": \"" << compute_file_hash(mod.source_path) << "\"";

        // Hash additional sources
        for (const auto& add_src : mod.additional_sources) {
            std::string add_src_path = replace_all(add_src, "\\", "/");
            json << ",\n        \"" << add_src_path << "\": \"" << compute_file_hash(add_src) << "\"";
        }

        // Hash header if exists
        if (mod.has_header) {
            std::string header_path = replace_all(mod.header_path, "\\", "/");
            json << ",\n        \"" << header_path << "\": \"" << compute_file_hash(mod.header_path) << "\"";
        }

        // Hash .cp file with special key format (for compatibility with Python code)
        json << ",\n        \"" << mod.module_name << ".cp\": \"" << compute_file_hash(cp_file) << "\"";
        json << "\n      },\n";

        // v2.0: Add structs with fields
        json << "      \"structs\": [\n";
        for (size_t j = 0; j < mod.structs.size(); ++j) {
            const auto& st = mod.structs[j];
            json << "        {\n";
            json << "          \"name\": \"" << st.struct_name << "\"";
            if (!st.documentation.empty()) {
                json << ",\n          \"doc\": \"" << replace_all(st.documentation, "\"", "\\\"") << "\"";
            }
            if (st.is_template) {
                json << ",\n          \"is_template\": true";
                json << ",\n          \"template_types\": [";
                for (size_t k = 0; k < st.template_types.size(); ++k) {
                    json << "\"" << st.template_types[k] << "\"";
                    if (k < st.template_types.size() - 1) json << ", ";
                }
                json << "]";
            } else {
                json << ",\n          \"is_template\": false";
            }
            json << ",\n          \"fields\": [\n";
            for (size_t k = 0; k < st.fields.size(); ++k) {
                const auto& fi = st.fields[k];
                json << "            {\"type\": \"" << fi.type << "\", \"name\": \"" << fi.name << "\"";
                if (fi.is_array) {
                    json << ", \"is_array\": true, \"array_size\": " << fi.array_size;
                }
                json << "}";
                if (k < st.fields.size() - 1) json << ",";
                json << "\n";
            }
            json << "          ]\n";
            json << "        }";
            if (j < mod.structs.size() - 1) json << ",";
            json << "\n";
        }
        json << "      ],\n";

        // Add functions with enhanced signature metadata (v2.3.5)
        json << "      \"functions\": [\n";
        for (size_t j = 0; j < mod.functions.size(); ++j) {
            const auto& func = mod.functions[j];
            json << "        {\n";
            json << "          \"name\": \"" << func.function_name << "\"";

            if (!func.documentation.empty()) {
                json << ",\n          \"doc\": \"" << replace_all(func.documentation, "\"", "\\\"") << "\"";
            }

            // v2.3.5: Add return type
            json << ",\n          \"return_type\": \"" << func.return_type << "\"";

            // v2.3.5: Add parameters with types
            json << ",\n          \"parameters\": [\n";
            for (size_t k = 0; k < func.parameters.size(); ++k) {
                const auto& param = func.parameters[k];
                json << "            {\n";
                json << "              \"name\": \"" << param.name << "\",\n";
                json << "              \"type\": \"" << param.type << "\"";
                if (!param.default_value.empty()) {
                    json << ",\n              \"default\": \"" << replace_all(param.default_value, "\"", "\\\"") << "\"";
                }
                if (param.is_const) json << ",\n              \"const\": true";
                if (param.is_reference) json << ",\n              \"reference\": true";
                if (param.is_pointer) json << ",\n              \"pointer\": true";
                json << "\n            }";
                if (k < func.parameters.size() - 1) json << ",";
                json << "\n";
            }
            json << "          ]";

            // v2.3.5: Add function qualifiers
            if (func.is_static) json << ",\n          \"static\": true";
            if (func.is_const) json << ",\n          \"const\": true";
            if (func.is_inline) json << ",\n          \"inline\": true";

            // v3.1.5: Add template function info
            if (func.is_template) {
                json << ",\n          \"is_template\": true";
                json << ",\n          \"template_types\": [";
                for (size_t k = 0; k < func.template_types.size(); ++k) {
                    json << "\"" << func.template_types[k] << "\"";
                    if (k < func.template_types.size() - 1) json << ", ";
                }
                json << "]";
            }

            json << "\n        }";
            if (j < mod.functions.size() - 1) json << ",";
            json << "\n";
        }
        json << "      ],\n";

        // Add classes with methods, constructors, and documentation
        json << "      \"classes\": [\n";
        for (size_t j = 0; j < mod.classes.size(); ++j) {
            const auto& cls = mod.classes[j];
            json << "        {\n";
            json << "          \"name\": \"" << cls.class_name << "\"";
            if (!cls.documentation.empty()) {
                json << ",\n          \"doc\": \"" << replace_all(cls.documentation, "\"", "\\\"") << "\"";
            }

            // v2.4.3: Add constructor signatures
            json << ",\n          \"constructors\": [\n";
            if (cls.constructors.empty()) {
                // Default constructor
                json << "            {\"params\": []}\n";
            } else {
                for (size_t k = 0; k < cls.constructors.size(); ++k) {
                    const auto& ctor = cls.constructors[k];
                    json << "            {\"params\": [";
                    for (size_t p = 0; p < ctor.param_types.size(); ++p) {
                        json << "\"" << ctor.param_types[p] << "\"";
                        if (p < ctor.param_types.size() - 1) json << ", ";
                    }
                    json << "]}";
                    if (k < cls.constructors.size() - 1) json << ",";
                    json << "\n";
                }
            }
            json << "          ]";

            json << ",\n          \"methods\": [\n";
            if (!cls.method_signatures.empty()) {
                for (size_t k = 0; k < cls.method_signatures.size(); ++k) {
                    const auto& sig = cls.method_signatures[k];
                    json << "            {\n";
                    json << "              \"name\": \"" << sig.name << "\"";
                    if (!sig.documentation.empty()) {
                        json << ",\n              \"doc\": \"" << replace_all(sig.documentation, "\"", "\\\"") << "\"";
                    }
                    json << ",\n              \"return_type\": \"" << sig.return_type << "\"";
                    json << ",\n              \"parameters\": [\n";
                    for (size_t p = 0; p < sig.parameters.size(); ++p) {
                        const auto& param = sig.parameters[p];
                        json << "                {\n";
                        json << "                  \"name\": \"" << param.name << "\",\n";
                        json << "                  \"type\": \"" << param.type << "\"";
                        if (!param.default_value.empty()) {
                            json << ",\n                  \"default\": \"" << replace_all(param.default_value, "\"", "\\\"") << "\"";
                        }
                        if (param.is_const) json << ",\n                  \"const\": true";
                        if (param.is_reference) json << ",\n                  \"reference\": true";
                        if (param.is_pointer) json << ",\n                  \"pointer\": true";
                        json << "\n                }";
                        if (p < sig.parameters.size() - 1) json << ",";
                        json << "\n";
                    }
                    json << "              ]";
                    if (sig.is_const) json << ",\n              \"const\": true";
                    if (sig.is_static) json << ",\n              \"static\": true";
                    json << "\n            }";
                    if (k < cls.method_signatures.size() - 1) json << ",";
                    json << "\n";
                }
            } else {
                for (size_t k = 0; k < cls.methods.size(); ++k) {
                    const auto& method = cls.methods[k];
                    json << "            {\n";
                    json << "              \"name\": \"" << method << "\"";
                    if (cls.method_docs.count(method)) {
                        json << ",\n              \"doc\": \"" << replace_all(cls.method_docs.at(method), "\"", "\\\"") << "\"";
                    }
                    json << "\n            }";
                    if (k < cls.methods.size() - 1) json << ",";
                    json << "\n";
                }
            }
            json << "          ]\n";
            json << "        }";
            if (j < mod.classes.size() - 1) json << ",";
            json << "\n";
        }
        json << "      ],\n";

        auto t = std::time(nullptr);
        std::tm tm_buffer;
#ifdef _WIN32
        localtime_s(&tm_buffer, &t);
#else
        localtime_r(&t, &tm_buffer);
#endif
        std::ostringstream timestamp;
        timestamp << std::put_time(&tm_buffer, "%Y-%m-%dT%H:%M:%S");
        json << "      \"last_built\": \"" << timestamp.str() << "\"\n";

        json << "    }";
        if (i < modules.size() - 1) {
            json << ",";
        }
        json << "\n";
    }

    json << "  }\n";
    json << "}\n";
    return json.str();
}

std::string API::trim(const std::string& str) {
    size_t start = 0;
    while (start < str.length() && std::isspace(static_cast<unsigned char>(str[start]))) start++;

    size_t end = str.length();
    while (end > start && std::isspace(static_cast<unsigned char>(str[end - 1]))) end--;

    return str.substr(start, end - start);
}

std::vector<std::string> API::split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;

    while (std::getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }

    return tokens;
}

std::string API::extract_between(const std::string& str, char open, char close) {
    size_t start = str.find(open);
    size_t end = str.find(close, start);

    if (start == std::string::npos || end == std::string::npos) {
        return "";
    }

    return str.substr(start + 1, end - start - 1);
}

std::string API::safe_extract_between(const std::string& str,
                                      size_t start_pos,
                                      size_t end_pos,
                                      const std::string& context) {
    if (start_pos == std::string::npos || end_pos == std::string::npos) {
        throw std::runtime_error("Parse error: missing parenthesis in " + context);
    }
    if (start_pos >= end_pos) {
        throw std::runtime_error("Parse error: invalid syntax in " + context +
                                " (closing parenthesis before opening)");
    }
    if (end_pos > str.length()) {
        throw std::runtime_error("Parse error: position out of bounds in " + context);
    }
    return trim(str.substr(start_pos + 1, end_pos - start_pos - 1));
}

bool API::starts_with(const std::string& str, const std::string& prefix) {
    return str.size() >= prefix.size() &&
           str.compare(0, prefix.size(), prefix) == 0;
}

std::string API::normalize_path(const std::string& path) {
    std::string p = trim(path);
    std::replace(p.begin(), p.end(), '/', '\\');
    return p;
}

std::string API::replace_all(std::string str, const std::string& from, const std::string& to) {
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
    return str;
}

std::string API::extract_doc_string(const std::string& str) {
    // Extract string from DOC(..., "...") - get the part after comma
    size_t comma = str.find(',');
    if (comma == std::string::npos) return "";

    std::string after_comma = str.substr(comma + 1);
    after_comma = trim(after_comma);

    // Find quoted string
    size_t quote1 = after_comma.find('"');
    if (quote1 == std::string::npos) return "";

    size_t quote2 = after_comma.find('"', quote1 + 1);
    if (quote2 == std::string::npos) return "";

    return after_comma.substr(quote1 + 1, quote2 - quote1 - 1);
}

std::map<std::string, std::string> API::parse_doc_statements(const std::string& content) {
    std::map<std::string, std::string> docs;

    // Find all DOC(...) statements
    size_t pos = 0;
    while ((pos = content.find("DOC(", pos)) != std::string::npos) {
        // Find matching closing parenthesis
        int paren_count = 1;
        size_t i = pos + 4;  // Start after "DOC("
        size_t doc_start = i;

        while (i < content.length() && paren_count > 0) {
            if (content[i] == '(') paren_count++;
            else if (content[i] == ')') paren_count--;
            i++;
        }

        if (paren_count == 0) {
            // Extract full DOC(...) content
            std::string doc_content = content.substr(doc_start, i - doc_start - 1);

            // Find first closing paren to get the key (FUNC(name), CLASS(name), METHOD(name))
            size_t first_close = doc_content.find(')');
            if (first_close != std::string::npos) {
                std::string key = doc_content.substr(0, first_close + 1);
                key = trim(key);

                // Extract doc string
                std::string doc_str = extract_doc_string(doc_content);

                if (!key.empty() && !doc_str.empty()) {
                    docs[key] = doc_str;
                }
            }
        }

        pos = i;
    }

    return docs;
}

// v2.0: TypeRegistry method implementations
void TypeRegistry::register_struct(const std::string& module, const StructBinding& s) {
    structs_[s.struct_name] = s;
    type_to_module_[s.struct_name] = module;
}

void TypeRegistry::register_class(const std::string& module, const ClassBinding& c) {
    classes_[c.class_name] = c;
    type_to_module_[c.class_name] = module;
}

void TypeRegistry::register_dependency(const std::string& from_module, const ModuleDependency& dep) {
    dependencies_[from_module].push_back(dep);
}

TypeMetadata TypeRegistry::resolve_type(const std::string& type_string) const {
    TypeMetadata meta;
    // Basic implementation - can be enhanced with TypeResolver
    meta.full_signature = type_string;
    meta.base_type = type_string;

    if (type_string.find("vector") != std::string::npos || type_string.find("std::vector") != std::string::npos) {
        meta.category = TypeMetadata::VECTOR_TYPE;
    } else if (type_string.find("map") != std::string::npos || type_string.find("std::map") != std::string::npos) {
        meta.category = TypeMetadata::MAP_TYPE;
    } else if (is_struct(type_string)) {
        meta.category = TypeMetadata::STRUCT_TYPE;
    } else if (is_class(type_string)) {
        meta.category = TypeMetadata::CLASS_TYPE;
    } else {
        meta.category = TypeMetadata::PRIMITIVE;
    }

    return meta;
}

bool TypeRegistry::is_struct(const std::string& type_name) const {
    return structs_.count(type_name) > 0;
}

bool TypeRegistry::is_class(const std::string& type_name) const {
    return classes_.count(type_name) > 0;
}

bool TypeRegistry::type_exists(const std::string& type_name) const {
    return type_to_module_.count(type_name) > 0;
}

std::vector<std::string> TypeRegistry::get_dependencies(const std::string& module) const {
    std::vector<std::string> result;
    if (dependencies_.count(module)) {
        for (const auto& dep : dependencies_.at(module)) {
            result.push_back(dep.target_module);
        }
    }
    return result;
}

std::vector<std::string> TypeRegistry::get_dependency_order() const {
    return topological_sort();
}

bool TypeRegistry::has_circular_dependency() const {
    std::set<std::string> visited;
    std::set<std::string> rec_stack;
    std::vector<std::string> path;

    for (const auto& [module, _] : dependencies_) {
        if (has_cycle_dfs(module, visited, rec_stack, path)) {
            return true;
        }
    }

    return false;
}

std::vector<std::string> TypeRegistry::get_circular_path() const {
    std::set<std::string> visited;
    std::set<std::string> rec_stack;
    std::vector<std::string> path;

    for (const auto& [module, _] : dependencies_) {
        if (has_cycle_dfs(module, visited, rec_stack, path)) {
            return path;
        }
    }

    return {};
}

std::string TypeRegistry::get_module_for_type(const std::string& type_name) const {
    if (type_to_module_.count(type_name)) {
        return type_to_module_.at(type_name);
    }
    return "";
}

std::vector<std::string> TypeRegistry::get_all_modules() const {
    std::set<std::string> modules;
    for (const auto& [type, module] : type_to_module_) {
        modules.insert(module);
    }
    return std::vector<std::string>(modules.begin(), modules.end());
}

std::vector<std::string> TypeRegistry::topological_sort() const {
    std::map<std::string, int> in_degree;
    std::set<std::string> all_modules;

    // Get all modules
    for (const auto& [module, _] : dependencies_) {
        all_modules.insert(module);
        in_degree[module] = 0;
    }

    // Calculate in-degrees
    for (const auto& [module, deps] : dependencies_) {
        for (const auto& dep : deps) {
            all_modules.insert(dep.target_module);
            in_degree[dep.target_module]++;
        }
    }

    // Kahn's algorithm
    std::vector<std::string> result;
    std::vector<std::string> queue;

    // Find all nodes with in-degree 0
    for (const auto& module : all_modules) {
        if (in_degree[module] == 0) {
            queue.push_back(module);
        }
    }

    while (!queue.empty()) {
        std::string current = queue.back();
        queue.pop_back();
        result.push_back(current);

        // Reduce in-degree for neighbors
        if (dependencies_.count(current)) {
            for (const auto& dep : dependencies_.at(current)) {
                in_degree[dep.target_module]--;
                if (in_degree[dep.target_module] == 0) {
                    queue.push_back(dep.target_module);
                }
            }
        }
    }

    return result;
}

bool TypeRegistry::has_cycle_dfs(const std::string& module,
                                 std::set<std::string>& visited,
                                 std::set<std::string>& rec_stack,
                                 std::vector<std::string>& path) const {
    visited.insert(module);
    rec_stack.insert(module);
    path.push_back(module);

    if (dependencies_.count(module)) {
        for (const auto& dep : dependencies_.at(module)) {
            if (!visited.count(dep.target_module)) {
                if (has_cycle_dfs(dep.target_module, visited, rec_stack, path)) {
                    return true;
                }
            } else if (rec_stack.count(dep.target_module)) {
                // Found cycle
                path.push_back(dep.target_module);
                return true;
            }
        }
    }

    rec_stack.erase(module);
    path.pop_back();
    return false;
}

// v2.0: TypeMetadata conversion methods implementation
std::string TypeMetadata::to_python_type_hint() const {
    static const std::map<std::string, std::string> type_map = {
        {"int", "int"}, {"long", "int"}, {"short", "int"},
        {"float", "float"}, {"double", "float"},
        {"bool", "bool"},
        {"string", "str"}, {"std::string", "str"},
        {"void", "None"}
    };

    if (type_map.count(base_type)) {
        return type_map.at(base_type);
    }

    if (category == VECTOR_TYPE && !template_args.empty()) {
        return "List[" + template_args[0].to_python_type_hint() + "]";
    }

    if (category == MAP_TYPE && template_args.size() >= 2) {
        return "Dict[" + template_args[0].to_python_type_hint() + ", " +
               template_args[1].to_python_type_hint() + "]";
    }

    // For custom types (struct/class)
    return base_type;
}

std::string TypeMetadata::to_pybind11_type() const {
    std::ostringstream oss;
    if (is_const) oss << "const ";
    oss << base_type;

    if (!template_args.empty()) {
        oss << "<";
        for (size_t i = 0; i < template_args.size(); ++i) {
            if (i > 0) oss << ", ";
            oss << template_args[i].to_pybind11_type();
        }
        oss << ">";
    }

    if (is_pointer) oss << "*";
    if (is_reference) oss << "&";

    return oss.str();
}

std::string TypeMetadata::to_cpp_type() const {
    return to_pybind11_type();  // Same as pybind11 type
}

int main(int argc, char* argv[]) {
    return API::main(argc, argv);
}
