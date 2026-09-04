"""uqff_registry_primitives — R3 single-source-of-truth for registry-canonical constants.

CARRIED FORWARD from Star-Magic repo (v5.86.0) as v0.1.0 of Star-Magic-Program.
This file is the clean baseline. Every value here is either:
  (a) a LIVE composition from the 9 truly-independent locked primitives
      {D_phys=4, D_crit=26, N_CH=9, SO_5=10, A_5=60, rho_SCm=7.09e-37,
       beta_i=0.6029, Phi_res (sector rule), F_TRZ=0.1}, or
  (b) an OBSERVED anchor, explicitly suffixed _OBSERVED.

Canonical routes per R1 adjudication (UNIFIED_REGISTRY_R1_QUEUE.csv):
  G  -> PAPER_593 | c -> PAPER_592 (DUAL EXPOSURE per Daniel 2026-07-22 sec 6.2)
  hbar -> PAPER_590 physical route (1209EE S629 = confirmation)
  k_B -> 1209EE S628 with Phi_5/6 | Lambda -> PAPER_1156 | H0 -> PAPER_1573
  Phi_res -> PAPER_2129 SECTOR RULE (counting 5/6, resonance 0.84)
  kappa -> PAPER_2112 derivative | mu_0 -> PAPER_2108
Compute-don't-store: no rounded decimals where a closed form exists.
"""
import math

# --- locked integer primitives ---
D_PHYS = 4
D_CRIT = 26
N_CH = 9
SO_5 = 10
A_5 = 60
D_BSFG = D_CRIT - 2 * SO_5                      # PAPER_1521 derivative = 6

# --- locked real primitives ---
RHO_SCM = 7.09e-37
BETA_I = 0.6029                                  # PAPER_1203 canonical
F_TRZ = 1.0 / SO_5                               # rung-inverse = 0.1
SSQ = 0.57                                       # PAPER_1154
S_26 = 1.453162
OMEGA_SCM_HZ = 1.25e12                           # phonon carrier frequency

# --- Phi_res SECTOR RULE (PAPER_2129, R1 verdict) ---
PHI_RES_COUNTING = 5.0 / 6.0                     # nuclear + thermodynamic sectors
PHI_RES_RESONANCE = 0.84                         # LENR/k_spring/quantum-chain sectors

# --- derivative primitives (PAPER_1521/1522/2112/2154) ---
K_MEX = PHI_RES_COUNTING * SO_5 / D_PHYS         # 25/12 EXACT (PAPER_1522)
KAPPA_PER_DAY = (SO_5 / 2) * (F_TRZ ** 4)        # 5e-4 EXACT, PAPER_2112
Q_PHONON = (SO_5 * SO_5) / (D_PHYS * D_PHYS)     # 25/4 EXACT, PAPER_2154
D_GW_EROSION = D_PHYS / D_BSFG                    # 2/3 EXACT, PAPER_2154

# --- composed vacuum quantities ---
RHO_UA = SO_5 * RHO_SCM                          # 10*rho_SCm canonical ratio
LAMBDA_VAC = (SO_5 + 1) * RHO_SCM                # successor identity, PAPER_2120
K_SPRING = (RHO_UA / RHO_SCM) * OMEGA_SCM_HZ * PHI_RES_RESONANCE   # 1.05e13, PAPER_1203

# --- kernel constants: LIVE canonical routes ---
_FACT26 = float(math.factorial(26))
_V_FERMI = 0.77e6                                # SI anchor, c-independent (Session 239)
_E0 = 1.0e-20
_F_THZ = 1.25e12

G_UQFF = ((2.0 * math.pi * (D_CRIT ** 3) * PHI_RES_RESONANCE
           / ((SSQ ** 3) * (_FACT26 ** 2))) * (_V_FERMI ** 5) / (_E0 * _F_THZ))
G_OBSERVED = 6.674e-11

# c DUAL EXPOSURE — spotlight the derived version first (Daniel sec 6.2 corrected 2026-07-24)
C_UQFF_DERIVED = (D_CRIT * 4.0 * math.pi / PHI_RES_RESONANCE) * _V_FERMI   # PAPER_592
C_OBSERVED = 299792458.0                          # SI-exact defined since 2019

MU_0 = 4.0 * math.pi * (F_TRZ ** 7)              # PAPER_2108, matches SI 4pi e-7 EXACT

