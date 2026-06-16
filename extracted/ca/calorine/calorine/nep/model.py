import copy
from dataclasses import dataclass
from itertools import product

import numpy as np

NetworkWeights = dict[str, dict[str, np.ndarray]]
DescriptorWeights = dict[tuple[str, str], np.ndarray]
RestartParameters = dict[str, dict[str, dict[str, np.ndarray]]]


def _get_restart_contents(filename: str) -> tuple[list[float], list[float]]:
    """Parses a ``nep.restart`` file, and returns an unformatted list of the
    mean and standard deviation for all model parameters.
    Intended to be used by the py:meth:`~Model.read_restart` function.

    Parameters
    ----------
    filename
        input file name
    """
    mu = []     # Mean
    sigma = []  # Standard deviation
    with open(filename) as f:
        for k, line in enumerate(f.readlines()):
            flds = line.split()
            assert len(flds) != 0, f'Empty line number {k}'
            if len(flds) == 2:
                mu.append(float(flds[0]))
                sigma.append(float(flds[1]))
            else:
                raise IOError(f'Failed to parse line {k} from {filename}')
    return mu, sigma


def _get_model_type(first_row: list[str]) -> str:
    """Parses a the first row of a ``nep.txt`` file, and returns the
    type of NEP model. Available types are `potential`, `potential_with_charges`,
    `dipole`, and `polarizability`.

    Parameters
    ----------
    first_row
        First row of a NEP file, split by white space.
    """
    model_type = first_row[0]
    if 'charge' in model_type:
        return 'potential_with_charges'
    elif 'dipole' in model_type:
        return 'dipole'
    elif 'polarizability' in model_type:
        return 'polarizability'
    return 'potential'


def _get_nep_contents(filename: str) -> tuple[dict, list[float]]:
    """Parses a ``nep.txt`` file, and returns a dict describing the header
    and an unformatted list of all model parameters.
    Intended to be used by the :func:`read_model <calorine.nep.read_model>` function.

    Parameters
    ----------
    filename
        input file name
    """
    # parse file and split header and parameters
    header = []
    parameters = []
    nheader = 5  # 5 rows for NEP2, 6-7 rows for NEP3 onwards
    base_line = 3
    with open(filename) as f:
        for k, line in enumerate(f.readlines()):
            flds = line.split()
            assert len(flds) != 0, f'Empty line number {k}'
            if k == 0 and 'zbl' in flds[0]:
                base_line += 1
                nheader += 1
            if k == base_line and 'basis_size' in flds[0]:
                # Introduced in nep.txt after GPUMD v3.2
                nheader += 1
            if k < nheader:
                header.append(tuple(flds))
            elif len(flds) == 1:
                parameters.append(float(flds[0]))
            else:
                raise IOError(f'Failed to parse line {k} from {filename}')
    # compile data from the header into a dict
    data = {}
    for flds in header:
        if flds[0] in ['cutoff', 'zbl']:
            data[flds[0]] = tuple(map(float, flds[1:]))
        elif flds[0] in ['n_max', 'l_max', 'ANN', 'basis_size']:
            data[flds[0]] = tuple(map(int, flds[1:]))
        elif flds[0].startswith('nep'):
            version = flds[0].replace('nep', '').split('_')[0]
            version = int(version)
            data['version'] = version
            data['types'] = flds[2:]
            data['model_type'] = _get_model_type(flds)
        else:
            raise ValueError(f'Unknown field: {flds[0]}')
    return data, parameters


def _sort_descriptor_parameters(parameters: list[float],
                                types: list[str],
                                n_max_radial: int,
                                n_basis_radial: int,
                                n_max_angular: int,
                                n_basis_angular: int) -> tuple[DescriptorWeights,
                                                               DescriptorWeights]:
    """Reads a list of descriptors parameters and sorts them into two
    appropriately structured `dicts`, one for radial and one for angular descriptor weights.
    Intended to be used by the :func:`read_model <calorine.nep.read_model>` function.
    """
    # split up descriptor by chemical species and radial/angular
    n_types = len(types)
    n = len(parameters) / (n_types * n_types)
    assert n.is_integer(), 'number of descriptor groups must be an integer'
    n = int(n)

    m = (n_max_radial + 1) * (n_basis_radial + 1)
    descriptor_weights = parameters.reshape((n, n_types * n_types)).T
    descriptor_weights_radial = descriptor_weights[:, :m]
    descriptor_weights_angular = descriptor_weights[:, m:]

    # add descriptors to data dict
    radial_descriptor_weights = {}
    angular_descriptor_weights = {}
    m = -1
    for i, j in product(range(n_types), repeat=2):
        m += 1
        s1, s2 = types[i], types[j]
        radial_descriptor_weights[(s1, s2)] = descriptor_weights_radial[m, :].reshape(
            (n_max_radial + 1, n_basis_radial + 1)
        )
        angular_descriptor_weights[(s1, s2)] = descriptor_weights_angular[m, :].reshape(
            (n_max_angular + 1, n_basis_angular + 1)
        )
    return radial_descriptor_weights, angular_descriptor_weights


def _sort_ann_parameters(parameters: list[float],
                         ann_groupings: list[str],
                         n_neuron: int,
                         n_networks: int,
                         n_bias: int,
                         n_descriptor: int,
                         is_polarizability_model: bool,
                         is_model_with_charges: bool
                         ) -> NetworkWeights:
    """Reads a list of model parameters and sorts them into an appropriately structured `dict`.
    Intended to be used by the :func:`read_model <calorine.nep.read_model>` function.
    """
    n_ann_input_weights = (n_descriptor + 1) * n_neuron  # weights + bias
    n_ann_output_weights = 2*n_neuron if is_model_with_charges else n_neuron  # only weights
    n_ann_parameters = (
        n_ann_input_weights + n_ann_output_weights
    ) * n_networks + n_bias

    # Group ANN parameters
    pars = {}
    n1 = 0
    n_network_params = n_ann_input_weights + n_ann_output_weights  # except last bias(es)

    n_count = 2 if is_polarizability_model else 1
    n_outputs = 2 if is_model_with_charges else 1
    for count in range(n_count):
        # if polarizability model, all parameters including bias are repeated
        # need to offset n1 by +1 to handle bias
        n1 += count
        for s in ann_groupings:
            # Get the parameters for the ANN; in the case of NEP4, there is effectively
            # one network per atomic species.
            ann_parameters = parameters[n1 : n1 + n_network_params]
            ann_input_weights = ann_parameters[:n_ann_input_weights]
            w0 = np.zeros((n_neuron, n_descriptor))
            w0[...] = np.nan
            b0 = np.zeros((n_neuron, 1))
            b0[...] = np.nan
            for n in range(n_neuron):
                for nu in range(n_descriptor):
                    w0[n, nu] = ann_input_weights[n * n_descriptor + nu]
            b0[:, 0] = ann_input_weights[n_neuron * n_descriptor :]

            assert np.all(
                w0.shape == (n_neuron, n_descriptor)
            ), f'w0 has invalid shape for key {s}; please submit a bug report'
            assert np.all(
                b0.shape == (n_neuron, 1)
            ), f'b0 has invalid shape for key {s}; please submit a bug report'
            assert not np.any(
                np.isnan(w0)
            ), f'some weights in w0 are nan for key {s}; please submit a bug report'
            assert not np.any(
                np.isnan(b0)
            ), f'some weights in b0 are nan for key {s}; please submit a bug report'

            ann_output_weights = ann_parameters[
                n_ann_input_weights : n_ann_input_weights + n_ann_output_weights
            ]
            w1 = np.zeros((1, n_neuron * n_outputs))
            w1[0, :] = ann_output_weights[:]
            assert np.all(
                w1.shape == (1, n_neuron * n_outputs)
            ), f'w1 has invalid shape for key {s}; please submit a bug report'
            assert not np.any(
                np.isnan(w1)
            ), f'some weights in w1 are nan for key {s}; please submit a bug report'

            if count == 0 and n_outputs == 1:
                pars[s] = dict(w0=w0, b0=b0, w1=w1)
            elif count == 0 and n_outputs == 2:
                pars[s] = dict(w0=w0, b0=b0, w1=w1[0, :n_neuron], w1_charge=w1[0, n_neuron:])
            else:
                pars[s].update({'w0_polar': w0, 'b0_polar': b0, 'w1_polar': w1})
            # Jump to bias
            n1 += n_network_params
            if n_bias > 1 and not is_model_with_charges:
                # For NEP5 models we additionally have one bias term per species.
                # Currently NEP5 only exists for potential models, but we'll
                # keep it here in case it gets added down the line.
                bias_label = 'b1' if count == 0 else 'b1_polar'
                pars[s][bias_label] = parameters[n1]
                n1 += 1
        # For NEP3 and NEP4 we only have one bias.
        # For NEP4 with charges we have two biases.
        # For NEP5 we have one bias per species, and one global.
        if count == 0 and n_outputs == 1:
            pars['b1'] = parameters[n1]
        elif count == 0 and n_outputs == 2:
            pars['sqrt_epsilon_infinity'] = parameters[n1]
            pars['b1'] = parameters[n1+1]
        else:
            pars['b1_polar'] = parameters[n1]
    sum = 0
    for s in pars.keys():
        if s.startswith('b1') or s.startswith('sqrt'):
            sum += 1
        else:
            sum += np.sum([np.array(p).size for p in pars[s].values()])
    assert sum == n_ann_parameters * n_count, (
        'Inconsistent number of parameters accounted for; please submit a bug report\n'
        f'{sum} != {n_ann_parameters}'
    )
    return pars


