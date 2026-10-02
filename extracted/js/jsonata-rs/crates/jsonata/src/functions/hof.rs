//! Higher-order built-ins (need the evaluator). Ported from
//! `com.dashjoin.jsonata.Functions` (map, filter, single, foldLeft, sift, each,
//! sort) and validated against jsonata-js (`jsonata/src/functions.js`).

use crate::error::{JError, JResult};
use crate::evaluator::Evaluator;
use crate::functions::{arg, boolize, function_arity, hof_func_args, to_boolean};
use crate::value::{ArrayFlags, JValue, Object};

/// `Functions.map` — `$map(arr, func)`.
///
/// Java:
/// ```java
/// public static List map(List arr, Object func) {
///     if (arr == null) return null;
///     List result = Utils.createSequence();
///     for (int i=0; i<arr.size(); i++) {
///         Object arg = arr.get(i);
///         List funcArgs = hofFuncArgs(func, arg, i, arr);
///         Object res = funcApply(func, funcArgs);
///         if (res!=null) result.add(res);
///     }
///     return result;
/// }
/// ```
pub fn map(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let arr = arg(args, 0);
    let func = arg(args, 1);

    // undefined inputs always return undefined
    if arr.is_undefined() {
        return Ok(JValue::Undefined);
    }

    // The `a` signature coerces a single value into [value]; arr is an array here.
    let items = arr.array_clone().unwrap_or_else(|| vec![arr.clone()]);

    let mut result: Vec<JValue> = Vec::new();
    for (i, entry) in items.iter().enumerate() {
        let func_args = hof_func_args(&func, entry.clone(), JValue::Number(i as f64), arr.clone());
        let res = ev.func_apply(&func, func_args)?;
        if !res.is_undefined() {
            result.push(res);
        }
    }
    Ok(JValue::array(result, ArrayFlags::sequence()))
}

/// `Functions.filter` — `$filter(arr, func)`.
///
/// Java:
/// ```java
/// public static List filter(List arr, Object func) {
///     if (arr == null) return null;
///     var result = Utils.createSequence();
///     for (var i = 0; i < arr.size(); i++) {
///         var entry = arr.get(i);
///         var func_args = hofFuncArgs(func, entry, i, arr);
///         var res = funcApply(func, func_args);
///         var booledValue = toBoolean(res);
///         if (booledValue == null ? false : booledValue) result.add(entry);
///     }
///     return result;
/// }
/// ```
pub fn filter(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let arr = arg(args, 0);
    let func = arg(args, 1);

    // undefined inputs always return undefined
    if arr.is_undefined() {
        return Ok(JValue::Undefined);
    }

    let items = arr.array_clone().unwrap_or_else(|| vec![arr.clone()]);

    let mut result: Vec<JValue> = Vec::new();
    for (i, entry) in items.iter().enumerate() {
        let func_args = hof_func_args(&func, entry.clone(), JValue::Number(i as f64), arr.clone());
        let res = ev.func_apply(&func, func_args)?;
        // booledValue == null ? false : booledValue
        if to_boolean(&res).unwrap_or(false) {
            result.push(entry.clone());
        }
    }
    Ok(JValue::array(result, ArrayFlags::sequence()))
}

/// `Functions.single` — `$single(arr, func?)`. Returns the single matching
/// element; D3138 if more than one matches, D3139 if none match.
///
/// Java:
/// ```java
/// public static Object single(List arr, Object func) {
///     if (arr == null) return null;
///     var hasFoundMatch = false;
///     Object result = null;
///     for (var i = 0; i < arr.size(); i++) {
///         var entry = arr.get(i);
///         var positiveResult = true;
///         if (func != null) {
///             var func_args = hofFuncArgs(func, entry, i, arr);
///             var res = funcApply(func, func_args);
///             var booledValue = toBoolean(res);
///             positiveResult = booledValue == null ? false : booledValue;
///         }
///         if (positiveResult) {
///             if(!hasFoundMatch) { result = entry; hasFoundMatch = true; }
///             else throw new JException("D3138", i);
///         }
///     }
///     if(!hasFoundMatch) throw new JException("D3139", -1);
///     return result;
/// }
/// ```
pub fn single(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let arr = arg(args, 0);
    let func = arg(args, 1);

    // undefined inputs always return undefined
    if arr.is_undefined() {
        return Ok(JValue::Undefined);
    }

    let items = arr.array_clone().unwrap_or_else(|| vec![arr.clone()]);

    let has_func = !func.is_undefined();
    let mut has_found_match = false;
    let mut result = JValue::Undefined;

    for (i, entry) in items.iter().enumerate() {
        let positive_result = if has_func {
            let func_args =
                hof_func_args(&func, entry.clone(), JValue::Number(i as f64), arr.clone());
            let res = ev.func_apply(&func, func_args)?;
            to_boolean(&res).unwrap_or(false)
        } else {
            true
        };

        if positive_result {
            if !has_found_match {
                result = entry.clone();
                has_found_match = true;
            } else {
                // Java: throw new JException("D3138", i);
                return Err(JError::at("D3138", i as i32));
            }
        }
    }

    if !has_found_match {
        // Java: throw new JException("D3139", -1);
        return Err(JError::at("D3139", -1));
    }

    Ok(result)
}

