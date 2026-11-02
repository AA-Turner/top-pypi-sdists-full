import wave
from praatio import audio


def testWithWave(wavFN):
    with open(wavFN, "rb") as fd:
        wavObj = wave.open(fd, mode="rb")
        waveParams = wavObj.getparams()

        waveData = wavObj.readframes(waveParams.nframes)

        wav = audio.Wav(waveData, waveParams)
        print(wav.findNearestZeroCrossing(10))


def testWithQueryWav(wavFN):
    wav = audio.QueryWav(wavFN)
    print(wav.findNearestZeroCrossing(10))


tmpFN = "/Users/tmahrt/Downloads/mono-KK-Otjiwarongo-20220806-2a-C.wav"
tmpFN = "/Users/tmahrt/Downloads/bobby.wav"

testWithWave(tmpFN)
testWithQueryWav(tmpFN)
