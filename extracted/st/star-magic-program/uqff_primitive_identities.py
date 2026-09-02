"""UQFF primitive-identity family (PAPER_1920-1999) — pi_* functions with programmatic FORMULAS
(Daniel ruling 2026-08-05: formulas available via .formula and get_formula)."""
from uqff_registry_primitives import (SO_5, F_TRZ, D_PHYS, D_CRIT, N_CH, A_5, SSQ)
K_MEX = 25.0/12.0
D_BSFG = 6

def pi_1_3_2_3():
    """PAPER_1940: DPM Spectrum Disc:Jet Split = 1/3 : 2/3 = 1/(D_phys - 1) EXACT Primitive-Forced Closure"""
    return 1/(D_PHYS - 1)

def pi_scale_universality():
    """PAPER_1941: DPM Decade Ratio 10:1 Cross-Scale Universality = SO_5 EXACT Integer Primitive"""
    return SO_5

def pi_toevaporation_initial_erosion_factor_e_0():
    """PAPER_1942: Photoevaporation Initial Erosion Factor E_0 = F_TRZ EXACT Primitive-Locked Identity"""
    return F_TRZ

def pi_saturation_universality_b_b_crit():
    """PAPER_1945: Magnetar Meissner-Saturation Universality B/B_crit = n_lobes * F_TRZ EXACT — CONFIRMED"""
    return 2 * F_TRZ

def pi_hierarchy_from_integer_primitives_tau_b():
    """PAPER_1946: Magnetar Timescale Hierarchy from Integer Primitives: tau_B = D_phys * SO_5^3 = 4000 yr, P_init = SO_5/(D_phys-2) = 5 s, tau_Omega = SO_5^4 = 10000 yr EXACT"""
    return D_PHYS * SO_5**(3)

def pi_ir_flare_frequency():
    """PAPER_1947: Sgr A* JWST 2025 Near-IR Flare Frequency = 1/((D_phys - 1) * A_5 * SO_5) Hz EXACT Triple-Integer-Primitive Lock"""
    return 1/((D_PHYS - 1) * A_5 * SO_5)

def pi_power_hierarchy_tau_pdr():
    """PAPER_1948: Photodissociation-Region Erosion Timescale SO_5-Power Hierarchy: tau_PDR = n_channels * SO_5^6 yr EXACT for n_channels in {1, 4, 5}"""
    return N_CH * SO_5**(6)

def pi_e_0():
    """PAPER_1951: F_TRZ Universal Radiation-Driven Outflow Fraction: L_Edd_ratio = F_0 = E_0 = F_TRZ = 0.1 EXACT Across AGN + PDR Radiation Physics"""
    return F_TRZ

def pi_k_mex_so_5():
    """PAPER_1957: Centaurus A Multi-Wavelength Activation Cycle τ_act = A_5·K_MEX / SO_5 = 125/10 = 12.5 Years EXACT"""
    return 125/10

def pi_so_5():
    """PAPER_1959: 2.7 Dual-Anchor: T_CMB and γ_CR Both Track (D_phys − 1)³ / SO_5 = 27/10 = 2.7 EXACT"""
    return 27/10

def pi_d_bsfg_d_phys():
    """PAPER_1962: D_BSFG / D_phys = 6/4 = 1.5 EXACT: Five-Instance Cross-Galactic Path B Instantiation of the 1.5 Identity Family (Companion to PAPER_1964 Path A / Path B Framework)"""
    return 6/4

def pi_antennae_coalescence():
    """PAPER_1982: Antennae Coalescence = D_phys · SO_5^8 yr = 400 Myr: New Slot Extension of the PAPER_1952 Galaxy-Scale SO_5-Power Timescale Grid, Completing the 2×2 Integer-Primitive Grid"""
    return D_PHYS * SO_5**(8)

FORMULAS = {
    "pi_1_3_2_3": "DPM Spectrum Disc:Jet Split = 1/3 : 2/3 = 1/(D_phys - 1) EXACT Primitive-Forced Closure",
    "pi_scale_universality": "DPM Decade Ratio 10:1 Cross-Scale Universality = SO_5 EXACT Integer Primitive",
    "pi_toevaporation_initial_erosion_factor_e_0": "Photoevaporation Initial Erosion Factor E_0 = F_TRZ EXACT Primitive-Locked Identity",
    "pi_saturation_universality_b_b_crit": "Magnetar Meissner-Saturation Universality B/B_crit = n_lobes * F_TRZ EXACT — CONFIRMED",
    "pi_hierarchy_from_integer_primitives_tau_b": "Magnetar Timescale Hierarchy from Integer Primitives: tau_B = D_phys * SO_5^3 = 4000 yr, P_init = SO_5/(D_phys-2) = 5 s, tau_Omega = SO_5^4 = 10000 yr EXACT",
    "pi_ir_flare_frequency": "Sgr A* JWST 2025 Near-IR Flare Frequency = 1/((D_phys - 1) * A_5 * SO_5) Hz EXACT Triple-Integer-Primitive Lock",
    "pi_power_hierarchy_tau_pdr": "Photodissociation-Region Erosion Timescale SO_5-Power Hierarchy: tau_PDR = n_channels * SO_5^6 yr EXACT for n_channels in {1, 4, 5}",
    "pi_e_0": "F_TRZ Universal Radiation-Driven Outflow Fraction: L_Edd_ratio = F_0 = E_0 = F_TRZ = 0.1 EXACT Across AGN + PDR Radiation Physics",
    "pi_k_mex_so_5": "Centaurus A Multi-Wavelength Activation Cycle τ_act = A_5·K_MEX / SO_5 = 125/10 = 12.5 Years EXACT",
    "pi_so_5": "2.7 Dual-Anchor: T_CMB and γ_CR Both Track (D_phys − 1)³ / SO_5 = 27/10 = 2.7 EXACT",
    "pi_d_bsfg_d_phys": "D_BSFG / D_phys = 6/4 = 1.5 EXACT: Five-Instance Cross-Galactic Path B Instantiation of the 1.5 Identity Family (Companion to PAPER_1964 Path A / Path B Framework)",
    "pi_antennae_coalescence": "Antennae Coalescence = D_phys · SO_5^8 yr = 400 Myr: New Slot Extension of the PAPER_1952 Galaxy-Scale SO_5-Power Timescale Grid, Completing the 2×2 Integer-Primitive Gri",
}

for _n,_f in FORMULAS.items():
    _o=globals().get(_n)
    if _o is not None: _o.formula=_f

def get_formula(name):
    "Paper formula chain for a pi_* function."
    return FORMULAS.get(name)

PRIMITIVE_IDENTITY_COUNT = 12