def _adaptive_sigma(mu_arr, sigma_factor: float, sigma_floor: float) -> np.ndarray:
    """Return adaptive SNES sigma: ``max(sigma_floor, sigma_factor * |mu|)``."""
    return np.maximum(sigma_floor, sigma_factor * np.abs(mu_arr))


def _apply_adaptive_sigma_to_restart(restart_params, keys, sigma_factor, sigma_floor):
    """Apply adaptive SNES sigma to every parameter in *restart_params* in-place.

    Covers per-species ANN weights (w0, b0, w1, optional w1_charge), the global b1
    scalar, the optional sqrt_epsilon_infinity scalar, and all radial/angular descriptor
    weight pairs. *keys* is the list of per-species ANN keys to update.
    """
    for s in keys:
        ann_mu = restart_params['ann_mu'][s]
        ann_sigma = restart_params['ann_sigma'][s]
        ann_sigma['w0'] = _adaptive_sigma(ann_mu['w0'], sigma_factor, sigma_floor)
        ann_sigma['b0'] = _adaptive_sigma(ann_mu['b0'], sigma_factor, sigma_floor)
        ann_sigma['w1'] = _adaptive_sigma(ann_mu['w1'], sigma_factor, sigma_floor)
        if 'w1_charge' in ann_mu:
            ann_sigma['w1_charge'] = _adaptive_sigma(
                ann_mu['w1_charge'], sigma_factor, sigma_floor
            )
    b1_mu = restart_params['ann_mu']['b1']
    restart_params['ann_sigma']['b1'] = float(_adaptive_sigma(b1_mu, sigma_factor, sigma_floor))
    if 'sqrt_epsilon_infinity' in restart_params['ann_mu']:
        sei_mu = restart_params['ann_mu']['sqrt_epsilon_infinity']
        restart_params['ann_sigma']['sqrt_epsilon_infinity'] = float(
            _adaptive_sigma(sei_mu, sigma_factor, sigma_floor)
        )
    for desc_type in ['radial', 'angular']:
        sigma_key = f'{desc_type}_descriptor_sigma'
        mu_key = f'{desc_type}_descriptor_mu'
        for pair in restart_params[sigma_key]:
            restart_params[sigma_key][pair] = _adaptive_sigma(
                restart_params[mu_key][pair], sigma_factor, sigma_floor
            )


def _recalculate_parameter_counts(new) -> None:
    """Recompute n_ann_parameters, n_descriptor_parameters, and n_parameters on *new*.

    Reads all architectural state from *new* directly, so callers must update
    new.n_neuron, new.n_descriptor_radial/angular, new.model_type, and new.types
    before calling this function.
    """
    n_types = len(new.types)
    n_desc = new.n_descriptor_radial + new.n_descriptor_angular
    is_charged = new.model_type == 'potential_with_charges'
    n_networks = n_types if new.version in (4, 5) else 1
    n_bias = 2 if is_charged else (1 + n_types if new.version == 5 else 1)
    n_ann_input_weights = (n_desc + 1) * new.n_neuron
    n_ann_output_weights = 2 * new.n_neuron if is_charged else new.n_neuron
    new.n_ann_parameters = (n_ann_input_weights + n_ann_output_weights) * n_networks + n_bias
    new.n_descriptor_parameters = n_types ** 2 * (
        (new.n_max_radial + 1) * (new.n_basis_radial + 1)
        + (new.n_max_angular + 1) * (new.n_basis_angular + 1)
    )
    new.n_parameters = new.n_ann_parameters + new.n_descriptor_parameters + n_desc
    if new.model_type == 'polarizability':
        new.n_parameters += new.n_ann_parameters


