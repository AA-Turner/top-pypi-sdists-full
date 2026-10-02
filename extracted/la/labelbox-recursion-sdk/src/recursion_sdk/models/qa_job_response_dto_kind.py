from enum import StrEnum

class QaJobResponseDtoKind(StrEnum):
    AGGREGATE = "aggregate"
    INDIVIDUAL = "individual"

    def __str__(self) -> str:
        return str(self.value)
