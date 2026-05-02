# sprigconfig/help.py

COMMAND_HELP = {
    "dump": {
        "summary": "Dump merged configuration for inspection/debugging",
        "examples": [
            "sprigconfig dump --config-dir=config --profile=dev",
            "sprigconfig dump --config-dir=config --profile=prod --secrets",
            "sprigconfig dump --config-dir=config --profile=test --output-format=json",
            "sprigconfig dump --config-dir=config --profile=dev --output out.yml",
        ],
    }
}
