import os
import pandas as pd


def get_shared_uniq_elements(list_1, list_2):

    shared_set = set(list_1).intersection(list_2)

    list_1_uniq = []
    for e1 in list_1:
        if e1 not in shared_set:
            list_1_uniq.append(e1)
    list_2_uniq = []
    for e2 in list_2:
        if e2 not in shared_set:
            list_2_uniq.append(e2)

    return shared_set, list_1_uniq, list_2_uniq


def subset_df(file_in, file_out, cols_to_keep_set):

    column_name_pos = 0
    row_name_pos    = 0
    sep_symbol      = '\t'

    ###################################### get the id of rows and cols to subset #######################################

    # put all row and col headers in list
    df = pd.read_csv(file_in, sep=sep_symbol, header=column_name_pos, index_col=row_name_pos)

    ####################################################################################################################

    # turn sets into lists
    rows_to_keep_list_sorted = set()
    cols_to_keep_list_sorted = sorted(list(cols_to_keep_set))

    if len(rows_to_keep_list_sorted) == 0:
        if len(cols_to_keep_list_sorted) == 0:
            subset_df = df.loc[:, :]
        else:
            subset_df = df.loc[:, cols_to_keep_list_sorted]
    else:
        if len(cols_to_keep_list_sorted) == 0:
            subset_df = df.loc[rows_to_keep_list_sorted, :]
        else:
            subset_df = df.loc[rows_to_keep_list_sorted, cols_to_keep_list_sorted]

    subset_df.to_csv(file_out, sep=sep_symbol)


def rarefaction(otu_table_txt, sample_group_txt, color_code_txt, op_prefix, op_dir):

    default_color = '#999999'

    # get path to rarefaction_R
    pwd_current_file  = os.path.realpath(__file__)
    current_file_path = '/'.join(pwd_current_file.split('/')[:-1])
    rarefaction_R     = '%s/rarefaction.R' % current_file_path
    if os.path.isfile(rarefaction_R) is False:
        print('rarefaction.R not found, program exited!')
        exit()

    # define file name
    otu_table_subset = '%s/%s_otu_table_subset.txt' % (op_dir, op_prefix)
    group_color_txt  = '%s/%s_color.txt'            % (op_dir, op_prefix)
    output_plot      = '%s/%s_rarefaction.pdf'      % (op_dir, op_prefix)

    otu_table_sample_list = open(otu_table_txt).readline().strip().split('\t')[1:]

    # get interested_sample_set
    interested_sample_set = set()
    for each_sample in open(sample_group_txt):
        interested_sample_set.add(each_sample.strip().split()[0])

    shared_sample_set, uniq_to_otu_table, uniq_to_interested = get_shared_uniq_elements(otu_table_sample_list, interested_sample_set)

    # subset OTU table
    otu_table_to_plot = otu_table_txt
    if len(shared_sample_set) < len(otu_table_sample_list):
        subset_df(otu_table_txt, otu_table_subset, shared_sample_set)
        otu_table_to_plot = otu_table_subset

    group_set = set()
    for each_sample in open(sample_group_txt):
        group_set.add(each_sample.strip().split()[1])

    color_code_dict = dict()
    for each_sample_type in open(color_code_txt):
        sample_type_split = each_sample_type.strip().split('\t')
        sample_type = sample_type_split[0]
        sample_color = sample_type_split[1]
        color_code_dict[sample_type] = sample_color

    group_color_txt_handle = open(group_color_txt, 'w')
    group_color_txt_handle.write('GroupID\tGroupColor\n')
    for grp in sorted(list(group_set)):
        grp_color = color_code_dict.get(grp, default_color)
        group_color_txt_handle.write('%s\t%s\n' % (grp, grp_color))
    group_color_txt_handle.close()

    rarefaction_cmd = 'Rscript %s -i %s -g %s -c %s -o %s' % (rarefaction_R, otu_table_to_plot, sample_group_txt, group_color_txt, output_plot)
    print(rarefaction_cmd)
    os.system(rarefaction_cmd)
    print('Done')


########################################################################################################################

# file in
otu_table_txt           = 'ASV_Table.txt'
color_code_sample_txt   = 'group_color_code.txt'
sample_group_txt        = 'sample_group.txt'

# file out
op_dir                  = 'output_folder'
op_prefix               = 'Coral_Water_Sediment'

########################################################################################################################

rarefaction(otu_table_txt, sample_group_txt, color_code_sample_txt, op_prefix, op_dir)
