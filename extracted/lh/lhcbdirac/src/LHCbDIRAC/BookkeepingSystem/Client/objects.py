###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""reimplementation of the dictionary."""

from DIRAC import gLogger


def prepend(string, indent="___"):
    """add string."""
    string = string.strip("\n")
    tokens = string.split("\n")
    newstr = ""
    for token in tokens[0:-1]:
        newstr += indent + token + "\n"
    newstr += indent + tokens[-1]
    return newstr


class Entity(dict):
    """Entity class."""

    def __init__(self, properties={}):
        """initialize an Entity."""
        if isinstance(properties, list):
            for key in properties:
                self[key] = None  # find a simpler way to declare all keys
        elif isinstance(properties, dict):
            if properties:
                self.update(properties.items())
        else:
            gLogger.warn("Cannot create Entity from properties:" + str(properties))

    def __repr__(self):
        """print."""
        if not self:
            rString = "{\n " + str(None) + "\n}"
        else:
            rString = "{"
            keys = self.keys()
            if "fullpath" in keys:
                rString += "\n" + "fullpath: " + str(self["fullpath"])
            for key in keys:
                if key not in ("name", "level", "fullpath", "expandable", "selection", "method", "showFiles"):
                    rString += "\n " + str(key) + " : "
                    value = self[key]
                    # some entities do not have this key. Ignore then.
                    try:
                        if key in self["not2show"]:
                            rString += "-- not shown --"
                            continue
                    except Exception:
                        pass
                    if isinstance(value, dict):
                        value = Entity(value)
                        rString += "\n" + prepend(str(value), (len(str(key)) + 3) * " ")
                    else:
                        rString += str(value)
            else:
                for key in keys:
                    if key not in ("name", "fullpath", "FileName"):
                        value = self[key]
                        if isinstance(value, dict):
                            value = Entity(value)
                            rString += "\n" + prepend(str(value), (len(str(key)) + 3) * " ")
                        else:
                            rString += str(value)

            rString += "\n}"
        return rString
