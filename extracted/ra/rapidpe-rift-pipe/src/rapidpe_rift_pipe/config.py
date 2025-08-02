__author__ = "Daniel Wysocki"

import os
import sys
import warnings
from ast import literal_eval
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import shutil
import getpass
from rapidpe_rift_pipe.modules import *


# Directory containing default config files
DEFAULT_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config_files")


@dataclass
class Config:
    """
    # Example usage
    cfg = Config.load(config_fname)
    cfg.output_parent_directory
    """
    # Path to the config file itself
    config_fname: Optional[str]

    # GraceDB settings
    gracedb_url: Optional[str]
    # Condor info
    accounting_group: str
    accounting_group_user: str
    email_address_for_job_complete_notice: Optional[str]
    getenv: List[str]
    environment: Dict[str, str]
    # Paths
    output_parent_directory: str
    injections_filename: str
    web_dir: Optional[str]
    # Sampling settings
    n_iterations_per_job: int
    seed: Optional[int]

    # Parameters
    intrinsic_param_to_search: List[str]
    # Flags
    # TODO: should convert from ints to bool (only have values 0 and 1 currently)
    event_params_in_cfg: bool
    overwrite_existing_event_dag: int
    submit_only_at_exact_signal_position: int
    submit_dag: int
    use_skymap: int
    use_event_spin: bool
    cProfile: bool

    # Grid refinement options
    distance_coordinates: str

    # Executable paths
    exe_create_event_dag: str
