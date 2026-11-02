import os

from praatio import textgrid
from praatio.utilities import utils


def getSyllableNuclei(
    praatEXE,
    scriptFN,
    wavFN,
    outputTextGridFN=None,
    silenceThreshold=-25,
    minDipBetweenPeaks=2,
    minPauseDuration=0.3,
):
    """
    This will launch praat as an separate process.  Python will wait until execution finishes
    and then continue.  We can't capture the output, so we the praat script should dump a file
    that python can read.
    """
    if outputTextGridFN is None:
        root = os.path.split(wavFN)[0]
        outputTextGridFN = os.path.join(root, "temp.TextGrid")

    utils.runPraatScript(
        praatEXE,
        scriptFN,
        [
            silenceThreshold,
            minDipBetweenPeaks,
            minPauseDuration,
            wavFN,
            outputTextGridFN,
        ],
    )

    return calculateIntervalsBetweenSyllableNuclei(outputTextGridFN)


def _iterateSpeechSegments(textgridFn):
    speechTierName = "silences"
    pulseTierName = "syllables"

    tg = textgrid.openTextgrid(textgridFn, False)
    tier = tg.getTier(speechTierName)
    speechSegments = [entry for entry in tier.entries if entry.label == "sounding"]

    nucleiTier = tg.getTier(pulseTierName)
    for start, end, _ in speechSegments:
        croppedTier = nucleiTier.crop(start, end, None, False)
        yield start, end, croppedTier.entries


def calculateSpeechRateFromTextgrid(textgridFn):
    numPulses = 0
    duration = 0
    for start, end, nuclei in _iterateSpeechSegments(textgridFn):
        numPulses += len(nuclei)
        duration += end - start

    return numPulses / float(duration)


def calculateIntervalsBetweenSyllableNuclei(textgridFn):
    intervalDurations = []
    for _, _, nuclei in _iterateSpeechSegments(textgridFn):
        intervalDurations.extend(
            [nuclei[i + 1][0] - nuclei[i][0] for i in range(len(nuclei) - 1)]
        )

    return intervalDurations


if __name__ == "__main__":
    # praatEXE = r"C:\Praat.exe"
    praatEXE = "/Applications/Praat.app/Contents/MacOS/Praat"
    scriptFN = "/Users/tmahrt/Downloads/syllable_nuclei_praatio.praat"
    wavFN = "/Users/tmahrt/Downloads/mary.wav"
    # wavFN = "/Users/tmahrt/Dropbox/workspace/pyAcoustics/examples/files/introduction.wav"

    durationBetweenSyllableNuclei = getSyllableNuclei(praatEXE, scriptFN, wavFN)
    print(durationBetweenSyllableNuclei)
