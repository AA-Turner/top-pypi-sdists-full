//! Allocation-free iteration over a `CodeUnit`'s root + part dependency edges.
//!
//! Every iterator yields root first, then parts in array order. This order is
//! load-bearing: `graph::set_predecessor_missing` `zip`s the mutable iterator
//! with the `Vec<bool>` built by `RefreshState::resolve_unit_edges`, so both
//! sides must traverse edges in the same sequence.
use crate::generated::types::{CodeUnit, Dependencies, Dependency};

/// Owning location of a dependency edge, used for diagnostics only.
#[derive(Copy, Clone)]
pub(crate) enum Origin<'a> {
    Root,
    /// Part id, or `"<unknown>"` if the part did not set an `id`.
    Part(&'a str),
}

/// Iterate immutably over every `Dependencies` block on a unit (root + parts).
pub(crate) fn dep_blocks(unit: &CodeUnit) -> impl Iterator<Item = &Dependencies> {
    unit.dependencies.iter().chain(
        unit.parts
            .iter()
            .flatten()
            .flat_map(|p| p.dependencies.iter()),
    )
}

/// Iterate mutably over every `Dependencies` block on a unit (root + parts).
pub(crate) fn dep_blocks_mut(unit: &mut CodeUnit) -> impl Iterator<Item = &mut Dependencies> {
    unit.dependencies.iter_mut().chain(
        unit.parts
            .iter_mut()
            .flatten()
            .flat_map(|p| p.dependencies.iter_mut()),
    )
}

/// Iterate every `dependsOn` edge, yielding `(origin, dep)`.
pub(crate) fn depends_on_with_origin(
    unit: &CodeUnit,
) -> impl Iterator<Item = (Origin<'_>, &Dependency)> {
    let root = unit
        .dependencies
        .iter()
        .flat_map(|d| d.depends_on.iter().map(|dep| (Origin::Root, dep)));
    let parts = unit.parts.iter().flatten().flat_map(|p| {
        let origin = Origin::Part(p.id.as_deref().unwrap_or("<unknown>"));
        p.dependencies
            .iter()
            .flat_map(move |d| d.depends_on.iter().map(move |dep| (origin, dep)))
    });
    root.chain(parts)
}

/// Mutable iterator over every `dependsOn` edge. Mirrors the order of
/// [`depends_on_with_origin`] exactly (with origin discarded).
pub(crate) fn depends_on_mut(unit: &mut CodeUnit) -> impl Iterator<Item = &mut Dependency> {
    dep_blocks_mut(unit).flat_map(|d| d.depends_on.iter_mut())
}

/// Every `requiredBy` id (root + parts).
pub(crate) fn required_by(unit: &CodeUnit) -> impl Iterator<Item = &str> {
    dep_blocks(unit).flat_map(|d| d.required_by.iter().map(String::as_str))
}
