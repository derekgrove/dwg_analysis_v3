# So, this is a coffea analysis framework.

## To setup dependencies (FIRST STEP) I recommend doing what I did:

install miniforge3 to get mamba, lookup how to do that online.

Once you have mamba:

`mamba create -n dwg_analysis python=3.12`

`mamba activate dwg_analysis`

`mamba install pip` (probably already installed)

`pip install coffea` This should grab the required dependencies, we'll see. Check the version you got like:

`pip show coffea` And I got this version:

```
Name: coffea
Version: 2025.3.0
Summary: Basic tools and wrappers for enabling not-too-alien syntax when running columnar Collider HEP analysis.
Home-page: https://github.com/coffeateam/coffea
Author: 
Author-email: Lindsey Gray <lagray@fnal.gov>, Nick Smith <ncsmith@fnal.gov>
License: BSD-3-Clause
Location: /Users/derekgrove/miniforge3/envs/dwg_analysis/lib/python3.12/site-packages
Requires: aiohttp, awkward, cachetools, cloudpickle, correctionlib, dask, dask-awkward, dask-histogram, fsspec-xrootd, hist, lz4, matplotlib, mplhep, numba, numpy, packaging, pandas, pyarrow, requests, scipy, toml, tqdm, uproot, vector
Required-by:
```

`mamba install dask distributed`

`mamba install xrootd`

