from pathlib import Path

#ChatGPT gave me this, I just want to simplify paths to my .json


# This is the directory where this file lives (i.e., analysis_tools/)
PACKAGE_DIR = Path(__file__).resolve().parent

# This assumes your project root is one level up (e.g., dwg_analysis_v3/)
REPO_ROOT = PACKAGE_DIR.parent

# Optional: helper function to get paths within the repo
def get_config_path(filename):
    return REPO_ROOT / "config" / filename
