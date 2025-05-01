import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema

#from analysis_tools.cuts import skim_ele, skim_muon, skim_lpte
from analysis_tools.cuts.KU_ntupilizer import make_ntuple


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
        total_entries = len(events)

        ele = events.Electron
        muon = events.Muon
        lpte = events.LowPtElectron

        lpte_pt = lpte.pt

        #print(events.fields)
        #print(events.MET)
        #print(events.MET.fields)
        #print(events.Flag.METFilters)

        #my_electrons = skim_ele(ele)
        #my_events = events.MET
        #my_muons = skim_muons(muon)
        #my_lpte = skim_lpte(lpte)
        
        
        #ntuple = {
        #    "numEvents": total_entries,
        #    "dataset": dataset,
        #    "Electron": my_electrons,
        #    "Muon": my_muons,
        #}
        ntuple = make_ntuple(events, ele, muon, lpte)
        
        output = {
            "ntuple": ntuple,
            "events.Flag.METFilters": events.Flag.METFilters,
            "lpte_pt": lpte_pt,
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass

