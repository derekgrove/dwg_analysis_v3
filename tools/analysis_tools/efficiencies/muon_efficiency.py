import awkward as ak
import hist.dask as dah
import numpy as np


# file works assuming skim_muon is of dictionary shape defined in the function skim_muon_signal:


# from analysis_tools.skimming.muon_skim import skim_muon_signal
# skim_muon = skim_muon_signal(muon)





def get_variables(skim_muon):

    variables = { #should be whatever variables are needed for our eff calculations
        'pt': {},
        'eta': {},
        'softMva': {},
        'pfRelIso_3': {},
        'pfRelIso_4': {},
        'miniIso': {},
        'SIP3D': {},
    } 
    
    
    for name, muon_col in skim_muon.items():
        #print(name)
        #print(muon_col)

        
        variables['pt'][name] = ak.flatten(muon_col.pt)
        variables['eta'][name] = ak.flatten(muon_col.eta)
        variables['softMva'][name] = ak.flatten(muon_col.softMva)
        variables['pfRelIso_3'][name] = ak.flatten(muon_col.pfRelIso03_all)
        variables['pfRelIso_4'][name] = ak.flatten(muon_col.pfRelIso04_all)
        variables['miniIso'][name] = ak.flatten(muon_col.miniPFRelIso_all)
        variables['SIP3D'][name] = ak.flatten(muon_col.sip3d)

        
        
        #can add more variables here, just be sure to modify above dictionary and following functions

    return variables



# use above function as first step in functions below:

def get_1d_pt_hist(muon_pt, name="default"):

    hist = dah.Hist.new.Regular(97, 3, 100, name=f"{name} muon $p_T$").Double()

    hist.fill(muon_pt)
    
    return hist



def get_1d_eta_hist(muon_eta, name="default"):

    hist = dah.Hist.new.Regular(50, -2.5, 2.5, name=f"{name} muon η").Double()
    
    hist.fill(muon_eta)
    
    return hist



def get_1d_softMva_hist(muon_softMVA, name="default"):

    hist = dah.Hist.new.Regular(20, 0, 1, name=f"{name} muon softMVA").Double()
    
    hist.fill(muon_softMVA)
    
    return hist

    

def get_1d_pfRelIso_3_hist(muon_pfRelIso_3, name="default"):

    hist = dah.Hist.new.Regular(50, 0, 5, name=f"{name} muon pfRelIso_3").Double()
    
    hist.fill(muon_pfRelIso_3)
    
    return hist



def get_1d_pfRelIso_4_hist(muon_pfRelIso_4, name="default"):

    hist = dah.Hist.new.Regular(50, 0, 5, name=f"{name} muon pfRelIso_4").Double()
    
    hist.fill(muon_pfRelIso_4)
    
    return hist



def get_1d_miniIso_hist_muon(muon_miniIso, name="default"):

    hist = dah.Hist.new.Regular(50, 0, 5, name=f"{name} muon miniIso").Double()
    
    hist.fill(muon_miniIso)
    
    return hist



def get_1d_sip3d_hist_muon(muon_sip3d, name="default"):

    hist = dah.Hist.new.Regular(50, 0, 8, name=f"{name} muon SIP3D").Double()
    
    hist.fill(muon_sip3d)
    
    return hist



def get_2d_eta_pt_hist(muon_pt, muon_eta, name="default"):


    eta_bins = [-2.5, -1.479, -0.8, 0, 0.8, 1.479, 2.5]
    pt_bins = [ 5, 6, 7, 8, 9, 10,
               11, 12, 13, 14, 15,
               16, 17, 18, 19, 20,
               25, 30, 35, 40, 45,
               50, 55, 60, 65, 70,
               75, 80, 85, 90, 95,
               100]
        #a lot of bins in pt, slice them later after the compute like:
        # hist[:, :10] → selects the first 10 bins in the second axis, i.e. pT
    
    hist = (
        dah.Hist.new
        .Variable(eta_bins, name="eta", label = "Muon η")
        .Variable(pt_bins, name="pt", label = "Muon $p_T$")
        .Double()
        )

    hist.fill(pt=muon_pt, eta=muon_eta)
    
    return hist




