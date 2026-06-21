from operator import itemgetter

a               = '/Users/songweizhi/Desktop/Sponge_r226/11_Functional_enrichment_analysis/functional_enrichment_Nitrosoabyssus_10_arCOG/Nitrosoabyssus_10_arCOG_enriched_in_The_rest_symbionts.txt'
a2              = '/Users/songweizhi/Desktop/Sponge_r226/11_Functional_enrichment_analysis/functional_enrichment_Nitrosoabyssus_10_arCOG/Nitrosoabyssus_10_arCOG_enriched_in_The_rest_symbionts2.txt'
ignore_unknown  = True


def sort_stats_by_diff_value(file_in, file_out, ignore_unknown):

    line_index = 0
    header_line = ''
    diff_na_dict = dict()
    diff_na_list = []
    line_to_diff_dict = dict()
    for each_line in open(file_in):

        if line_index == 0:
            header_line = each_line.strip()
        else:
            each_line_split = each_line.strip().split('\t')
            mean_diff = each_line_split[4]

            to_ignore = False
            if ignore_unknown is True:
                if ('uncharacterized protein' in each_line) or ('Uncharacterized protein' in each_line):
                    to_ignore = True

            if to_ignore is False:
                if mean_diff == 'NA':
                    print(each_line_split)
                    a_b = float(each_line_split[2]) - float(each_line_split[3])
                    a_b = abs(a_b)
                    print(a_b)
                    diff_na_dict[each_line.strip()] = a_b

                    diff_na_list.append(each_line.strip())
                else:
                    line_to_diff_dict[each_line.strip()] = float(mean_diff)
        line_index += 1

    file_out_handle = open(file_out, 'w')
    file_out_handle.write(header_line + '\n')
    for k, v in sorted(line_to_diff_dict.items(), key=itemgetter(1))[::-1]:
        file_out_handle.write(k + '\n')
    for k2, v2 in sorted(diff_na_dict.items(), key=itemgetter(1))[::-1]:
        file_out_handle.write(k2 + '\n')
    file_out_handle.close()


sort_stats_by_diff_value(a, a2, ignore_unknown)
