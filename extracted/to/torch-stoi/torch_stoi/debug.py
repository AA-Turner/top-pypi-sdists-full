from pulse_ai.metrics.pytorch_stoi import PytorchSTOI
import torchaudio

enhanced, sr = torchaudio.load("bugged_data/enhanced_9.wav")
reference, sr = torchaudio.load("bugged_data/reference_9.wav")
metric = PytorchSTOI(sample_rate=sr, use_vad=True, extended=True, do_resample=True)
print(metric(enhanced, reference))
