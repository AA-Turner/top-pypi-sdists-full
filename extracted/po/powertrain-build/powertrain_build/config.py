# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Script to update configs based on c-files."""
import argparse
import copy
import glob
import itertools
import json
import operator
import os
import re
import sys
from pprint import pformat
from typing import List, Optional

from powertrain_build.lib import logger

LOGGER = logger.create_logger('config')


class ConfigParserCommon:
    """Parser for c and h files."""

    def __init__(self):
        """Initialize common properties."""
        self.ifs = []
        self.def_map = {}
        self.configs = {}
        self.code_regexes = [(re.compile(r'^\s*#(?P<type>if|ifdef|ifndef) (?P<condition>.*)$'),
                              self.parse_if),
                             (re.compile(r'^\s*#else.*$'), self.parse_else),
                             (re.compile(r'^\s*#define (\w*)\s?(.*)?'), self.parse_defines),
                             (re.compile(r'^\s*#endif.*$'), self.parse_endif)]

    def parse_line(self, line):
        """Process each regex.

        Arguments:
        line (str): line of code
        """
        for regex, function in self.code_regexes:
            self.process_regex(line, regex, function)

    @staticmethod
    def process_regex(line, regex, function):
        """Process one regex.

        Arguments:
        line (str): line of code
        regex (object): compiled re object
        function (function): function to run if regex matches
        """
        match = regex.match(line)
        if match:
            function(*match.groups())

    def parse_file_content(self, file_content):
        """Parse each line in the file.

        Arguments:
        file_contents (list): Contents of a file
        """
        for line in file_content:
            self.parse_line(line)

    def parse_if(self, if_type, condition):
        """Parse an if-preprocessor statement.

        Arguments:
        match (object): match object
        """
        self.ifs.append((if_type, condition))

    def parse_else(self):
        """Stub for parsing."""
        raise NotImplementedError

    def parse_defines(self, variable, definition):
        """Stub for parsing."""
        raise NotImplementedError

    def parse_endif(self):
        """Parse an endif-preprocessor statement.

        Arguments:
        match (object): match object
        """
        if self.ifs:
            c_type, condition = self.ifs.pop()
            LOGGER.debug('Removing %s %s', c_type, condition)

    @staticmethod
    def read_file(c_file):
        """Read file.

        Arguments:
        c_file (str): Full path to a file
        """
        file_content = ''
        with open(c_file, encoding='latin-1') as file_handle:
            for line in file_handle:
                file_content += line
        out = re.sub(r'/\*.*?\*/', '', file_content, flags=re.S).splitlines()
        return out

    @staticmethod
    def compose_and(conditions):
        """Return and conditions."""
        return f"({' && '.join(conditions)})"

    @staticmethod
    def compose_or(conditions):
        """Return and conditions."""
        return f"({' || '.join(conditions)})"

    @staticmethod
    def sort_u(item):
        """Get a unique list of configs.

        Can handle unhashable elements.

        Arguments:
        item (list): list to unique elements of.
        """
        return map(
            operator.itemgetter(0),
            itertools.groupby(sorted(item)))


