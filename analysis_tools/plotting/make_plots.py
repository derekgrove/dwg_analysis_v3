import matplotlib.pyplot as plt
import mplhep
import hist
from hist import Hist
import numpy as np

def bug_call():

    #have to call this a second time to get proper scaling, a known bug
    
    mplhep.style.use(mplhep.style.CMS)
    plt.figure()
    mplhep.style.use(mplhep.style.CMS)

def plot_1d_hist(hist_obj, name, output_folder = "1d_plots", filename="test_1d_plot.png", save = False):
    
    y_min, y_max = 1, 1e5
    
    #output_folder = "1d_plots"
    os.makedirs(output_folder, exist_ok=True)
    
    plt.figure()
    mplhep.style.use(mplhep.style.CMS)
    plt.subplots(figsize=(6, 6))
    plt.title(name, fontsize=20, pad=22)
    plt.yscale("log")
    plt.ylabel("Counts")
    plt.ylim(y_min, y_max)
    
    mplhep.cms.label(loc=0, fontsize=14)
    values = hist_obj.values()
    total_counts = hist_obj.values().sum()
    #print(total_counts)
    overflow = hist_obj.values(flow=True).sum()
    #print(overflow)
    delta = overflow - total_counts
    plt.text(
        0.95, 0.95,  # Position in figure coordinates (near top-right)
        f"Total Counts: {int(total_counts)}",  # Format text
        fontsize=14,
        color="black",
        verticalalignment="top",
        horizontalalignment="right",
        transform=plt.gca().transAxes,
        bbox=dict(facecolor='white', alpha=0.7) # Ensures placement in figure coordinates
    )
    plt.text(
        0.95, 0.87,  # Position in figure coordinates (near top-right)
        f"Flow: {int(delta)}",  # Format text
        fontsize=14,
        color="black",
        verticalalignment="top",
        horizontalalignment="right",
        transform=plt.gca().transAxes,
        bbox=dict(facecolor='white', alpha=0.7) # Ensures placement in figure coordinates
    )
    
    hist_obj.plot1d()

    
    save_path = os.path.join(output_folder, filename)
    if save:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()



def plot_2d_hist(hist_obj, name, output_folder = "test_2d_plots", filename="test_2d_plot.png", save = False):
    
    color_min, color_max = 1, 1e3

    #output_folder = "2d_plots"
    os.makedirs(output_folder, exist_ok=True)
    
    plt.figure()
    mplhep.style.use(mplhep.style.CMS)
    plt.subplots(figsize=(6, 6))
    plt.title(name, fontsize=20, pad=22)
    
    mplhep.cms.label(loc=0, fontsize=14)
    values = hist_obj.values()
    total_counts = hist_obj.values().sum()
    #print(total_counts)
    overflow = hist_obj.values(flow=True).sum()
    #print(overflow)
    delta = overflow - total_counts
    plt.text(
        0.95, 0.95,  # Position in figure coordinates (near top-right)
        f"Total Counts: {int(total_counts)}",  # Format text
        fontsize=14,
        color="black",
        verticalalignment="top",
        horizontalalignment="right",
        transform=plt.gca().transAxes,
        bbox=dict(facecolor='white', alpha=0.7) # Ensures placement in figure coordinates
    )
    plt.text(
        0.95, 0.87,  # Position in figure coordinates (near top-right)
        f"Overflow: {int(delta)}",  # Format text
        fontsize=14,
        color="black",
        verticalalignment="top",
        horizontalalignment="right",
        transform=plt.gca().transAxes,
        bbox=dict(facecolor='white', alpha=0.7) # Ensures placement in figure coordinates
    )
    
    hist_obj.plot2d(norm=colors.LogNorm(vmin=color_min, vmax=color_max))

    
    save_path = os.path.join(output_folder, filename)
    if save:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()



#1d eff plot here, use ratio plot from hist for plot generation in make_hist file


    
def make_2d_eff_plot(h_num, h_denom, num_name, denom_name, output_folder="test_2d_eff_plots", filename="test_2d_eff_plot.png", save = False):

    h_eff = h_num.copy()  # Copy histogram structure
    h_eff.view()[:] = h_num.view() / h_denom.view()

    #output_folder = "2d_eff_plots"
    os.makedirs(output_folder, exist_ok=True)

    plt.figure()
    mplhep.style.use(mplhep.style.CMS)
    plt.subplots(figsize=(6, 6))

    # Set title with histogram names
    plt.title(f"{num_name} / {denom_name} Eff. ", fontsize=20, pad=22)

    mplhep.cms.label(loc=0, fontsize=14)

    num_count = h_num.values().sum()
    denom_count = h_denom.values().sum()
    
    delta = denom_count - num_count

    percent = (1 - delta/denom_count)*100
    

    plt.text(
        0.95, 0.95,  
        fr"% removed: {percent:.2f}",  
        fontsize=14,
        color="black",
        verticalalignment="top",
        horizontalalignment="right",
        transform=plt.gca().transAxes,
        bbox=dict(facecolor='white', alpha=0.7)  
    )

    h_eff.plot2d(cmin=color_min, cmax=color_max)

    save_path = os.path.join(output_folder, filename)
    if save:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()
 
