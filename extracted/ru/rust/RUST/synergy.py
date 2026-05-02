#!/usr/bin/python
#####################################################################################
# rust_synergy, Identifies tripeptides that are candidates for synergistic interactions
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

import numpy as np
import argparse, os, sys
from RUST.methods import *


def main(args):
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

    infileopen = open(args.tri)
    infileopen.readline()
    list_amino = []
    list_zscores = []
    list_fold_change = []
    list_loc = []

    for line in infileopen:
        linesplit = line[:-1].split(",")
        if len(linesplit) == 1:
            break
        amino = linesplit[0]
        coverage = list(map(float, linesplit[1:]))
        coverage_a = coverage[0]
        if coverage_a == 0:
            continue
        coverage_n = [n / coverage_a for n in coverage[1:]]

        if len(amino) != 3 or len(set(amino) - set(amino_acids)) != 0:
            sys.stderr.write(
                "Tripeptide metafootprint file not in correct, check input file\n"
            )
            # if os.path.exists( tmp_dir ): shutil.rmtree( tmp_dir )
            exit()
        aminoA = amino[0]
        aminoB = amino[1]
        aminoC = amino[2]

        infileopen2 = open(args.aa)
        infileopen2.seek(0)
        infileopen2.readline()
        for line2 in infileopen2:
            linesplit = line2[:-1].split(",")
            if len(linesplit) == 1:
                break
            amino2 = linesplit[0]
            if len(amino2) != 1 or len(set(amino2) - set(amino_acids)) != 0:
                sys.stderr.write(
                    "Amino acid metafootprint file not correct, check input file\n"
                )
                # if os.path.exists( tmp_dir ): shutil.rmtree( tmp_dir )
                exit()
            if amino2 in amino:
                coverage = list(map(float, linesplit[1:]))
                coverage_a = coverage[0]
                if coverage_a == 0:
                    continue
                if amino2 == aminoA:
                    coverage_n1 = [n / coverage_a for n in coverage[1:]]
                if amino2 == aminoB:
                    coverage_n2 = [n / coverage_a for n in coverage[1:]]
                if amino2 == aminoC:
                    coverage_n3 = [n / coverage_a for n in coverage[1:]]
        infileopen2.close()

        coverage_n_e = 0
        differences = []

        # for number_i in range(11):
        ##coverage_n_e = coverage_n1[number_i]*coverage_n2[number_i+1]*coverage_n3[number_i+2]
        # differences.append(abs(coverage_n[number_i]) - abs(coverage_n_e))
        for number_i in range(58):
            coverage_n_e = (
                coverage_n1[number_i]
                * coverage_n2[number_i + 1]
                * coverage_n3[number_i + 2]
            )
            differences.append(abs(coverage_n[number_i]) - abs(coverage_n_e))

        std_diff = np.std(differences)

        line_count = 0
        for number_i in range(0, len(coverage_n) - 2):
            coverage_n_e = (
                coverage_n1[number_i]
                * coverage_n2[number_i + 1]
                * coverage_n3[number_i + 2]
            )

            list_amino.append(amino)
            list_zscores.append((coverage_n[number_i] - coverage_n_e) / std_diff)
            list_loc.append(number_i)
            if coverage_n_e == 0:
                list_fold_change.append("not defined")
            else:
                list_fold_change.append(coverage_n[number_i] / coverage_n_e)

    if not os.path.exists(args.Path):
        os.mkdir(args.Path)
    if "/" in args.aa:
        amino_file_split = args.aa.split("/")[-1]
    else:
        amino_file_split = args.aao
    if "RUST_amino_file_" in amino_file_split:
        amino_file = amino_file_split[16:]
    else:
        amino_file = amino_file_split

    if "/" in args.tri:
        tripeptide_file_split = args.tri.split("/")[-1]
    else:
        tripeptide_file_split = args.tri
    if "RUST_tripeptide_file_" in tripeptide_file_split:
        tripeptide_file = tripeptide_file_split[21:]
    else:
        tripeptide_file = tripeptide_file_split

    outfile = open("%s/synergy_%s_%s" % (args.Path, amino_file, tripeptide_file), "w")
    outfile.write(
        "Tripeptide, Standard score, distance of 1st residue from A-site, fold change\n"
    )
    zipped_list = list(zip(list_zscores, list_amino, list_loc, list_fold_change))
    zipped_list.sort()
    zipped_list.reverse()
    for zscore, amino, loc, fold_change in zipped_list:
        if abs(zscore) > 5:
            outfile.write("%s, %s, %s, %s\n" % (amino, zscore, loc - 40, fold_change))
    outfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Identifies tripeptides that are candidates for synergistic interactions"
    )
    parser.add_argument(
        "-t",
        "--transcriptome",
        help="fasta file of transcripts, CDS start and end may be provided on description line using tab separation e.g. >NM_0001  10  5000, otherwise it searches for longest ORF"
        ", required=True",
    )
    parser.add_argument(
        "--aa", help='path to file produced from "rust_amino"', required=True
    )
    parser.add_argument(
        "--tri", help='path to file produced from "rust_tripeptide"', required=True
    )
    parser.add_argument(
        "-P",
        "--Path",
        help='path to outputfile, default is "synergy"',
        default="synergy",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.2")
    args = parser.parse_args(None)

    main(args)
