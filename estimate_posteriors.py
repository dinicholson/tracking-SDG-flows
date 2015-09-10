__author__ = 'vinayvijayan'

import pandas
from node_value_weight import NodeValueWeight
import copy

class EstimatePosteriors:

    def __init__(self, dict_priors):
        self.dict_priors = dict_priors
        self.dict_posteriors = {}

        for each_sdg in self.dict_priors:
            self._create_posteriors(each_sdg, copy.copy(self.dict_priors[each_sdg]))

    def _create_posteriors(self, sdg_value, list_nodes):
        for each_node in list_nodes:
            child_node = NodeValueWeight(sdg_value, self._get_posterior_prob(sdg_value, each_node.value))
            if each_node.value not in self.dict_posteriors:
                self.dict_posteriors[each_node.value] = [child_node]
            else:
                self.dict_posteriors[each_node.value].append(child_node)

    def _get_posterior_prob(self, sdg_value, pc_value):
        denominator_list = [self._get_prior_prob(each_sdg_value, pc_value) for each_sdg_value in self.dict_priors]
        denominator_list = filter(None, denominator_list)
        posterior_prob = self._get_prior_prob(sdg_value, pc_value)/sum(denominator_list)
        return posterior_prob

    def _get_prior_prob(self, sdg_value, pc_value):
        list_nodes = self.dict_priors[sdg_value]
        for each_node in list_nodes:
            if each_node.value == pc_value:
                return each_node.weight

    def get_posteriors(self):
        return self.dict_posteriors