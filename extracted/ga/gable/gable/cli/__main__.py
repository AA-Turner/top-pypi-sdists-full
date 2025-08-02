# This is a temporary file which will allow us to be backwards compatible with the CICD change (https://github.com/gabledata/cicd/pull/17). The CLI code can either be run as a module or as a CLI.

from gable.cli.cli_setup import cli

if __name__ == "__main__":
    cli()  # This will invoke the CLI with all the commands defined in cli_setup.py
