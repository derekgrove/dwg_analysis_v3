# So, this is a coffea analysis framework.

## My general workflow is something like this:

### Write all tools in python files (skims for particle objects in NanoAOD, plotting functions, caculations, etc.)

### Import tools into a processor file, this file runs over each slice of a root file. It "does the analysis".

### Import processor into a jupyter notebook, run it here. The output is a dictionary filled with whatever calculations/objects the processor returns, so histograms or lists or whatever else.

The bottom of the notebook (after the processor has ran) is where you should access and play with these things, either displaying counts/plots or whatever.

Can run multiple processors in a notebook, so could run one on signal, one on background, etc.
