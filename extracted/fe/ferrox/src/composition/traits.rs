use super::{Composition, quantize_amount};
use std::hash::Hasher;

// === Trait Implementations ===

/// Equality compares actual Species and amounts (with tolerance).
///
/// Two compositions are equal if they have the same Species with the same
/// amounts (using quantized comparison for Eq/Hash consistency).
/// Oxidation states matter: Fe²⁺O ≠ Fe³⁺O.
/// Scaling also matters: Fe2O3 ≠ Fe4O6 (use `reduced_composition()` first if
/// you want to compare reduced forms).
impl PartialEq for Composition {
    fn eq(&self, other: &Self) -> bool {
        // Quick check: same number of species
        if self.species.len() != other.species.len() {
            return false;
        }
        // Compare each species and quantized amount (ensures Eq/Hash consistency)
        for (sp, amt) in &self.species {
            match other.species.get(sp) {
                Some(other_amt) if quantize_amount(*amt) == quantize_amount(*other_amt) => {}
                _ => return false,
            }
        }
        true
    }
}

impl Eq for Composition {}

impl std::hash::Hash for Composition {
    fn hash<H: Hasher>(&self, state: &mut H) {
        // Hash species in a deterministic order (sorted by string representation)
        let mut entries: Vec<_> = self.species.iter().collect();
        entries.sort_by_key(|(sp, _)| sp.to_string());
        for (sp, amt) in entries {
            sp.hash(state);
            // Use same quantization as PartialEq for Eq/Hash contract consistency
            quantize_amount(*amt).hash(state);
        }
    }
}
