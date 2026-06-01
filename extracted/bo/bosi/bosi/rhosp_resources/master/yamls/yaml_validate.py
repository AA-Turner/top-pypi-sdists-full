#!/usr/bin/env python
# Copyright 2018 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import os
import sys
import yaml

EXIT_ERROR = -1
YAML_FILE_EXT = ".yaml"
SUPPORTED_BOND = ['linux_bond']


class BsnParser(argparse.ArgumentParser):
    """Overrides the error handler to print help text each time with error.

    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def validate_yaml_bridge(yaml_file_path):
    """
    Validate the bridge info in the controller or compute's yaml file given
    as param.

    :param yaml_file_path:
    :return:
    """
    valid_bridge = False
    last_exception = None
    try:
        yaml_file = open(yaml_file_path, 'r')
        config_yaml = yaml.load(yaml_file)
        network_config_list = (config_yaml['resources']['OsNetConfigImpl'][
                                   'properties']['config']['str_replace'][
                                   'params']['$network_config']['network_config'])
        for config in network_config_list:
            config_type = config.get('type')
            # if its neither ivs_bridge or ovs_bridge, move on
            if config_type != 'ivs_bridge' and config_type != 'ovs_bridge':
                last_exception = Exception('Bridge type must be either '
                                           'ivs_bridge or ovs_bridge, neither '
                                           'found in config.')
                continue

            # for ivs_bridge, no other checks required. return True
            if config_type == 'ivs_bridge':
                valid_bridge = True
                break

            # for ovs_bridge, check that bridge name is br-ex
            if config_type == 'ovs_bridge':
                bridge_name = config.get('name')
                # name of the bridge should be either 'br-ex' or 'bridge_name'
                # when it is 'bridge_name', it is autoconfigured and the
                # default is 'br-ex'
                # anything else is invalid
                if ((bridge_name != 'br-ex') and
                        ('bridge_name' not in str(bridge_name))):
                    last_exception = (
                        Exception('In case of ovs_bridge, bridge name must be '
                                  'br-ex for auto-interface-group to work. If '
                                  'not please create manual interface-group in '
                                  'BCF.'))
                    continue
                members = config.get('members')
                for member in members:
                    # also check that type of bond for interface is supported
                    if member.get('type') not in SUPPORTED_BOND:
                        last_exception = (
                            Exception('Bond type for the interfaces under the '
                                      'bridge is not supported. Please use one '
                                      'of %(SUPPORTED_BOND)s' %
                                      {'SUPPORTED_BOND': SUPPORTED_BOND}))
                        continue
                    # everythig checks out, return True
                    valid_bridge = True
                    break
        if not valid_bridge:
            raise last_exception
    except IOError as fileError:
        print("INVALID file passed as argument. \nERROR: %(error_string)s" %
              {'error_string': fileError})
    except Exception as e:
        print("ERROR while checking bridge config in yaml: %(error_string)s" %
              {'error_string': e})

    if valid_bridge:
        print ("VALID bridge configuration in %s" % yaml_file_path)
    else:
        # we looped through the config, did not find anything matching completely
        # return False
        print ("INVALID bridge configuration in %s. Please check "
               "deployment guide before proceeding." % yaml_file_path)


def check_yaml_syntax(f):
    """ Check the syntax of the given YAML file.
        return: True if valid, False otherwise
    """
    with open(f, 'r') as stream:
        try:
            yaml.load(stream)
        except yaml.YAMLError as exc:
            print "%s: Invalid YAML syntax.\n%s\n" % (f, exc)
            return False
    return True


def check_yaml_syntax_dir(yaml_dir):
    if not os.path.isdir(yaml_dir):
        print "ERROR: Invalid directory %s" % yaml_dir
        sys.exit(EXIT_ERROR)

    all_valid = True
    for root, dirs, files in os.walk(yaml_dir):
        for f in files:
            if YAML_FILE_EXT in f:
                fname = root + "/" + f
                valid = check_yaml_syntax(fname)
                if valid:
                    print "%s: Valid YAML syntax" % fname
                else:
                    all_valid = False
        break

    if all_valid:
        print "All files have valid YAML syntax"
    else:
        print "Some files have invalid YAML syntax"


def main():
    parser = BsnParser()
    either_one_group = parser.add_mutually_exclusive_group(required=True)
    either_one_group.add_argument("-b", "--check-bridge-config",
                                  help="RHOSP controller.yaml or compute.yaml "
                                       "or ceph-storage.yaml with the bridge "
                                       "configuration to be validated.")
    either_one_group.add_argument("-s", "--check-syntax",
                                  help="Find all YAML files in the input "
                                       "directory and validate their syntax.")
    args = parser.parse_args()

    if args.check_bridge_config:
        validate_yaml_bridge(args.check_bridge_config)
        return

    if args.check_syntax:
        check_yaml_syntax_dir(args.check_syntax)
        return


if __name__ == "__main__":
    main()

