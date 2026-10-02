//! Port of `com.dashjoin.jsonata.utils.Signature`.
//!
//! Parses a JSONata function signature string (the part between the angle
//! brackets, e.g. `"<s-nn?:s>"`) into a list of parameter specs, builds a
//! regular expression that the "type signature" of an argument list is matched
//! against, and then `validate(args, context)` validates/coerces the argument
//! list against that signature.
//!
//! This is a faithful 1:1 port of the Java reference implementation. The Java
//! code builds a `java.util.regex.Pattern` from the signature; here we use the
//! `regex` crate. The signature patterns only use character classes and the
//! `?` / `+` quantifiers, so the standard `regex` engine matches Java's
//! semantics for these inputs.

use regex::Regex;

use crate::error::{JError, JResult};
use crate::value::JValue;

/// A single parsed parameter of a signature (Java `Signature.Param`).
#[derive(Debug, Clone)]
struct Param {
    /// The parameter type symbol, e.g. "s", "n", "a", "f", "(sf)".
    /// `None` mirrors a freshly-allocated Java `Param` whose `type` is still
    /// null (relevant to the `<...>` sub-type handling on `_prevParam`).
    type_: Option<String>,
    /// The regex fragment for this parameter, e.g. "[sm]", "[asnblfom]", "f".
    /// `None` mirrors Java's null `regex` before assignment.
    regex: Option<String>,
    /// True if this parameter uses the context value when missing (the `-`
    /// modifier).
    context: bool,
    /// True if this parameter is an array (the `a` type).
    array: bool,
    /// Sub-type string from a `<...>` parameter (array element / function
    /// type), e.g. "n" in `a<n>`.
    subtype: Option<String>,
    // Java also declares `contextRegex`, but it is never assigned or read, so
    // it is omitted here.
}

/// A signature parse error (S0401/S0402), stored *without* a `JValue` payload.
///
/// The parse-error path only ever records an error code + location (see the
/// `JError::at` call sites this replaces — `current`/`expected` were always
/// `None`). Storing just those keeps [`Signature`] free of `JValue`, so it is
/// `Send + Sync` and can live in the process-global builtin-signature table
/// (`evaluator::builtin_signatures`) shared across threads via `Arc`. A full
/// [`JError`] is reconstructed at the point the parser surfaces it.
#[derive(Debug, Clone)]
pub struct SignatureParseError {
    pub code: String,
    pub location: i32,
}

impl Param {
    fn new() -> Param {
        Param {
            type_: None,
            regex: None,
            context: false,
            array: false,
            subtype: None,
        }
    }
}

/// Port of `com.dashjoin.jsonata.utils.Signature`.
#[derive(Debug, Clone)]
pub struct Signature {
    params: Vec<Param>,
    /// The compiled match regex (Java `_regex`). `None` only if compilation
    /// failed; in practice all real JSONata signatures compile.
    regex: Option<Regex>,
    /// The regex source string (Java `_signature`). Kept for parity / debug.
    #[allow(dead_code)]
    signature: String,
    function_name: String,
    /// Parse error (S0401/S0402) recorded instead of panicking; the parser
    /// surfaces it (as a [`JError`]) when compiling a lambda signature.
    pub parse_error: Option<SignatureParseError>,
}

impl Signature {
    /// Java constructor: `Signature(String signature, String function)`.
    pub fn new(signature: &str, function_name: &str) -> Signature {
        let mut sig = Signature {
            params: Vec::new(),
            regex: None,
            signature: String::new(),
            function_name: function_name.to_string(),
            parse_error: None,
        };
        sig.parse_signature(signature);
        sig
    }

    /// Java `setFunctionName`.
    pub fn set_function_name(&mut self, name: &str) {
        self.function_name = name.to_string();
    }

    /// Java `getNumberOfArgs` — total number of parameters.
    pub fn get_number_of_args(&self) -> usize {
        self.params.len()
    }

    /// Whether the first declared parameter is an array type (`a`). Stands in
    /// for Java reflection's "first method parameter is a List" test in
    /// `Functions.call` (the builtin signatures mirror the method shapes).
    pub fn first_param_is_array(&self) -> bool {
        self.params
            .first()
            .is_some_and(|p| p.type_.as_deref() == Some("a"))
    }

