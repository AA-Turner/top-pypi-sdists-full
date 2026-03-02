import pandas as pd
from pydub import AudioSegment
import soundfile as sf
import pyloudnorm as pyln
from warpq.core import warpqMetric
from warpq.utils import load_audio, plot_warpq_scores, group_dataframe_by_columns
import numpy as np

df = pd.read_csv("results_with_details_new.csv")

exp1 = False
if exp1:

    def compute_dbfs(file_path):
        try:
            audio = AudioSegment.from_file(file_path)
            normalized_sound = audio.apply_gain(-audio.max_dBFS)
            # return audio.dBFS
            return audio.max_dBFS
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None  # Return None if there's an error

    # Compute dBFS for reference audio files and add to a new column
    df["ref_dBFS"] = df["ref_wave"].apply(compute_dbfs)

    # Compute dBFS for degraded audio files and add to a new column
    df["deg_dBFS"] = df["deg_wave"].apply(compute_dbfs)

    dd = plot_warpq_scores(
        df=df,
        mos_col="ref_dBFS",
        warpq_col="deg_dBFS",
        hue_col="db",
        style_col="db",
        title="MOS vs WARP-Q",
        # save_path="plots/Genspeech1",
    )

    dd = plot_warpq_scores(
        df=df,
        mos_col="Raw WARP-Q Score",
        warpq_col="deg_dBFS",
        hue_col="db",
        style_col="db",
        title="MOS vs WARP-Q",
        # save_path="plots/Genspeech1",
    )

exp2 = False
if exp2:

    def compute_dbfs(file_path):
        try:
            data, rate = sf.read(file_path)  # load audio (with shape (samples, channels))
            meter = pyln.Meter(rate)  # create BS.1770 meter
            loudness_org = meter.integrated_loudness(data)
            # loudness normalize audio to -12 dB LUFS
            loudness_normalized_audio = pyln.normalize.loudness(data, loudness_org, -25.0)
            loudness_new = meter.integrated_loudness(loudness_normalized_audio)
            # return audio.dBFS
            return loudness_org, loudness_new
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None  # Return None if there's an error

    # Apply the function to the DataFrame and store the results in two new columns
    df[["ref_dBFS_org", "ref_dBFS_new"]] = df["ref_wave"].apply(compute_dbfs).apply(pd.Series)

    # Compute dBFS for degraded audio files and add to a new column
    df[["deg_dBFS_org", "deg_dBFS_new"]] = df["deg_wave"].apply(compute_dbfs).apply(pd.Series)

    dd = plot_warpq_scores(
        df=df,
        mos_col="ref_dBFS_org",
        warpq_col="deg_dBFS_new",
        hue_col="db",
        style_col="db",
        title="MOS vs WARP-Q",
        # save_path="plots/Genspeech1",
    )

exp3 = True
if exp3:
    model = warpqMetric()

    def compute_dbfs(model, file_path1, file_path2):
        data1, data2, rate1, rate2 = load_audio(ref_path=file_path1, deg_path=file_path2, sr=16000, native_sr=False, verbose=False)

        # Process file_path1
        meter1 = pyln.Meter(rate1)
        loudness_org1 = meter1.integrated_loudness(data1)
        loudness_normalized_audio1 = pyln.normalize.loudness(data1, loudness_org1, -28.0)
        loudness_new1 = meter1.integrated_loudness(loudness_normalized_audio1)

        # Process file_path2
        meter2 = pyln.Meter(rate2)
        loudness_org2 = meter2.integrated_loudness(data2)
        # loudness_normalized_audio2 = pyln.normalize.loudness(data2, loudness_org2, -28.0)
        loudness_normalized_audio2 = pyln.normalize.loudness(data2, loudness_org2, loudness_org1)
        loudness_new2 = meter2.integrated_loudness(loudness_normalized_audio2)

        results = model.evaluate(np.clip(loudness_normalized_audio1, -1, 1), np.clip(loudness_normalized_audio2, -1, 1), arr_sr=rate1, verbose=False)

        # Return results for both files
        return (loudness_org1, loudness_new1), (loudness_org2, loudness_new2), (results["raw_warpq_score"], results["normalized_warpq_score"])

    # Initialize empty lists to store the results
    file1_dBFS_org = []
    file1_dBFS_new = []
    file2_dBFS_org = []
    file2_dBFS_new = []
    warpq_raw_dBFS_25 = []
    warpq_norm_dBFS_25 = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Call the function on the two columns of the current row
        (loudness1_org, loudness1_new), (loudness2_org, loudness2_new), (raw_warpq_score, normalized_warpq_score) = compute_dbfs(
            model, row["ref_wave"], row["deg_wave"]
        )

        # Append the results to the lists
        file1_dBFS_org.append(loudness1_org)
        file1_dBFS_new.append(loudness1_new)
        file2_dBFS_org.append(loudness2_org)
        file2_dBFS_new.append(loudness2_new)
        warpq_raw_dBFS_25.append(raw_warpq_score)
        warpq_norm_dBFS_25.append(normalized_warpq_score)

    # Assign the results back to the DataFrame
    df["ref_dBFS_org"] = file1_dBFS_org
    df["ref_dBFS_new"] = file1_dBFS_new
    df["deg_dBFS_org"] = file2_dBFS_org
    df["deg_dBFS_new"] = file2_dBFS_new
    df["warpq_raw_dBFS_25"] = warpq_raw_dBFS_25
    df["warpq_norm_dBFS_25"] = warpq_norm_dBFS_25

    dd = plot_warpq_scores(
        df=df,
        mos_col="mos",
        warpq_col="Raw WARP-Q Score",
        hue_col="db",
        style_col="db",
        title="MOS vs WARP-Q",
        # save_path="plots/Genspeech1",
    )
