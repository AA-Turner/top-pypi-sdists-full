#!/usr/bin/env python3
# A script to generate a g3w suite config.properties file

import sys
import os
import g3w_config_scripts.g3w_config as cfg


def main():
    """
    Ask the user for the parameters to be used in the configuration file, proposing
    default values.

    Then generate a config.properties file in the current folder.
    """

    parameters = cfg.Parameters(doDevel=True)

    answ = input(f"Set the SUITE_REPO_TAG parameter: [{parameters.SUITE_REPO_TAG}] -> ")
    if answ:
        parameters.SUITE_REPO_TAG = answ
        parameters.SUITE_ADMIN_REPO_TAG = answ
    
    answ = input(f"Set the SUITE_DOCKER_IMAGE parameter: [{parameters.SUITE_DOCKER_IMAGE}] -> ")
    if answ:
        parameters.SUITE_DOCKER_IMAGE = answ

    answ = input(f"Set the MY_NEW_BRANCH parameter: [{parameters.MY_NEW_BRANCH}] -> ")
    if answ:
        parameters.MY_NEW_BRANCH = answ

    answ = input(f"Set the SUITE_SHARED_VOLUME parameter: [{parameters.SUITE_SHARED_VOLUME}] -> ")
    if answ:
        parameters.SUITE_SHARED_VOLUME = answ

    answ = input(f"Set the DEBUG parameter: [{parameters.DEBUG}] -> ")
    if answ:
        parameters.DEBUG = answ

    answ = input(f"Set the FRONTEND parameter: [{parameters.FRONTEND}] -> ")
    if answ:
        parameters.FRONTEND = answ

        if parameters.FRONTEND:
            answ = input(f"Set optional FRONTEND_REPO: [{parameters.FRONTEND_REPO}] -> ")
            if answ:
                parameters.FRONTEND_REPO = answ
    
    answ = input(f"Set the WEBGIS_PUBLIC_HOSTNAME parameter: [{parameters.WEBGIS_PUBLIC_HOSTNAME}] -> ")
    if answ:
        parameters.WEBGIS_PUBLIC_HOSTNAME = answ

    answ = input(f"Set the G3WSUITE_POSTGRES_PASS parameter: [{parameters.G3WSUITE_POSTGRES_PASS}] -> ")
    if answ:
        parameters.G3WSUITE_POSTGRES_PASS = answ

    addService = input("Do you want to add a pg_service definition? (y/n) ")
    if addService == "y":
        answ = input(f"Set the PG_SERVICE_CONF parameter: ")
        if answ:
            parameters.PG_SERVICE_CONF = answ

    addHttps = input("Do you want to enable HTTPS? (y/n) ")
    if addHttps == "y":
        parameters.DO_HTTPS = True

        addCert = input("Add your certificate file: ")
        if addCert and os.path.exists(addCert):
            parameters.HTTPS_CERT = addCert
        
        addKey = input("Add your key file: ")
        if addKey and os.path.exists(addKey):
            parameters.HTTPS_KEY = addKey

    

    print("#### The parameters are:")
    cfg.print_used_configuration(parameters)
        
    if input("#### Do you want to continue with these parameters? (y/n) ") != "y":
        print("#### Exiting.")
        sys.exit(0)

    with open("config.properties", "w") as f:
        f.write("# Configuration file for the g3w suite setup\n")
        f.write("\n")
        f.write(f"SUITE_REPO_TAG={parameters.SUITE_REPO_TAG}\n")
        f.write(f"SUITE_ADMIN_REPO_TAG={parameters.SUITE_ADMIN_REPO_TAG}\n")
        f.write(f"SUITE_DOCKER_IMAGE={parameters.SUITE_DOCKER_IMAGE}\n")
        f.write(f"MY_NEW_BRANCH={parameters.MY_NEW_BRANCH}\n")
        f.write(f"SUITE_SHARED_VOLUME={parameters.SUITE_SHARED_VOLUME}\n")
        f.write(f"DEBUG={parameters.DEBUG}\n")
        f.write(f"FRONTEND={parameters.FRONTEND}\n")
        f.write(f"WEBGIS_PUBLIC_HOSTNAME={parameters.WEBGIS_PUBLIC_HOSTNAME}\n")
        f.write(f"G3WSUITE_POSTGRES_PASS={parameters.G3WSUITE_POSTGRES_PASS}\n")
        if addService == "y":
            f.write(f"PG_SERVICE_CONF={parameters.PG_SERVICE_CONF}\n")

    print("#### The configuration file has been written to: config.properties")

if __name__ == "__main__":
    main()