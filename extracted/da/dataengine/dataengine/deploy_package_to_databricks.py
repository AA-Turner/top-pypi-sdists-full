"""
This is a generic script that will allow dataengine users to easily deploy
their python packages to DataBricks.
"""
import os
import sys
import argparse
import re
from .utilities import databricks_utils


def parse_args():
    """
    This method will parse the arguments provided to the script.
    Returns:
        parsed args
    """
    # Instantiate parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dbt", "--token", dest="databricks_token", help="DataBricks API token")
    parser.add_argument(
        "-dbh", "--host", dest="databricks_host", help="DataBricks Host / URL")
    parser.add_argument(
        "-dbsid", "--scriptid", dest="databricks_script_id",
        help="DataBricks global init script id")

    return vars(parser.parse_args())


def main():
    """
    Main method for deploying a wheel to DataBricks.
    """
    # Parse arguments passed via the command line
    args = parse_args()
    # Get the dynamic name of the whl file from the directory
    whl_files = os.listdir("dist")
    whl_filename = [file for file in whl_files if file.endswith(".whl")][0]
    # Pull the package name from the wheel filename
    package_name = re.match(r"(.+)-\d+\.(\w+)", whl_filename).group(1)
    # Setup the local filepath and the desired dbfs path
    local_wheel_path = os.path.join("dist", whl_filename)
    dbfs_path = os.path.join("dbfs:/mnt/", whl_filename)
    # Upload the wheel file to the databricks filesystem
    databricks_utils.put_file(
        args["databricks_host"], args["databricks_token"], local_wheel_path,
        dbfs_path)
    # Generate basic shell init script to pip install the wheel
    init_script_text = "#!/bin/bash\ndatabricks/python/bin/pip install {}".format(
        dbfs_path.replace(":", ""))
    # Update the databricks global init script
    success = databricks_utils.update_global_init_script(
        args["databricks_host"], args["databricks_token"], init_script_text,
        args["databricks_script_id"], package_name)
    # If unsuccessful exit with a 1 status code
    if success:
        print("Global init script successfully updated.")
    else:
        print("Global init script update failed")
        sys.exit(1)

    return


if __name__ == "__main__":
    main()
