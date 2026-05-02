#!/usr/bin/env python
#####################################################################################
# rust_codon, Produces RUST metagene profile of codons
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
        codon = linesplit[0]
        coverage = list(map(float, linesplit[1:]))
        coverage_a = coverage[0]
        if coverage_a == 0:
            continue
        coverage_n = [n / coverage_a for n in coverage[1:]]
        log2_values = [math.log(n, 2) if n != 0 else float("-inf") for n in coverage_n]
        ax36.plot(log2_values, color="gray")

    line = infileopen36.readline()
    linesplit = line.split(",")
    if "NA" not in line:
        coverage = map(float, linesplit[2:])
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
    ax36.set_ylabel("Codon RUST ratio (observed/expected), log2")
    ax36.axvline(40, color="red")


def A_site_plot(infileopen35, dict_codon75, axis_Asite53, loc2):
    codon_to_amino_dict = {}
    amino_to_codons_dict = {}
    for amino_acid, codons in dict_codon75.items():
        for codon in codons:
            codon_to_amino_dict[codon] = amino_acid
            amino_to_codons_dict.setdefault(amino_acid, []).append(codon)

    list1 = []
    list2 = []
    infileopen35.seek(0)
    infileopen35.readline()
    dict_amino_value = {}
    for line in infileopen35:
        linesplit = line.split(",")
        if len(linesplit) == 1:
            break
        codon = linesplit[0]
        if codon in ["TAA", "TAG", "TGA"]:
            continue
        list1.append(linesplit[0])
        coverage = list(map(float, linesplit[1:]))
        coverage_a = coverage[0]
        coverage_n = [n / coverage_a for n in coverage[1:]]
        list2.append(float(coverage_n[loc2]))

        amino = codon_to_amino_dict[linesplit[0]]
        if amino in dict_amino_value:
            dict_amino_value[codon_to_amino_dict[linesplit[0]]].append(
                float(coverage_n[loc2])
            )
        else:
            dict_amino_value[codon_to_amino_dict[linesplit[0]]] = [
                float(coverage_n[loc2])
            ]

    list_amino_sorted = []
    for key, value in dict_amino_value.items():
        list_amino_sorted.append((mean_value(value), key))
    list_amino_sorted.sort()

    A_site_value_norm = [n / min(list2) for n in list2]
    list3 = list(zip(A_site_value_norm, list1))
    list3.sort()
    A_site_value_norm_dict = {}
    for tupel in list3:
        A_site_value_norm_dict[tupel[1]] = tupel[0]

    used_codons = []
    xloc = []
    xtick_label = []
    n1 = 0

    for _, amino_acid in list_amino_sorted:
        if amino_acid in used_codons:
            continue
        used_codons.append(amino_acid)
        n1 += 1  # len(dict_list_codon[amino_acid])

        xloc.append(n1)
        for amino_acid_codon in amino_to_codons_dict[amino_acid]:
            axis_Asite53.scatter(
                n1,
                A_site_value_norm_dict[amino_acid_codon],
                color="gray",
                s=50,
                edgecolor="gray",
            )
        xtick_label.append(amino_acid)

    axis_Asite53.set_xticks(xloc)
    axis_Asite53.set_xticklabels(xtick_label, rotation=90)
    for tick in axis_Asite53.get_xticklabels():
        if tick.get_text() in ["Phe", "Tyr", "Trp"]:
            a2 = tick.set_backgroundcolor("lightgreen")  # (dict(facecolor = "red"))
            # tick.set_color("white")
        if tick.get_text() in ["Val", "Ala", "Leu", "Met", "Ile"]:
            tick.set_backgroundcolor("lightgrey")
            # tick.set_color("white")
        if tick.get_text() in ["Ser", "Asn", "Thr", "Gln"]:
            tick.set_backgroundcolor("ForestGreen")
            tick.set_color("white")

        if tick.get_text() in ["His", "Lys", "Arg"]:
            tick.set_backgroundcolor("blue")
            tick.set_color("white")
        if tick.get_text() in ["Glu", "Asp"]:
            tick.set_backgroundcolor("red")
            tick.set_color("white")
    axis_Asite53.set_xlim(0, n1 + 1)
    axis_Asite53.set_ylabel("A-site codon RUST ratio")

    red = mpl.patches.Rectangle((0, 0), 1, 1, fc="r")
    blue = mpl.patches.Rectangle((0, 0), 1, 1, fc="b")
    fgreen = mpl.patches.Rectangle((0, 0), 1, 1, fc="ForestGreen")
    lgreen = mpl.patches.Rectangle((0, 0), 1, 1, fc="lightGreen")
    grey = mpl.patches.Rectangle((0, 0), 1, 1, fc="lightgrey")

    axis_Asite53.legend(
        [red, grey, lgreen, blue, fgreen],
        ["acidic", "aliphatic", "aromatic", "basic", "polar\nuncharged"],
        bbox_to_anchor=(0, 0, 0.8, 1.12),
        ncol=3,
    )


