import os
import textwrap
#######################################
# PARAMETERS
#######################################
class Parameters:

    def __init__(self, doDevel=None):
        if doDevel is not None:
            self.DO_DEVEL = doDevel
        else:
            raise Exception("You must specify if you are in development mode or not.")
        
        # The public hostname of the web
        self.WEBGIS_PUBLIC_HOSTNAME="v38.g3wsuite.it"
        # The docker project tag of the g3w-suite-docker to use
        self.SUITE_REPO_TAG="v3.8.0" 
        self.SUITE_ADMIN_REPO_TAG=self.SUITE_REPO_TAG 
        # The docker image to use
        self.SUITE_DOCKER_IMAGE="g3wsuite/g3w-suite:v3.8.x" 
        # The name of the new branch to create
        self.MY_NEW_BRANCH=f"{self.SUITE_REPO_TAG}_myniceproject" 
        
        self.G3WSUITE_POSTGRES_PASS='myPgPasswd'
        
        self.PG_SERVICE_CONF=None #"[service@111.111.11.111]|host=111.111.11.111|user=myuser|password=mypwd|dbname=mydb|port=5432"

        # The path to the shared volume
        self.SUITE_SHARED_VOLUME="/myniceproject/" 
        self.DEBUG=True
        self.FRONTEND=False
        self.FRONTEND_REPO="https://github.com/g3w-suite/g3w-admin-frontend.git"

        # FIXED FILES
        self.ENV_FILE = "g3w-suite-docker/.env"
        self.SETTINGS_FILE="g3w-suite-docker/config/g3w-suite/settings_docker.py"
        self.PG_SERVICE_FILE="g3w-suite-docker/secrets/pg_service.conf"
        self.NGINX_FOLDER="g3w-suite-docker/config/nginx/"

        # get absolute path to the g3w-admin code, automatically generated
        self.LOCAL_ADMIN_CODE_PATH = os.path.abspath("g3w-admin")


        self.COMPOSE_FILE = "g3w-suite-docker/docker-compose-dev.yml" if doDevel else "g3w-suite-docker/docker-compose.yml"
        self.ENTRYPOINT_FILE="g3w-suite-docker/scripts/docker-entrypoint-dev.sh" if doDevel else "g3w-suite-docker/scripts/docker-entrypoint.sh"

        self.DO_HTTPS = False
        self.HTTPS_CERT = None
        self.HTTPS_KEY = None

#######################################
def read_config_from_file(path: str, parameters: Parameters):
    with open(path, "r") as f:
        lines = f.readlines()
    paramsDict = {}
    for line in lines:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            # find first = and split the line
            key, value = line.split("=", maxsplit=1)
            #  check type of value
            if value.strip().lower() in ["true", "false"]:
                value = value.strip().lower() == "true"
            else:
                value = value.strip()
            paramsDict[key.strip()] = value
            print(f"##### Found parameter: {key.strip()} = {value}")

    # set the parameters. FIXED FILES vars are not handled
    parameters.SUITE_REPO_TAG = paramsDict.get("SUITE_REPO_TAG", parameters.SUITE_REPO_TAG)
    parameters.SUITE_ADMIN_REPO_TAG = paramsDict.get("SUITE_ADMIN_REPO_TAG", parameters.SUITE_REPO_TAG)
    parameters.SUITE_DOCKER_IMAGE = paramsDict.get("SUITE_DOCKER_IMAGE", parameters.SUITE_DOCKER_IMAGE)
    parameters.MY_NEW_BRANCH = paramsDict.get("MY_NEW_BRANCH", parameters.MY_NEW_BRANCH)
    parameters.SUITE_SHARED_VOLUME = paramsDict.get("SUITE_SHARED_VOLUME", parameters.SUITE_SHARED_VOLUME)
    parameters.DEBUG = paramsDict.get("DEBUG", parameters.DEBUG)
    parameters.FRONTEND = paramsDict.get("FRONTEND", parameters.FRONTEND)
    if parameters.FRONTEND:
        parameters.FRONTEND_REPO = paramsDict.get("FRONTEND_REPO", parameters.FRONTEND_REPO)
    parameters.WEBGIS_PUBLIC_HOSTNAME = paramsDict.get("WEBGIS_PUBLIC_HOSTNAME", parameters.WEBGIS_PUBLIC_HOSTNAME)
    parameters.G3WSUITE_POSTGRES_PASS = paramsDict.get("G3WSUITE_POSTGRES_PASS", parameters.G3WSUITE_POSTGRES_PASS)
    parameters.PG_SERVICE_CONF = paramsDict.get("PG_SERVICE_CONF", parameters.PG_SERVICE_CONF)
    if not parameters.DO_DEVEL:
        parameters.DO_HTTPS = paramsDict.get("DO_HTTPS", parameters.DO_HTTPS)
        parameters.HTTPS_CERT = paramsDict.get("HTTPS_CERT", parameters.HTTPS_CERT)
        parameters.HTTPS_KEY = paramsDict.get("HTTPS_KEY", parameters.HTTPS_KEY)

    if parameters.DO_DEVEL:
        parameters.DEBUG = True




