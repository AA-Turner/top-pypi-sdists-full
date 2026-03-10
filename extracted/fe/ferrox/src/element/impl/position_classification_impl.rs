use super::super::{Block, Element, ShannonRadii, get_element_data};

impl Element {
    // =========================================================================
    // Periodic Table Positioning
    // =========================================================================

    /// Get the periodic table row (1-7).
    ///
    /// For lanthanoids (Z=57-71), returns 6.
    /// For actinoids (Z=89-103), returns 7.
    /// For pseudo-elements (Z>118), returns 0.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert_eq!(Element::H.row(), 1);
    /// assert_eq!(Element::Fe.row(), 4);
    /// assert_eq!(Element::La.row(), 6);  // Lanthanoid
    /// assert_eq!(Element::U.row(), 7);   // Actinoid
    /// ```
    pub fn row(&self) -> u8 {
        let z = self.atomic_number();
        if z > 118 {
            return 0; // Pseudo-elements
        }
        if (57..=71).contains(&z) {
            return 6; // Lanthanoids
        }
        if (89..=103).contains(&z) {
            return 7; // Actinoids
        }

        const ROW_SIZES: [u8; 7] = [2, 8, 8, 18, 18, 32, 32];
        let mut total: u8 = 0;
        for (row_idx, &size) in ROW_SIZES.iter().enumerate() {
            total += size;
            if z <= total {
                return (row_idx + 1) as u8;
            }
        }
        7
    }

    /// Get the periodic table group (1-18).
    ///
    /// For lanthanoids and actinoids, returns 3.
    /// For pseudo-elements, returns 0.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// assert_eq!(Element::H.group(), 1);
    /// assert_eq!(Element::He.group(), 18);
    /// assert_eq!(Element::Fe.group(), 8);
    /// assert_eq!(Element::La.group(), 3);  // Lanthanoid
    /// ```
    pub fn group(&self) -> u8 {
        let z = self.atomic_number();
        if z > 118 {
            return 0;
        }

        match z {
            1 => 1,
            2 => 18,
            3..=18 => {
                let pos = (z - 2) % 8;
                if pos == 0 {
                    18
                } else if pos <= 2 {
                    pos
                } else {
                    10 + pos
                }
            }
            19..=54 => {
                let pos = (z - 18) % 18;
                if pos == 0 { 18 } else { pos }
            }
            57..=71 | 89..=103 => 3, // Lanthanoids and actinoids
            _ => {
                let pos = (z - 54) % 32;
                if pos == 0 {
                    18
                } else if pos >= 18 {
                    pos - 14
                } else {
                    pos
                }
            }
        }
    }

    /// Get the periodic table block (s, p, d, or f).
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::{Element, Block};
    ///
    /// assert_eq!(Element::H.block(), Block::S);
    /// assert_eq!(Element::C.block(), Block::P);
    /// assert_eq!(Element::Fe.block(), Block::D);
    /// assert_eq!(Element::Ce.block(), Block::F);
    /// ```
    pub fn block(&self) -> Block {
        let z = self.atomic_number();

        // Lanthanoids (except Lu) and actinoids (except Lr) are f-block
        if (57..=70).contains(&z) || (89..=102).contains(&z) {
            return Block::F;
        }

        let group = self.group();
        match group {
            0 => Block::S, // Pseudo-elements
            1 | 2 => Block::S,
            3..=12 => Block::D,
            13..=18 => Block::P,
            _ => Block::S,
        }
    }

    // =========================================================================
    // Element Classification
    // =========================================================================

    /// True if element is a noble gas (He, Ne, Ar, Kr, Xe, Rn, Og).
    pub fn is_noble_gas(&self) -> bool {
        matches!(self.atomic_number(), 2 | 10 | 18 | 36 | 54 | 86 | 118)
    }

    /// True if element is an alkali metal (Li, Na, K, Rb, Cs, Fr).
    pub fn is_alkali(&self) -> bool {
        matches!(self.atomic_number(), 3 | 11 | 19 | 37 | 55 | 87)
    }

