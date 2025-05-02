# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import sys
import logging

# See readme for information on how to setup Anzo for tests
GRAPHMART = "http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7"  # noqa
ANZOGRAPH_DS = "http://cambridgesemantics.com/GqeDatasource/guid_3af6a337ad444400a1f01dbe2e16b82b"  # noqa

DOMAIN = "localhost"
PORT = "8443"
AUTH_TOKEN = "auth_token"
EMPTY_AUTH_TOKEN = ""
USERNAME = "sysadmin"
PASSWORD = "123"
PATH = ""

def log_while_running_tests():
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)

