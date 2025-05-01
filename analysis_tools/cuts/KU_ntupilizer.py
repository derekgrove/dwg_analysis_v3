from analysis_tools.cuts import skim_ele, skim_muon, skim_lpte, skim_events
import awkward as ak

def make_ntuple(events=None, ele=None, muon=None, lpte=None):

    dataset = events.metadata["dataset"] if hasattr(events, "metadata") else "unknown"

    total_entries = ak.num(events, axis=0)
    total_ele = ak.sum(ak.num(ele))
    total_lpte = ak.sum(ak.num(lpte))
    total_mu = ak.sum(ak.num(muon))

    #my_events = skim_events(events)
    my_electrons = skim_ele(ele)
    my_muons = skim_muon(muon)
    my_lptes = skim_lpte(lpte)

    ntuple = {
        "num_tot_Events": total_entries,
        "num_tot_ele": total_ele,
        "num_tot_lpte": total_lpte,
        "num_tot_mu": total_mu,
        "dataset": dataset,
        #"Event": my_events,
        "Electron": my_electrons,
        "Muon": my_muons,
        "LowPtElectron": my_lptes,
        }

    return ntuple