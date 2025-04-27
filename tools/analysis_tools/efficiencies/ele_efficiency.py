import awkward as ak
import hist.dask as dah
import numpy as np


# file works assuming skim_ele is of dictionary shape defined in the function skim_ele_signal:


# from analysis_tools.skimming.ele_skim_v3 import skim_ele_signal
# skim_ele = skim_ele_signal(ele)





def get_variables(skim_ele):

    variables = { #should be whatever variables are needed for our eff calculations
        'pts': {},
        'eta': {},
    } 
    
    
    for name, ele_col in skim_ele.items():
        #print(name)
        #print(ele_col)
        variables['pts'][name] = ak.flatten(ele_col.pt)
        variables['eta'][name] = ak.flatten(ele_col.eta)
        
        #can add more variables here, just be sure to modify above dictionary and following functions

    return variables



#use above function as first step in functions below:

def get_1d_pt_hist(ele_pt, name="default"):

    hist = dah.Hist.new.Regular(95, 5, 100, name=f"{name} electron $p_T$").Double()

    hist.fill(ele_pt)
    
    return hist


    
def get_1d_eta_hist(ele_eta, name="default"):

    hist = dah.Hist.new.Regular(50, -2.5, 2.5, name=f"{name} electron η").Double()
    
    hist.fill(ele_eta)
    
    return hist


    
    
def get_2d_eta_pt_hist(ele_pt, ele_eta, name="default"):


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
        .Variable(eta_bins, name="eta", label = "Electron η")
        .Variable(pt_bins, name="pt", label = "Electron $p_T$")
        .Double()
        )

    hist.fill(pt=ele_pt, eta=ele_eta)
    
    return hist


    

def get_hists(skim_ele):
    
    variables = get_variables(skim_ele)
    
    histograms = {
        
    'one_d': {
        'pt': {},
        'eta': {},
    },
        
    'two_d': {
        'pt_eta' : {}
    },
        
    }
    
    for name, ele_pts in variables['pts'].items():
    
        ele_eta = variables['eta'][name] 
        
        histograms['one_d']['pt'][name] = get_1d_pt_hist(ele_pts, name)
        histograms['one_d']['eta'][name] = get_1d_eta_hist(ele_eta, name)
        histograms['two_d']['pt_eta'][name] = get_2d_eta_pt_hist(ele_pts, ele_eta, name)
    
    
    
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







