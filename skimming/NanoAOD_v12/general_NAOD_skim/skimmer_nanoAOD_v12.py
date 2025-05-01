import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema

path_to_tools = '/home/cms-jovyan/dwg_analysis_v3/tools/'
import sys
sys.path.insert(1, path_to_tools)

#from analysis_tools.skimming.naod_v12.lepton_skim import skim_ele


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


        # Default NanoAODv12 variables, easiest to add to the ntuple
        # Just add variable to the below list of the appropriate collection
        
        event_variables = ["MET"]
        
        ele_variables = ["pt", "eta", "phi", "mass", "sip3d", "dxy", "dz"]
        
        muon_variables = ["pt", "eta", "phi", "mass", "sip3d", "dxy", "dz"]
        
        lpte_variables = ["pt", "eta", "phi", "mass", "ID", "dxy", "dz"]


        my_events = {var: getattr(events, var) for var in event_variables}
        
        my_electrons = {var: getattr(ele, var) for var in ele_variables}
        
        my_muons = {var: getattr(muon, var) for var in muon_variables}
        
        my_lptes = {var: getattr(lpte, var) for var in lpte_variables}
                  
        #Custom variables, not that hard to add but each one is specific
        
        ntuple = {
            "event_count": total_entries,
            "dataset": dataset,
            "Events": my_events,
            "Electron": my_electrons,
            "Muon": my_muons,
            "LowPtElectrons": my_lptes,
        }

        #ak.to_parquet(ntuple, "test_nutple.parquet")
        
        output = {
            "ntuple": ntuple,
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass