# These are used to apply custom modifications for each scheme.
from anarcii.inference.utils import alphabet


def scheme_specifics(regions, scheme_name, chain_type):
    if scheme_name == "imgt":
        return regions

    function = function_dict[scheme_name]

    # The complexity of AHo means that it needs the exact chain type (H, K or L).
    scheme, *_ = scheme_name.split("_")  # Remove the chain name suffix.
    if scheme == "aho":
        result = function(regions, chain_type)
    else:
        result = function(regions)
    return result


def get_cdr3_annotations(length, scheme="imgt", chain_type=""):
    """
    Given a length of a cdr3 give back a list of the annotations that should be applied
    to the sequence. This function should be depreciated - Why?
    """
    az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    za = "ZYXWVUTSRQPONMLKJIHGFEDCBA"

    if scheme == "imgt":
        start, end = 105, 118  # start (inclusive) end (exclusive)
        annotations = [None for _ in range(max(length, 13))]
        front = 0
        back = -1
        if (length - 13) > 49:
            # We ran out of letters.
            exit("Too many insertions for numbering scheme to handle.")
        for i in range(min(length, 13)):
            if i % 2:
                annotations[back] = (end + back, " ")
                back -= 1
            else:
                annotations[front] = (start + front, " ")
                front += 1
        for i in range(max(0, length - 13)):  # add insertions onto 111 and 112 in turn
            if i % 2:
                annotations[back] = (112, za[back + 6])
                back -= 1
            else:
                annotations[front] = (111, az[front - 7])
                front += 1
        return annotations

    elif (
        scheme in ["chothia", "kabat"] and chain_type == "heavy"
    ):  # For chothia and kabat
        # print("RENUMBERING CDR3 HEAVY")
        # Number forwards from 93
        insertions = max(length - 10, 0)
        if insertions > 26:
            # We ran out of letters.
            exit("Too many insertions for numbering scheme to handle.")
        ordered_deletions = [
            (100, " "),
            (99, " "),
            (98, " "),
            (97, " "),
            (96, " "),
            (95, " "),
            (101, " "),
            (102, " "),
            (94, " "),
            (93, " "),
        ]
        annotations = sorted(
            ordered_deletions[max(0, 10 - length) :]
            + [(100, a) for a in az[:insertions]]
        )
        return annotations

    elif scheme in ["chothia", "kabat"] and chain_type == "light":
        # print("RENUMBERING CDR3 LIGHT")
        # Number forwards from 89
        insertions = max(length - 9, 0)
        if insertions > 26:
            # We ran out of letters.
            exit("Too many insertions for numbering scheme to handle.")
        ordered_deletions = [
            (95, " "),
            (94, " "),
            (93, " "),
            (92, " "),
            (91, " "),
            (96, " "),
            (97, " "),
            (90, " "),
            (89, " "),
        ]
        annotations = sorted(
            ordered_deletions[max(0, 9 - length) :] + [(95, a) for a in az[:insertions]]
        )
        return annotations

    else:
        exit("Unimplemented scheme.")


