#!/usr/bin/env python3
# A script to setup a docker based development environment for the g3w suite

import sys
import os
import g3w_config_scripts.g3w_config as cfg

def main():
    parameters = cfg.Parameters(doDevel=False)

    # if a file was supplied as an argument, use that as the parameters properties file
    if len(sys.argv) > 1:
        print(f"#### Using parameters from file: {sys.argv[1]}")
        # read the file and set the parameters
        cfg.read_config_from_file(sys.argv[1], parameters)
    else:
        # check if there is a config.properties file in the current folder
        if os.path.exists("config.properties"):
            print(f"#### Using parameters from file: config.properties")
            cfg.read_config_from_file("config.properties", parameters)


    cfg.print_used_configuration(parameters)

    if input("#### Do you want to continue with these parameters? (y/n)") != "y":
        print("#### Exiting.")
        sys.exit(0)

    #######################################

    if not os.path.exists(parameters.SUITE_SHARED_VOLUME):
        os.makedirs(parameters.SUITE_SHARED_VOLUME)
        print("#### The shared volume has been created.\n")

    cfg.clone_suite_docker_repo(parameters)
    cfg.clone_suite_admin_repo(parameters)
    cfg.setup_env_file(parameters)
    cfg.setup_pg_service_file(parameters)

    cfg.toggle_frontend(parameters)

    cfg.setup_plugin(parameters)

    cfg.setup_https(parameters)

    cfg.createRunScripts(parameters)


    print("###################################################################################################")
    print("###################################################################################################")
    print("# The setup is complete. You can now start the docker environment with the following command:")
    print("#")
    print("#    cd g3w-suite-docker && docker compose -f docker-compose.yml up")
    print("#")
    print("# You can stop it with:")
    print("#")
    print("#    cd g3w-suite-docker && docker compose -f docker-compose.yml down")
    print("#")
    print("###################################################################################################")
    print("###################################################################################################")

if __name__ == "__main__":
    main()