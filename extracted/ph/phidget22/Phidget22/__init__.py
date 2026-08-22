# Copyright (c) 2015-2026 Phidgets Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__version__='1.26.20260821'

from Phidget22.PhidgetException import PhidgetException
from Phidget22.NDEFRecords import NDEFURIRecord, NDEFTextRecord
from Phidget22.Phidget import Phidget
from Phidget22.Devices.Manager import Manager
from Phidget22.Net import Net
from Phidget22.Devices.Log import Log
from Phidget22.Devices.Accelerometer import Accelerometer
from Phidget22.Devices.BLDCMotor import BLDCMotor
from Phidget22.Devices.CapacitiveTouch import CapacitiveTouch
from Phidget22.Devices.CurrentInput import CurrentInput
from Phidget22.Devices.DataAdapter import DataAdapter
from Phidget22.Devices.DCMotor import DCMotor
from Phidget22.Devices.Dictionary import Dictionary
from Phidget22.Devices.DigitalInput import DigitalInput
from Phidget22.Devices.DigitalOutput import DigitalOutput
from Phidget22.Devices.DistanceSensor import DistanceSensor
from Phidget22.Devices.Encoder import Encoder
from Phidget22.Devices.FrequencyCounter import FrequencyCounter
from Phidget22.Devices.GPS import GPS
from Phidget22.Devices.Gyroscope import Gyroscope
from Phidget22.Devices.Hub import Hub
from Phidget22.Devices.HumiditySensor import HumiditySensor
from Phidget22.Devices.IR import IR
from Phidget22.Devices.LCD import LCD
from Phidget22.Devices.LEDArray import LEDArray
from Phidget22.Devices.LightSensor import LightSensor
from Phidget22.Devices.Magnetometer import Magnetometer
from Phidget22.Devices.MotorPositionController import MotorPositionController
from Phidget22.Devices.MotorVelocityController import MotorVelocityController
from Phidget22.Devices.PHSensor import PHSensor
from Phidget22.Devices.PowerGuard import PowerGuard
from Phidget22.Devices.PressureSensor import PressureSensor
from Phidget22.Devices.RCServo import RCServo
from Phidget22.Devices.ResistanceInput import ResistanceInput
from Phidget22.Devices.RFID import RFID
from Phidget22.Devices.SoundSensor import SoundSensor
from Phidget22.Devices.Spatial import Spatial
from Phidget22.Devices.Stepper import Stepper
from Phidget22.Devices.TemperatureSensor import TemperatureSensor
from Phidget22.Devices.VoltageInput import VoltageInput
from Phidget22.Devices.VoltageOutput import VoltageOutput
from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput
from Phidget22.EncoderIOMode import EncoderIOMode
from Phidget22.ErrorCode import ErrorCode
from Phidget22.ErrorEventCode import ErrorEventCode
from Phidget22.DeviceID import DeviceID
from Phidget22.LogLevel import LogLevel
from Phidget22.DeviceClass import DeviceClass
from Phidget22.ChannelClass import ChannelClass
from Phidget22.ChannelSubclass import ChannelSubclass
from Phidget22.PowerSupply import PowerSupply
from Phidget22.DataAdapterVoltage import DataAdapterVoltage
from Phidget22.RTDWireSetup import RTDWireSetup
from Phidget22.InputMode import InputMode
from Phidget22.FanMode import FanMode
from Phidget22.DriveMode import DriveMode
from Phidget22.PositionType import PositionType
from Phidget22.SpatialPrecision import SpatialPrecision
from Phidget22.Unit import Unit
from Phidget22.UnitInfo import UnitInfo
from Phidget22.PhidgetServerType import PhidgetServerType
from Phidget22.PhidgetServer import PhidgetServer
from Phidget22.BridgeGain import BridgeGain
from Phidget22.VoltageRatioSensorType import VoltageRatioSensorType
from Phidget22.LEDForwardVoltage import LEDForwardVoltage
from Phidget22.OutputVoltage import OutputVoltage
from Phidget22.RCServoVoltage import RCServoVoltage
from Phidget22.VoltageOutputRange import VoltageOutputRange
from Phidget22.VoltageOutputWaveformShape import VoltageOutputWaveformShape
from Phidget22.VoltageRange import VoltageRange
from Phidget22.VoltageSensorType import VoltageSensorType
from Phidget22.RFIDProtocol import RFIDProtocol
from Phidget22.RFIDChipset import RFIDChipset
from Phidget22.RFIDTagType import RFIDTagType
from Phidget22.RFIDTNF import RFIDTNF
from Phidget22.NDEFRecord import NDEFRecord
from Phidget22.GPSTime import GPSTime
from Phidget22.GPSDate import GPSDate
from Phidget22.GPGGA import GPGGA
from Phidget22.GPGSA import GPGSA
from Phidget22.GPRMC import GPRMC
from Phidget22.GPVTG import GPVTG
from Phidget22.NMEAData import NMEAData
from Phidget22.SpatialAlgorithm import SpatialAlgorithm
from Phidget22.SpatialQuaternion import SpatialQuaternion
from Phidget22.SpatialEulerAngles import SpatialEulerAngles
from Phidget22.RTDType import RTDType
from Phidget22.ThermocoupleType import ThermocoupleType
from Phidget22.FilterType import FilterType
from Phidget22.IRCodeEncoding import IRCodeEncoding
from Phidget22.IRCodeLength import IRCodeLength
from Phidget22.CodeInfo import CodeInfo
from Phidget22.StepperControlMode import StepperControlMode
from Phidget22.StepperMotionProfilePoint import StepperMotionProfilePoint
from Phidget22.LCDFont import LCDFont
from Phidget22.LCDScreenSize import LCDScreenSize
from Phidget22.LCDPixelState import LCDPixelState
from Phidget22.DataAdapterSPIMode import DataAdapterSPIMode
from Phidget22.DataAdapterFrequency import DataAdapterFrequency
from Phidget22.PacketErrorCode import PacketErrorCode
from Phidget22.DataAdapterSPIChipSelect import DataAdapterSPIChipSelect
from Phidget22.DataAdapterEndianness import DataAdapterEndianness
from Phidget22.DataAdapterParity import DataAdapterParity
from Phidget22.DataAdapterModbusFunction import DataAdapterModbusFunction
from Phidget22.LEDArrayColor import LEDArrayColor
from Phidget22.LEDArrayColorOrder import LEDArrayColorOrder
from Phidget22.LEDArrayAnimationType import LEDArrayAnimationType
from Phidget22.LEDArrayAnimation import LEDArrayAnimation
from Phidget22.SPLRange import SPLRange
from Phidget22.HubPortMode import HubPortMode

