#!/usr/bin/python
#####################################################################################
# rust_predict_profiles, Correlation between observed and predicted profiles from CDS start + 120 to CDS stop - 60
# Copyright (C) 2015 Patrick O'Connor

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#####################################################################################

import os, pysam, sys, numpy, argparse, re
from RUST.methods import *


def rank(lsit1):
    lsit2 = []
    lsit1s = lsit1[:]
    lsit1s.sort()
    dict_ranks = {}
    for value_i, value in enumerate(lsit1s):
        dict_ranks.setdefault(value, []).append(value_i)

    for value in lsit1:
        lsit2.append(mean_value(dict_ranks[value]))
    return lsit2


def main(args):

    RUST_file = open(args.rustfile)  # file output of RUST_script.py
    RUST_file.readline()
    codon_rust_dict = {}
    for line in RUST_file:
        linesplit = line.split(",")
        if len(linesplit) == 1:
            break
        codon = linesplit[0]
        if len(codon) != 3 or len(set(codon) - set(["A", "T", "G", "C"])) != 0:
            stop_err("Codon metafootprint file not correct, check input file")
        codon_rust_dict[codon] = {}
        rust_values = list(map(float, linesplit[1:]))
        expected = rust_values[0]
        rust_metafootprint = [ro_value / expected for ro_value in rust_values[1:]]
        for n in range(34, 46):
            codon_rust_dict[codon][n - 40] = rust_metafootprint[
                n
            ]  # for 12 codons positions near A-site
    RUST_file.close()

    mRNA_sequences = args.transcriptome  # path to fastq file of transcripts
    in_seq_handle = open(mRNA_sequences)
    cds_start_dict = {}
    cds_end_dict = {}
    seq_dict = {}
    for line in in_seq_handle:
        if line[0] != ">":
            seq_dict.setdefault(transcript, "")
            seq_dict[transcript] += line[:-1]
            continue
        try:
            transcript_split = line[:-1].split("\t")
            transcript = transcript_split[0][1:]
            cds_start_dict[transcript] = int(transcript_split[1])
            cds_end_dict[transcript] = int(transcript_split[2])
        except:
            pass
    in_seq_handle.close()

    offset = args.offset
    readlen_range = args.lengths
    readlen_rangesplit = readlen_range.split(":")
    if len(readlen_rangesplit) == 1:
        accepted_read_lengths = [int(readlen_rangesplit[0])]
        length_values = "%s" % int(readlen_rangesplit[0])
    elif len(readlen_rangesplit) == 2:
        accepted_read_lengths = [
            readlen
            for readlen in range(
                int(readlen_rangesplit[0]), int(readlen_rangesplit[1]) + 1
            )
        ]
        length_values = "%s_%s" % (
            int(readlen_rangesplit[0]),
            int(readlen_rangesplit[1]),
        )
    else:
        stop_err(
            "Lengths of footprints parameter not in correct format, it should be either colon seperated with the second value greater or equal to the first, (28:32) or a single interger (31)"
        )
    if len(accepted_read_lengths) == 0:
        stop_err(
            "Lengths of footprints parameter not in correct format, it should be either colon seperated with the second value greater or equal to the first, (28:32) or a single interger (31)"
        )

    amino_acids = [
        "A",
        "C",
        "E",
        "D",
        "G",
        "F",
        "I",
        "H",
        "K",
        "M",
        "L",
        "N",
        "Q",
        "P",
        "S",
        "R",
        "T",
        "W",
        "V",
        "Y",
    ]
    aligments_A1 = pysam.Samfile(args.alignment, "rb")

    if not os.path.exists(args.Path):
        os.mkdir(args.Path)
    if args.profiles:
        if not os.path.exists("%s/rust_profile_predictions" % args.Path):
            os.mkdir("%s/rust_profile_predictions" % args.Path)

    if "/" in args.rustfile:
        rustfile_split = args.rustfile.split("/")[-1]
    # elif "\\" in args.rustfile:
    # rustfile_split= args.rustfile.split("\\")[-1]
    else:
        rustfile_split = args.rustfile

    if "RUST_codon_file_" in rustfile_split:
        alignment_filename = rustfile_split[16:]
    else:
        alignment_filename = rustfile_split

    correlations_file = open(
        "%s/predict_profiles_%s_%s_%s"
        % (args.Path, alignment_filename, args.offset, length_values),
        "w",
    )
    correlations_file.write(
        "transcript,average read density,Spearman's coefficient,Pearson's coefficient\n"
    )

    list_transcripts = seq_dict.keys()
    number_transcripts = 0
    list_10_percentile = []
    for value in range(1, 10):
        list_10_percentile.append((len(list_transcripts) * value) / 10)
    for transcript in list_transcripts:
        number_transcripts += 1
        if number_transcripts in list_10_percentile:
            sys.stdout.write(
                "%s percent\n"
                % ((list_10_percentile.index(number_transcripts) + 1) * 10)
            )

        try:
            cds_start = cds_start_dict[transcript]
            cds_end = cds_end_dict[transcript]
            if cds_end < cds_start:
                raise Exception
        except Exception:
            transcript_seq = seq_dict[transcript]
            cds_start = -1
            start_post = []
            end_post = []
            for match in re.finditer(r"(?=(%s))" % re.escape("ATG"), transcript_seq):
                start_post.append(match.start())
            for match in re.finditer(r"(?=(%s))" % re.escape("TAG"), transcript_seq):
                end_post.append(match.start())
            for match in re.finditer(r"(?=(%s))" % re.escape("TAA"), transcript_seq):
                end_post.append(match.start())
            for match in re.finditer(r"(?=(%s))" % re.escape("TGA"), transcript_seq):
                end_post.append(match.start())

            end_post.sort()
            len_max_orf = 0
            for value in start_post:
                for value2 in end_post:
                    if value < value2:
                        if value % 3 == value2 % 3:
                            len_orf = value2 - value
                            if len_orf > len_max_orf:
                                cds_start = value
                                cds_end = value2 + 3
                                len_max_orf = len_orf
                            break
            if cds_start == -1:
                # sys.stdout.write( '%s, AUG codon not found\n'%transcript  )
                continue

        elongation_region_all = seq_dict[transcript][cds_start:cds_end]

        if (
            len(elongation_region_all) % 3 != 0
        ):  # genes with codon region not divisible by 3 skipped
            # sys.stdout.write( '%s, CDS not divisible by 3\n'%transcript  )
            continue

        profile_expect = []
        for n in range(
            0, len(elongation_region_all[120:-60]), 3
        ):  # predicts profile from 120 nts after start to 60 before stop
            minus6_plus5_footprint = elongation_region_all[
                120 + n - 18 : 120 + n + 19
            ]  # contains sequence of region used to predict profile
            value = 1.0
            amino_loc = -6
            for number in range(0, len(minus6_plus5_footprint) - 2, 3):
                codon = minus6_plus5_footprint[number : number + 3]
                if len(set(codon) - set(["A", "T", "G", "C"])) != 0 or codon in [
                    "TAG",
                    "TGA",
                    "TAA",
                ]:
                    amino_loc += 1
                    continue
                value = value * codon_rust_dict[codon][amino_loc]
                amino_loc += 1
            profile_expect.append(value)
        profile_expect_sum = sum(profile_expect)
        profile_expect_probablility = [
            float(value) / profile_expect_sum for value in profile_expect
        ]

        profile_list = [
            0.0 for n in range(cds_start + 120, cds_end - 60)
        ]  # records ribo-seq profile
        if len(profile_list) < 50:
            # sys.stdout.write( '%s, ORF too short\n'%transcript  )
            continue
        all_reads = aligments_A1.fetch(transcript)

        len_elongation_region = len(profile_list)
        for read in all_reads:
            readlen = read.qlen
            if readlen not in accepted_read_lengths:
                continue  # selection of read of acceptable length
            A_site = read.pos + offset - cds_start - 120  # addition of offset
            if len_elongation_region > A_site > -1:
                profile_list[A_site] += 1

        average_gene_density = float(sum(profile_list)) / len(
            profile_list
        )  # average gene density calculated
        if average_gene_density > 0:
            profiles_control_codon = [
                profile_list[codon_ind]
                + profile_list[codon_ind + 1]
                + profile_list[codon_ind + 2]
                for codon_ind in range(0, len(profile_list), 3)
            ]
            spearmanr_value = numpy.corrcoef(
                rank(profiles_control_codon), rank(profile_expect)
            )[0, 1]
            pearsonr_value = numpy.corrcoef(profiles_control_codon, profile_expect)[
                0, 1
            ]
            correlations_file.write(
                "%s,%s,%s,%s\n"
                % (transcript, average_gene_density, spearmanr_value, pearsonr_value)
            )
            if args.profiles:
                open_file = open(
                    "%s/rust_profile_predictions/observed_predicted_%s_%s_%s_%s.csv"
                    % (
                        args.Path,
                        transcript,
                        alignment_filename,
                        args.offset,
                        length_values,
                    ),
                    "w",
                )
                profile_expect_probablility_index = 0
                open_file.write("%s\n" % transcript)
                open_file.write("codon, predicted probability, alignments\n")
                for coordinate_index in range(
                    0, len(elongation_region_all[120:-60]), 3
                ):
                    codon = elongation_region_all[
                        120 + coordinate_index : 120 + coordinate_index + 3
                    ]
                    open_file.write("%s, " % (codon))
                    open_file.write(
                        "%s, "
                        % (
                            profile_expect_probablility[
                                profile_expect_probablility_index
                            ]
                        )
                    )
                    open_file.write(
                        "%s\n"
                        % (profiles_control_codon[profile_expect_probablility_index])
                    )
                    profile_expect_probablility_index += 1
                open_file.close()
    correlations_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Correlation between observed and predicted profiles from CDS start + 120 to CDS stop - 60"
    )
    parser.add_argument(
        "-t",
        "--transcriptome",
        help="fasta file of transcripts, CDS start and end may be provided on description line using tab separation e.g. >NM_0001  10  5000, otherwise it searches for longest ORF"
        ", required=True",
    )
    parser.add_argument(
        "-a",
        "--alignment",
        help="sorted bam file of transcriptome alignments",
        required=True,
    )
    parser.add_argument("-o", "--offset", help="nucleotide offset to A-site", type=int)
    parser.add_argument(
        "-l",
        "--lengths",
        help="lengths of footprints included, for example 28:32 is 28,29,30,31,32",
    )
    parser.add_argument(
        "-P",
        "--Path",
        help='path to outputfile, default is "amino"',
        default="predict_profiles",
    )
    parser.add_argument("-r", "--rustfile", help="path to rust file produced by codon")
    parser.add_argument(
        "-o",
        metavar="outfile directory",
        help='path to outputfile, default is "predict_profiles"',
        default="predict_profiles",
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help="writes all profiles in csv files, may produce >10,000 files",
        default=False,
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.2")
    args = parser.parse_args(None)
    main(args)
