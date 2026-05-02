import board
import displayio
import audiobusio, audiocore, audiomp3
import array, math

# To show return tooltips for functions
class Any:pass
class pin_number:pass
class audiobusio__i2s:pass
class audiocore__rawsample:pass
class audiocore__wavefile:pass
class circuitpython_typing__AudioSample:pass

# Reset all pins to allow new connections
displayio.release_displays()

class Audio:
    def __init__(self,
                 bit_clock_pin: pin_number = board.GP10,
                 word_select_pin: pin_number = board.GP11,
                 data_pin: pin_number = board.GP9) -> None:
        # Store inputs for future use if needed
        self.bit_clock_pin = bit_clock_pin
        self.word_select_pin = word_select_pin
        self.data_pin = data_pin

        # Create audio device
        self.i2s = self.createI2S(bit_clock_pin, word_select_pin, data_pin)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.i2s

    def createI2S(self,
                  bit_clock_pin: pin_number,
                  word_select_pin: pin_number,
                  data_pin: pin_number) -> audiobusio__i2s:
        i2s = audiobusio.I2SOut(bit_clock_pin, word_select_pin, data_pin)
        return i2s

    # Directly opens and plays a .wav file without extra lines
    def playWaveFile(self,
                     wave_filename: str,
                     loop: bool = False) -> None:
        self.playAudio(self.i2s, openWaveFile(wave_filename), loop)

    # Directly opens and plays an .mp3 file without extra lines
    # NOTE: https://docs.circuitpython.org/en/latest/shared-bindings/audiomp3/index.html#:~:text=Playback%20of%20mp3,explicitly%20call%20refresh.
    def playMP3File(self,
                    mp3_filename: str,
                    loop: bool = False) -> None:
        self.playAudio(self.i2s, openWaveFile(mp3_filename), loop)

    # Plays audio returned from createAudioSample or openWaveFile
    def playAudio(self,
                  audio: circuitpython_typing__AudioSample,
                  loop: bool = False) -> None:
        self.i2s.play(audio, loop=loop)

    # Checks if sound is being played
    def isPlaying(self) -> bool:
        if self.i2s.playing:
            return True
        return False

    # Stop all audio from playing on the inputted audio bus
    def stopAudio(self) -> None:
        self.i2s.stop()

    # Pauses the current audio from being played on the inputted audio bus
    def pauseAudio(self) -> None:
        self.i2s.pause()

    # Resumes the current audio on the inputted audio bus if it was paused
    def resumeAudio(self) -> None:
        self.i2s.resume()


# Creates an audio sample from an input buffer and can be used with the playAudio function
def createAudioSample(audio_buffer: "list[int]",
                      sample_rate: int = 8000) -> circuitpython_typing__AudioSample:
    audio_sample = audiocore.RawSample(audio_buffer, sample_rate=sample_rate)

    return audio_sample

# Opens 8-bit unsigned or 16-bit signed .wav files as Samples
# Use openMP3File for an easier experience, but this is less intensive to play
def openWaveFile(wave_filename: str) -> circuitpython_typing__AudioSample:
    wave_file = audiocore.WaveFile(wave_filename)

    return wave_file

# Opens .mp3 files and stores them as Samples
# NOTE: https://docs.circuitpython.org/en/latest/shared-bindings/audiomp3/index.html#:~:text=Playback%20of%20mp3,explicitly%20call%20refresh.
def openMP3File(mp3_filename: str) -> circuitpython_typing__AudioSample:
    wave_file = audiomp3.MP3Decoder(mp3_filename)
    return wave_file

# Generate one period of sine wave.
def createSineWave() -> "list[int]":
    length = 8000 // 440
    sine_wave = array.array("H", [0] * length)

    amplitude = 2 ** 15
    x_offset = 2 ** 15

    for i in range(length):
        sine_wave[i] = int(amplitude * math.sin(math.pi * 2 * i / length) + x_offset)

    return sine_wave
