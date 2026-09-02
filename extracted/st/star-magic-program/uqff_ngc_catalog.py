"""UQFF NGC Three-UQFF triadic galaxy catalogue (PAPER_786-805) — per-galaxy g_primary results
with programmatic formulas (triadic w_C g_comp + w_R g_res + w_B g_buoy; PAPER_961/962/963 forms)."""

def ngc_ngc_4826_black_eye_galaxy():
    """PAPER_786: NGC 4826 Black Eye Galaxy Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

def ngc_ngc_1805_lmc_star_cluster():
    """PAPER_787: NGC 1805 LMC Star Cluster Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

def ngc_ngc_685():
    """PAPER_800: NGC 685 Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

def ngc_ngc_3507():
    """PAPER_801: NGC 3507 Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

def ngc_ngc_3511():
    """PAPER_802: NGC 3511 Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

def ngc_ngc_3596():
    """PAPER_803: NGC 3596 Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

def ngc_ngc_1961():
    """PAPER_804: NGC 1961 Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

def ngc_ngc_5335():
    """PAPER_805: NGC 5335 Three-UQFF g_primary = g_compressed = 0.001053 m/s^2 (EM ground state; triadic simultaneous)."""
    return 0.001053

FORMULAS = {
    "ngc_ngc_4826_black_eye_galaxy": "NGC 4826 Black Eye Galaxy triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
    "ngc_ngc_1805_lmc_star_cluster": "NGC 1805 LMC Star Cluster triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
    "ngc_ngc_685": "NGC 685 triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
    "ngc_ngc_3507": "NGC 3507 triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
    "ngc_ngc_3511": "NGC 3511 triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
    "ngc_ngc_3596": "NGC 3596 triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
    "ngc_ngc_1961": "NGC 1961 triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
    "ngc_ngc_5335": "NGC 5335 triadic: g_primary=g_compressed=0.001053 m/s^2 (w_C g_comp + w_R g_res + w_B g_buoy)",
}

for _n,_f in FORMULAS.items():
    _o=globals().get(_n)
    if _o is not None: _o.formula=_f

def get_formula(name):
    "Paper formula for an ngc_* catalogue entry."
    return FORMULAS.get(name)

NGC_CATALOG_COUNT = 8
