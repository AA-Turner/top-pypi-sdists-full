#!/usr/bin/python
#####################################################################################
# rust_nucleotide, Produces RUST metagene profile of nucleotides
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
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    from pylab import MaxNLocator
except:
    pass


def RUST_metagene_plot(infileopen36, ax36):
    infileopen36.seek(0)
    infileopen36.readline()
    while 1:
        line = infileopen36.readline()
        linesplit = line.split(",")
        if len(linesplit) == 1:
            break
        nucleotide_type = linesplit[0]
        coverage = list(map(float, linesplit[1:]))
        coverage_a = coverage[0]
        if coverage_a == 0:
            continue
        coverage_n = [n / coverage_a for n in coverage[1:]]
        # ax36.plot(log2(coverage_n[:-2]),color = "gray")
        log2_values = [math.log(n, 2) for n in coverage_n]
        if nucleotide_type == "A":
            ax36.plot(log2_values, color="firebrick", label=nucleotide_type)
        elif nucleotide_type == "T":
            ax36.plot(log2_values, color="seagreen", label=nucleotide_type)
        elif nucleotide_type == "G":
            ax36.plot(log2_values, color="Orange", label=nucleotide_type)
        else:
            ax36.plot(log2_values, color="MediumPurple", label=nucleotide_type)

    line = infileopen36.readline()
    linesplit = line.split(",")
    if "NA" not in linesplit:
        coverage = list(map(float, linesplit[2:]))
        ax2 = ax36.twinx()
        ax2.plot(coverage, color="blue")
        for tl in ax2.get_yticklabels():
            tl.set_color("blue")
            tl.set_rotation(0)

        ax2.yaxis.set_major_locator(MaxNLocator(3))
        ax2.set_ylim(0, 1.0)
        ax2.set_ylim(-2, 1.0)
        ax2.set_yticks([0, 1], minor=False)
        ax2.set_yticklabels(["0", "1"])
        ax2.set_ylabel("Kullback-Leibler divergence", color="blue")

    ax36.set_xticks([15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165])
    ax36.set_xticklabels([-105, -90, -75, -60, -45, -30, -15, 0, 15, 30, 45])
    ax36.set_xlabel("distance from A-site [codon]")
    ax36.set_ylabel("Nucleotide RUST ratio (observed/expected), log2")
    ax36.axvline(120, color="red")
    ax36.legend(bbox_to_anchor=(0, 0, 0.2, 0.9))