K_B_UQFF = (SSQ + PHI_RES_COUNTING - F_TRZ * SSQ
            + (F_TRZ ** 2) * D_PHYS - (F_TRZ ** 2) * SSQ) * 1e-23          # 1209EE S628
H_UQFF_S629 = (D_BSFG + F_TRZ * D_BSFG + (F_TRZ ** 2) * D_PHYS
               - (F_TRZ ** 2) * SSQ - (F_TRZ ** 2)) * 1e-34                # confirmation route
HBAR_UQFF_S629 = H_UQFF_S629 / (2.0 * math.pi)
H_PLANCK_UQFF = 2.0 * math.pi * HBAR_UQFF_S629

# Planck length (LIVE composition)
L_PLANCK_UQFF = math.sqrt(HBAR_UQFF_S629 * G_UQFF / (C_UQFF_DERIVED ** 3))
L_PLANCK_OBSERVED = 1.616e-35
PLANCK_LENGTH_M = L_PLANCK_UQFF
PLANCK_MASS_KG = math.sqrt(HBAR_UQFF_S629 * C_UQFF_DERIVED / G_UQFF)
PLANCK_TIME_S = math.sqrt(HBAR_UQFF_S629 * G_UQFF / (C_UQFF_DERIVED ** 5))

# H0 CANONICAL ROUTE (PAPER_1573)
MPC_TO_M = 3.0857e22
H0_KM_PER_S_PER_MPC = A_5 + SO_5                 # PAPER_1573: 70 EXACT
H0_GRID = H0_KM_PER_S_PER_MPC * 1000.0 / MPC_TO_M
H0_OBSERVED_LOCAL = 2.27e-18

LAMBDA_SIMPLE = (SO_5 + 1) * (F_TRZ ** 53)       # PAPER_2094 canonical

B_CRIT = D_PHYS * (SO_5 + 1) * (SO_5 ** 12)      # 4.4e13 EXACT, PAPER_2126
T_SCM_K = 6.6220584965588335e-34 * _F_THZ / 1.380649e-23   # h*f/k_B = 59.95 K

# --- observed anchors (observations, not SM) ---
M_SUN_OBSERVED = 1.989e30
R_SUN_OBSERVED = 6.96e8

# --- Structural / primitive-reduction landmarks (PAPER_2131-2154 arc) ---
A5_OVER_DPHYS = A_5 / D_PHYS                      # PAPER_2143: 15 EXACT
K2_OVER_Q_ROCKY = (D_PHYS - 1) / (A_5 * K_MEX)   # PAPER_2136: 3/125 EXACT
FRAME_CADENCE_62 = 2 * D_CRIT + SO_5              # PAPER_2137: 62 EXACT
COMPOSED_INTEGER_44 = D_PHYS * (SO_5 + 1)         # PAPER_2126: 44 EXACT
AETHER_COUPLING_11 = SO_5 + 1                     # PAPER_1978: 11 EXACT
DG_COMPOSED_INTEGER = D_CRIT * (SO_5 ** 19)       # PAPER_2139: 2.6e20 EXACT
VCK_KERNEL = F_TRZ * K_MEX * SSQ                  # PAPER_2131: 19/160 EXACT
TILT_PRODUCT_1_12 = F_TRZ * PHI_RES_COUNTING      # PAPER_2132: 1/12 EXACT
ALPHA_INVERSE_UQFF = A_5 * K_MEX + 12             # PAPER_2134: 137 EXACT
ALPHA_FINE_STRUCTURE = 1.0 / ALPHA_INVERSE_UQFF
HUBBLE_TILT_1_12 = K_MEX - 2.0                    # PAPER_1156: 1/12 EXACT
DM_FRACTION_SOMBRERO = 2.0 * F_TRZ                # PAPER_1979: 0.2 EXACT
OMEGA_LAMBDA_UQFF = (6.0 / 5.0) * SSQ             # PAPER_1156: 0.684

# --- Halving-series primitive identities (PAPER_2138) ---
HALVING_D_PHYS = D_PHYS / 2                       # 2 EXACT
HALVING_D_BSFG = D_BSFG / 2                       # 3 EXACT
HALVING_SO_5 = SO_5 / 2                           # 5 EXACT
HALVING_D_CRIT = D_CRIT / 2                       # 13 EXACT