#    exe_compute_intrinsic_grid: str
    exe_generate_initial_grid: str
    exe_grid_refine: str
    exe_integration_extrinsic_likelihood: str

    # Entire sections parsed as dicts
    common_event_info: dict
    integrate_likelihood_cmds_dict: dict
    integrate_likelihood_condor_commands: dict
    create_event_dag_info: dict
    create_event_dag_condor_commands: dict
    grid_refine_info: dict
    grid_refine_condor_commands: dict

    # Mutually exclusive groups
    event: "EventConfig"
    initial_grid_setup: "InitialGridSetupConfig"
    pastro: "Pastro"

    # Entire sections parsed as command line args
    initial_grid_only_cli_args: str

    @staticmethod
    def load(fname) -> "Config":
        from configparser import ConfigParser

        cfg = ConfigParser()
        cfg.optionxform = str
        cfg.read(fname)

        attrs = {}

        attrs["config_fname"] = fname

        ###########
        # General #
        ###########
        # GraceDB info
        attrs["gracedb_url"] = cfg.get(
            "General", "gracedb_url",
            fallback="https://gracedb.ligo.org/api/",
        )

        # Condor info
        attrs["accounting_group"] = cfg.get("General","accounting_group")
        attrs["accounting_group_user"] = cfg.get(
                "General","accounting_group_user",
                fallback=getpass.getuser()
                )
        attrs["email_address_for_job_complete_notice"] = cfg.get(
            "General", "email_address_for_job_complete_notice",
            fallback="",
        )
        attrs["web_dir"] = cfg.get(
            "General", "web_dir",
            fallback="",

        )
        attrs["getenv"] = parse_list(cfg, "General", "getenv", ["True"])
        attrs["environment"] = parse_dict(cfg, "General", "environment", {})
        # Paths
        attrs["output_parent_directory"] = cfg.get("General", "output_parent_directory")
        attrs["injections_filename"] = cfg.get("General", "injections_file", fallback=None)
        # Sampling settings
        attrs["n_iterations_per_job"] = cfg.getint("General", "n_iterations_per_job")
        attrs["seed"] = cfg.getint("General", "seed", fallback=None)
        # Parameters
        attrs["intrinsic_param_to_search"] = literal_eval(correct_list_string_formatting(
            cfg.get("General","intrinsic_param_to_search", fallback="[mass1,mass2]")
        ))

        # Flags
        attrs["event_params_in_cfg"] = cfg.getboolean(
            "General", "event_parameters_in_config_file",
            fallback=False,
        )
        if attrs["event_params_in_cfg"]:
            raise ValueError(
                "event_parameters_in_config_file=True is currently unsupported"
            )

        attrs["overwrite_existing_event_dag"] = cfg.getint(
            "General", "overwrite_existing_event_dag",
            fallback=0,
        )
        attrs["submit_only_at_exact_signal_position"] = cfg.getint(
            "General", "submit_only_at_exact_signal_position",
            fallback=0,
        )
        attrs["submit_dag"] = cfg.getint("General", "submit_dag")
        attrs["use_skymap"] = cfg.getint("General", "use_skymap")
        attrs["use_event_spin"] = cfg.getboolean("General", "use_event_spin", fallback=False)
        attrs["cProfile"] = cfg.getboolean("General", "cProfile", fallback=False)
        # Executables
        attrs["exe_create_event_dag"] = os.path.abspath(shutil.which(
            cfg.get(
                "General", "exe_create_event_dag",
                fallback="rapidpe_create_event_dag",
            )
        ))
        attrs["exe_generate_initial_grid"] = shutil.which(
            cfg.get(
                "General", "exe_generate_initial_grid",
                fallback=""
            )
        )
        if attrs["exe_generate_initial_grid"] is not None:
            warnings.warn(
                "exe_generate_initial_grid is not currently supported"
            )
            attrs["exe_generate_initial_grid"] = os.path.abspath(
                attrs["exe_generate_initial_grid"]
            )
        attrs["exe_grid_refine"] = os.path.abspath(shutil.which(
            cfg.get(
                "General", "exe_grid_refine",
                fallback="rapidpe_compute_intrinsic_grid",
            )
        ))
        attrs["exe_integration_extrinsic_likelihood"] = (
            os.path.abspath(shutil.which(
                cfg.get(
                    "General", "exe_integration_extrinsic_likelihood",
                    fallback="rapidpe_integrate_extrinsic_likelihood",
                )
            ))
        )

        ##############
        # GridRefine #
        ##############
        attrs["distance_coordinates"] = cfg.get(
            "GridRefine", "distance-coordinates",
            fallback="",
        )

        #########
        # Event #
        #########
        attrs["event"] = EventConfig(cfg)

        ####################
        # InitialGridSetup #
        ####################
        attrs["initial_grid_setup"] = InitialGridSetupConfig(cfg)

        ##########
        # Pastro #
        ##########
        attrs["pastro"] = PastroConfig(cfg)

        #####################
        # Sections as Dicts #
        #####################
        attrs["common_event_info"] = convert_section_args_to_dict(cfg, "Event")
        attrs["integrate_likelihood_cmds_dict"] = (
            convert_section_args_to_dict(cfg, "LikelihoodIntegration")
        )
        attrs["integrate_likelihood_condor_commands"] = (
            convert_section_args_to_dict(
                cfg, "LikelihoodIntegration_condor_commands",
            )
        )
        attrs["create_event_dag_info"] = (
            convert_section_args_to_dict(cfg, "CreateEventDag")
        )
        attrs["create_event_dag_condor_commands"] = (
            convert_section_args_to_dict(cfg, "CreateEventDag_condor_commands")
        )
        attrs["grid_refine_info"] = (
            convert_section_args_to_dict(cfg, "GridRefine")
        )
        attrs["grid_refine_condor_commands"] = (
            convert_section_args_to_dict(cfg, "GridRefine_condor_commands")
        )

        #################################
        # Sections as command line args #
        #################################
        attrs["initial_grid_only_cli_args"] = (
            convert_cfg_section_to_cmd_line(cfg, "InitialGridOnly")
            if cfg.has_section("InitialGridOnly")
            else ""
        )

        return Config(**attrs)




_INACCESSIBLE = object()


def possibly_inaccessible_property(field_name):
    protected_field_name = f"_{field_name}"

    def wrapper(self):
        field = getattr(self, protected_field_name)
        if field is _INACCESSIBLE:
            raise AttributeError(
                "Cannot access field {field_name} in mode {self.mode}"
            )

        return field

    return property(wrapper)


def parse_str(cfg, section, option, fallback=None):
    return cfg.get(section, option, fallback=fallback)

def parse_int(cfg, section, option, fallback=None):
    return cfg.getint(section, option, fallback=fallback)

def parse_float(cfg, section, option, fallback=None):
    return cfg.getfloat(section, option, fallback=fallback)

def parse_bool(cfg, section, option, fallback=None):
    return cfg.getboolean(section, option, fallback=fallback)

def parse_list(cfg, section, option, fallback=None):
    if not cfg.has_option(section, option):
        return fallback

    lst_str = cfg.get(section, option)
    lst = ast.literal_eval(lst_str)

    if not isinstance(lst, list):
        raise TypeError(
            f"parse_list expected a string representation of a list, "
            f"got {type(lst)} instead."
        )

    return lst

def parse_dict(cfg, section, option, fallback=None):
    if not cfg.has_option(section, option):
        return fallback

    json_str = cfg.get(section, option)
    return json.loads(json_str)