/// `Functions.foldLeft` — `$reduce(arr, func, init?)`. D3050 if func arity < 2.
///
/// Java:
/// ```java
/// public static Object foldLeft(List sequence, Object func, Object init) {
///     if (sequence == null) return null;
///     Object result = null;
///     var arity = getFunctionArity(func);
///     if (arity < 2) throw new JException("D3050", 1);
///     int index;
///     if (init == null && sequence.size() > 0) { result = sequence.get(0); index = 1; }
///     else { result = init; index = 0; }
///     while (index < sequence.size()) {
///         List args = new ArrayList<>(); args.add(result); args.add(sequence.get(index));
///         if (arity >= 3) args.add(index);
///         if (arity >= 4) args.add(sequence);
///         result = funcApply(func, args);
///         index++;
///     }
///     return result;
/// }
/// ```
pub fn reduce(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let sequence = arg(args, 0);
    let func = arg(args, 1);
    let init = arg(args, 2);

    // undefined inputs always return undefined
    if sequence.is_undefined() {
        return Ok(JValue::Undefined);
    }

    let arity = function_arity(&func);
    if arity < 2 {
        // Java: throw new JException("D3050", 1);
        return Err(JError::at("D3050", 1));
    }

    let items = sequence
        .array_clone()
        .unwrap_or_else(|| vec![sequence.clone()]);

    let mut result;
    let mut index;
    if init.is_undefined() && !items.is_empty() {
        result = items[0].clone();
        index = 1usize;
    } else {
        result = init;
        index = 0usize;
    }

    while index < items.len() {
        let mut call_args = vec![result, items[index].clone()];
        if arity >= 3 {
            call_args.push(JValue::Number(index as f64));
        }
        if arity >= 4 {
            call_args.push(sequence.clone());
        }
        result = ev.func_apply(&func, call_args)?;
        index += 1;
    }

    Ok(result)
}

/// `Functions.sift` — `$sift(obj, func)`. Filter object entries; func(value, key)
/// truthy keeps the entry. Empty result becomes undefined.
///
/// Java:
/// ```java
/// public static Object sift(Map<Object,Object> arg, Object func) {
///     if (arg==null) return null;
///     var result = new LinkedHashMap<>();
///     for (var item : arg.keySet()) {
///         var entry = arg.get(item);
///         var func_args = hofFuncArgs(func, entry, item, arg);
///         var res = funcApply(func, func_args);
///         if (Jsonata.boolize(res)) result.put(item, entry);
///     }
///     if (result.isEmpty()) result = null;
///     return result;
/// }
/// ```
pub fn sift(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let obj = arg(args, 0);
    let func = arg(args, 1);

    if obj.is_undefined() {
        return Ok(JValue::Undefined);
    }

    // The `o` signature guarantees an object here.
    let entries: Vec<(String, JValue)> = match obj.as_object() {
        Some(o) => o.iter().map(|(k, v)| (k.clone(), v.clone())).collect(),
        None => return Ok(JValue::Undefined),
    };

    let mut result = Object::new();
    for (key, entry) in entries {
        let func_args = hof_func_args(
            &func,
            entry.clone(),
            JValue::string(key.clone()),
            obj.clone(),
        );
        let res = ev.func_apply(&func, func_args)?;
        if boolize(&res) {
            result.insert(key, entry);
        }
    }

    // empty objects should be changed to undefined
    if result.is_empty() {
        return Ok(JValue::Undefined);
    }

    Ok(JValue::object(result))
}

