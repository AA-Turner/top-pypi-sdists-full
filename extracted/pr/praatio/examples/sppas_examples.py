import os
from os.path import join

from praatio import textgrid

# utputPath = "f'{cwd}\\{SPPAS_DIR_NAME}\\{SPPAS_OUTPUT_FOLDER_NAME}"
inputPath = "/Users/tmahrt/Downloads/files"
outputPath = join(inputPath, "output_files")
if not os.path.exists(outputPath):
    os.mkdir(outputPath)
basename = "家传秘方_Recording_10"

phon_tier_list = []
token_tier_list = []
name_list = [basename + "_seg_" + str(i) for i in range(1, 7)]

for i, name in enumerate(name_list):
    tg_dict = textgrid.openTextgrid(
        join(inputPath, name + "-palign.TextGrid"), includeEmptyIntervals=False
    ).tierDict
    tg_dict_tokens = textgrid.openTextgrid(
        join(inputPath, name + "-token.TextGrid"), includeEmptyIntervals=True
    ).tierDict

    if i == 0:
        phon_base_tier = tg_dict["PhonAlign"]
        token_base_tier = tg_dict_tokens["Tokens"]
    else:
        phon_base_tier = phon_base_tier.appendTier(tg_dict["PhonAlign"])
        token_base_tier = token_base_tier.appendTier(tg_dict_tokens["Tokens"])

    final_tg = textgrid.Textgrid()
    final_tg.addTier(phon_base_tier)
    final_tg.addTier(token_base_tier)

    print("-----------")
    print(final_tg.maxTimestamp)
    targetTier = final_tg.getTier(phon_base_tier.name)
    print([targetTier.maxTimestamp, targetTier.entries[-2], targetTier.entries[-1]])
    targetTier = final_tg.getTier(token_base_tier.name)
    print([targetTier.maxTimestamp, targetTier.entries[-2], targetTier.entries[-1]])

    final_tg.save(
        join(outputPath, basename + str(i) + "-palign.TextGrid"), "short_textgrid", True
    )