def parse_special_list(cfg, section, option, fallback=None):
    if not cfg.has_option(section, option):
        return fallback

    return literal_eval(
        correct_list_string_formatting(cfg.get(section, option))
    )

def parse_json(cfg, section, option, fallback=None):
    if not cfg.has_option(section, option):
        return fallback

    json_fname = cfg.get(section, option)
    with open(json_fname, "r") as json_file:
        return json.load(json_file)

def fields_match(fields, field_descriptors) -> bool:
    """
    Returns `True` if the fields match precisely with the fields named in the
    descriptors, though if the descriptors have a `"fallback"` value, they do
    not need to be present.  Otherwise return `False`.
    """
    # Make copies that we can modify
    fields_remaining = fields.copy()
    field_descriptors_remaining = field_descriptors.copy()

    # Iterate through fields, removing from both data structures if present, and
    # returning `False` if a field is not in the descriptors.
    while fields_remaining:
        field, _ = fields_remaining.pop()
        if field not in field_descriptors_remaining:
            return False
        del field_descriptors_remaining[field]

    # Now the only remaining descriptors should have `"fallback"` values.
    for field, descriptor in field_descriptors_remaining.items():
        if "fallback" not in descriptor:
            return False

    # Everything matched, return `True`.
    return True





def _make_config_group(type_name: str, section_name: str, spec: dict):
    """
    Programmatically defines the `EventConfig` class.
    """
    # Set of field names which occur under all possible groups.
    possible_field_names = set()
    for _, group_field_descriptors in spec.items():
        possible_field_names |= set(group_field_descriptors)


    def __init__(self, cfg):
        # Ensure "Event" section is present.
        if not cfg.has_section(section_name):
            raise RuntimeError(f"Missing section '{section_name}'")

        # Initialize all possible fields to be inaccessible.  Accessible ones
        # will be overwritten later.
        for field_name in possible_field_names:
            protected_field_name = f"_{field_name}"
            setattr(self, protected_field_name, _INACCESSIBLE)

        # Get the names of all options in "Event" section
        fields = set(cfg.items(section_name))

        # Attempt to find a group that matches the options in the config file.
        for group_name, group_field_descriptors in spec.items():
            if fields_match(fields, group_field_descriptors):
                # Found a match.

                # Set the mode
                self._mode = group_name

                # Add each field as an attribute, prefixed by `_` so they cannot
                # be modified later.
                for field_name, descriptor in group_field_descriptors.items():
                    protected_field_name = f"_{field_name}"

                    # Get information needed for parsing the line in the config
                    # file.
                    parser = descriptor["parser"]
                    fallback = descriptor.get("fallback")
                    # Parse the value from the config file.
                    value = parser(
                        cfg, section_name, field_name,
                        fallback=fallback,
                    )

                    # Store the value.
                    setattr(self, protected_field_name, value)

                # No need to process any other groups.
                return

        # No group matched, config is malformed.
        raise RuntimeError(
            f"'{section_name}' section does not have all required fields."
        )

    def mode(self) -> str:
        return self._mode

    # Superclass
    type_bases = (object,)
    # Define the class's methods
    type_dict = {
        "__init__" : __init__,
        "mode" : property(mode),
    }
    # Track information included in `__repr__`
    repr_fields = ["mode"]

    # Dynamically add properties for each possible field
    for field_name in possible_field_names:
        type_dict[field_name] = possibly_inaccessible_property(field_name)
        repr_fields.append(field_name)

    # Define __repr__
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        field_descriptors = []
        for field in repr_fields:
            if hasattr(self, field):
                value = getattr(self, field)
                field_descriptors.append(f"{field}={value!r}")
        return f"{class_name}({', '.join(field_descriptors)})"

    type_dict["__repr__"] = __repr__

    return type(type_name, type_bases, type_dict)


