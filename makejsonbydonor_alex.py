__author__ = 'vinayvijayan'
import pandas
import collections
import json
import numpy

class MakeJsonByDonor(object):

    def __init__(self, data_set_filepath):
        df_whole_data = pandas.read_csv(data_set_filepath, encoding='utf-8', sep=',')
        list_goals = ['Goal ' + str(x) for x in range(1, 18)]
        df_trimmed = df_whole_data[['donor', 'recipient', 'year'] + list_goals]

        summed_df = df_trimmed.groupby(['donor', 'recipient', 'year']).sum()
        cumulative_tree = {}
        for each_index in list(summed_df.index.values):
            list_index = list(each_index)
            dict_sdg_amounts = self._convert_sdg_amount_list_to_dict(list(summed_df.loc[each_index]))
            list_index.append(dict_sdg_amounts)
            tree = self._convert_index_to_dict(list_index)
            tree = {'root': tree}
            cumulative_tree = self._deep_update(cumulative_tree, tree)

        with open('data/json_output_donor_alex.json', 'w') as outfile:
            json.dump(cumulative_tree['root'], outfile)
        outfile.close()

    def _convert_index_to_dict(self, index):
        def inner_convert_index_to_dict(list_index):
            dict_index = {}
            if len(list_index) == 1:
                return list_index[0]
            else:
                dict_index[list_index[0]] = inner_convert_index_to_dict(list_index[1:])
                return dict_index
        dict_index = inner_convert_index_to_dict(index)
        return dict_index

    def _convert_sdg_amount_list_to_dict(self, amount_list):
        dict_sdg = {}
        counter = 0
        for each_value in amount_list:
            counter+=1
            try:
                if each_value is not numpy.isnan and each_value > 1:
                    # dict_sdg['Goal '+str(counter)] = int(round(each_value))
                    dict_sdg['sdg'+str(counter)] = int(round(each_value))
            except ValueError:
                print amount_list
        return dict_sdg

    def _deep_update(self, source, overrides):
        for key, value in overrides.iteritems():
            if isinstance(value, collections.Mapping) and value:
                returned = self._deep_update(source.get(key, {}), value)
                source[key] = returned
            else:
                source[key] = overrides[key]
        return source

if __name__ == '__main__':
    makejson_object = MakeJsonByDonor('data/withsplitamtsfinal.csv')


