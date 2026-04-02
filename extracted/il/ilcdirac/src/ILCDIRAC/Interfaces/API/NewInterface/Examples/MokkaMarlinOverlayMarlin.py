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
"""Overlay with Marlin and Mokka."""
from __future__ import print_function
from __future__ import absolute_import
from DIRAC.Core.Base.Script import Script
from six.moves import range
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Mokka, Marlin, OverlayInput
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

from DIRAC import exit as dexit

d = DiracILC(True, "repo.rep")


n_evts = 500
n_evts_per_job = 100
n_jobs = n_evts / n_evts_per_job

for i in range(n_jobs):
  j = UserJob()

  mo = Mokka()
  mo.setEnergy(3000)
  mo.setVersion("0706P08")
  mo.setSteeringFile("clic_ild_cdr.steer")
  mo.setMacFile("particlegun_electron.mac")
  mo.setOutputFile("MyFile.slcio")
  mo.setNbEvts(n_evts_per_job)
  res = j.append(mo)
  if not res['OK']:
    print(res['Message'])
    break
  ma = Marlin()
  ma.setVersion("v0111Prod")
  ma.setSteeringFile("clic_ild_cdr_steering.xml")
  ma.getInputFromApp(mo)
  ma.setOutputDstFile("mydst_no_ov_%s.slcio" % i)
  res = j.append(ma)
  if not res['OK']:
    print(res['Message'])
    break
  ov = OverlayInput()
  ov.setBXOverlay(60)
  ov.setGGToHadInt(3.2)
  ov.setNbSigEvtsPerJob(n_evts_per_job)
  ov.setBkgEvtType("gghad")
  ov.setDetectorModel("CLIC_ILD_CDR")

  res = j.append(ov)
  if not res['OK']:
    print(res['Message'])
    break
  ma2 = Marlin()
  ma2.setVersion("v0111Prod")
  ma2.setSteeringFile("clic_ild_cdr_steering_overlay.xml")
  ma2.getInputFromApp(mo)
  ma2.setOutputDstFile("mydst_ov_%s.slcio" % i)
  res = j.append(ma2)
  if not res['OK']:
    print(res['Message'])
    break
  j.setOutputSandbox(["mydst_no_ov_%s.slcio" % i, "mydst_ov_%s.slcio" % i, "*.log"])
  j.setName("SingleElectron_%s" % i)
  j.setJobGroup("singleElectrons")

  j.submit(d)

dexit(0)
