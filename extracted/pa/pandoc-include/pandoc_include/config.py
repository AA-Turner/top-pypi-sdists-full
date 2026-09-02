import re
import ast
import os
import json
import tempfile
import uuid

import panflute as pf


CONFIG_KEYS = {
    "startLine": int,
    "endLine": int,
    "snippetStart": str,
    "snippetEnd": str,
    "xslt": str,
    "includeSnippetDelimiters": bool,
    "incrementSection": int,
    "dedent": int,
    "format": str,
    "raw": str
}

def parseBoolValue(val):
    # use 1 or 0 (otherwise default to true if not empty)
    return val and val != "0"

# Keys for env config in a singleton pattern to ensure consistent access 
# across parent and child processes without re-reading environment variables 
# multiple times. This also allows for future expansion of config options 
# without changing the interface.
class Env:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # guard against reinitialisation
        if hasattr(self, "_initialized"):
            return
        # Throw error when included file not found
        self.NotFoundError  = parseBoolValue(os.environ.get("PANDOC_INCLUDE_NOT_FOUND_ERROR", "0"))
        # Pandoc binary for parsing included files
        self.PandocBin      = os.environ.get("PANDOC_BIN") or None
        # The identifier for this run (unique per execution, used for temp file naming)
        # Generate a unique run ID if not already set (e.g. by a parent process) to allow
        # multiple concurrent runs without conflict. Use the environment to ensure sub-process
        # can access the same run ID. This also allows the run ID to be set externally if needed.
        if os.environ.get("PANDOC_INCLUDE_RUN_ID") is None:
            os.environ["PANDOC_INCLUDE_RUN_ID"] = str(uuid.uuid4())
        self.RunId          = os.environ["PANDOC_INCLUDE_RUN_ID"]
        # Temp file for storing options and state between parent and child processes. 
        # Use environment variable to allow override and ensure sub-processes can access 
        # the same path. Default to a unique file in the system temp directory to avoid 
        # conflicts between concurrent runs and ensure cleanup after execution.
        if os.environ.get("PANDOC_INCLUDE_TEMP_FILE") is None:
            os.environ["PANDOC_INCLUDE_TEMP_FILE"] = os.path.join(tempfile.gettempdir(), '.temp.pandoc-include.' + self.RunId)
        self.TempFile       = os.environ.get("PANDOC_INCLUDE_TEMP_FILE")
        
        self._initialized   = True
        
    def GetEnv():
        return Env._instance or Env()

def parseConfig(text):
    regex = re.compile(
        r'''
            (?P<key>\w+)=      # Key consists of only alphanumerics
            (?P<quote>["'`]?)  # Optional quote character.
            (?P<value>.*?)     # Value is a non greedy match
            (?P=quote)         # Closing quote equals the first.
            ($|,)              # Entry ends with comma or end of string
        ''',
        re.VERBOSE
    )

    config = {}
    for match in regex.finditer(text):
        key = match.group('key')
        if key in CONFIG_KEYS:
            # Include the original quotes
            raw_value = f"{match.group('quote')}{match.group('value')}{match.group('quote')}"
            try:
                value = ast.literal_eval(raw_value)
            except:
                raise ValueError(f"Invalid config: {key}={raw_value}")
            if not isinstance(value, CONFIG_KEYS[key]):
                raise ValueError(f"Invalid value type: {key}={raw_value}")
            config[key] = value

        else:
            pf.debug("[Warn] Invalid config key: " + key)

    return config


defaultOptions = {
    "include-entry": {
        "path": ".",
        "entered": False
    },
    "current-path": ".",
    "include-resources": ".",
    "process-path": None,
    "include-order": "natural",
    "rewrite-path": True,
    "pandoc-options": ["--filter=pandoc-include"]
}

def parseOptions(doc):
    if os.path.isfile(Env.GetEnv().TempFile):
        with open(Env.GetEnv().TempFile, 'r') as f:
            # merge with default options to prevent missing keys
            options = { **defaultOptions, **json.load(f) }
    else:
        # entry file (default values)
        options = defaultOptions.copy()

    # include entry
    include_entry = doc.get_metadata('include-entry')
    if include_entry is not None:
        if not options["include-entry"]["entered"]:
            options['include-entry'] = dict(path=include_entry, entered=False)
        else:
            pf.debug("[WARN] include-entry specified multiple times")

    # pandoc options
    pandoc_options = doc.get_metadata('pandoc-options')
    if pandoc_options is not None:
        # Replace em-dash to double dashes in smart typography
        for i in range(len(pandoc_options)):
            pandoc_options[i] = pandoc_options[i].replace('\u2013', '--')
        options['pandoc-options'] = pandoc_options

    # order of included files (natural, alphabetical, shell_default)
    include_order = doc.get_metadata("include-order")
    if include_order is not None:
        options["include-order"] = include_order

    # rewrite path
    rewrite_path = doc.get_metadata("rewrite-path")
    if rewrite_path is not None:
        options["rewrite-path"] = rewrite_path

    # resource path
    resource_path = doc.get_metadata("include-resources")
    if resource_path is not None:
        options["include-resources"] = resource_path

    # process path
    process_path = os.getcwd()
    if options["process-path"] is None:
        options["process-path"] = process_path

    return options
