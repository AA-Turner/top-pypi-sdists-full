# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Feature configuration (codeswitches) module."""

import copy
import glob
import os
import re
from pprint import pformat

from powertrain_build.lib.helper_functions import deep_dict_update
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.xlrd_csv import WorkBook


class FeatureConfigs(ProblemLogger):
    """Hold feature configurations read from SPM_Codeswitch_Setup*.csv config files.

    Provides methods for retrieving the currently
    used configurations of a unit.
    """

    convs = (('~=', '!='), ('~', ' not '), ('!', ' not '), (r'\&\&', ' and '),
             (r'\|\|', ' or '))

    def __init__(self, prj_config):
        """Constructor.

        Args:
            prj_config (BuildProjConfig): configures which units are active in the current project and where
                                          the codeswitches files are located

        """
        super().__init__()
        self._if_define_dict = {}
        self._build_prj_config = prj_config
        self._missing_codesw = set()
        # Get the config switches configuration
        self._set_config(self._parse_all_code_sw_configs())
        self._parse_all_local_defs()
        self._add_local_defs_to_tot_code_sw()

    def __repr__(self):
        """Get string representation of object."""
        return pformat(self.__code_sw_cfg.keys())

    def _parse_all_code_sw_configs(self):
        """Parse all SPM_Codeswitch_Setup*.csv config files.

        Returns:
            dict: with the projects as keys, and the values are
                another dict with the config-parameter and it's value.

        """
        # TODO: Change this when condeswitches are moved to model config
        # cfg_paths = self._build_prj_config.get_unit_mdl_dirs('all')
        cfg_paths = [self._build_prj_config.get_prj_cfg_dir()]
        cfg_fname = self._build_prj_config.get_codeswitches_name()
        cfg_files = []
        for cfg_path in cfg_paths:
            cfg_files.extend(glob.glob(os.path.join(cfg_path, cfg_fname)))
        self.debug('cfg_paths: %s', pformat(cfg_paths))
        self.debug('cfg_fname: %s', pformat(cfg_fname))
        self.debug('cfg_files: %s', pformat(cfg_files))
        conf_dict = {}
        for file_ in cfg_files:
            conf_dict = deep_dict_update(conf_dict, self._parse_code_sw_config(file_))
        return conf_dict

    def _parse_code_sw_config(self, file_name):
        """Parse the SPM_Codeswitch_Setup.csv config file.

        Returns:
            dict: with the projects as keys, and the values are
                another dict with the config-parameter and it's value.

        """
        self.debug('_parse_code_sw_config: %s', file_name)
        wbook = WorkBook(file_name)
        conf_dict = {'NEVER_ACTIVE': 0,
                     'ALWAYS_ACTIVE': 1}
        # TODO: handle sheet names in a better way!
        wsheet = wbook.single_sheet()
        prjs = [d.value for d in wsheet.row(0)[2:]]
        prj_row = enumerate(prjs, 2)
        for col, prj in prj_row:
            if prj != self._build_prj_config.get_prj_config():
                self.debug('Skipping %s', prj)
                continue
            for r_nbr in range(1, wsheet.nrows):
                row = wsheet.row(r_nbr)
                conf_par = row[0].value.strip().replace('.', '_')
                val = row[col].value
                if not isinstance(val, str):
                    conf_dict[conf_par] = val
                elif val.lower().strip() == 'na' or val.lower().strip() == 'n/a':
                    conf_dict[conf_par] = 0
                else:
                    self.warning('Unexpected codeswitch value %s = "%s". Ignored!', row[0].value.strip(), val)
            return conf_dict
        return conf_dict

    def _recursive_subs(self, m_def, code_sws):
        """Recursivly replaces macro definitions with values."""
        # find and replace all symbols with values
        symbols = re.findall(r'(?!(?:and|or|not)\b)(\b[a-zA-Z_]\w+)', m_def)
        m_def_subs = m_def
        for symbol in symbols:
            if symbol in code_sws:
                m_def_subs = re.sub(symbol, str(code_sws[symbol]), m_def_subs)
            elif symbol in self._if_define_dict:
                m_def_subs = re.sub(symbol, str(self._if_define_dict[symbol]), m_def_subs)
                m_def_subs = self._recursive_subs(m_def_subs, code_sws)
            else:
                self.critical('Symbol %s not defined in config switches.', symbol)
                return None
        return m_def_subs

    def _add_local_defs_to_tot_code_sw(self):
        """Add the defines from the LocalDefs.h files to the code switch dict."""
        for macro, m_def in self._if_define_dict.items():
            tmp_subs = self._recursive_subs(m_def, self.__tot_code_sw)
            if tmp_subs is None:
                continue
            self.__tot_code_sw[macro] = eval(tmp_subs)

    def get_preprocessor_macro(self, nested_code_switches):
        """Get the #if macro string for a code switch configuration from a unit config json file.

        Args:
            nested_code_switches(list()): list of lists of code switches from unitconfig
        return:
            string: A string with an #if macro that defines if the code should be active
                    '#if (<CS1> && <CS2>) || (<CS3> && <CS4>)'
        """
        if_macro_and = []
        if not isinstance(nested_code_switches, list):
            self.warning("Unitconfig codeswitches should be in a nested list")
            nested_code_switches = [nested_code_switches]
        if not isinstance(nested_code_switches[0], list):
            self.warning("Unitconfig codeswitches should be in a nested list")
            nested_code_switches = [nested_code_switches]

        for code_switches in nested_code_switches:
            if isinstance(code_switches, str):
                code_switches = [code_switches]
            if_macro_and.append(f"( { ' && '.join(code_switches) } )")
        if_macro_string = f"#if {' || '.join(if_macro_and)}" if if_macro_and else ""
        all_projects = re.search('all', if_macro_string, re.I)
        if all_projects:
            return ""
        return if_macro_string

    def gen_unit_cfg_header_file(self, file_name):
        """Generate a header file with preprocessor defines needed to configure the SW.

        Args:
            file_name (str): The file name (with path) of the unit config header file

        """
        with open(file_name, 'w', encoding="utf-8") as f_hndl:
            _, fname = os.path.split(file_name)
            fname = fname.replace('.', '_').upper()
            f_hndl.write(f'#ifndef {fname}\n')
            f_hndl.write(f'#define {fname}\n\n')
            conf_sw = self.__code_sw_cfg
            for key_, val in conf_sw.items():
                if val == "":
                    self.warning('Code switch "%s" is missing a defined value', key_)
                f_hndl.write(f'#define {key_} {val}\n')
            f_hndl.write(f'\n#endif /* {fname} */\n')

    def _eval_cfg_expr(self, elem):
        """Convert matlab config expression to python expression.

        Uses the tuple self.convs, and evaluates the result using
        self.__code_sw_cfg[config]
        This function does not handle the complex definitions made outside
        the dict.

        Args:
            elem (str): element string

        Returns:
            Bool: True if config is active, False if not.

        """
        res = re.search('all', elem, re.I)
        if res is not None:
            return True
        # modify all matlab expressions
        elem_tmp = elem
        # find and replace all symbols with values
        symbols = re.findall(r'[a-zA-Z_]\w+', elem_tmp)
        code_sw_dict = self.__tot_code_sw
        for symbol in symbols:
            try:
                elem_tmp = re.sub(fr'\b{symbol}\b', str(code_sw_dict[symbol]), elem_tmp)
            except KeyError:
                if symbol not in self._missing_codesw:
                    self.critical('Missing %s in CodeSwitch definition', symbol)
                    self._missing_codesw.add(symbol)
                return False
        # convert matlab/c to python expressions
        for conv in self.convs:
            elem_tmp = re.sub(conv[0], conv[1], elem_tmp)
        # evaluate and return result
        return eval(elem_tmp)

    def check_if_active_in_config(self, config_def):
        """Check if a config is active in the current context.

        Takes a collection of config strings and checks if this config definition is active
        within the current configuration. The structure of the provided string collection
        determines how the config definition is evaluated. (logical and/or expressions)

        list of list of config strings
            [[*cs1* and *cs2*] or [*cs3* and *cs4*]].

        list of config strings
            [*cs1* and *cs2*]

        single config string
            *cs1*

        Args:
            config_def (list): the config definitions as described above

        Returns:
            Bool: True if active the current configuration

        """
        if not config_def:
            return True
        # format the input to a list of list of strings
        if isinstance(config_def, str):
            c_def = [[config_def]]
        elif isinstance(config_def, list) and isinstance(config_def[0], str):
            c_def = [config_def]
        else:
            c_def = config_def
        eval_ = False
        for or_elem in c_def:
            for and_elem in or_elem:
                eval_ = self._eval_cfg_expr(and_elem)
                if not eval_:
                    break
            if eval_:
                break
        return eval_

    def _conv_mlab_def_to_py(self, matlab_def):
        """Convert matlab syntax to python syntax.

        TODO: Move this functionality to the matlab-scripts, which are
        run on the local machine.

        """
        m_def_tmp = matlab_def
        for from_, to_ in self.convs:
            m_def_tmp = re.sub(from_, to_, m_def_tmp)
        return m_def_tmp

    def _parse_local_def(self, file_data):
        """Parse one local define file."""
        res = re.findall(r'#if\s+(.*?)(?<!\\)$\s*#define (\w+)\s+#endif',
                         file_data, flags=re.M | re.DOTALL)
        def_wo_if_endif = re.sub(r'#if(.*?)#endif', '', file_data, flags=re.M | re.DOTALL)
        one_line_def = re.findall(r'#define\s+(\w+)\s+(.+?)(?:(?://|/\*).*?)?$',
                                  def_wo_if_endif, flags=re.M)
        res.extend([(v, d) for (d, v) in one_line_def])
        # remove line break '\' characters and line break
        self._if_define_dict.update({d: self._conv_mlab_def_to_py(re.sub(r'\s*?\\$\s*', ' ', i))
                                     for (i, d) in res})

    def _parse_all_local_defs(self):
        """Parse all local define files."""
        def_paths = self._build_prj_config.get_unit_src_dirs()
        ld_fname = self._build_prj_config.get_local_defs_name()
        loc_def_files = []
        for def_path in def_paths.values():
            loc_def_files.extend(glob.glob(os.path.join(def_path, ld_fname)))
        for file_ in loc_def_files:
            with open(file_, 'r', encoding="utf-8") as fhndl:
                data = fhndl.read()
                self._parse_local_def(data)
        self.debug('self._if_define_list:\n%s\n', pformat(self._if_define_dict))

    def _set_config(self, code_sw):
        """Set config for code switches.

        Useful for unit testing.

        Args:
            code_sw
        """
        # __tot_code_sw
        self.__code_sw_cfg = code_sw
        self.__tot_code_sw = copy.deepcopy(self.__code_sw_cfg)