    /// True if element is an alkaline earth metal (Be, Mg, Ca, Sr, Ba, Ra).
    pub fn is_alkaline(&self) -> bool {
        matches!(self.atomic_number(), 4 | 12 | 20 | 38 | 56 | 88)
    }

    /// True if element is a halogen (F, Cl, Br, I, At).
    ///
    /// Note: Tennessine (Ts, Z=117) is excluded despite being in group 17,
    /// as its chemical properties are predicted to differ significantly from
    /// traditional halogens. This matches pymatgen's classification.
    pub fn is_halogen(&self) -> bool {
        matches!(self.atomic_number(), 9 | 17 | 35 | 53 | 85)
    }

    /// True if element is a chalcogen (O, S, Se, Te, Po).
    pub fn is_chalcogen(&self) -> bool {
        matches!(self.atomic_number(), 8 | 16 | 34 | 52 | 84)
    }

    /// True if element is a lanthanoid (La-Lu, Z=57-71).
    pub fn is_lanthanoid(&self) -> bool {
        (57..=71).contains(&self.atomic_number())
    }

    /// True if element is an actinoid (Ac-Lr, Z=89-103).
    pub fn is_actinoid(&self) -> bool {
        (89..=103).contains(&self.atomic_number())
    }

    /// True if element is a transition metal.
    ///
    /// Includes Sc-Zn (21-30), Y-Cd (39-48), La (57), Hf-Hg (72-80),
    /// Ac (89), and Rf-Cn (104-112).
    ///
    /// Note: La and Ac return true for both `is_transition_metal()` and
    /// `is_lanthanoid()`/`is_actinoid()`. This reflects that these elements
    /// are often classified both ways in the literature.
    pub fn is_transition_metal(&self) -> bool {
        let z = self.atomic_number();
        matches!(z, 21..=30 | 39..=48 | 72..=80 | 104..=112) || z == 57 || z == 89
    }

    /// True if element is a post-transition metal (Al, Ga, In, Tl, Sn, Pb, Bi).
    pub fn is_post_transition_metal(&self) -> bool {
        matches!(
            self,
            Self::Al | Self::Ga | Self::In | Self::Tl | Self::Sn | Self::Pb | Self::Bi
        )
    }

    /// True if element is a metalloid (B, Si, Ge, As, Sb, Te, Po).
    pub fn is_metalloid(&self) -> bool {
        matches!(
            self,
            Self::B | Self::Si | Self::Ge | Self::As | Self::Sb | Self::Te | Self::Po
        )
    }

    /// True if element is a metal (alkali, alkaline, transition, post-transition,
    /// lanthanoid, or actinoid).
    pub fn is_metal(&self) -> bool {
        self.is_alkali()
            || self.is_alkaline()
            || self.is_transition_metal()
            || self.is_post_transition_metal()
            || self.is_lanthanoid()
            || self.is_actinoid()
    }

    /// True if element is radioactive.
    ///
    /// Includes Tc (43), Pm (61), and all elements with Z >= 84.
    pub fn is_radioactive(&self) -> bool {
        let z = self.atomic_number();
        z == 43 || z == 61 || z >= 84
    }

    /// True if element is a rare earth (lanthanoid, actinoid, Sc, or Y).
    pub fn is_rare_earth(&self) -> bool {
        self.is_lanthanoid() || self.is_actinoid() || matches!(self, Self::Sc | Self::Y)
    }

    // =========================================================================
    // Oxidation States (from JSON data)
    // =========================================================================

