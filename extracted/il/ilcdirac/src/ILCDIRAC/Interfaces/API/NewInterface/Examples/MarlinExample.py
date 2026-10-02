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
"""This is a Marlin example."""
from __future__ import print_function
from __future__ import absolute_import
from DIRAC.Core.Base.Script import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
d = DiracILC(True, "repo.rep")

# In case one wants a loop: comment the folowing.
# for i in range(2):
j = UserJob()
j.setJobGroup("Tutorial")
j.setName("example")  # %i)

ma = Marlin()
ma.setVersion("v0111Prod")
ma.setSteeringFile("clic_ild_cdr_steering.xml")
ma.setGearFile("clic_ild_cdr.gear")
ma.setInputFile("LFN:/ilc/prod/clic/3tev/gghad/ILD/SIM/00000187/000/gghad_sim_187_97.slcio")
outdst = "toto.dst.slcio"  # % i
outrec = "toto.rec.slcio"  # % i
ma.setOutputDstFile(outdst)
ma.setOutputRecFile(outrec)

res = j.append(ma)
if not res['OK']:
  print(res['Message'])
  exit(1)

j.setOutputData([outdst, outrec], "some/path", "KEK-SRM")
j.setOutputSandbox("*.log")
j.dontPromptMe()
j.submit(d)
