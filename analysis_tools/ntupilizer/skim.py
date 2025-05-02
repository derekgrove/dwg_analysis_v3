# Define our skims or (categories) for Electrons, Muons, LowPtElectrons
from analysis_tools.paths import get_config_path
import json

from analysis_tools.ntupilizer.funcs import *

import awkward as ak

json_path = get_config_path("skim_variables.json")

with open(json_path, 'r') as f:
    skim_config = json.load(f)


###########################################################################
# skim objects (defined in skim_variables.json), save leps that are baseline and some variables
# also flatten the awkward arrays but KEEP the event info as awk_info array


def skim_obj(obj, collection, genInfo=False): #obj must be a collection in skim_variables.json

    skim = {}
    col = skim_config[collection] #for readability, maybe?

    if col["isLep"]: # add lepton quality variables
        if collection == "Electron":
            obj = tag_ele_quality(obj)
        elif collection == "LowPtElectron":
            obj = tag_lpte_quality(obj)
        elif collection == "Muon":
            obj = tag_muon_quality(obj)
            
        obj = obj[obj.isBaseline] #keep ONLY baseline electrons or better

        skim["isGold"] = ak.flatten(obj.isGold)
        skim["isSilver"] = ak.flatten(obj.isSilver)
        skim["isBronze"] = ak.flatten(obj.isBronze)

    
    if genInfo: #gen only stuff, delete for data
        if collection == "Electron":
            obj = tag_gen_flags(obj, ele_gen)
        elif collection == "LowPtElectron":
            obj = tag_gen_flags(obj, lpte_gen)
        elif collection == "Muon":
            obj = tag_gen_flags(obj, muon_gen)
        
        skim["isSignal"] = ak.flatten(obj.isSignal)
        skim["isLightFake"] = ak.flatten(obj.isLightFake)
        skim["isHeavyFake"] = ak.flatten(obj.isHeavyFake)


    # Add event-level counts only for jagged collections
    # This is so we can re-awkward-ify the lists later, get our event
    # info back that way
    
    try:
        skim["awk_info"] = ak.num(obj)
    except Exception:
        skim["awk_info"] = None



    for var in col["variables"]: #flatten all awk variable arrays
        
        field = getattr(obj, var)
        
        try:
            skim[var] = ak.flatten(field)
        
        except Exception:
            skim[var] = field 

    return skim



#now define a recursive function to skim all collections in .json file

def skim_all(events, genInfo=False):
    """
    Skim all collections defined in skim_variables.json from the given events object.
    Returns a dictionary of skimmed collections.
    Format of returned skim is:
    {
        Collection1:
            var1: [awk.arr or flat arr],
            va2: [awk.arr or flat arr],
            ...
        Collection2:
            var1: [awk.arr or flat arr],
            ...    
    }
    """
    ntuple = {}

    for collection in skim_config:
        if collection == "flags": #have this for later updates, idk, maybe we can do something with flags in the json
            continue

        # Check if the collection exists in the event
        if hasattr(events, collection):
            obj = getattr(events, collection)
            ntuple[collection] = skim_obj(obj, collection, genInfo=genInfo)
        else:
            print(f"Warning: Collection '{collection}' not found in events.")

    return ntuple