class CConfigParser(ConfigParserCommon):
    """Parser for c-files."""

    def set_regexes(self, variable):
        """Create regexes to find configs for a single variable.

        Arguments:
        variable (str): variable
        """
        self.code_regexes.append((re.compile(r'.*\b({})\b.*'.format(variable)), self.parse_code))

    def parse_defines(self, variable, definition):
        """Parse defines in c-files."""
        if definition:
            LOGGER.warning('Configuration using %s might be wrong. Set to %s in the c-file', variable, definition)
        if variable:
            if self.ifs and variable == self.ifs[-1][-1]:
                self.ifs.pop()

    def parse_else(self):
        """Parse defines in c-files."""
        if_type, condition = self.ifs.pop()
        self.ifs.append(('else' + if_type, condition))

    def parse_code(self, variable):
        """Parse a line with the variable we are looking for.

        Arguments:
        match (object): match object
        """
        LOGGER.debug('Found %s with %s', variable, self.ifs)
        if variable not in self.configs:
            self.configs[variable] = []
        # In this case, we add to a list which should be joined by 'and'
        self.configs[variable].append(copy.deepcopy(self.ifs))

    @staticmethod
    def define_config(condition, header_map, ctype):
        """Get a config from the header map.

        Arguments:
        condition
        header_map
        ctype
        """
        if ctype == 'ifdef':
            if condition in header_map.keys():
                config = header_map[condition]
            else:
                config = 'ALWAYS_ACTIVE'
                LOGGER.error('Define not found: %s %s in %s', ctype, condition, header_map)
        if ctype == 'ifndef':
            if condition in header_map.keys():
                config = '!(' + header_map[condition] + ')'
            else:
                config = 'NEVER_ACTIVE'
                LOGGER.error('Define not found: %s %s in %s', ctype, condition, header_map)
        if ctype == 'elseifdef':
            if condition in header_map.keys():
                config = f'!({header_map[condition]})'
            else:
                config = 'NEVER_ACTIVE'
                LOGGER.error('Define not found: %s %s in %s', ctype, condition, header_map)
        if ctype == 'elseifndef':
            if condition in header_map.keys():
                config = header_map[condition]
            else:
                config = 'ALWAYS_ACTIVE'
                LOGGER.error('Define not found: %s %s in %s', ctype, condition, header_map)
        return config

    def get_configs(self, variable, header_map):
        """Get configs.

        Does not remove redundant configs.
        """
        configs = []
        if variable not in self.configs:
            LOGGER.warning('%s not found. Inport that leads to terminal suspected.', variable)
            return '(NEVER_ACTIVE)'
        for config in self.configs[variable]:
            tmp_config = []
            for ctype, condition in config:
                if ctype == 'if':
                    if condition in header_map.keys():
                        LOGGER.debug('Redefining %s as %s', condition, header_map[condition])
                        tmp_config.append(header_map[condition])
                    else:
                        tmp_config.append(condition)
                elif ctype == 'elseif':
                    if condition in header_map.keys():
                        LOGGER.debug('Redefining %s as !(%s)', condition, header_map[condition])
                        tmp_config.append('!(' + header_map[condition] + ')')
                    else:
                        LOGGER.debug('Negating %s to !(%s)', condition, condition)
                        tmp_config.append('!(' + condition + ')')
                else:
                    tmp_config.append(self.define_config(condition, header_map, ctype))
            if not tmp_config and config:
                LOGGER.warning('Config not found: %s from %s', config, self.configs)
                tmp_config.append('ALWAYS_ACTIVE')
                LOGGER.info('Current config: %s', tmp_config)
            elif not config:
                LOGGER.debug('No config, always active')
                tmp_config.append('ALWAYS_ACTIVE')
            configs.append(self.compose_and(list(self.sort_u(tmp_config))))
        return self.compose_or(list(self.sort_u(configs)))


class JsonConfigHandler:
    """Handle the json config."""

    def __init__(self, cparser, header_map):
        """Initialize handling of one json file.

        Arguments:
        parser (obj): c-parser
        header_map (dict): defines in the header files
        """
        self.cparser = cparser
        self.header_map = header_map

    def traverse_unit(self, struct, setup=True):
        """Go through a data structure and look for configs to update.

        Arguments:
        struct (dict): data to go through
        parser (obj): parsing object
        header_map (dict): dict of defines
        setup (bool): Set up the parser obecjt (True) or replace configs (False)
        """
        for name, data in struct.items():
            if isinstance(data, dict) and name != 'API_blk':
                # Core data has the propety config, not configs
                if data.get('API_blk') is not None or data.get('configs') is not None:
                    if setup:
                        self.cparser.set_regexes(name)
                    else:
                        data['configs'] = self.cparser.get_configs(name, self.header_map)
                else:
                    self.traverse_unit(data, setup)

    def update_config(self, struct, c_code, header_map=None):
        """Update dict.

        Arguments:
        data (dict): A configuration dict or subdict
        c_code (list): code part of a c-file
        """
        if header_map is None:
            header_map = {}
        # Set up regexes:
        self.traverse_unit(struct, setup=True)
        self.cparser.parse_file_content(c_code)
        self.traverse_unit(struct, setup=False)

    @staticmethod
    def read_config(config_file):
        """Read config file.

        Arguments:
        config_file (str): Full path to config file
        """
        with open(config_file, encoding='latin-1') as unit_json:
            unit_config = json.load(unit_json)
        return unit_config

    @staticmethod
    def write_config(config_file, unit_config):
        """Write config file.

        Arguments:
        config_file (str): Full path to config file
        unit_config (dict): Unit config to write to file
        """
        with open(config_file, 'w', encoding="utf-8") as unit_json:
            unit_json.write(json.dumps(unit_config, indent=2))