/// `Functions.each` — `$each(obj, func)`. Map func(value, key) over object entries;
/// collect non-undefined results into a sequence.
///
/// Java:
/// ```java
/// public static List each(Map obj, Object func) {
///     if (obj==null) return null;
///     var result = Utils.createSequence();
///     for (var key : obj.keySet()) {
///         var func_args = hofFuncArgs(func, obj.get(key), key, obj);
///         var val = funcApply(func, func_args);
///         if(val != null) result.add(val);
///     }
///     return result;
/// }
/// ```
pub fn each(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let obj = arg(args, 0);
    let func = arg(args, 1);

    if obj.is_undefined() {
        return Ok(JValue::Undefined);
    }

    let entries: Vec<(String, JValue)> = match obj.as_object() {
        Some(o) => o.iter().map(|(k, v)| (k.clone(), v.clone())).collect(),
        None => return Ok(JValue::Undefined),
    };

    let mut result: Vec<JValue> = Vec::new();
    for (key, value) in entries {
        let func_args = hof_func_args(&func, value, JValue::string(key), obj.clone());
        let val = ev.func_apply(&func, func_args)?;
        if !val.is_undefined() {
            result.push(val);
        }
    }

    Ok(JValue::array(result, ArrayFlags::sequence()))
}

/// `Functions.sort` — `$sort(arr, comparator?)`. Stable merge sort.
///
/// With no comparator a default comparator is injected, which only works for an
/// array of all-numbers or all-strings (D3070 otherwise). With a comparator,
/// the comparator returns a boolean "swap" flag (true => `a` should come after
/// `b`).
///
/// Ported from jsonata-js `functions.js` `sort` (the stable recursive merge
/// sort), matching the Java port's `toBoolean`-of-comparator-result semantics
/// (null/false => no swap).
///
/// JS:
/// ```js
/// async function sort(arr, comparator) {
///     if (typeof arr === 'undefined') return undefined;
///     if (arr.length <= 1) return arr;
///     var comp;
///     if (typeof comparator === 'undefined') {
///         if (!isArrayOfNumbers(arr) && !isArrayOfStrings(arr))
///             throw { code: "D3070", index: 1 };
///         comp = async function (a, b) { return a > b; };
///     } else { comp = comparator; }
///     // recursive merge sort using comp(left[0], right[0]) as the swap predicate
/// }
/// ```
pub fn sort(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let arr = arg(args, 0);
    let comparator = arg(args, 1);

    // undefined inputs always return undefined
    if arr.is_undefined() {
        return Ok(JValue::Undefined);
    }

    let items = arr.array_clone().unwrap_or_else(|| vec![arr.clone()]);

    if items.len() <= 1 {
        // Preserve the original value (and its flags) when nothing to sort.
        return Ok(arr);
    }

    // Determine the comparison mode.
    let use_default = comparator.is_undefined();
    if use_default {
        // The default comparator only works for numeric or string arrays.
        let all_numbers = items.iter().all(|v| v.is_number());
        let all_strings = items.iter().all(|v| v.is_string());
        if !all_numbers && !all_strings {
            // Java/JS: throw D3070 with index 1.
            return Err(JError::at("D3070", 1));
        }
    }

    let sorted = if use_default {
        // Natural ordering (stable) — equivalent to Java `result.sort(null)`.
        msort(ev, items, &comparator, true)?
    } else {
        // With a user comparator, Java calls `List.sort(comp)` where `comp`
        // returns 1 (swap), -1 (no swap) or 0 (comparator returned undefined).
        // Java's TimSort uses binary insertion sort for arrays < 32 elements;
        // we replicate that exactly so equal-by-comparator elements land in the
        // same positions as the reference (which differs from a plain stable
        // merge for the inconsistent `a > b` comparator). For larger arrays we
        // fall back to the same binary insertion sort (O(n^2) but faithful).
        binary_insertion_sort(ev, items, &comparator)?
    };

    // Result is a plain array (matches the order-by / $sort observable behavior).
    Ok(JValue::array(sorted, ArrayFlags::default()))
}

