# Define our skims or (categories) for Electrons, Muons, LowPtElectrons

from . import lepton_cuts


###########################################################################
# Electron skim here
def ele_filters(ele, debug=False):

    signal_mask = (
        signal_mask(ele) &
        ele_gen_mask(ele)
    )

    signal_ele = ele[signal_mask]
    light_fakes = ele[light_fake_mask(ele)]
    heavy_fakes = ele[heavy_fake_mask(ele)]

    if debug:
        print("Signal ele:", ak.sum(ak.num(signal_ele)))
        print("Light fakes:", ak.sum(ak.num(light_fakes)))
        print("Heavy fakes:", ak.sum(ak.num(heavy_fakes)))

    return signal_ele, light_fakes, heavy_fakes


def ele_baseline(f_ele): #use on filtered ele
    # Eventually, when running on data, apply this category directly to the raw electrons, skipping the filtered step since that one is gen variables only

    mask = (
    pt_selection(f_ele, 8, 1.4e12) &
    eta_2p5(f_ele) &
    loose_sip3d(f_ele) &
    dxy_0p05(f_ele) &
    dz_0p1(f_ele) &
    pfRelIso(f_ele, tight=False) &
    miniIso(f_ele, tight=False) &
    veto_no_iso_hoe(f_ele)
    )

    bl_ele = f_ele[mask]
    
    return bl_ele



def ele_gsb(bl_ele): #use on baseline ele

    gold_mask = (
        tight_sip3d(bl_ele) &
        pfRelIso(bl_ele, tight=True) &
        miniIso(bl_ele, tight=True) &
        tight_no_iso_hoe(bl_ele)
    )

    silver_mask = (
        ~tight_sip3d(bl_ele) &
        pfRelIso(bl_ele, tight=True) &
        miniIso(bl_ele, tight=True) &
        tight_no_iso_hoe(bl_ele)
    )

    bronze_mask = (
        ~(gold_mask | silver_mask)
    )

    gold_ele = bl_ele[gold_mask]
    silver_ele = bl_ele[silver_mask]
    bronze_ele = bl_ele[bronze_mask]
    
    return gold_ele, silver_ele, bronze_ele

def skim_ele(ele, debug=False):
    
    skim = {
        "signal": {},
        "light_fakes": {},
        "heavy_fakes": {},
    }
    
    signal_ele, light_fakes, heavy_fakes = ele_filters(ele)

    filtered_map = {
        "signal": signal_ele,
        "light_fakes": light_fakes,
        "heavy_fakes": heavy_fakes,
    }
    
    # first get baseline ele for each filtered category:
    
    for category, filtered_ele in filtered_map.items(): 
        
        baseline = ele_baseline(filtered_ele)
        
        gold, silver, bronze = ele_gsb(baseline)
        
        skim[category]["baseline"] = baseline
        skim[category]["gold"] = gold
        skim[category]["silver"] = silver
        skim[category]["bronze"] = bronze
        
        if debug:
            print(f"{category} baseline ele:", ak.sum(ak.num(baseline)))
            print(f"{category} gold ele:", ak.sum(ak.num(gold)))
            print(f"{category} silver ele:", ak.sum(ak.num(silver)))
            print(f"{category} bronze ele:", ak.sum(ak.num(bronze)))
        
    return skim


###########################################################################
# LowPtElectron skim here

def skim_lpte(lpte):
    
    skim = {
        "signal": {},
        "light_fakes": {},
        "heavy_fakes": {},
    }

    return skim


###########################################################################
# Muon skim here


def skim_muon(muon):
    
    skim = {
        "signal": {},
        "light_fakes": {},
        "heavy_fakes": {},
    }

    return skim



