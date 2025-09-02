import logging
import random
import math
import pyaes

from crownstone_core.Constants import UserLevel
from crownstone_core.Exceptions import CrownstoneBleException, EncryptionError
from crownstone_core.util.Conversion import Conversion

BLOCK_LENGTH             = 16
NONCE_LENGTH             = 16
SESSION_DATA_LENGTH      = 5
SESSION_KEY_LENGTH       = 4
PACKET_USER_LEVEL_LENGTH = 1
PACKET_NONCE_LENGTH      = 3
CHECKSUM                 = 0xcafebabe

_LOGGER = logging.getLogger(__name__)

class EncryptedPackage:
    
    def __init__(self, dataArray):
        self.nonce = None
        self.userLevel = None
        self.payload = None
        
        prefixLength = PACKET_NONCE_LENGTH + PACKET_USER_LEVEL_LENGTH
        if len(dataArray) < prefixLength + BLOCK_LENGTH:
            raise CrownstoneBleException(EncryptionError.INVALID_ENCRYPTION_PACKAGE, "Invalid package for encryption. It is too short (min length 20) got " + str(len(dataArray)) + " bytes.")

        self.nonce = [0] * PACKET_NONCE_LENGTH
        
        for i in range(0, PACKET_NONCE_LENGTH):
            self.nonce[i] = dataArray[i]
            
        if dataArray[PACKET_NONCE_LENGTH] > 2 and dataArray[PACKET_NONCE_LENGTH] != UserLevel.setup.value:
            raise CrownstoneBleException(EncryptionError.INVALID_ENCRYPTION_USER_LEVEL, "User level in read packet is invalid:" + str(dataArray[PACKET_NONCE_LENGTH]))
        
        try:
            self.userLevel = UserLevel(dataArray[PACKET_NONCE_LENGTH])
        except ValueError:
            raise CrownstoneBleException(EncryptionError.INVALID_ENCRYPTION_USER_LEVEL, "User level in read packet is invalid:" + str(dataArray[PACKET_NONCE_LENGTH]))
        
        payload = [0] * (len(dataArray) - prefixLength)
        for i in range(0, (len(dataArray) - prefixLength)):
            payload[i] = dataArray[i + prefixLength]
            
        if len(payload) % 16 != 0:
            raise CrownstoneBleException(EncryptionError.INVALID_ENCRYPTION_PACKAGE, f"Invalid size for encrypted payload: len={len(payload)} payload={payload}")
        
        self.payload = payload