def print_used_configuration(parameters: Parameters):
    print("###################################################################################################")
    print("###################################################################################################")
    if parameters.DO_DEVEL:
        print(f"# SETTING UP FOR DEVEL MODE")
    else:
        print(f"# SETTING UP FOR PRODUCTION MODE")
    print(f"# Setting up the g3w suite development environment with the following parameters:")

    useMyBranch = False
    if not os.path.exists("g3w-admin"):
        print(f"# SUITE_REPO_TAG: {parameters.SUITE_REPO_TAG}")
        useMyBranch = True
    else:
        print(f"# Using g3w-admin from existing folder.")
    if not os.path.exists("g3w-suite-docker"):
        if parameters.SUITE_ADMIN_REPO_TAG != parameters.SUITE_REPO_TAG:
            print(f"# SUITE_ADMIN_REPO_TAG: {parameters.SUITE_ADMIN_REPO_TAG}")
        useMyBranch = True
    else:
        print(f"# Using g3w-suite-docker from existing folder.")
    if useMyBranch:
        print(f"# MY_NEW_BRANCH: {parameters.MY_NEW_BRANCH}")

    print(f"# SUITE_DOCKER_IMAGE: {parameters.SUITE_DOCKER_IMAGE}")
    print(f"#")
    print(f"# -> SUITE_SHARED_VOLUME: {parameters.SUITE_SHARED_VOLUME}")
    print(f"# -> MOUNTED CODE PATH: {parameters.LOCAL_ADMIN_CODE_PATH}")
    print(f"#")
    print(f"# DEBUG: {parameters.DEBUG}")
    print(f"# ")
    print(f"# FRONTEND: {parameters.FRONTEND}")
    if parameters.FRONTEND:
        print(f"# FRONTEND_REPO: {parameters.FRONTEND_REPO}")
    print(f"# ")

    print(f"# COMPOSE_FILE: {parameters.COMPOSE_FILE}")
    print(f"# ENV_FILE: {parameters.ENV_FILE}")
    print(f"# SETTINGS_FILE: {parameters.SETTINGS_FILE}")
    print(f"# ENTRYPOINT_FILE: {parameters.ENTRYPOINT_FILE}")
    print(f"# WEBGIS_PUBLIC_HOSTNAME: {parameters.WEBGIS_PUBLIC_HOSTNAME}")
    print(f"# G3WSUITE_POSTGRES_PASS: {parameters.G3WSUITE_POSTGRES_PASS}")
    print(f"#")
    print(f"# PG_SERVICE_CONF: {parameters.PG_SERVICE_CONF}")
    print(f"#")
    if parameters.DO_HTTPS and not parameters.DO_DEVEL:
        print(f"# HTTPS will be enabled")
        if parameters.HTTPS_CERT and parameters.HTTPS_KEY:
            print(f"# -> HTTPS_CERT: {parameters.HTTPS_CERT}")
            print(f"# -> HTTPS_KEY: {parameters.HTTPS_KEY}")
    print("###################################################################################################")
    print("###################################################################################################")


