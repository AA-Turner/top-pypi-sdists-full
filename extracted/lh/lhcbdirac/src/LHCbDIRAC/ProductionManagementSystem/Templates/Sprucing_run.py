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
"""The Sprucing template creates workflows for the following use-cases:
  WORKFLOW1: Sprucing
  WORKFLOW2: Sprucing+Merge
"""

import ast

from DIRAC import initialize

initialize()

from DIRAC import gConfig, gLogger, exit as DIRACexit
from LHCbDIRAC.ProductionManagementSystem.Client.ProductionRequest import ProductionRequest

gLogger = gLogger.getSubLogger("Sprucing_run.py")

pr = ProductionRequest()

stepsList = ["{{p1Step}}"]
stepsList.append("{{p2Step}}")
stepsList.append("{{p3Step}}")
stepsList.append("{{p4Step}}")
stepsList.append("{{p5Step}}")
stepsList.append("{{p6Step}}")
stepsList.append("{{p7Step}}")
stepsList.append("{{p8Step}}")
stepsList.append("{{p9Step}}")
pr.stepsList = stepsList

###########################################
# Configurable and fixed parameters
###########################################

pr.appendName = "{{WorkflowAppendName#GENERAL: Workflow string to append to production name#1}}"

w = "{{w#----->WORKFLOW: choose one below#}}"
w1 = "{{w1#-WORKFLOW1: Sprucing#False}}"
w2 = "{{w2#-WORKFLOW2: Sprucing+Merge#False}}"

validationFlag = "{{validationFlag#GENERAL: Set True for validation prod#False}}"

# workflow params for all productions
pr.startRun = "{{startRun#GENERAL (obligatory): run start, to set the start run#0}}"
pr.endRun = "{{endRun#GENERAL (obligatory): run end, to set the end of the range#0}}"
pr.runsList = "{{runsList#GENERAL: discrete list of run numbers (do not mix with start/endrun)#}}"
pr.derivedProduction = "{{AncestorProd#GENERAL: ancestor prod to be derived#0}}"
eventTimeouts = "{{eventTimeouts#GENERAL: event timeouts as python dict stepNumber:seconds#}}"
if eventTimeouts:
    pr.eventTimeouts = ast.literal_eval(eventTimeouts)

# spruc params
sprucPriority = int("{{priority#PROD-1:sprucing: priority#2}}")
sprucCPU = "{{sprucMaxCPUTime#PROD-1:sprucing: Max CPU time in secs#1000000}}"
sprucPlugin = "{{sprucPluginType#PROD-1:sprucing: plugin name#Sprucing}}"
sprucFilesPerJob = "{{sprucFilesPerJob#PROD-1:sprucing: Group size or number of files per job#2}}"
sprucDataSE = "{{sprucStreamSE#PROD-1:sprucing: output data SE (un-merged streams)#Tier1-Buffer}}"
try:
    sprucDataSESpecial = ast.literal_eval("{{sprucDataSESpecial#PROD-1:sprucing: Special SE (a dictionary Type:SE)#}}")
except SyntaxError:
    sprucDataSESpecial = {}
sprucAncestorDepth = int("{{sprucAncestorDepth#PROD-1: Ancestor Depth#0}}")
sprucCompressionLvl = "{{sprucCompressionLvl#PROD-1: compression level#LOW}}"
sprucOutputVisFlag = "{{sprucOutputVisFlag#PROD-1: Visibility flag of output files#N}}"
try:
    sprucOutputVisFlagSpecial = ast.literal_eval(
        "{{sprucOutputVisFlagSpecial#PROD-1: Special Visibility flag of output files (dict FType:Y|N)#}}"
    )
except SyntaxError:
    sprucOutputVisFlagSpecial = {}

# merging params
mergingPriority = int("{{MergePriority#PROD-2:Merging: priority#8}}")
mergingCPU = "{{MergeMaxCPUTime#PROD-2:Merging: Max CPU time in secs#300000}}"
mergingPlugin = "{{MergePlugin#PROD-2:Merging: plugin#ByRunFileTypeSizeWithFlush}}"
mergingGroupSize = "{{MergeFileSize#PROD-2:Merging: Size (in GB) of the merged files#5}}"
mergingDataSE = "{{MergeStreamSE#PROD-2:Merging: output data SE (merged streams)#Tier1-DST}}"
try:
    mergingDataSESpecial = ast.literal_eval(
        "{{MergingDataSESpecial#PROD-2:Merging: Special SE (a dictionary Type:SE)#}}"
    )
except SyntaxError:
    mergingDataSESpecial = {}
mergingRemoveInputsFlag = "{{MergeRemoveFlag#PROD-2:Merging: remove input data flag True/False#True}}"
mergeCompressionLvl = "{{mergeCompressionLvl#PROD-2: compression level#HIGH}}"
mergeOutputVisFlag = "{{mergeOutputVisFlag#PROD-2: Visibility flag of output files#Y}}"
try:
    mergeOutputVisFlagSpecial = ast.literal_eval(
        "{{mergeOutputVisFlagSpecial#PROD-2: Special Visibility flag of output files (dict FType:Y|N)#}}"
    )
except SyntaxError:
    mergeOutputVisFlagSpecial = {}

pr.requestID = "{{ID}}"
pr.prodGroup = "{{inProPass}}" + "/" + "{{pDsc}}"
# used in case of a test e.g. certification etc.
pr.configName = "{{configName}}"
pr.configVersion = "{{configVersion}}"
# Other parameters from the request page
pr.dqFlag = "{{inDataQualityFlag}}"  # UNCHECKED
pr.dataTakingConditions = "{{simDesc}}"
pr.processingPass = "{{inProPass}}"
pr.bkFileType = "{{inFileType}}"
pr.eventType = "{{eventType}}"
pr.visibility = "Yes"
targetSite = "ALL"
sprucMulticoreFlag = mergeMulticoreFlag = "True"
sprucIDPolicy = mergingIDPolicy = "download"


w1 = ast.literal_eval(w1)
w2 = ast.literal_eval(w2)

validationFlag = ast.literal_eval(validationFlag)

mergeRemoveInputsFlag = ast.literal_eval(mergingRemoveInputsFlag)

if not w1 and not w2:
    gLogger.error("I told you to select at least one workflow!")
    DIRACexit(2)

pr.outConfigName = pr.configName

# In case we want just to test, we publish in the certification/test part of the BKK
if gConfig.getValue("DIRAC/Setup") == "LHCb-Certification":
    pr.outConfigName = "certification"
    if "lhcb" not in pr.configName.lower():  # in case of reconstruction
        pr.configVersion = "test"

if validationFlag:
    pr.outConfigName = "validation"

if w1:
    pr.prodsTypeList = ["Sprucing"]
    pr.outputSEs = [sprucDataSE]
    pr.specialOutputSEs = [sprucDataSESpecial]
    pr.stepsInProds = [list(range(1, len(pr.stepsList) + 1))]
    pr.removeInputsFlags = [False]
    pr.priorities = [sprucPriority]
    pr.cpus = [sprucCPU]
    pr.groupSizes = [sprucFilesPerJob]
    pr.plugins = [sprucPlugin]
    pr.inputs = [[]]
    pr.inputDataPolicies = [sprucIDPolicy]
    pr.bkQueries = ["Full"]
    pr.targets = [targetSite]
    pr.multicore = [sprucMulticoreFlag]
    pr.outputModes = ["Run"]
    pr.ancestorDepths = [sprucAncestorDepth]
    pr.compressionLvl = [sprucCompressionLvl] * len(pr.stepsInProds[0])
    pr.outputVisFlag = [{str(i + 1): sprucOutputVisFlag} for i in range(len(pr.stepsInProds[0]))]
    pr.specialOutputVisFlag = [{"1": sprucOutputVisFlagSpecial}]

elif w2:
    pr.prodsTypeList = ["Sprucing", "Merge"]
    pr.outputSEs = [sprucDataSE, mergingDataSE]
    pr.specialOutputSEs = [sprucDataSESpecial, mergingDataSESpecial]
    pr.stepsInProds = [list(range(1, len(pr.stepsList))), [len(pr.stepsList)]]
    pr.removeInputsFlags = [False, mergeRemoveInputsFlag]
    pr.priorities = [sprucPriority, mergingPriority]
    pr.cpus = [sprucCPU, mergingCPU]
    pr.groupSizes = [sprucFilesPerJob, mergingGroupSize]
    pr.plugins = [sprucPlugin, mergingPlugin]
    pr.inputs = [[], []]
    pr.inputDataPolicies = [sprucIDPolicy, mergingIDPolicy]
    pr.bkQueries = ["Full", "fromPreviousProd"]
    pr.targets = [targetSite, targetSite]
    pr.multicore = [sprucMulticoreFlag, mergeMulticoreFlag]
    pr.outputModes = ["Run", "Run"]
    pr.ancestorDepths = [sprucAncestorDepth, 0]
    pr.compressionLvl = [sprucCompressionLvl] * len(pr.stepsInProds[0]) + [mergeCompressionLvl] * len(
        pr.stepsInProds[1]
    )
    pr.outputVisFlag = [{"1": sprucOutputVisFlag}, {"2": mergeOutputVisFlag}]
    pr.specialOutputVisFlag = [{"1": sprucOutputVisFlagSpecial}, {"2": mergeOutputVisFlagSpecial}]


if not (pr.startRun and pr.endRun) and not pr.runsList:
    gLogger.error("Please do select a start and an end run, or a runs list")
    DIRACexit(2)

pr.buildAndLaunchRequest()
