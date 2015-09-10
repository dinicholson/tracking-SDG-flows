__author__ = 'vinayvijayan'

import pandas
import time
from preprocess_crosswalk import PreProcessCrosswalk


class BuildCwMap(object):
    def __init__(self, data_set_filepath):
        df_whole_data = pandas.read_csv(data_set_filepath, encoding='utf-8', sep=',')

        for each_sdg in range(1,18):
            df_whole_data['Goal '+str(each_sdg)] = ''
        codemap = self.getCodeMap()
        list_indices = []
        for index, row in df_whole_data.iterrows():
            if index % 10000 == 0:
                print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ' Row number in output ', index

            commitment_amount = df_whole_data.iloc[index]['commitment_amount_usd_constant']

            try:
                purpose_code = str(int(df_whole_data.iloc[index]['coalesced_purpose_code']))
                map = codemap[purpose_code]
                for each_object in map:
                    df_whole_data.set_value(index, each_object.value, round((each_object.weight * commitment_amount), 2))
                    pass
            except (KeyError, ValueError):
                list_indices.append(index)

        df_dropped = df_whole_data.drop(list_indices)
        df_dropped.to_csv('data/withsplitamtsfinal.csv', encoding='utf-8', sep=',', index=False)

    def getCodeMap(self):
        preprocess_crosswalk_object1 = PreProcessCrosswalk()
        return preprocess_crosswalk_object1.get_dict_posteriors()
if __name__ == '__main__':
    buildmap_object = BuildCwMap('data/shortandthin.csv')