    /// Get all known oxidation states for this element.
    ///
    /// Returns an empty slice for pseudo-elements or elements without data.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// let fe_oxi = Element::Fe.oxidation_states();
    /// assert!(fe_oxi.contains(&2));
    /// assert!(fe_oxi.contains(&3));
    /// ```
    pub fn oxidation_states(&self) -> &'static [i8] {
        get_element_data(self.atomic_number())
            .and_then(|d| d.oxidation_states.as_deref())
            .unwrap_or(&[])
    }

    /// Get common oxidation states for this element.
    ///
    /// Returns an empty slice for pseudo-elements or elements without data.
    pub fn common_oxidation_states(&self) -> &'static [i8] {
        get_element_data(self.atomic_number())
            .and_then(|d| d.common_oxidation_states.as_deref())
            .unwrap_or(&[])
    }

    /// Get ICSD oxidation states (oxidation states with at least 10 instances in ICSD).
    pub fn icsd_oxidation_states(&self) -> &'static [i8] {
        get_element_data(self.atomic_number())
            .and_then(|d| d.icsd_oxidation_states.as_deref())
            .unwrap_or(&[])
    }

    /// Get maximum oxidation state.
    pub fn max_oxidation_state(&self) -> Option<i8> {
        self.oxidation_states().iter().copied().max()
    }

    /// Get minimum oxidation state.
    pub fn min_oxidation_state(&self) -> Option<i8> {
        self.oxidation_states().iter().copied().min()
    }

    // =========================================================================
    // Radii (from JSON data)
    // =========================================================================

    /// Get atomic radius in Angstroms.
    ///
    /// Returns `None` for pseudo-elements or elements without data.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// let fe_radius = Element::Fe.atomic_radius();
    /// assert!(fe_radius.is_some());
    /// assert!(fe_radius.unwrap() > 1.0 && fe_radius.unwrap() < 2.0);
    /// ```
    pub fn atomic_radius(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.atomic_radius)
    }

    /// Get covalent radius in Angstroms.
    pub fn covalent_radius(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.covalent_radius)
    }

    /// Get ionic radii by oxidation state.
    ///
    /// Returns a reference to a HashMap where keys are oxidation states as strings
    /// (e.g., "2", "-1") and values are radii in Angstroms.
    pub fn ionic_radii(&self) -> Option<&'static std::collections::HashMap<String, f64>> {
        get_element_data(self.atomic_number()).and_then(|d| d.ionic_radii.as_ref())
    }

    /// Get ionic radius for a specific oxidation state.
    ///
    /// # Arguments
    ///
    /// * `oxidation_state` - The oxidation state (e.g., 2 for Fe2+, -2 for O2-)
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// let fe2_radius = Element::Fe.ionic_radius(2);
    /// assert!(fe2_radius.is_some());
    /// ```
    pub fn ionic_radius(&self, oxidation_state: i8) -> Option<f64> {
        self.ionic_radii()
            .and_then(|radii| radii.get(&oxidation_state.to_string()))
            .copied()
    }

    /// Get Shannon radii data for this element.
    ///
    /// Shannon radii provide detailed ionic radii accounting for coordination number
    /// and spin state. The returned structure is:
    /// oxidation_state -> coordination -> spin -> {crystal_radius, ionic_radius}
    pub fn shannon_radii(&self) -> Option<&'static ShannonRadii> {
        get_element_data(self.atomic_number()).and_then(|d| d.shannon_radii.as_ref())
    }

    /// Get Shannon ionic radius for a specific oxidation state, coordination, and spin.
    ///
    /// # Arguments
    ///
    /// * `oxidation_state` - The oxidation state (e.g., 2 for Fe2+)
    /// * `coordination` - Coordination number as Roman numeral (e.g., "VI" for octahedral)
    /// * `spin` - Spin state (e.g., "High Spin", "Low Spin", or "" for no spin)
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// // Fe2+ in octahedral (VI) high spin coordination
    /// let radius = Element::Fe.shannon_ionic_radius(2, "VI", "High Spin");
    /// ```
    pub fn shannon_ionic_radius(
        &self,
        oxidation_state: i8,
        coordination: &str,
        spin: &str,
    ) -> Option<f64> {
        self.shannon_radii()
            .and_then(|sr| sr.get(&oxidation_state.to_string()))
            .and_then(|coord_map| coord_map.get(coordination))
            .and_then(|spin_map| spin_map.get(spin))
            .map(|pair| pair.ionic_radius)
    }

    /// Get the full name of this element (e.g., "Iron" for Fe).
    pub fn name(&self) -> &'static str {
        get_element_data(self.atomic_number())
            .map(|d| d.name.as_str())
            .unwrap_or("Unknown")
    }
}
