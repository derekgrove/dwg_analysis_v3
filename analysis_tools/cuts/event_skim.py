# Define our skims or (categories) for Electrons, Muons, LowPtElectrons

import json

json_path = "/home/cms-jovyan/dwg_analysis_v3/analysis_tools/cuts/skim_variables.json"
with open(json_path, 'r') as f:
    lep_var = json.load(f)


###########################################################################
# Electron skim here


def skim_events(events):
    
    skim = {}

    for var in lep_var["event_variables"]:
        skim[var] = getattr(events, var)

    return skim





