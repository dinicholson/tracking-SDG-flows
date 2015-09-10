__author__ = 'vinayvijayan'
import pandas
import math
import copy
from os import listdir
from os.path import join
from node_value_weight import NodeValueWeight
from estimate_posteriors import EstimatePosteriors

dir_path = 'data/SDG_Codes'

class PreProcessCrosswalk(object):

    def __init__(self):
        list_filenames = [f for f in listdir(dir_path) if f.endswith('.csv')]
        self.dict_cum_posteriors = {}
        for each_filename in list_filenames:
            print each_filename

            df_whole_data = pandas.read_csv(join(dir_path, each_filename), encoding='utf-8', sep=',')
            df_grouped = df_whole_data.groupby('Goal_Num')
            dict_count_pc = {}
            dict_priors = {}

            for each_group in df_grouped.groups:
                dict_count_pc[each_group] = {}
                list_pc = [str(df_whole_data.ix[index][col])[0:5] for index in df_grouped.groups[each_group] for col in range (4,9) if
                           not math.isnan(df_whole_data.ix[index][col])]

                for each_pc in list_pc:
                    if each_pc in dict_count_pc[each_group]:
                        dict_count_pc[each_group][each_pc] += 1
                    else:
                        dict_count_pc[each_group][each_pc] = 1

                for each_pc in dict_count_pc[each_group]:
                    dict_count_pc[each_group][each_pc] = dict_count_pc[each_group][each_pc]/float(len(list_pc))

            for each_group in dict_count_pc:
                dict_priors[each_group] = []
                for each_pc in dict_count_pc[each_group]:
                    x = NodeValueWeight(each_pc, dict_count_pc[each_group][each_pc])
                    dict_priors[each_group].append(x)
            estimate_posteriors_object1 = EstimatePosteriors(dict_priors)
            dict_posteriors = estimate_posteriors_object1.get_posteriors()

            for each_pc in dict_posteriors:
                    if each_pc in self.dict_cum_posteriors:
                        for each_object in dict_posteriors[each_pc]:
                            self.dict_cum_posteriors[each_pc] = self._check_if_available(each_object, copy.copy(self.dict_cum_posteriors[each_pc]))
                    else:
                        self.dict_cum_posteriors[each_pc] = dict_posteriors[each_pc]

        for each_pc in self.dict_cum_posteriors:
            self.dict_cum_posteriors[each_pc] = self._normalize(copy.copy(self.dict_cum_posteriors[each_pc]))

        # for each_pc in dict_cum_posteriors:
        #     list_sdg = dict_cum_posteriors[each_pc]
        #     sum_value = sum([float(each_sdg.weight) for each_sdg in list_sdg])
        #     print each_pc
        #     print [each_sdg.value for each_sdg in list_sdg]

    def _check_if_available(self,object, list_of_objects):
        for each_object in list_of_objects:
            if each_object.value == object.value:
                each_object.weight = float(each_object.weight) + float(object.weight)
                return list_of_objects
        list_of_objects.append(object)
        return list_of_objects

    def _normalize(self, list_of_objects):
        sum_weights = sum([each_object.weight for each_object in list_of_objects])
        for each_object in list_of_objects:
            each_object.weight = each_object.weight/sum_weights
        return list_of_objects

    def get_dict_posteriors(self):
        return self.dict_cum_posteriors