__all__ = [
    "PhidgetException",
    "NDEFURIRecord",
    "NDEFTextRecord",
    "Phidget",
    "Manager",
    "Net",
    "Log",
    "Accelerometer",
    "BLDCMotor",
    "CapacitiveTouch",
    "CurrentInput",
    "DataAdapter",
    "DCMotor",
    "Dictionary",
    "DigitalInput",
    "DigitalOutput",
    "DistanceSensor",
    "Encoder",
    "FrequencyCounter",
    "GPS",
    "Gyroscope",
    "Hub",
    "HumiditySensor",
    "IR",
    "LCD",
    "LEDArray",
    "LightSensor",
    "Magnetometer",
    "MotorPositionController",
    "MotorVelocityController",
    "PHSensor",
    "PowerGuard",
    "PressureSensor",
    "RCServo",
    "ResistanceInput",
    "RFID",
    "SoundSensor",
    "Spatial",
    "Stepper",
    "TemperatureSensor",
    "VoltageInput",
    "VoltageOutput",
    "VoltageRatioInput",
    "EncoderIOMode",
    "ErrorCode",
    "ErrorEventCode",
    "DeviceID",
    "LogLevel",
    "DeviceClass",
    "ChannelClass",
    "ChannelSubclass",
    "PowerSupply",
    "DataAdapterVoltage",
    "RTDWireSetup",
    "InputMode",
    "FanMode",
    "DriveMode",
    "PositionType",
    "SpatialPrecision",
    "Unit",
    "UnitInfo",
    "PhidgetServerType",
    "PhidgetServer",
    "BridgeGain",
    "VoltageRatioSensorType",
    "LEDForwardVoltage",
    "OutputVoltage",
    "RCServoVoltage",
    "VoltageOutputRange",
    "VoltageOutputWaveformShape",
    "VoltageRange",
    "VoltageSensorType",
    "RFIDProtocol",
    "RFIDChipset",
    "RFIDTagType",
    "RFIDTNF",
    "NDEFRecord",
    "GPSTime",
    "GPSDate",
    "GPGGA",
    "GPGSA",
    "GPRMC",
    "GPVTG",
    "NMEAData",
    "SpatialAlgorithm",
    "SpatialQuaternion",
    "SpatialEulerAngles",
    "RTDType",
    "ThermocoupleType",
    "FilterType",
    "IRCodeEncoding",
    "IRCodeLength",
    "CodeInfo",
    "StepperControlMode",
    "StepperMotionProfilePoint",
    "LCDFont",
    "LCDScreenSize",
    "LCDPixelState",
    "DataAdapterSPIMode",
    "DataAdapterFrequency",
    "PacketErrorCode",
    "DataAdapterSPIChipSelect",
    "DataAdapterEndianness",
    "DataAdapterParity",
    "DataAdapterModbusFunction",
    "LEDArrayColor",
    "LEDArrayColorOrder",
    "LEDArrayAnimationType",
    "LEDArrayAnimation",
    "SPLRange",
    "HubPortMode",
]