class EncryptionHandler:
    

    @staticmethod
    def decryptECB(uint8Array, key):
        aes = pyaes.AESModeOfOperationECB(key)
        
        stringPayload = "".join(chr(b) for b in uint8Array)
        
        decrypted = aes.decrypt(stringPayload)
        
        return decrypted


    @staticmethod
    def encryptECB(uint8Array, key):
        aes = pyaes.AESModeOfOperationECB(key)
    
        stringPayload = "".join(chr(b) for b in uint8Array)
    
        encrypted = aes.encrypt(stringPayload)
    
        return encrypted


    @staticmethod
    def decryptCTR(data, packetNonce, sessionNonce, key):
        IV = EncryptionHandler.generateIV(packetNonce, sessionNonce)
    
        stringPayload = "".join(chr(b) for b in data)
    
        aes = pyaes.AESModeOfOperationCTR(key, counter=IVCounter(IV))
    
        decryptedData = aes.decrypt(stringPayload)
    
        return decryptedData


    @staticmethod
    def decrypt(data, settings):
        if settings.sessionNonce is None:
            raise CrownstoneBleException(EncryptionError.NO_SESSION_NONCE_SET, "Can't Decrypt: No session nonce set")
    
        if settings.userLevel == UserLevel.unknown:
            raise CrownstoneBleException(EncryptionError.NO_ENCRYPTION_KEYS_SET, "Can't Decrypt: No encryption keys set.")
        
        #unpack the session data
        package = EncryptedPackage(data)
        
        key = EncryptionHandler._getKeyForLevel(package.userLevel, settings)
    
        # decrypt data
        decrypted = EncryptionHandler.decryptCTR(package.payload, package.nonce, settings.sessionNonce, key)
        
        return EncryptionHandler._verifyDecryption(decrypted, settings.validationKey)
    
    
    @staticmethod
    def _verifyDecryption(decrypted, validationKey):
        # the conversion to uint32 only takes the first 4 bytes
        if Conversion.uint8_array_to_uint32(decrypted) == Conversion.uint8_array_to_uint32(validationKey):
            # remove checksum from decryption and return payload
            result = [0] * (len(decrypted) - SESSION_KEY_LENGTH)
            for i in range(0,len(result)):
                result[i] = decrypted[i+SESSION_KEY_LENGTH]
            return result
    
        else:
            raise CrownstoneBleException(EncryptionError.ENCRYPTION_VALIDATION_FAILED, "Failed to validate result, Could not decrypt")
            
    
    @staticmethod
    def getRandomNumber(testing=False):
        if testing:
            return 128
        return random.randint(0,255)


    @staticmethod
    def encryptCTR(dataArray, packetNonce, settings, key):

        IV = EncryptionHandler.generateIV(packetNonce, settings.sessionNonce)
        
        # calculate the amount of blocks
        amountOfBlocks = int(math.ceil(float(SESSION_KEY_LENGTH + len(dataArray)) / float(BLOCK_LENGTH)))
    
        # create buffer that is zero padded
        paddedPayload = [0] * amountOfBlocks * BLOCK_LENGTH
    
        # fill the payload with the key and the data
        for i in range(0, SESSION_KEY_LENGTH):
            paddedPayload[i] = settings.validationKey[i]
    
        for i in range(0, len(dataArray)):
            paddedPayload[i + SESSION_KEY_LENGTH] = dataArray[i]
    
        stringPayload = "".join(chr(b) for b in paddedPayload)
    
        aes = pyaes.AESModeOfOperationCTR(key, counter=IVCounter(IV))
    
        encryptedData = aes.encrypt(stringPayload)
        
        return encryptedData
    
    @staticmethod
    def encrypt(dataArray, settings):
        if settings.sessionNonce is None:
            raise CrownstoneBleException(EncryptionError.NO_SESSION_NONCE_SET, "Can't Decrypt: No session nonce set")
    
        if settings.userLevel == UserLevel.unknown:
            raise CrownstoneBleException(EncryptionError.NO_ENCRYPTION_KEYS_SET, "Can't Decrypt: No encryption keys set.")

        packetNonce = [0] * PACKET_NONCE_LENGTH
        # create a random nonce
        for i in range(0, PACKET_NONCE_LENGTH):
            packetNonce[i] = EncryptionHandler.getRandomNumber()
        
        key = EncryptionHandler._getKey(settings)
        encryptedData = EncryptionHandler.encryptCTR(dataArray, packetNonce, settings, key)
    
        result = packetNonce + [settings.userLevel.value]
        
        for byte in encryptedData:
            result.append(byte)
    
        return bytes(result)
            
    
    @staticmethod
    def _getKey(settings):
        return EncryptionHandler._getKeyForLevel(settings.userLevel, settings)
        
    @staticmethod
    def _getKeyForLevel(userLevel: UserLevel, settings):
        _LOGGER.debug(f"get key for level {userLevel}")
        if settings.initializedKeys == False and userLevel != UserLevel.setup:
            raise CrownstoneBleException(EncryptionError.NO_ENCRYPTION_KEYS_SET, "Could not encrypt: Keys not set.")
    
        key = None
        if userLevel == UserLevel.admin:
            key = settings.adminKey
        elif userLevel == UserLevel.member:
            key = settings.memberKey
        elif userLevel == UserLevel.basic:
            key = settings.basicKey
        elif userLevel == UserLevel.setup:
            key = settings.setupKey
        else:
            raise CrownstoneBleException(EncryptionError.NO_ENCRYPTION_KEYS_SET, "Could not encrypt: Invalid key for encryption.")
    
        if key is None:
            raise CrownstoneBleException(EncryptionError.NO_ENCRYPTION_KEYS_SET, "Could not encrypt: Keys not set.")
    
        return key
        
    
    @staticmethod
    def generateIV(packetNonce, sessionData):
        if len(packetNonce) != PACKET_NONCE_LENGTH:
            raise CrownstoneBleException(EncryptionError.INVALID_SESSION_NONCE, "Invalid size for session nonce packet")
        
        IV = [0] * NONCE_LENGTH
        
        # the IV used in the CTR mode is 8 bytes, the first 3 are random
        for i in range(0,PACKET_NONCE_LENGTH):
            IV[i] = packetNonce[i]
        
        # the IV used in the CTR mode is 8 bytes, the last 5 are from the session data
        for i in range(0,SESSION_DATA_LENGTH):
            IV[i + PACKET_NONCE_LENGTH] = sessionData[i]
            
        return IV

    """
     * This method is used to encrypt data with the CTR method and wrap the envelope around it according to protocol V5
    """
    @staticmethod
    def encryptBroadcast(dataArray, key, IV, validationNonce):
        IV = IV + [0] * (NONCE_LENGTH - len(IV))

        # create buffer that is zero padded
        paddedPayload = [0] * BLOCK_LENGTH

        # fill the payload with the key and the data
        for i in range(0, SESSION_KEY_LENGTH):
            paddedPayload[i] = validationNonce[i]

        for i in range(0, len(dataArray)):
            paddedPayload[i + SESSION_KEY_LENGTH] = dataArray[i]

        stringPayload = "".join(chr(b) for b in paddedPayload)

        aes = pyaes.AESModeOfOperationCTR(key, counter=IVCounter(IV))

        encryptedData = aes.encrypt(stringPayload)

        return encryptedData


    
class IVCounter(object):
    """
        A counter object for the Counter (CTR) mode of operation.

       To create a custom counter, you can usually just override the
       increment method.
    """
    
    def __init__(self, initialList):
        
        # Convert the value into an array of bytes long
        self._counter = initialList

    def get_value(self):
        return self._counter

    value = property(get_value)
    
    def increment(self):
        self._counter[len(self._counter)-1] += 1

        
