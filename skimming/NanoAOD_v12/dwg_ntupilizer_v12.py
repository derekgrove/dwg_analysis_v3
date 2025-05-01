import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema
import json

from analysis_tools.cuts import skim_ele
#import analysis_tools
#print(analysis_tools.__file__)


from analysis_tools.cuts.lepton_skim import skim_ele


# my tools:
# from analysis_tools.skimming.parent_filter import prim_ele

# from analysis_tools.skimming.signal_filter import (
#    signal_filter_cut, parent_mask
# )

import hist
import dask
import hist.dask as dah


class SkimNanoAODv12(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        total_entries = ak.num(events, axis=0)

        ele = events.Electron
        muon = events.Muon
        lpte = events.LowPtElectron

        print(dataset)

        
        with open("lep_variables.json", "r") as f:
            lep_variables = json.load(f)
        
        event_variables = ["MET"]

        
        skim_electrons = skim_ele(ele)
        #skim_muons = skim_muon(muon)
        #skim_lpte = skim_lpte(lpte)


        my_events = {var: getattr(events, var) for var in event_variables}

        my_electrons = {}

        for category, quality_dict in skim_electrons.items():
            my_electrons[category] = {}  # initialize sub-dictionary

            for quality, dawk_array in quality_dict.items():
                my_electrons[category][quality] = dawk_array


            
        #my_muons = {var: getattr(muon, var) for var in muon_variables}
        
        #my_lptes = {var: getattr(lpte, var) for var in lpte_variables}
                  
        
        ntuple = {
            "event_count": total_entries,
            "dataset": dataset,
            "Events": my_events,
            "Electron": my_electrons,
            #"Muon": my_muons,
            #"LowPtElectrons": my_lptes,
        }

        #ak.to_parquet(ntuple, "test_nutple.parquet")
        
        output = {
            "ntuple": ntuple,
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