def run_command(command):
    import subprocess
    print(f"#### Running command: {command}")
    process = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if process.returncode != 0:
        print(f"Error: {process.stderr.decode()}")
        raise Exception(f"Error running command: {command}")

def clone_suite_docker_repo(parameters: Parameters):
    # clone the g3w-suite-docker repository
    if not os.path.exists("g3w-suite-docker"):
        command = "git clone https://github.com/g3w-suite/g3w-suite-docker"
        run_command(command)
        # add the original g3w-suite-docker as a remote
        run_command("cd g3w-suite-docker && git fetch")
        # checkout version to work on
        run_command("cd g3w-suite-docker && git checkout " + parameters.SUITE_REPO_TAG)
        # create a local branch from that
        run_command("cd g3w-suite-docker && git checkout -b " + parameters.MY_NEW_BRANCH)
        print("#### The new branch has been created locally, you can push it to the remote repository at any time.")


        print("#### The g3w-suite-docker repository has been cloned and the new branch has been created.\n")
    else:
        print("#### The g3w-suite-docker repository is already cloned.\n")
        
    if parameters.DO_DEVEL:
        # in the g3w-suite-docker/docker-compose-dev.yml substitute the right image to address (in this case the v3.7.x train):
        # -    image: g3wsuite/g3w-suite:dev
        # +    image: g3wsuite/g3w-suite:v3.7.x
        with open(parameters.COMPOSE_FILE, "r") as f:
            lines = f.readlines()
        with open(parameters.COMPOSE_FILE, "w") as f:
            for line in lines:
                f.write(line.replace("image: g3wsuite/g3w-suite:dev", f"image: {parameters.SUITE_DOCKER_IMAGE}"))

        # add missing line: ./secrets/pg_service.conf:${PGSERVICEFILE} to the volumes part of the db service
        with open(parameters.COMPOSE_FILE, "r") as f:
            lines = f.readlines()
        with open(parameters.COMPOSE_FILE, "w") as f:
            for line in lines:
                if "QGIS3.ini" in line:
                    f.write("      - ./secrets/pg_service.conf:${PGSERVICEFILE}\n")
                f.write(line) 
    else:
        # in the g3w-suite-docker/docker-compose.yml add before the secrets volumes line:
        # ${G3WSUITE_LOCAL_CODE_PATH}:/code to mount the source code used
        with open(parameters.COMPOSE_FILE, "r") as f:
            lines = f.readlines()
        with open(parameters.COMPOSE_FILE, "w") as f:
            for line in lines:
                f.write(line) 
                if "./config/qgis/QGIS3.ini:" in line:
                    # mount source code
                    f.write(f"      - {parameters.LOCAL_ADMIN_CODE_PATH}:/code\n")
                    # also add the mounting of the entrypoint
                    f.write("      - ./scripts/docker-entrypoint.sh:/usr/bin/docker-entrypoint.sh\n\n")
                    # add entrypoint definition
                    f.write('    entrypoint: ["/bin/sh", "/usr/bin/docker-entrypoint.sh"]\n')

def clone_suite_admin_repo(parameters: Parameters):
    if not os.path.exists("g3w-admin"):
        run_command("git clone https://github.com/g3w-suite/g3w-admin")
        # add the original g3w-admin as a remote
        run_command("cd g3w-admin && git fetch")
        # checkout version to work on
        run_command("cd g3w-admin && git checkout " + parameters.SUITE_ADMIN_REPO_TAG)
        # create a local branch from that
        run_command("cd g3w-admin && git checkout -b " + parameters.MY_NEW_BRANCH)
        print("#### The new g3w-admin branch has been created locally, you can push it to the remote repository at any time.")

        print("#### The g3w-admin repository has been cloned and the new branch has been created.\n")
    else:
        print("#### The g3w-admin repository is already cloned.\n")

