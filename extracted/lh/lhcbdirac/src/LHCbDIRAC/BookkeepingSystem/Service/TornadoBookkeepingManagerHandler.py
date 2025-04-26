###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
""" TornadoBookkeepingManager is the implementation of the BookkeepingManager service in HTTPS

    .. literalinclude:: ../ConfigTemplate.cfg
      :start-after: ##BEGIN TornadoBookkeepingManager:
      :end-before: ##END
      :dedent: 2
      :caption: TornadoBookkeepingManager options
"""
from DIRAC import S_OK
from DIRAC.Core.Tornado.Server.TornadoService import TornadoService
from LHCbDIRAC.BookkeepingSystem.Client import JEncoder
from LHCbDIRAC.BookkeepingSystem.Service.BookkeepingManagerHandler import BookkeepingManagerHandlerMixin
from LHCbDIRAC.BookkeepingSystem.Service.BookkeepingManagerHandler import default


class TornadoBookkeepingManagerHandler(BookkeepingManagerHandlerMixin, TornadoService):
    def export_streamToClient(self, parameters):
        """This method is used to transfer data using a file.

        Currently two client methods are using this function: getFiles, getFilesWithMetadata
        """

        in_dict = JEncoder.loads(parameters)
        self.log.verbose("Received the following dictionary:", str(in_dict))
        methodName = in_dict["MethodName"]
        if methodName == "getFiles":
            retVal = self._getFiles(in_dict)
        elif methodName == "getFilesWithMetadata":
            retVal = self._getFilesWithMetadata(in_dict)
        else:
            raise NotImplementedError(methodName)

        if not retVal["OK"]:
            self.log.error("Failed to send files:", str(in_dict))
            return retVal

        return S_OK(JEncoder.dumps(retVal["Value"]))