def main(args):

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

    nts = ["A", "G", "C", "T"]
    aligments_A1 = pysam.Samfile(args.alignment, "rb")

    nucleotide_enrichment_dict = {}
    nucleotide_enrichment_expected_dict = {}
    for nt in nts:
        nucleotide_enrichment_dict[nt] = {}
        nucleotide_enrichment_expected_dict[nt] = []
        for number in range(0, 180, 1):
            nucleotide_enrichment_dict[nt][number] = [0.0, 0.0]

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

        try:  # use supplied CDS annotation
            cds_start = cds_start_dict[transcript]
            cds_end = cds_end_dict[transcript]
            if cds_end < cds_start:
                raise Exception
        except Exception:  # find longest ORF
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
        elongation_region_part = elongation_region_all[
            120:-60
        ]  # first 120 and last 60 nt are not used
        # peptide_sequence       = elongation_region_all.translate()

        if len(elongation_region_part) % 3 != 0:
            # sys.stdout.write( '%s, CDS not divisible by 3\n'%transcript  )
            continue
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

        average_gene_density = float(sum(profile_list)) / len(profile_list)

        if average_gene_density != 0:
            num_codon = len(
                [
                    1
                    for number88 in range(0, len(profile_list), 3)
                    if (
                        (
                            profile_list[number88]
                            + profile_list[number88 + 1]
                            + profile_list[number88 + 2]
                        )
                        / 3
                    )
                    > average_gene_density
                ]
            )
            # number of codons that exceed average gene density
            expected_codon_density = float(num_codon) / (len(profile_list) / 3)

            codon_start = 0
            for sliding_w_n in range(
                0, len(elongation_region_part), 3
            ):  # sliding window using increments of 3 nts
                codon_window = str(
                    elongation_region_all[codon_start : codon_start + 180]
                )
                if len(set(codon_window) - set(["A", "T", "G", "C"])) != 0:
                    codon_start += 3
                    continue

                if (
                    profile_list[sliding_w_n]
                    + profile_list[sliding_w_n + 1]
                    + profile_list[sliding_w_n + 2]
                ) / 3 > average_gene_density:
                    for number in range(0, 180):
                        nucleotide3 = codon_window[number]
                        nucleotide_enrichment_dict[nucleotide3][number][0] += 1
                        nucleotide_enrichment_dict[nucleotide3][number][1] += 1
                else:
                    for number in range(0, 180):
                        nucleotide3 = codon_window[number]
                        nucleotide_enrichment_dict[nucleotide3][number][0] += 1

                nucleotide3 = codon_window[120:121]
                nucleotide_enrichment_expected_dict[nucleotide3].append(
                    expected_codon_density
                )
                nucleotide3 = codon_window[121:122]
                nucleotide_enrichment_expected_dict[nucleotide3].append(
                    expected_codon_density
                )
                nucleotide3 = codon_window[122:123]
                nucleotide_enrichment_expected_dict[nucleotide3].append(
                    expected_codon_density
                )
                codon_start += 3

    if not os.path.exists(args.Path):
        os.mkdir(args.Path)
    alignment_filename = args.alignment.split("/")[-1]
    outfile = open(
        "%s/RUST_nucleotide_file_%s_%s_%s"
        % (args.Path, alignment_filename, args.offset, length_values),
        "w",
    )
    outfile.write("nucleotide, expected value")
    for number106 in range(-120, 60):
        outfile.write(", %s" % number106)
    outfile.write("\n")

    list_nucleotide2 = []
    nucleotides = list(nucleotide_enrichment_expected_dict.keys())
    nucleotides.sort()
    rust_expected = []
    rust_observed_metafootprint = []
    for nucleotide2 in nucleotides:
        if nucleotide2 in list_nucleotide2:
            continue
        list_nucleotide2.append(nucleotide2)
        outfile.write("%s" % nucleotide2)
        outfile.write(
            ", %s" % mean_value(nucleotide_enrichment_expected_dict[nucleotide2])
        )
        list_data = []
        for number in range(0, 180):
            if nucleotide_enrichment_dict[nucleotide2][number][0] != 0:
                outfile.write(
                    ", %s"
                    % (
                        nucleotide_enrichment_dict[nucleotide2][number][1]
                        / nucleotide_enrichment_dict[nucleotide2][number][0]
                    )
                )
                list_data.append(
                    nucleotide_enrichment_dict[nucleotide2][number][1]
                    / nucleotide_enrichment_dict[nucleotide2][number][0]
                )
            else:
                outfile.write(", 0")
                list_data.append(0)
        rust_expected.append(
            mean_value(nucleotide_enrichment_expected_dict[nucleotide2])
        )
        rust_observed_metafootprint.append(list_data)
        outfile.write("\n")

    rust_expected_sum = sum(rust_expected)
    q_values = [n / rust_expected_sum for n in rust_expected]
    shannon_values = []
    for loc_i in range(180):
        rust_observed = [n[loc_i] for n in rust_observed_metafootprint]
        rust_observed_sum = sum(rust_observed)
        rust_observed_min = min(rust_observed)
        if rust_observed_min == 0:
            shannon_values.append("NA")
        else:
            p_values = [n / rust_observed_sum for n in rust_observed]
            shannon = []
            list_normalised = []  ####
            for p_value, q_value in zip(p_values, q_values):
                shannon.append(abs(p_value * math.log((p_value / q_value), 2)))
                list_normalised.append(p_value / q_value)  ####
            shannon_values.append(sum(shannon))

    outfile.write("\nKullback Leibler divergence,")
    for value in shannon_values:
        outfile.write(", %s" % value)
    outfile.close()

    try:
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
        infileopen = open(
            "%s/RUST_nucleotide_file_%s_%s_%s"
            % (args.Path, alignment_filename, args.offset, length_values)
        )
        ax1_metafootprint = fig.add_subplot(111)
        RUST_metagene_plot(infileopen, ax1_metafootprint)
        plt.savefig(
            "%s/RUST_nucleotide_metafootprint_%s_%s_%s.png"
            % (args.Path, alignment_filename, args.offset, length_values)
        )
    except:
        sys.stdout.write("Error producing images\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Produces RUST metagene profile of nucleotides"
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
        help='path to outputfile, default is "nucleotide"',
        default="nucleotide",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.2")
    args = parser.parse_args(None)

    main(args)
