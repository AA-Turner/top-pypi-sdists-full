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

import os
import sys
import yaml

EXIT_ERROR = -1
YAML_FILE_EXT = ".yaml"


def help():
    """ Print how to use the script """
    print "Usage: %s <directory>" % sys.argv[0]


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


def main():
    """ Find all YAML files in the input directory and validate their syntax
    """
    if len(sys.argv) < 2:
        help()
        sys.exit(EXIT_ERROR)

    yaml_dir = sys.argv[1]
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


if __name__ == "__main__":
    main()

