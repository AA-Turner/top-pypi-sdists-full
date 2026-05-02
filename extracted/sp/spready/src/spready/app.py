#!/usr/bin/env python
import os
from redis import Redis
import logging
from rq import Worker
import jwt
from loguru import logger

from spready.config import getEnvURL
from spready.parser import SpreadyDecoratorParser


rqLogger = logging.getLogger("rq.worker")
rqLogger.propagate = False
rqLogger.disabled = True

appLogger = logging.getLogger("app")
appLogger.log(10, "Starting worker")
import json
import jwt
# from .config import EnvURLS
import requests

os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
os.environ["no_proxy"] = "*"
print(os.environ.get("OBJC_DISABLE_INITIALIZE_FORK_SAFETY"))

def register(envURL: str):
    res = requests.get(f"{envURL}/register")
    return res.json()

def run(credFilePath: str, modulePath: str):
    with open(credFilePath, "r") as f:
        creds = json.load(f)
        if "privateKey" in creds:
            _creds = jwt.decode(creds["privateKey"], creds["publicKey"], algorithms=["HS256"])
            __run(_creds["__H"], _creds["__P"], _creds["__D"], _creds["__PW"], creds['publicKey'], modulePath)


def __run(host, port, db, password, channel, modulePath="."):
    conn = Redis(
        host=host,
        port=port,
        db=db,
        password=password,
    )
    logger.info(f"""
                
                Starting Spread-Y Worker
                ~~~~~~~~~~~~~~~~~~~~~~~~
                
                Channel     : {channel}
                Module      : {modulePath}
                API         : {getEnvURL()}


                """)
    os.environ["SPREADY_MODULES"] = modulePath

    parser = SpreadyDecoratorParser(modulePath)
    spreadyModules = parser.spreadyRouts


    mStr = "\t~~~~~~~ APIs ~~~~~~~\n"
    for mod in spreadyModules:
        mStr += f"\n\t{mod} : {spreadyModules[mod]}\n"
    print(f"""{mStr}""")

    

    # Provide the worker with the list of queues (str) to listen to.
    w = Worker([channel], connection=conn, log_job_description=False)
    w.work()

# if __name__ == "__main__":
#     import sys
#     run(sys.argv[1]) 
    
# register(EnvURLS.DEV)