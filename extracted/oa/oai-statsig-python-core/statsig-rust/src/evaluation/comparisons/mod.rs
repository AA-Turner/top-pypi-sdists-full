pub(crate) use compare_arrays::compare_arrays;
pub(crate) use compare_case_sensitive_strings_in_array::compare_case_sensitive_strings_in_array;
pub(crate) use compare_numbers::compare_numbers;
pub(crate) use compare_str_with_regex::compare_str_with_regex;
pub(crate) use compare_strings_in_array::compare_strings_in_array;
pub(crate) use compare_time::compare_time;
pub(crate) use compare_versions::compare_versions;
mod compare_arrays;
mod compare_case_sensitive_strings_in_array;
mod compare_numbers;
mod compare_str_with_regex;
mod compare_strings_in_array;
mod compare_time;
mod compare_versions;

#[cfg(test)]
#[path = "../../../benches/evaluation/case_sensitive_target_bench.rs"]
mod case_sensitive_target_bench;
