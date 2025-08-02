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
"""Several utilities to "guess" the files names and the paths.

:author: sposs
:since: March 13th, 2013
"""
from __future__ import absolute_import
import six
__RCSID__ = "$Id$"

import os
from DIRAC import S_OK, S_ERROR
from DIRAC import gLogger
from ILCDIRAC.Core.Utilities.FilenameEncoder import FilenameEncoder, decodeFilename
###############################################################################


def getProdFilenameFromInput(inputfile, outfileOriginal, prodID, jobID):
  """Build the output file names based on inputfile name and job property.

  If outfileOriginal starts with 's' we assume a simulation job, if it starts
  with 'r' we assume a reconstruction job, if starts with "E" we assume
  a stdhepsplit job.

  :param str inputfile: Input file LFN, either \\*.stdhep or \\*.slcio
  :param str outfileOriginal: Output file LFN before change
  :param prodID: Production ID
  :type prodID: `str`, `int`
  :param jobID: jobID
  :type jobID: `str`, `int`
  :returns: Full LFN to changed output file
  """
  finp = FilenameEncoder()
  inpitem = decodeFilename(inputfile)

  origitem = decodeFilename(outfileOriginal)
  originalOutputBaseName = os.path.basename(outfileOriginal)

  outfile = ""
  if originalOutputBaseName.startswith("s"):
    inpitem["s"] = origitem["s"]
    inpitem["m"] = origitem["m"]
    inpitem["d"] = "sim"
    inpitem["t"] = str(prodID).zfill(8)
    inpitem["j"] = str(jobID)
    outfile = finp.convert("sim", "file", inpitem)
  elif originalOutputBaseName.startswith("r"):
    inpitem["r"] = origitem["r"]
    inpitem["m"] = origitem["m"] if "m" in origitem else inpitem["m"]  # Use model name defined by reconstruction
    inpitem["d"] = origitem["d"]
    inpitem["t"] = str(prodID).zfill(8)
    if "n" not in inpitem:  # For DBD sim files ad input
      inpitem["n"] = inpitem["j"] if "j" in inpitem else "0"
    inpitem["j"] = str(jobID)  # Allways use jobID given by production.
    outfile = finp.convert(origitem["d"], "file", inpitem)
  elif originalOutputBaseName.startswith("E"):
    inpitem["d"] = "gen"
    if "n" not in origitem:
      inpitem["n"] = "001"
    else:
      if "_" not in origitem["n"]:
        inpitem["n"] = origitem["n"]
      else:
        inpitem["n"] += "_" + origitem["n"].split("_", 1)[1]
    inpitem["t"] = str(prodID).zfill(8)
    inpitem["j"] = str(jobID)
    outfile = finp.convert("gen", "file", inpitem)
  else:  # Output as it is if not match above
    outfile = originalOutputBaseName

  basepath = os.path.dirname(outfileOriginal)
  return os.path.join(basepath, outfile)

###############################################################################


def getProdFilename(filename, prodID, jobID, workflow_commons=None):
  """Build the output file names based of local job property.

  If workflow_commons is given and contains a ProductionOutputData entry of
  six.string_types that file is returned.

  :param str filename: File name before change
  :param int prodID: Production ID
  :param int jobID: Job ID
  :param dict workflow_commons: workflow_commons dictionary
  :return: the modified file name
  """
  log = gLogger.getSubLogger("getProdFilename")

  if workflow_commons is not None:
    wfProdOut = workflow_commons.get('ProductionOutputData')
    if wfProdOut and isinstance(wfProdOut, six.string_types) and \
      ';' not in wfProdOut:  # a single prod output file
      outfile = wfProdOut
      return os.path.basename(outfile)

  knownFileTypes = ('.slcio', '.stdhep', '.root', '.lhe')
  outfile = ""
  if filename.endswith(knownFileTypes):
    name = filename.rsplit('.', 1)[0]
    extension = filename.rsplit('.', 1)[1]
    outfile = name + '_' + str(prodID) + '_' + str(jobID) + '.' + extension
  elif '.' in filename:
    name = filename.rsplit('.', 1)[0]
    extension = filename.rsplit('.', 1)[1]
    outfile = name + '_' + str(prodID) + '_' + str(jobID) + '.' + extension
  else:
    log.error('Dealing with untreatable outputfile!', filename)
    raise RuntimeError('Cannot treat this production filename!')
  return outfile

###############################################################################


def resolveIFpaths(inputfiles):
  """Try to find out in which sub-directory are each file. In the future, should be useless if PoolXMLCatalog can be used.

  :param list inputfiles: list of inputfiles
  :returns: S_OK(listOfFilePaths), S_ERROR
  """
  log = gLogger.getSubLogger("ResolveInputFiles")
  listoffiles = []
  string = "Will look for:"
  for myfile in inputfiles:
    if not len(myfile):
      continue
    listoffiles.append(os.path.basename(myfile))
    string += "%s\n" % os.path.basename(myfile)
  string = string.rstrip()
  log.info(string)

  listofpaths = []
  listofdirs = []
  for mydir in os.listdir(os.getcwd()):
    if os.path.isdir(mydir):
      listofdirs.append(mydir)
  filesnotfound = []
  for infile in listoffiles:
    filefound = False
    if os.path.exists(os.path.join(os.getcwd(), infile)):
      listofpaths.append(os.path.join(os.getcwd(), infile))
      filefound = True
    else:
      for mydir in listofdirs:
        if os.path.exists(os.path.join(os.getcwd(), mydir, infile)):
          listofpaths.append(os.path.join(os.getcwd(), mydir, infile))
          listofdirs.remove(mydir)
          filefound = True
          break
    if not filefound:
      filesnotfound.append(infile)
  if filesnotfound:
    log.error('The following files were not found locally:', ', '.join(filesnotfound))
    return S_ERROR('resolveIFPath: Input file(s) not found locally')
  log.verbose("Found all input files")
  return S_OK(listofpaths)
