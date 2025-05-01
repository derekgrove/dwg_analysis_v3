import awkward as ak
import hist.dask as dah
import numpy as np


# file works assuming skim_ele is of dictionary shape defined in the function skim_lpte_signal:


# from analysis_tools.skimming.lpte_skim import skim_lpte_signal
# skim_ele = skim_lpte_signal(ele)

from analysis_tools.skimming.lpte_skim import sip3D # Aprroximation for lpte



def get_variables(skim_ele):

    variables = { #should be whatever variables are needed for our eff calculations
        'pt': {},
        'eta': {},
        'ID': {},
        'miniIso': {},
        'SIP3D': {},
    } 
    
    
    for name, ele_col in skim_ele.items():
        #print(name)
        #print(ele_col)

        #ele_col = ele_col[(ele_col.pt >= 3) & (ele_col.pt < 8)]
        variables['pt'][name] = ak.flatten(ele_col.pt)
        variables['eta'][name] = ak.flatten(ele_col.eta)
        variables['ID'][name] = ak.flatten(ele_col.ID)
        variables['miniIso'][name] = ak.flatten(ele_col.miniPFRelIso_all)
        variables['SIP3D'][name] = ak.flatten(sip3D(ele_col))

        
        
        #can add more variables here, just be sure to modify above dictionary and following functions

    return variables



# use above function as first step in functions below:

def get_1d_pt_hist_lpte(ele_pt, name="default"):

    hist = dah.Hist.new.Regular(29, 1, 30, name=f"{name} lpte $p_T$").Double()

    hist.fill(ele_pt)
    
    return hist



def get_1d_eta_hist_lpte(ele_eta, name="default"):

    hist = dah.Hist.new.Regular(50, -2.5, 2.5, name=f"{name} lpte η").Double()
    
    hist.fill(ele_eta)
    
    return hist



def get_1d_ID_hist_lpte(ele_ID, name="default"):

    hist = dah.Hist.new.Regular(50, 0, 5, name=f"{name} lpte ID").Double()
    
    hist.fill(ele_ID)
    
    return hist



def get_1d_miniIso_hist_lpte(ele_miniIso, name="default"):

    hist = dah.Hist.new.Regular(50, 0, 5, name=f"{name} lpte miniIso").Double()
    
    hist.fill(ele_miniIso)
    
    return hist



def get_1d_sip3d_hist_lpte(ele_sip3d, name="default"):

    hist = dah.Hist.new.Regular(50, 0, 8, name=f"{name} lpte SIP3D").Double()
    
    hist.fill(ele_sip3d)
    
    return hist




def get_2d_eta_pt_hist_lpte(ele_pt, ele_eta, name="default"):

    
    eta_bins = [-2.5, -1.479, -0.8, 0, 0.8, 1.479, 2.5]
    pt_bins = [ 2, 3, 4, 5,
                6, 7, 8]
                #11, 12, 13, 14, 15,
                #16, 17, 18, 19, 20,
                #25, 30]
        #a lot of bins in pt, slice them later after the compute like:
        # hist[:, :10] → selects the first 10 bins in the second axis, i.e. pT
    
    hist = (
        dah.Hist.new
        .Variable(eta_bins, name="eta", label = "LowPtElectron η")
        .Variable(pt_bins, name="pt", label = "LowPtElectron $p_T$")
        .Double()
        )

    hist.fill(pt=ele_pt, eta=ele_eta)
    
    return hist



def get_2d_eta_ID_hist_lpte(ele_ID, ele_eta, name="default"):


    eta_bins = [-2.5, -1.479, -0.8, 0, 0.8, 1.479, 2.5]

    
    hist = (
        dah.Hist.new
        .Variable(eta_bins, name="eta", label = "LowPtElectron η")
        .Regular(40, 1, 5, name="ID", label = "LowPtElectron ID")
        .Double()
        )

    hist.fill(ID=ele_ID, eta=ele_eta)
    
    return hist

def get_2d_eta_miniIso_hist_lpte(ele_miniIso, ele_eta, name="default"):


    eta_bins = [-2.5, -1.479, -0.8, 0, 0.8, 1.479, 2.5]
                
        
    hist = (
        dah.Hist.new
        .Variable(eta_bins, name="eta", label = "LowPtElectron η")
        .Regular(50, 0, 5, name="miniIso", label = "LowPtElectron miniIso")
        .Double()
        )

    hist.fill(miniIso=ele_miniIso, eta=ele_eta)
    
    return hist



def get_2d_ID_pt_hist_lpte(ele_pt, ele_ID, name="default"):


    pt_bins = [ 1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
                11, 12, 13, 14, 15,
                16, 17, 18, 19, 20,
                25, 30]
        #a lot of bins in pt, slice them later after the compute like:
        # hist[:, :10] → selects the first 10 bins in the second axis, i.e. pT
    
    hist = (
        dah.Hist.new
        .Regular(100, 0, 10, name="ID", label = "LowPtElectron ID")
        .Variable(pt_bins, name="pt", label = "LowPtElectron $p_T$")
        .Double()
        )

    hist.fill(pt=ele_pt, ID=ele_ID)
    
    return hist


    
def get_2d_miniIso_pt_hist_lpte(ele_pt, ele_miniIso, name="default"):


    pt_bins = [ 1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
                11, 12, 13, 14, 15,
                16, 17, 18, 19, 20,
                25, 30]
        #a lot of bins in pt, slice them later after the compute like:
        # hist[:, :10] → selects the first 10 bins in the second axis, i.e. pT
    
    hist = (
        dah.Hist.new
        .Regular(20, 0, 4, name="miniIso", label = "Electron miniIso")
        .Variable(pt_bins, name="pt", label = "Electron $p_T$")
        .Double()
        )

    hist.fill(pt=ele_pt, miniIso=ele_miniIso)
    
    return hist



def get_2d_sip3D_pt_hist_lpte(ele_pt, ele_SIP3D, name="default"):


    pt_bins = [ 1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
                11, 12, 13, 14, 15,
                16, 17, 18, 19, 20,
                25, 30]
        #a lot of bins in pt, slice them later after the compute like:
        # hist[:, :10] → selects the first 10 bins in the second axis, i.e. pT
    
    hist = (
        dah.Hist.new
        .Regular(80, 0, 8, name="sip3d", label = "Electron SIP3D")
        .Variable(pt_bins, name="pt", label = "Electron $p_T$")
        .Double()
        )

    hist.fill(pt=ele_pt, sip3d=ele_SIP3D)
    
    return hist






def get_hists_lpte(skim_ele):
    
    variables = get_variables(skim_ele)
    skim_names = variables['pt'].keys()

    
    histograms = {
        
    'one_d': {
        'pt': {},
        'eta': {},
        'ID': {},
        'miniIso': {},
        'SIP3D': {},
    },
        
    'two_d': {
        'pt_eta': {},
        'pt_ID': {},
        'pt_miniIso': {},
        'pt_SIP3D': {},
        'eta_ID': {},
        'eta_miniIso': {},
        
    },
        
    }
    
    for name in skim_names:
    
        ele_pt = variables['pt'][name]
        ele_eta = variables['eta'][name]
        ele_ID = variables['ID'][name]
        ele_miniIso = variables['miniIso'][name]
        ele_SIP3D = variables['SIP3D'][name]
        
        histograms['one_d']['pt'][name] = get_1d_pt_hist_lpte(ele_pt, name)
        histograms['one_d']['eta'][name] = get_1d_eta_hist_lpte(ele_eta, name)
        histograms['one_d']['ID'][name] = get_1d_ID_hist_lpte(ele_ID, name)
        histograms['one_d']['miniIso'][name] = get_1d_ID_hist_lpte(ele_miniIso, name)
        histograms['one_d']['SIP3D'][name] = get_1d_ID_hist_lpte(ele_SIP3D, name)
        histograms['two_d']['pt_eta'][name] = get_2d_eta_pt_hist_lpte(ele_pt, ele_eta, name)
        histograms['two_d']['pt_ID'][name] = get_2d_ID_pt_hist_lpte(ele_pt, ele_ID, name)
        histograms['two_d']['pt_miniIso'][name] = get_2d_miniIso_pt_hist_lpte(ele_pt, ele_miniIso, name)
        histograms['two_d']['pt_SIP3D'][name] = get_2d_sip3D_pt_hist_lpte(ele_pt, ele_SIP3D, name)
        histograms['two_d']['eta_ID'][name] = get_2d_eta_ID_hist_lpte(ele_ID, ele_eta, name)
        histograms['two_d']['eta_miniIso'][name] = get_2d_eta_miniIso_hist_lpte(ele_miniIso, ele_eta, name)
    
    
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

    numerator_keys = ['bronze', 'silver', 'gold']
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

    

def yield_plot(hist_signal, hist_fakes): # This does the same thing as calc_eff_err() above, just in two lines.

    h_yield = h_signal.copy()  # Creating a histogram that has identical binning schemes
    # now replace those bins with the calculated yield below:
    h_yield.view()[:] = h_signal.view() / h_fakes.view() # Directly calculation the results using the numpy view of the histograms and passing it into h_eff
    

    return h_yield





