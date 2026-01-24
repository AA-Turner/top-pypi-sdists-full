"""Do not edit by hand"""
from smartcard.util import toHexString
expectedReaders = ['Gemalto PC Twin Reader', 'Gemalto PC Twin Reader 01']
expectedATRs = [[59, 167, 0, 64, 24, 128, 101, 162, 8, 1, 1, 82], [59, 111, 0, 0, 128, 90, 40, 19, 2, 16, 18, 43, 117, 13, 211, 130, 130, 144, 0]]
expectedATRinReader = {}
for i, reader in enumerate(expectedReaders):
    expectedATRinReader[reader] = expectedATRs[i]
expectedReaderForATR = {}
for i, reader in enumerate(expectedReaders):
    expectedReaderForATR[toHexString(expectedATRs[i])] = reader
expectedReaderGroups = ['SCard$DefaultReaders']