class HeaderConfigParser(ConfigParserCommon):
    """Parser for c-files."""

    def set_defines(self, defines):
        """Set already defined defines."""
        self.def_map = defines

    def parse_else(self):
        """Crash if this is found in a header."""
        raise NotImplementedError

    def parse_defines(self, variable, definition):
        """Parse defines in c-files."""
        if self.ifs and self.ifs[-1][0] == 'ifndef' and variable == self.ifs[-1][-1]:
            # We have encountered a case of:
            #
            # #ifndef a
            # #define a
            # #define b
            #
            # Then we don't want b to be dependent on a not being defined.

            c_type, condition = self.ifs.pop()
            LOGGER.debug('Removing now defined %s from ifs: %s %s', variable, c_type, condition)
        if definition:
            LOGGER.info('Redefining %s as %s', variable, definition)
            # Here we ignore the potential #if statements preceding this.
            # Have not encountered a case where that matters.
            # This structure does not support that logic.
            # Potential for bugs.
            self.configs[variable] = [definition]
        elif self.ifs:
            config = self.get_configs(self.ifs, self.def_map)
            LOGGER.info('Defining %s as %s', variable, config)
            if variable not in self.configs:
                self.configs[variable] = []
            self.configs[variable].append(copy.deepcopy(config))
            self.def_map.update({variable: copy.deepcopy(config)})

    @staticmethod
    def define_config(condition, header_map, ctype):
        """Get a config from the header map.

        Arguments:
        condition
        header_map
        ctype
        """
        if ctype == 'ifdef':
            if condition in header_map.keys():
                LOGGER.debug('returning %s as %s', condition, header_map[condition])
                config = header_map[condition]
            else:
                config = 'ALWAYS_ACTIVE'
                LOGGER.warning('Not Implemented Yet: %s %s', ctype, condition)
        if ctype == 'ifndef':
            if condition in header_map.keys():
                LOGGER.debug('returning %s as %s', condition, header_map[condition])
                config = '!(' + header_map[condition] + ')'
            else:
                config = 'ALWAYS_ACTIVE'
                LOGGER.warning('Not Implemented Yet: %s %s', ctype, condition)
        return config

    def process_config(self, inconfigs, header_map):
        """Process configs."""
        configs = []
        for config in inconfigs:
            LOGGER.debug('Current config: %s', config)
            if isinstance(config, list):
                configs.append(self.process_config(config, header_map))
            else:
                ctype, condition = config
                if ctype == 'if':
                    if condition in header_map.keys():
                        configs.append(header_map[condition])
                    else:
                        configs.append(condition)
                elif ctype in ['ifdef', 'ifndef']:
                    configs.append(self.define_config(condition, header_map, ctype))
                else:
                    LOGGER.error('Not Implemented: %s', ctype)
            if not configs:
                configs = ['ALWAYS_ACTIVE']
        return list(self.sort_u(configs))

    def get_configs(self, configs, header_map):
        """Get configs.

        Does not remove redundant configs.
        """
        configs = self.process_config(configs, header_map)
        if len(configs) > 1:
            return self.compose_and(list(self.sort_u(configs)))
        return configs[0]

    def get_config(self):
        """Get the header map."""
        header_map = self.def_map
        for header_def, configs in self.configs.items():
            header_map[header_def] = self.compose_or(configs)
        return header_map


