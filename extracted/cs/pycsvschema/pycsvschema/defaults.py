#!/usr/bin/python
# -*-coding: utf-8 -*-

# Default value is not required for each option

# root
FIELDS = []
ADDITIONALFIELDS = True
DEFINITIONS = {}
DEPENDENCIES = {}
EXACTFIELDS = False
# MAXFIELDS = math.inf
# MINFIELDS = 0
MISSINGVALUES = [""]
PATTERNFIELDS = {}

# field
FIELDS_ENUM = []
FIELDS_EXCLUSIVEMAXIMUM = False
FIELDS_EXCLUSIVEMININUM = False
# FIELDS_MAXINUM = math.inf
# FIELDS_MININUM = 0
# FIELDS_MAXLENGTH = math.inf
# FIELDS_MINLENGTH = 0
FIELDS_TYPE = "string"
FIELDS_FORMAT = ""
FIELDS_GROUPCHAR = ""
FIELDS_TRUEVALUES = {"TRUE", "True", "true", "1"}
FIELDS_FALSEVALUES = {"FALSE", "False", "false", "0"}
FIELDS_FORMAT_DATETIME_PATTERN = "%Y-%m-%dT%H:%M:%S.%f%z"
FIELDS_TYPE_STRING_PATTERN = ""
FIELDS_REQUIRED = False
