# Define our skims or (categories) for Electrons, Muons, LowPtElectrons
import json
from analysis_tools.cuts.lep_cuts import *


####################################################################
# functions that take the lepton collections, checks if the lepton is baseline, gold, etc., adds a boolean to it if so. Thats it.



def tag_ele_quality(ele): #use on raw ele collection

    """
    Add an 'isBaseline', 'isGold', 'isSilver', 'isBronze' field to each Electron based on cuts.
    """
    baseline_mask = (
        pt_selection(ele, 8, 1.4e12) &
        eta_2p5(ele) &
        loose_sip3d(ele) &
        dxy_0p05(ele) &
        dz_0p1(ele) &
        pfRelIso(ele, tight=False) &
        miniIso(ele, tight=False) &
        veto_no_iso_hoe(ele)
    )

    gold_mask = (
        baseline_mask &
        tight_sip3d(ele) &
        pfRelIso(ele, tight=True) &
        miniIso(ele, tight=True) &
        tight_no_iso_hoe(ele)
    )

    silver_mask = (
        baseline_mask &
        ~tight_sip3d(ele) &
        pfRelIso(ele, tight=True) &
        miniIso(ele, tight=True) &
        tight_no_iso_hoe(ele)
    )

    bronze_mask = (
        baseline_mask &
        ~(gold_mask | silver_mask)
    )
    
    # Add new fields: isGold, isSilver, isBronze
    ele = ak.with_field(ele, baseline_mask, "isBaseline")
    ele = ak.with_field(ele, gold_mask, "isGold")
    ele = ak.with_field(ele, silver_mask, "isSilver")
    ele = ak.with_field(ele, bronze_mask, "isBronze")

    ele = tag_ele_gen(ele) #when running on data, remove this line. It is MC only, gen information.

    return ele



def tag_ele_gen(ele): #this is for MC files only, will not work on data

    """
    Add an 'isSignal', 'isLightFake', 'isHeavyFake' field to each Electron based on gen information cuts.
    """
    signal_mask = (
        primary_mask(ele) &
        ele_gen(ele)
    )

    lfake_mask = light_fake_mask(ele)
    hfake_mask = heavy_fake_mask(ele)

    
    
    # Add new fields: isSignal, isLightFake, isHeavyFake
    ele = ak.with_field(ele, signal_mask, "isSignal")
    ele = ak.with_field(ele, lfake_mask, "isLightFake")
    ele = ak.with_field(ele, hfake_mask, "isHeavyFake")

    return ele

####################################################################
# LowPtElectrons


def tag_lpte_quality(lpte): #use on raw lpte collection

    """
    Add an 'isBaseline', 'isGold', 'isSilver', 'isBronze' field to each LowPtElectron based on cuts.
    """
    baseline_mask = (
        pt_selection(lpte, 2, 8) &
        eta_2p5(lpte) &
        loose_sip3d_lpte(lpte) &
        dxy_0p05(lpte) &
        dz_0p1(lpte) &
        miniIso(lpte, tight=False) &
        loose_ID(lpte)
    )

    gold_mask = (
        baseline_mask &
        tight_sip3d_lpte(lpte) &
        miniIso(lpte, tight=True) & 
        central_eta_ID_regions(lpte)
        
    )

    silver_mask = (
        baseline_mask &
        ~tight_sip3d_lpte(lpte) &
        miniIso(lpte, tight=True) &
        central_eta_ID_regions(lpte)
    )

    bronze_mask = (
        baseline_mask &
        ~(gold_mask | silver_mask)
    )
    
    # Add new fields: isGold, isSilver, isBronze
    lpte = ak.with_field(lpte, baseline_mask, "isBaseline")
    lpte = ak.with_field(lpte, gold_mask, "isGold")
    lpte = ak.with_field(lpte, silver_mask, "isSilver")
    lpte = ak.with_field(lpte, bronze_mask, "isBronze")

    lpte = tag_lpte_gen(lpte) #when running on data, remove this line. It is MC only, gen information.

    return lpte



def tag_lpte_gen(lpte): #this is for MC files only, will not work on data

    """
    Add an 'isSignal', 'isLightFake', 'isHeavyFake' field to each LowPtElectron based on gen information cuts.
    """
    signal_mask = (
        primary_mask(lpte) &
        lpte_gen(lpte)
    )

    lfake_mask = light_fake_mask(lpte)
    hfake_mask = heavy_fake_mask(lpte)

    
    
    # Add new fields: isSignal, isLightFake, isHeavyFake
    lpte = ak.with_field(lpte, signal_mask, "isSignal")
    lpte = ak.with_field(lpte, lfake_mask, "isLightFake")
    lpte = ak.with_field(lpte, hfake_mask, "isHeavyFake")

    return lpte

####################################################################
# Muons:

def tag_muon_quality(muon): #use on raw muon collection

    """
    Add an 'isBaseline', 'isGold', 'isSilver', 'isBronze' field to each Muon based on cuts.
    """
    baseline_mask = (
        pt_selection(muon, 3, 1.4e12) &
        eta_2p5(muon) &
        loose_sip3d(muon) &
        dxy_0p05(muon) &
        dz_0p1(muon) &
        pfRelIso(muon, tight=False) &
        miniIso(muon, tight=False)
    )

    gold_mask = (
        baseline_mask &
        tight_sip3d(muon) &
        pfRelIso(muon, tight=True) &
        miniIso(muon, tight=True) &
        muon_tightID(muon)
    )

    silver_mask = (
        baseline_mask &
        ~tight_sip3d(muon) &
        pfRelIso(muon, tight=True) &
        miniIso(muon, tight=True) &
        muon_tightID(muon)
    )

    bronze_mask = (
        baseline_mask &
        ~(gold_mask | silver_mask)
    )
    
    # Add new fields: isGold, isSilver, isBronze
    muon = ak.with_field(muon, baseline_mask, "isBaseline")
    muon = ak.with_field(muon, gold_mask, "isGold")
    muon = ak.with_field(muon, silver_mask, "isSilver")
    muon = ak.with_field(muon, bronze_mask, "isBronze")

    muon = tag_muon_gen(muon) #when running on data, remove this line. It is MC only, gen information.

    return muon



def tag_muon_gen(muon): #this is for MC files only, will not work on data

    """
    Add an 'isSignal', 'isLightFake', 'isHeavyFake' field to each Muon based on gen information cuts.
    """
    signal_mask = (
        primary_mask(muon) &
        muon_gen(muon)
    )

    lfake_mask = light_fake_mask(muon)
    hfake_mask = heavy_fake_mask(muon)

    
    
    # Add new fields: isSignal, isLightFake, isHeavyFake
    muon = ak.with_field(muon, signal_mask, "isSignal")
    muon = ak.with_field(muon, lfake_mask, "isLightFake")
    muon = ak.with_field(muon, hfake_mask, "isHeavyFake")

    return muon