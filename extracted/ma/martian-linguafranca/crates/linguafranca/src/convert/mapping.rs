use crate::convert::ctx::ConversionCtx;

/// Conversion helper for mappings that may be lossy and need path-aware warnings.
pub(crate) trait LossyTryFromWithCtx<S, C = ()>: Sized {
    fn lossy_try_from(value: S, ctx: &mut ConversionCtx<C>, field: &str) -> Option<Self>;
}

/// Map a vector while preserving warning paths like `base[3]`.
pub(crate) fn map_vec_with_ctx_path<T, U, C, F>(
    ctx: &mut ConversionCtx<C>,
    base: &str,
    values: Vec<T>,
    mut map: F,
) -> Vec<U>
where
    F: FnMut(T, &mut ConversionCtx<C>) -> Option<U>,
{
    values
        .into_iter()
        .enumerate()
        .filter_map(|(i, value)| {
            ctx.push(format!("{base}[{i}]"));
            let mapped = map(value, ctx);
            ctx.pop();
            mapped
        })
        .collect()
}

/// Map a vector while preserving warning paths and return `None` when empty.
pub(crate) fn map_non_empty_vec_with_ctx_path<T, U, C, F>(
    ctx: &mut ConversionCtx<C>,
    base: &str,
    values: Vec<T>,
    map: F,
) -> Option<Vec<U>>
where
    F: FnMut(T, &mut ConversionCtx<C>) -> Option<U>,
{
    let mapped = map_vec_with_ctx_path(ctx, base, values, map);
    (!mapped.is_empty()).then_some(mapped)
}
