
class ActiveDays:

    def __init__(self):
        self.Monday = True
        self.Tuesday = True
        self.Wednesday = True
        self.Thursday = True
        self.Friday = True
        self.Saturday = True
        self.Sunday = True

    def fromData(self, data):
        self.Sunday = (data >> 0) & 0x01 == 1
        self.Monday = (data >> 1) & 0x01 == 1
        self.Tuesday = (data >> 2) & 0x01 == 1
        self.Wednesday = (data >> 3) & 0x01 == 1
        self.Thursday = (data >> 4) & 0x01 == 1
        self.Friday = (data >> 5) & 0x01 == 1
        self.Saturday = (data >> 6) & 0x01 == 1
        return self

    def getMask(self):
        mask = 0

        # bits:
        MondayBit = 0
        TuesdayBit = 0
        WednesdayBit = 0
        ThursdayBit = 0
        FridayBit = 0
        SaturdayBit = 0
        SundayBit = 0
        if self.Sunday:  MondayBit = 1
        if self.Monday:  TuesdayBit = 1
        if self.Tuesday:  WednesdayBit = 1
        if self.Wednesday:  ThursdayBit = 1
        if self.Thursday:  FridayBit = 1
        if self.Friday:  SaturdayBit = 1
        if self.Saturday:  SundayBit = 1

        # configure mask
        mask = mask | SundayBit << 0
        mask = mask | MondayBit << 1
        mask = mask | TuesdayBit << 2
        mask = mask | WednesdayBit << 3
        mask = mask | ThursdayBit << 4
        mask = mask | FridayBit << 5
        mask = mask | SaturdayBit << 6

        return mask

    def getDictionary(self):
        returnDict = {
            "Sun": self.Sunday,
            "Mon": self.Monday,
            "Tue": self.Tuesday,
            "Wed": self.Wednesday,
            "Thu": self.Thursday,
            "Fri": self.Friday,
            "Sat": self.Saturday,
        }

        return returnDict
