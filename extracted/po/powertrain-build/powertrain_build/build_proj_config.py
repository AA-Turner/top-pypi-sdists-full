# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module used to read project and base configuration files and provides methods for abstraction."""

import glob
import json
import os
import shutil
import pathlib
from pprint import pformat

from powertrain_build.lib.helper_functions import deep_dict_update
from powertrain_build.versioncheck import Version


class BuildProjConfig:
    """A class holding build project configurations."""

    def __init__(self, prj_config_file):
        """Read project configuration file to internal an representation.

        Args:
            prj_config_file (str): Project config filename
        """
        super().__init__()
        self._prj_cfg_file = prj_config_file
        prj_root_dir, _ = os.path.split(prj_config_file)
        self._prj_root_dir = os.path.abspath(prj_root_dir)

        with open(prj_config_file, 'r', encoding="utf-8") as pcfg:
            self._prj_cfg = json.load(pcfg)
        if not Version.is_compatible(self._prj_cfg.get('ConfigFileVersion')):
            raise ValueError('Incompatible project config file version.')
        # Load a basic config that can be common for several projects
        # the local config overrides the base config
        if 'BaseConfig' in self._prj_cfg:
            fil_tmp = os.path.join(prj_root_dir, self._prj_cfg['BaseConfig'])
            fil_ = os.path.abspath(fil_tmp)
            with open(fil_, 'r', encoding="utf-8") as bcfg:
                base_cnfg = json.load(bcfg)
            deep_dict_update(self._prj_cfg, base_cnfg)
            if not Version.is_compatible(self._prj_cfg.get('BaseConfigFileVersion')):
                raise ValueError('Incompatible base config file version.')
        deep_dict_update(self._prj_cfg, self._get_code_generation_config())
        self._composition_config = self._parse_composition_config(self._prj_cfg.get('CompositionConfig', {}))
        self.has_yaml_interface = self._prj_cfg['ProjectInfo'].get('yamlInterface', False)
        self.device_domains = self._get_device_domains()
        self.services_file = self._get_services_file()
        self._load_unit_configs()
        self._add_global_const_file()
        self._all_units = []
        self._calc_all_units()
        self.name = self._prj_cfg['ProjectInfo']['projConfig']
        self.allow_undefined_unused = self._prj_cfg['ProjectInfo'].get('allowUndefinedUnused', True)
        self._scheduler_prefix = self._prj_cfg['ProjectInfo'].get('schedulerPrefix', '')
        if self._scheduler_prefix:
            self._scheduler_prefix = self._scheduler_prefix + '_'

    def __repr__(self):
        """Get string representation of object."""
        return pformat(self._prj_cfg['ProjectInfo'])

    def _get_default_code_generation_config(self):
        return {
            'generalAsilLevelDebug': 'B',
            'generalAsilLevelDependability': 'B',
            'generateCalibrationInterfaceFiles': False,
            'useCalibrationRteMacroExpansion': False,
            'generateCoreDummy': False,
            'generateDummyVar': False,
            'generateInterfaceHeaders': False,
            'rteCheckpointIdSize': None,
            'customRteCheckpointEntityName': 'AR_{raster}_CheckpointReached',
            'generateYamlInterfaceFile': False,
            'includeAllEnums': False,
            'mapToRteEnums': False,
            'propagateTagName': False,
            'useA2lSymbolLinks': False,
            'useRteNvmStructs': False,
            'useCamelCaseForNvmVariables': False
        }

    def _get_code_generation_config(self):
        """ Get code generation configuration.

        Anything already set in CodeGenerationConfig in ProjectCfg.json takes priority.
        If there is a project template for the ECU supplier, those values are used,
        unless already set in ProjectCfg.json.
        Finally, default values are inserted for missing keys.

        Args:
            item (str): Item to get from the configuration. If None, the whole configuration is returned.
        Returns:
            (dict): Code generation configuration.
        """
        code_generation_configuration = {}
        ecu_supplier = self.get_ecu_info()[0]
        deep_dict_update(code_generation_configuration, self._prj_cfg.get('ProjectTemplates', {}).get(ecu_supplier, {}))
        deep_dict_update(code_generation_configuration, self._get_default_code_generation_config())
        return {'CodeGenerationConfig': code_generation_configuration}

    def _get_device_domains(self):
        file_name = self._prj_cfg['ProjectInfo'].get('deviceDomains')
        full_path = pathlib.Path(self._prj_root_dir, file_name)
        if full_path.is_file():
            with open(full_path, 'r', encoding="utf-8") as device_domains:
                return json.loads(device_domains.read())
        return {}

    def _get_services_file(self):
        file_name = self._prj_cfg['ProjectInfo'].get('serviceInterfaces', '')
        full_path = pathlib.Path(self._prj_root_dir, file_name)
        return full_path

    @staticmethod
    def get_services(services_file):
        """Get the services from the services file.

        Args:
            services_file (pathlib.Path): The services file.

        Returns:
            (dict): The services.
        """
        if services_file.is_file():
            with services_file.open() as services:
                return json.loads(services.read())
        return {}

    def _load_unit_configs(self):
        """Load Unit config json file.

        This file contains which units are included in which projects.
        """
        if 'UnitCfgs' in self._prj_cfg:
            fil_tmp = os.path.join(self._prj_root_dir, self._prj_cfg['UnitCfgs'])
            with open(fil_tmp, 'r', encoding="utf-8") as fpr:
                tmp_unit_cfg = json.load(fpr)
                sample_times = tmp_unit_cfg.pop('SampleTimes')
                self._unit_cfg = {
                    'Rasters': tmp_unit_cfg,
                    'SampleTimes': sample_times
                }
        else:
            raise ValueError('UnitCfgs is not specified in project config')

    def _add_global_const_file(self):
        """Add the global constants definition to the 'not_scheduled' time raster."""
        ugc = self.get_use_global_const()
        if ugc:
            self._unit_cfg['Rasters'].setdefault('NoSched', []).append(ugc)

    def create_build_dirs(self):
        """Create the necessary output build dirs if they are missing.

        Clear the output build dirs if they exist.
        """
        src_outp = self.get_src_code_dst_dir()
        if os.path.exists(src_outp):
            shutil.rmtree(src_outp)
        os.makedirs(src_outp)

        log_outp = self.get_log_dst_dir()
        if os.path.exists(log_outp):
            shutil.rmtree(log_outp)
        os.makedirs(log_outp)

        rep_outp = self.get_reports_dst_dir()
        if os.path.exists(rep_outp):
            shutil.rmtree(rep_outp)
        os.makedirs(rep_outp)

        unit_cfg_outp = self.get_unit_cfg_deliv_dir()
        if os.path.exists(unit_cfg_outp):
            shutil.rmtree(unit_cfg_outp)
        if unit_cfg_outp is not None:
            os.makedirs(unit_cfg_outp)

    def get_code_generation_config(self, item=None):
        """ Get code generation configuration.

        Args:
            item (str): Item to get from the configuration. If None, the whole configuration is returned.
        Returns:
            (dict): Code generation configuration.
        """
        if item is not None:
            return self._prj_cfg['CodeGenerationConfig'].get(item, {})
        return self._prj_cfg['CodeGenerationConfig']

    def get_memory_map_config(self):
        """ Get memory map configuration.

        Returns:
            (dict): Memory map configuration.
        """
        return self._prj_cfg.get('MemoryMapConfig', {})

    def get_a2l_cfg(self):
        """ Get A2L configuration from A2lConfig.

        Returns:
            config (dict): A2L configuration
        """
        a2l_config = self._prj_cfg.get('A2lConfig', {})
        return {
            'name': a2l_config.get('name', self._prj_cfg["ProjectInfo"]["projConfig"]),
            'allow_kp_blob': a2l_config.get('allowKpBlob', True),
            'ip_address':  a2l_config.get('ipAddress', "169.254.4.10"),
            'ip_port': '0x%X' % a2l_config.get('ipPort', 30000),
            'asap2_version': a2l_config.get('asap2Version', "1 51")
        }

    def get_enable_end_to_end_status_signals(self):
        """Get the enable end-to-end status signals configuration.

        NOTE: Only appicable for device proxy type signal interfaces.

        Returns:
            (bool): True if end-to-end status signals are enabled, False otherwise.
        """
        return self._prj_cfg['ProjectInfo'].get('enableEndToEndStatusSignals', False)

    def get_unit_cfg_deliv_dir(self):
        """Get the directory where to put the unit configuration files.

        If this key is undefined, or set to None, the unit-configs will
        not be copied to the output folder.

        Returns:
            A path to the unit deliver dir, or None

        """
        if 'unitCfgDeliveryDir' in self._prj_cfg['ProjectInfo']:
            return os.path.join(self.get_root_dir(),
                                os.path.normpath(self._prj_cfg['ProjectInfo']
                                                 ['unitCfgDeliveryDir']))
        return None

    def get_root_dir(self):
        """Get the root directory of the project.

        Returns:
            A path to the project root (with wildcards)

        """
        return self._prj_root_dir

    def get_src_code_dst_dir(self):
        """Return the absolute path to the source output folder."""
        return os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['srcCodeDstDir']))

    def _parse_composition_config(self, file_config):
        """Parse the composition configuration from project config."""
        composition_config = {
            'compositionName': None,
            'compositionEnding': 'yml',
            'compositionArxml': file_config.get("compositionArxml", None),
            'customYamlInitFunctionName': file_config.get("customYamlInitFunctionName", None),
            'customYamlStepFunctionName': file_config.get("customYamlStepFunctionName", None),
            'generateExternalImplementationType': file_config.get("generateExternalImplementationType", True),
            'softwareComponentName': file_config.get("softwareComponentName", self.get_a2l_cfg()['name']),
            'asil': file_config.get('asil', 'QM'),
            'secure': file_config.get('secure', False),
            'includeStatic': file_config.get('includeStatic', True),
            'includeShared': file_config.get('includeShared', True),
            'includeSharedSwAddrMethod': file_config.get('includeSharedSwAddrMethod', None),
            'includeDiagnostics': file_config.get('includeDiagnostics', True),
            'includeNvm': file_config.get('includeNvm', True),
            'scaleMapsAndCurves': file_config.get('scaleMapsAndCurves', True),
        }
        composition_name = file_config.get("compositionName", None)
        if composition_name is not None:
            composition_config["compositionName"] = composition_name.split(".")[0]
            if "." in composition_name:
                composition_config["compositionEnding"] = composition_name.split(".")[1]
        return composition_config

    def get_composition_config(self, key=None):
        """Get the composition configuration from project config."""
        if key is None:
            return self._composition_config
        return self._composition_config[key]

    def get_car_com_dst(self):
        """Return the absolute path to the source output folder."""
        return os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['didCarCom']))

    def get_reports_dst_dir(self):
        """Get the destination dir for build reports.

        Returns:
            A path to the report files destination directory (with wildcards)

        """
        return os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['reportDstDir']))

    def get_all_reports_dst_dir(self):
        """Get the destination dir for build reports.

        Returns:
            A path to the report files destination directory (for all projects)

        """
        return os.path.join(self.get_root_dir(), "..", "..", "Reports")

    def get_log_dst_dir(self):
        """Return the absolute path to the log output folder.

        Returns:
            A path to the log files destination directory (with wildcards)

        """
        return os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['logDstDir']))

    def get_core_dummy_name(self):
        """Return the file name of the core dummy file from the config file.

        Returns:
            A file name for the core dummy files

        """
        path = os.path.join(self.get_src_code_dst_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['coreDummyFileName']))
        return path

    def get_feature_conf_header_name(self):
        """Return the feature configuration header file name.

        Returns:
            A file name for the feature config header file

        """
        return self._prj_cfg['ProjectInfo']['featureHeaderName']

    def get_ts_header_name(self):
        """Return the name of the ts header file, defined in the config file.

        Returns:
            The file name of the file defining all unit raster times

        """
        return self._prj_cfg['ProjectInfo']['tsHeaderName']

    def get_included_units(self):
        """Return a list of all the included units in the project.

        TODO:Consider moving this to the Feature Configs class if we start
        using our configuration tool for model inclusion and scheduling
        TODO:Consider calculate this on init and storing the result in the
        class. this method would the just return the stored list.
        """
        units_dict = self._unit_cfg['Rasters']
        units = []
        for unit in units_dict.values():
            units.extend(unit)
        return units

    def get_included_common_files(self):
        """Return a list of all the included common files in the project.

        Returns:
            included_common_files ([str]): The names of the common files which are included in the project.

        """
        return self._prj_cfg.get('includedCommonFiles', [])

    def _calc_all_units(self):
        """Return a list of all the units."""
        units = set()
        for runits in self._unit_cfg['Rasters'].values():
            units = units.union(set(runits))
        self._all_units = list(units)

    def get_includes_paths_flat(self):
        """Return list of paths to files to be included flat in source directory."""
        includes_paths = self._prj_cfg.get('includesPaths', [])
        return [os.path.join(self.get_root_dir(), os.path.normpath(path)) for path in includes_paths]

    def get_includes_paths_tree(self):
        """Return list of paths to files to included with directories in source directory."""
        includes_paths_tree = self._prj_cfg.get('includesPathsTree', [])
        return [os.path.join(self.get_root_dir(), os.path.normpath(path)) for path in includes_paths_tree]

    def get_all_units(self):
        """Return a list of all the units."""
        return self._all_units

    def get_prj_cfg_dir(self):
        """Return the directory containing the project configuration files.

        Returns:
            An absolute path to the project configuration files

        """
        return os.path.join(self._prj_root_dir,
                            self._prj_cfg['ProjectInfo']['configDir'])

    def get_scheduler_prefix(self):
        """Returns a prefix used to distinguish function calls in one project from
        similarly named functions in other projects, when linked/compiled together

        Returns:
        scheduler_prefix (string): prefix for scheduler functions.
        """
        return self._scheduler_prefix

    def get_local_defs_name(self):
        """Return a string which defines the file name of local defines.

        Returns:
            A string containing the wildcard file name local defines

        """
        return self._prj_cfg['ProjectInfo']['prjLocalDefs']

    def get_codeswitches_name(self):
        """Return a string which defines the file name of code switches.

        Returns:
            A string containing the wildcard file name code switches

        """
        return self._prj_cfg['ProjectInfo']['prjCodeswitches']

    def get_did_cfg_file_name(self):
        """Return the did definition file name.

        Returns:
            DID definition file name

        """
        return self._prj_cfg['ProjectInfo']['didDefFile']

    def get_prj_config(self):
        """Get the project configuration name from the config file.

        Returns:
            Project config name

        """
        return self._prj_cfg['ProjectInfo']["projConfig"]

    def get_a2l_name(self):
        """Get the name of the a2l-file, which the build system shall generate."""
        return self._prj_cfg['ProjectInfo']['a2LFileName']

    def get_ecu_info(self):
        """Return ecuSupplier and ecuType.

        Returns:
            (ecuSupplier, ecuType)
        """
        return (
            self._prj_cfg['ProjectInfo'].get('ecuSupplier', None),
            self._prj_cfg['ProjectInfo'].get('ecuType', '')
        )

    def get_xcp_enabled(self):
        """Return True/False whether XCP is enabled in the project or not.

        Returns:
            (bool): True/False whether XCP is enabled in the project or not

        """
        return self._prj_cfg['ProjectInfo'].get('enableXcp', True)

    def get_nvm_defs(self):
        """Return NVM-ram block definitions.

        The definitions contains the sizes of the six NVM areas
        which are defined in the build-system.

        Returns:
        NvmConfig dict from config file.

        """
        return self._prj_cfg['NvmConfig']

    def _get_inc_dirs(self, path):
        """Get the dirs with the models defined in the units config file.

        Model name somewhere in the path.
        """
        all_dirs = glob.glob(path)
        inc_units = self.get_included_units()
        psep = os.path.sep
        out = {}
        for dir_ in all_dirs:
            folders = dir_.split(psep)
            for inc_unit in inc_units:
                if inc_unit in folders:
                    out.update({inc_unit: dir_})
                    break
        return out

    def get_units_raster_cfg(self):
        """Get the units' scheduling raster config.

        I.e. which units are included, and in which
        rasters they are scheduled, and in which order.

        Returns:
            A dict in the following format.

        ::

            {
              "SampleTimes": {
                "NameOfRaster": scheduling time},
               "Rasters": {
                 "NameOfRaster": [
                   "NameOfFunction",
                   ...],
                 ...}
            }

        Example::

            {
              "SampleTimes": {
                "Vc10ms": 0.01,
                "Vc40ms": 0.04},
               "Rasters": {
                 "Vc10ms": [
                   "VcPpmImob",
                   "VcPpmPsm",
                   "VcPpmRc",
                   "VcPpmSt",
                   "VcPemAlc"],
                 "Vc40ms": [
                   "VcRegCh"]
            }

        """
        return self._unit_cfg

    def get_unit_cfg_dirs(self):
        """Get config dirs which matches the project config parameter prjUnitCfgDir.

        Furthermore, they should be included in the unit definition for this project

        Returns:
            A list with absolute paths to all unit config dirs
            included in the project

        """
        path = os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['prjUnitCfgDir']))
        return self._get_inc_dirs(path)

    def get_translation_files_dirs(self):
        """Get translation files directories, specified as a path regex in project
        config by key prjTranslationDir. If key is not present, will fall back to
        prjUnitCfgDir.

        Returns:
            A dictionary with absolute paths to all translation file dirs included
            in the project
        """

        if "prjTranslationDir" not in self._prj_cfg['ProjectInfo']:
            return self.get_unit_cfg_dirs()

        normpath_dir = os.path.normpath(self._prj_cfg['ProjectInfo']['prjTranslationDir'])
        path = os.path.join(self.get_root_dir(), normpath_dir)

        all_dirs = glob.glob(path)
        translation_dirs = {}
        for directory in all_dirs:
            file = pathlib.Path(directory).stem
            translation_dirs[file] = directory
        return translation_dirs

    def get_common_src_dir(self):
        """Get source dir which matches the project config parameter commonSrcDir.

        Returns:
            Absolute path to common source dir

        """
        return os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']['commonSrcDir']))

    def get_unit_src_dirs(self):
        """Get source dirs which matches the project config parameter prjUnitCfgDir.

        Furthermore, they should be included in the unit definition for this project

        Returns:
            A list with absolute paths to all source dirs included in the
            project

        """
        path = os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['prjUnitSrcDir']))
        return self._get_inc_dirs(path)

    def get_unit_mdl_dirs(self):
        """Get source dirs which matches the project config parameter prjUnitCfgDir.

        Furthermore, they should be included in the unit definition for this project

        Returns:
            A list with absolute paths to all model dirs included in the
            project

        """
        path = os.path.join(self.get_root_dir(),
                            os.path.normpath(self._prj_cfg['ProjectInfo']
                                             ['prjUnitMdlDir']))
        return self._get_inc_dirs(path)

    def get_use_global_const(self):
        """Get the name of the global constant module."""
        return self._prj_cfg['ProjectInfo']['useGlobalConst']

    def get_use_volatile_globals(self):
        """Get if global variables should be defined as volatile or not."""
        if 'useVolatileGlobals' in self._prj_cfg['ProjectInfo']:
            return self._prj_cfg['ProjectInfo']['useVolatileGlobals']
        return False

    def get_use_custom_dummy_spm(self):
        """Get path to file defining missing internal variables, if any.

        This file will be used instead of generating VcDummy_spm.c,
        to make it easier to maintain missing internal signals.

        Returns:
            customDummySpm (os.path): An absolute path to the custom dummy spm file, if existent.
        """
        if 'customDummySpm' in self._prj_cfg['ProjectInfo']:
            return os.path.join(
                self.get_root_dir(),
                os.path.normpath(self._prj_cfg['ProjectInfo']['customDummySpm'])
            )
        return None

    def get_use_custom_sources(self):
        """Get path to files with custom handwritten sourcecode, if any.

        Returns:
            customSources (os.path): A list of absolute paths to custom sources, if existent.
        """
        if 'customSources' in self._prj_cfg['ProjectInfo']:
            normalized_paths = (os.path.normpath(p) for p in self._prj_cfg['ProjectInfo']['customSources'])
            return [os.path.join(self.get_root_dir(), p) for p in normalized_paths]
        return None

    def get_if_cfg_dir(self):
        """Return the directory containing the interface configuration files.

        Returns:
            An absolute path to the interface configuration files

        """
        return os.path.join(self._prj_root_dir,
                            self._prj_cfg['ProjectInfo']['interfaceCfgDir'])

    def get_enum_def_dir(self):
        """Get path to dir containing simulink enumeration definitions, if any.

        Returns:
            enumDefDir (os.path): An absolute path to the simulink enumerations, if existent.
        """
        if 'enumDefDir' in self._prj_cfg['ProjectInfo']:
            return os.path.join(
                self.get_root_dir(),
                os.path.normpath(self._prj_cfg['ProjectInfo']['enumDefDir'])
            )
        return None


if __name__ == '__main__':
    # Function for testing the module
    BPC = BuildProjConfig('../../ProjectCfg.json')