### ### HEAVY FUNCTIONS ### ###
def chothia_heavy(regions):
    # Chothia H region 1 (index 0) >>> Insertions are placed at Chothia position 6.
    # Count how many we recognised as insertion by the hmm
    insertions = len([1 for _ in regions[0] if _[0][1] != " "])
    # We will place all insertion in this region at Chothia position 6.
    if insertions:
        # The starting Chothia number as found by the HMM (could easily start from 2 for
        # example) I have a feeling this may be a source of a bug in very unusual cases.
        # Can't break for now. Will catch mistakes in a validate function.
        start = regions[0][0][0][0]
        length = len(regions[0])
        annotations = (
            [(_, " ") for _ in range(start, 7)]
            + [(6, alphabet[_]) for _ in range(insertions)]
            + [(7, " "), (8, " "), (9, " ")]
        )
        regions[0] = [(annotations[i], regions[0][i][1]) for i in range(length)]
    else:
        regions[0] = regions[0]

    # CDR1
    # Chothia H region 3 (index 2) >>> put insertions onto 31
    length = len(regions[2])
    insertions = max(
        length - 11, 0
    )  # Pulled back to the cysteine as heavily engineered cdr1's are not playing nicely
    if insertions:
        annotations = (
            [(_, " ") for _ in range(23, 32)]
            + [(31, alphabet[i]) for i in range(insertions)]
            + [(32, " "), (33, " ")]
        )
    else:
        annotations = [(_, " ") for _ in range(23, 32)][: length - 2] + [
            (32, " "),
            (33, " "),
        ][:length]
    regions[2] = [(annotations[i], regions[2][i][1]) for i in range(length)]

    # CDR2
    # Chothia H region 5 (index 4) >>> put insertions onto 52
    length = len(regions[4])
    # 50 to 57 inclusive
    insertions = max(
        length - 8, 0
    )  # Eight positions can be accounted for, the remainder are insertions
    # Delete in the order, 52, 51, 50,53, 54 ,55, 56, 57
    annotations = [(50, " "), (51, " "), (52, " ")][: max(0, length - 5)]
    annotations += [(52, alphabet[i]) for i in range(insertions)]
    annotations += [(53, " "), (54, " "), (55, " "), (56, " "), (57, " ")][
        abs(min(0, length - 5)) :
    ]
    regions[4] = [(annotations[i], regions[4][i][1]) for i in range(length)]

    # CDR3
    # Chothia H region 7 (index 6) >>> put insertions onto 100
    length = len(regions[6])
    if length > 36:
        return []
    annotations = get_cdr3_annotations(length, scheme="chothia", chain_type="heavy")
    regions[6] = [(annotations[i], regions[6][i][1]) for i in range(length)]

    return regions


def kabat_heavy(regions):
    # Kabat H region 1 (index 0)
    # Insertions are placed at Kabat position 6.
    # Count how many we recognised as insertion by the hmm
    insertions = len([1 for _ in regions[0] if _[0][1] != " "])
    # We will place all insertion in this region at Kabat position 6.
    if insertions:
        # The starting Kabat number as found by the HMM (could easily start from 2 for
        # example) I have a feeling this may be a source of a bug in very unusual cases.
        # Can't break for now. Will catch mistakes in a validate function.
        start = regions[0][0][0][0]
        length = len(regions[0])
        annotations = (
            [(_, " ") for _ in range(start, 7)]
            + [(6, alphabet[_]) for _ in range(insertions)]
            + [(7, " "), (8, " "), (9, " ")]
        )
        regions[0] = [(annotations[i], regions[0][i][1]) for i in range(length)]
    else:
        regions[0] = regions[0]

    # CDR1
    # Kabat H region 3 (index 2) >>> Put insertions onto 35. Delete from 35 backwards
    length = len(regions[2])
    insertions = max(0, length - 13)
    annotations = [(_, " ") for _ in range(23, 36)][:length]
    annotations += [(35, alphabet[i]) for i in range(insertions)]
    regions[2] = [(annotations[i], regions[2][i][1]) for i in range(length)]

    # CDR2
    # Chothia H region 5 (index 4) >>> put insertions onto 52
    length = len(regions[4])
    # 50 to 57 inclusive
    insertions = max(
        length - 8, 0
    )  # Eight positions can be accounted for, the remainder are insertions
    # Delete in the order, 52, 51, 50,53, 54 ,55, 56, 57
    annotations = [(50, " "), (51, " "), (52, " ")][: max(0, length - 5)]
    annotations += [(52, alphabet[i]) for i in range(insertions)]
    annotations += [(53, " "), (54, " "), (55, " "), (56, " "), (57, " ")][
        abs(min(0, length - 5)) :
    ]
    regions[4] = [(annotations[i], regions[4][i][1]) for i in range(length)]

    # CDR3
    # Chothia H region 7 (index 6) >>> put insertions onto 100
    length = len(regions[6])
    if length > 36:
        return []  # Too many insertions. Do not apply numbering.

    annotations = get_cdr3_annotations(length, scheme="kabat", chain_type="heavy")
    regions[6] = [(annotations[i], regions[6][i][1]) for i in range(length)]

    return regions


