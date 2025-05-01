# Define our skims or (categories) for Electrons, Muons, LowPtElectrons

import json
from analysis_tools.cuts.lep_cuts import *
from analysis_tools.cuts.lep_tagger import *

json_path = "/home/cms-jovyan/dwg_analysis_v3/analysis_tools/cuts/skim_variables.json"
with open(json_path, 'r') as f:
    lep_var = json.load(f)


###########################################################################
# Electron skim here


def skim_ele(ele):
    
    skim = {}
    
    ele = tag_ele_quality(ele)

    ele = ele[ele.isBaseline] #keep ONLY baseline electrons or better
    
    for var in lep_var["electron_variables"]:
        skim[var] = getattr(ele, var)

    skim["isGold"] = ele.isGold
    skim["isSilver"] = ele.isSilver
    skim["isBronze"] = ele.isBronze

    #gen only stuff, delete for data
    
    skim["isSignal"] = ele.isSignal
    skim["isLightFake"] = ele.isLightFake
    skim["isHeavyFake"] = ele.isHeavyFake


    return skim

###########################################################################
# LowPtElectron skim here

def skim_lpte(lpte):
    
    skim = {}
    
    lpte = tag_lpte_quality(lpte)

    lpte = lpte[lpte.isBaseline] #keep ONLY baseline electrons or better
    
    for var in lep_var["lpte_variables"]:
        skim[var] = getattr(lpte, var)
        
    skim["isBaseline"] = lpte.isBaseline
    skim["isGold"] = lpte.isGold
    skim["isSilver"] = lpte.isSilver
    skim["isBronze"] = lpte.isBronze

    #gen only stuff, delete for data
    
    skim["isSignal"] = lpte.isSignal
    skim["isLightFake"] = lpte.isLightFake
    skim["isHeavyFake"] = lpte.isHeavyFake


    return skim


###########################################################################
# Muon skim here


def skim_muon(muon):
    
    skim = {}
    
    muon = tag_muon_quality(muon)

    muon = muon[muon.isBaseline] #keep ONLY baseline electrons or better
    
    for var in lep_var["muon_variables"]:
        skim[var] = getattr(muon, var)

    skim["isGold"] = muon.isGold
    skim["isSilver"] = muon.isSilver
    skim["isBronze"] = muon.isBronze

    #gen only stuff, delete for data
    
    skim["isSignal"] = muon.isSignal
    skim["isLightFake"] = muon.isLightFake
    skim["isHeavyFake"] = muon.isHeavyFake


    return skim




