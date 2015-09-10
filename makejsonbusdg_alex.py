
__author__ = 'vinayvijayan'

from  makejsonbydonor import MakeJsonByDonor
import pandas
import collections
import json
import numpy
import copy

class MakeJsonBySDG(MakeJsonByDonor):
    def __init__(self, data_set_filepath):

        df_whole_data = pandas.read_csv(data_set_filepath, encoding='utf-8', sep=',')
        list_goals = ['Goal ' + str(x) for x in range(1,18)]
        df_trimmed = df_whole_data[['donor', 'recipient_iso3', 'year'] + list_goals]

        summed_df = df_trimmed.groupby(['donor', 'recipient_iso3', 'year']).sum()
        dict_each_sdg = {}

        #initialize the dict containing lists of
        for each_sdg in range(1, 18):
            dict_each_sdg['sdg' + str(each_sdg)] = {}

        for each_index in list(summed_df.index.values):
            list_index = list(each_index)
            count = 0
            for each_amount in list(summed_df.loc[each_index]):
                count += 1
                list_index_modified = list_index[:]
                if each_amount is not numpy.isnan and each_amount > 1:
                    list_index_modified.insert(0, 'sdg'+str(count))
                    list_index_modified.append(int(round(each_amount)))
                    dict_each_sdg['sdg' + str(count)] = self._deep_update(dict_each_sdg['sdg' + str(count)],
                                                                 self._convert_index_to_dict(list_index_modified))
        dict_each_sdg_copy = {}
        for each_tree in dict_each_sdg:
            if bool(dict_each_sdg[each_tree]):
                dict_each_sdg_copy[each_tree] = dict_each_sdg[each_tree][each_tree]

        with open('data/json_output_sdg_alex.json', 'w') as outfile:
            json.dump(dict_each_sdg_copy, outfile)
        outfile.close()

if __name__ == '__main__':
    makejson_object = MakeJsonBySDG('data/withsplitamtsfinal.csv')

