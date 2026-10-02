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
"""Create Full Chain."""
from __future__ import print_function
from __future__ import absolute_import
from DIRAC.Core.Base.Script import Script
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Whizard, Mokka, Marlin, OverlayInput
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob

from DIRAC import exit as dexit

dirac = DiracILC()

# wh.setOutputFile("myfile.stdhep")

j = UserJob()

wh = Whizard(processlist=dirac.getProcessList())
wh.setEnergy(3000)
wh.setEvtType("ee_h_mumu")
wh.setNbEvts(1)
wh.setEnergy(3000)
params = {}
params['USERB1'] = 'F'
wh.setParameterDict(params)
wh.setModel("sm")
res = j.append(wh)
if not res['OK']:
  print(res['Message'])
  dexit(1)


mo = Mokka()
mo.getInputFromApp(wh)
mo.setVersion("0706P08")
mo.setSteeringFile("clic_ild_cdr.steer")
mo.setNbEvts(1)
mo.setOutputFile("somefile.slcio")
res = j.append(mo)
if not res['OK']:
  print(res['Message'])
  dexit(1)


ov = OverlayInput()
ov.setDetectorModel("CLIC_ILD_CDR")
ov.setBXOverlay(60)
ov.setGGToHadInt(3.2)
ov.setNbSigEvtsPerJob(1)
ov.setBkgEvtType("gghad")
res = j.append(ov)
if not res['OK']:
  print(res['Message'])
  dexit(1)


ma = Marlin()
ma.setVersion("v0111Prod")
ma.setSteeringFile("clic_ild_cdr_steering_overlay.xml")
ma.setGearFile("clic_ild_cdr.gear")
ma.getInputFromApp(mo)
ma.setDebug(True)
res = j.append(ma)
if not res['OK']:
  print(res['Message'])
  dexit(1)
# print appplication's attributes.
ma.listAttributes()

j.setName("test")
j.setOutputSandbox("*.log")

res = dirac.checkparams(j)
if not res['OK']:
  print(res['Message'])
  dexit(1)
