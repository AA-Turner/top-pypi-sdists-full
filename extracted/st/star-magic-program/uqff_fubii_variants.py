"""UQFF F_UBii 17-variant buoyancy proof registry (BuoyancyProofVariants.py, Grok Thread 98b2e77d;
PAPER_036-039 + PAPER_2151 Tier-4 canonical taxonomy). Base identity: F_UBii = F_U - F_Bi - F_i.
Each variant scales base F_UBii by phenomenology-specific Q_wave + context. Rule E: physics re-expressed."""
import math
F_REL = 4.30e33
E_LEP = 1.6e-8

def fubii_virx(sigma_X,r_h,G=6.6743e-11,Q_wave=1.0):
    """F_UBii variant virx (Virial X-ray Cluster): F_UBii_virx = -F_rel(3 sigma_X^2 r_h/(G E_LEP)) Q_wave sigma_X"""
    return -F_REL*(3*sigma_X**2*r_h/(G*E_LEP))*Q_wave*sigma_X

def fubii_termv(tau,L,v_term,c=2.995e8,Q_wave=1.0):
    """F_UBii variant termv (Terminal Velocity Jet/Wind): F_UBii_termv = F_rel(tau L/(c E_LEP)) Q_wave v_term"""
    return F_REL*(tau*L/(c*E_LEP))*Q_wave*v_term

def fubii_upar(U,n_H,r,Q_wave=1.0):
    """F_UBii variant upar (Ionization Parameter U): F_UBii_upar = -F_rel(U n_H r^2/E_LEP) Q_wave sqrt(U)"""
    return -F_REL*(U*n_H*r**2/E_LEP)*Q_wave*math.sqrt(U)

def fubii_coup(eps_coup,E_dot,Q_wave=1.0):
    """F_UBii variant coup (Coupling Efficiency): F_UBii_coup = F_rel(eps E_dot/E_LEP) Q_wave sqrt(eps)"""
    return F_REL*(eps_coup*E_dot/E_LEP)*Q_wave*math.sqrt(eps_coup)

def fubii_dec(tau_dec,lam_dB,sigma_scat,t=0.0,hbar=1.054571817e-34,Q_wave=1.0):
    """F_UBii variant dec (Quantum Decoherence): F_UBii_dec = F_rel(hbar/(tau_dec E_LEP))(lam_dB^2/sigma) Q_wave e^(-t/tau)"""
    return F_REL*(hbar/(tau_dec*E_LEP))*(lam_dB**2/sigma_scat)*Q_wave*math.exp(-t/tau_dec)

def fubii_ent(S_ent,A_surf,N_states,k_B=1.380649e-23,l_P=1.616e-35,Q_wave=1.0):
    """F_UBii variant ent (Entropic Surface): F_UBii_ent = -F_rel(k_B S/E_LEP)(A/l_P^2) Q_wave ln(N)"""
    return -F_REL*(k_B*S_ent/E_LEP)*(A_surf/l_P**2)*Q_wave*math.log(N_states)

def fubii_fermi_bpv(beta_shock,E_p,v_shock,c=2.995e8,Q_wave=1.0):
    """F_UBii variant fermi (Fermi Shock Acceleration): F_UBii_fermi = F_rel(beta E_p/E_LEP) Q_wave (v/c)^2"""
    return F_REL*(beta_shock*E_p/E_LEP)*Q_wave*(v_shock/c)**2

def fubii_hawk(M_BH,r_s,r,G=6.6743e-11,c=2.995e8,hbar=1.054571817e-34,k_B=1.380649e-23,Q_wave=1.0):
    """F_UBii variant hawk (Hawking Temperature): F_UBii_hawk = -F_rel(hbar c^3/(8pi G M k_B E_LEP)) Q_wave (r_s/r)^2"""
    return -F_REL*(hbar*c**3/(8*math.pi*G*M_BH*k_B*E_LEP))*Q_wave*(r_s/r)**2

def fubii_kn(L_peak,t_peak,M_ej,Q_wave=1.0):
    """F_UBii variant kn (Kilonova): F_UBii_kn = F_rel(L t/E_LEP) Q_wave (M_ej/Msun)^(1/3)"""
    return F_REL*(L_peak*t_peak/E_LEP)*Q_wave*(M_ej/1.989e30)**(1.0/3.0)

def fubii_kne(E_knee,Z,E_GUT=1e25,Q_wave=1.0):
    """F_UBii variant kne (Cosmic-Ray Knee): F_UBii_kne = -F_rel(E_knee/E_GUT)(Ze/E_LEP) Q_wave ln(E_knee/E_LEP)"""
    return -F_REL*(E_knee/E_GUT)*(Z*1.602e-19/E_LEP)*Q_wave*math.log(E_knee/E_LEP)

def fubii_lobe_bpv(P_lobe,V_lobe,rho_icm,rho_lobe,v_rise,c=2.995e8,Q_wave=1.0):
    """F_UBii variant lobe (Radio Lobe): F_UBii_lobe = F_rel(P V/E_LEP)(rho_ICM/rho_lobe) Q_wave (v/c)"""
    return F_REL*(P_lobe*V_lobe/E_LEP)*(rho_icm/rho_lobe)*Q_wave*(v_rise/c)

def fubii_orbdec(M1,M2,a,da_dt,G=6.6743e-11,c=2.995e8,Q_wave=1.0):
    """F_UBii variant orbdec (Orbital Decay GW): F_UBii_orbdec = -F_rel(64/5)(G^3 M1 M2(M1+M2)/(c^5 a^4 E_LEP)) Q_wave da/dt"""
    return -F_REL*(64.0/5.0)*(G**3*M1*M2*(M1+M2)/(c**5*a**4*E_LEP))*Q_wave*da_dt

