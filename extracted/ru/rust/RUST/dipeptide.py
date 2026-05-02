#!/usr/bin/python
#####################################################################################
# rust_dipeptide, Produces RUST metagene profile of dipeptides
# Copyright (C) 2015, Patrick O'Connor

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
    log_style = 1
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
        if min(coverage_n[:-1]) == 0:
            log_style = 0
            continue

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
        if log_style:
            log2_values = [math.log(n, 2) for n in coverage_n[:-1]]
            ax36.plot(log2_values, color="gray")
        else:
            ax36.plot(coverage_n[:-1], color="gray")

    line = infileopen36.readline()
    linesplit = line.split(",")
    if "NA" not in line[:-3]:
        coverage = list(map(float, linesplit[2:-1]))
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

    ax36.set_xticks([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
    ax36.set_xticklabels([-35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15])
    ax36.set_xlabel("distance from A-site [codon]")
    if log_style:
        ax36.set_ylabel("Dipeptide RUST ratio (observed/expected), log2")
    else:
        ax36.set_ylabel("Dipeptide RUST ratio (observed/expected)")
    ax36.axvline(40, color="red")
    # ax36.legend()


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

    offset = args.offset  # path to fastq file of transcripts
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
    aligments_A1 = pysam.Samfile(
        args.alignment, "rb"
    )  # path to aligments in bam format

    dipeptide_enrichment_dict = {}
    dipeptide_enrichment_expected_dict = {}
    for amino_acid in amino_acids:
        for amino_acid2 in amino_acids:
            # for amino_acid3 in amino_acids :
            dipeptide = "%s%s" % (amino_acid, amino_acid2)
            dipeptide_enrichment_dict[dipeptide] = {}
            dipeptide_enrichment_expected_dict[dipeptide] = []
            for number in range(0, 60, 1):
                dipeptide_enrichment_dict[dipeptide][number] = [0.0, 0.0]

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
        if len(elongation_region_part) % 3 != 0:
            # sys.stdout.write( '%s, CDS not divisible by 3\n'%transcript  )
            continue
        peptide_sequence = translate_dna(elongation_region_all)

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
            expected_codon_density = float(num_codon) / (
                len(profile_list) / 3
            )  # expected enrichment value

            peptide_start = 0
            for sliding_w_n in range(
                0, len(elongation_region_part), 3
            ):  # sliding window using increments of 3 nts
                amino_window = str(peptide_sequence[peptide_start : peptide_start + 60])
                if len(set(amino_window) - set(amino_acids)) != 0:
                    peptide_start += 1
                    continue

                if (
                    profile_list[sliding_w_n]
                    + profile_list[sliding_w_n + 1]
                    + profile_list[sliding_w_n + 2]
                ) / 3 > average_gene_density:
                    for number in range(0, 59):
                        amino_acid_2 = amino_window[number : number + 2]
                        dipeptide_enrichment_dict[amino_acid_2][number][0] += 1
                        dipeptide_enrichment_dict[amino_acid_2][number][1] += 1
                else:
                    for number in range(0, 59):
                        amino_acid_2 = amino_window[number : number + 2]
                        dipeptide_enrichment_dict[amino_acid_2][number][0] += 1

                amino_acid_2 = amino_window[40:42]
                dipeptide_enrichment_expected_dict[amino_acid_2].append(
                    expected_codon_density
                )
                peptide_start += 1

    alignment_filename = args.alignment.split("/")[-1]
    if not os.path.exists(args.Path):
        os.mkdir(args.Path)

    outfile = open(
        "%s/RUST_dipeptide_file_%s_%s_%s"
        % (args.Path, alignment_filename, args.offset, length_values),
        "w",
    )
    outfile.write("dipeptide, expected value")
    for number106 in range(-40, 20):
        outfile.write(", %s" % number106)
    outfile.write("\n")

    list_codons = []
    list_amino_acids = list(dipeptide_enrichment_dict.keys())
    list_amino_acids.sort()
    rust_expected = []
    rust_observed_metafootprint = []
    for amino2 in list_amino_acids:
        if amino2 in list_codons:
            continue
        list_codons.append(amino2)
        outfile.write("%s" % amino2)
        if dipeptide_enrichment_expected_dict[amino2] != []:
            outfile.write(
                ", %s" % mean_value(dipeptide_enrichment_expected_dict[amino2])
            )
        list_data = []
        for number in range(0, 60):
            if dipeptide_enrichment_dict[amino2][number][0] != 0:
                outfile.write(
                    ", %s"
                    % (
                        dipeptide_enrichment_dict[amino2][number][1]
                        / dipeptide_enrichment_dict[amino2][number][0]
                    )
                )
                list_data.append(
                    dipeptide_enrichment_dict[amino2][number][1]
                    / dipeptide_enrichment_dict[amino2][number][0]
                )
            else:
                outfile.write(", 0")
                list_data.append(0)
        outfile.write("\n")
        rust_expected.append(mean_value(dipeptide_enrichment_expected_dict[amino2]))
        rust_observed_metafootprint.append(list_data)

    rust_expected_sum = sum(rust_expected)
    q_values = [n / rust_expected_sum for n in rust_expected]

    shannon_values = []
    for loc_i in range(60):
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
            "%s/RUST_dipeptide_file_%s_%s_%s"
            % (args.Path, alignment_filename, args.offset, length_values)
        )
        ax1_metafootprint = fig.add_subplot(111)
        RUST_metagene_plot(infileopen, ax1_metafootprint)
        plt.savefig(
            "%s/RUST_dipeptide_metafootprint_%s_%s_%s.png"
            % (args.Path, alignment_filename, args.offset, length_values)
        )

    except:
        sys.stdout.write("Error producing images\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Produces RUST metagene profile of dipeptides"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.2")

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
        help='path to outputfile, default is "dipeptide"',
        default="dipeptide",
    )
    args = parser.parse_args(None)
    main(args)