def martin_heavy(regions):
    # Chothia H region 1 (index 0)
    # Insertions are placed at Chothia position 8.
    insertions = len([1 for _ in regions[0] if _[0][1] != " "])
    # We will place all insertion in this region at Chothia position 8.
    if insertions:
        # The starting Chothia number as found by the HMM (could easily start from 2 for
        # example). I have a feeling this may be a source of a bug in very unusual
        # cases. Can't break for now. Will catch mistakes in a validate function.
        start = regions[0][0][0][0]
        length = len(regions[0])
        annotations = (
            [(_, " ") for _ in range(start, 9)]
            + [(8, alphabet[_]) for _ in range(insertions)]
            + [(9, " ")]
        )
        regions[0] = [(annotations[i], regions[0][i][1]) for i in range(length)]
    else:
        regions[0] = regions[0]

    # CDR1
    # Chothia H region 3 (index 2) >>> put insertions onto 31
    length = len(regions[2])
    insertions = max(
        length - 11, 0
    )  # Pulled back to the cysteine as heavily engineered cdr1's are not playing nicely
    if insertions:
        annotations = (
            [(_, " ") for _ in range(23, 32)]
            + [(31, alphabet[i]) for i in range(insertions)]
            + [(32, " "), (33, " ")]
        )
    else:
        annotations = [(_, " ") for _ in range(23, 32)][: length - 2] + [
            (32, " "),
            (33, " "),
        ][:length]
    regions[2] = [(annotations[i], regions[2][i][1]) for i in range(length)]

    # CDR2
    # Chothia H region 5 (index 4) >>> put insertions onto 52
    length = len(regions[4])
    # 50 to 57 inclusive
    insertions = max(
        length - 8, 0
    )  # Eight positions can be accounted for, the remainder are insertions
    # Delete in the order, 52, 51, 50,53, 54 ,55, 56, 57
    annotations = [(50, " "), (51, " "), (52, " ")][: max(0, length - 5)]
    annotations += [(52, alphabet[i]) for i in range(insertions)]
    annotations += [(53, " "), (54, " "), (55, " "), (56, " "), (57, " ")][
        abs(min(0, length - 5)) :
    ]
    regions[4] = [(annotations[i], regions[4][i][1]) for i in range(length)]

    # FW3
    # Place all insertions on 72 explicitly. This is in contrast to Chothia
    # implementation where 3 insertions are on 82 and then further insertions are placed
    # by the  alignment Gaps are placed according to the alignment...
    length = len(regions[5])
    insertions = max(length - 35, 0)
    if insertions > 0:  # Insertions on 72
        annotations = (
            [(i, " ") for i in range(58, 73)]
            + [(72, alphabet[i]) for i in range(insertions)]
            + [(i, " ") for i in range(73, 93)]
        )
        regions[5] = [(annotations[i], regions[5][i][1]) for i in range(length)]
    else:  # Deletions - all alignment to place them.
        regions[4] = regions[4]

    # CDR3
    # Chothia H region 7 (index 6) >>> put insertions onto 100
    length = len(regions[6])
    if length > 36:
        return []  # Too many insertions. Do not apply numbering.

    annotations = get_cdr3_annotations(length, scheme="chothia", chain_type="heavy")
    regions[6] = [(annotations[i], regions[6][i][1]) for i in range(length)]

    return regions


