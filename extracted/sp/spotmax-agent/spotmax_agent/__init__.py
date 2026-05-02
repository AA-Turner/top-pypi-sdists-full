import os
import argparse
from .agent import run_agent
from time import sleep


def main():
    results = parse_arguments()
    action = results.action
    args = vars(results)
    verbose = False
    debug = False

    if args['verbose']:
        verbose = True

    if args['debug']:
        debug = True

    elif action == "run":
        run_agent(debug, verbose)

    elif action == "configure":
        print("Spotmax agent configuration")

    elif action == "init":
        try_num = 1
        install_succeed = False
        while (not install_succeed) and (try_num <= 3):
            if try_num > 1:
                sleep(20)
                print("trying to Initializing agent again (retry %s/3)" % (format(try_num)))
            try_num += 1
            print("Initializing agent")
            install_succeed = install_and_init_agent()

        if not install_succeed:
            print("init failed")
            exit(1)
        else:
            print("Spotmax agent installed successfully")
    else:
        print("Unrecognized action. Please use one of the following : add-worker, add-collector, configure")


def install_and_init_agent():
    try:
        create_agent_local_folders()
    except:
        return False
    return True


def create_agent_local_folders():
    if not os.path.exists('/etc/spotmax'):
        os.makedirs('/etc/spotmax')
    if not os.path.exists('/etc/spotmax/agent'):
        os.makedirs('/etc/spotmax/agent')
    if not os.path.exists('/etc/spotmax/agent/config'):
        os.makedirs('/etc/spotmax/agent/config')
    if not os.path.exists('/var/log/spotmax'):
        os.makedirs('/var/log/spotmax')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Spotmax Agent')
    parser.add_argument('action',
                        action="store",
                        help='The action to be performed. Options : add-worker / add-collector / configure.')
    parser.add_argument('--verbose', help='Verbose mode', required=False, action='store_true')
    parser.add_argument('--debug', help='Mock credentials', required=False, action='store_true')
    results = parser.parse_args()
    return results
