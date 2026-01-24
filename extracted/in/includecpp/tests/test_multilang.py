"""
Test Suite for CSSL Multi-Language Support (v4.1.0)

Tests:
1. libinclude() function
2. Language instance access (lang$InstanceName)
3. supports keyword in functions
4. supports keyword in classes
5. Cross-language inheritance
6. Instance sharing API
7. Syntax highlighting
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from includecpp import CSSL
from includecpp.core.cssl.cssl_languages import (
    get_language, SupportedLanguage, LanguageSupport,
    LANGUAGE_DEFINITIONS
)
from includecpp.core.cssl.cssl_syntax import (
    TokenCategory, highlight_cssl, ColorScheme,
    CSSLSyntaxRules
)
from includecpp.core.cssl.cssl_parser import CSSLParser, CSSLLexer, TokenType

def test_section(name):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print('='*60)

def test_pass(msg):
    print(f"  [PASS] {msg}")

def test_fail(msg, error=None):
    print(f"  [FAIL] {msg}")
    if error:
        print(f"    Error: {error}")
    return False

def run_all_tests():
    passed = 0
    failed = 0

    # =========================================
    # TEST 1: Language Definitions
    # =========================================
    test_section("Language Definitions")

    try:
        # Test all language aliases
        lang_tests = [
            ("python", SupportedLanguage.PYTHON),
            ("py", SupportedLanguage.PYTHON),
            ("c++", SupportedLanguage.CPP),
            ("cpp", SupportedLanguage.CPP),
            ("java", SupportedLanguage.JAVA),
            ("c#", SupportedLanguage.CSHARP),
            ("csharp", SupportedLanguage.CSHARP),
            ("javascript", SupportedLanguage.JAVASCRIPT),
            ("js", SupportedLanguage.JAVASCRIPT),
        ]

        for lang_id, expected_lang in lang_tests:
            lang = get_language(lang_id)
            if lang is None:
                test_fail(f"get_language('{lang_id}') returned None")
                failed += 1
            elif lang.language != expected_lang:
                test_fail(f"get_language('{lang_id}') returned wrong language: {lang.language}")
                failed += 1
            else:
                test_pass(f"get_language('{lang_id}') = {lang.language.value}")
                passed += 1

    except Exception as e:
        test_fail("Language definitions test failed", str(e))
        failed += 1

    # =========================================
    # TEST 2: libinclude() Builtin
    # =========================================
    test_section("libinclude() Builtin Function")

    try:
        # Test loading each language
        result = CSSL.run('''
            cpp = libinclude("c++");
            py = libinclude("python");
            java = libinclude("java");
            csharp = libinclude("c#");
            js = libinclude("javascript");

            // Verify they loaded
            if (cpp != null and py != null and java != null) {
                parameter.return(true);
            } else {
                parameter.return(false);
            }
        ''')

        if result == True:
            test_pass("libinclude() loads all supported languages")
            passed += 1
        else:
            test_fail("libinclude() failed to load languages")
            failed += 1

    except Exception as e:
        test_fail("libinclude() test failed", str(e))
        failed += 1

    # Test invalid language
    try:
        result = CSSL.run('''
            try {
                invalid = libinclude("unknown_language");
                parameter.return(false);
            } catch (e) {
                parameter.return(true);
            }
        ''')

        if result == True:
            test_pass("libinclude() throws error for invalid language")
            passed += 1
        else:
            test_fail("libinclude() should throw for invalid language")
            failed += 1

    except Exception as e:
        # This is expected - invalid language should throw
        test_pass("libinclude() throws error for invalid language")
        passed += 1

    # =========================================
    # TEST 3: Instance Sharing
    # =========================================
    test_section("Instance Sharing API")

    try:
        # Test share() and get_instance()
        py_lang = get_language("python")

        # Share a test instance
        class TestClass:
            def __init__(self):
                self.value = 42

        test_instance = TestClass()
        py_lang.share("TestInstance", test_instance)

        # Get it back
        retrieved = py_lang.get_instance("TestInstance")

        if retrieved is test_instance and retrieved.value == 42:
            test_pass("share() and get_instance() work correctly")
            passed += 1
        else:
            test_fail("share()/get_instance() returned wrong instance")
            failed += 1

        # Test non-existent instance
        none_result = py_lang.get_instance("NonExistent")
        if none_result is None:
            test_pass("get_instance() returns None for non-existent")
            passed += 1
        else:
            test_fail("get_instance() should return None for non-existent")
            failed += 1

    except Exception as e:
        test_fail("Instance sharing test failed", str(e))
        failed += 1

    # =========================================
    # TEST 4: Parser - LANG_INSTANCE_REF Token
    # =========================================
    test_section("Parser - Language Instance Reference Token")

    try:
        # Test various lang$instance patterns
        test_patterns = [
            ("cpp$MyClass", "cpp", "MyClass"),
            ("py$Object", "py", "Object"),
            ("java$Service", "java", "Service"),
            ("javascript$Handler", "javascript", "Handler"),
        ]

        for pattern, expected_lang, expected_instance in test_patterns:
            lexer = CSSLLexer(pattern)
            lexer.tokenize()
            tokens = lexer.tokens

            # Find LANG_INSTANCE_REF token
            found = False
            for token in tokens:
                if token.type == TokenType.LANG_INSTANCE_REF:
                    if (token.value.get('lang') == expected_lang and
                        token.value.get('instance') == expected_instance):
                        found = True
                        break

            if found:
                test_pass(f"Tokenized '{pattern}' correctly")
                passed += 1
            else:
                test_fail(f"Failed to tokenize '{pattern}'")
                failed += 1

    except Exception as e:
        test_fail("Parser token test failed", str(e))
        failed += 1

    # =========================================
    # TEST 5: Parser - supports Keyword
    # =========================================
    test_section("Parser - 'supports' Keyword")

    try:
        # Test function with supports
        # Syntax: define funcName(params) : supports lang { }
        code = '''
        define myFunc() : supports @py {
            printl("test");
        }
        '''

        lexer = CSSLLexer(code)
        lexer.tokenize()
        parser = CSSLParser(lexer.tokens, lexer.source_lines)
        ast = parser.parse_program()  # Use parse_program for standalone code

        # Check if AST contains function with supports_language
        found_supports = False
        for node in ast.children:  # parse_program returns ASTNode with children
            if node.type == 'function':
                if node.value.get('supports_language') == '@py':
                    found_supports = True
                    break

        if found_supports:
            test_pass("Parser recognizes 'supports' in function definition")
            passed += 1
        else:
            test_fail("Parser failed to recognize 'supports' in function")
            failed += 1

    except Exception as e:
        test_fail("Parser supports keyword test failed", str(e))
        failed += 1

    # Test class with supports
    try:
        code = '''
        class MyClass : supports cpp {
            int value;
        }
        '''

        lexer = CSSLLexer(code)
        lexer.tokenize()
        parser = CSSLParser(lexer.tokens, lexer.source_lines)
        ast = parser.parse_program()  # Use parse_program for standalone code

        found_supports = False
        for node in ast.children:  # parse_program returns ASTNode with children
            if node.type == 'class':
                if node.value.get('supports_language') == 'cpp':
                    found_supports = True
                    break

        if found_supports:
            test_pass("Parser recognizes 'supports' in class definition")
            passed += 1
        else:
            test_fail("Parser failed to recognize 'supports' in class")
            failed += 1

    except Exception as e:
        test_fail("Parser supports in class test failed", str(e))
        failed += 1

    # =========================================
    # TEST 6: Syntax Highlighting
    # =========================================
    test_section("Syntax Highlighting")

    try:
        # Test highlighting rules exist
        rules = CSSLSyntaxRules.get_rules()

        # Check for supports keyword rule
        supports_found = False
        libinclude_found = False
        lang_prefix_found = False
        lang_instance_found = False

        for rule in rules:
            if rule.category == TokenCategory.SUPPORTS_KW:
                supports_found = True
            elif rule.category == TokenCategory.LIBINCLUDE_KW:
                libinclude_found = True
            elif rule.category == TokenCategory.LANG_PREFIX:
                lang_prefix_found = True
            elif rule.category == TokenCategory.LANG_INSTANCE:
                lang_instance_found = True

        if supports_found:
            test_pass("SUPPORTS_KW highlighting rule exists")
            passed += 1
        else:
            test_fail("Missing SUPPORTS_KW highlighting rule")
            failed += 1

        if libinclude_found:
            test_pass("LIBINCLUDE_KW highlighting rule exists")
            passed += 1
        else:
            test_fail("Missing LIBINCLUDE_KW highlighting rule")
            failed += 1

        if lang_prefix_found:
            test_pass("LANG_PREFIX highlighting rule exists")
            passed += 1
        else:
            test_fail("Missing LANG_PREFIX highlighting rule")
            failed += 1

        if lang_instance_found:
            test_pass("LANG_INSTANCE highlighting rule exists")
            passed += 1
        else:
            test_fail("Missing LANG_INSTANCE highlighting rule")
            failed += 1

    except Exception as e:
        test_fail("Syntax highlighting test failed", str(e))
        failed += 1

    # Test actual highlighting
    try:
        code = 'cpp = libinclude("c++"); engine = cpp$MyEngine;'
        highlights = highlight_cssl(code, ColorScheme.CSSL_THEME)

        # Check if highlights were generated
        if len(highlights) > 0:
            test_pass(f"Generated {len(highlights)} highlight regions")
            passed += 1
        else:
            test_fail("No highlights generated")
            failed += 1

        # Check for specific categories
        categories = [h[3] for h in highlights]

        if TokenCategory.LIBINCLUDE_KW in categories:
            test_pass("libinclude keyword highlighted")
            passed += 1
        else:
            test_fail("libinclude keyword not highlighted")
            failed += 1

    except Exception as e:
        test_fail("Highlight generation test failed", str(e))
        failed += 1

    # =========================================
    # TEST 7: Color Schemes
    # =========================================
    test_section("Color Schemes")

    try:
        # Check CSSL_THEME has new colors
        theme_categories = [
            TokenCategory.SUPPORTS_KW,
            TokenCategory.LIBINCLUDE_KW,
            TokenCategory.LANG_PREFIX,
            TokenCategory.LANG_INSTANCE,
        ]

        for cat in theme_categories:
            if cat in ColorScheme.CSSL_THEME:
                test_pass(f"CSSL_THEME has {cat.name} color")
                passed += 1
            else:
                test_fail(f"CSSL_THEME missing {cat.name} color")
                failed += 1

            if cat in ColorScheme.LIGHT_THEME:
                test_pass(f"LIGHT_THEME has {cat.name} color")
                passed += 1
            else:
                test_fail(f"LIGHT_THEME missing {cat.name} color")
                failed += 1

    except Exception as e:
        test_fail("Color scheme test failed", str(e))
        failed += 1

    # =========================================
    # TEST 8: Complex Scenario - Full Integration
    # =========================================
    test_section("Complex Integration Scenario")

    try:
        # Complex scenario: Load language, share instance, access it
        result = CSSL.run('''
            // Load language support
            cpp = libinclude("c++");

            // Create a CSSL class
            class Engine {
                int power;

                constr Engine(int p) {
                    this->power = p;
                }

                int getPower() {
                    return this->power;
                }
            }

            // Create instance
            engine = new Engine(500);

            // Share with C++ context
            cpp.share("Engine", engine);

            // Verify the instance was shared
            shared = cpp.get_instance("Engine");

            if (shared != null and shared.power == 500) {
                parameter.return("success");
            } else {
                parameter.return("failed");
            }
        ''')

        if result == "success":
            test_pass("Full integration: class creation + instance sharing")
            passed += 1
        else:
            test_fail(f"Full integration test returned: {result}")
            failed += 1

    except Exception as e:
        test_fail("Full integration test failed", str(e))
        failed += 1

    # =========================================
    # TEST 9: Language Transformer
    # =========================================
    test_section("Language Transformers")

    try:
        from includecpp.core.cssl.cssl_languages import LanguageTransformer

        # Test Python transformer
        py_lang = get_language("python")
        transformer = py_lang.get_transformer()

        if transformer is not None:
            test_pass("Python transformer created successfully")
            passed += 1
        else:
            test_fail("Failed to create Python transformer")
            failed += 1

        # Test JavaScript transformer
        js_lang = get_language("javascript")
        transformer = js_lang.get_transformer()

        if transformer is not None:
            test_pass("JavaScript transformer created successfully")
            passed += 1
        else:
            test_fail("Failed to create JavaScript transformer")
            failed += 1

    except Exception as e:
        test_fail("Language transformer test failed", str(e))
        failed += 1

    # =========================================
    # Summary
    # =========================================
    print(f"\n{'='*60}")
    print(f"  TEST SUMMARY")
    print('='*60)
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total:  {passed + failed}")
    print('='*60)

    if failed == 0:
        print("\n  [SUCCESS] ALL TESTS PASSED!")
    else:
        print(f"\n  [FAILED] {failed} TEST(S) FAILED")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
