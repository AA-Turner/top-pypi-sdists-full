import argparse

from pyhocon import ConfigFactory, ConfigTree


def parse_args():
    parser = argparse.ArgumentParser(description="Spark Application")
    parser.add_argument(
        "-C",
        "--config",
        nargs="+",
        help=(
            "Property of the config that needs to be overridden. Set a number of key-value "
            "pairs(do not put spaces before or after the = sign). Ex: -C fabricName=dev "
            'dbConnection="db.prophecy.io" dbUserName="prophecy"'
        ),
    )
    parser.add_argument(
        "-d",
        "--defaultConfFile",
        help="Full path of default hocon config file. Ex: -d dbfs:/some_path/default.json",
        default=None
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Location of the hocon config file. Ex: -f /opt/prophecy/dev.json",
    )
    parser.add_argument(
        "-i",
        "--confInstance",
        help="Config instance name present in config directory. Ex.: -i default",
    )
    parser.add_argument(
        "-O",
        "--overrideJson",
        type=str,
        help="Overridden values in json format"
    )
    args = parser.parse_args()

    return args


def get_resource_file_content(resource_file_name, config_package):
    try:
        # python 3.7+
        import importlib.resources
        with importlib.resources.open_text(config_package, f"{resource_file_name}") as file:
            data = file.read()
    except:
        # python < 3.7
        import importlib.util
        config_instances_path = importlib.util.find_spec(config_package).submodule_search_locations[0]
        config_file_path = f"{config_instances_path}/{resource_file_name}"
        with open(config_file_path, 'r') as file:
            data = file.read()
    return data


# 1 arg parse_config() for backward compatibility.
def parse_config(args, pipeline_dot_conf=None, config_package=None):
    config_package = "prophecy_config_instances" if config_package is None else config_package
    if args.file is not None:
        if hasattr(args, "defaultConfFile"):
            default_config = ConfigFactory.parse_file(
                args.defaultConfFile) if args.defaultConfFile is not None else ConfigFactory.parse_string("{}")
            conf = ConfigFactory.parse_file(args.file).with_fallback(default_config)
        else:
            conf = ConfigFactory.parse_file(args.file)
    elif args.confInstance is not None:
        try:
            # python 3.7+
            import importlib.resources
            with importlib.resources.open_text(
                    config_package,
                    "{instance}.json".format(instance=args.confInstance),
            ) as file:
                data = file.read()
                conf = ConfigFactory.parse_string(data)
        except:
            # python < 3.7
            import importlib.util
            config_instances_path = importlib.util.find_spec(config_package).submodule_search_locations[0]
            config_file_path = f"{config_instances_path}/{args.confInstance}.json"
            with open(config_file_path, 'r') as file:
                data = file.read()
                conf = ConfigFactory.parse_string(data)
    else:
        conf = ConfigFactory.parse_string("{}")

    if args.overrideJson is not None:
        # Override fields
        conf = ConfigTree.merge_configs(conf, ConfigFactory.parse_string(args.overrideJson))
    # override the file config with explicit value passed
    if args.config is not None:
        for config in args.config:
            c = config.split("=", 1)
            conf.put(c[0], c[1])

    if pipeline_dot_conf is not None:
        # `resolve=False` is important here because variable substitution should happen after overriding
        try:
            # Check in resources/
            pipeline_default_conf = ConfigFactory.parse_string(get_resource_file_content(pipeline_dot_conf, config_package),
                                                               resolve=False)
        except:
            # Check as full file path
            pipeline_default_conf = ConfigFactory.parse_file(pipeline_dot_conf, resolve=False)
        # `resolve=True` so that variables get substituted at this step with overridden values
        # pipeline_dot_conf contains default values for a given pipeline. It should have the lowest priority,
        conf = conf.with_fallback(pipeline_default_conf, resolve=True)

    return conf
