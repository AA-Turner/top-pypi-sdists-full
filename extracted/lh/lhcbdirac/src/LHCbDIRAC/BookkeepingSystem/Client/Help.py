###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Help class."""


def helpConfig(treeLevels):
    """configure the help."""
    if treeLevels == -1:
        print("-------------------------------------")
        print("| Please use the following comand:   |")
        print("| client.list()                      |")
        print("--------------------------------------")
    elif treeLevels == 0:
        print("-----------------------------------------")
        print("| Please choose one configuration!       |")
        print("| For example:                           |")
        print("| client.list('/CFG_DC06 phys-v3-lumi5') |")
        print("------------------------------------------")

    elif treeLevels == 1:
        print("-------------------------------------------------------")
        print("| Please choose one event type!                       |")
        print("| For example:                                        |")
        print("| client.list('/CFG_DC06 phys-v3-lumi5/EVT_10000010') |")
        print("-------------------------------------------------------")

    elif treeLevels == 2:
        print("-----------------------------------------------------------------")
        print("| Please choose one production!                                 |")
        print("| For example:                                                  |")
        print("| client.list('/CFG_DC06 phys-v3-lumi5/EVT_10000010/PROD_1933') |")
        print("-----------------------------------------------------------------")

    elif treeLevels == 3:
        print("------------------------------------------------------------------------|")
        print("| Please choose one file type!                                          |")
        print("| For example:                                                          |")
        print("| client.list('/CFG_DC06 phys-v3-lumi5/EVT_10000010/PROD_1933/FTY_RDST Brunel v30r17')|")
        print("-------------------------------------------------------------------------|")


def helpProcessing(treeLevels):
    """help."""
    if treeLevels == -1:
        print("-------------------------------------")
        print("| Please use the following comand:   |")
        print("| client.list()                      |")
        print("--------------------------------------")
    elif treeLevels == 0:
        print("-----------------------------------------")
        print("| Please choose one Processing Pass!     |")
        print("| For example:                           |")
        print("| client.list('/PPA_Pass342')            |")
        print("------------------------------------------")

    elif treeLevels == 1:
        print("-------------------------------------------------------")
        print("| Please choose one production!                       |")
        print("| For example:                                        |")
        print("| client.list('/PPA_Pass342/PRO_1858')                |")
        print("-------------------------------------------------------")

    elif treeLevels == 2:
        print("-----------------------------------------------------------------")
        print("| Please choise one event type!                                 |")
        print("| For example:                                                  |")
        print("| client.list('/PPA_Pass342/PRO_1858/EVT_10000000')             |")
        print("-----------------------------------------------------------------")

    elif treeLevels == 3:
        print("-----------------------------------------------------------------")
        print("| Please choose one file type!                                  |")
        print("| For example:                                                  |")
        print("| client.list('/PPA_Pass342/PRO_1858/EVT_10000000/FTY_RDST')    |")
        print("-----------------------------------------------------------------")


def helpEventType(treeLevels):
    print("Not Implemented!")
