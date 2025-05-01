import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema

#from analysis_tools.cuts import skim_ele, skim_muon, skim_lpte
from analysis_tools.ntupilizer.skim import skim_all



import hist
import dask
import hist.dask as dah


class TestProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):

        ntuple = skim_all(events)
        
        output = {  
            "ntuple": ntuple,
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass

