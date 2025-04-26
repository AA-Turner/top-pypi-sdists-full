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
import os
import socket

import psutil
import xml.etree.ElementTree as ET
from pydantic import BaseModel as _BaseModel

import LHCbDIRAC


class BaseModel(_BaseModel, extra="forbid"):
    pass


DEFAULT_WNCPUPOWER = "unknown"
DEFAULT_WorkerNode = "unknown"
DEFAULT_WNMEMORY = "unknown"
DEFAULT_WNMODEL = "unknown"
DEFAULT_WNCACHE = "unknown"
try:
    DEFAULT_WNCPUPOWER = str(psutil.cpu_freq()[0])
    DEFAULT_WorkerNode = os.environ.get("HOSTNAME", os.environ.get("HOST", socket.gethostname()))
    DEFAULT_WNMEMORY = str(psutil.virtual_memory()[1] // 1024)
    with open("/proc/cpuinfo") as cpuinfo:
        info = cpuinfo.readlines()
    DEFAULT_WNMODEL = [x.strip().split(":")[1] for x in info if "model name" in x][0].strip()
    DEFAULT_WNCACHE = [x.strip().split(":")[1] for x in info if "cache size" in x][0].strip()
except Exception as x:
    pass


class BookkeepingJobInfo(BaseModel):
    ConfigName: str
    ConfigVersion: str
    Date: str
    Time: str

    class TypedParameters(BaseModel):
        CPUTIME: str | None = None
        ExecTime: str | None = None
        WNMODEL: str = DEFAULT_WNMODEL
        WNCPUPOWER: str = DEFAULT_WNCPUPOWER
        WNCACHE: str = DEFAULT_WNCACHE
        WorkerNode: str = DEFAULT_WorkerNode
        WNMEMORY: str = DEFAULT_WNMEMORY
        WNCPUHS06: str | None = None
        WNMJFHS06: str | None = None
        NumberOfProcessors: str | None = None
        Production: str | None = None
        DiracJobId: str | None = None
        Name: str | None = None
        JobStart: str | None = None
        JobEnd: str | None = None
        Location: str | None = None
        JobType: str | None = None
        ProgramName: str | None = None
        ProgramVersion: str | None = None
        DiracVersion: str = LHCbDIRAC.__version__
        FirstEventNumber: str | None = None
        StatisticsRequested: str | None = None
        StepID: str | None = None
        NumberOfEvents: str | None = None

    typed_parameters: TypedParameters = TypedParameters()

    input_files: list[str] = []

    class OutputFile(BaseModel):
        Name: str
        TypeName: str
        TypeVersion: str
        EventTypeId: str | None = None
        EventStat: str | None = None
        FileSize: str
        CreationDate: str
        MD5Sum: str
        Guid: str
        Replica: str | None = None

    output_files: list[OutputFile] = []

    simulation_condition: str | None = None

    def to_xml(self):
        root = ET.Element(
            "Job",
            ConfigName=self.ConfigName,
            ConfigVersion=self.ConfigVersion,
            Date=self.Date,
            Time=self.Time,
        )
        root.extend(
            [
                ET.Element("TypedParameter", Name=k, Value=str(v), Type="Info")
                for k, v in self.typed_parameters.model_dump().items()
                if v is not None
            ]
        )
        root.extend([ET.Element("InputFile", Name=lfn) for lfn in self.input_files])
        for output_file in self.output_files:
            data = dict(output_file.dict())
            output_file = ET.Element(
                "OutputFile",
                Name=data.pop("Name"),
                TypeName=data.pop("TypeName"),
                TypeVersion=data.pop("TypeVersion"),
            )
            if replica := data.pop("Replica"):
                output_file.append(ET.Element("Replica", Name=replica, Location="Web"))
            output_file.extend(
                [ET.Element("Parameter", Name=k, Value=str(v)) for k, v in data.items() if v is not None]
            )
            root.append(output_file)
        if self.simulation_condition is not None:
            simulation_condition = ET.Element("SimulationCondition")
            simulation_condition.append(ET.Element("Parameter", Name="SimDescription", Value=self.simulation_condition))
        ET.indent(root, "    ")
        return b"\n".join(
            [
                b'<?xml version="1.0" encoding="ISO-8859-1"?>\n',
                b'<!DOCTYPE Job SYSTEM "book.dtd">\n',
                ET.tostring(root, encoding="ISO-8859-1", method="xml", xml_declaration=False),
            ]
        )
