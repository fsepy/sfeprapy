# -*- coding: utf-8 -*-

from sfeprapy.mcs.mcs_gen import _test_dict_flatten as test_mcs_gen_dict_flatten
from sfeprapy.mcs.mcs_gen import _test_random_variable_generator as test_mcs_gen_random_variable_generator
from sfeprapy.mcs.mcs_gen_2 import TestInputParser

test_mcs_gen_dict_flatten()
test_mcs_gen_random_variable_generator()
TestInputParser()