use super::super::Element;
use std::collections::HashMap;
use std::sync::OnceLock;

impl Element {
    /// All element symbols in atomic number order.
    pub(crate) const SYMBOLS: [&'static str; 118] = [
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S",
        "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga",
        "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd",
        "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm",
        "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os",
        "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa",
        "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg",
        "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
    ];

    /// Standard atomic weights in atomic mass units (u).
    /// Source: IUPAC 2021 values. Index 0 corresponds to H (Z=1).
    /// For radioactive elements without stable isotopes, the most stable isotope mass is used.
    pub(crate) const ATOMIC_MASSES: [f64; 118] = [
        1.008,         // H
        4.0026022,     // He
        6.94,          // Li
        9.01218315,    // Be
        10.81,         // B
        12.011,        // C
        14.007,        // N
        15.999,        // O
        18.9984031636, // F
        20.17976,      // Ne
        22.989769282,  // Na
        24.305,        // Mg
        26.98153857,   // Al
        28.085,        // Si
        30.9737619985, // P
        32.06,         // S
        35.45,         // Cl
        39.9481,       // Ar
        39.09831,      // K
        40.0784,       // Ca
        44.9559085,    // Sc
        47.8671,       // Ti
        50.94151,      // V
        51.99616,      // Cr
        54.9380443,    // Mn
        55.8452,       // Fe
        58.9331944,    // Co
        58.69344,      // Ni
        63.5463,       // Cu
        65.382,        // Zn
        69.7231,       // Ga
        72.6308,       // Ge
        74.9215956,    // As
        78.9718,       // Se
        79.904,        // Br
        83.7982,       // Kr
        85.46783,      // Rb
        87.621,        // Sr
        88.905842,     // Y
        91.2242,       // Zr
        92.906372,     // Nb
        95.951,        // Mo
        98.0,          // Tc (radioactive)
        101.072,       // Ru
        102.905502,    // Rh
        106.421,       // Pd
        107.86822,     // Ag
        112.4144,      // Cd
        114.8181,      // In
        118.7107,      // Sn
        121.7601,      // Sb
        127.603,       // Te
        126.904473,    // I
        131.2936,      // Xe
        132.905451966, // Cs
        137.3277,      // Ba
        138.905477,    // La
        140.1161,      // Ce
        140.907662,    // Pr
        144.2423,      // Nd
        145.0,         // Pm (radioactive)
        150.362,       // Sm
        151.9641,      // Eu
        157.253,       // Gd
        158.925352,    // Tb
        162.5001,      // Dy
        164.930332,    // Ho
        167.2593,      // Er
        168.934222,    // Tm
        173.0451,      // Yb
        174.96681,     // Lu
        178.492,       // Hf
        180.947882,    // Ta
        183.841,       // W
        186.2071,      // Re
        190.233,       // Os
        192.2173,      // Ir
        195.0849,      // Pt
        196.9665695,   // Au
        200.5923,      // Hg
        204.38,        // Tl
        207.21,        // Pb
        208.980401,    // Bi
        209.0,         // Po (radioactive)
        210.0,         // At (radioactive)
        222.0,         // Rn (radioactive)
        223.0,         // Fr (radioactive)
        226.0,         // Ra (radioactive)
        227.0,         // Ac (radioactive)
        232.03774,     // Th
        231.035882,    // Pa
        238.028913,    // U
        237.0,         // Np (radioactive)
        244.0,         // Pu (radioactive)
        243.0,         // Am (radioactive)
        247.0,         // Cm (radioactive)
        247.0,         // Bk (radioactive)
        251.0,         // Cf (radioactive)
        252.0,         // Es (radioactive)
        257.0,         // Fm (radioactive)
        258.0,         // Md (radioactive)
        259.0,         // No (radioactive)
        266.0,         // Lr (radioactive)
        267.0,         // Rf (radioactive)
        268.0,         // Db (radioactive)
        269.0,         // Sg (radioactive)
        270.0,         // Bh (radioactive)
        277.0,         // Hs (radioactive)
        278.0,         // Mt (radioactive)
        281.0,         // Ds (radioactive)
        282.0,         // Rg (radioactive)
        285.0,         // Cn (radioactive)
        286.0,         // Nh (radioactive)
        289.0,         // Fl (radioactive)
        289.0,         // Mc (radioactive)
        293.0,         // Lv (radioactive)
        294.0,         // Ts (radioactive)
        294.0,         // Og (radioactive)
    ];