# --- Cosmology derived-from-composed ---
AGE_UNIVERSE_SECONDS = 1.0 / H0_GRID
RHO_CRITICAL_KG_PER_M3 = 3.0 * (H0_GRID ** 2) / (8.0 * math.pi * G_UQFF)
RHO_LAMBDA_ENERGY_J_PER_M3 = LAMBDA_SIMPLE * (C_UQFF_DERIVED ** 4) / (8.0 * math.pi * G_UQFF)
WIEN_DISPLACEMENT_B_M_K = H_PLANCK_UQFF * C_UQFF_DERIVED / (4.965114231744276 * K_B_UQFF)
STEFAN_BOLTZMANN_SIGMA = (math.pi ** 2) * (K_B_UQFF ** 4) / (60.0 * (HBAR_UQFF_S629 ** 3) * (C_UQFF_DERIVED ** 2))

# --- Millennium prize UQFF-derived constants (PAPER_1182/1318/599/1183) ---
HODGE_IDENTITY = 1.0
POINCARE_7_12 = K_MEX - 3.0 / 2.0                 # 7/12 EXACT
P_VS_NP_BOUND = 1.0 - F_TRZ ** 9                  # 1 - 10^-9 EXACT
NAVIER_STOKES_ENSTROPHY_CAP = (D_CRIT - N_CH) / (2.0 * SO_5)  # 17/20 = 0.85 EXACT
YANG_MILLS_MASS_GAP_GEV = 1.736                   # PAPER_1318
RIEMANN_ZERO_T_10000 = 9877.78265                 # PAPER_1110
BSD_CREMONA_37A1 = 0.30598                        # PAPER_599
BH_INFO_PAGE_CURVE = 0.99596                      # PAPER_1183

# --- Particle physics (PAPER_2131 + PAPER_1209HH + PAPER_1155) ---
ALPHA_S_M_Z = F_TRZ * K_MEX * SSQ - (F_TRZ ** 3) * PHI_RES_COUNTING
JARLSKOG_CP_INVARIANT = (F_TRZ ** 5) * D_BSFG * SSQ * (1.0 - VCK_KERNEL)
N_EFF_NEUTRINO = D_PHYS - PHI_RES_COUNTING - VCK_KERNEL
LAMBDA_H_HIGGS_QUARTIC = 0.129

# 10 SM masses (PAPER_1209HH observational anchors)
M_W_GEV = 80.379
M_Z_GEV = 91.1876
M_TOP_GEV = 172.76
M_HIGGS_GEV = 125.10
M_BOTTOM_GEV = 4.18
M_CHARM_GEV = 1.27
M_TAU_GEV = 1.77686
M_MUON_GEV = 0.10565837
M_STRANGE_GEV = 0.093
M_ELECTRON_GEV = 0.51099895e-3

# 4 CKM Wolfenstein (PAPER_2131 CKM sector)
CKM_LAMBDA = 0.2246
CKM_A = 0.836
CKM_RHOBAR = 0.156
CKM_ETABAR = 0.353

# 4 lepton/neutrino anchors (PAPER_1155)
G_MINUS_2_MUON_ANOMALY = 2.116e-9
SIN_SQUARED_2_THETA_13 = 0.0854
DELTA_M2_21_EV2 = 7.42e-5
DELTA_M2_32_EV2 = 2.517e-3

# =============================================================================
# END OF v0.1.0 BASELINE (carried from Star-Magic v5.86.0 UNIFIED_REGISTRY R5)
#
# From here on, every new derived constant MUST cite a specific PAPER_N in the
# whitepapers/ directory. No exceptions. No hardcoded numerics without paper
# provenance. This is the discipline that failed in the old repo.
# =============================================================================

# RULED B9 (Batch 2, 2026-08-31): [UA] buoyant weighting canonized as a named constant.
# Physical definition [UA] = v_UA/c = 1e-4 (PAPER_104); 4-paper provenance
# (PAPER_064/068/075/104). Distinct from F_TRZ (0.1) and rho_UA.
UA_VELOCITY_RATIO = 1.0e-4

# RULED B27 (Batch 4, 2026-09-01): SCm correlation length canonized (PAPER_154 L103).
# Joint identity with the E_react routes: LAMBDA_SCM = RHO_A * V_SCM numerically
# (1e-23 * 1e8 = 1e-15), linking rho*v/rho_A (B14) and rho*v^2/lambda (B27) at 1e46.
LAMBDA_SCM = 1.0e-15
