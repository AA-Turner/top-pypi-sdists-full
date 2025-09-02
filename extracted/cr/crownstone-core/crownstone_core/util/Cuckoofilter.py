from crownstone_core.packets.assetFilter.CuckooFilterPackets import CuckooFilterData
from crownstone_core.util.CRC import crc16ccitt, djb2_hash
from crownstone_core.util.Conversion import Conversion

from crownstone_core.util.Randomgenerator import RandomGenerator

# nice nonsensical value which will never be in uint16 range to mark an empty spot.
EMPTY = -1e8

class CuckooFilter:
    """
    Cuckoo filter implementation, currently supporting only 16 bit fingerprints.

    Byte arrays, 'keys', can be added to a cuckoo filter. They are stored as hashed, 'fingerprints',
    in an array. The array is organized in 'buckets' of fixed size. The fingerprint for a key is
    stored in one of two buckets, determined by a hash of the key. (The hash for fingerprints and
    the hash for buckets must be 'independent'.)

    Expected types for arguments and return values:
    - ByteArrayType = List[uint8]
    - FingerprintType = uint16
    - IndexType = uint8
    - FingerprintArrayType = List[FingerprintType]
    """
    max_kick_attempts = int(100)

    class ExtendedFingerprint:
        def __init__(self, fingerprint, bucketA, bucketB):
            self.fingerprint = fingerprint
            self.bucketA = bucketA
            self.bucketB = bucketB

        def __str__(self):
            return f"CuckooFilter.ExtendedFingerprint({self.fingerprint:#0{6}x},{self.bucketA:#0{4}x},{self.bucketB:#0{4}x})"

        def __eq__(self, other):
            """ Buckets are allowed to be reversed. Fingerprints must be equal. """
            return self.fingerprint == other.fingerprint and (
                   (self.bucketA == other.bucketA and self.bucketB == other.bucketB) or
                   (self.bucketB == other.bucketA and self.bucketA == other.bucketB)
            )

    def getExtendedFingerprint(self, key):
        """
        key: ByteArrayType
        returns ExtendedFingerprint
        """
        fingerprint = self.hash_to_fingerprint(key)
        buckethash = self.hash_to_bucket(key)

        return CuckooFilter.ExtendedFingerprint(
            fingerprint,
            buckethash % self.bucketCount(),
            (buckethash ^ fingerprint) % self.bucketCount())

    def getExtendedFingerprintFromFingerprintAndBucket(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        bucket_index: IndexType
        returns: ExtendedFingerprint
        """
        bucket_a = (bucket_index % self.bucketCount()) & 0xff
        bucket_b =((bucket_index ^ fingerprint) % self.bucketCount()) & 0xff
        return CuckooFilter.ExtendedFingerprint (fingerprint, bucket_a, bucket_b)

    # -------------------------------------------------------------
    # Run time variables
    # -------------------------------------------------------------

    def __init__(self, bucketCountLog2, nests_per_bucket):
        """
        bucketCountLog2: IndexType. Number of buckets allocated is 2**bucketCountLog2.
        nests_per_bucket: IndexType
        returns: n/a
        """
        self.bucketCountLog2 = int(bucketCountLog2)
        self.nests_per_bucket = int(nests_per_bucket)
        self.victim = CuckooFilter.ExtendedFingerprint(0,0,0)
        self.bucket_array = []

        self.clear()

    # -------------------------------------------------------------
    # ----- Private methods -----
    # -------------------------------------------------------------

    def getData(self) -> CuckooFilterData:
        data = CuckooFilterData()
        data.bucketCountLog2 = self.bucketCountLog2
        data.nestsPerBucket = self.nests_per_bucket
        data.victim.fingerprint = self.victim.fingerprint
        data.victim.bucketA = self.victim.bucketA
        data.victim.bucketB = self.victim.bucketB
        data.bucketArray = self._cleanBucketArray(0)
        return data

    def serialize(self):
        return self.getData().serialize()

    def filterhash(self):
        """
        Flatten the filter settings and the uint16 array of fingerprints
        to a uint8 array in little endian and return a crc16 of the result.

        Must match firmware.

        returns: FingerprintType
        """
        return crc16ccitt(self.serialize())

    def hash_to_fingerprint(self, key):
        """
        key: ByteArrayType
        returns: FingerprintType
        """
        return crc16ccitt(key)

    def hash_to_bucket(self, key):
        """
        key: ByteArrayType
        returns: FingerprintType
        """
        return djb2_hash(key)

    def lookup_fingerprint(self, bucket_number, finger_index):
        """
        bucket_number: IndexType
        finger_index: IndexType
        returns: FingerprintType
        """
        return self.bucket_array[self.lookup_fingerprint_index(bucket_number, finger_index)]

    def lookup_fingerprint_index(self, bucket_number, finger_index):
        """
        bucket_number: IndexType
        finger_index: IndexType
        returns: int
        """
        return (bucket_number * self.nests_per_bucket) + finger_index

    def add_fingerprint_to_bucket (self, fingerprint, bucket_number):
        """
        fignerprint: FingerprintType
        bucket_number: IndexType
        returns: bool
        """
        for ii in range(self.nests_per_bucket):
            fingerprint_index = self.lookup_fingerprint_index(bucket_number, ii)
            if self.bucket_array[fingerprint_index] == EMPTY:
                self.bucket_array[fingerprint_index] = fingerprint
                return True
        return False

    def remove_fingerprint_from_bucket (self, fingerprint, bucket_number):
        """
        fignerprint: FingerprintType
        bucket_number: IndexType
        returns: bool
        """
        for ii in range(self.nests_per_bucket):
            candidate = self.lookup_fingerprint_index(bucket_number, ii) # candidate_fingerprint_for_removal_in_array_index

            if self.bucket_array[candidate] == fingerprint:
                self.bucket_array[candidate] = EMPTY
                # to keep the bucket front loaded, move the last non-zero
                # fingerprint behind ii into the slot.
                for jj in reversed(range(ii + 1, self.nests_per_bucket)):
                    last = self.lookup_fingerprint_index(bucket_number, jj) # last_fingerprint_in_bucket

                    if self.bucket_array[last] != EMPTY:
                        self.bucket_array[candidate] = self.bucket_array[last]
                        self.bucket_array[last] = EMPTY
                        break
                return True
        return False

    # -------------------------------------------------------------
    def moveExtendedFingerprint(self, entry_to_insert):
        """
        entry_to_insert: ExtendedFingerprint
        returns: bool
        """
        # seeding with a hash for this filter guarantees exact same sequence of
        # random integers used for moving fingerprints in the filter on every crownstone.
        seed = self.filterhash()
        rand = RandomGenerator(seed)

        for attempts_left in range(CuckooFilter.max_kick_attempts):
            # try to add to bucket A
            if self.add_fingerprint_to_bucket(entry_to_insert.fingerprint, entry_to_insert.bucketA):
                return True

            # try to add to bucket B
            if self.add_fingerprint_to_bucket(entry_to_insert.fingerprint, entry_to_insert.bucketB):
                return True

            # no success, time to kick a fingerprint from one of our buckets

            # determine which bucket to kick from
            kick_A = rand() % 2
            kicked_item_bucket =  entry_to_insert.bucketA if kick_A else entry_to_insert.bucketB

            # and which fingerprint index
            kicked_item_index = rand() % self.nests_per_bucket

            # swap entry to insert and the randomly chosen ('kicked') item
            kicked_item_fingerprint_index = self.lookup_fingerprint_index(kicked_item_bucket, kicked_item_index)
            kicked_item_fingerprint_value = self.bucket_array[kicked_item_fingerprint_index]

            self.bucket_array[kicked_item_fingerprint_index] = entry_to_insert.fingerprint

            entry_to_insert = self.getExtendedFingerprintFromFingerprintAndBucket(
                kicked_item_fingerprint_value, kicked_item_bucket)

            # next iteration will try to re-insert the footprint previously at (h,i).

        # iteration ended: failed to re-place the last kicked entry into the buffer after max attempts.
        self.victim = entry_to_insert

        return False

    def addExtendedFingerprint(self, extended_finger):
        """
        extended_finger: ExtendedFingerprint
        returns: bool
        """
        if self.containsExtendedFingerprint(extended_finger):
            return True

        if self.victim.fingerprint != 0: # already full.
            return False

        return self.moveExtendedFingerprint(extended_finger)

    def removeExtendedFingerprint(self, extended_finger):
        """
        extended_finger: ExtendedFingerprint
        returns: bool
        """
        if self.remove_fingerprint_from_bucket(extended_finger.fingerprint, extended_finger.bucketA) or \
                self.remove_fingerprint_from_bucket(extended_finger.fingerprint, extended_finger.bucketB):
            # short ciruits nicely:
            #    tries bucketA,
            #    on fail try B,
            #    if either succes, fix victim.
            if self.victim.fingerprint !=  0:
                if self.addExtendedFingerprint(self.victim):
                    self.victim = CuckooFilter.ExtendedFingerprint(0,0,0)
            return True
        return False

    def containsExtendedFingerprint(self, extended_finger):
        """
        extended_finger: ExtendedFingerprint
        returns: bool
        """
        # (loops are split to improve cache hit rate)
        # search bucketA
        for ii in range(self.nests_per_bucket):
            if extended_finger.fingerprint == self.lookup_fingerprint(extended_finger.bucketA, ii):
                return True
        # search bucketB
        for ii in range(self.nests_per_bucket):
            if extended_finger.fingerprint == self.lookup_fingerprint(extended_finger.bucketB, ii):
                return True

        return False

    # -------------------------------------------------------------

    def addFingerprintType(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        returns: bool
        """
        return self.addExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fingerprint, bucket_index))


    def removeFingerprintType(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        bucket_index: Indextype
        returns: bool
        """
        return self.removeExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fingerprint, bucket_index))


    def containsFingerprintType(self, fingerprint, bucket_index):
        """
        fingerprint: FingerprintType
        bucket_index: IndexType
        returns: bool
        """
        return self.containsExtendedFingerprint(
            self.getExtendedFingerprintFromFingerprintAndBucket(fingerprint, bucket_index))

    # -------------------------------------------------------------

    def add(self, key):
        """
        key: ByteArrayType
        returns: bool
        """
        return self.addExtendedFingerprint(self.getExtendedFingerprint(key))

    def remove(self, key):
        """
        key: ByteArrayType
        returns: bool
        """
        return self.removeExtendedFingerprint(self.getExtendedFingerprint(key))

    def contains(self, key):
        """
        key: ByteArrayType
        returns: bool
        """
        return self.containsExtendedFingerprint(self.getExtendedFingerprint(key))


    # -------------------------------------------------------------
    # Init/deinit like stuff.
    # -------------------------------------------------------------

    def clear(self):
        """
        returns: None
        """
        self.victim = CuckooFilter.ExtendedFingerprint(0,0,0)
        self.bucket_array = [EMPTY] * CuckooFilter.getfingerprintcount(self.bucketCount(), self.nests_per_bucket)

    # -------------------------------------------------------------
    # Size stuff.
    # -------------------------------------------------------------

    @staticmethod
    def sizeof(typ):
        size_dict = {
            'uint8': 1,
            'uint16': 2,
            'uint32': 4,
            'uint64': 8,
            'CuckooFilter': 1 + 1 + 2 + 1 + 1,
            'FingerprintType': 2,
            'IndexType': 1
        }
        if typ in size_dict:
            return size_dict[typ]
        return -1

    @staticmethod
    def getfingerprintcount(bucket_count, nests_per_bucket):
        """
        bucket_count: IndexType
        nests_per_bucket: IndexType
        returns: int
        """
        return bucket_count * nests_per_bucket

    @staticmethod
    def getbuffersize(bucket_count, nests_per_bucket):
        """
        bucket_count: IndexType
        nests_per_bucket: IndexType
        returns: int
        """
        return CuckooFilter.getfingerprintcount(bucket_count, nests_per_bucket) * CuckooFilter.sizeof('FingerprintType')

    @staticmethod
    def getsize(bucket_count, nests_per_bucket):
        """
        bucket_count: IndexType
        nests_per_bucket: IndexType
        returns: int
        """
        return CuckooFilter.sizeof('CuckooFilter') + CuckooFilter.getbuffersize(bucket_count, nests_per_bucket)

    def fingerprintcount(self):
        """
        returns: int
        """
        return CuckooFilter.getfingerprintcount(self.bucketCount(), self.nests_per_bucket)

    def bucketCount(self):
        return 1 << self.bucketCountLog2

    def buffersize(self):
        """
        returns: int
        """
        return CuckooFilter.getbuffersize(self.bucketCount(), self.nests_per_bucket)

    def size(self):
        """
        returns: int
        """
        return CuckooFilter.getsize(self.bucketCount(), self.nests_per_bucket)


    def saturate(self):
        self.bucket_array = self._cleanBucketArray(self.bucket_array[0])

    def _cleanBucketArray(self, replaceValue = 0):
        actual_bucket_array = []
        for item in self.bucket_array:
            if item == EMPTY:
                actual_bucket_array.append(replaceValue)
            else:
                actual_bucket_array.append(item)
        return actual_bucket_array