_event_group_spec = {
    "gid" : {
        "gracedb_id" : {
            "parser" : parse_str,
        },
        "run_mode" : {
            "parser" : parse_str,
            "fallback" : "online",
        },
        "query_shm": {
            "parser" : parse_bool,
            "fallback" : False,
        },
        "mdc_event_injection_file" : {
            "parser": parse_str,
            "fallback": None
        },
        "mdc_time_offset" : {
            "parser" : parse_str,
            "fallback" : None
        },
    },
    "sid" : {
        "superevent_id" : {
            "parser" : parse_str,
        },
        "run_mode" : {
            "parser" : parse_str,
            "fallback" : "online",
        },
        "query_shm": {
            "parser" : parse_bool,
            "fallback" : False,
        },
        "mdc_event_injection_file" : {
            "parser": parse_str,
            "fallback": None
        },
        "mdc_time_offset" : {
            "parser" : parse_str,
            "fallback" : None
        },
    },
    "injections" : {
        "injections_file" : {
            "parser" : parse_str,
            "fallback" : "/home/caitlin.rose/my_rapidPE_work/f2y2016data/subset_f2y2016inj/exact_inj/f2y2016_HLV_100shuffled_exactmasses.txt",
        },
        "cache_file" : {
            "parser" : parse_str,
            "fallback" : "/home/caitlin.rose/my_rapidPE_work/f2y2016data/create_2016_L1H1_data/2016injecteddata/injected_frames.cache",
        },
        "psd_file" : {
            "parser" : parse_special_list,
            "fallback" : [
                "H1=/home/caitlin.rose/my_rapidPE_work/f2y2016data/create_2016_L1H1_data/firstattempt/H1_psd_mid.xml.gz",
                "L1=/home/caitlin.rose/my_rapidPE_work/f2y2016data/create_2016_L1H1_data/firstattempt/L1_psd_mid.xml.gz",
                "V1=/home/caitlin.rose/my_rapidPE_work/f2y2016data/check_virgo_psd/V1_psd.xml.gz",
            ],
        },
        "skymap_file" : {
            "parser" : parse_str,
            "fallback" : "/home/vinaya.valsan/rapidPE/sinead_rapidPE/pp-plots-from-scratch/skymap/2016_fits/$INJINDEX$/bayestar.fits.gz",
        },
        "channel_name" : {
            "parser" : parse_special_list,
            "fallback" : [
                "H1=INJ_GAUSSIAN",
                "L1=INJ_GAUSSIAN",
                "V1=INJ_GAUSSIAN",
            ],
        },
    }
}

# Add frame_data_types field to all Event modes
_default_frame_data_types = {
    "H1" : "H1_HOFT_C00",
    "L1" : "L1_HOFT_C00",
    "V1" : "V1Online",
}

def parse_frame_data_types(cfg, section, option, fallback=None):
    _frame_data_types = parse_dict(
        cfg, section, option,
        fallback={},
    )
    return {**_default_frame_data_types, **_frame_data_types}

for spec in _event_group_spec.values():
    spec["frame_data_types"] = {
        "parser" : parse_frame_data_types,
        "fallback" : None,
    }

EventConfig = _make_config_group("EventConfig", "Event", _event_group_spec)


_initial_grid_setup_spec = {
    "overlap_bank" : {
        "overlap_bank" : {
            "parser" : parse_str,
        },
    },
    "initial_region" : {
        "initial_region" : {
            "parser" : parse_dict,
        },
    },
    "search_bias_bounds": {
        "search_bias_bounds_spec" : {
            "parser" : parse_str,
            "fallback" : os.path.join(DEFAULT_CONFIG_DIR,
                                      "search_bias_bounds/default.json"),
        },
    },
    "svd_bounds" : {
        "svd_bounds_file" : {
            "parser" : parse_str,
        },
        # Should be a JSON file with a list of dictionaries of the form
        # {"bounds": {"param0": [param0_min, param0_max],
        #             "param1": [param1_min, param1_max]},
        #  "fudge_factors": {"param0": fudge_factor_0,
        #                    "param1": fudge_factor_1},
        #  "svd_depth": depth}
        # For a given trigger, we find the dictionary for which it falls in the
        # bounds for each parameter, and then set the initial region to enclose
        # the 'svd_depth' highest-SNR SVD bins, and add on the fudge factor
        # (as a fraction of the initial range) to each parameter's limits.
        "svd_depth_json" : {
            "parser" : parse_str,
        },
        "svd_bin_params" : {
            "parser" : parse_list,
            "fallback" : ["mchirp", "eta"],
        },
    },
}

InitialGridSetupConfig = _make_config_group(
    "InitialGridSetupConfig", "InitialGridSetup",
    _initial_grid_setup_spec,
)


_pastro_group_spec = {
    "enabled" : {
        "category_rates": {
            "parser": parse_dict,
        },
        "category_rates_inj": {
            "parser": parse_dict,
        },
        "prior_boundary": {
            "parser": parse_dict,
        },
    },
    "disabled" : {}
}

PastroConfig = _make_config_group("PastroConfig", "Pastro", _pastro_group_spec)
