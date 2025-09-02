import logging

from crownstone_core.Constants import UserLevel
from crownstone_core.Exceptions import CrownstoneBleException, EncryptionError
from crownstone_core.protocol.BlePackets import SUPPORTED_PROTOCOL_VERSION
from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.EncryptionHandler import SESSION_KEY_LENGTH, SESSION_DATA_LENGTH


_LOGGER = logging.getLogger(__name__)

class EncryptionSettings:
    
    def __init__(self):
        self.adminKey = None
        self.memberKey = None
        self.basicKey = None
        self.setupKey = None
        self.serviceDataKey = None
        self.localizationKey = None
        self.meshApplicationKey = None
        self.meshNetworkKey = None

        self.sessionNonce = None
        self.crownstoneProtocolVersion = None
        self.validationKey = None
        self.initializedKeys = False
        self.temporaryDisable = False
        self.userLevel = UserLevel.unknown


    def loadKeys(self, adminKey, memberKey, basicKey, serviceDataKey, localizationKey, meshApplicationKey, meshNetworkKey):
        self.adminKey  = Conversion.ascii_or_hex_string_to_16_byte_array(adminKey)
        self.memberKey = Conversion.ascii_or_hex_string_to_16_byte_array(memberKey)
        self.basicKey  = Conversion.ascii_or_hex_string_to_16_byte_array(basicKey)
        self.serviceDataKey  = Conversion.ascii_or_hex_string_to_16_byte_array(serviceDataKey)
        self.localizationKey  = Conversion.ascii_or_hex_string_to_16_byte_array(localizationKey)
        self.meshApplicationKey = Conversion.ascii_or_hex_string_to_16_byte_array(meshApplicationKey)
        self.meshNetworkKey  = Conversion.ascii_or_hex_string_to_16_byte_array(meshNetworkKey)

        self.initializedKeys = True
        self.determineUserLevel()
        

    def determineUserLevel(self):
        if   len(self.adminKey)  == 16:
            self.userLevel = UserLevel.admin
        elif len(self.memberKey) == 16:
            self.userLevel = UserLevel.member
        elif len(self.basicKey)  == 16:
            self.userLevel = UserLevel.basic
        else:
            self.userLevel = UserLevel.unknown
            self.initializedKeys = False


    def invalidateSessionNonce(self):
        self.sessionNonce = None
        self.validationKey = None
        self.crownstoneProtocolVersion = 0


    def setSessionNonce(self, sessionNonce):
        if len(sessionNonce) != SESSION_DATA_LENGTH:
            raise CrownstoneBleException(EncryptionError.INVALID_SESSION_DATA, "Invalid Session Data")
        self.sessionNonce = sessionNonce

    def setValidationKey(self, validationKey):
        if len(validationKey) != SESSION_KEY_LENGTH:
            raise CrownstoneBleException(EncryptionError.INVALID_SESSION_DATA, "Invalid Session Data")
        self.validationKey = validationKey

    def setCrownstoneProtocolVersion(self, protocolVersion):
        self.crownstoneProtocolVersion = protocolVersion
        if protocolVersion != SUPPORTED_PROTOCOL_VERSION:
            print("Warning: Crownstone has protocol version", protocolVersion, "while the library uses", SUPPORTED_PROTOCOL_VERSION, ". Check if you have the correct version of the library for your firmware version.")

    def loadSetupKey(self, setupKey):
        _LOGGER.debug(f"loadSetupKey")
        self.setupKey  = setupKey
        self.userLevel = UserLevel.setup

    def exitSetup(self):
        _LOGGER.debug(f"exitSetup")
        self.setupKey = None
        self.determineUserLevel()


    def disableEncryptionTemporarily(self):
        self.temporaryDisable = True


    def restoreEncryption(self):
        self.temporaryDisable = False


    def isTemporarilyDisabled(self):
        return self.temporaryDisable


    def isEncryptionEnabled(self):
        if self.temporaryDisable:
            return False
        return True






