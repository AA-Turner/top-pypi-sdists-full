use super::dynamic_string::DynamicString;
use crate::evaluation::evaluator_context::EvaluatorContext;
use lazy_static::lazy_static;

lazy_static! {
    static ref EMPTY_STR: String = String::new();
}

pub(crate) fn get_unit_id<'a>(
    ctx: &'a mut EvaluatorContext,
    id_type: &'a DynamicString,
) -> &'a str {
    ctx.user
        .get_unit_id(id_type)
        .and_then(crate::user::user_value::UserValueRef::string_value)
        .unwrap_or(&EMPTY_STR)
}