class ProcessHandler:
    """Class to collect functions for the process."""

    PARSER_HELP = "Parse configs.json and c-files, to update code switch configs"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser):
        """Parse arguments."""
        parser.description = "Parse configs.json and c-files, to update code switch configs"

        subparser = parser.add_subparsers(
            title='Operation mode',
            dest='mode',
            help="Run chosen files on in a number of directories",
        )
        dir_parser = subparser.add_parser(
            'models',
            help="Run for one or multiple models. Script finds files generated from the model(s).")
        dir_parser.add_argument('models', nargs='+',
                                help="Space separated list of model directories")

        file_parser = subparser.add_parser('files',
                                           help="Choose specific files. Mainly for manually written configs.")
        file_parser.add_argument('c_file',
                                 help="Full path to C-file")
        file_parser.add_argument('config_file',
                                 help="Full path to config file")
        file_parser.add_argument('--aux_file',
                                 help="Full path to tl_aux file. (Optional) ")
        file_parser.add_argument('--local_file',
                                 help="Full path to OPort file. (Optional) ")

        parser.set_defaults(func=ProcessHandler.main)

    @staticmethod
    def get_files(model_path):
        """Get file paths from model path.

        Arguments:
        model_path (str): Path to a model (.mdl)

        Returns:
        local_file (str): Path to model_OPortMvd_LocalDefs.h
        aux_file (str): Path to tl_aux_defines_model.h
        config_file (str): Path to config_model.json
        c_file (str): Path to model.c

        """
        model_dir = os.path.dirname(model_path)
        LOGGER.info('Processing %s', model_dir)
        model_name = os.path.basename(model_dir)
        local_file = os.path.join(model_dir, 'pybuild_src', f'{model_name}_OPortMvd_LocalDefs.h')
        # aux_file does not contain the whole model-name if it is too long.
        aux_file = os.path.join(model_dir, 'pybuild_src', f'tl_aux_defines_{model_name[2:12]}.h')
        config_file = os.path.join(model_dir, 'pybuild_cfg', f'config_{model_name}.json')
        clean_model_name = model_name.split('__')[0]
        c_file = os.path.join(model_dir, 'pybuild_src', f'{clean_model_name}.c')
        return local_file, aux_file, c_file, config_file

    @staticmethod
    def update_config_file(c_file, config_file, header_map):
        """Update one config file.

        Arguments:
        c_file (str): Full path to c-file
        config_file (str): Full path to config.json
        oport_file (str): Full path to OPortMvd_LocalDefs.h (Optional)
        """
        LOGGER.info('Updating %s based on %s', config_file, c_file)
        cparser = CConfigParser()
        c_code = cparser.read_file(c_file)
        json_handler = JsonConfigHandler(cparser, header_map)
        unit_config = json_handler.read_config(config_file)
        json_handler.update_config(unit_config, c_code, header_map)
        json_handler.write_config(config_file, unit_config)

    @staticmethod
    def get_header_config(header_file, def_map):
        """Get header config.

        Arguments:
        c_file (str): Full path to c-file
        config_file (str): Full path to config.json
        oport_file (str): Full path to OPortMvd_LocalDefs.h (Optional)
        """
        if header_file is None:
            LOGGER.info('File not found: %s', header_file)
            return def_map
        if not os.path.isfile(header_file):
            LOGGER.info('File not found: %s', header_file)
            model_dir = os.path.dirname(header_file)
            for tl_aux_file in glob.glob(os.path.join(model_dir, 'tl_aux*')):
                LOGGER.warning('Looking for %s?', tl_aux_file)
            return def_map
        LOGGER.info('Parsing %s', header_file)
        parser = HeaderConfigParser()
        header_code = parser.read_file(header_file)
        parser.set_defines(def_map)
        parser.parse_file_content(header_code)
        LOGGER.debug('Header configs: %s', pformat(parser.configs))
        return parser.get_config()

    @classmethod
    def main(cls, args: argparse.Namespace):
        """Run the main function of the script."""
        if args.mode == 'files':
            LOGGER.info('Using manually supplied files %s', args)
            local_defs = cls.get_header_config(args.local_file, {})
            aux_defs = cls.get_header_config(args.aux_file, local_defs)
            cls.update_config_file(args.c_file, args.config_file, aux_defs)
        else:
            for model in args.models:
                local_file, aux_file, c_file, config_file = cls.get_files(model)
                local_defs = cls.get_header_config(local_file, {})
                aux_defs = cls.get_header_config(aux_file, local_defs)
                if os.path.isfile(c_file) and os.path.isfile(config_file):
                    cls.update_config_file(c_file, config_file, aux_defs)


def main(argv: Optional[List[str]] = None):
    """Run main function."""
    parser = argparse.ArgumentParser(ProcessHandler.PARSER_HELP)
    ProcessHandler.configure_parser(parser)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
