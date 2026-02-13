
import numpy as np
from kwave.kgrid import kWaveGrid
from kwave.kmedium import kWaveMedium
from AOT_biomaps.AOT_Medium._mainMedium import Medium


class HomogeneousMedium(Medium):
    """
    Class representing a homogeneous medium for acoustic wave propagation.
    This class can be used
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_medium(self):
        """
        Génère un milieu k-Wave homogène basé sur les paramètres définis.
        """
        # --- 1. Grid setup et respect de Nyquist ---
        dx = self.params.general['dx']
        if dx >= self.params.acoustic['probe']['element_width']:
            dx = self.params.acoustic['probe']['element_width'] / 2
        # Dimensions physiques → pixels
        width = self.params.acoustic['medium'].get('width',
                self.params.general['Xrange'][1] - self.params.general['Xrange'][0])
        height = self.params.acoustic['medium'].get('height',
                self.params.general['Zrange'][1] - self.params.general['Zrange'][0])
        pva_nx = int(np.round(width / dx))
        pva_nz = int(np.round(height / dx))
        
        # Ajout des marges d'air si nécessaire
        air_margin = 20 if self.params.acoustic['medium']['isAirReflection'] else 0
        Nx, Nz = pva_nx + 2 * air_margin, pva_nz

        x_start = air_margin
        x_end = x_start + pva_nx

        # --- 2. Initialisation des cartes (air ou PVA) ---
        c_map = np.full((Nx, Nz), 343.0 if air_margin else self.params.acoustic['medium']['c0'], dtype=np.float32)
        rho_map = np.full((Nx, Nz), 1.2 if air_margin else self.params.acoustic['medium']['density'], dtype=np.float32)
        alpha_coeff_map = np.zeros((Nx, Nz), dtype=np.float32)
        BonA_map = np.zeros((Nx, Nz), dtype=np.float32)

        # Vitesse du son et densité dans le phantom
        c_map[x_start:x_end, :] = self.params.acoustic['medium']['c0']
        rho_map[x_start:x_end, :] = self.params.acoustic['medium']['density']

        # Atténuation et non-linéarité dans le phantom
        alpha_coeff_map[x_start:x_end, :] = self.params.acoustic['medium']['alpha_coeff']
        BonA_map[x_start:x_end, :] = self.params.acoustic['medium']['BonA']

        c_map = c_map.astype(np.float32)
        rho_map = rho_map.astype(np.float32)
        alpha_coeff_map = alpha_coeff_map.astype(np.float32)
        BonA_map = BonA_map.astype(np.float32)

        # --- 5. Création du milieu k-Wave ---
        self.kmedium = kWaveMedium(
            sound_speed=c_map,
            density=rho_map,
            alpha_coeff=alpha_coeff_map,
            alpha_power=self.params.acoustic['medium']['alpha_power'],
            BonA=BonA_map,
            absorbing=True,
            stokes=False
        )

        self.kgrid = kWaveGrid([Nx, Nz], [dx, dx])
        dt = 1/(self.params.acoustic['f_AQ'])
        self.kgrid.setTime(self.params.general['Nt'], dt)  # Garder Nt constant

        # Saving variable for later use
        self.factorX = int(np.ceil(self.params.general['dx'] / dx))
        self.factorZ = self.factorX
        self.factorT = int(np.ceil((1/self.kgrid.dt) / (self.params.acoustic['f_saving'])))
        self.c_mean = np.mean(c_map[:, 0])
        self.Nx_reshaped = Nx
        self.Nz_reshaped = Nz
        self.dx_reshaped = dx