    /// Pauling electronegativities (NaN for elements without defined values).
    /// Index 0 corresponds to H (Z=1).
    pub(crate) const ELECTRONEGATIVITIES: [f64; 118] = [
        2.20,
        f64::NAN,
        0.98,
        1.57,
        2.04,
        2.55,
        3.04,
        3.44,
        3.98,
        f64::NAN, // H-Ne
        0.93,
        1.31,
        1.61,
        1.90,
        2.19,
        2.58,
        3.16,
        f64::NAN,
        0.82,
        1.00, // Na-Ca
        1.36,
        1.54,
        1.63,
        1.66,
        1.55,
        1.83,
        1.88,
        1.91,
        1.90,
        1.65, // Sc-Zn
        1.81,
        2.01,
        2.18,
        2.55,
        2.96,
        3.00,
        0.82,
        0.95,
        1.22,
        1.33, // Ga-Zr
        1.60,
        2.16,
        1.90,
        2.20,
        2.28,
        2.20,
        1.93,
        1.69,
        1.78,
        1.96, // Nb-Sn
        2.05,
        2.10,
        2.66,
        2.60,
        0.79,
        0.89,
        1.10,
        1.12,
        1.13,
        1.14, // Sb-Nd
        f64::NAN,
        1.17,
        f64::NAN,
        1.20,
        f64::NAN,
        1.22,
        1.23,
        1.24,
        1.25,
        f64::NAN, // Pm-Yb
        1.27,
        1.30,
        1.50,
        2.36,
        1.90,
        2.20,
        2.20,
        2.28,
        2.54,
        2.00, // Lu-Hg
        1.62,
        2.33,
        2.02,
        2.00,
        2.20,
        f64::NAN,
        0.70,
        0.90,
        1.10,
        1.30, // Tl-Th
        1.50,
        1.38,
        1.36,
        1.28,
        1.30,
        1.30,
        1.30,
        1.30,
        1.30,
        1.30, // Pa-Fm
        1.30,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN, // Md-Hs
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN, // Mt-Lv
        f64::NAN,
        f64::NAN, // Ts-Og
    ];

    /// Create an element from its symbol string.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert_eq!(Element::from_symbol("Fe"), Some(Element::Fe));
    /// assert_eq!(Element::from_symbol("fe"), Some(Element::Fe));  // Case insensitive
    /// assert_eq!(Element::from_symbol("D"), Some(Element::D));    // Deuterium
    /// assert_eq!(Element::from_symbol("X"), Some(Element::Dummy)); // Dummy atom
    /// ```
    pub fn from_symbol(symbol: &str) -> Option<Self> {
        let lower = symbol.to_lowercase();

        // Check pseudo-elements first (before the static map)
        match lower.as_str() {
            "d" => return Some(Self::D),
            "t" => return Some(Self::T),
            "x" | "xx" | "dummy" | "vac" | "va" => return Some(Self::Dummy),
            _ => {}
        }

        // Static lookup map initialized once (case-insensitive via lowercase keys)
        static SYMBOL_MAP: OnceLock<HashMap<String, Element>> = OnceLock::new();
        let map = SYMBOL_MAP.get_or_init(|| {
            let mut map = HashMap::with_capacity(118);
            for (idx, sym) in Self::SYMBOLS.iter().enumerate() {
                if let Some(elem) = Self::from_atomic_number((idx + 1) as u8) {
                    map.insert(sym.to_lowercase(), elem);
                }
            }
            map
        });
        map.get(&lower).copied()
    }

