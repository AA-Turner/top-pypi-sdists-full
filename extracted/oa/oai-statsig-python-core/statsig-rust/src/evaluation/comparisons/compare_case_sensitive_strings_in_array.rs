use crate::{
    evaluation::evaluator_value::EvaluatorValueRef, specs_response::spec_types::ConditionOperator,
    user::user_value::UserValueRef,
};

// Condition parsing keys these targets by original spelling. Keep this path
// separate from comparisons whose targets use normalized keys.
pub(crate) fn compare_case_sensitive_strings_in_array<'a>(
    value: UserValueRef<'_>,
    target_value: impl Into<EvaluatorValueRef<'a>>,
    op: ConditionOperator,
) -> bool {
    let target_value = target_value.into();
    let original = value.string_value().unwrap_or_default();
    let cached_original = value.original_lookup_key();

    // Scanning small targets avoids lookup overhead and temporary owned keys
    // for numeric/bool inputs that do not cache an InternedString.
    let contains = match target_value.array_len() {
        None => false,
        Some(len) if len <= 4 || (cached_original.is_none() && len <= 64) => {
            target_value.any_array_string(false, |candidate| original == candidate)
        }
        Some(_) => target_value.array_contains_exact_string(original, cached_original),
    };

    if matches!(op, ConditionOperator::NoneCaseSensitive) {
        !contains
    } else {
        contains
    }
}
