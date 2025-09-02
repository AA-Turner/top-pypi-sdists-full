import time

from crownstone_core.util.Conversion import Conversion


def obtainTimestamp(fullTimeStamp, lsbTimestamp):
	"""
	Combines the full timestamp with a partial timestamp.

	:param fullTimeStamp:         Full unix timestamp.
	:param lsbTimestamp:          Partial (least significant) timestamp, as a uint16.
	:returns:                     Unix timestamp with the least significant bytes set to the partial timestamp.
	"""
	restoredTimestamp = (int(fullTimeStamp) & 0xFFFF0000) + (int(lsbTimestamp) & 0x0000FFFF)
	return restoredTimestamp


def reconstructTimestamp(currentTimestamp, lsbTimestamp):
	"""
	Reconstructs a timestamp from a partial timestamp, that only has the least significant bytes.

	:param currentTimestamp:      Current time, obtained with time.time().
	:param lsbTimestamp:          Partial (least significant) timestamp, as a uint16.
	:returns:                     Reconstructed unix timestamp.
	"""
	# embed location data in the timestamp
	correctedTimestamp = getCorrectedLocalTimestamp(currentTimestamp)

	# attempt restoration
	restoredTimestamp = obtainTimestamp(correctedTimestamp, lsbTimestamp)

	halfUInt16 = 0x7FFF # roughly 9 hours in seconds

	# correct for overflows, check for drift from current time
	delta = correctedTimestamp - restoredTimestamp

	if -halfUInt16 < delta < halfUInt16:
		return restoredTimestamp
	elif delta < -halfUInt16:
		restoredTimestamp = obtainTimestamp(correctedTimestamp - 0xFFFF, lsbTimestamp)
	elif delta > halfUInt16:
		restoredTimestamp = obtainTimestamp(correctedTimestamp + 0xFFFF, lsbTimestamp)

	return restoredTimestamp

def getCorrectedLocalTimestamp(currentTimestamp):
	"""
	Get a timestamp in seconds from epoch, set to the local time.

	:param currentTimestamp:      Current time, obtained with time.time().
	:returns:                     Local unix timestamp.
	"""
	# This does not work, as mktime() ignores the daylight saving time:
	#     secondsFromGMT = round(time.time() - time.mktime(time.gmtime()))
	secondsFromGMT = time.localtime().tm_gmtoff
	correctedTimestamp = currentTimestamp + secondsFromGMT
	return correctedTimestamp