    /// Java `getMinNumberOfArgs` — the number of all non-optional arguments,
    /// i.e. params whose regex does not contain `?` (the `-` and `?`
    /// modifiers both append a `?` to the regex).
    pub fn get_min_number_of_args(&self) -> usize {
        let mut res = 0;
        for p in &self.params {
            // Java: `if (!p.regex.contains("?"))`. Java would NPE on a null
            // regex, but by construction every pushed param has a regex.
            let regex = p.regex.as_deref().unwrap_or("");
            if !regex.contains('?') {
                res += 1;
            }
        }
        res
    }

    /// Returns the position of the closing symbol that balances the opening
    /// symbol at position `start` (Java `findClosingBracket`).
    ///
    /// Operates on a `&[char]` so indexing matches Java's `charAt`. Signatures
    /// are ASCII, so char indices and Java UTF-16 indices coincide.
    fn find_closing_bracket(
        str_chars: &[char],
        start: usize,
        open_symbol: char,
        close_symbol: char,
    ) -> usize {
        let mut depth = 1;
        let mut position = start;
        while position < str_chars.len() {
            position += 1;
            let symbol = str_chars[position];
            if symbol == close_symbol {
                depth -= 1;
                if depth == 0 {
                    // we're done
                    break;
                }
            } else if symbol == open_symbol {
                depth += 1;
            }
        }
        position
    }

