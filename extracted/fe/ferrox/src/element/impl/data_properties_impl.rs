use super::super::{Element, get_element_data};

impl Element {
    // =========================================================================
    // Physical Properties (from JSON data)
    // =========================================================================

    /// Get melting point in Kelvin.
    ///
    /// Returns `None` for elements without data (e.g., noble gases, superheavy elements).
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::element::Element;
    ///
    /// let fe_mp = Element::Fe.melting_point();
    /// assert!(fe_mp.is_some());
    /// assert!(fe_mp.unwrap() > 1800.0); // Iron melts at ~1811 K
    /// ```
    pub fn melting_point(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.melting_point)
    }

    /// Get boiling point in Kelvin.
    ///
    /// Returns `None` for elements without data.
    pub fn boiling_point(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.boiling_point)
    }

    /// Get density in g/cm³ (or g/L for gases at STP).
    ///
    /// Returns `None` for elements without data.
    pub fn density(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.density)
    }

    /// Get electron affinity in kJ/mol.
    ///
    /// The energy released when an electron is added to a neutral atom.
    /// Negative values indicate energy is required (unfavorable).
    ///
    /// Returns `None` for elements without data.
    pub fn electron_affinity(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.electron_affinity)
    }

    /// Get first ionization energy in kJ/mol.
    ///
    /// The energy required to remove the first electron from a neutral atom.
    ///
    /// Returns `None` for elements without data.
    pub fn first_ionization_energy(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.first_ionization)
    }

    /// Get all ionization energies in kJ/mol.
    ///
    /// Returns ionization energies for successive electron removals.
    /// Index 0 is the first ionization energy, index 1 is second, etc.
    ///
    /// Returns an empty slice for elements without data.
    pub fn ionization_energies(&self) -> &'static [f64] {
        get_element_data(self.atomic_number())
            .and_then(|d| d.ionization_energies.as_deref())
            .unwrap_or(&[])
    }

    /// Get molar heat capacity (Cp) in J/(mol·K).
    ///
    /// Returns `None` for elements without data.
    pub fn molar_heat(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.molar_heat)
    }

    /// Get specific heat capacity in J/(g·K).
    ///
    /// Returns `None` for elements without data.
    pub fn specific_heat(&self) -> Option<f64> {
        get_element_data(self.atomic_number()).and_then(|d| d.specific_heat)
    }

    /// Get the number of valence electrons.
    ///
    /// Returns `None` for elements without data.
    pub fn n_valence(&self) -> Option<u8> {
        get_element_data(self.atomic_number()).and_then(|d| d.n_valence)
    }

    /// Get electron configuration string (e.g., "1s2 2s2 2p6 3s2 3p6 4s2 3d6" for Fe).
    ///
    /// Returns `None` for elements without data.
    pub fn electron_configuration(&self) -> Option<&'static str> {
        get_element_data(self.atomic_number()).and_then(|d| d.electron_configuration.as_deref())
    }

    /// Get semantic electron configuration string (e.g., "[Ar] 4s2 3d6" for Fe).
    ///
    /// Uses noble gas core notation for brevity.
    /// Returns `None` for elements without data.
    pub fn electron_configuration_semantic(&self) -> Option<&'static str> {
        get_element_data(self.atomic_number())
            .and_then(|d| d.electron_configuration_semantic.as_deref())
    }
}
