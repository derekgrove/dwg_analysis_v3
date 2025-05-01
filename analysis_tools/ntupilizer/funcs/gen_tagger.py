# Define our skims or (categories) for Electrons, Muons, LowPtElectrons
import json
from analysis_tools.ntupilizer.funcs.lep_cuts import *

# This tagger is only to be used on MC files that have gen info, won't work on data

####################################################################
# functions that take the lepton collections, add what type of gen it was to the collection, thats it.

def tag_gen_flags(obj, signal_func): #signal function is from lep_cuts, either 'ele_gen', 'lpte_gen', or 'muon_gen'
    
    """Add isSignal, isLightFake, isHeavyFake to a lepton object."""
    
    signal_mask = primary_mask(obj) & signal_func(obj)
    lfake_mask = light_fake_mask(obj)
    hfake_mask = heavy_fake_mask(obj)

    obj = ak.with_field(obj, signal_mask, "isSignal")
    obj = ak.with_field(obj, lfake_mask, "isLightFake")
    obj = ak.with_field(obj, hfake_mask, "isHeavyFake")
    
    return obj
