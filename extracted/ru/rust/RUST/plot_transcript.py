#!/usr/bin/python
#####################################################################################
# rust_plot_transcript, Plot observed and predicted ribosome profiles
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

import os, re, pysam, sys, math, argparse
from RUST.methods import *

try:
    import numpy
except:
    pass

try:
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    from pylab import MaxNLocator
except:
    pass


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
            ]  # for 12 codons positions near A-site the RUST ratios are recorded
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
            "l, lengths of footprints parameter not in correct format, it should be either colon seperated with the second value greater or equal to the first, (28:32) or a single interger (31)"
        )
    if len(accepted_read_lengths) == 0:
        stop_err(
            "l, lengths of footprints parameter not in correct format, it should be either colon seperated with the second value greater or equal to the first, (28:32) or a single interger (31)"
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

    list_transcripts = seq_dict.keys()
    transcript_of_inter = args.identifier
    transcript_of_inter2 = transcript_of_inter
    if transcript_of_inter not in list_transcripts:
        count_occurences = 0
        for known_transcript in list_transcripts:
            if transcript_of_inter in known_transcript:
                transcript_of_inter2 = known_transcript
                count_occurences += 1
        if transcript_of_inter2 == transcript_of_inter:
            stop_err("Transcript not in Transcriptome file")
        if count_occurences > 1:
            stop_err("%s not unique identifier" % transcript_of_inter)
        sys.stdout.write(
            "%s not in Transcriptome file, data provided for %s\n"
            % (transcript_of_inter, transcript_of_inter2)
        )

    for transcript in [transcript_of_inter2]:
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
                continue

        elongation_region_all = seq_dict[transcript][cds_start:cds_end]
        if (
            len(elongation_region_all) % 3 != 0
        ):  # genes with codon region not divisible by 3 skipped
            stop_err("%s, CDS not divisible by 3\n" % transcript)

        profile_expect = []
        for n in range(
            0, len(elongation_region_all[120:-60]), 3
        ):  # predicts profile from 120 nts after start to 60 before stop
            minus6_plus5_footprint = elongation_region_all[
                120 + n - 18 : 120 + n + 16
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
        all_reads = aligments_A1.fetch(transcript)

        len_elongation_region = len(profile_list)
        for read in all_reads:
            readlen = read.qlen
            if readlen not in accepted_read_lengths:
                continue  # selection of read of acceptable length
            A_site = read.pos + offset - cds_start - 120  # addition of offset
            if len_elongation_region > A_site > -1:
                profile_list[A_site] += 1

        sys.stdout.write(
            "Average read density = %s\n"
            % round(sum(profile_list) / len(profile_list), 3)
        )
        if not os.path.exists(args.Path):
            os.mkdir(args.Path)
        open_file = open(
            "%s/observed_predicted_%s_%s_%s_%s.csv"
            % (
                args.Path,
                args.identifier,
                alignment_filename,
                args.offset,
                length_values,
            ),
            "w",
        )
        profiles_control_codon = [
            profile_list[codon_ind]
            + profile_list[codon_ind + 1]
            + profile_list[codon_ind + 2]
            for codon_ind in range(0, len(profile_list), 3)
        ]
        profile_expect_probablility_index = 0
        open_file.write("%s\n" % transcript)
        open_file.write("codon, predicted probability, alignments\n")
        for coordinate_index in range(0, len(elongation_region_all[120:-60]), 3):
            codon = elongation_region_all[
                120 + coordinate_index : 120 + coordinate_index + 3
            ]
            open_file.write("%s, " % (codon))
            open_file.write(
                "%s, "
                % (profile_expect_probablility[profile_expect_probablility_index])
            )
            open_file.write(
                "%s\n" % (profiles_control_codon[profile_expect_probablility_index])
            )
            profile_expect_probablility_index += 1
    open_file.close()

    try:
        # if 1:
        mpl.rcParams["xtick.direction"] = "out"
        mpl.rcParams["ytick.direction"] = "out"
        mpl.rcParams["legend.fontsize"] = 10
        mpl.rcParams["ytick.labelsize"] = 10
        mpl.rcParams["xtick.labelsize"] = 10
        mpl.rcParams["font.size"] = 10
        mpl.rcParams["axes.titlesize"] = 10
        mpl.rcParams["legend.frameon"] = 0
        mpl.rcParams["axes.axisbelow"] = False
        mpl.rcParams["xtick.major.pad"] = 2.0
        mpl.rcParams["ytick.major.pad"] = 2
        mpl.rcParams["xtick.major.size"] = 2.0
        mpl.rcParams["ytick.major.size"] = 2
        mpl.rcParams["axes.linewidth"] = 0.5
        mpl.rcParams["ytick.major.width"] = 0.25
        mpl.rcParams["xtick.major.width"] = 0.25
        mpl.rcParams["lines.linewidth"] = 1
        mpl.rcParams["legend.borderpad"] = 0.01
        mpl.rcParams["legend.labelspacing"] = 0.05
        mpl.rcParams["legend.columnspacing"] = 0.5
        mpl.rcParams["legend.borderaxespad"] = 0.15
        mpl.rcParams["legend.handlelength"] = 1

        fig = plt.figure(figsize=(6.69, 6.0))
        plt.subplots_adjust(left=0.09, right=0.87)
        ax = fig.add_subplot(111)
        ax.plot(profiles_control_codon, color="gray", label="observed")
        ax2 = ax.twinx()
        ax2.plot(
            profile_expect_probablility, "--", color="DarkMagenta", label="predicted"
        )

        try:
            ax.text(
                0.1,
                1.05,
                "r =%s"
                % round(
                    numpy.corrcoef(profiles_control_codon, profile_expect_probablility)[
                        0, 1
                    ],
                    2,
                ),
                transform=ax.transAxes,
            )
        except:
            pass

        l = ax.legend(
            bbox_to_anchor=(0, 0, 0.890, 1.05), bbox_transform=ax.transAxes, ncol=1
        )
        l = ax2.legend(
            bbox_to_anchor=(0, 0, 0.890, 1.10), bbox_transform=ax2.transAxes, ncol=1
        )

        ax.set_xlabel("transcript coordinates [codon]")
        ax.set_ylabel("# alignments")
        ax.yaxis.set_major_locator(MaxNLocator(5))
        tciks = ax.get_xticks()
        cds_start_codon = cds_start / 3
        tciks2 = [int(n) + 40 + cds_start_codon for n in tciks]
        ax.set_xticklabels(tciks2)

        ax.set_title(transcript_of_inter)
        for tl in ax2.get_yticklabels():
            tl.set_color("DarkMagenta")
        ax2.yaxis.set_major_locator(MaxNLocator(5))
        ax2.set_ylabel("probability", color="darkmagenta")
        ax2.set_xlim(0, len(profile_expect_probablility))
        ax.set_xlim(0, len(profile_expect_probablility))

        plt.savefig(
            "%s/observed_predicted_%s_%s_%s_%s.png"
            % (
                args.Path,
                args.identifier,
                alignment_filename,
                args.offset,
                length_values,
            )
        )
    except:
        sys.stdout.write("Error producing images\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Plot observed and predicted ribosome profiles"
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
        "-P", "--Path", help='path to outputfile, default is "amino"', default="plot"
    )
    parser.add_argument(
        "-i",
        "--identifier",
        help='Specific transcript to plot (Use of unique identifier is sufficient for example "NM_031946"',
        required=True,
    )
    parser.add_argument(
        "-r",
        "--rustfile",
        help='path to file produced from "rust_codon"',
        required=True,
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.2")
    args = parser.parse_args(None)

    main(args)