    /// Java `getSymbol(Object value)` — maps a value to its single-character
    /// type signature symbol.
    fn get_symbol(value: &JValue) -> &'static str {
        // Java: `if (value == null) symbol = "m";`
        // Java `null` == absence of a value == JValue::Undefined here.
        if value.is_undefined() {
            return "m";
        }
        // First check whether this is a function: Java tests
        // `Utils.isFunction(value) || Functions.isLambda(value) ||
        //  (value instanceof Pattern)`. A JValue regex literal corresponds to a
        // `java.util.regex.Pattern` instance.
        if value.is_function() || matches!(value, JValue::Regex(_)) {
            "f"
        } else if value.is_string() {
            "s"
        } else if value.is_number() {
            "n"
        } else if value.is_bool() {
            "b"
        } else if value.is_array() {
            "a"
        } else if value.is_object() {
            "o"
        } else {
            // Java tests `value instanceof NullType` for symbol "l". In
            // jsonata-java a JSON null is the `Jsonata.NULL_VALUE` sentinel
            // (not a `javax.lang.model.type.NullType`), so it does NOT match
            // and falls through to "m". To match Java exactly, JValue::Null
            // (a JSON null) and every other value yield "m" here.
            // PORT-NOTE: the "l" symbol is therefore effectively dead in the
            // reference too; we never produce it, matching Java behavior.
            "m" // m for missing
        }
    }

    /// Java `next()` — push the current param and start a fresh one.
    fn next(params: &mut Vec<Param>, param: &mut Param) {
        params.push(param.clone());
        *param = Param::new();
    }

    /// Parses a function signature definition, building `self.params` and the
    /// match regex (Java `parseSignature`).
    fn parse_signature(&mut self, signature: &str) {
        let chars: Vec<char> = signature.chars().collect();

        // Java tracks three references:
        //   _param      — the current (in-progress) param
        //   _params     — accumulated params (self.params)
        //   _prevParam  — initially aliases _param; after a next() it points at
        //                 the param just pushed (the last element of _params).
        let mut param = Param::new();
        // `prev_is_current == true` models `_prevParam == _param` (before any
        // push). After the first `next()` it becomes false and `_prevParam`
        // refers to `self.params.last()`.
        let mut prev_is_current = true;

        // step through the signature, one symbol at a time
        let mut position = 1usize;
        while position < chars.len() {
            let symbol = chars[position];
            if symbol == ':' {
                // ignore the return type for now
                break;
            }

            match symbol {
                's' | 'n' | 'b' | 'l' | 'o' => {
                    // string / number / boolean / null? / object
                    param.regex = Some(format!("[{}m]", symbol));
                    param.type_ = Some(symbol.to_string());
                    Self::next(&mut self.params, &mut param);
                    prev_is_current = false;
                }
                'a' => {
                    // array — normally treat any value as singleton array
                    param.regex = Some("[asnblfom]".to_string());
                    param.type_ = Some(symbol.to_string());
                    param.array = true;
                    Self::next(&mut self.params, &mut param);
                    prev_is_current = false;
                }
                'f' => {
                    // function
                    param.regex = Some("f".to_string());
                    param.type_ = Some(symbol.to_string());
                    Self::next(&mut self.params, &mut param);
                    prev_is_current = false;
                }
                'j' => {
                    // any JSON type
                    param.regex = Some("[asnblom]".to_string());
                    param.type_ = Some(symbol.to_string());
                    Self::next(&mut self.params, &mut param);
                    prev_is_current = false;
                }
                'x' => {
                    // any type
                    param.regex = Some("[asnblfom]".to_string());
                    param.type_ = Some(symbol.to_string());
                    Self::next(&mut self.params, &mut param);
                    prev_is_current = false;
                }
                '-' => {
                    // use context if param not supplied — operates on _prevParam
                    Self::with_prev(prev_is_current, &mut param, &mut self.params, |p| {
                        p.context = true;
                        // Java: `_prevParam.regex += "?";`
                        let r = p.regex.get_or_insert_with(String::new);
                        r.push('?');
                    });
                }
                '?' | '+' => {
                    // optional param ('?') / one or more ('+') — on _prevParam
                    Self::with_prev(prev_is_current, &mut param, &mut self.params, |p| {
                        let r = p.regex.get_or_insert_with(String::new);
                        r.push(symbol);
                    });
                }
                '(' => {
                    // choice of types — search forward for matching ')'
                    let end_paren = Self::find_closing_bracket(&chars, position, '(', ')');
                    let choice: String = chars[position + 1..end_paren].iter().collect();
                    if !choice.contains('<') {
                        // no parameterized types, simple regex
                        param.regex = Some(format!("[{}m]", choice));
                    } else {
                        // Java: throw new RuntimeException(
                        //   "Choice groups containing parameterized types are not supported");
                        // (error-code table maps this text to S0402)
                        // PORT-NOTE: Java throws a raw RuntimeException (no
                        // code) from the constructor; we record S0402 and let
                        // the parser surface it.
                        self.parse_error = Some(SignatureParseError {
                            code: "S0402".to_string(),
                            location: position as i32,
                        });
                        return;
                    }
                    param.type_ = Some(format!("({})", choice));
                    position = end_paren;
                    Self::next(&mut self.params, &mut param);
                    prev_is_current = false;
                }
                '<' => {
                    // type parameter — can only be applied to 'a' and 'f';
                    // operates on _prevParam.
                    let prev_type = if prev_is_current {
                        param.type_.clone()
                    } else {
                        self.params.last().and_then(|p| p.type_.clone())
                    };
                    match prev_type {
                        Some(t) if t == "a" || t == "f" => {
                            let end_pos = Self::find_closing_bracket(&chars, position, '<', '>');
                            let subtype: String = chars[position + 1..end_pos].iter().collect();
                            if prev_is_current {
                                param.subtype = Some(subtype);
                            } else if let Some(p) = self.params.last_mut() {
                                p.subtype = Some(subtype);
                            }
                            position = end_pos;
                        }
                        _ => {
                            // Java: throw new RuntimeException(
                            //   "Type parameters can only be applied to functions and arrays");
                            // (error-code table maps this text to S0401)
                            // PORT-NOTE: raw RuntimeException in Java; recorded
                            // and surfaced by the parser.
                            self.parse_error = Some(SignatureParseError {
                                code: "S0401".to_string(),
                                location: position as i32,
                            });
                            return;
                        }
                    }
                }
                _ => {
                    // Java's switch has no default; unrecognized symbols are
                    // ignored (fall through to the trailing position++).
                }
            }
            position += 1;
        } // end while processing symbols

        // Build the match regex: "^" + "(" + regex + ")" ... + "$".
        let mut regex_str = String::from("^");
        for p in &self.params {
            regex_str.push('(');
            regex_str.push_str(p.regex.as_deref().unwrap_or(""));
            regex_str.push(')');
        }
        regex_str.push('$');

        self.regex = None;
        match Regex::new(&regex_str) {
            Ok(re) => {
                self.regex = Some(re);
                self.signature = regex_str;
            }
            Err(_e) => {
                // Java: catch PatternSyntaxException -> throw RuntimeException.
                self.parse_error = Some(SignatureParseError {
                    code: "S0401".to_string(),
                    location: -1,
                });
            }
        }
    }

    /// Applies a mutation to `_prevParam`, which is either the current working
    /// `param` (before any push) or the last param in `params`.
    fn with_prev<F: FnOnce(&mut Param)>(
        prev_is_current: bool,
        param: &mut Param,
        params: &mut [Param],
        f: F,
    ) {
        if prev_is_current {
            f(param);
        } else if let Some(p) = params.last_mut() {
            f(p);
        }
    }

    /// Java `throwValidationError(List badArgs, String badSig, String functionName)`.
    /// Always returns an `Err` (Java always throws).
    fn throw_validation_error(&self, bad_sig: &str) -> JError {
        // Apply each component of the regex incrementally until we find the one
        // that fails to match, to locate the offending argument.
        let mut partial_pattern = String::from("^");
        let mut good_to: usize = 0;

        for p in &self.params {
            partial_pattern.push_str(p.regex.as_deref().unwrap_or(""));
            // Java compiles `partialPattern` and calls `match.matches()`, which
            // requires the WHOLE input to match. We append '$' to force a full
            // match (Java's `matches()` is implicitly fully anchored).
            let tester = match Regex::new(&format!("{}$", partial_pattern)) {
                Ok(re) => re,
                Err(_) => {
                    // Java: throw new JException("T0410", -1, (goodTo+1), functionName);
                    return self.t0410(good_to);
                }
            };
            match tester.find(bad_sig) {
                Some(m) if m.start() == 0 => {
                    // matched fully (anchored both ends)
                    good_to = m.end();
                }
                _ => {
                    // failed here
                    // Java: throw new JException("T0410", -1, (goodTo+1), functionName);
                    return self.t0410(good_to);
                }
            }
        }
        // Likely extraneous arguments.
        // Java: throw new JException("T0410", -1, (goodTo+1), functionName);
        self.t0410(good_to)
    }

    /// Build the T0410 error: arg1 = (goodTo+1) index, arg2 = functionName.
    fn t0410(&self, good_to: usize) -> JError {
        JError::with_current_expected(
            "T0410",
            -1,
            JValue::number((good_to + 1) as f64),
            JValue::string(self.function_name.clone()),
        )
    }

    /// Java `validate(Object _args, Object context)`.
    ///
    /// `args` is the supplied argument list. `context` is the current
    /// evaluation context value (`JValue::Undefined` if none). Returns the
    /// (possibly coerced) argument vector, or an `Err` on a type mismatch.
    pub fn validate(&self, args: Vec<JValue>, context: &JValue) -> JResult<Vec<JValue>> {
        // Build the supplied type-signature string.
        let mut supplied_sig = String::new();
        for arg in &args {
            supplied_sig.push_str(Self::get_symbol(arg));
        }

        let regex = match &self.regex {
            Some(re) => re,
            None => {
                // No compiled regex (should not happen for real signatures).
                return Err(self.throw_validation_error(&supplied_sig));
            }
        };

        // `_regex.matcher(suppliedSig).matches()` — a full anchored match. The
        // regex already begins with '^' and ends with '$', so `captures` here
        // is equivalent to Java's `matches()`.
        if let Some(caps) = regex.captures(&supplied_sig) {
            let mut validated_args: Vec<JValue> = Vec::new();
            let mut arg_index: usize = 0;

            for (index, param) in self.params.iter().enumerate() {
                // String match = isValid.group(index + 1);
                // Java returns "" for a zero-width matched group. The `regex`
                // crate returns Some("") for a zero-width match and None for a
                // non-participating optional group; both map to Java's "".
                let match_str: &str = caps.get(index + 1).map(|m| m.as_str()).unwrap_or("");

                if match_str.is_empty() {
                    // if ("".equals(match))
                    if param.context && param.regex.is_some() {
                        // Substitute context value for the missing arg; first
                        // check that the context value is the right type.
                        let context_type = Self::get_symbol(context);
                        // Java: Pattern.matches(param.regex, contextType) —
                        // requires the WHOLE contextType to match the param
                        // regex (which still includes the trailing '?').
                        let param_regex = param.regex.as_deref().unwrap_or("");
                        if Self::full_match(param_regex, context_type) {
                            validated_args.push(context.clone());
                        } else {
                            // context value not compatible with this argument.
                            // Java: throw new JException("T0411", -1, context, argIndex + 1);
                            // arg1 = context (current), arg2 = argIndex+1 (expected).
                            return Err(JError::with_current_expected(
                                "T0411",
                                -1,
                                context.clone(),
                                JValue::number((arg_index + 1) as f64),
                            ));
                        }
                    } else {
                        // validatedArgs.add(arg); argIndex++;
                        let arg = Self::arg_at(&args, arg_index);
                        validated_args.push(arg);
                        arg_index += 1;
                    }
                } else {
                    // May have matched multiple args (regex ends with '+').
                    // Java: match.split("") -> one entry per char (Java 8+).
                    for single in match_str.chars() {
                        if param.type_.as_deref() == Some("a") {
                            let mut arg: JValue;
                            if single == 'm' {
                                // missing (undefined)
                                arg = JValue::Undefined;
                            } else {
                                arg = Self::arg_at(&args, arg_index);
                                let mut array_ok = true;
                                // Is there type info on the array contents?
                                if let Some(subtype) = &param.subtype {
                                    // if (!single.equals("a") && !match.equals(param.subtype))
                                    if single != 'a' && match_str != subtype.as_str() {
                                        array_ok = false;
                                    } else if single == 'a' {
                                        // List argArr = (List)arg; — guaranteed
                                        // an array because its symbol was "a".
                                        if let Some(arg_arr) = arg.as_array() {
                                            if !arg_arr.is_empty() {
                                                let item_type = Self::get_symbol(&arg_arr[0]);
                                                // Java: !itemType.equals(""+param.subtype.charAt(0))
                                                let subtype_first =
                                                    subtype.chars().next().map(|c| c.to_string());
                                                if Some(item_type.to_string()) != subtype_first {
                                                    array_ok = false;
                                                } else {
                                                    // every item must be this type
                                                    for o in arg_arr.iter() {
                                                        if Self::get_symbol(o) != item_type {
                                                            array_ok = false;
                                                            break;
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                if !array_ok {
                                    // Java: throw new JException("T0412", -1, arg, param.subtype);
                                    // arg1 = arg (current), arg2 = subtype (expected).
                                    let subtype_val = param
                                        .subtype
                                        .as_ref()
                                        .map(|s| JValue::string(s.clone()))
                                        .unwrap_or(JValue::Undefined);
                                    return Err(JError::with_current_expected(
                                        "T0412",
                                        -1,
                                        arg.clone(),
                                        subtype_val,
                                    ));
                                }
                                // The function expects an array; if it's not
                                // one, wrap it.
                                if single != 'a' {
                                    arg = JValue::array(vec![arg], Default::default());
                                }
                            }
                            validated_args.push(arg);
                            arg_index += 1;
                        } else {
                            let arg = Self::arg_at(&args, arg_index);
                            // Replicate the Java reference behaviour: built-in
                            // functions declare typed parameters (String /
                            // Number / Boolean) and the reflective call throws
                            // when a JSON `null` (NULL_VALUE) is supplied for
                            // one. The signature regex `[sm]`/`[nm]`/`[bm]`
                            // lets a `null` through as the "m" symbol, so we
                            // reject it here. (Undefined still passes — the
                            // function then yields undefined.)
                            if arg.is_null()
                                && matches!(
                                    param.type_.as_deref(),
                                    Some("s") | Some("n") | Some("b")
                                )
                            {
                                // Java: IllegalArgumentException from m.invoke,
                                // surfaced as a generic error. Use T0410.
                                return Err(JError::with_current_expected(
                                    "T0410",
                                    -1,
                                    JValue::number((arg_index + 1) as f64),
                                    JValue::string(self.function_name.clone()),
                                ));
                            }
                            validated_args.push(arg);
                            arg_index += 1;
                        }
                    }
                }
            }
            return Ok(validated_args);
        }

        Err(self.throw_validation_error(&supplied_sig))
    }

    /// `argIndex < args.size() ? args.get(argIndex) : null` (null == Undefined).
    fn arg_at(args: &[JValue], idx: usize) -> JValue {
        if idx < args.len() {
            args[idx].clone()
        } else {
            JValue::Undefined
        }
    }

    /// Equivalent of Java `Pattern.matches(regex, input)` — true iff the entire
    /// `input` matches `regex`.
    fn full_match(regex: &str, input: &str) -> bool {
        match Regex::new(&format!("^(?:{})$", regex)) {
            Ok(re) => re.is_match(input),
            Err(_) => false,
        }
    }
}

#[cfg(test)]
mod port_tests {
    use super::*;
    use crate::value::{ArrayFlags, JValue};

    fn n(x: f64) -> JValue {
        JValue::number(x)
    }
    fn s(x: &str) -> JValue {
        JValue::string(x)
    }

    #[test]
    fn arity() {
        let sig = Signature::new("<s-nn?:s>", "test");
        assert_eq!(sig.get_number_of_args(), 3);
        // s- => "[sm]?" contains '?', n => "[nm]" no '?', n? => "[nm]?" has '?'
        assert_eq!(sig.get_min_number_of_args(), 1);
    }

    #[test]
    fn context_injection() {
        // <s-:s>: first param uses context if missing.
        let sig = Signature::new("<s-:s>", "test");
        let out = sig.validate(vec![], &s("ctx")).unwrap();
        assert_eq!(out, vec![s("ctx")]);
        // supplied directly
        let out2 = sig.validate(vec![s("hi")], &JValue::Undefined).unwrap();
        assert_eq!(out2, vec![s("hi")]);
    }

    #[test]
    fn context_incompatible_t0411() {
        let sig = Signature::new("<n-:n>", "test");
        let err = sig.validate(vec![], &s("not-a-number")).unwrap_err();
        assert_eq!(err.error, "T0411");
    }

    #[test]
    fn array_singleton_wrap() {
        // <a:a> wraps a non-array singleton into an array
        let sig = Signature::new("<a:a>", "test");
        let out = sig.validate(vec![n(5.0)], &JValue::Undefined).unwrap();
        assert_eq!(out.len(), 1);
        assert!(out[0].is_array());
        assert_eq!(out[0].as_array().unwrap().as_ref(), &vec![n(5.0)]);
        // passing an array stays an array (not double-wrapped)
        let arr = JValue::array(vec![n(1.0), n(2.0)], ArrayFlags::default());
        let out2 = sig.validate(vec![arr.clone()], &JValue::Undefined).unwrap();
        assert!(out2[0].is_array());
        assert_eq!(out2[0].as_array().unwrap().len(), 2);
    }

    #[test]
    fn array_of_type_t0412() {
        // <a<n>:a> requires array elements to be numbers
        let sig = Signature::new("<a<n>:a>", "test");
        let bad = JValue::array(vec![s("x")], ArrayFlags::default());
        let err = sig.validate(vec![bad], &JValue::Undefined).unwrap_err();
        assert_eq!(err.error, "T0412");
        let good = JValue::array(vec![n(1.0), n(2.0)], ArrayFlags::default());
        let ok = sig.validate(vec![good], &JValue::Undefined).unwrap();
        assert!(ok[0].is_array());
    }

    #[test]
    fn mismatch_t0410() {
        let sig = Signature::new("<n:n>", "test");
        let err = sig.validate(vec![s("hi")], &JValue::Undefined).unwrap_err();
        assert_eq!(err.error, "T0410");
        // index arg should be 1 (first arg failed)
        assert_eq!(err.current, Some(n(1.0)));
        assert_eq!(err.expected, Some(s("test")));
    }

    #[test]
    fn variadic_plus() {
        // <s+:s> one-or-more strings
        let sig = Signature::new("<s+:s>", "test");
        let out = sig
            .validate(vec![s("a"), s("b"), s("c")], &JValue::Undefined)
            .unwrap();
        assert_eq!(out, vec![s("a"), s("b"), s("c")]);
    }

    #[test]
    fn choice_group() {
        // <(sn):s> first arg is string or number
        let sig = Signature::new("<(sn):s>", "test");
        assert!(sig.validate(vec![s("a")], &JValue::Undefined).is_ok());
        assert!(sig.validate(vec![n(1.0)], &JValue::Undefined).is_ok());
        assert!(sig
            .validate(vec![JValue::Bool(true)], &JValue::Undefined)
            .is_err());
    }

    #[test]
    fn function_param() {
        // <af>: array, function. Use a native fn value as the function arg.
        let sig = Signature::new("<fa:a>", "test");
        // function then array
        let f = JValue::Regex(std::rc::Rc::new(crate::value::JRegex {
            pattern: "x".into(),
            case_insensitive: false,
            multiline: false,
        }));
        let arr = JValue::array(vec![n(1.0)], ArrayFlags::default());
        let out = sig
            .validate(vec![f.clone(), arr], &JValue::Undefined)
            .unwrap();
        assert_eq!(out.len(), 2);
    }
}
