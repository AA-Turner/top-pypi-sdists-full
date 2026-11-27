"""This is a module to handle generic GUI configuration ...

... from the global ASE configuration in ase.config or an ~/.ase/gui.py
configuration file, for backwards compatibility. The configuration is
imported when opening ASE-GUI and can then be modified at runtime, if
necessary.
"""

import ast
import runpy
import warnings
from pathlib import Path

from ase.config import ASE_CONFIG_FILE, Config, cfg

gui_default_settings = {
    'default_graphs_string': 'i, e - E[-1]',
    'foreground_color': '#000000',  # hex or named color
    'background_color': '#ffffff',  # hex or named color
    'covalent_radii': None,  # Dictionary of {atomic number/symbol: radius}
    'radii_scale': 0.89,
    'force_vector_scale': 1.0,
    'velocity_vector_scale': 1.0,
    'magmom_vector_scale': 1.0,
    'show_unit_cell': True,
    'show_axes': True,
    'show_bonds': False,
    # Performance options for large systems.  Both are no-ops for small
    # structures; see View._draw_indices().
    # Draw fewer objects while dragging/zooming:
    'interactive_level_of_detail': True,
    'occlusion_culling': True,  # skip atoms fully obscured by nearer atoms
    'shift_cell': False,
    'swap_mouse': False,
    'movie_rate': 'auto',  # float or 'auto'
    'movie_skip': 'auto',  # int or 'auto'
    'movie_rock': False,
}  # end (Marker for a literalinclude in the docs. Please do not remove)


class GUIConfig(Config):
    """For interfacing with the GUI configuration in a backwards and
    hopefully forwards compatible way. Designed to be operated like
    a ConfigParser object.
    """

    def __init__(self):
        super().__init__()

    @property
    def _parser(self):
        if self.parser.has_section('gui'):
            return self.parser['gui']
        else:
            return self.parser

    def __iter__(self):
        yield from self._parser

    def __getitem__(self, key):
        return self._parser[key]

    def __len__(self):
        return len(self._parser)

    def get(self, option, fallback=None):
        return self._parser.get(option, fallback=fallback)

    def getint(self, option, fallback=None):
        return self._parser.getint(option, fallback=fallback)

    def getfloat(self, option, fallback=None):
        return self._parser.getfloat(option, fallback=fallback)

    def getboolean(self, option, fallback=None):
        return self._parser.getboolean(option, fallback=fallback)

    def getliteral(self, option, fallback=None):
        value = self.get(option, fallback)
        if value.lower() == 'auto':
            return 'auto'
        return ast.literal_eval(value)

    def set(self, option, value):
        if not self.parser.has_section('gui'):
            self.parser.add_section('gui')
        self.parser.set('gui', option, str(value))

    def read_dict(self, dct: dict) -> None:
        self.parser.read_dict({'gui': {k: str(dct[k]) for k in dct}})

    def read_ase_config(self, config: Config) -> None:
        self.parser.read_dict(config.as_dict())


def read_defaults(
    user_cfg: GUIConfig | Config | dict | None = None,
) -> GUIConfig:
    """Retrieves configuration from ASE configuration files (see ase.config).
    Returns a GUIConfig object from which one can get the settings. If user_cfg
    is specified, parses and adapts the provided configuration instead, ignoring
    the global config.
    """
    old_configfile = Path.home() / '.ase/gui.py'
    if old_configfile.exists():
        warnings.warn(
            'Found GUI configuration file gui.py which is deprecated'
            f'. Use {ASE_CONFIG_FILE} instead.',
            FutureWarning,
        )
        runpy.run_path(
            str(old_configfile),
            init_globals={'gui_default_settings': gui_default_settings},
        )

    config = GUIConfig()
    config.read_dict(gui_default_settings)

    if user_cfg is None:
        config.read_ase_config(cfg)
    else:
        if isinstance(user_cfg, dict):
            config.read_dict(user_cfg)
        else:
            config.read_ase_config(user_cfg)

    return config
