import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema

path_to_tools = '/home/cms-jovyan/dwg_analysis_v3/tools/'
import sys
sys.path.insert(1, path_to_tools)

from analysis_tools.skimming.naod_v12.lepton_skim import skim_ele


# my tools:
# from analysis_tools.skimming.parent_filter import prim_ele

# from analysis_tools.skimming.signal_filter import (
#    signal_filter_cut, parent_mask
# )

import hist
import dask
import hist.dask as dah


class TestProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        total_entries = ak.num(events, axis=0)

        ele = events.Electron
        
        skim_ele(ele)

        
        output = {
            "keys": skim_ele.keys(),
            "items": skim_ele.items(),
            
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