def get_hists(skim_muon):
    
    variables = get_variables(skim_muon)
    skim_names = variables['pt'].keys()
    
    histograms = {
        
    'one_d': {
        'pt': {},
        'eta': {},
        'softMva': {},
        'pfRelIso_3': {},
        'pfRelIso_4': {},
        'miniIso': {},
        'SIP3D': {},
    },
        
    'two_d': {
        'pt_eta' : {}
    },
        
    }
    
    for name in skim_names:
    
        muon_pt = variables['pt'][name]
        muon_eta = variables['eta'][name]
        muon_softMva = variables['softMva'][name]
        muon_pfRelIso_3 = variables['pfRelIso_3'][name]
        muon_pfRelIso_4 = variables['pfRelIso_4'][name]
        muon_miniIso = variables['miniIso'][name]
        muon_SIP3D = variables['SIP3D'][name]
    
        
        
        histograms['one_d']['pt'][name] = get_1d_pt_hist(muon_pt, name)
        histograms['one_d']['eta'][name] = get_1d_eta_hist(muon_eta, name)
        histograms['one_d']['softMva'][name] = get_1d_softMva_hist(muon_softMva, name)
        histograms['one_d']['pfRelIso_3'][name] = get_1d_pfRelIso_3_hist(muon_pfRelIso_3, name)
        histograms['one_d']['pfRelIso_4'][name] = get_1d_pfRelIso_4_hist(muon_pfRelIso_4, name)
        histograms['one_d']['miniIso'][name] = get_1d_miniIso_hist_muon(muon_miniIso, name)
        histograms['one_d']['SIP3D'][name] = get_1d_sip3d_hist_muon(muon_SIP3D, name)
        histograms['two_d']['pt_eta'][name] = get_2d_eta_pt_hist(muon_pt, muon_eta, name)
    
    
    
    return histograms



# post .compute() functions:

# have to fill histograms during compute, then afterwards we can use the hists
# in these below functions:


# binomial_error = "$\sigma_{\epsilon} = \sqrt{\frac{\epsilon (1 - \epsilon)}{N_{\text{total}}}}$"

def calc_eff_err(hist_1, hist_2): #hist_2 is the denominator of the efficiency
    
    #print(f"hist_1: {hist_1.values()}")
    #print(f"hist_2: {hist_2.values()}")

    num = hist_1.values()
    denom = hist_2.values()
    
    #eff = np.where(denom != 0, num / denom, 0)
    #err = np.where(denom != 0, np.sqrt(eff * (1 - eff) / denom), 0)
    #I was still getting warnings with the above "safe" code, so f it:
    
    eff = num/denom
    err = np.sqrt(eff * (1 - eff)/ denom)
    
        
    return eff, err




def calc_effs(one_d_histograms, two_d_histograms):

    numerator_keys = ['bronze', 'silver', 'gold', 'gold_plus_silver']
    denom_key = 'blp'
    

    efficiencies = {  
    'one_d': {},    
    'two_d': {},  
    } 
    
    # 1D efficiencies here:
    for variable, hists in one_d_histograms.items():
        
        efficiencies['one_d'][variable] = {}
        
        for name, hist in hists.items():

            if name not in numerator_keys:
                continue
                
            #print(variable)
            #print(name)
            #print(hist)

            efficiencies['one_d'][variable][name] = (
            calc_eff_err(hist, one_d_histograms[variable][denom_key])
            )

    
    # 2D efficiencies here:
    for key, hists in two_d_histograms.items():
        
        efficiencies['two_d'][key] = {}
        
        for name, hist in hists.items():

            if name not in numerator_keys:
                continue
                
            #print(key)
            #print(name)
            #print(hist)

            efficiencies['two_d'][key][name] = (
            calc_eff_err(hist, two_d_histograms[key][denom_key])
            )
            
    return efficiencies







