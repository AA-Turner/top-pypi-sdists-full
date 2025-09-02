from typing import List

from crownstone_core.protocol.BluenetTypes import ResultValue


class MeshResult:

    def __init__(self, crownstone_uid_array : List[int]):
        self.success = False
        self.resultCode = ResultValue.UNSPECIFIED
        self.acks = {}
        self.initial_crownstone_uid_array = crownstone_uid_array
        for uid in crownstone_uid_array:
            self.acks[uid] = False

    def merge(self, result: 'MeshResult'):
        for uid, success in result.acks.items():
            self.acks[uid] = result.acks[uid]

    def get_successful_ids(self) -> List[int]:
        successList = []
        for uid, success in self.acks.items():
            if self.acks[uid]:
                successList.append(uid)
        return successList

    def compare_get_failed(self, otherResult: 'MeshResult') -> List[int]:
        failedList = []
        for uid, success in self.acks.items():
            if success and uid in otherResult.acks:
                if not otherResult.acks[uid]:
                    failedList.append(uid)
        return failedList

    def compare_get_success(self, otherResult: 'MeshResult') -> List[int]:
        successList = []
        for uid, success in self.acks.items():
            if success and uid in otherResult.acks:
                if otherResult.acks[uid]:
                    successList.append(uid)
        return successList

    def collect_ack(self, uid, result):
        if uid in self.acks:
            self.acks[uid] = result

    def wasSuccessful(self, crownstone_uid_array : List[int] = None):
        array_to_use = self.initial_crownstone_uid_array
        if crownstone_uid_array is not None:
            array_to_use = crownstone_uid_array
        for uid in array_to_use:
            if not self.acks[uid]:
                return False
        return True

    def conclude(self, crownstone_uid_array : List[int] = None):
        self.success = self.wasSuccessful(crownstone_uid_array)