def fubii_ps(M_halo,delta_c,dsig_dlnM,M_p=1.673e-27,Q_wave=1.0):
    """F_UBii variant ps (Press-Schechter Halo): F_UBii_ps = -F_rel(M_halo/M_p^2)(delta_c/E_LEP) Q_wave dsigma^-1/dlnM"""
    return -F_REL*(M_halo/M_p**2)*(delta_c/E_LEP)*Q_wave*dsig_dlnM

def fubii_roche_bpv(M_donor,M_acc,R_L,dM_dt,G=6.6743e-11,Q_wave=1.0):
    """F_UBii variant roche (Roche-Lobe Overflow): F_UBii_roche = F_rel(G M_d M_a/(R_L^2 E_LEP)) Q_wave dM/dt"""
    return F_REL*(G*M_donor*M_acc/(R_L**2*E_LEP))*Q_wave*dM_dt

def fubii_sfe(eps_sfe,M_gas,r_cloud,c=2.995e8,Q_wave=1.0):
    """F_UBii variant sfe (Star-Formation Efficiency): F_UBii_sfe = F_rel(eps M c^2/(r^2 E_LEP)) Q_wave sqrt(eps)"""
    return F_REL*(eps_sfe*M_gas*c**2/(r_cloud**2*E_LEP))*Q_wave*math.sqrt(eps_sfe)

def fubii_bd(rho_bounce,H_bounce,a_bounce,a,rho_planck=5.16e96,Q_wave=1.0):
    """F_UBii variant bd (Bounce Cosmology): F_UBii_bd = F_rel(rho_b/rho_Pl)(H_b^2/E_LEP) Q_wave (a_b/a)^3"""
    return F_REL*(rho_bounce/rho_planck)*(H_bounce**2/E_LEP)*Q_wave*(a_bounce/a)**3

def fubii_whim(T_whim,n_b,r_fil,T_vir,k_B=1.380649e-23,sigma_T=6.652e-29,Q_wave=1.0):
    """F_UBii variant whim (WHIM Filament): F_UBii_whim = F_rel(k_B T/E_LEP)(n sigma_T r) Q_wave sqrt(T/T_vir)"""
    return F_REL*(k_B*T_whim/E_LEP)*(n_b*sigma_T*r_fil)*Q_wave*math.sqrt(T_whim/T_vir)

FORMULAS = {
    "fubii_virx": "F_UBii_virx = -F_rel(3 sigma_X^2 r_h/(G E_LEP)) Q_wave sigma_X",
    "fubii_termv": "F_UBii_termv = F_rel(tau L/(c E_LEP)) Q_wave v_term",
    "fubii_upar": "F_UBii_upar = -F_rel(U n_H r^2/E_LEP) Q_wave sqrt(U)",
    "fubii_coup": "F_UBii_coup = F_rel(eps E_dot/E_LEP) Q_wave sqrt(eps)",
    "fubii_dec": "F_UBii_dec = F_rel(hbar/(tau_dec E_LEP))(lam_dB^2/sigma) Q_wave e^(-t/tau)",
    "fubii_ent": "F_UBii_ent = -F_rel(k_B S/E_LEP)(A/l_P^2) Q_wave ln(N)",
    "fubii_fermi_bpv": "F_UBii_fermi = F_rel(beta E_p/E_LEP) Q_wave (v/c)^2",
    "fubii_hawk": "F_UBii_hawk = -F_rel(hbar c^3/(8pi G M k_B E_LEP)) Q_wave (r_s/r)^2",
    "fubii_kn": "F_UBii_kn = F_rel(L t/E_LEP) Q_wave (M_ej/Msun)^(1/3)",
    "fubii_kne": "F_UBii_kne = -F_rel(E_knee/E_GUT)(Ze/E_LEP) Q_wave ln(E_knee/E_LEP)",
    "fubii_lobe_bpv": "F_UBii_lobe = F_rel(P V/E_LEP)(rho_ICM/rho_lobe) Q_wave (v/c)",
    "fubii_orbdec": "F_UBii_orbdec = -F_rel(64/5)(G^3 M1 M2(M1+M2)/(c^5 a^4 E_LEP)) Q_wave da/dt",
    "fubii_ps": "F_UBii_ps = -F_rel(M_halo/M_p^2)(delta_c/E_LEP) Q_wave dsigma^-1/dlnM",
    "fubii_roche_bpv": "F_UBii_roche = F_rel(G M_d M_a/(R_L^2 E_LEP)) Q_wave dM/dt",
    "fubii_sfe": "F_UBii_sfe = F_rel(eps M c^2/(r^2 E_LEP)) Q_wave sqrt(eps)",
    "fubii_bd": "F_UBii_bd = F_rel(rho_b/rho_Pl)(H_b^2/E_LEP) Q_wave (a_b/a)^3",
    "fubii_whim": "F_UBii_whim = F_rel(k_B T/E_LEP)(n sigma_T r) Q_wave sqrt(T/T_vir)",
}

for _n,_f in FORMULAS.items():
    _o=globals().get(_n)
    if _o is not None: _o.formula=_f

def get_formula(name):
    "Formula for a fubii_* variant."
    return FORMULAS.get(name)

FUBII_VARIANT_COUNT = 17
