# -*- coding: utf-8 -*-
import warnings
from sfeprapy.mc0.mc0 import main

if __name__ == '__main__':
    path_input_csv = None
    warnings.filterwarnings('ignore')
    main(path_input_csv)