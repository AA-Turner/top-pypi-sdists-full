# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class GameInfo(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsGameInfo(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GameInfo()
        x.Init(buf, n + offset)
        return x

    # GameInfo
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GameInfo
    def SecondsElapsed(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # GameInfo
    def GameTimeRemaining(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # GameInfo
    def IsOvertime(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # GameInfo
    def IsUnlimitedTime(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

# /// True when cars are allowed to move, and during the pause menu. False during replays.
    # GameInfo
    def IsRoundActive(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

# /// True when the clock is paused due to kickoff, but false during kickoff countdown. In other words, it is true
# /// while cars can move during kickoff. Note that if both players sit still, game clock start and this will become false.
    # GameInfo
    def IsKickoffPause(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

# /// Turns true after final replay, the moment the 'winner' screen appears. Remains true during next match
# /// countdown. Turns false again the moment the 'choose team' screen appears.
    # GameInfo
    def IsMatchEnded(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # GameInfo
    def WorldGravityZ(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

# /// Game speed multiplier, 1.0 is regular game speed.
    # GameInfo
    def GameSpeed(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

# /// Tracks the number of physics frames the game has computed.
# /// May increase by more than one across consecutive packets.
# /// Data type will roll over after 207 days at 120Hz.
    # GameInfo
    def FrameNum(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def GameInfoStart(builder): builder.StartObject(10)
def GameInfoAddSecondsElapsed(builder, secondsElapsed): builder.PrependFloat32Slot(0, secondsElapsed, 0.0)
def GameInfoAddGameTimeRemaining(builder, gameTimeRemaining): builder.PrependFloat32Slot(1, gameTimeRemaining, 0.0)
def GameInfoAddIsOvertime(builder, isOvertime): builder.PrependBoolSlot(2, isOvertime, 0)
def GameInfoAddIsUnlimitedTime(builder, isUnlimitedTime): builder.PrependBoolSlot(3, isUnlimitedTime, 0)
def GameInfoAddIsRoundActive(builder, isRoundActive): builder.PrependBoolSlot(4, isRoundActive, 0)
def GameInfoAddIsKickoffPause(builder, isKickoffPause): builder.PrependBoolSlot(5, isKickoffPause, 0)
def GameInfoAddIsMatchEnded(builder, isMatchEnded): builder.PrependBoolSlot(6, isMatchEnded, 0)
def GameInfoAddWorldGravityZ(builder, worldGravityZ): builder.PrependFloat32Slot(7, worldGravityZ, 0.0)
def GameInfoAddGameSpeed(builder, gameSpeed): builder.PrependFloat32Slot(8, gameSpeed, 0.0)
def GameInfoAddFrameNum(builder, frameNum): builder.PrependInt32Slot(9, frameNum, 0)
def GameInfoEnd(builder): return builder.EndObject()