def main(args):

    universal_code = {
        "Ala": ["GCT", "GCC", "GCG", "GCA"],
        "Gly": ["GGT", "GGC", "GGG", "GGA"],
        "Pro": ["CCT", "CCC", "CCG", "CCA"],
        "Thr": ["ACT", "ACC", "ACG", "ACA"],
        "Val": ["GTT", "GTC", "GTG", "GTA"],
        "Ser": ["TCT", "TCC", "TCG", "TCA", "AGT", "AGC"],
        "Arg": ["CGT", "CGC", "CGG", "CGA", "AGG", "AGA"],
        "Leu": ["CTT", "CTC", "CTG", "CTA", "TTG", "TTA"],
        "Phe": ["TTT", "TTC"],
        "Asn": ["AAT", "AAC"],
        "Lys": ["AAG", "AAA"],
        "Asp": ["GAT", "GAC"],
        "Glu": ["GAG", "GAA"],
        "His": ["CAT", "CAC"],
        "Gln": ["CAG", "CAA"],
        "Ile": ["ATT", "ATC", "ATA"],
        "Met": ["ATG"],
        "Tyr": ["TAT", "TAC"],
        "Cys": ["TGT", "TGC"],
        "Trp": ["TGG"],
        "Stop": ["TGA", "TAG", "TAA"],
    }

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
    aligments_A1 = pysam.Samfile(
        args.alignment, "rb"
    )  # path to aligments in bam format

    codon_enrichment_dict = {}
    codon_enrichment_expected_dict = {}
    for nt in nts:
        for nt2 in nts:
            for nt3 in nts:
                codon = "%s%s%s" % (nt, nt2, nt3)
                codon_enrichment_dict[codon] = {}
                codon_enrichment_expected_dict[codon] = []
                for number in range(0, 60, 1):
                    codon_enrichment_dict[codon][number] = [0.0, 0.0]

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
        # peptide_sequence        = elongation_region_all.translate()

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

            codon_start = 0
            for sliding_w_n in range(
                0, len(elongation_region_part), 3
            ):  # sliding window using increments of 3 nts
                codon_window = str(
                    elongation_region_all[codon_start : codon_start + 180]
                )  # 60 codon window,
                if len(set(codon_window) - set(["A", "T", "G", "C"])) != 0:
                    codon_start += 3
                    continue

                if (
                    profile_list[sliding_w_n]
                    + profile_list[sliding_w_n + 1]
                    + profile_list[sliding_w_n + 2]
                ) / 3 > average_gene_density:
                    for number in range(0, 60):
                        codon = codon_window[number * 3 : (number + 1) * 3]
                        codon_enrichment_dict[codon][number][0] += 1
                        codon_enrichment_dict[codon][number][1] += 1
                else:
                    for number in range(0, 60):
                        codon = codon_window[number * 3 : (number + 1) * 3]
                        codon_enrichment_dict[codon][number][0] += 1

                codon = codon_window[120:123]  # corresponds to A-site codon
                codon_enrichment_expected_dict[codon].append(expected_codon_density)
                codon_start += 3

    if not os.path.exists(args.Path):
        os.mkdir(args.Path)
    alignment_filename = args.alignment.split("/")[-1]
    outfile = open(
        "%s/RUST_codon_file_%s_%s_%s"
        % (args.Path, alignment_filename, args.offset, length_values),
        "w",
    )
    outfile.write("codon, expected value")
    for number106 in range(-40, 20):
        outfile.write(", %s" % number106)
    outfile.write("\n")

    list_codons = []
    codons = list(codon_enrichment_dict)
    codons.sort()
    rust_expected = []
    rust_observed_metafootprint = []
    for codon in codons:
        if codon in list_codons:
            continue
        if codon in ["TAA", "TGA", "TAG"]:
            continue
        list_codons.append(codon)
        outfile.write("%s" % codon)
        if codon_enrichment_expected_dict[codon] != []:
            outfile.write(", %s" % mean_value(codon_enrichment_expected_dict[codon]))
        list_data = []
        for number in range(0, 60):
            if codon_enrichment_dict[codon][number][0] != 0:
                outfile.write(
                    ", %s"
                    % (
                        codon_enrichment_dict[codon][number][1]
                        / codon_enrichment_dict[codon][number][0]
                    )
                )
                list_data.append(
                    codon_enrichment_dict[codon][number][1]
                    / codon_enrichment_dict[codon][number][0]
                )
            else:
                outfile.write(", 0")
                list_data.append(0)
        outfile.write("\n")
        rust_expected.append(mean_value(codon_enrichment_expected_dict[codon]))
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
            "%s/RUST_codon_file_%s_%s_%s"
            % (args.Path, alignment_filename, args.offset, length_values)
        )
        ax1_metafootprint = fig.add_subplot(111)
        RUST_metagene_plot(infileopen, ax1_metafootprint)
        plt.savefig(
            "%s/RUST_codon_metafootprint_%s_%s_%s.png"
            % (args.Path, alignment_filename, args.offset, length_values)
        )
        plt.clf()

        infileopen = open(
            "%s/RUST_codon_file_%s_%s_%s"
            % (args.Path, alignment_filename, args.offset, length_values)
        )
        ax1codon_Asite = fig.add_subplot(111)
        A_site_plot(infileopen, universal_code, ax1codon_Asite, 40)
        plt.savefig(
            "%s/A_site_%s_%s_%s.png"
            % (args.Path, alignment_filename, args.offset, length_values)
        )

    except:
        sys.stdout.write("Error producing images\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Produces RUST metagene profile of codons"
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
        "-P", "--Path", help='path to outputfile, default is "codon"', default="codon"
    )
    args = parser.parse_args(None)

    main(args)
