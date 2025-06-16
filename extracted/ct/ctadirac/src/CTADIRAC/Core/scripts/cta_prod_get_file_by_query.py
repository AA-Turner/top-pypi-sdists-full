#!/usr/bin/env python
"""
Get files using file metadata query

Examples::

  $ cta_prod_get_file_by_query MCCampaign=PROD5b particle=gamma-diffuse thetaP=20.0 phiP=180.0 site=LaPalma
"""
from DIRAC.Core.Base.Script import Script


@Script()
def main():
    Script.registerSwitch("", "Path=", "    Path to search for")
    Script.registerSwitch(
        "", "SE=", "    (comma-separated list of) SEs/SE-groups to be searched"
    )
    # Registering arguments will automatically add their description to the help menu
    Script.registerArgument(
        [
            "metaspec: metadata index specification (of the form: "
            '"meta=value" or "meta<value", "meta!=value", etc.)'
        ],
        mandatory=False,
    )
    Script.parseCommandLine(ignoreErrors=True)
    args = Script.getPositionalArgs()

    import DIRAC
    from DIRAC import gLogger
    from DIRAC.DataManagementSystem.Client.DataManager import DataManager
    from DIRAC.DataManagementSystem.Client.MetaQuery import (
        FILE_STANDARD_METAKEYS,
        MetaQuery,
    )
    from DIRAC.DataManagementSystem.Utilities.DMSHelpers import resolveSEGroup
    from DIRAC.Resources.Catalog.FileCatalog import FileCatalog

    path = "/"
    seList = None
    for opt, val in Script.getUnprocessedSwitches():
        if opt == "Path":
            path = val
        elif opt == "SE":
            seList = resolveSEGroup(val.split(","))

    if seList:
        args.append(f"SE={','.join(seList)}")
    fc = FileCatalog()
    result = fc.getMetadataFields()
    if not result["OK"]:
        gLogger.error("Can not access File Catalog:", result["Message"])
        DIRAC.exit(-1)
    typeDict = result["Value"]["FileMetaFields"]
    typeDict.update(result["Value"]["DirectoryMetaFields"])
    # Special meta tags
    typeDict.update(FILE_STANDARD_METAKEYS)

    if len(args) < 1:
        print(f"Error: No argument provided\n{Script.scriptName}:")
        gLogger.notice(f"MetaDataDictionary: \n{str(typeDict)}")
        Script.showHelp(exitCode=1)

    mq = MetaQuery(typeDict=typeDict)
    result = mq.setMetaQuery(args)
    if not result["OK"]:
        gLogger.error("Illegal metaQuery:", result["Message"])
        DIRAC.exit(-1)
    metaDict = result["Value"]
    path = metaDict.pop("Path", path)

    result = fc.findFilesByMetadata(metaDict, path)
    if not result["OK"]:
        gLogger.error("Can not access File Catalog:", result["Message"])
        DIRAC.exit(-1)
    lfnList = sorted(result["Value"])

    gLogger.notice("Found lfns:")
    gLogger.notice("\n".join(lfn for lfn in lfnList))

    for lfn in lfnList:
        voName = lfn.split("/")[1]
        if voName not in ["ctao", "vo.cta.in2p3.fr"]:
            message = f"Wrong lfn: path must start with vo name (ctao or vo.cta.in2p3.fr):\n{lfn}"
            gLogger.error(message)
            return
        gLogger.notice("Start downloading file", lfn)
        dm = DataManager(vo=voName)
        res = dm.getFile(lfn)
        if not res["OK"]:
            gLogger.error("Error downloading file", lfn)
            return res["Message"]
        gLogger.notice("Successfully downloaded file", lfn)


if __name__ == "__main__":
    main()
