import awkward as ak
import numpy as np
import hist.dask as dah

# This file should be used to define in-house functions for making various histograms in coffea


# for particle objects (Jets, Electrons, LowPtElectrons, Muons):

#"attribute" is like the variable of the object we'd like to plot, for example Electron.pt, pt is the "attribute", Electron is the "object"


def make_1d_hist(obj, attribute, binning, label="axis_label", abs_val = False):

    if len(binning) != 3:
        raise ValueError("binning must be a list or tuple with exactly 3 values: [bins, start, stop]")

    bins, start, stop = binning
    
    hist = dah.Hist.new.Regular(bins, start, stop, name=label).Double()
    #since obj is a Class (?) have to use getattr python function to access the variable we're interested in
    values = getattr(obj, attribute)
    if abs_val:
        values = np.abs(values)
        print(f"abs val of {attribute} calculated")
    hist.fill(ak.flatten(values))

    return hist

#histograms need to be same binning I think

def make_1d_ratio(hist_num, hist_denom, label="axis_label"):

    hist = dah.Hist.new.Ratio(bins, start, stop, name=label).Double()
    #since obj is a Class (?) have to use getattr python function to access the variable we're interested in
    values = getattr(obj, attribute)
    if abs_val:
        values = np.abs(values)
        print(f"abs val of {attribute} calculated")
    hist.fill(ak.flatten(values))

    return hist


    
def make_1d_hist_variable(obj, attribute, binning, label="axis_label", abs_val = False):

    #This is for making a histogram with explicit binning, ex. [0, 0.8, 1.479, 2.5], give it a list of the explicit bins you want

    
        
    hist = dah.Hist.new.Variable(binning, name=label).Double()
    values = getattr(obj, attribute)
    if abs_val:
        values = np.abs(values)
        print(f"abs val of {attribute} calculated")
    hist.fill(ak.flatten(values))

    return hist


def make_2d_hist(obj, attribute_a, binning_a, attribute_b, binning_b, label_a="axis_label_a", label_b="axis_label_b"):


    bins_a, start_a, stop_a = binning_a
    bins_b, start_b, stop_b = binning_b
    
    hist = (
        dah.Hist.new
        .Regular(bins_a, start_a, stop_a, name=label_a)
        .Regular(bins_b, start_b, stop_b, name=label_b)
        .Double()
        )
    
    #since obj is a Class (?) have to use getattr python function to access the variable we're interested in
    values_a = getattr(obj, attribute_a)
    values_b = getattr(obj, attribute_b)
    
    #hist.fill(label_a= ak.flatten(values_a), label_b= ak.flatten(values_b))
    hist.fill(**{label_a: ak.flatten(values_a), label_b: ak.flatten(values_b)})
    return hist

    
"""
def make_electron_histograms(ele_obj, label="default"):
    """
"""
    Creates and fills histograms for an electron collection.

    Parameters:
    - ele_obj: Awkward Array of electrons
    - label: String label for the histograms (default="filtered")

    Returns:
    - Dictionary of histograms containing:
      - pT histogram
      - eta histogram
      - 2D histograms for pT vs miniISO, pT vs pfRelIso, and pT vs sip3D
    """

"""
    # Define histograms
    histograms = {
        f"{label}_pt": dah.Hist.new.Regular(100, 0, 50, name="pT", underflow=False, overflow=False).Double(),
        f"{label}_eta": dah.Hist.new.Regular(100, -3, 3, name="eta").Double(),
        f"{label}_pt_vs_mini_iso": (
            dah.Hist.new
            .Regular(100, 5, 30, name="pT")
            .Regular(100, 0, 10, name="mini_iso_pt")
            .Double()
        ),
        f"{label}_pt_vs_pfrel_iso": (
            dah.Hist.new
            .Regular(100, 5, 30, name="pT")
            .Regular(100, 0, 10, name="pfrel_iso_pt")
            .Double()
        ),
        f"{label}_pt_vs_sip3d": (
            dah.Hist.new
            .Regular(100, 5, 30, name="pT")
            .Regular(100, 0, 9, name="sip3D")
            .Double()
        ),
    }

    # Fill histograms
    histograms[f"{label}_pt"].fill(pT=ak.flatten(ele_obj.pt))
    histograms[f"{label}_eta"].fill(eta=ak.flatten(ele_obj.eta))
    histograms[f"{label}_pt_vs_mini_iso"].fill(
        pT=ak.flatten(ele_obj.pt), mini_iso_pt=ak.flatten(ele_obj.miniPFRelIso_all*ele_obj.pt)
    )
    histograms[f"{label}_pt_vs_pfrel_iso"].fill(
        pT=ak.flatten(ele_obj.pt), pfrel_iso_pt=ak.flatten(ele_obj.pfRelIso03_all*ele_obj.pt)
    )
    histograms[f"{label}_pt_vs_sip3d"].fill(
        pT=ak.flatten(ele_obj.pt), sip3D=ak.flatten(ele_obj.sip3d)
    )

    return histograms
          """