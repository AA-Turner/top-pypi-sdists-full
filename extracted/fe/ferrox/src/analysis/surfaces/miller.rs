// === Miller Index ===

use serde::{Deserialize, Serialize};
use std::collections::HashSet;

/// A Miller index (h, k, l) representing a crystallographic plane.
///
/// Miller indices specify the orientation of a plane in a crystal lattice.
/// Common low-index planes include (100), (110), (111), etc.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct MillerIndex {
    /// h component of the Miller index
    pub h: i32,
    /// k component of the Miller index
    pub k: i32,
    /// l component of the Miller index
    pub l: i32,
}

impl MillerIndex {
    /// Create a new Miller index.
    pub fn new(h: i32, k: i32, l: i32) -> Self {
        Self { h, k, l }
    }

    /// Create a Miller index from an array.
    pub fn from_array(hkl: [i32; 3]) -> Self {
        Self {
            h: hkl[0],
            k: hkl[1],
            l: hkl[2],
        }
    }

    /// Convert to array format.
    pub fn to_array(&self) -> [i32; 3] {
        [self.h, self.k, self.l]
    }

    /// Compute the GCD of two integers.
    fn gcd(a: i32, b: i32) -> i32 {
        if b == 0 { a.abs() } else { Self::gcd(b, a % b) }
    }

    /// Reduce the Miller index to its smallest coprime representation.
    ///
    /// For example, (2, 4, 6) becomes (1, 2, 3).
    pub fn reduced(&self) -> Self {
        let gcd = Self::gcd(Self::gcd(self.h, self.k), self.l);
        if gcd == 0 {
            *self
        } else {
            Self {
                h: self.h / gcd,
                k: self.k / gcd,
                l: self.l / gcd,
            }
        }
    }

    /// Check if this is a zero index (0, 0, 0).
    pub fn is_zero(&self) -> bool {
        self.h == 0 && self.k == 0 && self.l == 0
    }

    /// Get the sum of absolute values of indices.
    pub fn norm_l1(&self) -> i32 {
        self.h.abs() + self.k.abs() + self.l.abs()
    }
}

impl std::fmt::Display for MillerIndex {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(fmt, "({}, {}, {})", self.h, self.k, self.l)
    }
}

impl From<[i32; 3]> for MillerIndex {
    fn from(hkl: [i32; 3]) -> Self {
        Self::from_array(hkl)
    }
}

impl From<MillerIndex> for [i32; 3] {
    fn from(miller: MillerIndex) -> Self {
        miller.to_array()
    }
}

/// Enumerate all unique Miller indices up to a maximum index value.
///
/// This generates all unique low-index Miller planes with |h|, |k|, |l| <= max_index.
/// Each plane is returned in reduced form (coprime indices) and only once
/// per symmetry-equivalent family (avoiding both (1,0,0) and (-1,0,0)).
///
/// # Arguments
///
/// * `max_index` - Maximum absolute value for any index component
///
/// # Returns
///
/// A vector of unique Miller indices, excluding (0, 0, 0).
pub fn enumerate_miller_indices(max_index: i32) -> Vec<MillerIndex> {
    let mut indices = HashSet::new();

    for h in -max_index..=max_index {
        for k in -max_index..=max_index {
            for l in -max_index..=max_index {
                if h == 0 && k == 0 && l == 0 {
                    continue;
                }
                let miller = MillerIndex::new(h, k, l).reduced();
                // Normalize sign: first non-zero component should be positive
                let normalized = normalize_miller_sign(miller);
                indices.insert(normalized);
            }
        }
    }

    let mut result: Vec<MillerIndex> = indices.into_iter().collect();
    // Sort by L1 norm (sum of absolute values) then lexicographically
    result.sort_by(|a, b| {
        a.norm_l1()
            .cmp(&b.norm_l1())
            .then(a.h.cmp(&b.h))
            .then(a.k.cmp(&b.k))
            .then(a.l.cmp(&b.l))
    });
    result
}

/// Normalize Miller index sign so first non-zero component is positive.
fn normalize_miller_sign(miller: MillerIndex) -> MillerIndex {
    let first_nonzero = if miller.h != 0 {
        miller.h
    } else if miller.k != 0 {
        miller.k
    } else {
        miller.l
    };

    if first_nonzero < 0 {
        MillerIndex::new(-miller.h, -miller.k, -miller.l)
    } else {
        miller
    }
}