    /// Create an element from its atomic number (1-118 for real elements, 119-121 for pseudo-elements).
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert_eq!(Element::from_atomic_number(26), Some(Element::Fe));
    /// assert_eq!(Element::from_atomic_number(0), None);
    /// assert_eq!(Element::from_atomic_number(119), Some(Element::Dummy));
    /// assert_eq!(Element::from_atomic_number(120), Some(Element::D));
    /// assert_eq!(Element::from_atomic_number(121), Some(Element::T));
    /// assert_eq!(Element::from_atomic_number(122), None);
    /// ```
    pub fn from_atomic_number(z: u8) -> Option<Self> {
        // Compile-time checks for discriminant values
        const _: () = assert!(Element::Og as u8 == 118);
        const _: () = assert!(Element::Dummy as u8 == 119);
        const _: () = assert!(Element::D as u8 == 120);
        const _: () = assert!(Element::T as u8 == 121);

        if z == 0 || z > 121 {
            return None;
        }
        // SAFETY: z is in range 1-121, matching our enum discriminants.
        // The repr(u8) guarantees memory layout, and the const asserts validate bounds.
        Some(unsafe { std::mem::transmute::<u8, Element>(z) })
    }

    /// Get the element symbol.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert_eq!(Element::Fe.symbol(), "Fe");
    /// assert_eq!(Element::D.symbol(), "D");
    /// assert_eq!(Element::Dummy.symbol(), "X");
    /// ```
    pub fn symbol(&self) -> &'static str {
        match self {
            Self::Dummy => "X",
            Self::D => "D",
            Self::T => "T",
            _ => Self::SYMBOLS[self.atomic_number() as usize - 1],
        }
    }

    /// Get the atomic number (1-118).
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert_eq!(Element::Fe.atomic_number(), 26);
    /// ```
    pub fn atomic_number(&self) -> u8 {
        *self as u8
    }

    /// Get the Pauling electronegativity, if defined.
    ///
    /// Returns `None` for noble gases, transactinides, and pseudo-elements.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert!((Element::Fe.electronegativity().unwrap() - 1.83).abs() < 0.01);
    /// assert!(Element::He.electronegativity().is_none());  // Noble gas
    /// assert!(Element::Dummy.electronegativity().is_none()); // Pseudo-element
    /// ```
    pub fn electronegativity(&self) -> Option<f64> {
        // Pseudo-elements have no electronegativity
        if self.atomic_number() > 118 {
            return None;
        }
        let en = Self::ELECTRONEGATIVITIES[self.atomic_number() as usize - 1];
        if en.is_nan() { None } else { Some(en) }
    }

    /// Get the standard atomic weight in atomic mass units (u).
    ///
    /// For pseudo-elements:
    /// - Dummy returns 0.0
    /// - D (deuterium) returns 2.014
    /// - T (tritium) returns 3.016
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert!((Element::C.atomic_mass() - 12.011).abs() < 0.001);
    /// assert!((Element::D.atomic_mass() - 2.014).abs() < 0.001);
    /// assert_eq!(Element::Dummy.atomic_mass(), 0.0);
    /// ```
    pub fn atomic_mass(&self) -> f64 {
        match self {
            Self::Dummy => 0.0,
            Self::D => 2.014101778, // IUPAC deuterium mass
            Self::T => 3.01604928,  // IUPAC tritium mass
            _ => Self::ATOMIC_MASSES[self.atomic_number() as usize - 1],
        }
    }

    /// Check if this is a pseudo-element (Dummy, D, or T).
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert!(!Element::Fe.is_pseudo());
    /// assert!(Element::Dummy.is_pseudo());
    /// assert!(Element::D.is_pseudo());
    /// ```
    pub fn is_pseudo(&self) -> bool {
        self.atomic_number() > 118
    }

    /// Check if this is a dummy/placeholder element.
    pub fn is_dummy(&self) -> bool {
        matches!(self, Self::Dummy)
    }
}
