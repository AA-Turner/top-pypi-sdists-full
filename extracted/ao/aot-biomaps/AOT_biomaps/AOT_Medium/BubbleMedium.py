import numpy as np
from kwave.kgrid import kWaveGrid
from kwave.kmedium import kWaveMedium
from scipy.ndimage import gaussian_filter
from AOT_biomaps.AOT_Medium._mainMedium import Medium

class BubbleMedium(Medium):
    """
    Class representing a medium with random air bubbles for acoustic wave propagation.
    - Air bubbles are randomly distributed in a background medium (e.g., water or gel).
    - Optional air margin around the medium.
    - Respects Nyquist and optimizes VRAM (float32, in-place calculations).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_medium(self):
        """
        Génère un milieu k-Wave avec des bulles d'air aléatoires.
        - Si isAirReflection=True : l'air entoure le milieu (marges de 20 pixels).
        - Sinon : le milieu occupe toute la grille.
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
        nx = int(np.round(width / dx))
        nz = int(np.round(height / dx))

        # Ajout des marges d'air si nécessaire
        air_margin = 20 if self.params.acoustic['medium']['isAirReflection'] else 0
        Nx, Nz = nx + 2 * air_margin, nz

        # --- 2. Initialisation des cartes (air ou milieu de fond) ---
        c_map = np.full((Nx, Nz), 343.0 if air_margin else self.params.acoustic['medium']['c0'], dtype=np.float32)
        rho_map = np.full((Nx, Nz), 1.2 if air_margin else self.params.acoustic['medium']['density'], dtype=np.float32)
        alpha_coeff_map = np.zeros((Nx, Nz), dtype=np.float32)
        BonA_map = np.zeros((Nx, Nz), dtype=np.float32)

        # --- 3. Région du milieu de fond (avec ou sans marge d'air) ---
        x_start = air_margin
        x_end = x_start + nx

        # --- 4. Génération des bulles d'air ---
        # Carte de fond (eau/gel)
        c_background = self.params.acoustic['medium']['c0']
        rho_background = self.params.acoustic['medium']['density']

        # Masque pour les bulles d'air
        bubble_mask = np.zeros((nx, nz), dtype=np.float32)
        n_bubbles = self.params.acoustic['medium'].get('n_bubbles', 50)
        min_bubble_radius = self.params.acoustic['medium'].get('min_bubble_radius', 2)
        max_bubble_radius = self.params.acoustic['medium'].get('max_bubble_radius', 5)

        for _ in range(n_bubbles):
            radius = np.random.randint(min_bubble_radius, max_bubble_radius)
            x_center = np.random.randint(radius, nx - radius)
            z_center = np.random.randint(radius, nz - radius)
            # Dessine un cercle (bulle) dans le masque
            Y, X = np.ogrid[:nx, :nz]
            dist_from_center = np.sqrt((X - x_center)**2 + (Y - z_center)**2)
            bubble_mask[dist_from_center <= radius] = 1.0

        # --- 5. Propriétés physiques ---
        # Bulles d'air : c=343 m/s, rho=1.2 kg/m³
        c_map[x_start:x_end, :] = np.where(
            bubble_mask == 1.0,
            343.0,
            c_background
        )
        rho_map[x_start:x_end, :] = np.where(
            bubble_mask == 1.0,
            1.2,
            rho_background
        )
        # Atténuation nulle dans les bulles, sinon valeur de fond
        alpha_coeff_map[x_start:x_end, :] = np.where(
            bubble_mask == 1.0,
            0.0,
            self.params.acoustic['medium'].get('alpha_coeff', 0.5)
        )
        # BonA nul dans les bulles, sinon valeur de fond
        BonA_map[x_start:x_end, :] = np.where(
            bubble_mask == 1.0,
            0.0,
            self.params.acoustic['medium'].get('BonA', 6.0)
        )

        # --- 6. Création du milieu k-Wave ---
        self.kmedium = kWaveMedium(
            sound_speed=c_map,
            density=rho_map,
            sound_speed_ref=self.params.acoustic['medium']['c0'],
            alpha_coeff=alpha_coeff_map,
            alpha_power=self.params.acoustic['medium']['alpha_power'],
            BonA=BonA_map,
            absorbing=True,
            stokes=False
        )

        self.kgrid = kWaveGrid([Nx, Nz], [dx, dx])
        dt = 1/(self.params.acoustic['f_AQ'])
        self.kgrid.setTime(self.params.general['Nt'], dt)

        # Saving variable for later use
        self.factorX = int(np.ceil(self.params.general['dx'] / dx))
        self.factorZ = self.factorX
        self.factorT = int(np.ceil((1/self.kgrid.dt) / (self.params.acoustic['f_saving'])))
        self.c_mean = np.mean(c_map[:, 0])
        self.Nx_reshaped = Nx
        self.Nz_reshaped = Nz
        self.dx_reshaped = dx