### ### LIGHT FUNCTIONS ### ###
def chothia_light(regions):
    # CDR1
    # Chothia L region 2 (index 1)
    # put insertions onto 30
    length = len(regions[1])
    insertions = max(
        length - 11, 0
    )  # Eleven positions can be accounted for, the remainder are insertions
    # Delete forward from 31
    annotations = [
        (24, " "),
        (25, " "),
        (26, " "),
        (27, " "),
        (28, " "),
        (29, " "),
        (30, " "),
    ][: max(0, length)]
    annotations += [(30, alphabet[i]) for i in range(insertions)]
    annotations += [(31, " "), (32, " "), (33, " "), (34, " ")][
        abs(min(0, length - 11)) :
    ]
    regions[1] = [(annotations[i], regions[1][i][1]) for i in range(length)]

    # CDR2
    # Chothia L region 4 (index 3)
    # put insertions onto 52.
    length = len(regions[3])
    insertions = max(length - 4, 0)
    if insertions > 0:
        annotations = (
            [(51, " "), (52, " ")]
            + [(52, alphabet[i]) for i in range(insertions)]
            + [(53, " "), (54, " ")]
        )
        regions[3] = [(annotations[i], regions[3][i][1]) for i in range(length)]
    else:
        # How to gap L2 in Chothia/Kabat/Martin is unclear so we let the alignment do
        # it.
        regions[3] = regions[3]

    # FW3
    # Insertions on 68. First deletion 68. Otherwise default to alignment
    length = len(regions[4])
    insertions = max(length - 34, 0)
    if insertions > 0:  # Insertions on 68
        annotations = (
            [(i, " ") for i in range(55, 69)]
            + [(68, alphabet[i]) for i in range(insertions)]
            + [(i, " ") for i in range(69, 89)]
        )
        regions[4] = [(annotations[i], regions[4][i][1]) for i in range(length)]
    elif length == 33:  # First deletion on 68
        annotations = [(i, " ") for i in range(55, 68)] + [
            (i, " ") for i in range(69, 89)
        ]
        regions[4] = [(annotations[i], regions[4][i][1]) for i in range(length)]
    else:  # More deletions - allow alignment to place them
        regions[4] = regions[4]

    # CDR3
    # Chothia L region 6 (index 5)
    # put insertions onto 95
    length = len(regions[5])
    if length > 36:
        return []  # Too many insertions. Do not apply numbering.

    annotations = get_cdr3_annotations(length, scheme="chothia", chain_type="light")
    regions[5] = [(annotations[i], regions[5][i][1]) for i in range(length)]

    return regions


def kabat_light(regions):
    # CDR1
    # Kabat L region 2 (index 1) >>> put insertions onto 27
    length = len(regions[1])
    insertions = max(
        length - 11, 0
    )  # Eleven positions can be accounted for, the remainder are insertions
    # Delete forward from 28
    annotations = [(24, " "), (25, " "), (26, " "), (27, " ")][: max(0, length)]
    annotations += [(27, alphabet[i]) for i in range(insertions)]
    annotations += [
        (28, " "),
        (29, " "),
        (30, " "),
        (31, " "),
        (32, " "),
        (33, " "),
        (34, " "),
    ][abs(min(0, length - 11)) :]
    regions[1] = [(annotations[i], regions[1][i][1]) for i in range(length)]

    # CDR2
    # Chothia L region 4 (index 3) >>> put insertions onto 52.
    length = len(regions[3])
    insertions = max(length - 4, 0)
    if insertions > 0:
        annotations = (
            [(51, " "), (52, " ")]
            + [(52, alphabet[i]) for i in range(insertions)]
            + [(53, " "), (54, " ")]
        )
        regions[3] = [(annotations[i], regions[3][i][1]) for i in range(length)]
    else:
        # How to gap L2 in Chothia/Kabat/Martin is unclear so we let the alignment do
        # it.
        regions[3] = regions[3]

    # CDR3
    # Chothia L region 6 (index 5) >>> put insertions onto 95
    length = len(regions[5])
    if length > 36:
        return []  # Too many insertions. Do not apply numbering.

    annotations = get_cdr3_annotations(length, scheme="kabat", chain_type="light")
    regions[5] = [(annotations[i], regions[5][i][1]) for i in range(length)]

    return regions