@dataclass
class Model:
    r"""Objects of this class represent a NEP model in a form suitable for
    inspection and manipulation. Typically a :class:`Model` object is instantiated
    by calling the :func:`read_model <calorine.nep.read_model>` function.

    Attributes
    ----------
    version : int
        NEP version.
    model_type: str
        One of ``potential``, ``dipole`` or ``polarizability``.
    types : tuple[str, ...]
        Chemical species that this model represents.
    radial_cutoff : float | list[float]
        The radial cutoff parameter in Å.
        Is a list of radial cutoffs ordered after ``types`` in the case of typewise cutoffs.
    angular_cutoff : float | list[float]
        The angular cutoff parameter in Å.
        Is a list of angular cutoffs ordered after ``types`` in the case of typewise cutoffs.
    max_neighbors_radial : int
        Maximum number of neighbors in neighbor list for radial terms.
    max_neighbors_angular : int
        Maximum number of neighbors in neighbor list for angular terms.
    radial_typewise_cutoff_factor : float
        The radial cutoff factor if use_typewise_cutoff is used.
    angular_typewise_cutoff_factor : float
        The angular cutoff factor if use_typewise_cutoff is used.
    zbl : tuple[float, float]
        Inner and outer cutoff for transition to ZBL potential.
    zbl_typewise_cutoff_factor : float
        Typewise cutoff when use_typewise_cutoff_zbl is used.
    n_basis_radial : int
        Number of radial basis functions :math:`n_\mathrm{basis}^\mathrm{R}`.
    n_basis_angular : int
        Number of angular basis functions :math:`n_\mathrm{basis}^\mathrm{A}`.
    n_max_radial : int
        Maximum order of Chebyshev polymonials included in
        radial expansion :math:`n_\mathrm{max}^\mathrm{R}`.
    n_max_angular : int
        Maximum order of Chebyshev polymonials included in
        angular expansion :math:`n_\mathrm{max}^\mathrm{A}`.
    l_max_3b : int
        Maximum expansion order for three-body terms :math:`l_\mathrm{max}^\mathrm{3b}`.
    l_max_4b : int
        Maximum expansion order for four-body terms :math:`l_\mathrm{max}^\mathrm{4b}`.
    l_max_5b : int
        Maximum expansion order for five-body terms :math:`l_\mathrm{max}^\mathrm{5b}`.
    has_q_112 : int
        Flag enabling the 5-body :math:`q_{112}` descriptor (0 or 1).
    has_q_123 : int
        Flag enabling the 5-body :math:`q_{123}` descriptor (0 or 1).
    has_q_233 : int
        Flag enabling the 5-body :math:`q_{233}` descriptor (0 or 1).
    has_q_134 : int
        Flag enabling the higher-body :math:`q_{134}` descriptor (0 or 1).
    n_descriptor_radial : int
        Dimension of radial part of descriptor.
    n_descriptor_angular : int
        Dimension of angular part of descriptor.
    n_neuron : int
        Number of neurons in hidden layer.
    n_parameters : int
        Total number of parameters including scalers (which are not fit parameters).
    n_descriptor_parameters : int
        Number of parameters in descriptor.
    n_ann_parameters : int
        Number of neural network weights.
    ann_parameters : dict[tuple[str, dict[str, np.darray]]]
        Neural network weights.
    q_scaler : List[float]
        Scaling parameters.
    radial_descriptor_weights : dict[tuple[str, str], np.ndarray]
        Radial descriptor weights by combination of species; the array for each combination
        has dimensions of
        :math:`(n_\mathrm{max}^\mathrm{R}+1) \times (n_\mathrm{basis}^\mathrm{R}+1)`.
    angular_descriptor_weights : dict[tuple[str, str], np.ndarray]
        Angular descriptor weights by combination of species; the array for each combination
        has dimensions of
        :math:`(n_\mathrm{max}^\mathrm{A}+1) \times (n_\mathrm{basis}^\mathrm{A}+1)`.
    sqrt_epsilon_infinity : Optional[float]
        Square root of epsilon infinity $\epsilon_\infty$ (only for NEP models with charges).
    restart_parameters :  dict[str, dict[str, dict[str, np.ndarray]]]
        NEP restart parameters. A nested dictionary that contains the mean (mu) and standard
        deviation (sigma) for the ANN and descriptor parameters. Is set using the
        py:meth:`~Model.read_restart` method. Defaults to None.
    """

    version: int
    model_type: str
    types: tuple[str, ...]

    radial_cutoff: float | list[float]
    angular_cutoff: float | list[float]

    n_basis_radial: int
    n_basis_angular: int
    n_max_radial: int
    n_max_angular: int
    l_max_3b: int
    l_max_4b: int
    l_max_5b: int
    has_q_112: int
    has_q_123: int
    has_q_233: int
    has_q_134: int
    n_descriptor_radial: int
    n_descriptor_angular: int

    n_neuron: int
    n_parameters: int
    n_descriptor_parameters: int
    n_ann_parameters: int
    ann_parameters: NetworkWeights
    q_scaler: list[float]
    radial_descriptor_weights: DescriptorWeights
    angular_descriptor_weights: DescriptorWeights
    sqrt_epsilon_infinity: float = None
    restart_parameters: RestartParameters = None

    zbl: tuple[float, float] = None
    zbl_typewise_cutoff_factor: float = None
    max_neighbors_radial: int = None
    max_neighbors_angular: int = None
    radial_typewise_cutoff_factor: float = None
    angular_typewise_cutoff_factor: float = None

    _special_fields = [
        'ann_parameters',
        'q_scaler',
        'radial_descriptor_weights',
        'angular_descriptor_weights',
    ]

    def __str__(self) -> str:
        s = []
        for fld in self.__dataclass_fields__:
            if fld not in self._special_fields:
                value = getattr(self, fld)
                if fld == 'restart_parameters':
                    value = 'available' if value is not None else 'not available'
                s += [f'{fld:22} : {value}']
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        s = []
        s += ['<table border="1" class="dataframe"']
        s += [
            '<thead><tr><th style="text-align: left;">Field</th><th>Value</th></tr></thead>'
        ]
        s += ['<tbody>']
        for fld in self.__dataclass_fields__:
            if fld not in self._special_fields:
                value = getattr(self, fld)
                if fld == 'restart_parameters':
                    value = 'available' if value is not None else 'not available'
                s += [
                    f'<tr><td style="text-align: left;">{fld:22}</td>'
                    f'<td>{value}</td><tr>'
                ]
        for fld in self._special_fields:
            d = getattr(self, fld)
            # print('xxx', fld, d)
            if fld.endswith('descriptor_weights'):
                dim = list(d.values())[0].shape
            elif fld == 'ann_parameters' and self.version == 4:
                dim = (len(self.types), len(list(d.values())[0]))
            else:
                dim = len(d)
            s += [
                f'<tr><td style="text-align: left;">Dimension of {fld:22}</td><td>{dim}</td><tr>'
            ]
        s += ['</tbody>']
        s += ['</table>']
        return ''.join(s)

    @property
    def training_parameters(self) -> dict:
        """Return model hyperparameters in the format accepted by :func:`write_nepfile
        <calorine.nep.write_nepfile>`.

        Use this after any model modification (:meth:`augment`, :meth:`add_species`,
        :meth:`remove_species`, :meth:`keep_species`) to produce the architecture fields
        that must go into the new ``nep.in`` before training. Merge the result with your
        existing training-specific parameters (``lambda_*``, ``generation``, ``batch``,
        etc.) before calling :func:`write_nepfile <calorine.nep.write_nepfile>`.

        Returns
        -------
        dict
            Keys ``version``, ``type``, ``cutoff``, ``n_max``, ``basis_size``, ``l_max``,
            and ``neuron`` (plus ``zbl`` when applicable) with values in the format
            expected by :func:`write_nepfile <calorine.nep.write_nepfile>`.

        """
        l_max = [self.l_max_3b, self.l_max_4b, self.l_max_5b,
                 self.has_q_112, self.has_q_123, self.has_q_233, self.has_q_134]
        while len(l_max) > 1 and l_max[-1] == 0:
            l_max = l_max[:-1]

        if isinstance(self.radial_cutoff, list):
            cutoff = []
            for rc, ac in zip(self.radial_cutoff, self.angular_cutoff):
                cutoff += [rc, ac]
        else:
            cutoff = [self.radial_cutoff, self.angular_cutoff]

        params = {
            'version': self.version,
            'type': [len(self.types)] + list(self.types),
            'cutoff': cutoff,
            'n_max': [self.n_max_radial, self.n_max_angular],
            'basis_size': [self.n_basis_radial, self.n_basis_angular],
            'l_max': l_max,
            'neuron': self.n_neuron,
        }
        if self.zbl is not None:
            params['zbl'] = list(self.zbl)
        return params

    def remove_species(self,
                       species: list[str],
                       sigma_factor: float = 0.1,
                       sigma_floor: float = 1e-6) -> 'Model':
        """Remove one or more species from the model.

        Returns a new :class:`Model` with the specified species removed.
        The source model is not modified.

        If ``restart_parameters`` are loaded, the surviving parameters receive
        adaptive SNES sigma values: ``sigma = max(sigma_floor, sigma_factor * |mu|)``,
        re-opening the search distribution while preserving dormant parameters.

        Parameters
        ----------
        species
            Species names to remove.
        sigma_factor
            Used only when restart is loaded: ``sigma = max(sigma_floor, sigma_factor * |mu|)``
            for surviving parameters.
        sigma_floor
            Minimum sigma for surviving parameters when restart is loaded.

        Returns
        -------
        Model
            New model with the specified species removed.

        Raises
        ------
        ValueError
            If any of the provided species is not found in the model.
        """
        for s in species:
            if s not in self.types:
                raise ValueError(f'{s} is not a species supported by the NEP model')

        new = copy.deepcopy(self)
        types_to_keep = [t for t in self.types if t not in species]
        new.types = tuple(types_to_keep)

        # Prune ANN parameters (for NEP4 and NEP5)
        if self.version in [4, 5]:
            new.ann_parameters = {
                key: value for key, value in new.ann_parameters.items()
                if key in types_to_keep or key.startswith('b1')
            }

        # Prune descriptor weights; key is a (species1, species2) tuple
        new.radial_descriptor_weights = {
            key: value for key, value in new.radial_descriptor_weights.items()
            if key[0] in types_to_keep and key[1] in types_to_keep
        }
        new.angular_descriptor_weights = {
            key: value for key, value in new.angular_descriptor_weights.items()
            if key[0] in types_to_keep and key[1] in types_to_keep
        }

        # Prune typewise cutoff lists so remaining species map to correct cutoffs
        if isinstance(self.radial_cutoff, list):
            indices = [i for i, t in enumerate(self.types) if t not in species]
            new.radial_cutoff = [self.radial_cutoff[i] for i in indices]
            new.angular_cutoff = [self.angular_cutoff[i] for i in indices]

        # Prune and optionally re-open restart parameters
        if new.restart_parameters is not None:
            ann_keys = types_to_keep if self.version in [4, 5] else ['all_species']
            for param_type in ['mu', 'sigma']:
                ann_key = f'ann_{param_type}'
                if self.version in [4, 5]:
                    # Keep per-species keys for survivors, global bias keys, and
                    # sqrt_epsilon_infinity (charge models)
                    new.restart_parameters[ann_key] = {
                        key: value for key, value in new.restart_parameters[ann_key].items()
                        if (key in types_to_keep or key.startswith('b1')
                            or key == 'sqrt_epsilon_infinity')
                    }

                # Prune descriptor restart parameters
                for desc_type in ['radial', 'angular']:
                    key = f'{desc_type}_descriptor_{param_type}'
                    new.restart_parameters[key] = {
                        k: v for k, v in new.restart_parameters[key].items()
                        if k[0] in types_to_keep and k[1] in types_to_keep
                    }

            # Apply adaptive sigma to all surviving parameters
            _apply_adaptive_sigma_to_restart(
                new.restart_parameters, ann_keys, sigma_factor, sigma_floor
            )

        # Recalculate parameter counts
        _recalculate_parameter_counts(new)

        return new

    def keep_species(self,
                     species: list[str],
                     sigma_factor: float = 0.1,
                     sigma_floor: float = 1e-6) -> 'Model':
        """Retain only the specified species, removing all others.

        Convenience complement to :meth:`remove_species`. Useful when the set
        of species to drop is large (e.g. isolating two elements from a
        foundation model with dozens of species).

        Parameters
        ----------
        species
            Species names to keep. All other species are removed.
        sigma_factor
            Passed to :meth:`remove_species`. Controls adaptive sigma for
            surviving parameters when restart is loaded.
        sigma_floor
            Passed to :meth:`remove_species`. Minimum sigma for surviving
            parameters.

        Returns
        -------
        Model
            New model containing only the requested species.

        Raises
        ------
        ValueError
            If any of the requested species is not in the model.
        """
        unknown = [s for s in species if s not in self.types]
        if unknown:
            raise ValueError(
                f'Species not in model: {unknown}'
            )
        to_remove = [s for s in self.types if s not in species]
        return self.remove_species(to_remove, sigma_factor=sigma_factor, sigma_floor=sigma_floor)

    def add_species(self,
                    species: list[str],
                    radial_cutoff: float | list[float] = None,
                    angular_cutoff: float | list[float] = None,
                    sigma_new: float = 0.1,
                    sigma_factor: float = 0.1,
                    sigma_floor: float = 1e-6,
                    seed: int | None = None) -> 'Model':
        """Add one or more species to the model.

        Returns a new :class:`Model` with the requested species added. New ANN
        sub-networks and descriptor weight pairs are initialised by drawing
        ``mu`` uniformly from [-1, 1] (matching the GPUMD fresh-model
        initialisation), with ``sigma = sigma_new`` in the restart.
        Charge-specific parameters (``w1_charge``) are kept at ``mu = 0`` to
        preserve stability, also matching GPUMD.
        Existing parameters receive adaptive sigma:
        ``sigma = max(sigma_floor, sigma_factor * |mu|)``.

        Only supported for NEP4 models. For NEP3 the ANN is shared across all
        species and adding a per-species sub-network is not meaningful.

        Parameters
        ----------
        species
            New species names to add. Appended to ``types`` in the order given.
        radial_cutoff
            Radial cutoff(s) for the new species, in Å. Required when the model
            uses typewise cutoffs (i.e. ``isinstance(model.radial_cutoff, list)``
            is ``True``). Pass a single float or a list with one value per new
            species.
        angular_cutoff
            Angular cutoff(s) for the new species, in Å. Same requirements as
            ``radial_cutoff``.
        sigma_new
            SNES sigma assigned to all newly created parameters. Defaults to
            ``0.1``, matching the GPUMD ``sigma0`` default.
        sigma_factor
            Controls sigma for *existing* parameters:
            ``sigma = max(sigma_floor, sigma_factor * |mu|)``.
        sigma_floor
            Minimum sigma for existing parameters.
        seed
            Seed for the random number generator used to draw the initial ``mu``
            values. Pass an integer for reproducible initialisation.

        Returns
        -------
        Model
            New model with updated structure, weights, and restart statistics.

        Raises
        ------
        ValueError
            If the model version is not 4, if ``restart_parameters`` are not
            loaded, if any species is already in the model, or if typewise
            cutoffs are used and ``radial_cutoff``/``angular_cutoff`` are not
            provided.
        """
        if self.version != 4:
            raise ValueError(
                f'add_species() only supports NEP4 models; got version {self.version}.'
            )
        for s in species:
            if s in self.types:
                raise ValueError(f'{s!r} is already in the model.')
        if self.restart_parameters is None:
            raise ValueError(
                'restart_parameters must be loaded before calling add_species(). '
                'Pass restart_file= to read_model() or call model.read_restart() first.'
            )

        uses_typewise = isinstance(self.radial_cutoff, list)
        if uses_typewise:
            if radial_cutoff is None or angular_cutoff is None:
                raise ValueError(
                    'Model uses typewise cutoffs; provide radial_cutoff and angular_cutoff '
                    'for the new species.'
                )
            rc_list = ([radial_cutoff] * len(species)
                       if isinstance(radial_cutoff, (int, float)) else list(radial_cutoff))
            ac_list = ([angular_cutoff] * len(species)
                       if isinstance(angular_cutoff, (int, float)) else list(angular_cutoff))
            if len(rc_list) != len(species) or len(ac_list) != len(species):
                raise ValueError(
                    'Length of radial_cutoff/angular_cutoff must match the number of new species.'
                )

        new = copy.deepcopy(self)

        n_descriptor = self.n_descriptor_radial + self.n_descriptor_angular
        n_neuron = self.n_neuron
        is_charged = self.model_type == 'potential_with_charges'
        all_types_after = list(self.types) + list(species)
        rng = np.random.default_rng(seed)

        def _rand(shape):
            return rng.uniform(-1.0, 1.0, size=shape)

        # Step 1: Adaptive sigma for existing parameters
        _apply_adaptive_sigma_to_restart(
            new.restart_parameters, list(self.types), sigma_factor, sigma_floor
        )

        # Step 2: New ANN sub-networks
        w1_shape = (n_neuron,) if is_charged else (1, n_neuron)
        for s_new in species:
            w0_vals = _rand((n_neuron, n_descriptor))
            b0_vals = _rand((n_neuron, 1))
            w1_vals = _rand(w1_shape)
            s_params = {'w0': w0_vals.copy(), 'b0': b0_vals.copy(), 'w1': w1_vals.copy()}
            if is_charged:
                s_params['w1_charge'] = np.zeros(n_neuron)
            new.ann_parameters[s_new] = s_params

            mu_entry = {'w0': w0_vals, 'b0': b0_vals, 'w1': w1_vals}
            sigma_entry = {
                'w0': np.full((n_neuron, n_descriptor), sigma_new),
                'b0': np.full((n_neuron, 1), sigma_new),
                'w1': np.full(w1_shape, sigma_new),
            }
            if is_charged:
                mu_entry['w1_charge'] = np.zeros(n_neuron)
                sigma_entry['w1_charge'] = np.full(n_neuron, sigma_new)
            new.restart_parameters['ann_mu'][s_new] = mu_entry
            new.restart_parameters['ann_sigma'][s_new] = sigma_entry

        # Step 3: New descriptor weight pairs
        n_r = (self.n_max_radial + 1, self.n_basis_radial + 1)
        n_a = (self.n_max_angular + 1, self.n_basis_angular + 1)
        existing_pairs = set(self.radial_descriptor_weights)
        new_pairs = {
            (s1, s2)
            for s1 in all_types_after for s2 in all_types_after
            if (s1, s2) not in existing_pairs
        }
        for pair in new_pairs:
            r_vals = _rand(n_r)
            a_vals = _rand(n_a)
            new.radial_descriptor_weights[pair] = r_vals.copy()
            new.angular_descriptor_weights[pair] = a_vals.copy()
            new.restart_parameters['radial_descriptor_mu'][pair] = r_vals
            new.restart_parameters['angular_descriptor_mu'][pair] = a_vals
            new.restart_parameters['radial_descriptor_sigma'][pair] = np.full(n_r, sigma_new)
            new.restart_parameters['angular_descriptor_sigma'][pair] = np.full(n_a, sigma_new)

        # Step 4: Update types and typewise cutoffs
        new.types = tuple(all_types_after)
        if uses_typewise:
            new.radial_cutoff = list(self.radial_cutoff) + rc_list
            new.angular_cutoff = list(self.angular_cutoff) + ac_list

        # Step 5: Recalculate parameter counts
        _recalculate_parameter_counts(new)

        return new

    def write(self, filename: str, restart_file: str = None) -> None:
        """Write NEP model to file in `nep.txt` format.

        Parameters
        ----------
        filename
            Output file name for the NEP model.
        restart_file
            If provided, also write restart parameters to this file in
            `nep.restart` format. Defaults to None.
        """
        with open(filename, 'w') as f:
            # header
            version_name = f'nep{self.version}'
            if self.zbl is not None:
                version_name += '_zbl'
            elif self.model_type != 'potential':
                version_name += f'_{self.model_type}'
            f.write(f'{version_name} {len(self.types)} {" ".join(self.types)}\n')
            if self.zbl is not None:
                f.write(f'zbl {" ".join(map(str, self.zbl))}\n')
            f.write('cutoff')
            if isinstance(self.radial_cutoff, float) and isinstance(self.angular_cutoff, float):
                f.write(f' {self.radial_cutoff} {self.angular_cutoff}')
            else:
                # Typewise cutoffs: one set of cutoffs per type
                for i in range(len(self.types)):
                    f.write(f' {self.radial_cutoff[i]} {self.angular_cutoff[i]}')
            f.write(f' {self.max_neighbors_radial} {self.max_neighbors_angular}')
            f.write('\n')
            f.write(f'n_max {self.n_max_radial} {self.n_max_angular}\n')
            f.write(f'basis_size {self.n_basis_radial} {self.n_basis_angular}\n')
            l_max_line = f'l_max {self.l_max_3b} {self.l_max_4b} {self.l_max_5b}'
            if self.has_q_112 or self.has_q_123 or self.has_q_233 or self.has_q_134:
                l_max_line += f' {self.has_q_112}'
            if self.has_q_123 or self.has_q_233 or self.has_q_134:
                l_max_line += f' {self.has_q_123}'
            if self.has_q_233 or self.has_q_134:
                l_max_line += f' {self.has_q_233}'
            if self.has_q_134:
                l_max_line += f' {self.has_q_134}'
            f.write(l_max_line + '\n')
            f.write(f'ANN {self.n_neuron} 0\n')

            # neural network weights
            keys = self.types if self.version in (4, 5) else ['all_species']
            suffixes = ['', '_polar'] if self.model_type == 'polarizability' else ['']
            for suffix in suffixes:
                for s in keys:
                    # Order: w0, b0, w1 (, b1 if NEP5)
                    # w0 indexed as: n*N_descriptor + nu
                    w0 = self.ann_parameters[s][f'w0{suffix}']
                    b0 = self.ann_parameters[s][f'b0{suffix}']
                    w1 = self.ann_parameters[s][f'w1{suffix}']
                    for n in range(self.n_neuron):
                        for nu in range(
                            self.n_descriptor_radial + self.n_descriptor_angular
                        ):
                            f.write(f'{w0[n, nu]:15.7e}\n')
                    for b in b0[:, 0]:
                        f.write(f'{b:15.7e}\n')
                    for v in (w1[0, :] if w1.ndim == 2 else w1):
                        f.write(f'{v:15.7e}\n')
                    if f'w1_charge{suffix}' in self.ann_parameters[s]:
                        for v in self.ann_parameters[s][f'w1_charge{suffix}']:
                            f.write(f'{v:15.7e}\n')
                    if self.version == 5:
                        b1 = self.ann_parameters[s][f'b1{suffix}']
                        f.write(f'{b1:15.7e}\n')
                if self.sqrt_epsilon_infinity is not None:
                    f.write(f'{self.sqrt_epsilon_infinity:15.7e}\n')
                b1 = self.ann_parameters[f'b1{suffix}']
                f.write(f'{b1:15.7e}\n')

            # descriptor weights
            mat = []
            for s1 in self.types:
                for s2 in self.types:
                    mat = np.hstack(
                        [mat, self.radial_descriptor_weights[(s1, s2)].flatten()]
                    )
                    mat = np.hstack(
                        [mat, self.angular_descriptor_weights[(s1, s2)].flatten()]
                    )
            n_types = len(self.types)
            n = int(len(mat) / (n_types * n_types))
            mat = mat.reshape((n_types * n_types, n)).T
            for v in mat.flatten():
                f.write(f'{v:15.7e}\n')

            # scaler
            for v in self.q_scaler:
                f.write(f'{v:15.7e}\n')

        if restart_file is not None:
            self.write_restart(restart_file)

    def read_restart(self, filename: str):
        """Parses a file in `nep.restart` format and saves the
        content in the form of mean and standard deviation for each
        parameter in the corresponding NEP model.

        Parameters
        ----------
        filename
            Input file name.
        """
        mu, sigma = _get_restart_contents(filename)
        restart_parameters = np.array([mu, sigma]).T

        is_polarizability_model = self.model_type == 'polarizability'
        is_charged_model = self.model_type == 'potential_with_charges'

        n1 = self.n_ann_parameters
        n1 *= 2 if is_polarizability_model else 1
        n2 = n1 + self.n_descriptor_parameters
        ann_parameters = restart_parameters[:n1]
        descriptor_parameters = np.array(restart_parameters[n1:n2])

        if self.version == 3:
            n_networks = 1
            n_bias = 1
        elif self.version == 4:
            # one hidden layer per atomic species
            n_networks = len(self.types)
            n_bias = 1
        else:
            raise ValueError(f'Cannot load nep.restart for NEP model version {self.version}')

        ann_groups = [s for s in self.ann_parameters.keys() if not s.startswith('b1')]
        n_bias = len([s for s in self.ann_parameters.keys() if s.startswith('b1')])
        if self.sqrt_epsilon_infinity is not None:
            n_bias += 1  # charge models have sqrt_epsilon_infinity before b1
        n_descriptor = self.n_descriptor_radial + self.n_descriptor_angular
        restart = {}

        for i, content_type in enumerate(['mu', 'sigma']):
            ann = _sort_ann_parameters(ann_parameters[:, i],
                                       ann_groups,
                                       self.n_neuron,
                                       n_networks,
                                       n_bias,
                                       n_descriptor,
                                       is_polarizability_model,
                                       is_charged_model)
            radial, angular = _sort_descriptor_parameters(descriptor_parameters[:, i],
                                                          self.types,
                                                          self.n_max_radial,
                                                          self.n_basis_radial,
                                                          self.n_max_angular,
                                                          self.n_basis_angular)

            restart[f'ann_{content_type}'] = ann
            restart[f'radial_descriptor_{content_type}'] = radial
            restart[f'angular_descriptor_{content_type}'] = angular
        self.restart_parameters = restart

    def write_restart(self, filename: str):
        """Write NEP restart parameters to file in `nep.restart` format."""
        keys = self.types if self.version in (4, 5) else ['all_species']
        suffixes = ['', '_polar'] if self.model_type == 'polarizability' else ['']
        columns = []
        for i, parameter in enumerate(['mu', 'sigma']):
            # neural network weights
            ann_parameters = self.restart_parameters[f'ann_{parameter}']
            column = []
            for suffix in suffixes:
                for s in keys:
                    # Order: w0, b0, w1 (, b1 if NEP5)
                    # w0 indexed as: n*N_descriptor + nu
                    w0 = ann_parameters[s][f'w0{suffix}']
                    b0 = ann_parameters[s][f'b0{suffix}']
                    w1 = ann_parameters[s][f'w1{suffix}']
                    for n in range(self.n_neuron):
                        for nu in range(
                            self.n_descriptor_radial + self.n_descriptor_angular
                        ):
                            column.append(f'{w0[n, nu]:15.7e}')
                    for b in b0[:, 0]:
                        column.append(f'{b:15.7e}')
                    for v in (w1[0, :] if w1.ndim == 2 else w1):
                        column.append(f'{v:15.7e}')
                    if f'w1_charge{suffix}' in ann_parameters[s]:
                        for v in ann_parameters[s][f'w1_charge{suffix}']:
                            column.append(f'{v:15.7e}')
                if f'sqrt_epsilon_infinity{suffix}' in ann_parameters:
                    column.append(f'{ann_parameters[f"sqrt_epsilon_infinity{suffix}"]:15.7e}')
                b1 = ann_parameters[f'b1{suffix}']
                column.append(f'{b1:15.7e}')
            columns.append(column)

            # descriptor weights
            radial_descriptor_parameters = self.restart_parameters[f'radial_descriptor_{parameter}']
            angular_descriptor_parameters = self.restart_parameters[
                    f'angular_descriptor_{parameter}']
            mat = []
            for s1 in self.types:
                for s2 in self.types:
                    mat = np.hstack(
                        [mat, radial_descriptor_parameters[(s1, s2)].flatten()]
                    )
                    mat = np.hstack(
                        [mat, angular_descriptor_parameters[(s1, s2)].flatten()]
                    )
            n_types = len(self.types)
            n = int(len(mat) / (n_types * n_types))
            mat = mat.reshape((n_types * n_types, n)).T
            for v in mat.flatten():
                column.append(f'{v:15.7e}')

        # Join the mean and standard deviation columns
        assert len(columns[0]) == len(columns[1]), 'Length of means must match standard deviation'
        joined = [f'{s1} {s2}\n' for s1, s2 in zip(*columns)]
        with open(filename, 'w') as f:
            f.writelines(joined)

    def augment(self,
                n_neuron: int = None,
                l_max_4b: int = None,
                l_max_5b: int = None,
                has_q_112: bool = None,
                has_q_123: bool = None,
                has_q_233: bool = None,
                has_q_134: bool = None,
                charge_head: bool = False,
                sigma_new: float = 0.01,
                sigma_factor: float = 0.1,
                sigma_floor: float = 1e-6) -> 'Model':
        """Augment the model by adding neurons, descriptor terms, or a charge output head.

        Returns a new :class:`Model` with the requested structural changes applied.
        The source model is not modified. Existing parameter values are preserved exactly;
        new parameters are initialized to zero. The restart SNES statistics are updated
        as follows:

        - Existing parameters: ``sigma = max(sigma_floor, sigma_factor * |mu|)``, which
          re-opens the SNES search distribution while keeping parameters that were driven
          toward zero effectively dormant.
        - New parameters: ``mu = 0``, ``sigma = sigma_new``.

        Parameters
        ----------
        n_neuron
            Target neuron count; must be >= current. ``None`` leaves unchanged.
        l_max_4b
            Target 4-body l_max value; must be >= current. ``None`` leaves unchanged.
        l_max_5b
            Target 5-body l_max value; must be >= current. ``None`` leaves unchanged.
        has_q_112
            ``True`` enables the q_112 5-body descriptor; ``None`` or ``False`` leaves
            the current state unchanged (disabling an already-enabled term raises).
        has_q_123
            Same as ``has_q_112`` but for the q_123 term.
        has_q_233
            Same as ``has_q_112`` but for the q_233 term.
        has_q_134
            Same as ``has_q_112`` but for the q_134 term.
        charge_head
            If ``True``, promote a ``potential`` model to ``potential_with_charges`` by
            adding a charge output head (w1_charge per species and sqrt_epsilon_infinity).
        sigma_new
            SNES sigma assigned to all newly created parameters.
        sigma_factor
            Controls the sigma for *existing* parameters:
            ``sigma = max(sigma_floor, sigma_factor * |mu|)``.
        sigma_floor
            Minimum sigma for existing parameters; keeps near-zero (dormant) parameters
            from being accidentally re-activated.

        Returns
        -------
        Model
            New model with updated structure, weights, and restart statistics.

        Raises
        ------
        ValueError
            If ``restart_parameters`` is not loaded, if ``n_neuron`` or an ``l_max_*``
            target is smaller than the current value, if a ``has_q_*`` flag attempts to
            disable an already-enabled term, or if ``charge_head=True`` on a model that
            is not of type ``potential``.
        """
        # Structural checks (independent of restart)
        if self.version not in (3, 4):
            raise ValueError(
                f'augment() only supports NEP versions 3 and 4; got version {self.version}.'
            )
        if n_neuron is not None and n_neuron < self.n_neuron:
            raise ValueError(
                f'n_neuron ({n_neuron}) must be >= current n_neuron ({self.n_neuron}); '
                'use prune() to reduce.'
            )
        if l_max_4b is not None and l_max_4b < self.l_max_4b:
            raise ValueError(
                f'l_max_4b ({l_max_4b}) must be >= current l_max_4b ({self.l_max_4b}); '
                'use prune() to disable.'
            )
        if l_max_5b is not None and l_max_5b < self.l_max_5b:
            raise ValueError(
                f'l_max_5b ({l_max_5b}) must be >= current l_max_5b ({self.l_max_5b}); '
                'use prune() to disable.'
            )
        for flag_val, name in [
            (has_q_112, 'has_q_112'), (has_q_123, 'has_q_123'), (has_q_233, 'has_q_233'),
            (has_q_134, 'has_q_134')
        ]:
            if flag_val is False and getattr(self, name):
                raise ValueError(
                    f'Cannot disable {name} via augment(); '
                    'use prune() to disable descriptor terms.'
                )
        if charge_head and self.model_type != 'potential':
            raise ValueError(
                f'charge_head=True requires model_type="potential"; '
                f'got "{self.model_type}".'
            )
        if self.restart_parameters is None:
            raise ValueError(
                'restart_parameters must be loaded before calling augment(). '
                'Pass restart_file= to read_model() or call model.read_restart() first.'
            )

        new = copy.deepcopy(self)

        # Resolve new structural parameters
        new_l_max_4b = l_max_4b if l_max_4b is not None else self.l_max_4b
        new_l_max_5b = l_max_5b if l_max_5b is not None else self.l_max_5b
        new_has_q_112 = int(has_q_112) if has_q_112 is not None else self.has_q_112
        new_has_q_123 = int(has_q_123) if has_q_123 is not None else self.has_q_123
        new_has_q_233 = int(has_q_233) if has_q_233 is not None else self.has_q_233
        new_has_q_134 = int(has_q_134) if has_q_134 is not None else self.has_q_134
        new_n_neuron = n_neuron if n_neuron is not None else self.n_neuron

        new_l_max_enh = (self.l_max_3b
                         + (new_l_max_4b > 0) + (new_l_max_5b > 0)
                         + (new_has_q_112 > 0) + (new_has_q_123 > 0) + (new_has_q_233 > 0)
                         + (new_has_q_134 > 0))
        new_n_desc_angular = (self.n_max_angular + 1) * new_l_max_enh
        old_n_desc = self.n_descriptor_radial + self.n_descriptor_angular
        new_n_desc = self.n_descriptor_radial + new_n_desc_angular
        delta_desc = new_n_desc - old_n_desc
        delta_neuron = new_n_neuron - self.n_neuron

        keys = self.types if self.version in (4, 5) else ['all_species']

        # Step 1: Apply adaptive sigma to all existing parameters (re-open SNES search width)
        _apply_adaptive_sigma_to_restart(new.restart_parameters, keys, sigma_factor, sigma_floor)

        # Step 2: Expand descriptor dimensions (new columns in w0, new q_scaler entries)
        if delta_desc > 0:
            for s in keys:
                old_w0 = new.ann_parameters[s]['w0']  # (n_neuron_old, old_n_desc)
                new.ann_parameters[s]['w0'] = np.hstack(
                    [old_w0, np.zeros((self.n_neuron, delta_desc))]
                )
                old_mu_w0 = new.restart_parameters['ann_mu'][s]['w0']
                new.restart_parameters['ann_mu'][s]['w0'] = np.hstack(
                    [old_mu_w0, np.zeros((self.n_neuron, delta_desc))]
                )
                old_sigma_w0 = new.restart_parameters['ann_sigma'][s]['w0']
                new.restart_parameters['ann_sigma'][s]['w0'] = np.hstack(
                    [old_sigma_w0, np.full((self.n_neuron, delta_desc), sigma_new)]
                )
            new.q_scaler = list(new.q_scaler) + [1.0] * delta_desc

        # Step 3: Expand neuron count (new rows in w0/b0, new columns in w1)
        if delta_neuron > 0:
            for s in keys:
                # w0: append new rows
                cur_w0 = new.ann_parameters[s]['w0']  # (n_old, new_n_desc)
                new.ann_parameters[s]['w0'] = np.vstack(
                    [cur_w0, np.zeros((delta_neuron, new_n_desc))]
                )
                # b0: append new rows
                cur_b0 = new.ann_parameters[s]['b0']
                new.ann_parameters[s]['b0'] = np.vstack(
                    [cur_b0, np.zeros((delta_neuron, 1))]
                )
                # w1: append new columns; handle both 2D (standard) and 1D (charge)
                cur_w1 = new.ann_parameters[s]['w1']
                zeros_w1 = (np.zeros(delta_neuron) if cur_w1.ndim == 1
                            else np.zeros((1, delta_neuron)))
                new.ann_parameters[s]['w1'] = np.hstack([cur_w1, zeros_w1])
                if 'w1_charge' in new.ann_parameters[s]:
                    cur_wc = new.ann_parameters[s]['w1_charge']
                    new.ann_parameters[s]['w1_charge'] = np.hstack([cur_wc, np.zeros(delta_neuron)])

                # restart w0
                cur_mu_w0 = new.restart_parameters['ann_mu'][s]['w0']
                new.restart_parameters['ann_mu'][s]['w0'] = np.vstack(
                    [cur_mu_w0, np.zeros((delta_neuron, new_n_desc))]
                )
                cur_sigma_w0 = new.restart_parameters['ann_sigma'][s]['w0']
                new.restart_parameters['ann_sigma'][s]['w0'] = np.vstack(
                    [cur_sigma_w0, np.full((delta_neuron, new_n_desc), sigma_new)]
                )
                # restart b0
                cur_mu_b0 = new.restart_parameters['ann_mu'][s]['b0']
                new.restart_parameters['ann_mu'][s]['b0'] = np.vstack(
                    [cur_mu_b0, np.zeros((delta_neuron, 1))]
                )
                cur_sigma_b0 = new.restart_parameters['ann_sigma'][s]['b0']
                new.restart_parameters['ann_sigma'][s]['b0'] = np.vstack(
                    [cur_sigma_b0, np.full((delta_neuron, 1), sigma_new)]
                )
                # restart w1
                cur_mu_w1 = new.restart_parameters['ann_mu'][s]['w1']
                zeros_w1 = (np.zeros(delta_neuron) if cur_mu_w1.ndim == 1
                            else np.zeros((1, delta_neuron)))
                new.restart_parameters['ann_mu'][s]['w1'] = np.hstack([cur_mu_w1, zeros_w1])
                cur_sigma_w1 = new.restart_parameters['ann_sigma'][s]['w1']
                zeros_w1 = (np.full(delta_neuron, sigma_new) if cur_sigma_w1.ndim == 1
                            else np.full((1, delta_neuron), sigma_new))
                new.restart_parameters['ann_sigma'][s]['w1'] = np.hstack([cur_sigma_w1, zeros_w1])
                if 'w1_charge' in new.restart_parameters['ann_mu'][s]:
                    cur = new.restart_parameters['ann_mu'][s]['w1_charge']
                    new.restart_parameters['ann_mu'][s]['w1_charge'] = np.hstack(
                        [cur, np.zeros(delta_neuron)]
                    )
                    cur = new.restart_parameters['ann_sigma'][s]['w1_charge']
                    new.restart_parameters['ann_sigma'][s]['w1_charge'] = np.hstack(
                        [cur, np.full(delta_neuron, sigma_new)]
                    )

        # Step 4: Add charge output head
        if charge_head:
            new.model_type = 'potential_with_charges'
            new.sqrt_epsilon_infinity = 1.0
            for s in keys:
                cur_w1 = new.ann_parameters[s]['w1']  # (1, new_n_neuron)
                new.ann_parameters[s]['w1'] = cur_w1[0, :]  # flatten to 1D
                new.ann_parameters[s]['w1_charge'] = np.zeros(new_n_neuron)

                cur_mu_w1 = new.restart_parameters['ann_mu'][s]['w1']
                new.restart_parameters['ann_mu'][s]['w1'] = cur_mu_w1[0, :]
                new.restart_parameters['ann_mu'][s]['w1_charge'] = np.zeros(new_n_neuron)

                cur_sigma_w1 = new.restart_parameters['ann_sigma'][s]['w1']
                new.restart_parameters['ann_sigma'][s]['w1'] = cur_sigma_w1[0, :]
                new.restart_parameters['ann_sigma'][s]['w1_charge'] = np.full(
                    new_n_neuron, sigma_new
                )

            new.restart_parameters['ann_mu']['sqrt_epsilon_infinity'] = 1.0
            new.restart_parameters['ann_sigma']['sqrt_epsilon_infinity'] = float(sigma_new)

        # Step 5: Update header metadata
        new.l_max_4b = new_l_max_4b
        new.l_max_5b = new_l_max_5b
        new.has_q_112 = new_has_q_112
        new.has_q_123 = new_has_q_123
        new.has_q_233 = new_has_q_233
        new.has_q_134 = new_has_q_134
        new.n_descriptor_angular = new_n_desc_angular
        new.n_neuron = new_n_neuron

        # Step 6: Recalculate parameter counts
        _recalculate_parameter_counts(new)

        return new

    def prune(self,
              n_neuron: int = None,
              l_max_4b: int = None,
              l_max_5b: int = None,
              has_q_112: bool = None,
              has_q_123: bool = None,
              has_q_233: bool = None,
              has_q_134: bool = None,
              charge_head: bool = False,
              sigma_factor: float = 0.1,
              sigma_floor: float = 1e-6) -> 'Model':
        """Prune the model by removing neurons, disabling descriptor terms, or removing
        the charge output head.

        Returns a new :class:`Model` with the requested structural changes applied.
        The source model is not modified. When reducing ``n_neuron``, neurons are
        selected by importance score averaged over species:
        ``importance[n] = mean_s(||w0_s[n,:]||_2 * |w1_s[n]|)``.

        All surviving parameters receive adaptive SNES sigma:
        ``sigma = max(sigma_floor, sigma_factor * |mu|)``.

        Parameters
        ----------
        n_neuron
            Target neuron count; must be <= current. ``None`` leaves unchanged.
        l_max_4b
            Target 4-body l_max; must be <= current. Setting to ``0`` removes the
            4-body angular descriptor block. Reducing to a lower non-zero value is
            a header-only change (descriptor dimensions unchanged). ``None`` leaves
            unchanged.
        l_max_5b
            Same as ``l_max_4b`` but for five-body terms.
        has_q_112
            ``False`` disables and removes the q_112 descriptor block. ``None``
            leaves unchanged. ``True`` is not valid; use :meth:`augment` instead.
        has_q_123
            Same as ``has_q_112`` but for the q_123 term.
        has_q_233
            Same as ``has_q_112`` but for the q_233 term.
        has_q_134
            Same as ``has_q_112`` but for the q_134 term.
        charge_head
            If ``True``, remove the charge output head from a
            ``potential_with_charges`` model, converting it back to ``potential``.
            Removes ``w1_charge`` per species and ``sqrt_epsilon_infinity`` from
            the restart.
        sigma_factor
            Controls sigma for surviving parameters:
            ``sigma = max(sigma_floor, sigma_factor * |mu|)``.
        sigma_floor
            Minimum sigma for surviving parameters.

        Returns
        -------
        Model
            New model with reduced structure, weights, and restart statistics.

        Raises
        ------
        ValueError
            If ``restart_parameters`` is not loaded, if any target value would
            expand the model (use :meth:`augment` instead), if a ``has_q_*``
            flag is set to ``True``, or if ``charge_head=True`` on a model
            without charges.
        """
        # --- Resolve target values ---
        new_n_neuron = n_neuron if n_neuron is not None else self.n_neuron
        new_l_max_4b = l_max_4b if l_max_4b is not None else self.l_max_4b
        new_l_max_5b = l_max_5b if l_max_5b is not None else self.l_max_5b
        new_has_q_112 = 0 if has_q_112 is False else self.has_q_112
        new_has_q_123 = 0 if has_q_123 is False else self.has_q_123
        new_has_q_233 = 0 if has_q_233 is False else self.has_q_233
        new_has_q_134 = 0 if has_q_134 is False else self.has_q_134

        # --- Validate ---
        if self.version not in (3, 4):
            raise ValueError(
                f'prune() only supports NEP versions 3 and 4; got version {self.version}.'
            )
        if new_n_neuron > self.n_neuron:
            raise ValueError(
                f'n_neuron ({new_n_neuron}) must be <= current n_neuron ({self.n_neuron}); '
                'use augment() to increase.'
            )
        if new_l_max_4b > self.l_max_4b:
            raise ValueError(
                f'l_max_4b ({new_l_max_4b}) must be <= current l_max_4b ({self.l_max_4b}); '
                'use augment() to increase.'
            )
        if new_l_max_5b > self.l_max_5b:
            raise ValueError(
                f'l_max_5b ({new_l_max_5b}) must be <= current l_max_5b ({self.l_max_5b}); '
                'use augment() to increase.'
            )
        for flag_val, name in [
            (has_q_112, 'has_q_112'), (has_q_123, 'has_q_123'),
            (has_q_233, 'has_q_233'), (has_q_134, 'has_q_134')
        ]:
            if flag_val is True:
                raise ValueError(
                    f'Cannot enable {name} via prune(); '
                    'use augment() to enable descriptor terms.'
                )
        if charge_head and self.model_type != 'potential_with_charges':
            raise ValueError(
                f'charge_head=True requires model_type="potential_with_charges"; '
                f'got "{self.model_type}".'
            )
        if self.restart_parameters is None:
            raise ValueError(
                'restart_parameters must be loaded before calling prune(). '
                'Pass restart_file= to read_model() or call model.read_restart() first.'
            )

        new = copy.deepcopy(self)
        keys = self.types if self.version in (4, 5) else ['all_species']

        # Step 1: Adaptive sigma for all existing parameters
        _apply_adaptive_sigma_to_restart(new.restart_parameters, keys, sigma_factor, sigma_floor)

        # Step 2: Neuron pruning — keep the most important neurons
        if new_n_neuron < self.n_neuron:
            importances = []
            for s in keys:
                w0 = self.ann_parameters[s]['w0']   # (n_neuron, n_desc)
                w1_flat = self.ann_parameters[s]['w1'].ravel()
                if 'w1_charge' in self.ann_parameters[s]:
                    output_norm = np.abs(w1_flat) + np.abs(self.ann_parameters[s]['w1_charge'])
                else:
                    output_norm = np.abs(w1_flat)
                importances.append(np.linalg.norm(w0, axis=1) * output_norm)

            keep_idx = np.sort(np.argsort(np.mean(importances, axis=0))[-new_n_neuron:])

            for s in keys:
                new.ann_parameters[s]['w0'] = new.ann_parameters[s]['w0'][keep_idx, :]
                new.ann_parameters[s]['b0'] = new.ann_parameters[s]['b0'][keep_idx, :]
                w1 = new.ann_parameters[s]['w1']
                new.ann_parameters[s]['w1'] = w1[:, keep_idx] if w1.ndim == 2 else w1[keep_idx]
                if 'w1_charge' in new.ann_parameters[s]:
                    new.ann_parameters[s]['w1_charge'] = (
                        new.ann_parameters[s]['w1_charge'][keep_idx]
                    )
                for pk in ['ann_mu', 'ann_sigma']:
                    rp = new.restart_parameters[pk][s]
                    rp['w0'] = rp['w0'][keep_idx, :]
                    rp['b0'] = rp['b0'][keep_idx, :]
                    w1 = rp['w1']
                    rp['w1'] = w1[:, keep_idx] if w1.ndim == 2 else w1[keep_idx]
                    if 'w1_charge' in rp:
                        rp['w1_charge'] = rp['w1_charge'][keep_idx]

        # Step 3: Descriptor column pruning (disabling higher-body terms)
        n_per = self.n_max_angular + 1
        hb_terms = [
            (self.l_max_4b, new_l_max_4b),
            (self.l_max_5b, new_l_max_5b),
            (self.has_q_112, new_has_q_112),
            (self.has_q_123, new_has_q_123),
            (self.has_q_233, new_has_q_233),
            (self.has_q_134, new_has_q_134),
        ]
        keep_cols = list(range(self.n_descriptor_radial + n_per * self.l_max_3b))
        col_offset = len(keep_cols)
        for old_val, new_val in hb_terms:
            if old_val > 0:
                if new_val > 0:
                    keep_cols.extend(range(col_offset, col_offset + n_per))
                col_offset += n_per

        old_n_desc = self.n_descriptor_radial + self.n_descriptor_angular
        if len(keep_cols) < old_n_desc:
            keep_cols = np.array(keep_cols, dtype=int)
            for s in keys:
                new.ann_parameters[s]['w0'] = new.ann_parameters[s]['w0'][:, keep_cols]
                for pk in ['ann_mu', 'ann_sigma']:
                    rp = new.restart_parameters[pk][s]
                    rp['w0'] = rp['w0'][:, keep_cols]
            new.q_scaler = [new.q_scaler[i] for i in keep_cols]

        # Step 4: Charge head removal
        if charge_head:
            new.model_type = 'potential'
            new.sqrt_epsilon_infinity = None
            for s in keys:
                w1 = new.ann_parameters[s]['w1']        # 1D (n_neuron,)
                new.ann_parameters[s]['w1'] = w1.reshape(1, -1)
                del new.ann_parameters[s]['w1_charge']
                for pk in ['ann_mu', 'ann_sigma']:
                    rp = new.restart_parameters[pk][s]
                    rp['w1'] = rp['w1'].reshape(1, -1)
                    del rp['w1_charge']
            del new.restart_parameters['ann_mu']['sqrt_epsilon_infinity']
            del new.restart_parameters['ann_sigma']['sqrt_epsilon_infinity']

        # Step 5: Update header fields
        new.n_neuron = new_n_neuron
        new.l_max_4b = new_l_max_4b
        new.l_max_5b = new_l_max_5b
        new.has_q_112 = new_has_q_112
        new.has_q_123 = new_has_q_123
        new.has_q_233 = new_has_q_233
        new.has_q_134 = new_has_q_134

        new_l_max_enh = (self.l_max_3b
                         + (new_l_max_4b > 0) + (new_l_max_5b > 0)
                         + (new_has_q_112 > 0) + (new_has_q_123 > 0) + (new_has_q_233 > 0)
                         + (new_has_q_134 > 0))
        new.n_descriptor_angular = (self.n_max_angular + 1) * new_l_max_enh

        # Step 6: Recalculate parameter counts
        _recalculate_parameter_counts(new)

        return new