def setup_env_file(parameters: Parameters):
    # if g3w-suite-docker/.env does not exist, create it by copying the .env.example, and substituting the vars:
    # * WEBGIS_DOCKER_SHARED_VOLUME
    # * G3WSUITE_DEBUG
    # * G3WSUITE_LOCAL_CODE_PATH
    if not os.path.exists(parameters.ENV_FILE):
        with open("g3w-suite-docker/.env.example", "r") as f:
            lines = f.readlines()
        with open(parameters.ENV_FILE, "w") as f:
            hasSharedVolume = False
            hasDebug = False
            hasLocalCodePath = False
            hasFrontend = False
            hasHostname = False
            hasPostgresPass = False
            
            for line in lines:
                if line.startswith("WEBGIS_DOCKER_SHARED_VOLUME"):
                    f.write(f"WEBGIS_DOCKER_SHARED_VOLUME={parameters.SUITE_SHARED_VOLUME}\n")
                    hasSharedVolume = True
                elif line.startswith("G3WSUITE_DEBUG"):
                    f.write(f"G3WSUITE_DEBUG={parameters.DEBUG}\n")
                    hasDebug = True
                elif line.startswith("G3WSUITE_LOCAL_CODE_PATH"):
                    f.write(f"G3WSUITE_LOCAL_CODE_PATH={parameters.LOCAL_ADMIN_CODE_PATH}\n")
                    hasLocalCodePath = True
                elif line.startswith("FRONTEND"):
                    f.write(f"# FRONTEND={parameters.FRONTEND} -> this will be set directly in the local_settings.py\n")
                    hasFrontend = True
                elif line.startswith("WEBGIS_PUBLIC_HOSTNAME"):
                    f.write(f"WEBGIS_PUBLIC_HOSTNAME={parameters.WEBGIS_PUBLIC_HOSTNAME}\n")
                    hasHostname = True
                elif line.startswith("G3WSUITE_POSTGRES_PASS"):
                    f.write(f"G3WSUITE_POSTGRES_PASS={parameters.G3WSUITE_POSTGRES_PASS}\n")
                    hasPostgresPass = True
                else:
                    f.write(line)
            
            if not hasSharedVolume:
                f.write(f"WEBGIS_DOCKER_SHARED_VOLUME={parameters.SUITE_SHARED_VOLUME}\n")
            if not hasDebug:
                f.write(f"G3WSUITE_DEBUG={parameters.DEBUG}\n")
            if not hasLocalCodePath:
                f.write(f"G3WSUITE_LOCAL_CODE_PATH={parameters.LOCAL_ADMIN_CODE_PATH}\n")
            if not hasFrontend:
                f.write(f"# FRONTEND={parameters.FRONTEND} -> this will be set directly in the local_settings.py\n")
            if not hasHostname:
                f.write(f"WEBGIS_PUBLIC_HOSTNAME={parameters.WEBGIS_PUBLIC_HOSTNAME}\n")
            if not hasPostgresPass:
                f.write(f"G3WSUITE_POSTGRES_PASS={parameters.G3WSUITE_POSTGRES_PASS}\n")

        print("#### The .env file has been created.\n")
    else:
        print("#### The .env file is already present.\n")

def setup_pg_service_file(parameters: Parameters):
    # if the PG_SERVICE_CONF is not None, check inside the pg_service file, if the file contains the service already
    # if not, add the service to the file

    if parameters.PG_SERVICE_CONF:
        # get the service name from the PG_SERVICE_CONF
        pgServiceLines=parameters.PG_SERVICE_CONF.split("|")
        serviceName = pgServiceLines[0]
        with open(parameters.PG_SERVICE_FILE, "r") as f:
            lines = f.readlines()
        hasService = False
        serviceHasAnyLine = len(lines) > 0
        for line in lines:
            if serviceName in line:
                hasService = True
                break
        if not hasService:
            # add the service to the end of the file
            with open(parameters.PG_SERVICE_FILE, "a") as f:
                if serviceHasAnyLine:
                    f.write("\n")

                for line in pgServiceLines:
                    f.write(line + "\n")
                print("#### The pg_service.conf file has been updated.\n")
        else:
            print("#### The pg_service.conf file is already updated.\n")
    else:
        print("#### No pg_service.conf setup.\n")