/// Recursive stable merge sort mirroring jsonata-js `sort`'s `msort`.
/// Java `TimSort.binarySort` (used by `List.sort` for arrays < 32 elements).
/// `comp(pivot, a[mid]) < 0` ⟺ the comparator returned "no swap" (false),
/// since Java maps swap→1, !swap→-1, null→0 and only `< 0` (i.e. -1) routes
/// left. We reproduce that to match the reference's equal-element ordering.
fn binary_insertion_sort(
    ev: &mut Evaluator,
    mut a: Vec<JValue>,
    comparator: &JValue,
) -> JResult<Vec<JValue>> {
    let n = a.len();
    for start in 1..n {
        let pivot = a[start].clone();
        let mut left = 0usize;
        let mut right = start;
        while left < right {
            let mid = (left + right) / 2;
            // Java TimSort: if (c.compare(pivot, a[mid]) < 0) right = mid;
            // where compare returns 1 (swap), -1 (no swap) or 0 (comparator
            // returned undefined). Only -1 (< 0) routes left.
            if compare_three(ev, &pivot, &a[mid], comparator)? < 0 {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        // shift a[left..start] right by one, insert pivot at `left`
        let mut i = start;
        while i > left {
            a[i] = a[i - 1].clone();
            i -= 1;
        }
        a[left] = pivot;
    }
    Ok(a)
}

fn msort(
    ev: &mut Evaluator,
    array: Vec<JValue>,
    comparator: &JValue,
    use_default: bool,
) -> JResult<Vec<JValue>> {
    if array.len() <= 1 {
        return Ok(array);
    }
    let middle = array.len() / 2;
    let mut iter = array.into_iter();
    let left: Vec<JValue> = iter.by_ref().take(middle).collect();
    let right: Vec<JValue> = iter.collect();
    let left = msort(ev, left, comparator, use_default)?;
    let right = msort(ev, right, comparator, use_default)?;
    merge(ev, left, right, comparator, use_default)
}

/// Stable merge mirroring jsonata-js `sort`'s `merge`/`merge_iter`: take the
/// left head unless the comparator says to swap (i.e. left[0] should come after
/// right[0]), in which case take the right head.
fn merge(
    ev: &mut Evaluator,
    left: Vec<JValue>,
    right: Vec<JValue>,
    comparator: &JValue,
    use_default: bool,
) -> JResult<Vec<JValue>> {
    let mut result: Vec<JValue> = Vec::with_capacity(left.len() + right.len());
    let mut li = 0usize;
    let mut ri = 0usize;

    while li < left.len() && ri < right.len() {
        let swap = compare_swap(ev, &left[li], &right[ri], comparator, use_default)?;
        if swap {
            // comparator returned true -> right head comes first
            result.push(right[ri].clone());
            ri += 1;
        } else {
            // keep the same order -> left head comes first
            result.push(left[li].clone());
            li += 1;
        }
    }
    while li < left.len() {
        result.push(left[li].clone());
        li += 1;
    }
    while ri < right.len() {
        result.push(right[ri].clone());
        ri += 1;
    }
    Ok(result)
}

/// Evaluate the swap predicate for two elements. With the default comparator,
/// `a > b` over an array of all-numbers or all-strings. With a user comparator,
/// `toBoolean(funcApply(comparator, [a, b]))` with null/false meaning no swap.
fn compare_swap(
    ev: &mut Evaluator,
    a: &JValue,
    b: &JValue,
    comparator: &JValue,
    use_default: bool,
) -> JResult<bool> {
    if use_default {
        // a > b over a homogeneous numeric or string array.
        match (a, b) {
            (JValue::Number(x), JValue::Number(y)) => Ok(x > y),
            // Java String.compareTo — UTF-16 code-unit order.
            (JValue::String(x), JValue::String(y)) => {
                Ok(crate::value::java_string_cmp(x, y).is_gt())
            }
            // Should not happen: the array was validated to be all-numbers or
            // all-strings before sorting. Treat as "no swap" for safety.
            _ => Ok(false),
        }
    } else {
        let res = ev.func_apply(comparator, vec![a.clone(), b.clone()])?;
        // Java: toBoolean(res); null -> 0 (no swap), true -> swap.
        Ok(to_boolean(&res).unwrap_or(false))
    }
}

/// Java `Functions.sort` comparator value: `swap?1 : (toBoolean==null ? 0 : -1)`.
/// Used by the binary insertion sort to preserve the reference's ordering of
/// elements the comparator deems equal (when it returns `undefined`).
fn compare_three(ev: &mut Evaluator, a: &JValue, b: &JValue, comparator: &JValue) -> JResult<i32> {
    let res = ev.func_apply(comparator, vec![a.clone(), b.clone()])?;
    Ok(match to_boolean(&res) {
        None => 0,
        Some(true) => 1,
        Some(false) => -1,
    })
}
