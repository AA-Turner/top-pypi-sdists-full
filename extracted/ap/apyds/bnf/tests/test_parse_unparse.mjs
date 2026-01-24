import { parse, unparse } from "../atsds_bnf/index.mjs";

test("parse_simple_rule", () => {
    // Test parsing a simple rule with premises and conclusion
    const dsp_input = "a, b => c";
    const ds_output = parse(dsp_input);
    const expected = "a\nb\n----\nc\n";
    expect(ds_output).toBe(expected);
});

test("parse_no_premises", () => {
    // Test parsing a rule with no premises (axiom)
    const dsp_input = "a";
    const ds_output = parse(dsp_input);
    const expected = "----\na\n";
    expect(ds_output).toBe(expected);
});

test("parse_function", () => {
    // Test parsing a function call
    const dsp_input = "f(a, b) => c";
    const ds_output = parse(dsp_input);
    const expected = "(function f a b)\n----------------\nc\n";
    expect(ds_output).toBe(expected);
});

test("parse_subscript", () => {
    // Test parsing subscript notation
    const dsp_input = "a[i, j] => b";
    const ds_output = parse(dsp_input);
    const expected = "(subscript a i j)\n-----------------\nb\n";
    expect(ds_output).toBe(expected);
});

test("parse_binary_operator", () => {
    // Test parsing binary operators
    const dsp_input = "(a + b) => c";
    const ds_output = parse(dsp_input);
    const expected = "(binary + a b)\n--------------\nc\n";
    expect(ds_output).toBe(expected);
});

test("parse_unary_operator", () => {
    // Test parsing unary operators
    const dsp_input = "~ a => b";
    const ds_output = parse(dsp_input);
    const expected = "(unary ~ a)\n-----------\nb\n";
    expect(ds_output).toBe(expected);
});

test("parse_multiple_rules", () => {
    // Test parsing multiple rules
    const dsp_input = "a => b\nc => d";
    const ds_output = parse(dsp_input);
    const expected = "a\n----\nb\n\n\nc\n----\nd\n";
    expect(ds_output).toBe(expected);
});

test("parse_complex_expression", () => {
    // Test parsing complex nested expressions
    const dsp_input = "(a + b) * c, d[i] => f(g, h)";
    const ds_output = parse(dsp_input);
    const expected = "(binary * (binary + a b) c)\n(subscript d i)\n---------------------------\n(function f g h)\n";
    expect(ds_output).toBe(expected);
});

test("unparse_simple_rule", () => {
    // Test unparsing a simple rule
    const ds_input = "a\nb\n----\nc\n";
    const dsp_output = unparse(ds_input);
    const expected = "a, b => c";
    expect(dsp_output).toBe(expected);
});

test("unparse_no_premises", () => {
    // Test unparsing a rule with no premises
    const ds_input = "----\na\n";
    const dsp_output = unparse(ds_input);
    const expected = " => a";
    expect(dsp_output).toBe(expected);
});

test("unparse_function", () => {
    // Test unparsing a function
    const ds_input = "(function f a b)\n----\nc\n";
    const dsp_output = unparse(ds_input);
    const expected = "f(a, b) => c";
    expect(dsp_output).toBe(expected);
});

test("unparse_subscript", () => {
    // Test unparsing subscript notation
    const ds_input = "(subscript a i j)\n----\nb\n";
    const dsp_output = unparse(ds_input);
    const expected = "a[i, j] => b";
    expect(dsp_output).toBe(expected);
});

test("unparse_binary_operator", () => {
    // Test unparsing binary operators
    const ds_input = "(binary + a b)\n----\nc\n";
    const dsp_output = unparse(ds_input);
    const expected = "(a + b) => c";
    expect(dsp_output).toBe(expected);
});

test("unparse_unary_operator", () => {
    // Test unparsing unary operators
    const ds_input = "(unary ~ a)\n----\nb\n";
    const dsp_output = unparse(ds_input);
    const expected = "(~ a) => b";
    expect(dsp_output).toBe(expected);
});

test("unparse_multiple_rules", () => {
    // Test unparsing multiple rules
    const ds_input = "a\n----\nb\n\n\nc\n----\nd\n";
    const dsp_output = unparse(ds_input);
    const expected = "a => b\nc => d";
    expect(dsp_output).toBe(expected);
});

test("unparse_complex_expression", () => {
    // Test unparsing complex nested expressions
    const ds_input = "(binary * (binary + a b) c)\n(subscript d i)\n----\n(function f g h)\n";
    const dsp_output = unparse(ds_input);
    const expected = "((a + b) * c), d[i] => f(g, h)";
    expect(dsp_output).toBe(expected);
});

test("roundtrip_parse_unparse", () => {
    // Test that parse followed by unparse produces consistent results
    const dsp_original = "a, b => c";
    const ds_intermediate = parse(dsp_original);
    const dsp_result = unparse(ds_intermediate);
    expect(dsp_result).toBe(dsp_original);
});

test("roundtrip_unparse_parse", () => {
    // Test that unparse followed by parse produces consistent results
    const ds_original = "a\nb\n----\nc\n";
    const dsp_intermediate = unparse(ds_original);
    const ds_result = parse(dsp_intermediate);
    expect(ds_result).toBe(ds_original);
});

test("parse_error_missing_closing_parenthesis", () => {
    // Test that parse throws error on missing closing parenthesis
    const dsp_input = "(a + b => c";
    expect(() => parse(dsp_input)).toThrow(/line 1:7 no viable alternative/);
});

test("parse_error_bad_syntax", () => {
    // Test that parse throws error on bad syntax
    const dsp_input = "a b c => => d";
    expect(() => parse(dsp_input)).toThrow(/line 1:2 mismatched input/);
});

test("parse_error_malformed_parentheses", () => {
    // Test that parse throws error on malformed parentheses
    const dsp_input = "()()()";
    expect(() => parse(dsp_input)).toThrow(/line 1:1 no viable alternative/);
});

test("unparse_error_incomplete_binary", () => {
    // Test that unparse throws error on incomplete binary expression
    const ds_input = "(binary";
    expect(() => unparse(ds_input)).toThrow(/line 1:7 mismatched input/);
});

test("unparse_error_malformed_function", () => {
    // Test that unparse throws error on malformed function
    const ds_input = "(function";
    expect(() => unparse(ds_input)).toThrow(/line 1:9 mismatched input/);
});