def martin_light(regions):
    # The Martin and Chothia specification for light chains are very similar. Martin is
    # more explicit in the location of indels but unlike the heavy chain these are
    # additional instead of changes to the Chothia scheme. Thus, Chothia light is
    # implemented as martin light.
    return chothia_light(regions)


# James Dunbar was a genius... How did he do it?
# Heuristic regapping based on the AHo specification as detailed on AAAAA website.
# Gap order depends on the chain type
def aho(regions, chain_type):
    """
    Apply the Aho numbering scheme

    Rules should be implemented using two strings - the state string and the region string.

    There are 128 states in the HMMs. Treat X as a direct match in IMGT scheme, I is an insertion. (All X's for IMGT)

    XXXXXXX XXX XXXXXXXXXXXXXX XXXXXXXXXXXXXXXX XXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXX XXXXXXXXXXXXX XXXXXXXXXXXXX XXXXXXXXXXX
    AAAAAAA BBB CCCCCCCCCCCCCC DDDDDDDDDDDDDDDD EEEEEEEEEEEEEEE FFFFFFFFFFFFFFFFFFFF HHHHHHHHHHHHHHHH IIIIIIIIIIIII JJJJJJJJJJJJJ KKKKKKKKKKK


    Regions - (N.B These do not match up with any particular definition of CDR)
    A. EMPTY (now included in B)
    B. 1-10 inclusive. Indel occurs at 8
    C. 11-24 inclusive.
    D. 25-42 inclusive (deletion surround 28) 32-42 inclusive (deletions surround 36)
    E. 43-57 inclusive
    F. 58-77 inclusive (deletions surround 63). Alpha chains have deletions at 74,75
    G. EMPTY (now included in H)
    H. 78-93 inclusive  gaps on 86 then 85, insertions on 85 linearly
    I. 94-106 inclusive
    J. 107-138 inclusive gaps on 123 symetrically.
    K. 139-149 inclusive.

    """  # noqa: E501

    ##################################
    # Move the indel in fw 1 onto 8  #
    ##################################
    # Place indels on 8
    # Find the first recognised residue and change the expected length of the stretch
    # given the starting point. This prevents n terminal deletions being placed at 8
    # incorrectly.
    length = len(regions[1])
    if length > 0:
        start = regions[1][0][0][0]
        stretch_len = 10 - (start - 1)
        if length > stretch_len:  # Insertions are present. Place on 8
            annotations = (
                [(_, " ") for _ in range(start, 9)]
                + [(8, alphabet[_]) for _ in range(length - stretch_len)]
                + [(9, " "), (10, " ")]
            )
        else:
            ordered_deletions = [(8, " ")] + [
                (_, " ") for _ in range(start, 11) if _ != 8
            ]
            annotations = sorted(ordered_deletions[max(stretch_len - length, 0) :])
        regions[1] = [(annotations[i], regions[1][i][1]) for i in range(length)]

    #########
    # CDR 1 # - divided in two parts in the Aho scheme.
    ######### - gaps at 28 depending on the chain type.

    # "VH domains, as well as the majority of the VA domains, have a one-residue gap in
    # position 28, VK and VB domains a two-residue gap in position 27 and 28."

    # We use the link below as the reference for the scheme.
    # https://www.bioc.uzh.ch/plueckthun/antibody/Numbering/Alignment.html

    # Some of the header lines in these images are offset by one (VH)! The gaps really
    # are centered at 28 and 36
    # https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VK.html
    # https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VL.html
    # https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VH.html
    # https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VA.html
    # https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VB.html
    # https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VG.html
    # https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VD.html

    # We gap the CDR1 in a heuristic way using the gaps.

    # This means that CDR1 gapping will not always be correct. For example if one grafts
    # a Kappa CDR1 loop onto a Lambda framework the gapping patter might now be
    # incorrect. Not a fan of being so prescriptive.

    # The CDR1 region included here ranges from AHo 25 to AHo 42 inclusive

    # The order in which the two loops are gapped is dependent on the chain type (see
    # alignments in URLs above). Not all lengths are defined as not all lengths were
    # crystallised in 2001 (or today). Where no example of the length was available the
    # rule followed is to continue gapping the C terminal 'loop', then the N terminal
    # 'loop', then 31 then the fw. In all cases I have commented where the gapping is
    # undefined. Note that for alpha chains the gapping rules are inconsistent.

    _L = 28, 36, 35, 37, 34, 38, 27, 29, 33, 39, 32, 40, 26, 30, 25, 31, 41, 42
    #  |-> undefined by AHo. Gapping C terminal loop then N terminal then 31, then fw.

    _K = 28, 27, 36, 35, 37, 34, 38, 33, 39, 32, 40, 29, 26, 30, 25, 31, 41, 42
    #  |-> undefined by AHo. Gapping C terminal loop then N terminal then fw.

    _H = 28, 36, 35, 37, 34, 38, 27, 33, 39, 32, 40, 29, 26, 30, 25, 31, 41, 42
    #  |-> undefined by AHo. Gapping C terminal loop then N terminal then fw.
    #  N.B. The header on the alignment image for PDB_VH is offset by 1!

    _A = 28, 36, 35, 37, 34, 38, 33, 39, 27, 32, 40, 29, 26, 30, 25, 31, 41, 42
    # |-> undefined by AHo. Gapping C terminal loop then N terminal then fw.
    # N.B The gapping is inconsistent for alpha chains.
    # I follow the paper's statement that most VA have one gap at 28 and remove 28 and
    # 27 before removing 40.

    _B = 28, 36, 35, 37, 34, 38, 33, 39, 27, 32, 40, 29, 26, 30, 25, 31, 41, 42
    # |-> undefined by AHo. Gapping C terminal loop then N terminal then 31, then fw.

    _D = 28, 36, 35, 37, 34, 38, 27, 33, 39, 32, 40, 29, 26, 30, 25, 31, 41, 42
    # |-> undefined by AHo. Gapping C terminal loop then N terminal then 31, then fw.
    # N.B only two sequence patterns available.
    _G = 28, 36, 35, 37, 34, 38, 27, 33, 39, 32, 40, 29, 26, 30, 25, 31, 41, 42
    # |-> undefined by AHo. Gapping C terminal loop then N terminal then 31, then fw.
    # N.B only one sequence patterns available. Delta copied.

    ordered_deletions = {"L": _L, "K": _K, "H": _H, "A": _A, "B": _B, "D": _D, "G": _G}

    length = len(regions[3])

    annotations = [
        (i, " ") for i in sorted(ordered_deletions[chain_type][max(18 - length, 0) :])
    ]

    # Insertions are not described in the AHo scheme but must be included as there is a
    # significant number of CDRH1s that are longer than the number of positions.
    insertions = max(length - 18, 0)
    if insertions > 26:
        return []  # Too many insertions. Do not apply numbering.

    elif insertions > 0:
        # They are placed on residue 36 alphabetically.
        insertat = annotations.index((36, " ")) + 1  # Always 12

        if insertat != 12:
            exit("AHo numbering failed.")
        annotations = (
            annotations[:insertat]
            + [(36, alphabet[a]) for a in range(insertions)]
            + annotations[insertat:]
        )

    regions[3] = [(annotations[i], regions[3][i][1]) for i in range(length)]

    #########
    # CDR 2 #
    #########
    # Gaps are placed symetically at 63.
    # For VA a second gap is placed at 74 and 75 according to the text in the paper.
    # However, all the reference sequences show a gap at 73 and 74 see:
    #      https://www.bioc.uzh.ch/plueckthun/antibody/Sequences/Rearranged/PDB_VA.html
    # and
    #      https://www.bioc.uzh.ch/plueckthun/antibody/Numbering/Alignment.html
    # Either I am mis-interpreting the text in the paper or there is something a little
    # inconsistent here...
    # Given that *all* the numbered examples show the VA gap at 73 and 74 on the AAAAA
    # website I have decided to implement this.
    #

    # This region describes 58 to 77 inclusive
    ordered_deletions = [
        63,
        62,
        64,
        61,
        65,
        60,
        66,
        59,
        67,
        58,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        77,
    ]
    length = len(regions[5])

    annotations = [(i, " ") for i in sorted(ordered_deletions[max(20 - length, 0) :])]

    # Insertions are not described in the AHo scheme but must be included.
    insertions = max(length - 20, 0)
    if insertions > 26:
        return []  # Too many insertions. Do not apply numbering.
    elif insertions > 0:
        # They are placed on residue 63 alphabetically.
        insertat = annotations.index((63, " ")) + 1  # Always 6
        if insertat != 6:
            exit("AHo numbering failed.")
        annotations = (
            annotations[:insertat]
            + [(63, alphabet[a]) for a in range(insertions)]
            + annotations[insertat:]
        )

    regions[5] = [(annotations[i], regions[5][i][1]) for i in range(length)]

    #########
    # FW3   ############################################
    # Move deletions onto 86 then 85. Insertions on 85 #
    ####################################################
    ordered_deletions = [86, 85, 87, 84, 88, 83, 89, 82, 90, 81, 91, 80, 92, 79, 93, 78]
    length = len(regions[7])

    annotations = [(i, " ") for i in sorted(ordered_deletions[max(16 - length, 0) :])]

    # Insertions are not described in the AHo scheme but must be included.
    insertions = max(length - 16, 0)
    if insertions > 26:
        return []  # Too many insertions. Do not apply numbering.
    elif insertions > 0:
        # They are placed on residue 85 alphabetically.
        insertat = annotations.index((85, " ")) + 1  # Always 8
        if insertat != 8:
            exit("AHo numbering failed.")
        annotations = (
            annotations[:insertat]
            + [(85, alphabet[a]) for a in range(insertions)]
            + annotations[insertat:]
        )

    regions[7] = [(annotations[i], regions[7][i][1]) for i in range(length)]

    #########
    # CDR 3 #
    #########
    # Deletions on 123. >>> Point of the Aho scheme is that they have accounted for all
    # possible positions.
    # Assumption is that no more insertions will occur....
    # We'll put insertions on 123 linearly.(i.e.ABCDEF...) if they ever do.

    ordered_deletions = [
        123,
        124,
        122,
        125,
        121,
        126,
        120,
        127,
        119,
        128,
        118,
        129,
        117,
        130,
        116,
        131,
        115,
        132,
        114,
        133,
        113,
        134,
        112,
        135,
        111,
        136,
        110,
        137,
        109,
        138,
        108,
        107,
    ]
    length = len(regions[9])

    annotations = [(i, " ") for i in sorted(ordered_deletions[max(32 - length, 0) :])]

    # Insertions are not described in the AHo scheme but must be included.
    insertions = max(length - 32, 0)
    if insertions > 26:
        return []  # Too many insertions. Do not apply numbering.
    elif insertions > 0:
        # They are placed on residue 123 alphabetically.
        insertat = annotations.index((123, " ")) + 1  # Always 17
        if insertat != 17:
            exit("AHo numbering failed.")
        annotations = (
            annotations[:insertat]
            + [(123, alphabet[a]) for a in range(insertions)]
            + annotations[insertat:]
        )

    regions[9] = [(annotations[i], regions[9][i][1]) for i in range(length)]

    return regions


# Dict to call by string
function_dict = {
    "kabat_heavy": kabat_heavy,
    "kabat_light": kabat_light,
    "martin_heavy": martin_heavy,
    "martin_light": martin_light,
    "chothia_heavy": chothia_heavy,
    "chothia_light": chothia_light,
    "aho_heavy": aho,
    "aho_light": aho,
}