def read_model(filename: str, restart_file: str = None) -> Model:
    """Parses a file in ``nep.txt`` format and returns the
    content in the form of a :class:`Model <calorine.nep.model.Model>`
    object.

    Parameters
    ----------
    filename
        Input file name.
    restart_file
        If provided, also read restart parameters from this file in
        `nep.restart` format and attach them to the returned model.
        Defaults to None.
    """
    data, parameters = _get_nep_contents(filename)

    # sanity checks
    for fld in ['cutoff', 'basis_size', 'n_max', 'l_max', 'ANN']:
        assert fld in data, f'Invalid model file; {fld} line is missing'
    assert data['version'] in [
        3,
        4,
        5,
    ], 'Invalid model file; only NEP versions 3, 4 and 5 are currently supported'

    # split up cutoff tuple
    N_types = len(data['types'])
    # Either global cutoffs + max neighbirs, or typewise cutoffs + max_neighbors
    assert len(data['cutoff']) in [4, 2*N_types+2]
    data['max_neighbors_radial'] = int(data['cutoff'][-2])
    data['max_neighbors_angular'] = int(data['cutoff'][-1])
    if len(data['cutoff']) == 2*N_types+2:
        # Typewise cutoffs: radial are even, angular are odd
        data['radial_cutoff'] = [data['cutoff'][i*2] for i in range(N_types)]
        data['angular_cutoff'] = [data['cutoff'][i*2+1] for i in range(N_types)]
    else:
        data['radial_cutoff'] = data['cutoff'][0]
        data['angular_cutoff'] = data['cutoff'][1]
    del data['cutoff']

    # split up basis_size tuple
    assert len(data['basis_size']) == 2
    data['n_basis_radial'] = data['basis_size'][0]
    data['n_basis_angular'] = data['basis_size'][1]
    del data['basis_size']

    # split up n_max tuple
    assert len(data['n_max']) == 2
    data['n_max_radial'] = data['n_max'][0]
    data['n_max_angular'] = data['n_max'][1]
    del data['n_max']

    # split up nl_max tuple
    len_l = len(data['l_max'])
    assert len_l in [1, 2, 3, 4, 5, 6, 7]
    data['l_max_3b'] = data['l_max'][0]
    data['l_max_4b'] = data['l_max'][1] if len_l > 1 else 0
    data['l_max_5b'] = data['l_max'][2] if len_l > 2 else 0
    data['has_q_112'] = data['l_max'][3] if len_l > 3 else 0
    data['has_q_123'] = data['l_max'][4] if len_l > 4 else 0
    data['has_q_233'] = data['l_max'][5] if len_l > 5 else 0
    data['has_q_134'] = data['l_max'][6] if len_l > 6 else 0
    del data['l_max']

    # compute dimensions of descriptor components
    data['n_descriptor_radial'] = data['n_max_radial'] + 1
    l_max_enh = (data['l_max_3b']
                 + (data['l_max_4b'] > 0)
                 + (data['l_max_5b'] > 0)
                 + (data['has_q_112'] > 0)
                 + (data['has_q_123'] > 0)
                 + (data['has_q_233'] > 0)
                 + (data['has_q_134'] > 0))
    data['n_descriptor_angular'] = (data['n_max_angular'] + 1) * l_max_enh
    n_descriptor = data['n_descriptor_radial'] + data['n_descriptor_angular']

    is_charged_model = data['model_type'] == 'potential_with_charges'
    # compute number of parameters
    data['n_neuron'] = data['ANN'][0]
    del data['ANN']
    n_types = len(data['types'])
    if data['version'] == 3:
        n = 1
        n_bias = 1
    elif data['version'] == 4 and is_charged_model:
        # one hidden layer per atomic species, but two output nodes
        n = n_types
        n_bias = 2
    elif data['version'] == 4:
        # one hidden layer per atomic species
        n = n_types
        n_bias = 1
    else:  # NEP5
        # like nep4, but additionally has an
        # individual bias term in the output
        # layer for each species.
        n = n_types
        n_bias = 1 + n_types  # one global bias + one per species

    n_ann_input_weights = (n_descriptor + 1) * data['n_neuron']  # weights + bias
    n_ann_output_weights = 2*data['n_neuron'] if is_charged_model else data['n_neuron']  # weights
    n_ann_parameters = (
        n_ann_input_weights + n_ann_output_weights
    ) * n + n_bias

    n_descriptor_weights = n_types**2 * (
        (data['n_max_radial'] + 1) * (data['n_basis_radial'] + 1)
        + (data['n_max_angular'] + 1) * (data['n_basis_angular'] + 1)
    )
    data['n_parameters'] = n_ann_parameters + n_descriptor_weights + n_descriptor
    is_polarizability_model = data['model_type'] == 'polarizability'
    if data['n_parameters'] + n_ann_parameters == len(parameters):
        data['n_parameters'] += n_ann_parameters
        assert is_polarizability_model, (
            'Model is not labelled as a polarizability model, but the number of '
            'parameters matches a polarizability model.\n'
            'If this is a polarizability model trained with GPUMD <=v3.8, please '
            'modify the header in the nep.txt file to enable parsing '
            f'`nep{data["version"]}_polarizability`.\n'
        )
    assert data['n_parameters'] == len(parameters), (
        'Parsing of parameters inconsistent; please submit a bug report\n'
        f'{data["n_parameters"]} != {len(parameters)}'
    )
    data['n_ann_parameters'] = n_ann_parameters

    # split up parameters into the ANN weights, descriptor weights, and scaling parameters
    n1 = n_ann_parameters
    n1 *= 2 if is_polarizability_model else 1
    n2 = n1 + n_descriptor_weights
    data['ann_parameters'] = parameters[:n1]
    descriptor_weights = np.array(parameters[n1:n2])
    data['q_scaler'] = parameters[n2:]

    # add ann parameters to data dict
    ann_groups = data['types'] if data['version'] in (4, 5) else ['all_species']
    sorted_ann_parameters = _sort_ann_parameters(data['ann_parameters'],
                                                 ann_groups,
                                                 data['n_neuron'],
                                                 n,
                                                 n_bias,
                                                 n_descriptor,
                                                 is_polarizability_model,
                                                 is_charged_model)

    data['ann_parameters'] = sorted_ann_parameters
    if 'sqrt_epsilon_infinity' in sorted_ann_parameters.keys():
        data['sqrt_epsilon_infinity'] = sorted_ann_parameters['sqrt_epsilon_infinity']
        sorted_ann_parameters.pop('sqrt_epsilon_infinity')
        data['ann_parameters'] = sorted_ann_parameters

    # add descriptors to data dict
    data['n_descriptor_parameters'] = len(descriptor_weights)
    radial, angular = _sort_descriptor_parameters(descriptor_weights,
                                                  data['types'],
                                                  data['n_max_radial'],
                                                  data['n_basis_radial'],
                                                  data['n_max_angular'],
                                                  data['n_basis_angular'])
    data['radial_descriptor_weights'] = radial
    data['angular_descriptor_weights'] = angular

    model = Model(**data)
    if restart_file is not None:
        model.read_restart(restart_file)
    return model