def createRunScripts(parameters: Parameters):
    # check if there is a docker-compose command in the system, else
    # we need to use docker compose
    import shutil
    docker_compose_cmd = "docker compose"
    if shutil.which("docker-compose") is not None:
        print("#### Using docker-compose command.")
        # we will use docker-compose
        docker_compose_cmd = "docker-compose"

    if parameters.DO_DEVEL:
        # create devel run scripts
        #  start_dev.sh
        runsh = textwrap.dedent("""\
            #!/bin/bash
                                
            echo "Starting the g3w suite in development mode."
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose-dev.yml up -d
            cd ..
            echo "Done. You can now access the suite at http://localhost:8000"
        """)
        runsh = runsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("start_dev.sh", "w") as f:
            f.write(runsh)
        print("#### The start_dev.sh script has been created.\n")
        run_command("chmod +x start_dev.sh")

        # stop_dev.sh
        stopsh = textwrap.dedent("""\
            #!/bin/bash
                                 
            echo "Stopping the g3w suite in development mode."
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose-dev.yml down
            cd ..
            echo "Done."
        """)
        stopsh = stopsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("stop_dev.sh", "w") as f:
            f.write(stopsh)
        print("#### The stop_dev.sh script has been created.\n")
        run_command("chmod +x stop_dev.sh")

        # logs_dev.sh
        logsh = textwrap.dedent("""\
            #!/bin/bash

            echo "Starting the g3w suite dev logs."
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose-dev.yml logs -f $1
            cd ..
        """)
        logsh = logsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("logs_dev.sh", "w") as f:
            f.write(logsh)
        print("#### The logs_dev.sh script has been created.\n")
        run_command("chmod +x logs_dev.sh")

        # restart_dev.sh - to restart a service passed by name
        restartsh = textwrap.dedent("""\
            #!/bin/bash

            if [ -z "$1" ]
            then
              echo "Please provide the service name to restart."
              echo "Usage: ./restart_dev.sh <service_name>"
              exit 1
            fi

            echo "Restarting the g3w suite dev service: $1"
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose-dev.yml restart $1
            cd ..
            echo "Done."
        """)
        restartsh = restartsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("restart_dev.sh", "w") as f:
            f.write(restartsh)
        print("#### The restart_dev.sh script has been created.\n")
        run_command("chmod +x restart_dev.sh")

    else:
        # create production run scripts
        #  start.sh
        runsh = textwrap.dedent("""\
            #!/bin/bash
                                
            echo "Starting the g3w suite in production mode."
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose.yml up -d
            cd ..
            echo "Done."
        """)
        runsh = runsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("start.sh", "w") as f:
            f.write(runsh)
        print("#### The start.sh script has been created.\n")
        run_command("chmod +x start.sh")

        # stop.sh
        stopsh = textwrap.dedent("""\
            #!/bin/bash
                                 
            echo "Stopping the g3w suite in production mode."
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose.yml down
            cd ..
            echo "Done."
        """)
        stopsh = stopsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("stop.sh", "w") as f:
            f.write(stopsh)
        print("#### The stop.sh script has been created.\n")
        run_command("chmod +x stop.sh")

        # logs.sh
        logsh = textwrap.dedent("""\
            #!/bin/bash
                                
            echo "Starting the g3w suite logs."
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose.yml logs -f $1
            cd ..
        """)
        logsh = logsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("logs.sh", "w") as f:
            f.write(logsh)
        print("#### The logs.sh script has been created.\n")
        run_command("chmod +x logs.sh")

        # restart.sh - to restart a service passed by name
        restartsh = textwrap.dedent("""\
            #!/bin/bash

            if [ -z "$1" ]
            then
              echo "Please provide the service name to restart."
              echo "Usage: ./restart.sh <service_name>"
              exit 1
            fi

            echo "Restarting the g3w suite service: $1"
            cd g3w-suite-docker/
            COMPOSE_COMMAND -f docker-compose.yml restart $1
            cd ..
            echo "Done."
        """)
        restartsh = restartsh.replace("COMPOSE_COMMAND", docker_compose_cmd)
        with open("restart.sh", "w") as f:
            f.write(restartsh)
        print("#### The restart.sh script has been created.\n")
        run_command("chmod +x restart.sh")


