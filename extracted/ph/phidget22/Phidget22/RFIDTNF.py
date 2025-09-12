import sys
import ctypes
class RFIDTNF:
	# Record is Empty
	TNF_EMPTY = 0
	# Record is well known type
	TNF_WELL_KNOWN = 1
	# Record contains a media type
	TNF_MIME_MEDIA = 2
	# Record is ABSOLUTE_URI
	TNF_ABSOLUTE_URI = 3
	# Record is EXTERNAL
	TNF_EXTERNAL = 4
	# Record is unknown, treat payload as binary
	TNF_UNKNOWN = 5
	# Used in chunked records, same type as previous chunk.
	TNF_UNCHANGED = 6

	@classmethod
	def getName(self, val):
		if val == self.TNF_EMPTY:
			return "TNF_EMPTY"
		if val == self.TNF_WELL_KNOWN:
			return "TNF_WELL_KNOWN"
		if val == self.TNF_MIME_MEDIA:
			return "TNF_MIME_MEDIA"
		if val == self.TNF_ABSOLUTE_URI:
			return "TNF_ABSOLUTE_URI"
		if val == self.TNF_EXTERNAL:
			return "TNF_EXTERNAL"
		if val == self.TNF_UNKNOWN:
			return "TNF_UNKNOWN"
		if val == self.TNF_UNCHANGED:
			return "TNF_UNCHANGED"
		return "<invalid enumeration value>"
