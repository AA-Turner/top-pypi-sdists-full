#
# Copyright (c) 2009-2022 CERN. All rights nots expressly granted are
# reserved.
#
# This file is part of iLCDirac
# (see ilcdirac.cern.ch, contact: ilcdirac-support@cern.ch).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# In applying this licence, CERN does not waive the privileges and
# immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""This module implements an extension of the SingularityComputingElement that automatically deduces the OS image to use for a given job.

By default it uses the container for the ``/Operations/Defaults/Software/DefaultSingularityOS`` operating system,
defined under ``/Software/Containers/``. If the Application has an ``OS`` entry that will be used to find the image to
use. If the application has a ``CVMFSEnvScript`` but not ``OS``, we look for a substring match to identify the OS and
thus the container. Applications can also directly define ``ApptainerImage`` to specify that.  Or Jobs can define
``ApptainerImage`` in their JDL == JobParameters to shortcut any selection logic.

"""

from pprint import pformat

from DIRAC import S_ERROR

from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Resources.Computing.SingularityComputingElement import SingularityComputingElement

from ILCDIRAC.Core.Utilities.DetectOS import NativeMachine
from ILCDIRAC.Core.Utilities.Utilities import listify
class AutoSingularityComputingElement(SingularityComputingElement):
    """A computing element based on singularity that will automatically deduce the OS container it should run based on job
parameters."""

    def __init__(self, ceUniqueID):
        """Standard constructor."""
        super().__init__(ceUniqueID)

    def submitJob(self, executableFile, proxy=None, **kwargs):
       """Figure out the rootImage and call super submitJob"""
       self.log.debug("The kwargs are", pformat(kwargs))

       jobParameters = kwargs.get("jobDesc", {}).get("jobParams", {})

       # If the ApptainerImage is defined in the JobParameters / JDL we use it
       if theImage := jobParameters.get("ApptainerImage"):
           self.log.info(f"And we are using {theImage!r} from jobParameters")
           self._SingularityComputingElement__root = theImage
           return super().submitJob(executableFile, proxy=proxy, **kwargs)

       # we get the list of SoftwarePackages from the jobParameters
       apps = []
       if softPackages := jobParameters.get("SoftwarePackages"):
           if isinstance(softPackages, str):
               apps = [softPackages]
           elif isinstance(softPackages, list):
               apps = softPackages

       # Figure out the platform we are using since we have platform in the jobparameters
       # this is needed for finding the software package options
       jobConfig = ""
       if jobConfig := jobParameters.get("SystemConfig"):
           pass
       elif jobConfig := jobParameters.get("Platform"):
           pass
       else:
           jobConfig = NativeMachine().CMTSupportedConfig()[0]

       ops = Operations()
       # the default os we use, should be taken from VO specific operations section like this
       theOS = ops.getValue("/Software/DefaultSingularityOS", "el9")
       self.log.info("We found the defaultOS to use", theOS)
       theDefaultImage = ops.getValue("/Software/Containers/default")
       self.log.info(f"The default image would be {theDefaultImage}")

       imageSet = set()
       osSet = set()
       if apps:
           # if we have applications, check, if there is a specific image to use, or other OS to use
           for app in apps:
               appName, appVersion= app.split(".")
               # check if the software app has an ApptainerImage defined and use that
               if theImage := ops.getValue(f"/AvailableTarBalls/{jobConfig}/{appName}/{appVersion}/ApptainerImage", None):
                   self.log.info(f"And found {theImage!r} from the {appName}/{appVersion}")
                   imageSet.add(theImage)
                   continue

               # if there is an OS defined we are going to use that to figure out the image to use
               appOS = ops.getValue(f"/AvailableTarBalls/{jobConfig}/{appName}/{appVersion}/OS", None)
               if appOS:
                   self.log.info(f"Based on /AvailableTarBalls/{jobConfig}/{appName}/{appVersion}/OS")
                   osSet.add(appOS)
                   continue

               envScriptPath = ops.getValue(f"/AvailableTarBalls/{jobConfig}/{appName}/{appVersion}/CVMFSEnvScript", None)
               self.log.info(f"Did we find an env script?: {envScriptPath}")
               if envScriptPath is not None:
                   osEquivalence = ops.getOptionsDict("/Software/OperatingSystems").get("Value", {})
                   for anOS, equals in osEquivalence.items():
                       # let us guess the operating system
                       if any(opSys in envScriptPath for opSys in listify(equals)):
                           self.log.info(f"We found a matching OS: {anOS}")
                           osSet.add(anOS)

       # check that allOS are the same
       if len(osSet) > 1:
           self.log.error("We found different Operating Systems for the applications", osSet)
           return S_ERROR("Cannot deduce the image to use. Too many Operating Systems")
       if len(imageSet) > 1:
           self.log.error("We found multiple images for the applications", imageSet)
           return S_ERROR("Cannot deduce the image to use. Too many Images")

       # what if we found operating system and image to use?

       if imageSet:
           self._SingularityComputingElement__root = imageSet.pop()
           return super().submitJob(executableFile, proxy=proxy, **kwargs)

       if osSet:
           self.log.info(f"We are now going to use {theOS}")
           theOS = osSet.pop()

       theImage = ops.getValue(f"/Software/Containers/{theOS}", theDefaultImage)
       self.log.info(f"And we are using: {theImage}")

       self._SingularityComputingElement__root = theImage
       return super().submitJob(executableFile, proxy=proxy, **kwargs)