def setup_redis_service(parameters: Parameters):
    if not parameters.DO_DEVEL:
        print("#### WARNING: Redis service setup is usually to be setup only in development mode.")
    # in the compose file, make sure that the redis part exists and if not add before the volumes part:
    #   redis:
    #     image: redis:latest
    #     expose:
    #     - 6379
    #     networks:
    #       internal:
    #     restart: always
    with open(parameters.COMPOSE_FILE, "r") as f:
        lines = f.readlines()
    # check if the redis part exists
    redisExists = False
    for line in lines:
        if "redis:" in line:
            redisExists = True

    if not redisExists:
        print("#### Adding the redis service to the compose file before the volumes part.")
        with open(parameters.COMPOSE_FILE, "w") as f:
            for line in lines:
                if line.startswith("volumes:"):
                    f.write("  redis:\n")
                    f.write("    image: redis:latest\n")
                    f.write("    expose:\n")
                    f.write("    - 6379\n")
                    f.write("    networks:\n")
                    f.write("      internal:\n")
                    f.write("    restart: always\n\n")
                    print("#### The redis service has been added to the compose file.\n")
                f.write(line)
    else:
        print("#### The redis service is already present in the compose file.\n")


def toggle_frontend(parameters: Parameters):

    enableFrontend = parameters.FRONTEND
    if enableFrontend:
        print("#### Enabling the frontend app.")
    
    # in the settings file, make sure that in the G3WADMIN_LOCAL_MORE_APPS list, the 'frontend' app is commented (disabled)
    with open(parameters.SETTINGS_FILE, "r") as f:
        lines = f.readlines()
    with open(parameters.SETTINGS_FILE, "w") as f:
        doCheck = False
        hasFrontendExtraLines = False
        for line in lines:
            if "G3WADMIN_LOCAL_MORE_APPS" in line:
                doCheck = True
            if doCheck and "]" in line:
                doCheck = False

            if doCheck and "'frontend'" in line:
                if enableFrontend and line.strip().startswith("#"):
                    line = line.replace("#", "")
                    print("#### The 'frontend' app has been enabled in the settings file.\n")
                elif not enableFrontend and not line.strip().startswith("#"):
                    line = "# " + line
                    print("#### The 'frontend' app has been disabled in the settings file.\n")
                elif enableFrontend and not line.strip().startswith("#"):
                    print(f"#### The frontend app is already enabled.\n")
                elif not enableFrontend and line.strip().startswith("#"):
                    print(f"#### The frontend app is already disabled.\n")
                else:
                    print(f"#### enableFrontend={enableFrontend} with line={line}\n")
            
            # also check if FRONTEND = lines ar present
            if "FRONTEND = " in line or "FRONTEND_APP = " in line:
                hasFrontendExtraLines = True
                if not enableFrontend:
                    continue

            f.write(line)

        if enableFrontend and not hasFrontendExtraLines:
            f.write("\n\nFRONTEND = True")
            f.write("\nFRONTEND_APP = 'frontend'\n")
            print("#### The FRONTEND = True and FRONTEND_APP = 'frontend' lines have been added to the settings file.\n")

    
    # clone the g3w-frontend repository if it is not already present
    if enableFrontend:
        if not os.path.exists("g3w-admin/g3w-admin/frontend"):
            run_command(f"cd g3w-admin/g3w-admin && git clone {parameters.FRONTEND_REPO} frontend")

    # disable entrypoint lines that deal with frontend
        # temporary fix for the docker-entrypoint.sh
    newLines = []
    with open(parameters.ENTRYPOINT_FILE, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "if [[  -f /tmp/.X99-lock ]]; then" in line:
                newLines.append("if [  -f /tmp/.X99-lock ]; then\n")
            elif "if [[ \"${FRONTEND}\" =~ [Tt][Rr][Uu][Ee] ]] ; then" in line:
                newLines.append("if false; then # -> this part has been handled in the local_settings.py already, disabling here\n")
            else:
                newLines.append(line)

    with open(parameters.ENTRYPOINT_FILE, "w") as f:
        for line in newLines:
            f.write(line)

        


def setup_plugin(parameters: Parameters):
    """
    Add to the entrypoint the plugins
    """

    try:
        with open(parameters.ENTRYPOINT_FILE, "r") as f:
            lines = f.readlines()
        hasPipInstall = False
        for line in lines:
            if "PLUGINS_DIR=" in line:
                hasPipInstall = True
                break
        if not hasPipInstall:
            # collect lines and find the line to append after
            newLines = []
            for line in lines:
                newLines.append(line)
                if "cd /code/g3w-admin" in line:
                    newLines.append("\n")
                    newLines.append("# Installing the plugin app\n")
                    newLines.append("PLUGINS_DIR=\"/code/plugins\"\n")
                    newLines.append("for plugin_dir in \"$PLUGINS_DIR\"/*/; do\n")
                    newLines.append("    plugin_name=\"$(basename \"$plugin_dir\")\"\n")
                    newLines.append("    if ! pip list | grep -q \"^$plugin_name\"; then\n")
                    newLines.append("        figlet -t \"$plugin_name\"\n")
                    newLines.append("        pip3 install -v -e \"$plugin_dir\" --break-system-packages\n")
                    newLines.append("    fi\n")
                    newLines.append("done\n\n")
            with open(parameters.ENTRYPOINT_FILE, "w") as f:
                for line in newLines:
                    f.write(line)
            print(f"#### The plugin installation lines have been added to the entrypoint file.\n")
            print("#### NOTE: **********************************************************************\n")
            print(f"#### Please make sure to add your plugins to the settings installed apps!!!.\n")
            print("#### ******************************************************************************\n")
        else:
            print(f"#### The plugin installation lines are already present in the entrypoint file.\n")
        
    except Exception as e:
        print(f"#### Error: {e}")
        


def setup_https(parameters: Parameters):
    if parameters.DO_HTTPS:
        # tweak the nginx.conf file
        newLines = []
        with open(parameters.NGINX_FOLDER + "nginx.conf", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "default dev.g3wsuite.it" in line:
                    line = line.replace("dev.g3wsuite.it", f"{parameters.WEBGIS_PUBLIC_HOSTNAME}")
                elif "/etc/nginx/conf.d/django" in line and not "/etc/nginx/conf.d/django_ssl" in line:
                    line = "# " + line
                elif "/etc/nginx/conf.d/django_ssl" in line:
                    line = line.replace("#", "")

                newLines.append(line)

        with open(parameters.NGINX_FOLDER + "nginx.conf", "w") as f:
            for line in newLines:
                f.write(line)
        print("#### The nginx.conf file has been updated.\n")

        # if the HTTPS_CERT and HTTPS_KEY are set, copy the files to an ssl folder in the shared volume
        if parameters.HTTPS_CERT and os.path.exists(parameters.HTTPS_KEY):
            certFileName = os.path.basename(parameters.HTTPS_CERT)
            keyFileName = os.path.basename(parameters.HTTPS_KEY)
            # make folder ssl in the shared volume
            sslFolder = os.path.join(parameters.SUITE_SHARED_VOLUME, "ssl")
            if not os.path.exists(sslFolder):
                os.makedirs(sslFolder)
                print("#### The ssl folder has been created.\n")
            # copy the cert and key files
            run_command(f"cp {parameters.HTTPS_CERT} {sslFolder}/{certFileName}")
            run_command(f"cp {parameters.HTTPS_KEY} {sslFolder}/{keyFileName}")
            print("#### The certificate and key files have been copied to the ssl folder.\n")
            
            # now create the myssl file in the ssl folder
            with open(parameters.NGINX_FOLDER + "/myssl", "w") as f:
                f.write(f"ssl_certificate /shared-volume/ssl/{certFileName};\n")
                f.write(f"ssl_certificate_key /shared-volume/ssl/{keyFileName};\n")
            print("#### The myssl file has been created.\n")

            # now we need to set this instead of the "include /etc/nginx/conf.d/letsencrypt;" in the django_ssl file
            newLines = []
            with open(parameters.NGINX_FOLDER + "django_ssl", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if "/etc/nginx/conf.d/letsencrypt;" in line:
                        line = "   include /etc/nginx/conf.d/myssl;"
                    newLines.append(line)

            with open(parameters.NGINX_FOLDER + "django_ssl", "w") as f:
                for line in newLines:
                    f.write(line)

            print("#### The django_ssl file has been updated.\n")
            


            


def setup_debug_start(parameters: Parameters):
    # add "tail -f /dev/null" to the entrypoint file after the last line, if it is not there yet
    with open(parameters.ENTRYPOINT_FILE, "r") as f:
        lines = f.readlines()
    hasTail = False
    for line in lines:
        if "tail -f /dev/null" in line:
            hasTail = True
            break
    if not hasTail:
        with open(parameters.ENTRYPOINT_FILE, "a") as f:
            f.write("\ntail -f /dev/null\n")
            print("#### The tail command has been added to the entrypoint file.\n")
    else:
        print("#### The tail command is already present in the entrypoint file.\n")

def create_vscode_launch_json():
    # create the .vscode folder and the launch.json file with the debug configurations (if they do not exist)
    launchjson = """{
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Suite dev docker",
                "type": "debugpy",
                "request": "launch",
                "args": [
                    "runserver",
                    "0.0.0.0:8000"
                ],
                "django": true,
                "autoStartBrowser": false,
                "program": "${workspaceFolder}/g3w-admin/manage.py"
            },{
                "name": "Suite dev - make mirgation",
                "type": "debugpy",
                "request": "launch",
                "args": [
                    "makemigrations"
                ],
                "django": true,
                "autoStartBrowser": false,
                "program": "${workspaceFolder}/g3w-admin/manage.py"
            },{
                "name": "Suite dev - migrate",
                "type": "debugpy",
                "request": "launch",
                "args": [-> this will be set directly in the local_settings.py
                    "migrate"
                ],
                "django": true,
                "autoStartBrowser": false,
                "program": "${workspaceFolder}/g3w-admin/manage.py"
            },{
                "name": "Suite dev - create superuser",
                "type": "debugpy",
                "request": "launch",
                "args": [
                    "createsuperuser"
                ],
                "django": true,
                "autoStartBrowser": false,
                "program": "${workspaceFolder}/g3w-admin/manage.py"
            }
        ]
    }"""
    settingsJson="""{
        "python.analysis.extraPaths": [
            "${workspaceFolder}/g3w-admin",
            "${workspaceFolder}/plugins"
        ]
    }"""
    if not os.path.exists("g3w-admin/.vscode"):
        os.makedirs("g3w-admin/.vscode")
        print("#### The .vscode folder has been created.\n")
    if not os.path.exists("g3w-admin/.vscode/launch.json"):
        with open("g3w-admin/.vscode/launch.json", "w") as f:
            f.write(launchjson)
        print("#### The launch.json file has been created.\n")
    if not os.path.exists("g3w-admin/.vscode/settings.json"):
        with open("g3w-admin/.vscode/settings.json", "w") as f:
            f.write(settingsJson)
        print("#### The settings.json file has been created.\n")